import pandas as pd
from pathlib import Path

SAMSUNG_CARD_SHEETS = ["일시불", "연회비-기타수수료"]


def load_samsung_card(file_path: str) -> pd.DataFrame:
    """삼성카드 청구서 엑셀을 로드한다. 사용처 컬럼이 있으면 category로 사용한다."""
    xl = pd.ExcelFile(file_path, engine="openpyxl")
    frames = []

    for sheet in SAMSUNG_CARD_SHEETS:
        if sheet not in xl.sheet_names:
            continue
        df = xl.parse(sheet, header=1)
        df = df.rename(columns={"이용일": "date", "가맹점": "description", "원금": "amount"})

        if "date" not in df.columns or "amount" not in df.columns:
            continue

        # 합계/빈 행 제거: 이용일이 8자리 숫자인 행만 유지
        df = df[df["date"].notna() & df["date"].astype(str).str.fullmatch(r"\d{8}")]

        df["category"] = df["사용처"].fillna("미분류") if "사용처" in df.columns else "미분류"
        df = df[["date", "description", "amount", "category"]].copy()
        frames.append(df)

    result = (
        pd.concat(frames, ignore_index=True)
        if frames
        else pd.DataFrame(columns=["date", "description", "amount", "category"])
    )
    result["date"] = pd.to_datetime(result["date"].astype(str), format="%Y%m%d", errors="coerce")
    result["amount"] = pd.to_numeric(result["amount"], errors="coerce").fillna(0)
    return result


def is_samsung_card_file(file_path: str) -> bool:
    xl = pd.ExcelFile(file_path, engine="openpyxl")
    return any(s in xl.sheet_names for s in SAMSUNG_CARD_SHEETS)


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
