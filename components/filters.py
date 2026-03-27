"""Sidebar filters — returns a dict consumed by all sections."""

import datetime
import io
import streamlit as st
from utils.i18n import t
from utils.db import get_interactions_export


def render_sidebar() -> dict:
    """Render sidebar controls and return active filter state."""
    with st.sidebar:
        # ── Language toggle ───────────────────────────────────────────────
        st.markdown("---")
        if "lang_toggle" not in st.session_state:
            st.session_state.lang_toggle = st.session_state.get("lang", "es") == "en"

        def _on_lang_change():
            st.session_state.lang = "en" if st.session_state.lang_toggle else "es"

        st.toggle(
            "EN",
            key="lang_toggle",
            on_change=_on_lang_change,
        )

        st.markdown("---")
        st.subheader(t("filters"))

        # ── Date range ────────────────────────────────────────────────────
        today = datetime.date.today()
        default_from = today - datetime.timedelta(days=30)

        date_from = st.date_input(t("date_from"), value=default_from, key="filter_from")
        date_to = st.date_input(t("date_to"), value=today, key="filter_to")

        # Normalise: date_to is exclusive upper bound
        date_to_exclusive = date_to + datetime.timedelta(days=1)

        # ── Program ───────────────────────────────────────────────────────
        program = st.selectbox(
            t("program"),
            options=[t("all"), "co"],
            key="filter_program",
        )

        st.markdown("---")

        # ── Export Excel ──────────────────────────────────────────────────
        st.markdown(f"**{t('export_excel')}**")
        st.caption(t("export_hint"))
        if st.button(t("export_excel"), width='stretch'):
            df_export = get_interactions_export(
                date_from=str(date_from),
                date_to=str(date_to_exclusive),
            )
            buf = io.BytesIO()
            df_export.to_excel(buf, index=False, engine="openpyxl")
            buf.seek(0)
            st.download_button(
                label=t("export_excel"),
                data=buf,
                file_name=f"apapacho_export_{today}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                width='stretch',
            )

    return {
        "date_from": str(date_from),
        "date_to": str(date_to_exclusive),
        "program": None if program == t("all") else program,
    }
