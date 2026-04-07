# Workflow

## Canonical Data Locations

- Raw spreadsheet: `data/raw/results_2024_2025.xlsx`
- Raw source references: `data/raw/source_urls.txt`
- Cleaned match table: `data/processed/matches_processed.csv`
- Feature table: `data/features/matches_features.csv`
- Validation output: `results/validation_report.md`

## How To Run

From the project root:

```powershell
python scripts/run_pipeline.py
```

Optional arguments:

```powershell
python scripts/run_pipeline.py `
  --input data/raw/results_2024_2025.xlsx `
  --processed-output data/processed/matches_processed.csv `
  --features-output data/features/matches_features.csv `
  --report-output results/validation_report.md
```

## What The Pipeline Does

1. Reads the raw Excel workbook.
2. Validates that the expected schema exists.
3. Normalizes dates and numeric columns.
4. Exports a cleaned match-level dataset.
5. Builds starter modeling features.
6. Writes a validation report with errors and warnings.

## Current Constraints

- The raw Excel still appears partially incomplete.
- Date values in the current workbook should be reviewed manually.
- The generated features are starter features, not yet a final modeling set.
- A train/evaluation workflow still needs to be added after the dataset is stabilized.
