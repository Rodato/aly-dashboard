import os
import psycopg2
import psycopg2.extras
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")


def get_connection():
    return psycopg2.connect(DATABASE_URL)


def fetch_df(query: str, params=None) -> pd.DataFrame:
    with get_connection() as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(query, params or [])
            rows = cur.fetchall()
            return pd.DataFrame(rows)


# ---------------------------------------------------------------------------
# KPI queries
# ---------------------------------------------------------------------------

def get_user_kpis(date_from=None, date_to=None) -> dict:
    """Return unique users and sessions within optional date range."""
    where, params = _date_filter("created_at", date_from, date_to)
    query = f"""
        SELECT
            COUNT(DISTINCT client_number) AS n_users,
            COUNT(DISTINCT conversation_id) AS n_sessions
        FROM public.users_interactions
        {where}
    """
    df = fetch_df(query, params)
    row = df.iloc[0]
    return {"n_users": int(row["n_users"]), "n_sessions": int(row["n_sessions"])}


def get_messages_count(date_from=None, date_to=None) -> int:
    where, params = _date_filter("created_at", date_from, date_to)
    query = f"""
        SELECT COUNT(*) AS n FROM public.users_interactions {where}
    """
    df = fetch_df(query, params)
    return int(df.iloc[0]["n"])


# ---------------------------------------------------------------------------
# Time-of-day histogram
# ---------------------------------------------------------------------------

def get_hourly_distribution(date_from=None, date_to=None) -> pd.DataFrame:
    """Return message count per hour of day (0-23)."""
    where, params = _date_filter("created_at", date_from, date_to)
    query = f"""
        SELECT
            EXTRACT(HOUR FROM created_at) AS hour,
            COUNT(*) AS messages
        FROM public.users_interactions
        {where}
        GROUP BY 1
        ORDER BY 1
    """
    return fetch_df(query, params)


# ---------------------------------------------------------------------------
# User demographics (from users_data)
# ---------------------------------------------------------------------------

def get_users_by_country(date_from=None, date_to=None) -> pd.DataFrame:
    where_i, params_i = _date_filter("ui.created_at", date_from, date_to, extra="ud.country IS NOT NULL")
    query = f"""
        SELECT ud.country, COUNT(DISTINCT ud.number) AS n_users
        FROM public.users_data ud
        JOIN public.users_interactions ui ON ui.client_number = ud.number
        {where_i}
        GROUP BY 1
        ORDER BY 2 DESC
    """
    try:
        return fetch_df(query, params_i)
    except Exception:
        return pd.DataFrame(columns=["country", "n_users"])


def get_users_by_gender(date_from=None, date_to=None) -> pd.DataFrame:
    where_i, params_i = _date_filter("ui.created_at", date_from, date_to, extra="ud.gender IS NOT NULL")
    query = f"""
        SELECT ud.gender, COUNT(DISTINCT ud.number) AS n_users
        FROM public.users_data ud
        JOIN public.users_interactions ui ON ui.client_number = ud.number
        {where_i}
        GROUP BY 1
        ORDER BY 2 DESC
    """
    try:
        return fetch_df(query, params_i)
    except Exception:
        return pd.DataFrame(columns=["gender", "n_users"])


def get_users_by_region(date_from=None, date_to=None) -> pd.DataFrame:
    where_i, params_i = _date_filter("ui.created_at", date_from, date_to, extra="ud.region IS NOT NULL")
    query = f"""
        SELECT ud.region, COUNT(DISTINCT ud.number) AS n_users
        FROM public.users_data ud
        JOIN public.users_interactions ui ON ui.client_number = ud.number
        {where_i}
        GROUP BY 1
        ORDER BY 2 DESC
    """
    try:
        return fetch_df(query, params_i)
    except Exception:
        return pd.DataFrame(columns=["region", "n_users"])


# ---------------------------------------------------------------------------
# Export — full filtered dataset
# ---------------------------------------------------------------------------

def get_interactions_export(date_from=None, date_to=None) -> pd.DataFrame:
    where, params = _date_filter("created_at", date_from, date_to)
    query = f"""
        SELECT
            conversation_id, client_number, role, message,
            timestamp, status, created_at
        FROM public.users_interactions
        {where}
        ORDER BY created_at
    """
    return fetch_df(query, params)


# ---------------------------------------------------------------------------
# Analytics — new queries for redesigned dashboard
# ---------------------------------------------------------------------------

def get_daily_activity(date_from=None, date_to=None) -> pd.DataFrame:
    """Return message and unique-user counts per calendar day."""
    where, params = _date_filter("created_at", date_from, date_to)
    query = f"""
        SELECT
            DATE(created_at) AS day,
            COUNT(*) AS messages,
            COUNT(DISTINCT client_number) AS users
        FROM public.users_interactions
        {where}
        GROUP BY 1
        ORDER BY 1
    """
    return fetch_df(query, params)


def get_activity_heatmap(date_from=None, date_to=None) -> pd.DataFrame:
    """Return message counts indexed by day-of-week (0=Sun) and hour (0-23)."""
    where, params = _date_filter("created_at", date_from, date_to)
    query = f"""
        SELECT
            EXTRACT(DOW  FROM created_at)::int AS dow,
            EXTRACT(HOUR FROM created_at)::int AS hour,
            COUNT(*) AS messages
        FROM public.users_interactions
        {where}
        GROUP BY 1, 2
        ORDER BY 1, 2
    """
    return fetch_df(query, params)


