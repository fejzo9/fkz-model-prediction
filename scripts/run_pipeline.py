from __future__ import annotations

import argparse
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from fkz_model_prediction.pipeline import run_pipeline


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the FKZ data ingestion pipeline.")
    parser.add_argument(
        "--input",
        default=str(PROJECT_ROOT / "data" / "raw" / "results_2024_2025.xlsx"),
        help="Path to the raw Excel workbook.",
    )
    parser.add_argument(
        "--processed-output",
        default=str(PROJECT_ROOT / "data" / "processed" / "matches_processed.csv"),
        help="Path for the cleaned match-level CSV.",
    )
    parser.add_argument(
        "--features-output",
        default=str(PROJECT_ROOT / "data" / "features" / "matches_features.csv"),
        help="Path for the feature dataset CSV.",
    )
    parser.add_argument(
        "--report-output",
        default=str(PROJECT_ROOT / "results" / "validation_report.md"),
        help="Path for the validation report.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    outputs = run_pipeline(
        input_path=args.input,
        processed_output_path=args.processed_output,
        features_output_path=args.features_output,
        report_output_path=args.report_output,
    )
    print(f"Processed dataset: {outputs.processed_path}")
    print(f"Feature dataset:   {outputs.features_path}")
    print(f"Validation report: {outputs.report_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
