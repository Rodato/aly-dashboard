"""
Apapacho Dashboard — entry point.

Auth flow:
  1. Read credentials from .env (DASHBOARD_USERNAME, DASHBOARD_PASSWORD_HASH).
  2. Use streamlit-authenticator to gate the app.
  3. On success, render sidebar + main sections.
"""

import os
import datetime
import streamlit as st
import streamlit_authenticator as stauth
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
# Authentication setup
# ---------------------------------------------------------------------------
DASHBOARD_USERNAME = os.getenv("DASHBOARD_USERNAME", "admin")
DASHBOARD_PASSWORD_HASH = os.getenv("DASHBOARD_PASSWORD_HASH", "")

if not DASHBOARD_PASSWORD_HASH:
    st.error(
        "⚠️ **Setup required:** Add `DASHBOARD_USERNAME` and `DASHBOARD_PASSWORD_HASH` to your `.env` file.\n\n"
        "Generate a hash with:\n```\npython3 -c \"import bcrypt; print(bcrypt.hashpw(b'your_password', bcrypt.gensalt()).decode())\"\n```"
    )
    st.stop()

credentials = {
    "usernames": {
        DASHBOARD_USERNAME: {
            "name": DASHBOARD_USERNAME,
            "password": DASHBOARD_PASSWORD_HASH,
        }
    }
}

cookie_config = {
    "name": "apapacho_auth",
    "key": os.getenv("COOKIE_KEY", "apapacho_secret_key_change_me"),
    "expiry_days": int(os.getenv("COOKIE_EXPIRY_DAYS", "7")),
}

authenticator = stauth.Authenticate(
    credentials=credentials,
    cookie_name=cookie_config["name"],
    cookie_key=cookie_config["key"],
    cookie_expiry_days=cookie_config["expiry_days"],
)

# ---------------------------------------------------------------------------
# Login
# ---------------------------------------------------------------------------
authenticator.login(location="main")

auth_status = st.session_state.get("authentication_status")

if auth_status is False:
    st.error(t("login_error"))
    st.stop()

if auth_status is None:
    st.stop()

# ---------------------------------------------------------------------------
# Authenticated — render app
# ---------------------------------------------------------------------------

# Logout in sidebar
with st.sidebar:
    st.markdown(f"### 🤖 {t('dashboard_title')}")
    authenticator.logout(button_name=t("logout"), location="sidebar")
    st.caption(f"{t('last_updated')}: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}")

# Sidebar filters
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
