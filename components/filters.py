"""Sidebar — logo, filters, export. Writes to st.session_state for all pages."""

import datetime
import io
import streamlit as st
from utils.i18n import t
from utils.db import get_interactions_export


def render_sidebar():
    """Render the global sidebar. Pages read filters from st.session_state."""
    with st.sidebar:
        # ── Branding ──────────────────────────────────────────────────────────
        st.markdown(
            """
            <div style="padding:0.5rem 0 1rem">
                <span style="font-family:'Oswald',sans-serif;font-size:1.4rem;
                      font-weight:600;color:#FFFFFF;letter-spacing:0.02em">
                    🤖 AlyBot
                </span><br>
                <span style="font-family:'Open Sans',sans-serif;font-size:0.72rem;
                      color:#475569;text-transform:uppercase;letter-spacing:0.08em">
                    Dashboard
                </span>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            '<hr style="border-color:#1E2A30;margin:0 0 1rem">',
            unsafe_allow_html=True,
        )

        # ── Language toggle ───────────────────────────────────────────────────
        if "lang_toggle" not in st.session_state:
            st.session_state.lang_toggle = st.session_state.get("lang", "es") == "en"

        def _on_lang_change():
            st.session_state.lang = "en" if st.session_state.lang_toggle else "es"

        st.toggle("EN / ES", key="lang_toggle", on_change=_on_lang_change)

        st.markdown(
            '<hr style="border-color:#1E2A30;margin:0.75rem 0">',
            unsafe_allow_html=True,
        )

        # ── Date filters ──────────────────────────────────────────────────────
        st.markdown(
            '<p style="font-family:\'Open Sans\',sans-serif;font-size:0.7rem;'
            'font-weight:700;text-transform:uppercase;letter-spacing:0.08em;'
            'color:#475569;margin-bottom:0.5rem">' + t("filters") + '</p>',
            unsafe_allow_html=True,
        )

        today = datetime.date.today()
        default_from = today - datetime.timedelta(days=30)

        date_from = st.date_input(t("date_from"), value=default_from, key="filter_from")
        date_to   = st.date_input(t("date_to"),   value=today,        key="filter_to")

        # Quick-select presets
        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("7d", use_container_width=True):
                st.session_state.filter_from = today - datetime.timedelta(days=7)
                st.session_state.filter_to   = today
                st.rerun()
        with col_b:
            if st.button("30d", use_container_width=True):
                st.session_state.filter_from = today - datetime.timedelta(days=30)
                st.session_state.filter_to   = today
                st.rerun()

        st.markdown(
            '<hr style="border-color:#1E2A30;margin:0.75rem 0">',
            unsafe_allow_html=True,
        )

        # ── Export ────────────────────────────────────────────────────────────
        date_to_excl = date_to + datetime.timedelta(days=1)

        st.markdown(
            '<p style="font-family:\'Open Sans\',sans-serif;font-size:0.7rem;'
            'font-weight:700;text-transform:uppercase;letter-spacing:0.08em;'
            'color:#475569;margin-bottom:0.5rem">' + t("export_excel") + '</p>',
            unsafe_allow_html=True,
        )
        if st.button(t("export_excel"), use_container_width=True):
            df_export = get_interactions_export(
                date_from=str(date_from),
                date_to=str(date_to_excl),
            )
            buf = io.BytesIO()
            df_export.to_excel(buf, index=False, engine="openpyxl")
            buf.seek(0)
            st.download_button(
                label=t("export_excel"),
                data=buf,
                file_name=f"apapacho_export_{today}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True,
            )

        # ── Footer ────────────────────────────────────────────────────────────
        st.markdown(
            f'<div style="position:fixed;bottom:1rem;font-family:\'Open Sans\',sans-serif;'
            f'font-size:0.65rem;color:#334155">'
            f'{t("last_updated")}: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}'
            f'</div>',
            unsafe_allow_html=True,
        )


def get_filters() -> dict:
    """Return the current filter values from session_state (for use in pages)."""
    date_from = st.session_state.get("filter_from", datetime.date.today() - datetime.timedelta(days=30))
    date_to   = st.session_state.get("filter_to",   datetime.date.today())
    date_to_excl = date_to + datetime.timedelta(days=1)
    return {
        "date_from": str(date_from),
        "date_to":   str(date_to_excl),
    }