def get_conversation_metrics(date_from=None, date_to=None) -> dict:
    """Return average messages per conversation and per-user averages."""
    where, params = _date_filter("created_at", date_from, date_to)
    query = f"""
        SELECT
            COUNT(*)                                    AS total_messages,
            COUNT(DISTINCT conversation_id)             AS total_conversations,
            COUNT(DISTINCT client_number)               AS total_users,
            ROUND(
                COUNT(*)::numeric /
                NULLIF(COUNT(DISTINCT conversation_id), 0), 1
            )                                           AS avg_msg_per_conv,
            ROUND(
                COUNT(*)::numeric /
                NULLIF(COUNT(DISTINCT client_number), 0), 1
            )                                           AS avg_msg_per_user
        FROM public.users_interactions
        {where}
    """
    df = fetch_df(query, params)
    row = df.iloc[0]
    return {
        "total_messages":      int(row["total_messages"] or 0),
        "total_conversations": int(row["total_conversations"] or 0),
        "total_users":         int(row["total_users"] or 0),
        "avg_msg_per_conv":    float(row["avg_msg_per_conv"] or 0),
        "avg_msg_per_user":    float(row["avg_msg_per_user"] or 0),
    }


def get_kpi_deltas(date_from: str, date_to: str) -> dict:
    """Compare current period KPIs against the equivalent previous period.

    Returns a dict with keys: users_delta, sessions_delta, messages_delta
    where each value is a float fraction (e.g. 0.12 = +12%).
    """
    import datetime

    try:
        d_from = datetime.date.fromisoformat(date_from)
        d_to   = datetime.date.fromisoformat(date_to)
        span   = d_to - d_from
        prev_from = str(d_from - span)
        prev_to   = str(d_from)
    except Exception:
        return {"users_delta": None, "sessions_delta": None, "messages_delta": None}

    current = get_user_kpis(date_from, date_to)
    prev    = get_user_kpis(prev_from, prev_to)
    curr_msg = get_messages_count(date_from, date_to)
    prev_msg = get_messages_count(prev_from, prev_to)

    def _delta(curr, prev):
        if prev == 0:
            return None
        return round((curr - prev) / prev, 4)

    return {
        "users_delta":    _delta(current["n_users"],    prev["n_users"]),
        "sessions_delta": _delta(current["n_sessions"], prev["n_sessions"]),
        "messages_delta": _delta(curr_msg,              prev_msg),
    }


# ---------------------------------------------------------------------------
# Schema introspection (run once to discover available tables)
# ---------------------------------------------------------------------------

def get_schema_info() -> pd.DataFrame:
    """Return all columns across all non-system schemas in Supabase."""
    query = """
        SELECT
            table_schema,
            table_name,
            column_name,
            data_type,
            is_nullable
        FROM information_schema.columns
        WHERE table_schema NOT IN ('pg_catalog', 'information_schema')
        ORDER BY table_schema, table_name, ordinal_position
    """
    try:
        return fetch_df(query)
    except Exception as e:
        return pd.DataFrame({"error": [str(e)]})


# ---------------------------------------------------------------------------
# conversations_data — summaries, keywords, flags
# ---------------------------------------------------------------------------

def get_conversations_data(date_from=None, date_to=None) -> pd.DataFrame:
    """Return all processed conversations with summary, keywords, flags."""
    where, params = _date_filter("conversation_date", date_from, date_to)
    query = f"""
        SELECT
            conversation_id,
            user_number,
            conversation_date,
            summary,
            keywords,
            flags,
            session
        FROM public.conversations_data
        {where}
        ORDER BY conversation_date DESC
    """
    try:
        return fetch_df(query, params)
    except Exception:
        return pd.DataFrame()


def get_summaries(date_from=None, date_to=None, limit: int = 20) -> pd.DataFrame:
    """Return recent conversation summaries."""
    where, params = _date_filter("conversation_date", date_from, date_to,
                                 extra="summary IS NOT NULL AND summary != ''")
    query = f"""
        SELECT conversation_id, user_number, conversation_date, summary
        FROM public.conversations_data
        {where}
        ORDER BY conversation_date DESC
        LIMIT {limit}
    """
    try:
        return fetch_df(query, params)
    except Exception:
        return pd.DataFrame()


def get_flags_data(date_from=None, date_to=None) -> pd.DataFrame:
    """Return conversations that have a flag value."""
    where, params = _date_filter("conversation_date", date_from, date_to,
                                 extra="flags IS NOT NULL AND flags != ''")
    query = f"""
        SELECT conversation_id, user_number, conversation_date, flags, summary
        FROM public.conversations_data
        {where}
        ORDER BY conversation_date DESC
    """
    try:
        return fetch_df(query, params)
    except Exception:
        return pd.DataFrame()


# ---------------------------------------------------------------------------
# RAG knowledge base info
# ---------------------------------------------------------------------------

def get_rag_summary() -> pd.DataFrame:
    query = """
        SELECT project, document_name, COUNT(*) AS chunks
        FROM vector_aly.rag_embeddings
        GROUP BY 1, 2
        ORDER BY 3 DESC
    """
    try:
        return fetch_df(query)
    except Exception:
        return pd.DataFrame(columns=["project", "document_name", "chunks"])


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _date_filter(col: str, date_from, date_to, extra: str = ""):
    """Build a WHERE clause for date range + optional extra condition."""
    clauses = []
    params: list = []
    if extra:
        clauses.append(extra)
    if date_from:
        clauses.append(f"{col} >= %s")
        params.append(str(date_from))
    if date_to:
        clauses.append(f"{col} < %s")
        params.append(str(date_to))
    if clauses:
        return "WHERE " + " AND ".join(clauses), params
    return "", params
