import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

import pandas as pd
import streamlit as st

from src.loader import load_file, normalize_columns
from src.categorizer import get_categories, assign_category
from src.analyzer import monthly_summary, category_summary, monthly_category_pivot
from src.storage import save_records, load_all_records, clear_all
from src.charts import bar_monthly, pie_category, heatmap_monthly_category, line_monthly

st.set_page_config(page_title="가계부 대시보드", page_icon="💰", layout="wide")
st.title("💰 가계부 대시보드")

# ── 사이드바: 파일 업로드 ──────────────────────────────────────────────────
with st.sidebar:
    st.header("데이터 입력")
    uploaded = st.file_uploader("CSV 또는 Excel 파일 업로드", type=["csv", "xlsx"])

    if uploaded:
        import tempfile, os
        suffix = Path(uploaded.name).suffix
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            tmp.write(uploaded.read())
            tmp_path = tmp.name

        try:
            df_new = load_file(tmp_path)
            df_new = normalize_columns(df_new)
            df_new = assign_category(df_new)
            st.success(f"{len(df_new)}건 로드됨")
            st.session_state["df_new"] = df_new
        except Exception as e:
            st.error(f"파일 오류: {e}")
        finally:
            os.unlink(tmp_path)

    st.divider()
    if st.button("전체 데이터 초기화", type="secondary"):
        clear_all()
        st.session_state.pop("df_new", None)
        st.success("초기화 완료")

# ── 카테고리 지정 ─────────────────────────────────────────────────────────
if "df_new" in st.session_state:
    st.subheader("카테고리 지정")
    df_new: pd.DataFrame = st.session_state["df_new"]
    categories = get_categories()

    edited = st.data_editor(
        df_new[["date", "description", "amount", "category"]],
        column_config={
            "category": st.column_config.SelectboxColumn("카테고리", options=categories),
            "date": st.column_config.DateColumn("날짜"),
            "amount": st.column_config.NumberColumn("금액 (원)", format="%d"),
        },
        use_container_width=True,
        num_rows="fixed",
        key="editor",
    )

    if st.button("저장", type="primary"):
        count = save_records(edited)
        st.success(f"{count}건 저장 완료")
        del st.session_state["df_new"]
        st.rerun()

# ── 대시보드 ──────────────────────────────────────────────────────────────
df = load_all_records()

if df.empty:
    st.info("데이터가 없습니다. 사이드바에서 파일을 업로드하세요.")
    st.stop()

# 월 선택
months = sorted(df["date"].dt.to_period("M").astype(str).unique())
selected_month = st.selectbox("조회 월", ["전체"] + months)

col1, col2 = st.columns(2)

with col1:
    summary = monthly_summary(df)
    st.plotly_chart(bar_monthly(summary), use_container_width=True)

with col2:
    month_filter = None if selected_month == "전체" else selected_month
    cat_sum = category_summary(df, month_filter)
    st.plotly_chart(pie_category(cat_sum, selected_month), use_container_width=True)

col3, col4 = st.columns(2)

with col3:
    st.plotly_chart(line_monthly(summary), use_container_width=True)

with col4:
    pivot = monthly_category_pivot(df)
    if not pivot.empty:
        st.plotly_chart(heatmap_monthly_category(pivot), use_container_width=True)

# 상세 테이블
with st.expander("전체 데이터 보기"):
    view = df.copy()
    view["date"] = view["date"].dt.strftime("%Y-%m-%d")
    st.dataframe(view, use_container_width=True)
