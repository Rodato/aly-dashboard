"""USERS section — KPIs, demographics, time-of-day, region chart."""

import pandas as pd
import streamlit as st
import plotly.express as px
from utils.i18n import t
from utils import db
from utils.styles import COLORS, section_header

# Plotly theme matching Bloomberg Terminal style
_LAYOUT = dict(
    paper_bgcolor=COLORS["bg_card"],
    plot_bgcolor=COLORS["bg_card"],
    font=dict(family="Open Sans, sans-serif", size=11, color=COLORS["text"]),
    margin=dict(l=4, r=4, t=40, b=4),
    xaxis=dict(
        gridcolor=COLORS["border"],
        linecolor=COLORS["border"],
        tickfont=dict(family="Open Sans, sans-serif", size=10, color=COLORS["text_secondary"]),
    ),
    yaxis=dict(
        gridcolor=COLORS["border"],
        linecolor=COLORS["border"],
        tickfont=dict(family="Open Sans, sans-serif", size=10, color=COLORS["text_secondary"]),
    ),
    title=dict(font=dict(family="Open Sans, sans-serif", size=12, color=COLORS["text_secondary"]),
               x=0, xanchor="left"),
)


def render(filters: dict):
    section_header(t("users_title"), COLORS["accent"])

    date_from = filters.get("date_from")
    date_to = filters.get("date_to")

    # ── KPIs ─────────────────────────────────────────────────────────────
    try:
        kpis = db.get_user_kpis(date_from, date_to)
        n_messages = db.get_messages_count(date_from, date_to)
    except Exception as e:
        st.error(f"DB error: {e}")
        return

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(t("n_users"), kpis["n_users"])
    with col2:
        st.metric(t("n_sessions"), kpis["n_sessions"])
    with col3:
        st.metric(t("n_messages"), n_messages)

    st.markdown("<div style='margin:0.75rem 0'></div>", unsafe_allow_html=True)

    # ── Who is using it? ─────────────────────────────────────────────────
    section_header(t("who_is_using"), COLORS["blue"])

    df_country = db.get_users_by_country(date_from, date_to)
    df_gender = db.get_users_by_gender(date_from, date_to)

    col_a, col_b = st.columns(2)

    with col_a:
        if df_country.empty:
            st.info(t("no_data"))
        else:
            fig = px.bar(
                df_country,
                x="n_users", y="country", orientation="h",
                labels={"n_users": t("n_users"), "country": ""},
                title=t("by_country"),
                color_discrete_sequence=[COLORS["accent"]],
            )
            fig.update_layout(**_LAYOUT, yaxis_categoryorder="total ascending")
            st.plotly_chart(fig, use_container_width=True)

    with col_b:
        if df_gender.empty:
            st.info(t("no_data"))
        else:
            fig = px.pie(
                df_gender, names="gender", values="n_users",
                title=t("by_gender"),
                color_discrete_sequence=[COLORS["accent"], COLORS["green"], COLORS["blue"]],
                hole=0.45,
            )
            fig.update_traces(
                textfont=dict(family="Open Sans, sans-serif", size=11),
                marker=dict(line=dict(color=COLORS["bg_card"], width=2)),
            )
            fig.update_layout(**_LAYOUT)
            st.plotly_chart(fig, use_container_width=True)

    st.markdown("<div style='margin:0.25rem 0'></div>", unsafe_allow_html=True)

    # ── Specifics ─────────────────────────────────────────────────────────
    section_header(t("specifics"), COLORS["green"])

    col_c, col_d = st.columns(2)
    with col_c:
        _render_time_of_day(date_from, date_to)
    with col_d:
        _render_region_chart(date_from, date_to)


def _render_time_of_day(date_from, date_to):
    df = db.get_hourly_distribution(date_from, date_to)
    if df.empty:
        st.info(t("no_data"))
        return

    df["hour"] = df["hour"].astype(float).astype(int)
    all_hours = pd.DataFrame({"hour": range(24)})
    df = all_hours.merge(df, on="hour", how="left").fillna(0)
    df["messages"] = df["messages"].astype(int)

    fig = px.bar(
        df, x="hour", y="messages",
        labels={"hour": t("hour_axis"), "messages": t("messages_axis")},
        title=t("time_of_day"),
        color_discrete_sequence=[COLORS["accent"]],
    )
    fig.update_layout(**_LAYOUT, bargap=0.3, xaxis_dtick=1)
    st.plotly_chart(fig, use_container_width=True)


def _render_region_chart(date_from, date_to):
    df = db.get_users_by_region(date_from, date_to)
    if df.empty:
        st.info(t("no_data"))
        return

    fig = px.bar(
        df, x="n_users", y="region", orientation="h",
        labels={"n_users": t("n_users"), "region": ""},
        title=t("by_region"),
        color_discrete_sequence=[COLORS["green"]],
    )
    fig.update_layout(**_LAYOUT, yaxis_categoryorder="total ascending")
    st.plotly_chart(fig, use_container_width=True)
