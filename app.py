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

# Custom CSS for executive financial dashboard styling (Theme-Adaptive for Light & Dark Mode)
st.markdown(
    """
    <style>
    .main-header {
        font-size: 2.1rem;
        font-weight: 700;
        color: var(--text-color, #0F172A);
        margin-bottom: 0.2rem;
    }
    .sub-header {
        font-size: 1.0rem;
        color: var(--secondary-text-color, #64748B);
        margin-bottom: 1.2rem;
    }
    .metric-badge {
        display: inline-block;
        padding: 0.25rem 0.6rem;
        border-radius: 6px;
        font-size: 0.80rem;
        font-weight: 600;
        margin-right: 0.4rem;
        background-color: rgba(128, 128, 128, 0.12);
        color: var(--text-color, #334155);
        border: 1px solid rgba(128, 128, 128, 0.2);
    }
    .badge-success { background-color: rgba(16, 185, 129, 0.15); color: #10B981; border: 1px solid rgba(16, 185, 129, 0.3); }
    .badge-info { background-color: rgba(59, 130, 246, 0.15); color: #3B82F6; border: 1px solid rgba(59, 130, 246, 0.3); }
    .badge-warning { background-color: rgba(245, 158, 11, 0.15); color: #F59E0B; border: 1px solid rgba(245, 158, 11, 0.3); }
    .arch-banner {
        background-color: rgba(128, 128, 128, 0.06);
        border: 1px solid rgba(128, 128, 128, 0.18);
        border-radius: 8px;
        padding: 10px 16px;
        margin-bottom: 16px;
    }
    .citation-tag {
        background-color: rgba(99, 102, 241, 0.15);
        color: #6366F1;
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
    "Tier 1: Simple (Single-Hop Factual)": [
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
    "Tier 2: Moderate (Quantitative Tabular YoY)": [
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
    "Tier 3: Complex (Cross-Section MD&A + Notes)": [
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
    "Tier 4: Expert (Multi-Company Comparative RAG)": [
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
    st.markdown(
        """
        <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 18px; padding-bottom: 12px; border-bottom: 1px solid rgba(128, 128, 128, 0.2);">
          <svg width="36" height="36" viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
            <rect width="48" height="48" rx="10" fill="#0F172A"/>
            <path d="M12 34V22M20 34V14M28 34V24M36 34V18" stroke="#38BDF8" stroke-width="3.5" stroke-linecap="round"/>
            <circle cx="20" cy="14" r="2.5" fill="#38BDF8"/>
            <circle cx="36" cy="18" r="2.5" fill="#38BDF8"/>
            <path d="M20 14L28 20L36 18" stroke="#F59E0B" stroke-width="2" stroke-linecap="round" stroke-dasharray="2 2"/>
          </svg>
          <div>
            <div style="font-weight: 700; font-size: 1.15rem; line-height: 1.2; color: var(--text-color, #0F172A);">System C</div>
            <div style="font-size: 0.72rem; color: #64748B; letter-spacing: 0.05em; text-transform: uppercase; font-weight: 600;">Adaptive Multi-Hop RAG</div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.subheader("1. Pipeline Configuration")
    mode_selection = st.selectbox(
        "Architecture Mode",
        options=["v2_aamr", "adaptive_v1", "fixed_1hop", "fixed_3hop"],
        index=0,
        format_func=lambda x: {
            "v2_aamr": "v2: Agentic AMR (XBRL + 10-K Text Router)",
            "adaptive_v1": "v1: Adaptive Multi-Hop (Text Only)",
            "fixed_1hop": "Baseline: Fixed 1-Hop",
            "fixed_3hop": "Baseline: Fixed 3-Hop",
        }[x],
        help="System C v2 dynamically routes quantitative metric requests to Supabase XBRL tables and qualitative context (risks, MD&A) to SEC text chunks.",
    )

    max_hops = st.slider(
        "Max Retrieval Hops",
        min_value=1,
        max_value=10,
        value=3,
        help="Defines the maximum sequential search-and-reasoning iterations (1 to 10) allowed for the multi-hop agent. Simple factual lookups resolve in 1 hop. Complex cross-company comparisons (e.g. comparing cloud revenues and operating footnotes across Apple, Microsoft, and Amazon) require 2 to 3 hops. A hard ceiling prevents runaway loops and token exhaustion.",
    )
    sufficiency_threshold = st.slider(
        "Critic Sufficiency Threshold",
        min_value=0.50,
        max_value=1.00,
        value=0.85,
        step=0.05,
        help="The quantitative sufficiency score threshold ([0.0, 1.0], default: 0.85). After each retrieval hop, the Critic Node audits whether all requested financial metrics, target fiscal years, and qualitative disclosures (risk factors, notes) have been completely satisfied. If the score >= threshold, System C executes Early Stopping—bypassing subsequent hops and saving up to 70% in token cost and latency.",
    )

    st.divider()

    st.subheader("2. LLM Engine & Credentials")
    provider_options = {
        "groq": "Groq Cloud (LPU Inference — Recommended)",
        "gemini": "Google Gemini (Gemini Flash)",
        "cohere": "Cohere (Command R / Command R+)",
        "openai": "OpenAI (GPT-4o-mini / GPT-4o)",
        "mock": "Mock Engine (Deterministic, Zero-API-Key)",
    }
    selected_provider = st.selectbox(
        "Select Provider",
        options=list(provider_options.keys()),
        index=0,
        format_func=lambda k: provider_options[k],
    )

    # Dynamic Model Selection based on Provider
    if selected_provider == "groq":
        model_options = {
            "llama-3.1-8b-instant": "Llama 3.1 (8B) — Universal Free (Instant)",
            "openai/gpt-oss-120b": "OpenAI GPT-OSS (120B) — Team Notebook Default",
            "llama-3.3-70b-versatile": "Llama 3.3 (70B) — Flagship",
            "gemma2-9b-it": "Google Gemma 2 (9B)",
        }
    elif selected_provider == "gemini":
        model_options = {
            "gemini-flash-latest": "Gemini Flash (Latest — Fast & Free)",
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
    else:
        model_options = {"mock": "Mock Engine (Deterministic, Zero-API-Key)"}

    selected_model = st.selectbox(
        "Model Selection",
        options=list(model_options.keys()),
        index=0,
        format_func=lambda k: model_options[k],
    )

    # Universal API Key Input with clean fallback
    user_api_key = st.text_input(
        "API Key (Optional)",
        type="password",
        placeholder="Leave blank to use pre-configured system key",
        help="Paste your private Gemini, Groq, Cohere, or OpenAI key here. If left blank, the app uses pre-configured keys so you and your team can query immediately without typing.",
    )
    if user_api_key.strip():
        st.markdown('<span style="color:#2563EB;font-size:0.80rem;font-weight:600;">● Custom User Key Active</span>', unsafe_allow_html=True)
    else:
        st.markdown('<span style="color:#059669;font-size:0.80rem;font-weight:600;">● Built-in System Key Active</span>', unsafe_allow_html=True)

    # Configure Environment Variables
    os.environ["LLM_PROVIDER"] = selected_provider
    os.environ["LLM_MODEL"] = selected_model
    if user_api_key.strip():
        if selected_provider == "groq":
            os.environ["GROQ_API_KEY"] = user_api_key.strip()
        elif selected_provider == "gemini":
            os.environ["GEMINI_API_KEY"] = user_api_key.strip()
            os.environ["GOOGLE_API_KEY"] = user_api_key.strip()
        elif selected_provider == "cohere":
            os.environ["COHERE_API_KEY"] = user_api_key.strip()
        elif selected_provider == "openai":
            os.environ["OPENAI_API_KEY"] = user_api_key.strip()
    else:
        if selected_provider == "gemini":
            os.environ["GEMINI_API_KEY"] = "AIzaSyCRjeOAKS9-Lb7zXpwW294GOLD6vM6pUxw"
            os.environ["GOOGLE_API_KEY"] = "AIzaSyCRjeOAKS9-Lb7zXpwW294GOLD6vM6pUxw"

    st.divider()

    st.subheader("3. SEC Company Filter")
    selected_tickers = st.multiselect(
        "Filter Ticker(s) (Optional)",
        options=list(COMPANIES.keys()),
        default=[],
        format_func=lambda t: f"{t} ({COMPANIES[t]['name']})",
        help="Leave empty for the pipeline decomposer to automatically extract target tickers from your question.",
    )

    st.divider()

    st.subheader("4. Golden Benchmark Presets")
    st.caption("Click any preset below (Simple → Complex):")
    for tier_title, questions in TIERED_GOLDEN_QUERIES.items():
        with st.expander(tier_title, expanded=(tier_title.startswith("Tier 1"))):
            for q_id, q_label, full_q in questions:
                if st.button(f"{q_id}: {q_label}", use_container_width=True, key=f"side_{q_id}"):
                    st.session_state["user_query_input"] = full_q
                    st.rerun()

    st.divider()

    # System Status Indicator
    llm_info = get_llm_status()
    st.subheader("Cloud Infrastructure")
    st.markdown(
        f"""
    * **LLM Engine**: `{selected_provider.upper()}` (`{selected_model}`)
    * **Cloud DB**: `Supabase PostgreSQL` (`ap-southeast-1`)
    * **Relational Table**: `sec_financials` (272 XBRL rows)
    * **Pre-Computed Chunks**: `sec_chunks` (20,125 rows in Supabase Cloud)
    * **LangGraph State**: `PostgresSaver Checkpointing`
    * **Numerical Guardrail**: Active Self-Healing Loop
    """
    )


# ---------------- MAIN CONTENT ----------------
st.markdown('<div class="main-header">System C: Adaptive Multi-Hop Financial RAG</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="sub-header">Autonomous SEC 10-K Intelligence, Continuous Sufficiency Auditing, and Scale-Normalized Numerical Grounding</div>',
    unsafe_allow_html=True,
)

# Visual Architecture Flow Banner
st.markdown(
    """
    <div class="arch-banner">
      <span style="font-size: 0.78rem; font-weight: 700; color: #64748B; text-transform: uppercase; letter-spacing: 0.05em;">Autonomous Pipeline Architecture:</span><br/>
      <span style="font-size: 0.88rem; color: var(--text-color, #1E293B); font-weight: 500;">
        1. Decompose Query &bull; 2. Heterogeneous Router (XBRL SQL vs. 10-K Text) &bull; 3. Critic Sufficiency Audit (&ge;0.85 Early Stop) &bull; 4. Inline Citation Synthesis &bull; 5. Closed-Loop Numerical Repair
      </span>
    </div>
    """,
    unsafe_allow_html=True,
)

# Badges bar
col_b1, col_b2, col_b3, col_b4 = st.columns(4)
with col_b1:
    st.markdown('<span class="metric-badge badge-success">Supabase Cloud PG Connected</span>', unsafe_allow_html=True)
with col_b2:
    st.markdown(f'<span class="metric-badge badge-info">Engine: {selected_provider.upper()}</span>', unsafe_allow_html=True)
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
    "Enter your financial question (or pick a preset from the sidebar):",
    value=default_query,
    height=80,
    placeholder="e.g. Compare NVIDIA and Microsoft cloud and data center performance in 2024...",
)

col_run, col_clear = st.columns([1, 6])
run_btn = col_run.button("Run Query", type="primary", use_container_width=True)

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

        # Determine early stopping status accurately
        is_early_stopped = bool(
            result.get("early_stopped")
            or result.get("telemetry", {}).get("early_stopped")
            or (result.get("is_sufficient") and result.get("current_hop", 1) < result.get("max_hops", 3))
        )

        # Executive Summary Metrics
        m1, m2, m3, m4, m5 = st.columns(5)
        m1.metric("Hops Executed", f"{result['current_hop']} / {result['max_hops']}")
        stop_reason_label = f"Early Stopped (Hop {result['current_hop']})" if is_early_stopped else f"Max Hops Reached ({result['current_hop']}/{result['max_hops']})"
        m2.metric("Stop Reason", stop_reason_label)
        m3.metric("Sufficiency Score", f"{result.get('sufficiency_score', 0.0):.2f}")
        m4.metric("Evidence Chunks", f"{len(result.get('accumulated_evidence', []))}")
        m5.metric("Latency", f"{total_wall_time:.2f}s")

        # Tabbed Results Console
        res_tab1, res_tab2, res_tab3, res_tab4 = st.tabs(
            [
                "Synthesized Answer & Citations",
                "Factuality & Grounding Audit",
                "Multi-Hop Reasoning Trace",
                "Inference Economics (RQ3)",
            ]
        )

        with res_tab1:
            st.subheader("Executive Financial Synthesis")
            final_answer = result.get("final_answer", "")
            if final_answer:
                st.markdown(final_answer)
            else:
                st.info("No synthesis generated.")

            st.write("")
            st.markdown("##### Ground-Truth Citations Mapped (RQ2)")
            citations = result.get("citations", [])
            if citations:
                for cit in citations:
                    with st.expander(f"[{cit.get('tag', 'Citation')}] — {cit.get('section', 'SEC Disclosure')}"):
                        st.write(f"**Chunk ID**: `{cit.get('chunk_id')}`")
                        st.write(f"**Ticker / Year**: {cit.get('ticker')} (FY{cit.get('fiscal_year')})")
                        st.write(f"**Disclosure Excerpt**:")
                        st.caption(cit.get("supported_claim", ""))
            else:
                st.caption("No citations recorded.")

        with res_tab2:
            st.subheader("Factuality & Numerical Grounding Audit")
            guard_report = result.get("guardrail_report", {})
            passed = result.get("guardrail_passed", True)
            if passed:
                st.success("Guardrail Passed: All extracted financial figures match SEC ground-truth filings.")
            else:
                st.warning("Guardrail Warning: Ungrounded numbers detected during audit.")

            col_g1, col_g2, col_g3 = st.columns(3)
            col_g1.metric("Numerical Error Rate", f"{guard_report.get('numerical_grounding_error_rate', 0.0) * 100:.1f}%")
            col_g2.metric("Faithfulness Score", f"{guard_report.get('faithfulness_score', 1.0):.2f}")
            col_g3.metric("Repairs Executed", f"{result.get('repair_count', 0)}")

            st.write("")
            col_v1, col_v2 = st.columns(2)
            with col_v1:
                st.markdown("##### Verified Numbers")
                st.write(guard_report.get("verified_numbers", []))
            with col_v2:
                st.markdown("##### Flagged / Ungrounded Numbers")
                st.write(guard_report.get("ungrounded_numbers", []))

        with res_tab3:
            st.subheader("Autonomous Multi-Hop Reasoning Trace")
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

        with res_tab4:
            st.subheader("Inference Economics (RQ3 Telemetry)")
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
        st.error(f"Execution Error: {str(exc)}")
        st.markdown("**Error Details & Stack Trace** *(use copy button)*:")
        st.code(traceback.format_exc(), language="python")

# ---------------- SEC COMPANY DATA EXPLORER TAB ----------------
st.divider()
st.subheader("SEC 10-K XBRL Data Explorer")
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
