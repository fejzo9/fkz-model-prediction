# Workflow

## Canonical Data Locations

- Raw source match table: `data/raw/matches_source.csv`
- Raw starter spreadsheet: `data/raw/results_2024_2025.xlsx`
- Raw source references: `data/raw/source_urls.txt`
- Cleaned match table: `data/processed/matches_processed.csv`
- Feature table: `data/features/matches_features.csv`
- Validation output: `results/validation_report.md`

## How To Run

From the project root:

```powershell
python scripts/run_pipeline.py
```

To scrape currently visible NFSBiH results into the canonical raw CSV:

```powershell
python scripts/scrape_nfsbih.py
```

Optional arguments:

```powershell
python scripts/run_pipeline.py `
  --input data/raw/matches_source.csv `
  --processed-output data/processed/matches_processed.csv `
  --features-output data/features/matches_features.csv `
  --report-output results/validation_report.md
```

## What The Pipeline Does

1. Reads the raw CSV or Excel match table.
2. Validates that the expected schema exists.
3. Normalizes dates and numeric columns.
4. Exports a cleaned match-level dataset.
5. Builds starter modeling features.
6. Writes a validation report with errors and warnings.

## Current Constraints

- The old raw Excel still appears partially incomplete.
- The new CSV source table should become the main canonical raw input.
- The first scraper only captures the currently visible round on an NFSBiH team page.
- The generated features are starter features, not yet a final modeling set.
- A train/evaluation workflow still needs to be added after the dataset is stabilized.
