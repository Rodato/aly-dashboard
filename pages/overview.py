"""Página Inicio — KPIs, growth chart, activity heatmap."""

import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

from utils.i18n import t
from utils import db
from utils.styles import COLORS, page_header, section_label
from components.kpi_row import render as kpi_row
from components.filters import get_filters

# ── Plotly base layout ────────────────────────────────────────────────────────
_LAYOUT = dict(
    paper_bgcolor=COLORS["bg_card"],
    plot_bgcolor=COLORS["bg_card"],
    font=dict(family="Open Sans, sans-serif", size=11, color=COLORS["text"]),
    margin=dict(l=8, r=8, t=40, b=8),
    xaxis=dict(
        gridcolor="#F3F4F6",
        linecolor=COLORS["border"],
        tickfont=dict(size=10, color=COLORS["text_secondary"]),
        showgrid=True,
    ),
    yaxis=dict(
        gridcolor="#F3F4F6",
        linecolor=COLORS["border"],
        tickfont=dict(size=10, color=COLORS["text_secondary"]),
        showgrid=True,
    ),
    title=dict(
        font=dict(family="Open Sans, sans-serif", size=12, color=COLORS["text_secondary"]),
        x=0.01, xanchor="left",
    ),
    hoverlabel=dict(
        bgcolor=COLORS["bg_card"],
        bordercolor=COLORS["border"],
        font=dict(family="Open Sans, sans-serif", size=11),
    ),
)


def _chart_layout(**overrides):
    base = _LAYOUT.copy()
    base.update(overrides)
    return base


# ── Page ─────────────────────────────────────────────────────────────────────

filters = get_filters()
date_from = filters["date_from"]
date_to   = filters["date_to"]

page_header("Dashboard AlyBot", "Resumen operacional del bot de WhatsApp")

# ── KPI row ───────────────────────────────────────────────────────────────────
try:
    kpis    = db.get_user_kpis(date_from, date_to)
    n_msg   = db.get_messages_count(date_from, date_to)
    conv_m  = db.get_conversation_metrics(date_from, date_to)
    deltas  = db.get_kpi_deltas(date_from, date_to)
except Exception as e:
    st.error(f"Error de base de datos: {e}")
    st.stop()

delta_label = t("vs_prev_period")

kpi_row([
    {
        "label":       t("n_users"),
        "value":       kpis["n_users"],
        "delta":       deltas.get("users_delta"),
        "delta_label": delta_label,
    },
    {
        "label":       t("n_sessions"),
        "value":       kpis["n_sessions"],
        "delta":       deltas.get("sessions_delta"),
        "delta_label": delta_label,
    },
    {
        "label":       t("n_messages"),
        "value":       n_msg,
        "delta":       deltas.get("messages_delta"),
        "delta_label": delta_label,
    },
    {
        "label":       t("avg_msg_per_conv"),
        "value":       conv_m["avg_msg_per_conv"],
        "delta":       None,
        "delta_label": "",
    },
])

st.markdown("<div style='margin:1.5rem 0 0.5rem'></div>", unsafe_allow_html=True)

# ── Growth chart (daily messages) ─────────────────────────────────────────────
section_label(t("activity_over_time"))

try:
    df_daily = db.get_daily_activity(date_from, date_to)
except Exception:
    df_daily = pd.DataFrame()

if df_daily.empty:
    st.info(t("no_data"))
else:
    df_daily["day"] = pd.to_datetime(df_daily["day"])

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df_daily["day"],
        y=df_daily["messages"],
        mode="lines",
        name=t("messages_axis"),
        line=dict(color=COLORS["accent"], width=2.5, shape="spline"),
        fill="tozeroy",
        fillcolor="rgba(2,115,229,0.08)",
        hovertemplate="%{x|%d %b}<br><b>%{y}</b> mensajes<extra></extra>",
    ))
    fig.add_trace(go.Scatter(
        x=df_daily["day"],
        y=df_daily["users"],
        mode="lines",
        name=t("n_users"),
        line=dict(color=COLORS["yellow"], width=2, dash="dot"),
        hovertemplate="%{x|%d %b}<br><b>%{y}</b> usuarios<extra></extra>",
        yaxis="y2",
    ))
    fig.update_layout(
        **_chart_layout(
            title=dict(text=t("activity_over_time"), font=dict(size=12, color=COLORS["text_secondary"]), x=0.01, xanchor="left"),
            height=260,
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1,
                        font=dict(size=10)),
            yaxis2=dict(
                overlaying="y", side="right",
                gridcolor="rgba(0,0,0,0)", showgrid=False,
                tickfont=dict(size=10, color=COLORS["text_secondary"]),
            ),
            hovermode="x unified",
        )
    )
    st.plotly_chart(fig, use_container_width=True)

st.markdown("<div style='margin:0.5rem 0'></div>", unsafe_allow_html=True)

# ── Activity heatmap (hour × day-of-week) ────────────────────────────────────
section_label(t("activity_heatmap"))

try:
    df_heat = db.get_activity_heatmap(date_from, date_to)
except Exception:
    df_heat = pd.DataFrame()

col_heat, col_stats = st.columns([3, 1])

with col_heat:
    if df_heat.empty:
        st.info(t("no_data"))
    else:
        days_es  = ["Dom", "Lun", "Mar", "Mié", "Jue", "Vie", "Sáb"]
        days_en  = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
        day_labels = days_en if st.session_state.get("lang") == "en" else days_es

        # Build 7×24 matrix
        matrix = np.zeros((7, 24), dtype=int)
        for _, row in df_heat.iterrows():
            matrix[int(row["dow"]), int(row["hour"])] += int(row["messages"])

        fig_h = px.imshow(
            matrix,
            labels=dict(x=t("hour_axis"), y="", color=t("messages_axis")),
            x=[str(h) for h in range(24)],
            y=day_labels,
            color_continuous_scale=[
                [0.0,  "#F0F2F5"],
                [0.2,  "#BFDBFE"],
                [0.5,  "#3B82F6"],
                [0.8,  "#1D4ED8"],
                [1.0,  COLORS["navy"]],
            ],
            aspect="auto",
        )
        fig_h.update_layout(
            paper_bgcolor=COLORS["bg_card"],
            plot_bgcolor=COLORS["bg_card"],
            font=dict(family="Open Sans, sans-serif", size=10),
            margin=dict(l=8, r=8, t=30, b=8),
            height=220,
            coloraxis_showscale=False,
            title=dict(text=t("activity_heatmap"), font=dict(size=12, color=COLORS["text_secondary"]), x=0.01),
        )
        fig_h.update_traces(
            hovertemplate="<b>%{y}</b> %{x}h<br>%{z} mensajes<extra></extra>",
        )
        st.plotly_chart(fig_h, use_container_width=True)

with col_stats:
    if not df_heat.empty:
        # Peak hour
        hour_totals = df_heat.groupby("hour")["messages"].sum()
        peak_hour   = int(hour_totals.idxmax())
        # Most active day
        dow_totals  = df_heat.groupby("dow")["messages"].sum()
        peak_dow    = int(dow_totals.idxmax())
        day_name    = (days_en if st.session_state.get("lang") == "en" else days_es)[peak_dow]

        st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)
        st.metric(t("peak_hour"),  f"{peak_hour:02d}:00")
        st.metric(t("peak_day"),   day_name)
        st.metric(t("total_convs"), f"{conv_m['total_conversations']:,}")
