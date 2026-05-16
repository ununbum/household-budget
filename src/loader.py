import pandas as pd
from pathlib import Path


def load_file(file_path: str) -> pd.DataFrame:
    path = Path(file_path)
    if path.suffix == ".csv":
        df = pd.read_csv(file_path, encoding="utf-8-sig")
    elif path.suffix in (".xlsx", ".xls"):
        df = pd.read_excel(file_path, engine="openpyxl")
    else:
        raise ValueError(f"지원하지 않는 파일 형식입니다: {path.suffix}")
    return df


def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """날짜, 금액, 항목 컬럼명을 표준화한다."""
    rename_map = {}
    for col in df.columns:
        lower = col.strip().lower()
        if lower in ("날짜", "date", "일자"):
            rename_map[col] = "date"
        elif lower in ("금액", "amount", "지출", "비용"):
            rename_map[col] = "amount"
        elif lower in ("항목", "내용", "description", "내역"):
            rename_map[col] = "description"
        elif lower in ("카테고리", "category", "분류"):
            rename_map[col] = "category"
    df = df.rename(columns=rename_map)
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce").fillna(0)
    return df
