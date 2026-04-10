# Technical Assessment

## Summary

This repository currently represents a solid project idea with an early dataset draft, but it is not yet a usable machine learning project in its present form.

Historical note:

- this assessment reflects the repository state on `2026-04-06`
- newer additions such as the canonical CSV workflow and the first NFSBiH scraper were added afterwards
- see `docs/status-report-2026-04-10.md` for the updated project state

The strongest parts are:

- a clear domain focus: FK Zeljeznicar and WWIN Liga BiH
- an appropriate initial modeling direction: Poisson and logistic baselines before deeper models
- an explicit intent to model probabilities instead of exact-score guessing

The main blockers are:

- no reproducible project structure
- no executable code or data pipeline
- no validated dataset lifecycle
- no train/evaluation split strategy
- no feature engineering implementation
- no model training baseline
- no quality controls around raw data

## What Exists Today

- `README.md` defines the research goal and planned architecture
- `requirements.txt` lists a plausible analytics stack
- `results_2024_2025.xlsx` contains a starter spreadsheet for match-level data
- `izvor za unos.txt` points to the likely manual source for data entry

## What Is Missing

### 1. Data layer is not operational

The project has a raw spreadsheet, but not a proper data workflow.

Missing pieces:

- a canonical `data/raw` location
- a processed dataset format such as CSV or Parquet
- a deterministic ingestion script
- schema validation
- explicit handling for missing values and malformed rows
- versioning strategy for raw data changes

Impact:

- every future experiment would be manual and hard to reproduce
- modeling results would not be trustworthy because the input dataset is not controlled

### 2. Dataset quality is not yet sufficient

The current spreadsheet appears to be mostly a template rather than a finished dataset.

Observed issues:

- many rows only contain season, competition, round, and date
- the majority of predictive columns are empty
- date formulas appear to be copied incorrectly for several rows
- no evidence of unique match identifiers being consistently filled
- no indication that team names, venues, results, and points are standardized

Impact:

- the current file is not ready for feature engineering
- silent spreadsheet errors will propagate directly into models unless validation is added

### 3. No feature engineering implementation

The README lists the right kinds of features, but nothing computes them yet.

Still needed:

- rolling form features over last N matches
- cumulative points and goal-difference features
- home/away normalization
- head-to-head summaries
- opponent-strength features
- league-table context prior to kickoff rather than after the match

Impact:

- model inputs are not yet defined in code
- it is impossible to compare experiments consistently

### 4. No modeling baseline

The repository proposes Poisson regression, logistic regression, and CNNs, but none are implemented.

Recommended order:

1. Poisson goal model
2. Derived home/draw/away probabilities from expected goals
3. Simple multiclass baseline for W/D/L
4. Only after that, sequence/deep-learning experiments

Impact:

- there is no benchmark for whether the data is informative at all
- moving to CNNs too early would likely increase complexity without evidence of benefit

### 5. No evaluation protocol

A proper sports-prediction project needs time-aware evaluation, not random splitting.

Missing pieces:

- chronological train/validation/test split
- rolling-origin evaluation
- calibration analysis
- baseline comparisons against naive heuristics
- experiment logging

Impact:

- future scores could look good while still leaking future information
- model performance would be misleading without time-aware validation

### 6. No separation between research assets and production assets

The README mentions Colab notebooks, but the repository has no notebooks, no `src` package, and no scripts.

Missing pieces:

- notebooks for exploratory work
- source package for reusable code
- scripts for deterministic runs
- output locations for models and reports

Impact:

- work would drift into one-off notebooks
- reproducibility and maintainability would degrade quickly

## Recommended Target Architecture

The minimum practical structure should be:

```text
data/
  raw/
  processed/
  features/
docs/
models/
notebooks/
results/
scripts/
src/
  fkz_model_prediction/
```

Within that structure, responsibilities should be:

- `data/raw`: untouched source files
- `data/processed`: cleaned match-level tables
- `data/features`: model-ready feature sets
- `src/fkz_model_prediction`: reusable Python code
- `scripts`: thin CLI entry points
- `notebooks`: exploration and visual analysis only
- `results`: reports, metrics, figures
- `models`: serialized artifacts if later needed

## Recommended Work Order

### Phase 1. Stabilize data

- move raw inputs into a canonical data location
- implement spreadsheet ingestion
- validate schema and types
- fix date handling
- standardize team names and result labels
- export a cleaned processed table

### Phase 2. Build baseline features

- add home/away indicator
- add rolling form features
- add cumulative goals for and against
- add cumulative points before the match
- add opponent-level context features

### Phase 3. Establish baselines

- train a Poisson goal model
- derive outcome probabilities
- benchmark against naive baselines

### Phase 4. Evaluation and iteration

- add time-aware split logic
- compute log-loss, Brier, and calibration
- inspect feature drift and data sparsity

### Phase 5. Deep-learning experiments

- only start CNN or sequence models after strong baselines exist

## Main Technical Conclusions

1. The repository is currently a research concept with an initial dataset shell, not yet a functional ML system.
2. The immediate bottleneck is not model choice but data reliability and reproducibility.
3. The fastest path to value is a clean tabular pipeline and classical statistical baselines.
4. CNNs may become useful later, but they are not the next engineering priority.
5. Without validation and chronological evaluation, any future accuracy claims would be weak.

## Immediate Next Step

The correct next engineering action is to convert the repository into a reproducible data project with:

- raw and processed data directories
- a first ingestion and validation pipeline
- starter feature engineering
- documentation of assumptions and known data issues

That is the work implemented after this assessment.
