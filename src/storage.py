import pandas as pd
from tinydb import TinyDB, Query
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "data" / "budget.json"


def get_db() -> TinyDB:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    return TinyDB(DB_PATH, ensure_ascii=False, indent=2)


def save_records(df: pd.DataFrame) -> int:
    """DataFrame 행을 DB에 저장하고 저장된 건수를 반환한다."""
    db = get_db()
    records = df.to_dict(orient="records")
    for r in records:
        if "date" in r and hasattr(r["date"], "isoformat"):
            r["date"] = r["date"].isoformat()
    db.insert_multiple(records)
    return len(records)


def load_all_records() -> pd.DataFrame:
    db = get_db()
    records = db.all()
    if not records:
        return pd.DataFrame(columns=["date", "description", "amount", "category"])
    df = pd.DataFrame(records)
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce").fillna(0)
    return df


def clear_all() -> None:
    get_db().truncate()
