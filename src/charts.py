import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def bar_monthly(df_summary: pd.DataFrame) -> go.Figure:
    fig = px.bar(
        df_summary,
        x="month",
        y="total",
        title="월별 총 지출",
        labels={"month": "월", "total": "지출 (원)"},
        color_discrete_sequence=["#4C9BE8"],
    )
    fig.update_layout(xaxis_tickangle=-45)
    return fig


def pie_category(df_summary: pd.DataFrame, month: str = "") -> go.Figure:
    title = f"{month} 카테고리별 지출" if month else "전체 카테고리별 지출"
    fig = px.pie(
        df_summary,
        names="category",
        values="total",
        title=title,
        hole=0.35,
    )
    return fig


def heatmap_monthly_category(pivot: pd.DataFrame) -> go.Figure:
    fig = px.imshow(
        pivot,
        title="월×카테고리 지출 히트맵",
        labels={"x": "카테고리", "y": "월", "color": "지출 (원)"},
        aspect="auto",
        color_continuous_scale="Blues",
    )
    return fig


def line_monthly(df_summary: pd.DataFrame) -> go.Figure:
    fig = px.line(
        df_summary,
        x="month",
        y="total",
        title="월별 지출 추이",
        labels={"month": "월", "total": "지출 (원)"},
        markers=True,
    )
    return fig
