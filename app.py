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

# FLAGS + BUGS (side by side)
col_flags, col_bugs = st.columns(2)
with col_flags:
    placeholders.render_flags()
with col_bugs:
    placeholders.render_bugs()

# INSIGHTS + REPORTING (side by side)
col_ins, col_rep = st.columns(2)
with col_ins:
    placeholders.render_insights()
with col_rep:
    placeholders.render_reporting()
