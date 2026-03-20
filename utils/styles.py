"""Bloomberg Terminal dark style — applied globally to every dashboard."""

import streamlit as st

COLORS = {
    "bg_primary":    "#0A0E17",
    "bg_card":       "#131722",
    "bg_card_hover": "#1A1F2E",
    "border":        "#1E2330",
    "accent":        "#F5A623",   # amber/gold — primary
    "green":         "#00D4AA",
    "red":           "#FF4757",
    "blue":          "#3B82F6",
    "text":          "#D1D4DC",
    "text_secondary":"#787B86",
    "text_muted":    "#4A4E5A",
}


def inject():
    css = """
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;700&display=swap" rel="stylesheet">

    <style>
    /* ── CSS variables ─────────────────────────────────────── */
    :root {
        --bg-primary:     #0A0E17;
        --bg-card:        #131722;
        --bg-card-hover:  #1A1F2E;
        --border:         #1E2330;
        --accent-primary: #F5A623;
        --accent-green:   #00D4AA;
        --accent-red:     #FF4757;
        --accent-blue:    #3B82F6;
        --text-primary:   #D1D4DC;
        --text-secondary: #787B86;
        --text-muted:     #4A4E5A;
    }

    /* ── CRT scanline overlay ──────────────────────────────── */
    .stApp::before {
        content: "";
        position: fixed;
        top: 0; left: 0; right: 0; bottom: 0;
        background: repeating-linear-gradient(
            0deg,
            transparent,
            transparent 2px,
            rgba(0, 0, 0, 0.03) 2px,
            rgba(0, 0, 0, 0.03) 4px
        );
        pointer-events: none;
        z-index: 9999;
    }

    /* ── Global reset ──────────────────────────────────────── */
    html, body, [class*="css"], .stApp {
        background-color: var(--bg-primary) !important;
        color: var(--text-primary) !important;
        font-family: 'Inter', sans-serif !important;
    }

    /* ── Hide Streamlit chrome ─────────────────────────────── */
    #MainMenu, footer, header { visibility: hidden; }

    /* ── Sidebar ───────────────────────────────────────────── */
    [data-testid="stSidebar"] {
        background-color: var(--bg-card) !important;
        border-right: 1px solid var(--border) !important;
    }
    [data-testid="stSidebar"] * {
        font-family: 'Inter', sans-serif !important;
        color: var(--text-primary) !important;
    }
    [data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] > div,
    [data-testid="stSidebar"] .stDateInput input {
        background-color: var(--bg-primary) !important;
        border: 1px solid var(--border) !important;
        border-radius: 4px !important;
        color: var(--text-primary) !important;
        font-family: 'JetBrains Mono', monospace !important;
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
        box-shadow: 0 0 12px rgba(245, 166, 35, 0.15) !important;
    }
    [data-testid="metric-container"] [data-testid="stMetricLabel"] p {
        font-family: 'Inter', sans-serif !important;
        font-size: 0.7rem !important;
        font-weight: 600 !important;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        color: var(--text-secondary) !important;
    }
    [data-testid="metric-container"] [data-testid="stMetricValue"] {
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 2rem !important;
        font-weight: 700 !important;
        color: var(--accent-primary) !important;
        font-variant-numeric: tabular-nums;
    }

    /* ── Headings ──────────────────────────────────────────── */
    h1 {
        font-family: 'Inter', sans-serif !important;
        font-size: 1.3rem !important;
        font-weight: 700 !important;
        color: var(--text-primary) !important;
        letter-spacing: 0.05em;
        text-transform: uppercase;
    }
    h2, h3 {
        font-family: 'Inter', sans-serif !important;
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
        font-family: 'Inter', sans-serif !important;
        font-size: 0.8rem !important;
        font-weight: 600 !important;
        letter-spacing: 0.05em;
        text-transform: uppercase;
        transition: box-shadow 0.2s, background-color 0.2s;
    }
    .stButton > button:hover {
        background-color: rgba(245, 166, 35, 0.08) !important;
        box-shadow: 0 0 12px rgba(245, 166, 35, 0.15) !important;
    }

    /* ── Download button ───────────────────────────────────── */
    .stDownloadButton > button {
        background-color: transparent !important;
        color: var(--accent-green) !important;
        border: 1px solid var(--accent-green) !important;
        border-radius: 4px !important;
        font-family: 'Inter', sans-serif !important;
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
    st.markdown(css, unsafe_allow_html=True)


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
                font-family: 'Inter', sans-serif;
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
