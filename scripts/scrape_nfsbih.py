from __future__ import annotations

import argparse
import csv
import re
import sys
import unicodedata
from dataclasses import dataclass
from datetime import datetime
from html import unescape
from pathlib import Path
from typing import Iterable
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup, Tag


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from fkz_model_prediction.validation import REQUIRED_COLUMNS


DEFAULT_OUTPUT = PROJECT_ROOT / "data" / "raw" / "matches_source.csv"
DEFAULT_URLS_FILE = PROJECT_ROOT / "data" / "raw" / "source_urls.txt"
DEFAULT_TEAM_NAME = "FK Zeljeznicar"
DEFAULT_TIMEOUT = 30


@dataclass
class MatchRecord:
    season: str
    competititon: str
    round: int
    match_date: str
    match_id: str
    team: str
    opponent: str
    venue: str
    goals_for: int
    goals_against: int
    result: str
    points_earned: int
    points_total_after: int | None
    table_position_after: int | None
    coach: str
    notes: str

    def to_row(self) -> dict[str, str]:
        row = {
            "season": self.season,
            "competititon": self.competititon,
            "round": str(self.round),
            "match_date": self.match_date,
            "match_id": self.match_id,
            "team": self.team,
            "opponent": self.opponent,
            "venue": self.venue,
            "goals_for": str(self.goals_for),
            "goals_against": str(self.goals_against),
            "result": self.result,
            "points_earned": str(self.points_earned),
            "points_total_after": "" if self.points_total_after is None else str(self.points_total_after),
            "table_position_after": "" if self.table_position_after is None else str(self.table_position_after),
            "coach": self.coach,
            "notes": self.notes,
        }
        return row


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Scrape currently visible NFSBiH team results into the canonical CSV dataset."
    )
    parser.add_argument(
        "--url",
        action="append",
        default=[],
        help="One NFSBiH team stats URL to scrape. May be provided multiple times.",
    )
    parser.add_argument(
        "--urls-file",
        default=str(DEFAULT_URLS_FILE),
        help="Text file containing one NFSBiH team stats URL per line.",
    )
    parser.add_argument(
        "--output",
        default=str(DEFAULT_OUTPUT),
        help="Path to the canonical CSV output file.",
    )
    parser.add_argument(
        "--team-name",
        default=DEFAULT_TEAM_NAME,
        help="Target team name used to determine perspective, venue, and outcome.",
    )
    parser.add_argument(
        "--coach",
        default="",
        help="Optional coach value to write for scraped rows.",
    )
    parser.add_argument(
        "--notes",
        default="",
        help="Optional note to append to every scraped row.",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=DEFAULT_TIMEOUT,
        help="HTTP timeout in seconds.",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite existing rows instead of merging on match_id.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    urls = collect_urls(args.url, Path(args.urls_file))
    if not urls:
        raise SystemExit("No URLs were provided. Use --url or populate data/raw/source_urls.txt.")

    scraped_rows: list[dict[str, str]] = []
    for url in urls:
        html = fetch_html(url, timeout=args.timeout)
        records = parse_team_page(
            html=html,
            page_url=url,
            target_team=args.team_name,
            coach=args.coach,
            notes=args.notes,
        )
        scraped_rows.extend(record.to_row() for record in records)

    output_path = Path(args.output)
    final_rows = merge_rows(
        existing_rows=[] if args.overwrite else read_existing_rows(output_path),
        new_rows=scraped_rows,
    )
    write_rows(output_path, final_rows)

    print(f"Fetched URLs:      {len(urls)}")
    print(f"Scraped matches:   {len(scraped_rows)}")
    print(f"Written rows:      {len(final_rows)}")
    print(f"Output CSV:        {output_path}")
    return 0


def collect_urls(cli_urls: list[str], urls_file: Path) -> list[str]:
    urls: list[str] = [url.strip() for url in cli_urls if url.strip()]
    if urls_file.exists():
        file_urls = []
        for line in urls_file.read_text(encoding="utf-8").splitlines():
            stripped = line.strip()
            if not stripped or stripped.startswith("#"):
                continue
            file_urls.append(stripped)
        urls.extend(file_urls)

    deduped: list[str] = []
    seen: set[str] = set()
    for url in urls:
        if url not in seen:
            deduped.append(url)
            seen.add(url)
    return deduped


def fetch_html(url: str, timeout: int) -> str:
    response = requests.get(
        url,
        timeout=timeout,
        headers={
            "User-Agent": (
                "fkz-model-prediction/0.1 "
                "(research scraper; contact repository owner if there is a problem)"
            )
        },
    )
    response.raise_for_status()
    return response.text


def parse_team_page(
    html: str,
    page_url: str,
    target_team: str,
    coach: str,
    notes: str,
) -> list[MatchRecord]:
    soup = BeautifulSoup(html, "html.parser")

    results_round = extract_results_round(soup)
    competition_label = extract_competition_label(soup)
    season = infer_season(competition_label, page_url)
    standings = extract_standings(soup)

    results_div = soup.find("div", id="rezultati")
    if not isinstance(results_div, Tag):
        raise ValueError(f"Could not find the results table in {page_url}")

    table = results_div.find("table")
    if not isinstance(table, Tag):
        raise ValueError(f"Could not find the results table markup in {page_url}")

    normalized_target = normalize_name(target_team)
    current_date: str | None = None
    records: list[MatchRecord] = []

    for row in table.find_all("tr"):
        cells = row.find_all("td")
        if not cells:
            continue

        if len(cells) == 1 and cells[0].has_attr("colspan"):
            date_text = clean_text(cells[0].get_text(" ", strip=True))
            if not date_text:
                continue
            current_date = parse_match_datetime(date_text)
            continue

        if len(cells) < 5 or current_date is None:
            continue

        host = clean_text(cells[0].get_text(" ", strip=True))
        score = clean_text(cells[2].get_text(" ", strip=True))
        guest = clean_text(cells[4].get_text(" ", strip=True))

        if " : " not in score:
            continue

        match_id = extract_match_id(row, page_url, season, results_round, host, guest, current_date)

        host_goals, guest_goals = parse_score(score)
        if normalize_name(host) == normalized_target:
            venue = "home"
            opponent = guest
            goals_for = host_goals
            goals_against = guest_goals
        elif normalize_name(guest) == normalized_target:
            venue = "away"
            opponent = host
            goals_for = guest_goals
            goals_against = host_goals
        else:
            continue

        standing_after = standings.get(normalized_target, {})
        result = compute_result(goals_for, goals_against)
        points_earned = compute_points(result)
        row_notes = build_notes(page_url, notes)

        records.append(
            MatchRecord(
                season=season,
                competititon=competition_label,
                round=results_round,
                match_date=current_date,
                match_id=match_id,
                team=stable_team_name(host if venue == "home" else guest),
                opponent=stable_team_name(opponent),
                venue=venue,
                goals_for=goals_for,
                goals_against=goals_against,
                result=result,
                points_earned=points_earned,
                points_total_after=standing_after.get("points"),
                table_position_after=standing_after.get("position"),
                coach=coach,
                notes=row_notes,
            )
        )

    return records


def extract_results_round(soup: BeautifulSoup) -> int:
    tabs = soup.select("ul.mini_tab li a")
    for tab in tabs:
        text = clean_text(tab.get_text(" ", strip=True))
        match = re.search(r"Results round\s+(\d+)", text, re.IGNORECASE)
        if match:
            return int(match.group(1))
        match = re.search(r"Rezultati\s+(\d+)\.\s*kola", text, re.IGNORECASE)
        if match:
            return int(match.group(1))
    raise ValueError("Could not determine the active results round.")


def extract_competition_label(soup: BeautifulSoup) -> str:
    select = soup.select_one("#table-competition select")
    if isinstance(select, Tag):
        options = select.find_all("option")
        if options:
            return clean_text(options[0].get_text(" ", strip=True))
    return "WWIN Liga BiH"


def infer_season(competition_label: str, page_url: str) -> str:
    match = re.search(r"(\d{2})\s*/\s*(\d{2})", competition_label)
    if match:
        start = int(match.group(1))
        end = int(match.group(2))
        start_year = 2000 + start
        end_year = 2000 + end
        return f"{start_year}/{end_year}"

    match = re.search(r"(\d{2})-(\d{2})", page_url)
    if match:
        start = 2000 + int(match.group(1))
        end = 2000 + int(match.group(2))
        return f"{start}/{end}"

    return ""


def extract_standings(soup: BeautifulSoup) -> dict[str, dict[str, int]]:
    standings_div = soup.find("div", id="tabela")
    if not isinstance(standings_div, Tag):
        return {}

    table = standings_div.find("table")
    if not isinstance(table, Tag):
        return {}

    standings: dict[str, dict[str, int]] = {}
    for row in table.find_all("tr"):
        cells = row.find_all("td")
        if len(cells) < 7:
            continue

        try:
            position = int(clean_text(cells[0].get_text(" ", strip=True)))
            points = int(clean_text(cells[6].get_text(" ", strip=True)))
        except ValueError:
            continue

        team_name = clean_text(cells[1].get_text(" ", strip=True))
        standings[normalize_name(team_name)] = {
            "position": position,
            "points": points,
        }

    return standings


def parse_match_datetime(raw_value: str) -> str:
    cleaned = clean_text(raw_value).rstrip(".")
    parsed = datetime.strptime(cleaned, "%d.%m.%Y. %H:%M")
    return parsed.date().isoformat()


def parse_score(raw_score: str) -> tuple[int, int]:
    match = re.search(r"(\d+)\s*:\s*(\d+)", raw_score)
    if not match:
        raise ValueError(f"Invalid score string: {raw_score}")
    return int(match.group(1)), int(match.group(2))


def extract_match_id(
    row: Tag,
    page_url: str,
    season: str,
    round_number: int,
    host: str,
    guest: str,
    match_date: str,
) -> str:
    link = row.find("a", href=True)
    if isinstance(link, Tag):
        href = link["href"]
        match = re.search(r"/stats/match/(\d+)", href)
        if match:
            return match.group(1)

    fallback = f"{season}-{round_number}-{match_date}-{normalize_name(host)}-{normalize_name(guest)}"
    fallback = re.sub(r"[^a-z0-9-]+", "-", fallback.lower()).strip("-")
    return fallback or urljoin(page_url, "#match")


def compute_result(goals_for: int, goals_against: int) -> str:
    if goals_for > goals_against:
        return "W"
    if goals_for < goals_against:
        return "L"
    return "D"


def compute_points(result: str) -> int:
    return {"W": 3, "D": 1, "L": 0}[result]


def build_notes(page_url: str, extra_notes: str) -> str:
    parts = [part for part in [extra_notes.strip(), f"source={page_url}"] if part]
    return " | ".join(parts)


def canonical_team_name(name: str) -> str:
    cleaned = clean_text(name)
    replacements = {
        "FK ŽELJEZNIČAR": "FK Zeljeznicar",
        "FK ŽELJEZNICAR": "FK Zeljeznicar",
    }
    return replacements.get(cleaned.upper(), cleaned)


def clean_text(value: str) -> str:
    text = unescape(value).replace("\xa0", " ")
    return re.sub(r"\s+", " ", text).strip()


def normalize_name(value: str) -> str:
    ascii_value = (
        unicodedata.normalize("NFKD", clean_text(value))
        .encode("ascii", "ignore")
        .decode("ascii")
        .lower()
    )
    return re.sub(r"[^a-z0-9]+", " ", ascii_value).strip()


def stable_team_name(value: str) -> str:
    cleaned = clean_text(value)
    if normalize_name(cleaned) == "fk zeljeznicar":
        return "FK Zeljeznicar"
    return cleaned


def read_existing_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []

    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        return [normalize_existing_row(row) for row in reader]


def normalize_existing_row(row: dict[str, str]) -> dict[str, str]:
    normalized = {column: row.get(column, "") for column in REQUIRED_COLUMNS}
    return normalized


def merge_rows(
    existing_rows: Iterable[dict[str, str]],
    new_rows: Iterable[dict[str, str]],
) -> list[dict[str, str]]:
    merged: dict[str, dict[str, str]] = {}

    def row_key(row: dict[str, str]) -> str:
        if row.get("match_id"):
            return f"match_id:{row['match_id']}"
        fallback_parts = [row.get("season", ""), row.get("round", ""), row.get("team", ""), row.get("opponent", "")]
        return "|".join(fallback_parts)

    for row in existing_rows:
        merged[row_key(row)] = row

    for row in new_rows:
        merged[row_key(row)] = row

    ordered_rows = sorted(
        merged.values(),
        key=lambda row: (
            row.get("season", ""),
            safe_int(row.get("round", "")),
            row.get("match_date", ""),
            row.get("match_id", ""),
        ),
    )
    return ordered_rows


def safe_int(value: str) -> int:
    try:
        return int(float(value))
    except (TypeError, ValueError):
        return 0


def write_rows(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=REQUIRED_COLUMNS)
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    raise SystemExit(main())
