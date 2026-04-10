# Status Report

## Date

2026-04-10

## Current Project Phase

The project is now in the first practical data-acquisition phase.

The repository is no longer only a scaffold for manual Excel cleanup. It now has:

- a canonical raw CSV dataset
- a documented dataset schema
- a first official-source scraper for NFSBiH team stats pages
- an ingestion pipeline that reads CSV or Excel inputs

## What Was Added

### 1. Canonical raw dataset

The main raw input is now:

- `data/raw/matches_source.csv`

This replaces the old spreadsheet template as the preferred source of truth for match rows.

### 2. Dataset specification

A dedicated schema document was added:

- `docs/dataset-spec.md`

It defines:

- one row = one played match
- required columns
- allowed values
- collection rules
- minimum viable dataset criteria

### 3. First automated scraper

A first scraper was added:

- `scripts/scrape_nfsbih.py`

It currently:

- fetches one or more NFSBiH team stats URLs
- parses the visible results round
- extracts FK Zeljeznicar's match row from that round
- reads visible standings
- merges rows into the canonical CSV by `match_id`

### 4. First end-to-end scraper run

The scraper was executed successfully against the URL stored in:

- `data/raw/source_urls.txt`

Execution result:

- 1 URL fetched
- 1 match scraped
- 1 row written into `data/raw/matches_source.csv`

The first successfully collected record contains:

- season `2025/2026`
- competition `WWIN LIGA BIH 25/26`
- round `27`
- date `2026-04-04`
- match `FK Zeljeznicar` vs `FK SARAJEVO`
- score `0:0`
- result `D`
- `points_total_after=30`
- `table_position_after=6`

### 5. Scraping documentation

The scraping workflow was documented in:

- `docs/scraping.md`

### 6. Pipeline input flexibility

The ingestion layer now supports:

- CSV input
- Excel input

The default pipeline input was switched to:

- `data/raw/matches_source.csv`

### 7. Pipeline verification after scraping

After the scraper wrote the first row, the pipeline was also run successfully.

Generated outputs:

- `data/processed/matches_processed.csv`
- `data/features/matches_features.csv`
- `results/validation_report.md`

Current validation status:

- no errors
- no warnings

## Current State

What is ready:

- repository structure
- schema documentation
- canonical raw CSV
- first validation and feature pipeline
- first official-source scraper
- verified end-to-end scrape of one official NFSBiH match row

What is not yet ready:

- historical round-by-round automated crawling
- complete multi-season dataset
- coach history automation
- baseline trained models
- chronological evaluation workflow

## Important Limitation

The current scraper is intentionally narrow.

It scrapes the round that is visible on an NFSBiH team stats page, not every round in a season.

That means the project has entered automated data collection, but not yet full historical data extraction.

## Recommended Next Step

The next engineering priority is:

1. reverse-engineer the NFSBiH `com_ajax` workflow or related selectors
2. iterate competition and round views automatically
3. populate `matches_source.csv` with complete FK Zeljeznicar seasons
4. validate and clean the resulting dataset

## Summary

As of `2026-04-10`, the project has moved from manual dataset planning into initial automated collection from official web sources.
