"""Centralized Plotly chart factory — consistent styling across all pages."""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils.styles import COLORS

_BASE = dict(
    paper_bgcolor=COLORS["bg_card"],
    plot_bgcolor=COLORS["bg_card"],
    font=dict(family="Open Sans, sans-serif", size=11, color=COLORS["text"]),
    margin=dict(l=8, r=8, t=40, b=8),
    hoverlabel=dict(
        bgcolor=COLORS["bg_card"],
        bordercolor=COLORS["border"],
        font=dict(family="Open Sans, sans-serif", size=11),
    ),
    title=dict(
        font=dict(family="Open Sans, sans-serif", size=12, color=COLORS["text_secondary"]),
        x=0.01, xanchor="left",
    ),
)

_AXIS = dict(
    gridcolor="#F3F4F6",
    linecolor=COLORS["border"],
    tickfont=dict(size=10, color=COLORS["text_secondary"]),
)


def _layout(**kw):
    base = {**_BASE, "xaxis": _AXIS.copy(), "yaxis": _AXIS.copy()}
    base.update(kw)
    return base


# ── Bar (horizontal) ─────────────────────────────────────────────────────────

def bar_h(df: pd.DataFrame, x: str, y: str, title: str,
          color: str = None, height: int = 280) -> go.Figure:
    color = color or COLORS["accent"]
    fig = px.bar(
        df, x=x, y=y, orientation="h",
        title=title,
        color_discrete_sequence=[color],
    )
    fig.update_layout(**_layout(height=height, yaxis_categoryorder="total ascending"))
    fig.update_traces(
        marker_line_width=0,
        hovertemplate="%{y}<br><b>%{x}</b><extra></extra>",
    )
    return fig


# ── Donut chart ───────────────────────────────────────────────────────────────

def donut(df: pd.DataFrame, names: str, values: str, title: str,
          height: int = 280) -> go.Figure:
    palette = [COLORS["accent"], COLORS["yellow"], COLORS["red"], COLORS["green"], COLORS["navy"]]
    fig = px.pie(
        df, names=names, values=values,
        title=title,
        color_discrete_sequence=palette,
        hole=0.50,
    )
    fig.update_traces(
        textfont=dict(family="Open Sans, sans-serif", size=11),
        marker=dict(line=dict(color=COLORS["bg_card"], width=2)),
        hovertemplate="%{label}<br><b>%{value}</b> (%{percent})<extra></extra>",
    )
    fig.update_layout(**{**_BASE, "height": height, "showlegend": True,
                         "legend": dict(orientation="v", font=dict(size=10))})
    return fig


# ── Bar (vertical) ────────────────────────────────────────────────────────────

def bar_v(df: pd.DataFrame, x: str, y: str, title: str,
          color: str = None, height: int = 240) -> go.Figure:
    color = color or COLORS["accent"]
    fig = px.bar(df, x=x, y=y, title=title, color_discrete_sequence=[color])
    fig.update_layout(**_layout(height=height, bargap=0.25))
    fig.update_traces(marker_line_width=0)
    return fig


# ── Choropleth world map ──────────────────────────────────────────────────────

def choropleth(df: pd.DataFrame, locations: str, color: str, title: str,
               height: int = 280) -> go.Figure:
    fig = px.choropleth(
        df,
        locations=locations,
        locationmode="country names",
        color=color,
        title=title,
        color_continuous_scale=[
            [0.0, "#EFF6FF"],
            [0.5, "#3B82F6"],
            [1.0, COLORS["navy"]],
        ],
    )
    fig.update_layout(
        **{**_BASE, "height": height,
           "geo": dict(
               showframe=False,
               showcoastlines=True,
               coastlinecolor=COLORS["border"],
               showland=True, landcolor="#F9FAFB",
               showocean=True, oceancolor="#EFF6FF",
               bgcolor=COLORS["bg_card"],
           ),
           "coloraxis_showscale": False,
           }
    )
    return fig
