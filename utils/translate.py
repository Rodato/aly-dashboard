"""Keyword translation via OpenRouter (google/gemini-2.5-flash-lite)."""

import json
import os

import requests
import streamlit as st

_OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
_MODEL = "google/gemini-2.5-flash-lite"


@st.cache_data(ttl=3600)
def translate_keywords(keywords: tuple, target_lang: str) -> dict:
    """Translate a tuple of English keywords to target_lang.

    Returns a dict mapping original -> translated.
    Accepts a tuple (not list) because st.cache_data requires hashable args.
    Falls back to identity mapping on any error or missing API key.
    """
    if target_lang == "en" or not keywords:
        return {k: k for k in keywords}

    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        return {k: k for k in keywords}

    prompt = (
        "Translate these English keywords to natural Spanish.\n"
        "Return ONLY a valid JSON object where each key is the original English keyword "
        "and each value is its Spanish translation. No markdown, no explanation.\n\n"
        + json.dumps(list(keywords), ensure_ascii=False)
    )

    try:
        resp = requests.post(
            _OPENROUTER_URL,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            json={
                "model": _MODEL,
                "max_tokens": 1024,
                "messages": [{"role": "user", "content": prompt}],
            },
            timeout=15,
        )
        resp.raise_for_status()
        raw = resp.json()["choices"][0]["message"]["content"].strip()
        # Strip markdown code fences if model adds them despite instructions
        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]
            raw = raw.strip()
        result = json.loads(raw)
        return {k: result.get(k, k) for k in keywords}
    except Exception:
        return {k: k for k in keywords}
