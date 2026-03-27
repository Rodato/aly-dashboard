"""Placeholder cards for future sections: FLAGS, BUGS, INSIGHTS, REPORTING."""

import streamlit as st
from utils.i18n import t
from utils.styles import COLORS, section_header


def _card(title: str, color: str, desc: str, requires: str = "", metrics=None):
    section_header(f"{title}  ·  {t('coming_soon')}", color)

    if metrics:
        cols = st.columns(len(metrics))
        for col, (label, val) in zip(cols, metrics):
            with col:
                st.metric(label, val)

    st.info(desc)

    if requires:
        st.markdown(
            f"<span style='font-family:'Open Sans',sans-serif;font-size:0.75rem;"
            f"color:{COLORS['text_muted']}'>🔧 {requires}</span>",
            unsafe_allow_html=True,
        )

    st.markdown("<div style='margin:0.5rem 0'></div>", unsafe_allow_html=True)


def render_flags():
    _card(
        title=t("flags_title"),
        color=COLORS["red"],
        desc=t("flags_desc"),
        requires=t("flags_requires"),
        metrics=[
            ("🔴 Red flags", "—"),
            ("🟠 Orange flags", "—"),
            ("❓ Unsolved", "—"),
        ],
    )


def render_bugs():
    _card(
        title=t("bugs_title"),
        color=COLORS["red"],
        desc=t("bugs_desc"),
        metrics=[("🐛 Bugs", "—")],
    )


def render_insights():
    _card(
        title=t("insights_title"),
        color=COLORS["green"],
        desc=t("insights_desc"),
        requires=t("insights_requires"),
    )
    with st.expander("Preview structure"):
        c_sec = COLORS["text_secondary"]
        c_acc = COLORS["accent"]
        for i in range(1, 4):
            st.markdown(
                f"<span style='font-family:'Open Sans',sans-serif;font-size:0.85rem;color:{c_sec}'>"
                f"<b style='color:{c_acc}'>INSIGHT {i}:</b> —</span>",
                unsafe_allow_html=True,
            )


def render_reporting():
    _card(
        title=t("reporting_title"),
        color=COLORS["green"],
        desc=t("reporting_desc"),
        requires=t("reporting_requires"),
    )
    with st.expander("Preview structure"):
        c_sec = COLORS["text_secondary"]
        c_acc = COLORS["accent"]
        for label in ["Top topics", "Top questions"]:
            st.markdown(
                f"<span style='font-family:'Open Sans',sans-serif;font-size:0.85rem;color:{c_sec}'>"
                f"<b style='color:{c_acc}'>{label}:</b> —</span>",
                unsafe_allow_html=True,
            )
