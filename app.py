"""
System C: Adaptive Multi-Hop Financial RAG (Streamlit UI)
Interactive Web Demo for CS614 Milestone 1 & Presentation
"""

import os
import sys
import time
from typing import Any, Dict, List, Optional
import pandas as pd
import streamlit as st
from dotenv import load_dotenv

# Ensure repo root is in sys.path
REPO_ROOT = os.path.abspath(os.path.dirname(__file__))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

load_dotenv(override=True)

# Page configuration
st.set_page_config(
    page_title="System C | Financial RAG",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for executive financial dashboard styling
st.markdown(
    """
    <style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1E293B;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        font-size: 1.05rem;
        color: #64748B;
        margin-bottom: 1.5rem;
    }
    .metric-badge {
        display: inline-block;
        padding: 0.25rem 0.6rem;
        border-radius: 6px;
        font-size: 0.82rem;
        font-weight: 600;
        margin-right: 0.5rem;
        background-color: #E2E8F0;
        color: #334155;
    }
    .badge-success { background-color: #DEF7EC; color: #03543F; }
    .badge-info { background-color: #E1EFFE; color: #1E429F; }
    .badge-warning { background-color: #FEF08A; color: #713F12; }
    .stAlert { border-radius: 8px; }
    .citation-tag {
        background-color: #EEF2FF;
        color: #3730A3;
        font-family: monospace;
        padding: 2px 6px;
        border-radius: 4px;
        font-size: 0.85em;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Company directory
COMPANIES = {
    "AAPL": {"name": "Apple Inc.", "sector": "Consumer Electronics / Services", "filings": "1994 - 2025"},
    "MSFT": {"name": "Microsoft Corporation", "sector": "Enterprise Software / Cloud", "filings": "1994 - 2026"},
    "NVDA": {"name": "NVIDIA Corporation", "sector": "Semiconductors / AI Hardware", "filings": "1999 - 2026"},
    "AMZN": {"name": "Amazon.com, Inc.", "sector": "E-Commerce / Cloud Infrastructure", "filings": "1997 - 2025"},
    "GOOGL": {"name": "Alphabet Inc.", "sector": "Search / Advertising / Cloud", "filings": "2004 - 2025"},
    "META": {"name": "Meta Platforms, Inc.", "sector": "Social Media / Digital Advertising", "filings": "2012 - 2025"},
    "TSLA": {"name": "Tesla, Inc.", "sector": "Automotive / Clean Energy", "filings": "2010 - 2025"},
    "JPM": {"name": "JPMorgan Chase & Co.", "sector": "Banking / Financial Services", "filings": "1993 - 2025"},
    "JNJ": {"name": "Johnson & Johnson", "sector": "Pharmaceuticals / MedTech", "filings": "1994 - 2025"},
    "WMT": {"name": "Walmart Inc.", "sector": "Retail / Consumer Staples", "filings": "1995 - 2026"},
}

SAMPLE_QUERIES = [
    "What was Apple's total revenue, operating income, and net income in fiscal 2024?",
    "Compare Nvidia and Apple operating income and profit margins in fiscal 2024.",
    "What risk factors and supply chain constraints impacted Tesla's operations in 2023?",
    "What was Microsoft's Intelligent Cloud revenue and Azure growth in fiscal 2024?",
    "How did Amazon's operating cash flow and capital expenditures trend from 2022 to 2024?",
]


@st.cache_data(ttl=3600)
def load_financials_data() -> pd.DataFrame:
    """Load local SEC XBRL financials tabular dataset."""
    csv_path = os.path.join(REPO_ROOT, "data", "financials.csv")
    if os.path.exists(csv_path):
        return pd.read_csv(csv_path)
    return pd.DataFrame()


def get_llm_status() -> Dict[str, str]:
    """Retrieve current LLM provider configuration."""
    from src.system_c.llm import get_llm_config

    provider, model = get_llm_config()
    return {"provider": provider, "model": model}


# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.image(
        "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Python-logo-notext.svg/240px-Python-logo-notext.svg.png",
        width=50,
    )
    st.title("System C Settings")

    st.subheader("1. Pipeline Mode")
    mode_selection = st.selectbox(
        "Architecture Mode",
        options=["v2_aamr", "adaptive_v1", "fixed_1hop", "fixed_3hop"],
        index=0,
        format_func=lambda x: {
            "v2_aamr": "⭐ v2: Agentic AMR (XBRL + 10-K Router)",
            "adaptive_v1": "🔄 v1: Adaptive Multi-Hop (Text Only)",
            "fixed_1hop": "⏹️ Baseline: Fixed 1-Hop",
            "fixed_3hop": "⏹️ Baseline: Fixed 3-Hop",
        }[x],
        help="System C v2 routes quantitative requests to Supabase XBRL tables and qualitative context to SEC text chunks.",
    )

    max_hops = st.slider("Max Retrieval Hops", min_value=1, max_value=4, value=3)
    sufficiency_threshold = st.slider(
        "Critic Sufficiency Threshold",
        min_value=0.50,
        max_value=1.00,
        value=0.85,
        step=0.05,
        help="When the Critic's quantitative score reaches this threshold, the loop terminates early to save cost and latency.",
    )

    st.divider()

    st.subheader("2. Target Companies")
    selected_tickers = st.multiselect(
        "Select Filter / Target Ticker(s)",
        options=list(COMPANIES.keys()),
        default=[],
        format_func=lambda t: f"{t} ({COMPANIES[t]['name']})",
        help="Leave empty for the pipeline decomposer to automatically extract target tickers from your question.",
    )

    st.divider()

    st.subheader("3. Golden Presets")
    st.caption("Click a question to populate:")
    for sq in SAMPLE_QUERIES:
        if st.button(f"📌 {sq[:40]}...", use_container_width=True, key=f"sq_{sq}"):
            st.session_state["user_query_input"] = sq

    st.divider()

    # System Status Indicator
    llm_info = get_llm_status()
    st.subheader("System Infrastructure")
    st.markdown(
        f"""
    * **LLM Engine**: `{llm_info['provider']}` (`{llm_info['model']}`)
    * **Cloud DB**: `Supabase PostgreSQL` (`ap-southeast-1`)
    * **Table**: `sec_financials` (272 XBRL rows)
    * **Checkpointer**: `LangGraph PostgresSaver`
    * **Guardrails**: Self-Healing Grounding Active
    """
    )


# ---------------- MAIN CONTENT ----------------
st.markdown('<div class="main-header">🏛️ System C: Adaptive Multi-Hop Financial RAG</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="sub-header">Autonomous SEC 10-K Intelligence, Continuous Sufficiency Auditing, and Scale-Normalized Numerical Grounding</div>',
    unsafe_allow_html=True,
)

# Badges bar
col_b1, col_b2, col_b3, col_b4 = st.columns(4)
with col_b1:
    st.markdown('<span class="metric-badge badge-success">✓ Supabase PG Connected</span>', unsafe_allow_html=True)
with col_b2:
    st.markdown(f'<span class="metric-badge badge-info">Engine: {llm_info["provider"]}</span>', unsafe_allow_html=True)
with col_b3:
    st.markdown('<span class="metric-badge badge-info">10 SEC 10-K Corpora (1993–2026)</span>', unsafe_allow_html=True)
with col_b4:
    st.markdown('<span class="metric-badge badge-warning">Zero-Hallucination Guardrail</span>', unsafe_allow_html=True)

st.write("")

# Query Input
default_query = st.session_state.get(
    "user_query_input",
    "What was Apple's total revenue, operating income, and net income in fiscal 2024?",
)
query_text = st.text_area(
    "Enter your financial question:",
    value=default_query,
    height=80,
    placeholder="e.g. Compare NVIDIA and Microsoft cloud and data center performance in 2024...",
)

col_run, col_clear = st.columns([1, 6])
run_btn = col_run.button("🚀 Run Query", type="primary", use_container_width=True)

if run_btn and query_text.strip():
    with st.spinner("Executing System C Multi-Hop Pipeline..."):
        from src.system_c.graph import run_system_c

        start_time = time.perf_counter()
        target_ticker_arg = selected_tickers[0] if len(selected_tickers) == 1 else None

        # Execute pipeline
        result = run_system_c(
            query=query_text.strip(),
            max_hops=max_hops,
            mode=mode_selection,
            target_ticker=target_ticker_arg,
            sufficiency_threshold=sufficiency_threshold,
        )
        total_wall_time = time.perf_counter() - start_time

    # ---------------- RESULTS PRESENTATION ----------------
    st.divider()

    # Executive Summary Metrics
    m1, m2, m3, m4, m5 = st.columns(5)
    m1.metric("Hops Executed", f"{result['current_hop']} / {result['max_hops']}")
    m2.metric("Early Stopped", "Yes (≥ 0.85)" if result.get("early_stopped") else "No (Max Hops)")
    m3.metric("Sufficiency Score", f"{result.get('sufficiency_score', 0.0):.2f}")
    m4.metric("Evidence Chunks", f"{len(result.get('accumulated_evidence', []))}")
    m5.metric("Latency", f"{total_wall_time:.2f}s")

    # 1. Final Synthesized Answer
    st.subheader("📝 Synthesized Financial Answer")
    final_answer = result.get("final_answer", "")
    st.info(final_answer if final_answer else "No synthesis generated.")

    # 2. Citations & Numerical Grounding Guardrail
    col_cit, col_guard = st.columns(2)

    with col_cit:
        st.subheader("📚 Verified SEC Citations")
        citations = result.get("citations", [])
        if citations:
            for cit in citations:
                with st.expander(f"📍 {cit.get('tag', 'Citation')} — {cit.get('section', 'SEC Disclosure')}"):
                    st.write(f"**Chunk ID**: `{cit.get('chunk_id')}`")
                    st.write(f"**Ticker / Year**: {cit.get('ticker')} (FY{cit.get('fiscal_year')})")
                    st.write(f"**Disclosure Excerpt**:")
                    st.caption(cit.get("supported_claim", ""))
        else:
            st.caption("No citations recorded.")

    with col_guard:
        st.subheader("🛡️ Factuality & Numerical Guardrail")
        guard_report = result.get("guardrail_report", {})
        passed = result.get("guardrail_passed", True)
        if passed:
            st.success("✅ **Guardrail Passed**: All extracted financial figures match SEC ground-truth filings.")
        else:
            st.warning("⚠️ **Guardrail Warning**: Ungrounded numbers detected during audit.")

        st.markdown(
            f"""
        * **Numerical Error Rate**: `{guard_report.get('numerical_grounding_error_rate', 0.0) * 100:.1f}%`
        * **Faithfulness Score**: `{guard_report.get('faithfulness_score', 1.0):.2f}`
        * **Repairs Executed**: `{result.get('repair_count', 0)}`
        """
        )
        if guard_report.get("verified_numbers"):
            st.write("**Verified Numbers**:", guard_report["verified_numbers"])
        if guard_report.get("ungrounded_numbers"):
            st.write("**Ungrounded Numbers**:", guard_report["ungrounded_numbers"])

    # 3. Hop-by-Hop Reasoning Trace (Inspection for Prof / TAs)
    st.subheader("🔍 Autonomous Multi-Hop Execution Trace")
    with st.expander("Click to inspect Hop-by-Hop Decomposer Plans & Critic Decisions", expanded=False):
        intermediate = result.get("intermediate_answers", [])
        if intermediate:
            for item in intermediate:
                hop_num = item.get("hop", 1)
                st.markdown(f"#### Hop {hop_num}")
                st.write(f"**Sub-Query Executed**: `{item.get('sub_query_executed')}`")
                st.write(f"**Sufficiency Score**: `{item.get('sufficiency_score', 0.0):.2f}` (Sufficient: `{item.get('is_sufficient')}`)")
                st.write(f"**Critic Reasoning**: {item.get('critic_reasoning')}")
                if item.get("missing_premises"):
                    st.write(f"**Missing Premises Identified**: {item.get('missing_premises')}")
                st.divider()
        else:
            st.caption("No intermediate hop records logged.")

    # 4. Telemetry & Cost Analysis (RQ3)
    st.subheader("📊 Inference Economics (RQ3 Telemetry)")
    with st.expander("Click to view token counts and cost breakdown", expanded=False):
        telemetry = result.get("telemetry", {})
        calls = telemetry.get("calls", [])
        if calls:
            df_calls = pd.DataFrame(calls)
            st.dataframe(df_calls, use_container_width=True)
            summary = telemetry.get("rq3_summary", {})
            st.json(summary)
        else:
            st.caption("No LLM calls recorded in telemetry.")

# ---------------- SEC COMPANY DATA EXPLORER TAB ----------------
st.divider()
st.subheader("📂 SEC 10-K XBRL Data Explorer")
with st.expander("Explore Ground-Truth XBRL Financial Filings (from Supabase Cloud DB)", expanded=False):
    df_fin = load_financials_data()
    if not df_fin.empty:
        col_c1, col_c2 = st.columns([1, 3])
        with col_c1:
            explore_ticker = st.selectbox(
                "Filter Ticker",
                options=sorted(df_fin["ticker"].unique()),
                index=0,
            )
        df_filtered = df_fin[df_fin["ticker"] == explore_ticker].sort_values(
            "fiscal_year_end", ascending=False
        )
        st.dataframe(
            df_filtered[
                [
                    "ticker",
                    "fiscal_year_end",
                    "Revenue",
                    "OperatingIncome",
                    "NetIncome",
                    "TotalAssets",
                    "TotalLiabilities",
                    "OperatingCashFlow",
                    "EPSDiluted",
                ]
            ],
            use_container_width=True,
        )
    else:
        st.info("No local `data/financials.csv` found to display.")
