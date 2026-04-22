"""Sidebar — logo, nav, filters, export. Writes to st.session_state for all pages."""

import datetime
import io
import streamlit as st
from utils.i18n import t
from utils.db import get_interactions_export


# Material Symbols icons (rendered natively by Streamlit — consistent mono line style)
NAV_ITEMS = [
    ("analysis", [
        ("pages/overview.py",    "nav_home",        ":material/dashboard:"),
        ("pages/usuarios.py",    "nav_users",       ":material/group:"),
    ]),
    ("operation", [
        ("pages/alertas.py",     "nav_alerts",      ":material/warning:"),
        ("pages/leaderboard.py", "nav_leaderboard", ":material/emoji_events:"),
    ]),
]


def _render_logo():
    st.markdown(
        """
        <div style="padding:0.5rem 0 1.25rem;display:flex;align-items:center;gap:0.65rem">
            <div style="
                width:34px;height:34px;border-radius:9px;
                background:linear-gradient(135deg,#0273e5 0%,#110079 100%);
                display:flex;align-items:center;justify-content:center;
                box-shadow:0 2px 6px rgba(2,115,229,0.25)">
                <span style="font-family:'Oswald',sans-serif;font-size:1.1rem;
                    font-weight:700;color:#FFFFFF;letter-spacing:0.02em">A</span>
            </div>
            <div style="display:flex;flex-direction:column;line-height:1.1">
                <span style="font-family:'Oswald',sans-serif;font-size:1.35rem;
                    font-weight:600;color:#0C1214;letter-spacing:0.02em">Aly</span>
                <span style="font-family:'Open Sans',sans-serif;font-size:0.66rem;
                    color:#9CA3AF;text-transform:uppercase;letter-spacing:0.09em;
                    margin-top:0.1rem">Dashboard</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _render_nav():
    """Custom grouped navigation using st.page_link with Material icons."""
    section_labels = {
        "analysis":  {"es": "Análisis",  "en": "Analysis"},
        "operation": {"es": "Operación", "en": "Operations"},
    }
    lang = st.session_state.get("lang", "es")

    for section_id, items in NAV_ITEMS:
        label = section_labels[section_id][lang]
        st.markdown(
            f'<div class="nav-section">{label}</div>',
            unsafe_allow_html=True,
        )
        for page_path, label_key, icon in items:
            st.page_link(page_path, label=t(label_key), icon=icon)

    st.markdown(
        '<hr style="margin:1rem 0 0.75rem">',
        unsafe_allow_html=True,
    )


def render_sidebar():
    """Render the global sidebar. Pages read filters from st.session_state."""
    with st.sidebar:
        _render_logo()
        _render_nav()

        # ── Language toggle ───────────────────────────────────────────────────
        if "lang_toggle" not in st.session_state:
            st.session_state.lang_toggle = st.session_state.get("lang", "es") == "en"

        def _on_lang_change():
            st.session_state.lang = "en" if st.session_state.lang_toggle else "es"

        st.toggle("EN / ES", key="lang_toggle", on_change=_on_lang_change)

        st.markdown(
            '<hr style="margin:0.75rem 0">',
            unsafe_allow_html=True,
        )

        # ── Date filters ──────────────────────────────────────────────────────
        st.markdown(
            '<p style="font-family:\'Open Sans\',sans-serif;font-size:0.66rem;'
            'font-weight:700;text-transform:uppercase;letter-spacing:0.1em;'
            'color:#9CA3AF;margin-bottom:0.5rem">' + t("filters") + '</p>',
            unsafe_allow_html=True,
        )

        today = datetime.date.today()

        if "filter_from" not in st.session_state:
            st.session_state["filter_from"] = today - datetime.timedelta(days=30)
        if "filter_to" not in st.session_state:
            st.session_state["filter_to"] = today

        date_from = st.date_input(t("date_from"), key="filter_from")
        date_to   = st.date_input(t("date_to"),   key="filter_to")

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
            '<hr style="margin:0.75rem 0">',
            unsafe_allow_html=True,
        )

        # ── Export ────────────────────────────────────────────────────────────
        date_to_excl = date_to + datetime.timedelta(days=1)

        st.markdown(
            '<p style="font-family:\'Open Sans\',sans-serif;font-size:0.66rem;'
            'font-weight:700;text-transform:uppercase;letter-spacing:0.1em;'
            'color:#9CA3AF;margin-bottom:0.5rem">' + t("export_excel") + '</p>',
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
            f'<div style="margin-top:1.25rem;padding:0.5rem 0;'
            f'font-family:\'Open Sans\',sans-serif;font-size:0.68rem;'
            f'color:#9CA3AF;border-top:1px solid #E5E7EB">'
            f'{t("last_updated")}<br>'
            f'<span style="color:#6B7280;font-weight:500;font-variant-numeric:tabular-nums">'
            f'{datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}</span>'
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
