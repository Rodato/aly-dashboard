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
