from __future__ import annotations

import pandas as pd


def build_base_features(df: pd.DataFrame) -> pd.DataFrame:
    features = df.copy()

    features["is_home"] = (
        features["venue"]
        .astype("string")
        .str.strip()
        .str.lower()
        .map({"home": 1, "away": 0})
    )

    features = features.sort_values(["team", "match_date", "round"], na_position="last").reset_index(drop=True)

    features["goal_difference"] = features["goals_for"] - features["goals_against"]

    features["points_before_match"] = (
        pd.to_numeric(features["points_total_after"], errors="coerce")
        - pd.to_numeric(features["points_earned"], errors="coerce")
    )

    grouped = features.groupby("team", dropna=False)
    features["matches_played_before"] = grouped.cumcount()
    features["goals_for_cum_before"] = grouped["goals_for"].transform(
        lambda series: series.cumsum().shift(1)
    )
    features["goals_against_cum_before"] = grouped["goals_against"].transform(
        lambda series: series.cumsum().shift(1)
    )

    recent_points = (
        grouped["points_earned"]
        .apply(lambda series: series.shift(1).rolling(window=5, min_periods=1).sum())
        .reset_index(level=0, drop=True)
    )
    features["points_last_5"] = recent_points

    return features
