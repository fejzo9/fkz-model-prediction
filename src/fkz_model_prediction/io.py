from __future__ import annotations

from pathlib import Path

import pandas as pd


def read_matches_table(path: str | Path, sheet_name: str = 0) -> pd.DataFrame:
    """Read the raw match table from either CSV or Excel."""
    input_path = Path(path)
    suffix = input_path.suffix.lower()

    if suffix == ".csv":
        return pd.read_csv(input_path)

    if suffix in {".xlsx", ".xls"}:
        return pd.read_excel(input_path, sheet_name=sheet_name)

    raise ValueError(f"Unsupported input format: {input_path.suffix}")


def ensure_parent_dir(path: str | Path) -> Path:
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    return output_path


def write_csv(df: pd.DataFrame, path: str | Path) -> Path:
    output_path = ensure_parent_dir(path)
    df.to_csv(output_path, index=False)
    return output_path
