"""Cached loaders for the precomputed bundle in app_data/ (built by scripts/build_app_data.py)."""

import gzip
import json
from pathlib import Path
from typing import Any, Dict, List

import pandas as pd
import streamlit as st

APP_DATA = Path(__file__).resolve().parents[1] / "app_data"

COMPANIES = {
    "AAPL": "Apple", "AMZN": "Amazon", "GOOGL": "Alphabet", "JNJ": "Johnson & Johnson", "JPM": "JPMorgan Chase",
    "META": "Meta Platforms", "MSFT": "Microsoft", "NVDA": "NVIDIA", "TSLA": "Tesla", "WMT": "Walmart",
}

RECIPE_LABELS = {
    "text": "Text, one section", "table": "Table, one filing", "table_text": "Table + text",
    "cross_year_text": "Cross-year text", "cross_year_table": "Cross-year table",
    "cross_company_text": "Cross-company text", "cross_company_table": "Cross-company table",
}


@st.cache_data(show_spinner=False)
def load_benchmark() -> List[Dict[str, Any]]:
    # The repo keeps the gzip; the Hugging Face deploy unzips it, because the Space rejects binary files pushed without LFS.
    plain = APP_DATA / "benchmark.json"
    if plain.exists():
        return json.loads(plain.read_text(encoding="utf-8"))
    with gzip.open(APP_DATA / "benchmark.json.gz", "rt", encoding="utf-8") as f:
        return json.load(f)


@st.cache_data(show_spinner=False)
def benchmark_by_question() -> Dict[str, Dict[str, Any]]:
    return {q["question"].strip().lower(): q for q in load_benchmark()}


@st.cache_data(show_spinner=False)
def load_rq1() -> pd.DataFrame:
    df = pd.read_csv(APP_DATA / "rq1.csv")
    return df[df["unit"] == "question"]


@st.cache_data(show_spinner=False)
def load_rq2() -> Dict[str, Any]:
    return json.loads((APP_DATA / "rq2.json").read_text(encoding="utf-8"))


@st.cache_data(show_spinner=False)
def load_rq3() -> Dict[str, Any]:
    return json.loads((APP_DATA / "rq3.json").read_text(encoding="utf-8"))


def question_companies(q: Dict[str, Any]) -> List[str]:
    tickers = {ev.get("ticker") for ev in q.get("gold_evidence") or [] if ev.get("ticker")}
    return sorted(tickers)
