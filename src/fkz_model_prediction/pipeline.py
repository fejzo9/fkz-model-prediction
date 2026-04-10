from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .features import build_base_features
from .io import read_matches_table, write_csv
from .validation import validate_match_data


@dataclass
class PipelineOutputs:
    processed_path: Path
    features_path: Path
    report_path: Path


def run_pipeline(
    input_path: str | Path,
    processed_output_path: str | Path,
    features_output_path: str | Path,
    report_output_path: str | Path,
) -> PipelineOutputs:
    raw_df = read_matches_table(input_path)
    validation_report = validate_match_data(raw_df)

    processed_df = raw_df.copy()
    processed_df.columns = [column.strip().lower() for column in processed_df.columns]
    processed_df["match_date"] = processed_df["match_date"].apply(_normalize_excel_date)

    numeric_columns = [
        "round",
        "goals_for",
        "goals_against",
        "points_earned",
        "points_total_after",
        "table_position_after",
    ]
    for column in numeric_columns:
        if column in processed_df.columns:
            processed_df[column] = processed_df[column].astype("string").str.strip()
            processed_df[column] = processed_df[column].replace({"": None})
            processed_df[column] = processed_df[column].astype("Float64")

    feature_df = build_base_features(processed_df)

    processed_path = write_csv(processed_df, processed_output_path)
    features_path = write_csv(feature_df, features_output_path)
    report_path = _write_validation_report(validation_report, report_output_path)

    return PipelineOutputs(
        processed_path=processed_path,
        features_path=features_path,
        report_path=report_path,
    )


def _normalize_excel_date(value):
    if value is None:
        return None
    if hasattr(value, "isoformat"):
        return value
    try:
        numeric_value = float(value)
    except (TypeError, ValueError):
        return value
    return _excel_serial_to_timestamp(numeric_value)


def _excel_serial_to_timestamp(serial: float):
    import pandas as pd

    if pd.isna(serial):
        return pd.NaT
    return pd.Timestamp("1899-12-30") + pd.to_timedelta(serial, unit="D")


def _write_validation_report(report, output_path: str | Path) -> Path:
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    lines = ["# Validation Report", ""]

    lines.append("## Errors")
    if report.errors:
        lines.extend(f"- {item}" for item in report.errors)
    else:
        lines.append("- None")

    lines.append("")
    lines.append("## Warnings")
    if report.warnings:
        lines.extend(f"- {item}" for item in report.warnings)
    else:
        lines.append("- None")

    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return output_path
