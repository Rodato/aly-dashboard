"""Página Usuarios — KPIs demográficos + mapa Colombia + ranking lateral."""

import streamlit as st

from utils.i18n import t
from utils import db
from utils.styles import COLORS, page_header, card_header, stat_list
from components.charts import (
    bar_h, choropleth_colombia,
    colombia_region_lookup, _normalize_region,
)
from components.kpi_row import render as kpi_row, ICONS as KPI_ICONS
from components.filters import get_filters


filters   = get_filters()
date_from = filters["date_from"]
date_to   = filters["date_to"]

page_header(t("users_page_title"), t("users_page_sub"))


# ── Data fetch ───────────────────────────────────────────────────────────────
try:
    df_region = db.get_users_by_region(date_from, date_to)
    kpis      = db.get_user_kpis(date_from, date_to)
    conv_m    = db.get_conversation_metrics(date_from, date_to)
    deltas    = db.get_kpi_deltas(date_from, date_to)
except Exception as e:
    st.error(f"Error de base de datos: {e}")
    st.stop()


# ── KPI row ──────────────────────────────────────────────────────────────────
n_regions = len(df_region) if not df_region.empty else 0

kpi_row([
    {"label": t("n_users"),     "value": kpis["n_users"],
     "delta": deltas.get("users_delta"), "delta_label": t("vs_prev_period"),
     "accent": "accent", "icon": "users"},
    {"label": t("kpi_regions"), "value": n_regions,
     "delta": None, "accent": "navy", "icon": "activity"},
    {"label": "Msg / usuario",  "value": conv_m["avg_msg_per_user"],
     "delta": None, "accent": "yellow", "icon": "send"},
])

st.markdown("<div style='margin:1.4rem 0 0.25rem'></div>", unsafe_allow_html=True)


# ── Mapa + panel lateral ─────────────────────────────────────────────────────
lookup       = colombia_region_lookup()
total_depts  = 33  # GeoJSON tiene 33 features

if df_region.empty:
    n_covered = 0
    unmatched = []
else:
    matched_mask = df_region["region"].apply(
        lambda r: bool(r) and _normalize_region(r) in lookup
    )
    n_covered = int(matched_mask.sum())
    unmatched = sorted({
        str(r) for r in df_region.loc[~matched_mask, "region"] if r
    })

pct_covered = round(n_covered / total_depts * 100) if total_depts else 0

col_map, col_side = st.columns([2, 1])

with col_map:
    card_header(
        title=t("region_heatmap"),
        subtitle=f"{kpis['n_users']} usuarios · {n_regions} regiones",
        icon_svg=KPI_ICONS["activity"],
    )
    if df_region.empty:
        st.info(t("no_data"))
    else:
        fig_col = choropleth_colombia(df_region, "region", "n_users", height=460)
        st.plotly_chart(fig_col, use_container_width=True)
        if unmatched:
            st.caption(f"⚠️ Regiones sin mapear: {', '.join(unmatched)}")

with col_side:
    card_header(title=t("coverage"), icon_svg=KPI_ICONS["chart"])
    stat_list([
        {"label": t("coverage_depts"), "value": f"{n_covered} / {total_depts}"},
        {"label": t("coverage_pct"),   "value": f"{pct_covered}%"},
    ])

    st.markdown("<div style='margin:0.9rem 0 0'></div>", unsafe_allow_html=True)

    card_header(title=t("region_ranking"), icon_svg=KPI_ICONS["users"])
    if df_region.empty:
        st.info(t("no_data"))
    else:
        top = df_region.head(10)
        fig_rank = bar_h(
            top, x="n_users", y="region",
            height=max(220, 36 * len(top)),
        )
        st.plotly_chart(fig_rank, use_container_width=True)
