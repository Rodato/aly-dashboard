"""Página Leaderboard — usuarios más activos con detalle por usuario."""

import io
import json
import re
from collections import Counter

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from utils.i18n import t
from utils import db
from utils.styles import COLORS, page_header, section_label
from utils.translate import translate_keywords
from components.filters import get_filters

filters   = get_filters()
date_from = filters["date_from"]
date_to   = filters["date_to"]

page_header(t("lb_page_title"), t("lb_page_sub"))

df = db.get_leaderboard(date_from, date_to, limit=20)

if df.empty:
    st.info(t("lb_no_data"))
    st.stop()

# ── Prepare data ──────────────────────────────────────────────────────────────
df = df.reset_index(drop=True)
df.index = df.index + 1  # 1-based rank


def _mask(number):
    s = str(number)
    return s[:4] + "****" + s[-2:] if len(s) >= 8 else s[:3] + "****"


df["display_name"] = df.apply(
    lambda r: str(r["name"]) if pd.notna(r.get("name")) and str(r.get("name", "")).strip() else _mask(r["client_number"]),
    axis=1,
)


def _medal(rank):
    return {1: "🥇", 2: "🥈", 3: "🥉"}.get(rank, str(rank))


df["rank_label"] = df.index.map(_medal)

# ── Podium — top 3 ────────────────────────────────────────────────────────────
section_label(t("lb_top_stats"))

top3 = df.head(3)
podium_order = [1, 0, 2]  # silver, gold, bronze visual order
cols = st.columns(3)

