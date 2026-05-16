import pandas as pd

DEFAULT_CATEGORIES = [
    "식비",
    "교통",
    "주거/공과금",
    "의료/건강",
    "문화/여가",
    "쇼핑",
    "교육",
    "기타",
]


def get_categories() -> list[str]:
    return DEFAULT_CATEGORIES.copy()


def assign_category(df: pd.DataFrame, description_col: str = "description") -> pd.DataFrame:
    """category 컬럼이 없을 때 '미분류'로 초기화한다."""
    if "category" not in df.columns:
        df["category"] = "미분류"
    return df


def update_category(df: pd.DataFrame, index: int, category: str) -> pd.DataFrame:
    df.at[index, "category"] = category
    return df
