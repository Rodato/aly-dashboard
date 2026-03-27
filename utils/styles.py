"""Aly brand styles — global CSS injection for the redesigned dashboard."""

import streamlit as st

COLORS = {
    "bg_app":        "#F0F2F5",
    "bg_sidebar":    "#0C1214",
    "bg_card":       "#FFFFFF",
    "border":        "#E5E7EB",
    "accent":        "#0273e5",
    "navy":          "#110079",
    "green":         "#91EBF4",
    "red":           "#F15B22",
    "yellow":        "#FFCF24",
    "positive":      "#22C55E",
    "negative":      "#F15B22",
    "text":          "#0C1214",
    "text_secondary":"#6B7280",
    "text_muted":    "#9CA3AF",
}


def inject():
    css = """
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Open+Sans:ital,wght@0,300..800;1,300..800&family=Oswald:wght@400;500;600;700&display=swap" rel="stylesheet">

    <style>
    /* ── Variables ──────────────────────────────────────────────────────── */
    :root {
        --bg-app:         #F0F2F5;
        --bg-sidebar:     #0C1214;
        --bg-card:        #FFFFFF;
        --border:         #E5E7EB;
        --accent:         #0273e5;
        --accent-navy:    #110079;
        --accent-green:   #91EBF4;
        --accent-red:     #F15B22;
        --accent-yellow:  #FFCF24;
        --positive:       #22C55E;
        --negative:       #F15B22;
        --text:           #0C1214;
        --text-secondary: #6B7280;
        --text-muted:     #9CA3AF;
        --radius:         10px;
        --shadow:         0 1px 3px rgba(0,0,0,0.08), 0 1px 2px rgba(0,0,0,0.06);
        --shadow-md:      0 4px 12px rgba(0,0,0,0.10);
    }

    /* ── Global reset ───────────────────────────────────────────────────── */
    html, body, [class*="css"], .stApp {
        background-color: var(--bg-app) !important;
        color: var(--text) !important;
        font-family: 'Open Sans', sans-serif !important;
    }

    /* Hide Streamlit chrome */
    #MainMenu, footer { visibility: hidden; }
    header[data-testid="stHeader"] { background: transparent !important; }

    /* ── Sidebar — dark ─────────────────────────────────────────────────── */
    [data-testid="stSidebar"] {
        background-color: var(--bg-sidebar) !important;
        border-right: 1px solid #1E2A30 !important;
    }
    [data-testid="stSidebar"] * {
        font-family: 'Open Sans', sans-serif !important;
        color: #CBD5E1 !important;
    }
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        color: #FFFFFF !important;
        font-family: 'Oswald', sans-serif !important;
    }

    /* Navigation links in sidebar */
    [data-testid="stSidebar"] [data-testid="stSidebarNav"] a {
        color: #94A3B8 !important;
        font-size: 0.875rem !important;
        font-weight: 500 !important;
        border-radius: 8px !important;
        padding: 0.5rem 0.75rem !important;
        transition: background 0.15s, color 0.15s !important;
    }
    [data-testid="stSidebar"] [data-testid="stSidebarNav"] a:hover {
        background: rgba(255,255,255,0.07) !important;
        color: #FFFFFF !important;
    }
    [data-testid="stSidebar"] [data-testid="stSidebarNav"] [aria-current="page"] {
        background: rgba(2,115,229,0.18) !important;
        color: #60A5FA !important;
        border-left: 3px solid var(--accent) !important;
        font-weight: 600 !important;
    }

    /* Sidebar form inputs */
    [data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] > div,
    [data-testid="stSidebar"] .stDateInput input {
        background-color: #1E2A30 !important;
        border: 1px solid #2D3B42 !important;
        border-radius: 8px !important;
        color: #CBD5E1 !important;
    }
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] .stRadio label {
        color: #64748B !important;
        font-size: 0.7rem !important;
        font-weight: 700 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.06em !important;
    }
    [data-testid="stSidebar"] hr { border-color: #1E2A30 !important; }

    /* ── Main content ───────────────────────────────────────────────────── */
    .main .block-container {
        background-color: var(--bg-app) !important;
        padding: 1.5rem 2rem 2rem !important;
        max-width: 1400px !important;
    }

    /* ── Headings ───────────────────────────────────────────────────────── */
    h1 {
        font-family: 'Oswald', sans-serif !important;
        font-size: 1.75rem !important;
        font-weight: 600 !important;
        color: var(--text) !important;
        letter-spacing: 0.01em !important;
        margin-bottom: 0.25rem !important;
    }
    h2, h3 {
        font-family: 'Open Sans', sans-serif !important;
        color: var(--text-secondary) !important;
    }

    /* ── KPI metric cards ───────────────────────────────────────────────── */
    [data-testid="metric-container"] {
        background-color: var(--bg-card) !important;
        border: 1px solid var(--border) !important;
        border-radius: var(--radius) !important;
        padding: 1.25rem 1.5rem !important;
        box-shadow: var(--shadow) !important;
        transition: box-shadow 0.2s, transform 0.2s !important;
    }
    [data-testid="metric-container"]:hover {
        box-shadow: var(--shadow-md) !important;
        transform: translateY(-1px) !important;
    }
    [data-testid="metric-container"] [data-testid="stMetricLabel"] p {
        font-family: 'Open Sans', sans-serif !important;
        font-size: 0.7rem !important;
        font-weight: 700 !important;
        color: var(--text-muted) !important;
        text-transform: uppercase !important;
        letter-spacing: 0.07em !important;
    }
    [data-testid="metric-container"] [data-testid="stMetricValue"] {
        font-family: 'Oswald', sans-serif !important;
        font-size: 2.25rem !important;
        font-weight: 600 !important;
        color: var(--text) !important;
        font-variant-numeric: tabular-nums !important;
        line-height: 1.1 !important;
    }
    [data-testid="stMetricDeltaIcon-Up"]   { color: var(--positive) !important; }
    [data-testid="stMetricDeltaIcon-Down"] { color: var(--negative) !important; }

    /* ── Plotly chart containers ────────────────────────────────────────── */
    .js-plotly-plot {
        border-radius: var(--radius) !important;
        background: var(--bg-card) !important;
        box-shadow: var(--shadow) !important;
        border: 1px solid var(--border) !important;
    }

    /* ── Tabs ────────────────────────────────────────────────────────────── */
    [data-testid="stTabs"] [data-baseweb="tab-list"] {
        gap: 0.25rem !important;
        border-bottom: 1px solid var(--border) !important;
        background: transparent !important;
    }
    [data-testid="stTabs"] [data-baseweb="tab"] {
        font-family: 'Open Sans', sans-serif !important;
        font-size: 0.85rem !important;
        font-weight: 600 !important;
        color: var(--text-secondary) !important;
        border-radius: 8px 8px 0 0 !important;
        padding: 0.5rem 1.25rem !important;
        background: transparent !important;
        border: none !important;
    }
    [data-testid="stTabs"] [aria-selected="true"] {
        color: var(--accent) !important;
        border-bottom: 2px solid var(--accent) !important;
    }

    /* ── Buttons ─────────────────────────────────────────────────────────── */
    .stButton > button {
        background-color: var(--accent) !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 8px !important;
        font-family: 'Open Sans', sans-serif !important;
        font-size: 0.85rem !important;
        font-weight: 600 !important;
        padding: 0.45rem 1.25rem !important;
        transition: opacity 0.2s, box-shadow 0.2s !important;
    }
    .stButton > button:hover {
        opacity: 0.9 !important;
        box-shadow: 0 2px 8px rgba(2,115,229,0.35) !important;
    }
    .stDownloadButton > button {
        background-color: transparent !important;
        color: var(--accent) !important;
        border: 1.5px solid var(--accent) !important;
        border-radius: 8px !important;
        font-family: 'Open Sans', sans-serif !important;
        font-size: 0.85rem !important;
        font-weight: 600 !important;
    }

    /* ── DataFrames / Tables ─────────────────────────────────────────────── */
    [data-testid="stDataFrame"] {
        border: 1px solid var(--border) !important;
        border-radius: var(--radius) !important;
        overflow: hidden !important;
        box-shadow: var(--shadow) !important;
    }

    /* ── Expanders ───────────────────────────────────────────────────────── */
    [data-testid="stExpander"] {
        background-color: var(--bg-card) !important;
        border: 1px solid var(--border) !important;
        border-radius: var(--radius) !important;
        box-shadow: var(--shadow) !important;
    }

    /* ── Alerts ──────────────────────────────────────────────────────────── */
    .stAlert {
        border-radius: var(--radius) !important;
        border: 1px solid var(--border) !important;
        font-size: 0.85rem !important;
    }

    /* ── Dividers ────────────────────────────────────────────────────────── */
    hr { border-color: var(--border) !important; margin: 1rem 0 !important; }

    /* ── Scrollbar ───────────────────────────────────────────────────────── */
    ::-webkit-scrollbar { width: 6px; height: 6px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb { background: var(--border); border-radius: 3px; }
    ::-webkit-scrollbar-thumb:hover { background: var(--text-muted); }
    </style>
    """
    st.html(css)


def section_label(text: str):
    """Small all-caps section divider label."""
    st.markdown(
        f'<div style="font-family:\'Open Sans\',sans-serif;font-size:0.7rem;'
        f'font-weight:700;text-transform:uppercase;letter-spacing:0.1em;'
        f'color:#9CA3AF;padding-bottom:0.4rem;border-bottom:1px solid #E5E7EB;'
        f'margin-bottom:1rem;width:100%">{text}</div>',
        unsafe_allow_html=True,
    )


def page_header(title: str, subtitle: str = ""):
    """Page title with optional subtitle line."""
    sub_html = (
        f'<p style="margin:0.2rem 0 0;font-size:0.875rem;'
        f'color:#6B7280;font-family:\'Open Sans\',sans-serif">{subtitle}</p>'
        if subtitle else ""
    )
    st.markdown(
        f'<div style="margin-bottom:1.5rem">'
        f'<h1 style="margin:0;padding:0">{title}</h1>{sub_html}</div>',
        unsafe_allow_html=True,
    )
