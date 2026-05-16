import pandas as pd
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from src.analyzer import monthly_summary, category_summary


def make_df():
    return pd.DataFrame({
        "date": pd.to_datetime(["2026-01-05", "2026-01-20", "2026-02-10"]),
        "description": ["편의점", "카페", "마트"],
        "amount": [5000, 8000, 30000],
        "category": ["식비", "식비", "식비"],
    })


def test_monthly_summary():
    df = make_df()
    result = monthly_summary(df)
    assert list(result["month"]) == ["2026-01", "2026-02"]
    assert result.loc[result["month"] == "2026-01", "total"].values[0] == 13000


def test_category_summary_filtered():
    df = make_df()
    result = category_summary(df, month="2026-01")
    assert result.iloc[0]["total"] == 13000


def test_category_summary_all():
    df = make_df()
    result = category_summary(df)
    assert result.iloc[0]["total"] == 43000
