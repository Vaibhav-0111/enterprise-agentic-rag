"""
Visualization Agent — generates charts using Plotly and returns figures.
"""
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from typing import Any, Dict, List


PALETTE = ["#6382ff", "#a78bfa", "#2dd4bf", "#fbbf24", "#34d399", "#f97316"]


def run_visualization(
    rows: List[dict],
    columns: List[str],
    chart_type: str = "auto",
) -> go.Figure:
    """Generate an appropriate Plotly chart from query results."""
    df = pd.DataFrame(rows, columns=columns)
    numeric_cols = df.select_dtypes(include="number").columns.tolist()
    text_cols    = df.select_dtypes(exclude="number").columns.tolist()

    if not numeric_cols:
        return _empty_figure("No numeric data to visualize.")

    x_col = text_cols[0] if text_cols else df.index.name or "index"

    # Grouped bar: two numeric columns (e.g. q2_revenue, q3_revenue)
    if len(numeric_cols) >= 2 and chart_type in ("auto", "bar"):
        fig = go.Figure()
        for i, col in enumerate(numeric_cols[:4]):
            fig.add_trace(go.Bar(
                name=col.replace("_", " ").title(),
                x=df[x_col] if x_col in df.columns else df.index,
                y=df[col],
                marker_color=PALETTE[i % len(PALETTE)],
            ))
        fig.update_layout(**_layout("Revenue Comparison"))
        return fig

    # Single bar
    if chart_type in ("auto", "bar"):
        fig = px.bar(
            df,
            x=x_col if x_col in df.columns else df.index,
            y=numeric_cols[0],
            color_discrete_sequence=PALETTE,
        )
        fig.update_layout(**_layout(numeric_cols[0].replace("_", " ").title()))
        return fig

    # Line
    if chart_type == "line":
        fig = px.line(df, x=x_col, y=numeric_cols[0], color_discrete_sequence=PALETTE)
        fig.update_layout(**_layout("Trend"))
        return fig

    return _empty_figure("Unknown chart type.")


def _layout(title: str) -> dict:
    return dict(
        title=dict(text=title, font=dict(color="#e2e8f0", size=14)),
        paper_bgcolor="#111827",
        plot_bgcolor="#0a0e1a",
        font=dict(color="#94a3b8", family="Space Grotesk"),
        xaxis=dict(gridcolor="rgba(99,130,255,.1)", linecolor="rgba(99,130,255,.2)"),
        yaxis=dict(gridcolor="rgba(99,130,255,.1)", linecolor="rgba(99,130,255,.2)"),
        legend=dict(bgcolor="rgba(0,0,0,0)"),
        margin=dict(t=40, b=30, l=40, r=20),
    )


def _empty_figure(msg: str) -> go.Figure:
    fig = go.Figure()
    fig.add_annotation(text=msg, x=0.5, y=0.5, showarrow=False,
                       font=dict(color="#64748b", size=13))
    fig.update_layout(**_layout(""), xaxis_visible=False, yaxis_visible=False)
    return fig