for col_idx, df_idx in enumerate(podium_order):
    if df_idx >= len(top3):
        continue
    row   = top3.iloc[df_idx]
    rank  = df_idx + 1
    medal = {1: "🥇", 2: "🥈", 3: "🥉"}[rank]
    accent_colors = {1: COLORS["accent"], 2: COLORS["text_secondary"], 3: COLORS["red"]}

    country_flag = f"&nbsp;{row.get('country', '')}" if pd.notna(row.get("country")) and str(row.get("country", "")).strip() else ""

    with cols[col_idx]:
        st.markdown(
            f"""
            <div style="
                background:{COLORS['bg_card']};
                border:1.5px solid {accent_colors[rank]};
                border-radius:12px;
                padding:1.25rem 1rem 1rem;
                text-align:center;
                box-shadow:0 2px 8px rgba(0,0,0,0.08);
                min-height:160px;
            ">
                <div style="font-size:2rem;line-height:1">{medal}</div>
                <div style="margin-top:0.5rem;font-family:'Oswald',sans-serif;
                    font-size:1.5rem;font-weight:600;color:{COLORS['text']};
                    line-height:1.1">{int(row['total_messages']):,}</div>
                <div style="font-size:0.65rem;font-weight:700;text-transform:uppercase;
                    letter-spacing:0.08em;color:{COLORS['text_muted']};margin-bottom:0.5rem">
                    {t('lb_messages')}
                </div>
                <div style="font-family:'Open Sans',sans-serif;font-size:0.82rem;
                    font-weight:600;color:{COLORS['text']};white-space:nowrap;
                    overflow:hidden;text-overflow:ellipsis">{row['display_name']}{country_flag}</div>
                <div style="margin-top:0.4rem;font-size:0.75rem;color:{COLORS['text_secondary']}">
                    {int(row['total_conversations'])} conv · {int(row['days_active'])} días
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

st.markdown("<div style='margin:1.5rem 0 0.5rem'></div>", unsafe_allow_html=True)

# ── Bar chart — top 10 ────────────────────────────────────────────────────────
top10 = df.head(10).copy()
top10_sorted = top10.sort_values("total_messages", ascending=True)

bar_colors = [
    COLORS["accent"] if i == len(top10_sorted) - 1
    else "#93C5FD" if top10_sorted["total_messages"].iloc[i] >= top10_sorted["total_messages"].max() * 0.5
    else "#DBEAFE"
    for i in range(len(top10_sorted))
]

fig = go.Figure(go.Bar(
    x=top10_sorted["total_messages"],
    y=top10_sorted["display_name"],
    orientation="h",
    marker_color=bar_colors,
    marker_line_width=0,
    text=top10_sorted["total_messages"].apply(lambda v: f"{int(v):,}"),
    textposition="outside",
    textfont=dict(size=11, color=COLORS["text_secondary"]),
    hovertemplate="<b>%{y}</b><br>%{x:,} mensajes<extra></extra>",
))
fig.update_layout(
    paper_bgcolor=COLORS["bg_card"],
    plot_bgcolor=COLORS["bg_card"],
    font=dict(family="Open Sans, sans-serif", size=11),
    height=340,
    margin=dict(l=8, r=60, t=12, b=8),
    xaxis=dict(
        gridcolor="#F3F4F6",
        linecolor=COLORS["border"],
        tickfont=dict(size=10, color=COLORS["text_secondary"]),
        showgrid=True,
    ),
    yaxis=dict(
        linecolor=COLORS["border"],
        tickfont=dict(size=11, color=COLORS["text"]),
        automargin=True,
    ),
    bargap=0.3,
    hoverlabel=dict(bgcolor=COLORS["bg_card"], bordercolor=COLORS["border"],
                    font=dict(family="Open Sans, sans-serif", size=11)),
)
st.plotly_chart(fig, use_container_width=True)

st.markdown("<div style='margin:0.5rem 0'></div>", unsafe_allow_html=True)

# ── Full table (interactive) ───────────────────────────────────────────────────
section_label(t("lb_engagement"))

st.caption(t("lb_click_hint"))

display_df = df[["rank_label", "display_name", "country", "total_messages",
                  "total_conversations", "days_active", "avg_msg_per_conv", "last_seen"]].copy()

if "last_seen" in display_df.columns:
    display_df["last_seen"] = pd.to_datetime(display_df["last_seen"]).dt.strftime("%d/%m/%Y")

display_df.columns = [
    t("lb_rank"), t("lb_user"), t("lb_country"),
    t("lb_messages"), t("lb_conversations"), t("lb_days_active"),
    t("lb_avg_msg"), t("lb_last_seen"),
]

selection = st.dataframe(
    display_df,
    use_container_width=True,
    hide_index=True,
    on_select="rerun",
    selection_mode="single-row",
    column_config={
        t("lb_messages"):      st.column_config.NumberColumn(format="%d"),
        t("lb_conversations"): st.column_config.NumberColumn(format="%d"),
        t("lb_days_active"):   st.column_config.NumberColumn(format="%d"),
        t("lb_avg_msg"):       st.column_config.NumberColumn(format="%.1f"),
    },
)

# ── User detail panel ─────────────────────────────────────────────────────────

def _parse_keywords(text: str) -> list:
    """Parse a keywords text field — handles JSON arrays and CSV strings."""
    if not text or not isinstance(text, str):
        return []
    text = text.strip()
    try:
        parsed = json.loads(text)
        if isinstance(parsed, list):
            return [str(k).strip().lower() for k in parsed if k]
    except (json.JSONDecodeError, ValueError):
        pass
    parts = re.split(r"[,;|\n]+", text)
    return [p.strip().lower() for p in parts if p.strip()]


def _render_wordcloud(df_convs):
    try:
        from wordcloud import WordCloud
    except ImportError:
        st.warning("wordcloud package not installed. Run: pip install wordcloud")
        return

    if df_convs.empty:
        st.info(t("no_keywords_yet"))
        return

    all_kws = []
    for raw in df_convs["keywords"].dropna():
        all_kws.extend(_parse_keywords(raw))

    if not all_kws:
        st.info(t("no_keywords_yet"))
        return

    freq = Counter(all_kws)
    lang = st.session_state.get("lang", "es")
    translation_map = translate_keywords(tuple(sorted(freq.keys())), lang)

    translated_freq: dict = {}
    for word, count in freq.items():
        translated = translation_map.get(word, word)
        translated_freq[translated] = translated_freq.get(translated, 0) + count

    accent = COLORS["accent"]

    def _color_func(*args, **kwargs):
        return accent

    wc = WordCloud(
        width=800,
        height=380,
        background_color=COLORS["bg_card"],
        color_func=_color_func,
        max_words=60,
        prefer_horizontal=0.85,
    ).generate_from_frequencies(translated_freq)

    buf = io.BytesIO()
    wc.to_image().save(buf, format="PNG")
    buf.seek(0)
    st.image(buf, use_container_width=True)

    # Keyword frequency table
    rows = [(w, c) for w, c in sorted(translated_freq.items(), key=lambda x: -x[1])][:30]
    df_kw = pd.DataFrame(rows, columns=[t("keyword"), t("frequency")])
    st.dataframe(df_kw, use_container_width=True, hide_index=True, height=280)


def _render_summaries(df_convs):
    has_any = False
    for _, row in df_convs.iterrows():
        summary = str(row.get("summary", "")).strip()
        if not summary or summary == "None":
            continue
        has_any = True
        conv_id = str(row.get("conversation_id", "—"))[:20]
        fecha   = str(row.get("conversation_date", ""))[:16]
        label   = f"🗨️  {fecha}  ·  conv `{conv_id}`"
        with st.expander(label):
            st.html(
                f'<p style="font-family:\'Open Sans\',sans-serif;font-size:0.875rem;'
                f'color:{COLORS["text"]};line-height:1.7;margin:0">{summary}</p>'
            )
    if not has_any:
        st.info(t("lb_no_summaries"))


def _render_chat_bubble(role, text, ts):
    is_user    = str(role).lower() == "user"
    align      = "flex-end"         if is_user else "flex-start"
    bg         = COLORS["accent"]   if is_user else COLORS["border"]
    txt_color  = "#FFFFFF"           if is_user else COLORS["text"]
    role_label = t("lb_role_user")  if is_user else t("lb_role_assistant")
    meta_color = "rgba(255,255,255,0.65)" if is_user else COLORS["text_muted"]
    st.html(f"""
    <div style="display:flex;justify-content:{align};margin-bottom:0.5rem">
      <div style="max-width:75%;background:{bg};border-radius:12px;
           padding:0.6rem 0.85rem;box-shadow:0 1px 2px rgba(0,0,0,0.06)">
        <div style="font-family:'Open Sans',sans-serif;font-size:0.72rem;
             font-weight:700;color:{meta_color};margin-bottom:0.2rem">{role_label}</div>
        <div style="font-family:'Open Sans',sans-serif;font-size:0.875rem;
             color:{txt_color};line-height:1.6">{text}</div>
        <div style="font-family:'Open Sans',sans-serif;font-size:0.68rem;
             color:{meta_color};margin-top:0.3rem;text-align:right">{ts}</div>
      </div>
    </div>
    """)


def _render_transcripts_from_msgs(df_msgs):
    """Render transcripts grouped by conversation_id directly from users_interactions."""
    if df_msgs.empty:
        st.info(t("lb_no_transcripts"))
        return

    rendered_any = False
    for conv_id, group in df_msgs.groupby("conversation_id", sort=False):
        group = group.sort_values("timestamp").reset_index(drop=True)
        first_ts = str(group["timestamp"].iloc[0])[:16]
        n_msgs   = len(group)
        label    = f"💬  {first_ts}  ·  {n_msgs} {t('lb_messages_short')}"
        rendered_any = True
        with st.expander(label):
            for _, msg in group.iterrows():
                _render_chat_bubble(
                    msg.get("role", ""),
                    str(msg.get("message", "")),
                    str(msg.get("timestamp", ""))[:16],
                )


# ── Render detail panel when a row is selected ────────────────────────────────
selected_rows = selection.selection.rows
if selected_rows:
    pos          = selected_rows[0]
    user_row     = df.iloc[pos]
    user_number  = user_row["client_number"]
    display_name = user_row["display_name"]

    st.markdown("<div style='margin:1.5rem 0 0.5rem'></div>", unsafe_allow_html=True)
    section_label(f"{t('lb_detail_for')} {display_name}")

    df_convs = db.get_user_conversations(user_number, date_from, date_to)
    df_msgs  = db.get_user_messages(user_number, date_from, date_to)

    if df_msgs.empty and df_convs.empty:
        st.info(t("lb_no_conv_data"))
    else:
        tab_wc, tab_sum, tab_trans = st.tabs([
            t("lb_tab_wordcloud"),
            t("lb_tab_summaries"),
            t("lb_tab_transcripts"),
        ])

        with tab_wc:
            _render_wordcloud(df_convs)

        with tab_sum:
            _render_summaries(df_convs)

        with tab_trans:
            _render_transcripts_from_msgs(df_msgs)
