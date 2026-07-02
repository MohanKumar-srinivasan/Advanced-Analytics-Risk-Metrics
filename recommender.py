"""
recommender.py
Simple Fund Recommender — Bluestock Fintech Capstone

Given an investor's risk appetite (Low / Moderate / High), recommends the
top 3 funds by Sharpe ratio within the matching risk grade.

Usage:
    python3 recommender.py "Moderate"

Or import and call recommend_funds() directly.
"""

import sqlite3
import sys
import numpy as np
import pandas as pd

DB_PATH = "mutual_fund_analytics.db"
RISK_FREE_RATE = 0.06  # annualised, assumed


def load_data(db_path=DB_PATH):
    conn = sqlite3.connect(db_path)
    dim_fund = pd.read_sql("SELECT * FROM dim_fund", conn)
    fact_nav = pd.read_sql("SELECT fund_id, date, daily_return FROM fact_nav", conn)
    conn.close()
    return dim_fund, fact_nav


def recommend_funds(risk_appetite: str, dim_fund: pd.DataFrame, fact_nav: pd.DataFrame, top_n: int = 3) -> pd.DataFrame:
    """
    Recommend the top_n funds by Sharpe ratio whose risk_grade matches the
    investor's stated risk_appetite (Low / Moderate / High).
    """
    if risk_appetite not in ("Low", "Moderate", "High"):
        raise ValueError("risk_appetite must be one of: Low, Moderate, High")

    matching_ids = dim_fund.loc[dim_fund.risk_grade == risk_appetite, "fund_id"].tolist()
    if not matching_ids:
        return pd.DataFrame(columns=["fund_name", "category", "risk_grade", "sharpe_ratio"])

    rows = []
    for fid in matching_ids:
        r = fact_nav.loc[fact_nav.fund_id == fid, "daily_return"]
        if r.empty:
            continue
        ann_return = r.mean() * 252
        ann_vol = r.std() * np.sqrt(252)
        sharpe = (ann_return - RISK_FREE_RATE) / ann_vol if ann_vol > 0 else np.nan
        rows.append({"fund_id": fid, "sharpe_ratio": sharpe})

    result = (
        pd.DataFrame(rows)
        .merge(dim_fund[["fund_id", "fund_name", "category", "risk_grade"]], on="fund_id")
        .sort_values("sharpe_ratio", ascending=False)
        .head(top_n)[["fund_name", "category", "risk_grade", "sharpe_ratio"]]
        .reset_index(drop=True)
    )
    return result


def print_recommendation_table(risk_appetite: str, db_path=DB_PATH, top_n: int = 3):
    dim_fund, fact_nav = load_data(db_path)
    recs = recommend_funds(risk_appetite, dim_fund, fact_nav, top_n)
    print(f"\nTop {top_n} recommended funds for '{risk_appetite}' risk appetite:\n")
    if recs.empty:
        print("No matching funds found.")
    else:
        print(recs.to_string(index=False, formatters={"sharpe_ratio": "{:.3f}".format}))
    return recs


if __name__ == "__main__":
    risk_input = sys.argv[1] if len(sys.argv) > 1 else "Moderate"
    print_recommendation_table(risk_input)
