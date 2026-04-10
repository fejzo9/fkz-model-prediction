# Dataset Specification

## Goal

Build one canonical tabular dataset where each row represents one played match.

This dataset is the source of truth for:

- processed tables
- feature engineering
- train/validation/test splits
- baseline and advanced models

## Canonical Raw File

Use:

- `data/raw/matches_source.csv`

Keep this file as the main manually maintained source until collection is automated.

In the current repository state, this file is also the target written by:

- `scripts/scrape_nfsbih.py`

That makes the CSV the merge point between automated scraping and manual cleanup.

## Row Definition

One row = one match from FK Zeljeznicar's perspective.

That means:

- `team` is usually `FK Zeljeznicar`
- `opponent` is the opposing club
- `venue` is `home` or `away`
- `goals_for` and `goals_against` are recorded from `team` perspective

Later, when the project expands to the full league, the same schema can be reused for every team.

## Required Columns

### Identity and competition

- `season`: season label, for example `2024/2025`
- `competititon`: competition label kept as-is for backward compatibility with the current codebase
- `round`: league round as an integer
- `match_date`: match date in ISO format `YYYY-MM-DD`
- `match_id`: unique match identifier, recommended format `BIH-2024-2025-001`

### Match context

- `team`: team being modeled, for now `FK Zeljeznicar`
- `opponent`: opposing club name
- `venue`: `home` or `away`
- `coach`: head coach of `team` at kickoff

### Match outcome

- `goals_for`: goals scored by `team`
- `goals_against`: goals conceded by `team`
- `result`: `W`, `D`, or `L`
- `points_earned`: `3`, `1`, or `0`

### Table state after the match

- `points_total_after`: total league points after the match
- `table_position_after`: league position after the match

### Metadata

- `notes`: optional free-text note for postponed matches, coach changes, stadium issues, or uncertainty in data

## Allowed Values

- `venue`: only `home` or `away`
- `result`: only `W`, `D`, or `L`
- `round`: positive integer
- `goals_for`, `goals_against`: non-negative integers
- `points_earned`: only `0`, `1`, or `3`
- `match_date`: ISO date string

## Collection Rules

1. Enter only played matches.
2. Keep postponed or cancelled matches out of the main table until a real date exists.
3. Standardize team names and never mix aliases in the same file.
4. Enter final score only, not halftime score.
5. Record table position and total points after the match, not before it.
6. If one field is uncertain, leave a note in `notes` instead of guessing silently.

## Automation Notes

Current automation uses official NFSBiH team stats pages.

What the current scraper does:

- reads the visible `Results round N` table
- extracts the target team's played match
- reads visible standings to fill `points_total_after` and `table_position_after`
- merges rows into the canonical CSV using `match_id`

What it does not do yet:

- iterate every historical round automatically
- recover coach names automatically
- crawl every competition option on the site end-to-end

For operational details, see `docs/scraping.md`.

## Recommended Collection Order

1. Fill FK Zeljeznicar league matches for `2024/2025`.
2. Backfill `2023/2024` and `2022/2023`.
3. Extend to `2021/2022` and `2020/2021`.
4. Only after FK Zeljeznicar is complete, expand to other teams if needed for a league-wide model.

## Minimum Viable Dataset

Before model training starts, the dataset should contain at least:

- 3 complete seasons
- no missing `team`, `opponent`, `venue`, `goals_for`, `goals_against`, `result`
- unique `match_id` for every row
- verified dates

## Example Row

```csv
season,competititon,round,match_date,match_id,team,opponent,venue,goals_for,goals_against,result,points_earned,points_total_after,table_position_after,coach,notes
2024/2025,WWIN Liga BiH,1,2024-08-03,BIH-2024-2025-001,FK Zeljeznicar,FK Sarajevo,home,2,1,W,3,3,4,Denis Curic,
```
