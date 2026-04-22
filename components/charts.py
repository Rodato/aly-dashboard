"""Centralized Plotly chart factory — consistent styling across all pages."""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils.styles import COLORS

_BASE = dict(
    paper_bgcolor=COLORS["bg_card"],
    plot_bgcolor=COLORS["bg_card"],
    font=dict(family="Open Sans, sans-serif", size=11, color=COLORS["text"]),
    margin=dict(l=8, r=8, t=14, b=8),
    hoverlabel=dict(
        bgcolor=COLORS["bg_card"],
        bordercolor=COLORS["border"],
        font=dict(family="Open Sans, sans-serif", size=11),
    ),
)

_AXIS = dict(
    gridcolor="#F3F4F6",
    linecolor=COLORS["border"],
    tickfont=dict(size=10, color=COLORS["text_secondary"]),
    title=None,  # hidden by default — card_header shows the label
)


def _layout(title: str = "", **kw):
    base = {**_BASE, "xaxis": _AXIS.copy(), "yaxis": _AXIS.copy()}
    if title:
        base["title"] = dict(
            text=title, x=0.01, xanchor="left",
            font=dict(family="Open Sans, sans-serif", size=12,
                      color=COLORS["text_secondary"]),
        )
        base["margin"] = dict(l=8, r=8, t=40, b=8)
    base.update(kw)
    return base


# ── Bar (horizontal) ─────────────────────────────────────────────────────────

def bar_h(df: pd.DataFrame, x: str, y: str, title: str = "",
          color: str = None, height: int = 280) -> go.Figure:
    color = color or COLORS["accent"]
    fig = px.bar(
        df, x=x, y=y, orientation="h",
        color_discrete_sequence=[color],
    )
    fig.update_layout(**_layout(title=title, height=height,
                                yaxis_categoryorder="total ascending"))
    fig.update_xaxes(title_text="")
    fig.update_yaxes(title_text="")
    fig.update_traces(
        marker_line_width=0,
        hovertemplate="<b>%{y}</b><br>%{x} usuarios<extra></extra>",
    )
    return fig


# ── Donut chart ───────────────────────────────────────────────────────────────

def donut(df: pd.DataFrame, names: str, values: str, title: str = "",
          height: int = 280) -> go.Figure:
    palette = [COLORS["accent"], COLORS["yellow"], COLORS["red"], COLORS["green"], COLORS["navy"]]
    fig = px.pie(
        df, names=names, values=values,
        color_discrete_sequence=palette,
        hole=0.55,
    )
    fig.update_traces(
        textposition="inside",
        textinfo="percent",
        textfont=dict(family="Open Sans, sans-serif", size=12, color="#FFFFFF"),
        marker=dict(line=dict(color=COLORS["bg_card"], width=2)),
        hovertemplate="<b>%{label}</b><br>%{value} usuarios (%{percent})<extra></extra>",
    )
    layout = {**_BASE, "height": height, "showlegend": True,
              "legend": dict(orientation="h", yanchor="bottom", y=-0.1,
                             xanchor="center", x=0.5, font=dict(size=11))}
    if title:
        layout["title"] = dict(
            text=title, x=0.01, xanchor="left",
            font=dict(family="Open Sans, sans-serif", size=12,
                      color=COLORS["text_secondary"]),
        )
        layout["margin"] = dict(l=8, r=8, t=40, b=8)
    fig.update_layout(**layout)
    return fig


# ── Bar (vertical) ────────────────────────────────────────────────────────────

def bar_v(df: pd.DataFrame, x: str, y: str, title: str = "",
          color: str = None, height: int = 240) -> go.Figure:
    color = color or COLORS["accent"]
    fig = px.bar(df, x=x, y=y, color_discrete_sequence=[color])
    fig.update_layout(**_layout(title=title, height=height, bargap=0.25))
    fig.update_xaxes(title_text="")
    fig.update_yaxes(title_text="")
    fig.update_traces(marker_line_width=0)
    return fig


# ── Silhouette world map (flat land + accent dots at locations) ──────────────

def choropleth(df: pd.DataFrame, locations: str, color: str, title: str = "",
               height: int = 260) -> go.Figure:
    """Flat silhouette map: land mass in a single muted gray (no borders, no
    coastlines), with accent dots at each country with users. Kept under the
    original name for backwards compatibility with callers.
    """
    if df.empty:
        return go.Figure()

    max_n = max(int(df[color].max()), 1)
    df = df.copy()
    df["_size"] = (df[color] / max_n * 14) + 10

    fig = go.Figure()

    # Soft halo under each dot (same location, bigger + transparent)
    fig.add_trace(go.Scattergeo(
        locations=df[locations],
        locationmode="country names",
        marker=dict(
            size=df["_size"] * 2.2,
            color=COLORS["accent"],
            opacity=0.18,
            line=dict(width=0),
        ),
        showlegend=False, hoverinfo="skip",
    ))

    # Main accent dot per country
    fig.add_trace(go.Scattergeo(
        locations=df[locations],
        locationmode="country names",
        text=df[locations],
        customdata=df[color],
        marker=dict(
            size=df["_size"],
            color=COLORS["accent"],
            opacity=1.0,
            line=dict(color="#FFFFFF", width=1.5),
        ),
        hovertemplate="<b>%{text}</b><br>%{customdata} usuarios<extra></extra>",
        showlegend=False,
    ))

    layout = {
        **_BASE, "height": height,
        "geo": dict(
            showframe=False,
            showcoastlines=False,
            showcountries=False,
            showland=True,     landcolor="#D1D5DB",
            showocean=False,
            showlakes=False,
            projection_type="natural earth",
            resolution=110,
            bgcolor=COLORS["bg_card"],
            lonaxis_showgrid=False, lataxis_showgrid=False,
        ),
    }
    if title:
        layout["title"] = dict(
            text=title, x=0.01, xanchor="left",
            font=dict(family="Open Sans, sans-serif", size=12,
                      color=COLORS["text_secondary"]),
        )
        layout["margin"] = dict(l=0, r=0, t=40, b=0)
    else:
        layout["margin"] = dict(l=0, r=0, t=8, b=8)

    fig.update_layout(**layout)
    return fig
