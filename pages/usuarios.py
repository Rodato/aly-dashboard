"""Página Usuarios — demografía, mapa de distribución y arcos por región."""

import pandas as pd
import streamlit as st

from utils.i18n import t
from utils import db
from utils.styles import COLORS, page_header, card_header, arc_row
from components.charts import bar_h, choropleth
from components.kpi_row import render as kpi_row, ICONS as KPI_ICONS
from components.filters import get_filters


filters   = get_filters()
date_from = filters["date_from"]
date_to   = filters["date_to"]

page_header(t("users_page_title"), t("users_page_sub"))


# ── Data fetch ───────────────────────────────────────────────────────────────
try:
    df_country = db.get_users_by_country(date_from, date_to)
    df_region  = db.get_users_by_region(date_from, date_to)
    kpis       = db.get_user_kpis(date_from, date_to)
    conv_m     = db.get_conversation_metrics(date_from, date_to)
    deltas     = db.get_kpi_deltas(date_from, date_to)
except Exception as e:
    st.error(f"Error de base de datos: {e}")
    st.stop()


# ── KPI row ──────────────────────────────────────────────────────────────────
n_countries = len(df_country) if not df_country.empty else 0
n_regions   = len(df_region)  if not df_region.empty  else 0

kpi_row([
    {"label": t("n_users"),      "value": kpis["n_users"],
     "delta": deltas.get("users_delta"), "delta_label": t("vs_prev_period"),
     "accent": "accent", "icon": "users"},
    {"label": t("kpi_countries"),"value": n_countries,
     "delta": None, "accent": "navy",   "icon": "activity"},
    {"label": t("kpi_regions"),  "value": n_regions,
     "delta": None, "accent": "positive", "icon": "chart"},
    {"label": "Msg / usuario",   "value": conv_m["avg_msg_per_user"],
     "delta": None, "accent": "yellow", "icon": "send"},
])

st.markdown("<div style='margin:1.4rem 0 0.25rem'></div>", unsafe_allow_html=True)


# ── Geo distribution: map + arc gauges ───────────────────────────────────────
card_header(
    title=t("country_map"),
    subtitle=f"{kpis['n_users']} usuarios · {n_countries} países · {n_regions} regiones",
    icon_svg=KPI_ICONS["activity"],
)

if df_country.empty and df_region.empty:
    st.info(t("no_data"))
else:
    # Map (flat silhouette with accent dots)
    if not df_country.empty:
        fig = choropleth(df_country, "country", "n_users", "", height=280)
        st.plotly_chart(fig, use_container_width=True)

    # Arc gauges: top 5 regions by % of users
    if not df_region.empty:
        total_region_users = int(df_region["n_users"].sum()) or 1
        top_regions = df_region.head(5).copy()
        top_regions["pct"] = top_regions["n_users"] / total_region_users * 100
        items = [
            {
                "label": str(r["region"]),
                "pct":   float(r["pct"]),
                "value": f"{int(r['n_users'])}",
            }
            for _, r in top_regions.iterrows()
        ]
        arc_row(items)


# ── Country detail table (if multiple countries) ─────────────────────────────
if not df_country.empty and len(df_country) > 3:
    st.markdown("<div style='margin:1.2rem 0 0.25rem'></div>", unsafe_allow_html=True)
    card_header(
        title=t("by_country") + " — detalle",
        icon_svg=KPI_ICONS["chart"],
    )
    st.dataframe(
        df_country.rename(columns={"country": "País", "n_users": "Usuarios"}),
        use_container_width=True,
        hide_index=True,
    )
