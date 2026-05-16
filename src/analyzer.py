import pandas as pd


def monthly_summary(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["month"] = df["date"].dt.to_period("M").astype(str)
    return (
        df.groupby("month")["amount"]
        .sum()
        .reset_index()
        .rename(columns={"amount": "total"})
        .sort_values("month")
    )


def category_summary(df: pd.DataFrame, month: str | None = None) -> pd.DataFrame:
    """월을 지정하면 해당 월, None이면 전체 기간 카테고리별 합계를 반환한다."""
    df = df.copy()
    if month:
        df["month"] = df["date"].dt.to_period("M").astype(str)
        df = df[df["month"] == month]
    return (
        df.groupby("category")["amount"]
        .sum()
        .reset_index()
        .rename(columns={"amount": "total"})
        .sort_values("total", ascending=False)
    )


def monthly_category_pivot(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["month"] = df["date"].dt.to_period("M").astype(str)
    pivot = df.pivot_table(
        index="month", columns="category", values="amount", aggfunc="sum", fill_value=0
    )
    pivot = pivot.sort_index()
    return pivot
