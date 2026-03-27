"""Página Usuarios — demografía y distribución horaria."""

import pandas as pd
import streamlit as st

from utils.i18n import t
from utils import db
from utils.styles import COLORS, page_header, section_label
from components.charts import bar_h, donut, choropleth, bar_v
from components.filters import get_filters

filters  = get_filters()
date_from = filters["date_from"]
date_to   = filters["date_to"]

page_header(t("users_page_title"), t("users_page_sub"))

# ── Demographics row ─────────────────────────────────────────────────────────
section_label(t("demographics"))

df_country = db.get_users_by_country(date_from, date_to)
df_gender  = db.get_users_by_gender(date_from, date_to)
df_region  = db.get_users_by_region(date_from, date_to)

col1, col2, col3 = st.columns([1.4, 1, 1.2])

with col1:
    if df_country.empty:
        st.info(t("no_data"))
    else:
        # Try choropleth first, fallback to bar
        try:
            fig = choropleth(df_country, "country", "n_users", t("by_country"), height=260)
            st.plotly_chart(fig, use_container_width=True)
        except Exception:
            fig = bar_h(df_country, "n_users", "country", t("by_country"), height=260)
            st.plotly_chart(fig, use_container_width=True)

with col2:
    if df_gender.empty:
        st.info(t("no_data"))
    else:
        fig = donut(df_gender, "gender", "n_users", t("by_gender"), height=260)
        st.plotly_chart(fig, use_container_width=True)

with col3:
    if df_region.empty:
        st.info(t("no_data"))
    else:
        fig = bar_h(df_region, "n_users", "region", t("by_region"),
                    color=COLORS["yellow"], height=260)
        st.plotly_chart(fig, use_container_width=True)

st.markdown("<div style='margin:0.75rem 0'></div>", unsafe_allow_html=True)

# ── Hourly distribution ───────────────────────────────────────────────────────
section_label(t("hourly_dist"))

try:
    df_hour = db.get_hourly_distribution(date_from, date_to)
except Exception:
    df_hour = pd.DataFrame()

if df_hour.empty:
    st.info(t("no_data"))
else:
    df_hour["hour"] = df_hour["hour"].astype(float).astype(int)
    all_hours = pd.DataFrame({"hour": range(24)})
    df_hour   = all_hours.merge(df_hour, on="hour", how="left").fillna(0)
    df_hour["messages"] = df_hour["messages"].astype(int)

    # Color bars by intensity
    max_val = df_hour["messages"].max()
    df_hour["color"] = df_hour["messages"].apply(
        lambda v: COLORS["accent"] if v == max_val else (
            "#93C5FD" if v >= max_val * 0.6 else "#DBEAFE"
        )
    )

    import plotly.graph_objects as go
    fig = go.Figure(go.Bar(
        x=df_hour["hour"],
        y=df_hour["messages"],
        marker_color=df_hour["color"],
        marker_line_width=0,
        hovertemplate="%{x}:00h<br><b>%{y}</b> mensajes<extra></extra>",
    ))
    fig.update_layout(
        paper_bgcolor=COLORS["bg_card"],
        plot_bgcolor=COLORS["bg_card"],
        font=dict(family="Open Sans, sans-serif", size=11),
        height=220,
        bargap=0.25,
        margin=dict(l=8, r=8, t=40, b=8),
        title=dict(text=t("time_of_day"), font=dict(size=12, color=COLORS["text_secondary"]), x=0.01),
        xaxis=dict(
            tickmode="linear", dtick=1,
            gridcolor="#F3F4F6", linecolor=COLORS["border"],
            tickfont=dict(size=10, color=COLORS["text_secondary"]),
            title=t("hour_axis"),
        ),
        yaxis=dict(
            gridcolor="#F3F4F6", linecolor=COLORS["border"],
            tickfont=dict(size=10, color=COLORS["text_secondary"]),
        ),
        hoverlabel=dict(bgcolor=COLORS["bg_card"], bordercolor=COLORS["border"],
                        font=dict(family="Open Sans, sans-serif", size=11)),
    )
    st.plotly_chart(fig, use_container_width=True)

# ── Country table (if many countries) ────────────────────────────────────────
if not df_country.empty and len(df_country) > 5:
    st.markdown("<div style='margin:0.75rem 0'></div>", unsafe_allow_html=True)
    section_label(t("by_country") + " — detalle")
    st.dataframe(
        df_country.rename(columns={"country": "País", "n_users": "Usuarios"}),
        use_container_width=True,
        hide_index=True,
    )
