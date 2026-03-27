"""Aly brand light style — applied globally to every dashboard."""

import streamlit as st

COLORS = {
    "bg_primary":    "#EFEFEF",
    "bg_card":       "#FFFFFF",
    "bg_card_hover": "#F7F7F7",
    "border":        "#CCCCCC",
    "accent":        "#0273e5",   # brand blue — primary
    "green":         "#91EBF4",
    "red":           "#F15B22",
    "blue":          "#FFCF24",
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
        --accent-green:   #91EBF4;
        --accent-red:     #F15B22;
        --accent-blue:    #FFCF24;
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
        border-radius: 4px !important;
        color: var(--text-primary) !important;
        font-family: 'Open Sans', sans-serif !important;
    }

    /* ── Main content area ─────────────────────────────────── */
    .main .block-container {
        background-color: var(--bg-primary) !important;
        padding-top: 1.5rem !important;
    }

    /* ── Metric cards ──────────────────────────────────────── */
    [data-testid="metric-container"] {
        background-color: var(--bg-card) !important;
        border: 1px solid var(--border) !important;
        border-top: 3px solid var(--accent-primary) !important;
        border-radius: 4px !important;
        padding: 1rem 1.25rem !important;
        transition: background-color 0.2s, box-shadow 0.2s;
    }
    [data-testid="metric-container"]:hover {
        background-color: var(--bg-card-hover) !important;
        box-shadow: 0 0 12px rgba(2, 115, 229, 0.15) !important;
    }
    [data-testid="metric-container"] [data-testid="stMetricLabel"] p {
        font-family: 'Open Sans', sans-serif !important;
        font-size: 0.7rem !important;
        font-weight: 600 !important;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        color: var(--text-secondary) !important;
    }
    [data-testid="metric-container"] [data-testid="stMetricValue"] {
        font-family: 'Open Sans', sans-serif !important;
        font-size: 2rem !important;
        font-weight: 700 !important;
        color: var(--accent-primary) !important;
        font-variant-numeric: tabular-nums;
    }

    /* ── Headings ──────────────────────────────────────────── */
    h1 {
        font-family: 'Oswald', sans-serif !important;
        font-size: 1.3rem !important;
        font-weight: 700 !important;
        color: var(--text-primary) !important;
        letter-spacing: 0.05em;
        text-transform: uppercase;
    }
    h2, h3 {
        font-family: 'Open Sans', sans-serif !important;
        color: var(--text-secondary) !important;
    }

    /* ── Dividers ──────────────────────────────────────────── */
    hr {
        border-color: var(--border) !important;
        margin: 0.75rem 0 !important;
    }

    /* ── Buttons ───────────────────────────────────────────── */
    .stButton > button {
        background-color: transparent !important;
        color: var(--accent-primary) !important;
        border: 1px solid var(--accent-primary) !important;
        border-radius: 4px !important;
        font-family: 'Open Sans', sans-serif !important;
        font-size: 0.8rem !important;
        font-weight: 600 !important;
        letter-spacing: 0.05em;
        text-transform: uppercase;
        transition: box-shadow 0.2s, background-color 0.2s;
    }
    .stButton > button:hover {
        background-color: rgba(2, 115, 229, 0.08) !important;
        box-shadow: 0 0 12px rgba(2, 115, 229, 0.15) !important;
    }

    /* ── Download button ───────────────────────────────────── */
    .stDownloadButton > button {
        background-color: transparent !important;
        color: var(--accent-green) !important;
        border: 1px solid var(--accent-green) !important;
        border-radius: 4px !important;
        font-family: 'Open Sans', sans-serif !important;
        font-size: 0.8rem !important;
        font-weight: 600 !important;
        text-transform: uppercase;
    }

    /* ── Alerts / info boxes ───────────────────────────────── */
    .stAlert {
        background-color: var(--bg-card) !important;
        border: 1px solid var(--border) !important;
        border-radius: 4px !important;
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
        font-size: 0.7rem !important;
        font-weight: 600 !important;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: var(--text-muted) !important;
    }

    /* ── Plotly charts ─────────────────────────────────────── */
    .js-plotly-plot {
        border: 1px solid var(--border) !important;
        border-top: 3px solid var(--accent-primary) !important;
        border-radius: 4px !important;
        background: var(--bg-card) !important;
    }

    /* ── Expanders ─────────────────────────────────────────── */
    [data-testid="stExpander"] {
        background-color: var(--bg-card) !important;
        border: 1px solid var(--border) !important;
        border-radius: 4px !important;
    }
    </style>
    """
    st.html(css)


def section_header(label: str, color: str = None):
    """Terminal-style section header with amber top-bar."""
    c = color or COLORS["accent"]
    st.markdown(
        f"""<div style="
            background: {COLORS['bg_card']};
            border: 1px solid {COLORS['border']};
            border-top: 3px solid {c};
            border-radius: 4px;
            padding: 6px 14px;
            margin-bottom: 10px;
            display: inline-block;
        ">
            <span style="
                font-family: 'Oswald', sans-serif;
                font-size: 0.7rem;
                font-weight: 700;
                letter-spacing: 0.12em;
                text-transform: uppercase;
                color: {c};
            ">{label}</span>
        </div>""",
        unsafe_allow_html=True,
    )


def card_start(top_color: str = None):
    """Open a terminal-style card div."""
    c = top_color or COLORS["accent"]
    st.markdown(
        f"""<div style="
            background:{COLORS['bg_card']};
            border:1px solid {COLORS['border']};
            border-top:3px solid {c};
            border-radius:4px;
            padding:1rem 1.25rem;
            margin-bottom:0.75rem;
            transition: box-shadow 0.2s;
        ">""",
        unsafe_allow_html=True,
    )


def card_end():
    st.markdown("</div>", unsafe_allow_html=True)
