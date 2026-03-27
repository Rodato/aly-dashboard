"""Aly brand style — applied globally to every dashboard."""

import streamlit as st

COLORS = {
    "bg_primary":    "#EFEFEF",
    "bg_card":       "#FFFFFF",
    "bg_card_hover": "#F7F7F7",
    "border":        "#CCCCCC",
    "accent":        "#0273e5",
    "navy":          "#110079",
    "green":         "#91EBF4",
    "red":           "#F15B22",
    "yellow":        "#FFCF24",
    "text":          "#0C1214",
    "text_secondary":"#969696",
    "text_muted":    "#CCCCCC",
}


def inject():
    css = """
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Open+Sans:wght@400;500;600;700&family=Oswald:wght@400;500;600;700&display=swap" rel="stylesheet">

    <style>
    /* ── CSS variables ─────────────────────────────────────── */
    :root {
        --bg-primary:     #EFEFEF;
        --bg-card:        #FFFFFF;
        --bg-card-hover:  #F7F7F7;
        --border:         #CCCCCC;
        --accent-primary: #0273e5;
        --accent-navy:    #110079;
        --accent-green:   #91EBF4;
        --accent-red:     #F15B22;
        --accent-yellow:  #FFCF24;
        --text-primary:   #0C1214;
        --text-secondary: #969696;
        --text-muted:     #CCCCCC;
    }

    /* ── Global reset ──────────────────────────────────────── */
    html, body, [class*="css"], .stApp {
        background-color: var(--bg-primary) !important;
        color: var(--text-primary) !important;
        font-family: 'Open Sans', sans-serif !important;
    }

    /* ── Hide Streamlit chrome ─────────────────────────────── */
    #MainMenu, footer, header { visibility: hidden; }

    /* ── Sidebar ───────────────────────────────────────────── */
    [data-testid="stSidebar"] {
        background-color: var(--bg-card) !important;
        border-right: 1px solid var(--border) !important;
    }
    [data-testid="stSidebar"] * {
        font-family: 'Open Sans', sans-serif !important;
        color: var(--text-primary) !important;
    }
    [data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] > div,
    [data-testid="stSidebar"] .stDateInput input {
        background-color: var(--bg-primary) !important;
        border: 1px solid var(--border) !important;
        border-radius: 8px !important;
        color: var(--text-primary) !important;
        font-family: 'Open Sans', sans-serif !important;
    }

    /* ── Main content area ─────────────────────────────────── */
    .main .block-container {
        background-color: var(--bg-primary) !important;
        padding-top: 2rem !important;
        max-width: 1200px !important;
    }

    /* ── Metric cards ──────────────────────────────────────── */
    [data-testid="metric-container"] {
        background-color: var(--bg-card) !important;
        border: 1px solid var(--border) !important;
        border-radius: 12px !important;
        padding: 1.25rem 1.5rem !important;
        box-shadow: 0 1px 4px rgba(0,0,0,0.06) !important;
        transition: box-shadow 0.2s;
    }
    [data-testid="metric-container"]:hover {
        box-shadow: 0 4px 16px rgba(2, 115, 229, 0.12) !important;
    }
    [data-testid="metric-container"] [data-testid="stMetricLabel"] p {
        font-family: 'Open Sans', sans-serif !important;
        font-size: 0.8rem !important;
        font-weight: 400 !important;
        color: var(--text-secondary) !important;
        text-transform: none !important;
        letter-spacing: 0 !important;
    }
    [data-testid="metric-container"] [data-testid="stMetricValue"] {
        font-family: 'Oswald', sans-serif !important;
        font-size: 2.5rem !important;
        font-weight: 600 !important;
        color: var(--text-primary) !important;
        font-variant-numeric: tabular-nums;
    }

    /* ── Headings ──────────────────────────────────────────── */
    h1 {
        font-family: 'Oswald', sans-serif !important;
        font-size: 2rem !important;
        font-weight: 600 !important;
        color: var(--text-primary) !important;
        letter-spacing: 0.02em;
    }
    h2, h3 {
        font-family: 'Open Sans', sans-serif !important;
        color: var(--text-secondary) !important;
    }

    /* ── Dividers ──────────────────────────────────────────── */
    hr {
        border-color: var(--border) !important;
        margin: 1.25rem 0 !important;
    }

    /* ── Buttons ───────────────────────────────────────────── */
    .stButton > button {
        background-color: transparent !important;
        color: var(--accent-primary) !important;
        border: 1.5px solid var(--accent-primary) !important;
        border-radius: 999px !important;
        font-family: 'Open Sans', sans-serif !important;
        font-size: 0.85rem !important;
        font-weight: 600 !important;
        padding: 0.4rem 1.2rem !important;
        transition: box-shadow 0.2s, background-color 0.2s;
    }
    .stButton > button:hover {
        background-color: rgba(2, 115, 229, 0.06) !important;
        box-shadow: 0 2px 8px rgba(2, 115, 229, 0.15) !important;
    }

    /* ── Download button ───────────────────────────────────── */
    .stDownloadButton > button {
        background-color: transparent !important;
        color: var(--accent-primary) !important;
        border: 1.5px solid var(--accent-primary) !important;
        border-radius: 999px !important;
        font-family: 'Open Sans', sans-serif !important;
        font-size: 0.85rem !important;
        font-weight: 600 !important;
    }

    /* ── Alerts / info boxes ───────────────────────────────── */
    .stAlert {
        background-color: var(--bg-card) !important;
        border: 1px solid var(--border) !important;
        border-radius: 12px !important;
        color: var(--text-secondary) !important;
        font-size: 0.85rem !important;
    }

    /* ── Radio buttons (language toggle) ──────────────────── */
    [data-testid="stSidebar"] .stRadio label {
        font-size: 0.8rem !important;
        font-weight: 500 !important;
        color: var(--text-secondary) !important;
    }

    /* ── Sidebar labels ────────────────────────────────────── */
    [data-testid="stSidebar"] label {
        font-size: 0.75rem !important;
        font-weight: 600 !important;
        color: var(--text-muted) !important;
    }

    /* ── Plotly charts ─────────────────────────────────────── */
    .js-plotly-plot {
        border: 1.5px solid var(--accent-primary) !important;
        border-radius: 12px !important;
        background: var(--bg-card) !important;
        box-shadow: 0 1px 4px rgba(0,0,0,0.06) !important;
    }

    /* ── Tabs ──────────────────────────────────────────────── */
    [data-testid="stTabs"] [data-baseweb="tab-list"] {
        gap: 0.5rem !important;
        border-bottom: 1px solid var(--border) !important;
    }
    [data-testid="stTabs"] [data-baseweb="tab"] {
        font-family: 'Open Sans', sans-serif !important;
        font-size: 0.85rem !important;
        font-weight: 600 !important;
        color: var(--text-secondary) !important;
        border-radius: 8px 8px 0 0 !important;
        padding: 0.5rem 1.25rem !important;
    }
    [data-testid="stTabs"] [aria-selected="true"] {
        color: var(--accent-primary) !important;
        border-bottom: 2px solid var(--accent-primary) !important;
    }

    /* ── Expanders ─────────────────────────────────────────── */
    [data-testid="stExpander"] {
        background-color: var(--bg-card) !important;
        border: 1px solid var(--border) !important;
        border-radius: 12px !important;
    }
    </style>
    """
    st.html(css)


def section_header(label: str, color: str = None):
    """Pill-style section header."""
    c = color or COLORS["accent"]
    st.markdown(
        f"""<div style="margin-bottom: 1rem;">
            <span style="
                display: inline-block;
                font-family: 'Open Sans', sans-serif;
                font-size: 0.85rem;
                font-weight: 600;
                color: {c};
                border: 1.5px solid {c};
                border-radius: 999px;
                padding: 4px 16px;
                background: transparent;
            ">{label}</span>
        </div>""",
        unsafe_allow_html=True,
    )


def card_start(border_color: str = None):
    """Open a brand-style card div."""
    c = border_color or COLORS["accent"]
    st.markdown(
        f"""<div style="
            background: {COLORS['bg_card']};
            border: 1.5px solid {c};
            border-radius: 12px;
            padding: 1.25rem 1.5rem;
            margin-bottom: 1rem;
            box-shadow: 0 1px 4px rgba(0,0,0,0.06);
        ">""",
        unsafe_allow_html=True,
    )


def card_end():
    st.markdown("</div>", unsafe_allow_html=True)
