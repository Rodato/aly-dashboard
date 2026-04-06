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

    # ---- Overview page ----
    "activity_over_time":  {"es": "Actividad diaria", "en": "Daily activity"},
    "activity_heatmap":    {"es": "Mapa de actividad (hora × día)", "en": "Activity heatmap (hour × day)"},
    "avg_msg_per_conv":    {"es": "Msg / conversación", "en": "Msg / conversation"},
    "vs_prev_period":      {"es": "vs período anterior", "en": "vs previous period"},
    "peak_hour":           {"es": "Hora pico", "en": "Peak hour"},
    "peak_day":            {"es": "Día más activo", "en": "Most active day"},
    "total_convs":         {"es": "Conversaciones", "en": "Conversations"},

    # ---- Usuarios page ----
    "users_page_title":    {"es": "Usuarios", "en": "Users"},
    "users_page_sub":      {"es": "Demografía y distribución geográfica", "en": "Demographics & geographic distribution"},
    "demographics":        {"es": "Demografía", "en": "Demographics"},
    "hourly_dist":         {"es": "Distribución horaria", "en": "Hourly distribution"},
    "country_map":         {"es": "Distribución por país", "en": "Country distribution"},

    # ---- Conversaciones page ----
    "convs_page_title":    {"es": "Conversaciones", "en": "Conversations"},
    "convs_page_sub":      {"es": "Temas, keywords y resúmenes", "en": "Topics, keywords & summaries"},
    "top_keywords":        {"es": "Keywords más frecuentes", "en": "Top keywords"},
    "top_topics":          {"es": "Temas principales", "en": "Top topics"},
    "recent_summaries":    {"es": "Resúmenes recientes", "en": "Recent summaries"},
    "keyword":             {"es": "Keyword", "en": "Keyword"},
    "frequency":           {"es": "Frecuencia", "en": "Frequency"},
    "no_keywords_yet":     {
        "es": "Las keywords se poblarán cuando el agente procese conversaciones.",
        "en": "Keywords will populate once the agent processes conversations.",
    },

    # ---- Alertas page ----
    "alerts_page_title":   {"es": "Alertas", "en": "Alerts"},
    "alerts_page_sub":     {"es": "Flags y errores detectados por el bot", "en": "Bot-detected flags and errors"},
    "red_flags":           {"es": "Alertas rojas", "en": "Red flags"},
    "orange_flags":        {"es": "Alertas naranja", "en": "Orange flags"},
    "open_flags":          {"es": "Sin resolver", "en": "Unresolved"},
    "no_flags":            {
        "es": "No hay alertas registradas para este período.",
        "en": "No flags recorded for this period.",
    },
    "flags_setup":         {
        "es": "Para activar las alertas, agrega la columna `flag_type` (red | orange) en `users_interactions`.",
        "en": "To enable flags, add a `flag_type` column (red | orange) to `users_interactions`.",
    },
    "date_col":            {"es": "Fecha", "en": "Date"},
    "type_col":            {"es": "Tipo", "en": "Type"},
    "status_col":          {"es": "Estado", "en": "Status"},
    "description_col":     {"es": "Descripción", "en": "Description"},

    # ---- Leaderboard page ----
    "lb_page_title":       {"es": "Leaderboard", "en": "Leaderboard"},
    "lb_page_sub":         {"es": "Usuarios más activos en el período seleccionado", "en": "Most active users in the selected period"},
    "lb_rank":             {"es": "Pos.", "en": "Rank"},
    "lb_user":             {"es": "Usuario", "en": "User"},
    "lb_messages":         {"es": "Mensajes", "en": "Messages"},
    "lb_conversations":    {"es": "Conversaciones", "en": "Conversations"},
    "lb_days_active":      {"es": "Días activo", "en": "Days active"},
    "lb_avg_msg":          {"es": "Msg/conv", "en": "Msg/conv"},
    "lb_last_seen":        {"es": "Última vez", "en": "Last seen"},
    "lb_country":          {"es": "País", "en": "Country"},
    "lb_top_stats":        {"es": "Podio", "en": "Podium"},
    "lb_engagement":       {"es": "Tabla completa", "en": "Full table"},
    "lb_no_data":          {"es": "Sin datos para el período seleccionado.", "en": "No data for the selected period."},
    "lb_detail_for":       {"es": "Detalle de", "en": "Detail for"},
    "lb_no_conv_data":     {"es": "Sin conversaciones en este período.", "en": "No conversations in this period."},
    "lb_tab_wordcloud":    {"es": "Nube de palabras", "en": "Word cloud"},
    "lb_tab_summaries":    {"es": "Resúmenes", "en": "Summaries"},
    "lb_tab_transcripts":  {"es": "Transcripciones", "en": "Transcripts"},
    "lb_no_summaries":     {"es": "Sin resúmenes disponibles.", "en": "No summaries available."},
    "lb_no_transcripts":   {"es": "Sin mensajes disponibles.", "en": "No messages available."},
    "lb_messages_short":   {"es": "msgs", "en": "msgs"},
    "lb_role_user":        {"es": "Usuario", "en": "User"},
    "lb_role_assistant":   {"es": "Asistente", "en": "Assistant"},
    "lb_click_hint":       {"es": "Haz clic en una fila para ver el detalle del usuario.", "en": "Click a row to view user details."},

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
