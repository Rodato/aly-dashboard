"""Dashboard AlyBot — entry point with multi-page navigation."""

import streamlit as st
from dotenv import load_dotenv

from utils.styles import inject as inject_styles
from utils.i18n import t
from components.filters import render_sidebar

load_dotenv()

st.set_page_config(
    page_title="Dashboard AlyBot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_styles()

# Session state defaults
if "lang" not in st.session_state:
    st.session_state.lang = "es"

# Filter state is initialized in components/filters.py when the sidebar renders

# Define pages
pages = [
    st.Page("pages/overview.py",        title="Inicio",          icon="📊"),
    st.Page("pages/usuarios.py",         title="Usuarios",        icon="👥"),
    st.Page("pages/alertas.py",          title="Alertas",         icon="🚨"),
    st.Page("pages/leaderboard.py",      title="Leaderboard",     icon="🏆"),
]

pg = st.navigation(pages)

# Sidebar — logo + filters (rendered on every page)
render_sidebar()

pg.run()
