"""Apapacho Dashboard — entry point."""

import datetime
import streamlit as st
from dotenv import load_dotenv

from utils.i18n import t
from utils.styles import inject as inject_styles
from components import filters, users_section, placeholders

load_dotenv()

# ---------------------------------------------------------------------------
# Page config (must be first Streamlit call)
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="Dashboard AlyBot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_styles()

# ---------------------------------------------------------------------------
# Session state defaults
# ---------------------------------------------------------------------------
if "lang" not in st.session_state:
    st.session_state.lang = "es"

# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------
with st.sidebar:
    st.markdown(f"### 🤖 {t('dashboard_title')}")
    st.caption(f"{t('last_updated')}: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}")

active_filters = filters.render_sidebar()

# ---------------------------------------------------------------------------
# Main content
# ---------------------------------------------------------------------------
st.title(f"🤖 {t('dashboard_title')}")

# USERS section
users_section.render(active_filters)

# Divider
st.markdown("---")

# Secondary sections in tabs
tab_alertas, tab_bugs, tab_insights, tab_reportes = st.tabs([
    t("flags_title"),
    t("bugs_title"),
    t("insights_title"),
    t("reporting_title"),
])

with tab_alertas:
    placeholders.render_flags()

with tab_bugs:
    placeholders.render_bugs()

with tab_insights:
    placeholders.render_insights()

with tab_reportes:
    placeholders.render_reporting()
