"""KPI row component — premium metric cards with delta indicators."""

import streamlit as st


def render(metrics: list[dict]):
    """Render a row of KPI metric cards.

    Each metric dict:
        label       str   — display label (will be uppercased via CSS)
        value       any   — the main number or string
        delta       float | None — fraction change e.g. 0.12 = +12%
        delta_label str   — context label e.g. "vs mes anterior"
        prefix      str   — optional prefix (e.g. "$")
        suffix      str   — optional suffix (e.g. "%")
    """
    cols = st.columns(len(metrics))
    for col, m in zip(cols, metrics):
        with col:
            value = m["value"]
            if isinstance(value, (int, float)):
                pre  = m.get("prefix", "")
                suf  = m.get("suffix", "")
                disp = f"{pre}{value:,}{suf}" if isinstance(value, int) else f"{pre}{value:.1f}{suf}"
            else:
                disp = str(value)

            delta_str = None
            delta_col = None
            if m.get("delta") is not None:
                sign = "+" if m["delta"] >= 0 else ""
                delta_str = f"{sign}{m['delta']*100:.1f}% {m.get('delta_label','')}"
                delta_col = "normal" if m["delta"] >= 0 else "inverse"

            st.metric(
                label=m["label"],
                value=disp,
                delta=delta_str,
                delta_color=delta_col or "normal",
            )
