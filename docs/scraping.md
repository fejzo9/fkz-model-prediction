# Scraping Workflow

## Scope

The first scraper targets official NFSBiH team stats pages and converts the currently visible results round into the canonical CSV format.

Current implementation:

- fetches one or more NFSBiH team stats URLs
- parses the visible `Results round N` table
- extracts the target team's played match in that round
- reads the visible standings table for `points_total_after` and `table_position_after`
- merges rows into `data/raw/matches_source.csv` by `match_id`

## Script

Use:

```powershell
python scripts/scrape_nfsbih.py
```

Optional examples:

```powershell
python scripts/scrape_nfsbih.py `
  --url https://www.nfsbih.ba/en/stats/team/7856146/411/ `
  --team-name "FK Zeljeznicar"
```

```powershell
python scripts/scrape_nfsbih.py `
  --urls-file data/raw/source_urls.txt `
  --coach "Denis Curic" `
  --notes "official nfsbih scrape"
```

## Source URL File

`data/raw/source_urls.txt` should contain one URL per line.

Example:

```text
https://www.nfsbih.ba/en/stats/team/7856146/411/
```

Blank lines and lines starting with `#` are ignored.

## Current Limitation

The current script scrapes the round that is visible on the supplied page.

That means:

- it is useful immediately for automated population of current or selected round pages
- it is not yet a full historical crawler for every round of every season from a single URL

The likely next extension is to reverse-engineer the NFSBiH `com_ajax` endpoint so the scraper can iterate competition and round selectors automatically.

## Recommended Use Now

1. Keep using official NFSBiH URLs as the primary source.
2. Scrape what is available automatically into the canonical CSV.
3. Review the merged rows.
4. Extend the scraper to historical rounds once the hidden endpoint parameters are confirmed.
