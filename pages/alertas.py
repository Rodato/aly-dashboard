"""Página Alertas — flags detectados en conversations_data."""

import streamlit as st
import pandas as pd

from utils.i18n import t
from utils import db
from utils.styles import COLORS, page_header, section_label
from components.kpi_row import render as kpi_row
from components.filters import get_filters

filters   = get_filters()
date_from = filters["date_from"]
date_to   = filters["date_to"]

page_header(t("alerts_page_title"), t("alerts_page_sub"))

# ── Load flags ────────────────────────────────────────────────────────────────
try:
    df_flags = db.get_flags_data(date_from, date_to)
except Exception as e:
    st.error(f"Error de base de datos: {e}")
    df_flags = pd.DataFrame()

# ── Classify flags ────────────────────────────────────────────────────────────
# The `flags` column is text — try to classify as red/orange/other
def _classify_flag(val: str) -> str:
    if not val or not isinstance(val, str):
        return "other"
    v = val.lower()
    if "red" in v or "rojo" in v or "critico" in v or "crítico" in v:
        return "red"
    if "orange" in v or "naranja" in v or "warning" in v or "advertencia" in v:
        return "orange"
    return "other"

if not df_flags.empty:
    df_flags["_tipo"] = df_flags["flags"].apply(_classify_flag)
    n_red    = int((df_flags["_tipo"] == "red").sum())
    n_orange = int((df_flags["_tipo"] == "orange").sum())
    n_other  = int((df_flags["_tipo"] == "other").sum())
    n_total  = len(df_flags)
else:
    n_red = n_orange = n_other = n_total = 0

# ── KPI row ───────────────────────────────────────────────────────────────────
kpi_row([
    {"label": t("red_flags"),    "value": n_red,    "delta": None},
    {"label": t("orange_flags"), "value": n_orange, "delta": None},
    {"label": t("open_flags"),   "value": n_total,  "delta": None},
])
st.markdown("<div style='margin:1rem 0 0.5rem'></div>", unsafe_allow_html=True)

# ── Flags table ───────────────────────────────────────────────────────────────
section_label(t("flags_title"))

if df_flags.empty:
    st.markdown(
        f"""
        <div style="background:{COLORS['bg_card']};border:1px solid {COLORS['border']};
             border-radius:10px;padding:2.5rem 1.5rem;text-align:center;margin-top:0.5rem">
            <div style="font-size:2.5rem;margin-bottom:0.75rem">🚩</div>
            <p style="font-family:'Open Sans',sans-serif;font-size:1rem;
               color:{COLORS['text']};font-weight:600;margin:0 0 0.35rem">
                {t('no_flags')}
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
else:
    # Build display dataframe
    display = df_flags[["conversation_date", "conversation_id", "user_number", "flags"]].copy()

    # Add emoji prefix to flag value
    def _fmt_flag(val):
        t_ = _classify_flag(val)
        if t_ == "red":
            return f"🔴 {val}"
        if t_ == "orange":
            return f"🟠 {val}"
        return f"⚪ {val}"

    display["flags"] = display["flags"].apply(_fmt_flag)
    display["conversation_date"] = pd.to_datetime(display["conversation_date"]).dt.strftime("%Y-%m-%d %H:%M")

    display = display.rename(columns={
        "conversation_date": t("date_col"),
        "conversation_id":   "Conversación",
        "user_number":       "Usuario",
        "flags":             t("type_col"),
    })

    st.dataframe(display, use_container_width=True, hide_index=True)

    # Expandable: show summary for flagged conversations
    st.markdown("<div style='margin:1rem 0 0.5rem'></div>", unsafe_allow_html=True)
    section_label("Detalle de conversaciones")

    for _, row in df_flags.iterrows():
        conv_id = str(row.get("conversation_id", "—"))[:20]
        fecha   = str(row.get("conversation_date", ""))[:16]
        flag    = str(row.get("flags", ""))
        summary = str(row.get("summary", "")) if row.get("summary") else ""

        with st.expander(f"{_classify_flag(flag) == 'red' and '🔴' or '🟠'}  {fecha}  ·  `{conv_id}`"):
            st.markdown(
                f'<p style="font-family:\'Open Sans\',sans-serif;font-size:0.78rem;'
                f'font-weight:700;text-transform:uppercase;color:{COLORS["text_muted"]};margin:0 0 0.25rem">'
                f'Flag</p>'
                f'<p style="font-family:\'Open Sans\',sans-serif;font-size:0.875rem;'
                f'color:{COLORS["red"]};margin:0 0 0.75rem">{flag}</p>',
                unsafe_allow_html=True,
            )
            if summary:
                st.markdown(
                    f'<p style="font-family:\'Open Sans\',sans-serif;font-size:0.78rem;'
                    f'font-weight:700;text-transform:uppercase;color:{COLORS["text_muted"]};margin:0 0 0.25rem">'
                    f'Resumen</p>'
                    f'<p style="font-family:\'Open Sans\',sans-serif;font-size:0.875rem;'
                    f'color:{COLORS["text"]};line-height:1.6;margin:0">{summary}</p>',
                    unsafe_allow_html=True,
                )
