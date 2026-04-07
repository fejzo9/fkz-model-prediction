from __future__ import annotations

from pathlib import Path

import pandas as pd


def read_matches_excel(path: str | Path, sheet_name: str = 0) -> pd.DataFrame:
    """Read the raw Excel workbook into a DataFrame."""
    return pd.read_excel(path, sheet_name=sheet_name)


def ensure_parent_dir(path: str | Path) -> Path:
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    return output_path


def write_csv(df: pd.DataFrame, path: str | Path) -> Path:
    output_path = ensure_parent_dir(path)
    df.to_csv(output_path, index=False)
    return output_path
