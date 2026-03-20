"""Bilingual (ES / EN) string lookup."""

import streamlit as st

TRANSLATIONS: dict[str, dict[str, str]] = {
    # ---- Auth ----
    "login_title": {"es": "Iniciar sesión", "en": "Login"},
    "login_username": {"es": "Usuario", "en": "Username"},
    "login_password": {"es": "Contraseña", "en": "Password"},
    "login_button": {"es": "Entrar", "en": "Sign in"},
    "login_error": {"es": "Usuario o contraseña incorrectos.", "en": "Invalid username or password."},
    "logout": {"es": "Cerrar sesión", "en": "Logout"},

    # ---- Sidebar / Filters ----
    "filters": {"es": "Filtros", "en": "Filters"},
    "date_range": {"es": "Rango de fechas", "en": "Date range"},
    "date_from": {"es": "Desde", "en": "From"},
    "date_to": {"es": "Hasta", "en": "To"},
    "program": {"es": "Programa", "en": "Program"},
    "all": {"es": "Todos", "en": "All"},
    "language": {"es": "Idioma", "en": "Language"},
    "export_excel": {"es": "Exportar Excel", "en": "Export Excel"},
    "export_hint": {"es": "Descarga los datos filtrados.", "en": "Download filtered data."},

    # ---- Section headers ----
    "users_title": {"es": "USUARIOS", "en": "USERS"},
    "flags_title": {"es": "ALERTAS", "en": "FLAGS"},
    "bugs_title": {"es": "ERRORES", "en": "BUGS"},
    "insights_title": {"es": "INSIGHTS", "en": "INSIGHTS"},
    "reporting_title": {"es": "REPORTES", "en": "REPORTING"},

    # ---- KPIs ----
    "n_users": {"es": "Usuarios únicos", "en": "Unique users"},
    "n_sessions": {"es": "Sesiones", "en": "Sessions"},
    "n_messages": {"es": "Mensajes", "en": "Messages"},

    # ---- Charts ----
    "time_of_day": {"es": "Mensajes por hora del día", "en": "Messages by time of day"},
    "hour_axis": {"es": "Hora", "en": "Hour"},
    "messages_axis": {"es": "Mensajes", "en": "Messages"},
    "by_country": {"es": "Usuarios por país", "en": "Users by country"},
    "by_gender": {"es": "Usuarios por género", "en": "Users by gender"},
    "by_region": {"es": "Usuarios por región", "en": "Users by region"},
    "region_map": {"es": "Distribución geográfica", "en": "Geographic distribution"},
    "who_is_using": {"es": "¿Quién lo usa?", "en": "Who is using it?"},
    "specifics": {"es": "Detalles de uso", "en": "Usage specifics"},
    "no_data": {"es": "Sin datos disponibles aún.", "en": "No data available yet."},

    # ---- Placeholders ----
    "coming_soon": {"es": "Próximamente", "en": "Coming soon"},
    "flags_desc": {
        "es": "Monitoreo de alertas rojas/naranjas generadas por el agente.",
        "en": "Monitoring of red/orange flags raised by the agent.",
    },
    "bugs_desc": {
        "es": "Registro de errores detectados durante las conversaciones.",
        "en": "Log of errors detected during conversations.",
    },
    "insights_desc": {
        "es": "Tres insights accionables generados automáticamente con IA a partir de las conversaciones recientes.",
        "en": "Three actionable insights automatically generated with AI from recent conversations.",
    },
    "reporting_desc": {
        "es": "Temas frecuentes y preguntas principales detectadas con NLP.",
        "en": "Frequent topics and top questions detected with NLP.",
    },
    "flags_requires": {
        "es": "Requiere columna `flag_type` en `users_interactions`.",
        "en": "Requires `flag_type` column in `users_interactions`.",
    },
    "insights_requires": {
        "es": "Requiere integración con Claude API.",
        "en": "Requires Claude API integration.",
    },
    "reporting_requires": {
        "es": "Requiere extracción de temas con NLP/LLM.",
        "en": "Requires NLP/LLM topic extraction.",
    },

    # ---- Misc ----
    "dashboard_title": {"es": "Dashboard AlyBot", "en": "AlyBot Dashboard"},
    "last_updated": {"es": "Última actualización", "en": "Last updated"},
}


def t(key: str) -> str:
    """Return translated string for the current language."""
    lang = st.session_state.get("lang", "es")
    entry = TRANSLATIONS.get(key)
    if entry is None:
        return key
    return entry.get(lang, entry.get("es", key))
