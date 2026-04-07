from __future__ import annotations

from dataclasses import dataclass, field

import pandas as pd


REQUIRED_COLUMNS = [
    "season",
    "competititon",
    "round",
    "match_date",
    "match_id",
    "team",
    "opponent",
    "venue",
    "goals_for",
    "goals_against",
    "result",
    "points_earned",
    "points_total_after",
    "table_position_after",
    "coach",
    "notes",
]


@dataclass
class ValidationReport:
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    @property
    def is_valid(self) -> bool:
        return not self.errors


def validate_schema(df: pd.DataFrame) -> ValidationReport:
    report = ValidationReport()
    missing = [column for column in REQUIRED_COLUMNS if column not in df.columns]
    if missing:
        report.errors.append(f"Missing required columns: {', '.join(missing)}")
    return report


def validate_match_data(df: pd.DataFrame) -> ValidationReport:
    report = validate_schema(df)
    if not report.is_valid:
        return report

    if df["round"].isna().any():
        report.warnings.append("Some rows are missing round numbers.")

    if df["match_date"].isna().any():
        report.warnings.append("Some rows are missing match dates.")

    populated_core = df[["team", "opponent", "venue", "goals_for", "goals_against", "result"]].notna().sum()
    if (populated_core == 0).any():
        empty_columns = ", ".join(populated_core[populated_core == 0].index.tolist())
        report.warnings.append(f"Core columns appear fully empty: {empty_columns}")

    if {"team", "match_date"}.issubset(df.columns):
        duplicated_team_dates = df[["team", "match_date"]].dropna().duplicated().sum()
        if duplicated_team_dates > 0:
            report.warnings.append(
                f"Detected {duplicated_team_dates} duplicated team/date combinations. "
                "Check whether spreadsheet formulas or manual entries were copied incorrectly."
            )

    return report
