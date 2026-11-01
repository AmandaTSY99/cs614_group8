"""
CS614 Group 8: Adaptive Multi-Hop RAG for SEC 10-K filings (Streamlit demo, deployed to Hugging Face Spaces).

Pages live in ui/pages.py; precomputed benchmark data in app_data/ (scripts/build_app_data.py).
"""

import os
import sys

import streamlit as st
import streamlit.components.v1 as components
from dotenv import load_dotenv

REPO_ROOT = os.path.abspath(os.path.dirname(__file__))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

# Once per process, without overriding: re-loading .env on every rerun would reset provider and key variables
# in the middle of another visitor's run (ui/live.py scopes them per run).
if not os.environ.get("_APP_DOTENV_LOADED"):
    load_dotenv(override=False)
    os.environ["_APP_DOTENV_LOADED"] = "1"

st.set_page_config(
    page_title="10-K RAG · CS614 Group 8",
    page_icon="📑",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Hugging Face Spaces / Streamlit Cloud secrets arrive as environment variables or st.secrets.
try:
    for key, value in st.secrets.items():
        if isinstance(value, str):
            os.environ.setdefault(key, value)
except Exception:
    pass

from ui import pages  # noqa: E402
from ui.theme import apply_theme  # noqa: E402

apply_theme()

brand, nav_col = st.columns([5, 4], vertical_alignment="bottom")
with brand:
    st.markdown(
        '<div class="masthead"><span class="name">Adaptive Multi-Hop RAG</span>'
        '<span class="meta">SEC 10-K filings · CS614 Group 8 · SMU</span></div>',
        unsafe_allow_html=True,
    )
with nav_col:
    st.session_state.setdefault("nav", "Ask")
    page = st.segmented_control("Navigate", pages.PAGES, key="nav", label_visibility="collapsed",
                                on_change=pages.keep_selection, args=("nav", "nav_last", "Ask")) or "Ask"
st.markdown('<div class="top-rule"></div>', unsafe_allow_html=True)

# Start each page at the top (Streamlit keeps the previous scroll position across reruns)
if st.session_state.get("last_page") != page:
    st.session_state["last_page"] = page
    components.html(
        "<script>const scrollUp = () => window.parent.document.querySelector('[data-testid=\"stMain\"]')?.scrollTo(0, 0);"
        "scrollUp(); setTimeout(scrollUp, 150); setTimeout(scrollUp, 600);</script>"
        f"<!-- {page} -->",  # unique per page, so Streamlit re-runs the script instead of reusing the frame
        height=0,
    )

{
    "Ask": pages.page_ask,
    "Benchmark explorer": pages.page_explore,
    "Results": pages.page_results,
    "How it works": pages.page_architecture,
}[page]()

st.markdown(
    '<div class="footer">Xavier · Amanda · Aryan · Kevin · Anish — CS614 Generative AI with LLMs, Singapore Management University. '
    "Answers are generated from public SEC filings for research purposes and are not financial advice.</div>",
    unsafe_allow_html=True,
)
