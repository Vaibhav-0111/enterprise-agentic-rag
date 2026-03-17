"""
Analytics Agent — runs Python calculations on structured SQL results.
"""
import pandas as pd
from typing import Any, Dict, List


def run_analytics(rows: List[dict], columns: List[str], question: str) -> Dict[str, Any]:
    """Compute growth rates, correlations, and key statistics from SQL results."""
    df = pd.DataFrame(rows, columns=columns)
    stats: Dict[str, Any] = {}

    # Auto-detect numeric columns
    numeric_cols = df.select_dtypes(include="number").columns.tolist()

    for col in numeric_cols:
        stats[col] = {
            "mean":   round(df[col].mean(), 2),
            "max":    round(df[col].max(), 2),
            "min":    round(df[col].min(), 2),
            "sum":    round(df[col].sum(), 2),
            "std":    round(df[col].std(), 2),
        }

    # Growth rate if q2 and q3 columns present
    if "q2_revenue" in df.columns and "q3_revenue" in df.columns:
        df["growth_pct"] = (
            (df["q3_revenue"] - df["q2_revenue"]) / df["q2_revenue"] * 100
        ).round(2)
        stats["growth_rates"] = df[["product_name", "growth_pct"]].to_dict("records")
        stats["top_grower"]   = df.loc[df["growth_pct"].idxmax(), "product_name"]
        stats["avg_growth"]   = round(df["growth_pct"].mean(), 2)

    stats["row_count"] = len(df)
    stats["columns"]   = columns
    return stats
