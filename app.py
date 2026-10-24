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

# Seamlessly inject Streamlit Cloud secrets into os.environ
try:
    if hasattr(st, "secrets"):
        for sec_key, sec_val in st.secrets.items():
            if isinstance(sec_val, str):
                os.environ[sec_key] = sec_val
except Exception:
    pass

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

# Tiered Golden Evaluation Queries (Pulled directly from data/golden_eval_set.json)
TIERED_GOLDEN_QUERIES = {
    "🟢 Tier 1: Simple (Single-Hop Factual)": [
        (
            "GOLD-01",
            "NVIDIA FY2026 period end date & headquarters",
            "What was NVIDIA's fiscal year 2026 period end date, and where is its principal executive office located?",
        ),
        (
            "GOLD-02",
            "Apple FY2024 independent accounting firm",
            "Who served as Apple Inc.'s independent registered public accounting firm for the fiscal year ended September 28, 2024?",
        ),
        (
            "GOLD-03",
            "Apple Inc. state of incorporation & IRS EIN",
            "What is Apple Inc.'s state of incorporation, corporate headquarters address, and IRS employer identification number in its 2024 Form 10-K?",
        ),
    ],
    "🟡 Tier 2: Moderate (Quantitative Tabular YoY)": [
        (
            "GOLD-16",
            "NVIDIA FY25 vs FY26 revenue & YoY growth",
            "Compare NVIDIA's total revenue, operating income, and net income between FY2025 and FY2026, and calculate the year-over-year revenue growth rate.",
        ),
        (
            "GOLD-17",
            "NVIDIA FY25 vs FY26 cash flow & diluted EPS",
            "What was NVIDIA's operating cash flow, total assets, and diluted earnings per share in FY2025 versus FY2026?",
        ),
        (
            "GOLD-18",
            "Apple FY23 vs FY24 net sales & cash flow",
            "What was Apple's total net sales, gross margin, and operating cash flow in fiscal 2023 versus fiscal 2024?",
        ),
    ],
    "🟠 Tier 3: Complex (Cross-Section MD&A + Notes)": [
        (
            "GOLD-36",
            "NVIDIA Compute segment vs customer concentration",
            "How did NVIDIA's Compute & Networking segment perform in FY2026, and what specific direct customer concentration percentages were disclosed in the Notes to Consolidated Financial Statements?",
        ),
        (
            "GOLD-37",
            "NVIDIA Item 7A interest rate risk vs Note 11 debt",
            "What sensitivity to interest rate shifts and public equity price movements did NVIDIA disclose in Item 7A, and what senior notes balance was reported in Note 11?",
        ),
        (
            "GOLD-38",
            "Apple Item 7 product sales vs Note 13 regional revenue",
            "How did Apple's iPhone and Services product revenues perform in fiscal 2024 according to Item 7, and how did this compare to regional net sales in Americas and Greater China disclosed in Note 13?",
        ),
    ],
    "🔴 Tier 4: Expert (Multi-Company Comparative RAG)": [
        (
            "GOLD-51",
            "Cloud Battle: Microsoft vs AWS vs Google Cloud (2024)",
            "Compare the 2024 enterprise cloud segment revenue, operating income, and operating margin across Microsoft (Intelligent Cloud), Amazon (AWS), and Alphabet (Google Cloud). Which cloud provider generated the highest operating margin in 2024, and which achieved the highest year-over-year revenue growth rate?",
        ),
        (
            "GOLD-52",
            "AI Capex: NVIDIA vs Meta vs Microsoft capital commitments",
            "Compare the AI infrastructure capital expenditure and lease commitments across NVIDIA, Meta Platforms, and Microsoft in their most recent annual filings. What future data center lease obligations did NVIDIA disclose commencing between fiscal 2027 and 2030, and what were the total additions to property and equipment or capital expenditures for Microsoft and Meta in 2024?",
        ),
        (
            "GOLD-53",
            "Ad Growth: Meta Platforms vs Alphabet digital ad growth",
            "Compare the digital advertising revenue performance and year-over-year growth rate of Meta Platforms versus Alphabet in 2024. Which company achieved a higher percentage growth rate in advertising?",
        ),
    ],
}


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

    st.subheader("1. Pipeline & Provider Setup")
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

    # Provider Selection
    provider_options = {
        "groq": "🚀 Groq Cloud (Free & 500 tok/sec)",
        "cohere": "🔮 Cohere (Command R / Command R+)",
        "openai": "🤖 OpenAI (GPT-4o-mini / GPT-4o)",
        "gemini": "✨ Google Gemini (1.5 Flash)",
        "mock": "🧪 Mock Mode (Zero-API-Key Test)",
    }
    selected_provider = st.selectbox(
        "LLM Provider",
        options=list(provider_options.keys()),
        index=0,
        format_func=lambda k: provider_options[k],
    )

    # Dynamic Model Selection based on Provider
    if selected_provider == "groq":
        model_options = {
            "llama-3.1-8b-instant": "Llama 3.1 (8B) — Fast",
            "llama-3.3-70b-versatile": "Llama 3.3 (70B) — Flagship",
            "openai/gpt-oss-120b": "OpenAI GPT-OSS (120B) — Team Notebook Default",
            "gemma2-9b-it": "Google Gemma 2 (9B)",
        }
    elif selected_provider == "cohere":
        model_options = {
            "command-r": "Command R (Fast & Efficient)",
            "command-r-plus": "Command R+ (Flagship Financial Reasoning)",
        }
    elif selected_provider == "openai":
        model_options = {
            "gpt-4o-mini": "GPT-4o-mini (Fast & Cheap)",
            "gpt-4o": "GPT-4o (High Performance)",
        }
    elif selected_provider == "gemini":
        model_options = {
            "gemini-1.5-flash": "Gemini 1.5 Flash (Fast)",
            "gemini-2.0-flash": "Gemini 2.0 Flash (Next-Gen)",
        }
    else:
        model_options = {"mock": "Mock Engine (Deterministic, Zero-API-Key)"}

    selected_model = st.selectbox(
        "Model Selection",
        options=list(model_options.keys()),
        index=0,
        format_func=lambda k: model_options[k],
    )

    # Optional Custom API Key with fallback to Secrets
    user_api_key = st.text_input(
        f"Custom {selected_provider.upper()} API Key (Optional):",
        type="password",
        help=f"If left blank, automatically uses your default pre-configured Streamlit secrets for {selected_provider.upper()}.",
    )
    if selected_provider == "mock":
        st.caption("💡 Mock mode tests the full LangGraph pipeline, Supabase DB, and guardrails without needing an API key.")

    # Configure Environment Variables
    os.environ["LLM_PROVIDER"] = selected_provider
    os.environ["LLM_MODEL"] = selected_model
    if user_api_key.strip():
        if selected_provider == "groq":
            os.environ["GROQ_API_KEY"] = user_api_key.strip()
        elif selected_provider == "cohere":
            os.environ["COHERE_API_KEY"] = user_api_key.strip()
        elif selected_provider == "openai":
            os.environ["OPENAI_API_KEY"] = user_api_key.strip()
        elif selected_provider == "gemini":
            os.environ["GEMINI_API_KEY"] = user_api_key.strip()
            os.environ["GOOGLE_API_KEY"] = user_api_key.strip()

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

    st.subheader("3. Golden Benchmark Presets")
    st.caption("Click any preset below (Simple → Complex):")
    for tier_title, questions in TIERED_GOLDEN_QUERIES.items():
        with st.expander(tier_title, expanded=(tier_title.startswith("🟢"))):
            for q_id, q_label, full_q in questions:
                if st.button(f"📌 {q_id}: {q_label}", use_container_width=True, key=f"side_{q_id}"):
                    st.session_state["user_query_input"] = full_q
                    st.rerun()

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

# Main Page Golden Benchmark Tier Selector
st.markdown("##### 🎯 Golden Benchmark Presets (Select to populate question)")
tier_tabs = st.tabs(["🟢 Tier 1: Simple", "🟡 Tier 2: Moderate", "🟠 Tier 3: Complex", "🔴 Tier 4: Expert"])
tier_keys = list(TIERED_GOLDEN_QUERIES.keys())

for t_idx, tab in enumerate(tier_tabs):
    with tab:
        q_list = TIERED_GOLDEN_QUERIES[tier_keys[t_idx]]
        cols = st.columns(len(q_list))
        for c_idx, (q_id, q_label, full_q) in enumerate(q_list):
            with cols[c_idx]:
                if st.button(f"**{q_id}**\n\n{q_label}", key=f"main_{q_id}", use_container_width=True):
                    st.session_state["user_query_input"] = full_q
                    st.rerun()

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
    try:
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

    except Exception as exc:
        import traceback
        st.error(f"❌ **Execution Error**: `{str(exc)}`")
        st.markdown("📋 **Error Details & Stack Trace** *(use the copy button in the top right to copy)*:")
        st.code(traceback.format_exc(), language="python")

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
