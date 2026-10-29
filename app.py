"""
System C: Adaptive Multi-Hop Financial RAG (Institutional Quant Terminal UI — Option A)
Interactive Real-Time Streaming Web Demo for SEC 10-K Filings
"""

import html
import os
import re
import sys
import time
from typing import Any, Dict, List, Optional, Tuple

import pandas as pd
import streamlit as st
from dotenv import load_dotenv

from src.system_c.benchmark_adapter import (
    FEATURED_BENCHMARK_IDS,
    benchmark_to_system_c_query,
    get_benchmark_by_id,
    get_featured_benchmark_questions,
    load_benchmark_pool,
    run_finqa_program,
)

# Ensure repo root is in sys.path
REPO_ROOT = os.path.abspath(os.path.dirname(__file__))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

load_dotenv(override=True)

# Seamlessly inject Streamlit Cloud / Hugging Face Spaces secrets into os.environ
try:
    if hasattr(st, "secrets"):
        for sec_key, sec_val in st.secrets.items():
            if isinstance(sec_val, str):
                os.environ[sec_key] = sec_val
except Exception:
    pass

# Page configuration
st.set_page_config(
    page_title="Institutional SEC 10-K Quantitative Research Terminal",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------------------------
# OPTION A: INSTITUTIONAL QUANTITATIVE (BLOOMBERG / KOYFIN PRECISION) CSS
# ---------------------------------------------------------------------------
CUSTOM_CSS = """
:root {
    color-scheme: light dark;
    --bg-canvas-light: #F4F5F7;
    --bg-surface-light: #FFFFFF;
    --bg-elevated-light: #ECEEF2;
    --text-primary-light: #0F172A;
    --text-secondary-light: #334155;
    --text-muted-light: #64748B;
    --border-grid-light: #CBD5E1;
    --bg-canvas-dark: #0A0D12;
    --bg-surface-dark: #11161F;
    --bg-elevated-dark: #161D28;
    --text-primary-dark: #F1F5F9;
    --text-secondary-dark: #CBD5E1;
    --text-muted-dark: #94A3B8;
    --border-grid-dark: #263040;
    --term-bg-canvas: var(--bg-canvas-light);
    --term-bg-surface: var(--bg-surface-light);
    --term-bg-elevated: var(--bg-elevated-light);
    --term-text-primary: var(--text-primary-light);
    --term-text-secondary: var(--text-secondary-light);
    --term-text-muted: var(--text-muted-light);
    --term-border: var(--border-grid-light);
    --quant-amber: #F59E0B;
    --quant-emerald: #10B981;
    --quant-cyan: #06B6D4;
    --quant-blue: #3B82F6;
    --quant-indigo: #6366F1;
    --quant-violet: #8B5CF6;
    --quant-rose: #F43F5E;
    --quant-radius: 4px;
    --quant-mono: ui-monospace, "JetBrains Mono", "IBM Plex Mono", SFMono-Regular, Menlo, Monaco, Consolas, monospace;
    --brand-accent-light: #2563EB;
    --brand-accent-dark: #F59E0B;
    --accent-color: var(--brand-accent-light);
}
@media (prefers-color-scheme: dark) {
    :root {
        --term-bg-canvas: var(--bg-canvas-dark);
        --term-bg-surface: var(--bg-surface-dark);
        --term-bg-elevated: var(--bg-elevated-dark);
        --term-text-primary: var(--text-primary-dark);
        --term-text-secondary: var(--text-secondary-dark);
        --term-text-muted: var(--text-muted-dark);
        --term-border: var(--border-grid-dark);
        --accent-color: var(--brand-accent-dark);
    }
}
@supports (color: light-dark(white, black)) {
    :root {
        --term-bg-canvas: light-dark(var(--bg-canvas-light), var(--bg-canvas-dark));
        --term-bg-surface: light-dark(var(--bg-surface-light), var(--bg-surface-dark));
        --term-bg-elevated: light-dark(var(--bg-elevated-light), var(--bg-elevated-dark));
        --term-text-primary: light-dark(var(--text-primary-light), var(--text-primary-dark));
        --term-text-secondary: light-dark(var(--text-secondary-light), var(--text-secondary-dark));
        --term-text-muted: light-dark(var(--text-muted-light), var(--text-muted-dark));
        --term-border: light-dark(var(--border-grid-light), var(--border-grid-dark));
        --accent-color: light-dark(var(--brand-accent-light), var(--brand-accent-dark));
    }
}
html {
    accent-color: var(--accent-color);
    font-variant-numeric: tabular-nums;
}
@media (forced-colors: active) {
    .pipeline-shell, .node-box, .gauge-card, .grounding-pill, .timeline-card, .dossier-shell {
        border: 2px solid CanvasText !important;
    }
}
.sidebar-brand-wrap {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 16px;
    padding: 11px 13px;
    border-radius: var(--quant-radius);
    background: var(--term-bg-surface);
    border: 1px solid var(--term-border);
    border-left: 3.5px solid var(--quant-amber);
}
.sidebar-brand-title {
    font-family: var(--quant-mono);
    font-weight: 800;
    font-size: 1.05rem;
    line-height: 1.2;
    color: var(--text-color, var(--term-text-primary)) !important;
    letter-spacing: -0.02em;
}
.sidebar-brand-sub {
    font-family: var(--quant-mono);
    font-size: 0.68rem;
    color: var(--quant-amber) !important;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    font-weight: 700;
    margin-top: 2px;
}
.terminal-top-bar {
    display: flex;
    flex-wrap: wrap;
    justify-content: space-between;
    align-items: flex-end;
    gap: 12px;
    padding-bottom: 10px;
    margin-bottom: 12px;
    border-bottom: 1px solid var(--term-border);
}
.terminal-eyebrow {
    font-family: var(--quant-mono);
    font-size: 0.72rem;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: var(--quant-amber);
    margin-bottom: 2px;
}
.main-header {
    font-size: 1.95rem;
    font-weight: 800;
    color: var(--text-color, var(--term-text-primary));
    letter-spacing: -0.025em;
    margin-bottom: 0.1rem;
    line-height: 1.15;
}
.sub-header {
    font-size: 0.90rem;
    color: var(--text-color, var(--term-text-secondary));
    opacity: 0.85;
    font-weight: 500;
}
.terminal-status-cluster {
    display: flex;
    gap: 6px;
    flex-wrap: wrap;
    align-items: center;
}
.metric-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 4px 9px;
    border-radius: var(--quant-radius);
    font-family: var(--quant-mono);
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.03em;
    text-transform: uppercase;
    background: var(--term-bg-surface);
    color: var(--text-color, var(--term-text-primary));
    border: 1px solid var(--term-border);
}
.badge-emerald {
    background: rgba(16, 185, 129, 0.12);
    color: #10B981;
    border-color: rgba(16, 185, 129, 0.45);
}
.badge-amber {
    background: rgba(245, 158, 11, 0.14);
    color: #F59E0B;
    border-color: rgba(245, 158, 11, 0.5);
}
.badge-cyan {
    background: rgba(6, 182, 212, 0.12);
    color: #06B6D4;
    border-color: rgba(6, 182, 212, 0.45);
}
.badge-blue {
    background: rgba(59, 130, 246, 0.12);
    color: #3B82F6;
    border-color: rgba(59, 130, 246, 0.45);
}
div.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #1D4ED8 0%, #2563EB 50%, #4F46E5 100%) !important;
    color: #FFFFFF !important;
    border: 1px solid rgba(96, 165, 250, 0.55) !important;
    border-radius: var(--quant-radius) !important;
    font-family: var(--quant-mono) !important;
    font-weight: 700 !important;
    font-size: 0.84rem !important;
    letter-spacing: 0.04em !important;
    text-transform: uppercase !important;
    padding: 0.55rem 1.15rem !important;
    box-shadow: 0 2px 10px rgba(37, 99, 235, 0.3) !important;
    transition: all 0.18s ease !important;
}
div.stButton > button[kind="primary"]:hover {
    background: linear-gradient(135deg, #2563EB 0%, #3B82F6 50%, #6366F1 100%) !important;
    box-shadow: 0 0 18px rgba(59, 130, 246, 0.55) !important;
    border-color: #60A5FA !important;
    transform: translateY(-1px) !important;
}
@keyframes quantActivePulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.55; }
}
@keyframes dashFlow {
    to { stroke-dashoffset: -20; }
}
.pipeline-shell {
    background: var(--term-bg-surface);
    border: 1px solid var(--term-border);
    border-radius: var(--quant-radius);
    padding: 14px 16px;
    margin-bottom: 14px;
    font-variant-numeric: tabular-nums;
}
.pipeline-header-bar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 8px;
    padding-bottom: 10px;
    margin-bottom: 12px;
    border-bottom: 1px solid var(--term-border);
}
.pipeline-title {
    font-family: var(--quant-mono);
    font-size: 0.76rem;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 0.07em;
    color: var(--text-color, var(--term-text-primary));
    display: flex;
    align-items: center;
    gap: 8px;
}
.hop-banner {
    padding: 4px 10px;
    border-radius: var(--quant-radius);
    font-family: var(--quant-mono);
    font-size: 0.74rem;
    font-weight: 700;
    letter-spacing: 0.03em;
}
.hop-banner-active {
    background: rgba(245, 158, 11, 0.15);
    color: #F59E0B;
    border: 1px solid rgba(245, 158, 11, 0.55);
}
.hop-banner-normal {
    background: rgba(59, 130, 246, 0.12);
    color: #38BDF8;
    border: 1px solid rgba(56, 189, 248, 0.45);
}
.hop-banner-complete {
    background: rgba(16, 185, 129, 0.13);
    color: #10B981;
    border: 1px solid rgba(16, 185, 129, 0.45);
}
.sys-tier-card {
    border-radius: var(--quant-radius);
    padding: 10px 12px;
    margin-bottom: 10px;
    transition: all 0.22s ease;
    background: var(--term-bg-canvas);
    border: 1px solid var(--term-border);
}
.sys-tier-card.sys-tier-active {
    opacity: 1.0;
    background: var(--term-bg-surface);
    border: 1px solid rgba(59, 130, 246, 0.55);
    border-left: 4px solid var(--quant-amber);
    box-shadow: 0 4px 18px rgba(15, 23, 42, 0.14);
}
.sys-tier-card.sys-tier-inactive {
    opacity: 0.34;
    filter: grayscale(0.80);
    border: 1px dashed var(--term-border);
    padding: 7px 11px;
}
.sys-tier-card.sys-tier-inactive .node-box {
    min-height: 62px;
    padding: 7px 9px;
}
.sys-tier-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 6px;
    margin-bottom: 8px;
}
.sys-tier-title {
    font-family: var(--quant-mono);
    font-size: 0.74rem;
    font-weight: 800;
    letter-spacing: 0.05em;
    text-transform: uppercase;
    display: flex;
    align-items: center;
    gap: 8px;
}
.nodes-grid {
    display: grid;
    grid-template-columns: repeat(6, minmax(130px, 1fr));
    gap: 8px;
    align-items: stretch;
}
.nodes-grid-5 {
    display: grid;
    grid-template-columns: repeat(5, minmax(130px, 1fr));
    gap: 8px;
    align-items: stretch;
}
.nodes-grid-3 {
    display: grid;
    grid-template-columns: repeat(3, minmax(150px, 1fr));
    gap: 8px;
    align-items: stretch;
}
@media (max-width: 1100px) {
    .nodes-grid, .nodes-grid-5 {
        grid-template-columns: repeat(3, minmax(140px, 1fr));
    }
}
@media (max-width: 640px) {
    .nodes-grid, .nodes-grid-5, .nodes-grid-3 {
        grid-template-columns: repeat(2, 1fr);
    }
}
.node-box {
    position: relative;
    border-radius: var(--quant-radius);
    padding: 10px 11px;
    background: var(--term-bg-elevated);
    border: 1px solid var(--term-border);
    transition: all 0.2s ease;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    min-height: 88px;
}
.node-box.state-idle {
    opacity: 0.5;
}
.node-box.state-skipped {
    opacity: 0.4;
    border-style: dashed;
}
.node-top {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 4px;
    margin-bottom: 5px;
}
.node-step-num {
    font-family: var(--quant-mono);
    font-size: 0.68rem;
    font-weight: 800;
    color: var(--text-color, var(--term-text-muted));
}
.node-status-tag {
    font-family: var(--quant-mono);
    font-size: 0.64rem;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 0.04em;
    padding: 1px 5px;
    border-radius: 3px;
}
.node-name {
    font-size: 0.80rem;
    font-weight: 800;
    color: var(--text-color, var(--term-text-primary));
    line-height: 1.25;
    margin-bottom: 4px;
}
.node-telemetry {
    font-family: var(--quant-mono);
    font-size: 0.70rem;
    color: var(--text-color, var(--term-text-secondary));
    opacity: 0.88;
    line-height: 1.25;
    font-variant-numeric: tabular-nums;
}
.loop-trace-bar {
    margin-top: 8px;
    padding: 6px 12px;
    border-radius: var(--quant-radius);
    background: var(--term-bg-elevated);
    border: 1px solid var(--term-border);
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 12px;
    flex-wrap: wrap;
}
.telemetry-strip {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 8px;
    margin-top: 10px;
    padding-top: 10px;
    border-top: 1px solid var(--term-border);
}
@media (max-width: 1024px) {
    .telemetry-strip {
        grid-template-columns: repeat(3, 1fr);
    }
}
@media (max-width: 640px) {
    .telemetry-strip {
        grid-template-columns: repeat(2, 1fr);
    }
}
.gauge-card {
    background: var(--term-bg-elevated);
    border: 1px solid var(--term-border);
    border-radius: var(--quant-radius);
    padding: 7px 10px;
}
.gauge-label {
    font-family: var(--quant-mono);
    font-size: 0.65rem;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    color: var(--text-color, var(--term-text-muted));
    opacity: 0.85;
    font-weight: 700;
}
.gauge-val {
    font-family: var(--quant-mono);
    font-size: 0.88rem;
    font-weight: 800;
    color: var(--text-color, var(--term-text-primary));
    margin-top: 2px;
    font-variant-numeric: tabular-nums;
}
.gauge-bar-track {
    width: 100%;
    height: 4px;
    background: rgba(148, 163, 184, 0.2);
    border-radius: 2px;
    overflow: hidden;
    margin-top: 4px;
}
.gauge-bar-fill {
    height: 100%;
    transition: width 0.3s ease;
}
.pills-wrap {
    display: flex;
    flex-wrap: wrap;
    gap: 7px;
    margin-top: 6px;
    margin-bottom: 12px;
}
.grounding-pill {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 5px 10px;
    border-radius: var(--quant-radius);
    font-family: var(--quant-mono);
    font-size: 0.78rem;
    font-weight: 700;
    font-variant-numeric: tabular-nums;
    transition: transform 0.12s ease;
    cursor: help;
}
.grounding-pill:hover {
    transform: translateY(-1px);
}
.pill-verified {
    background: rgba(16, 185, 129, 0.11);
    color: #10B981;
    border: 1px solid rgba(16, 185, 129, 0.45);
}
.pill-verified .pill-source {
    font-size: 0.68rem;
    padding: 1px 5px;
    border-radius: 2px;
    background: rgba(16, 185, 129, 0.16);
    color: var(--text-color, var(--term-text-primary));
    font-weight: 600;
}
.pill-ungrounded {
    background: rgba(244, 63, 94, 0.12);
    color: #F43F5E;
    border: 1px solid rgba(244, 63, 94, 0.5);
}
.pill-ungrounded .strike-num {
    text-decoration: line-through;
    text-decoration-thickness: 2px;
}
.pill-ungrounded .pill-flag-tag {
    font-size: 0.65rem;
    padding: 1px 5px;
    border-radius: 2px;
    background: rgba(245, 158, 11, 0.22);
    color: #F59E0B;
    font-weight: 800;
    text-decoration: none;
}
.dossier-shell {
    background: var(--term-bg-surface);
    border: 1px solid var(--term-border);
    border-left: 3.5px solid var(--quant-amber);
    border-radius: var(--quant-radius);
    margin-bottom: 14px;
    overflow: hidden;
    font-variant-numeric: tabular-nums;
}
.dossier-tape {
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 8px;
    padding: 8px 16px;
    background: var(--term-bg-elevated);
    border-bottom: 1px solid var(--term-border);
    font-family: var(--quant-mono);
    font-size: 0.72rem;
    color: var(--text-color, var(--term-text-secondary));
}
.citation-chip {
    display: inline-block;
    background: var(--term-bg-elevated);
    color: var(--text-color, var(--term-text-secondary));
    border: 1px solid var(--term-border);
    font-family: var(--quant-mono);
    padding: 0px 6px;
    border-radius: 3px;
    font-size: 0.74em;
    font-weight: 700;
    vertical-align: baseline;
    margin: 0 1px;
}
.timeline-container {
    position: relative;
    padding-left: 22px;
    margin-top: 10px;
    font-variant-numeric: tabular-nums;
}
.timeline-container::before {
    content: "";
    position: absolute;
    left: 7px;
    top: 8px;
    bottom: 8px;
    width: 2px;
    background: var(--term-border);
}
.timeline-card {
    position: relative;
    background: var(--term-bg-surface);
    border: 1px solid var(--term-border);
    border-radius: var(--quant-radius);
    padding: 12px 16px;
    margin-bottom: 12px;
}
.timeline-dot {
    position: absolute;
    left: -20px;
    top: 16px;
    width: 12px;
    height: 12px;
    border-radius: 2px;
    border: 2px solid var(--term-bg-surface);
}
.timeline-loop-edge {
    position: relative;
    margin: -2px 0 10px 0;
    padding: 8px 12px;
    border-radius: var(--quant-radius);
    background: rgba(245, 158, 11, 0.1);
    border: 1px dashed rgba(245, 158, 11, 0.55);
    color: #F59E0B;
    font-family: var(--quant-mono);
    font-size: 0.76rem;
    font-weight: 700;
}
"""

# Strip any empty lines so CommonMark never breaks out of the <style> HTML block
clean_css = "\n".join(line.strip() for line in CUSTOM_CSS.splitlines() if line.strip())
st.markdown(f"<style>{clean_css}</style>", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# STATIC DATA & BENCHMARK PRESETS
# ---------------------------------------------------------------------------
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

TIERED_GOLDEN_QUERIES = {
    "Tier 1: Single-Hop Factual (1 Hop — Early-Stopping Baseline)": [
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
    "Tier 2: Quantitative Tabular YoY (2 Hops — Multi-Period Reconciliation)": [
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
    "Tier 3: Cross-Section MD&A + Notes (2 Hops — Narrative to Footnotes)": [
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
    "Tier 4: Multi-Company Comparative RAG (3 Hops — Multi-Entity Deep Dive)": [
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

BENCHMARK_RECIPE_GROUPS = {
    "Single Table Quantitative Math (10 Qs)": "table",
    "Cross-Year Multi-Hop Table Reconciliation (6 Qs)": "cross_year_table",
    "Table + Footnotes Hybrid Verification (12 Qs)": "table_text",
    "Narrative Business Strategy & Risk (8 Qs)": "text",
    "Cross-Year Qualitative Evolution (4 Qs)": "cross_year_text",
}

NODE_META = [
    {
        "id": "decomposer",
        "step": "C.01",
        "title": "Query Planner",
        "subtitle": "Decomposer",
        "color": "#06B6D4",
        "default_desc": "Extracts entities & atomic plan",
    },
    {
        "id": "tabular_tool",
        "step": "C.02",
        "title": "SEC XBRL Tables",
        "subtitle": "Tabular Router",
        "color": "#10B981",
        "default_desc": "Direct SQL table lookup (100% exact)",
    },
    {
        "id": "retriever",
        "step": "C.03",
        "title": "10-K Text Search",
        "subtitle": "Hybrid Retriever",
        "color": "#3B82F6",
        "default_desc": "Multi-hop evidence retrieval",
    },
    {
        "id": "critic",
        "step": "C.04",
        "title": "Sufficiency Critic",
        "subtitle": "Self-RAG Auditor (SYS C Only)",
        "color": "#F59E0B",
        "default_desc": "Audits sufficiency for early stop",
    },
    {
        "id": "synthesizer",
        "step": "C.05",
        "title": "Executive Synthesizer",
        "subtitle": "Citation Mapper",
        "color": "#6366F1",
        "default_desc": "Drafts brief with exact citations",
    },
    {
        "id": "guardrail",
        "step": "C.06",
        "title": "Active Guardrail",
        "subtitle": "Scale Verifier + Repair",
        "color": "#8B5CF6",
        "default_desc": "Verifies & self-heals numbers",
    },
]

NODE_META_SYS_B = [
    {
        "id": "b_scope",
        "step": "B.01",
        "title": "Metadata Scope",
        "subtitle": "Ticker & Filing Filter",
        "color": "#06B6D4",
        "default_desc": "Filters ticker/year filing pairs",
    },
    {
        "id": "b_bm25",
        "step": "B.02",
        "title": "Okapi BM25 Sparse",
        "subtitle": "Lexical Search (k1=1.5, b=0.75)",
        "color": "#10B981",
        "default_desc": "30 sparse lexical candidates",
    },
    {
        "id": "b_dense",
        "step": "B.03",
        "title": "BGE Dense Vector",
        "subtitle": "bge-small-en-v1.5 Cosine",
        "color": "#3B82F6",
        "default_desc": "30 dense embedding candidates",
    },
    {
        "id": "b_rerank",
        "step": "B.04",
        "title": "Hybrid Fusion + Rerank",
        "subtitle": "Min-Max Alpha + Cross-Encoder",
        "color": "#EC4899",
        "default_desc": "Weighted fusion + bge-reranker-large",
    },
    {
        "id": "b_generator",
        "step": "B.05",
        "title": "Single-Pass Generator",
        "subtitle": "1x LLM Call ([1],[2] Cites)",
        "color": "#6366F1",
        "default_desc": "Single-pass synthesis (No Critic)",
    },
]

NODE_META_SYS_A = [
    {
        "id": "a_embed",
        "step": "A.01",
        "title": "Query Embedder",
        "subtitle": "Vanilla Dense Encoder",
        "color": "#38BDF8",
        "default_desc": "Encodes raw user question once",
    },
    {
        "id": "a_lookup",
        "step": "A.02",
        "title": "Vector Top-K Lookup",
        "subtitle": "Chroma Cosine Search",
        "color": "#3B82F6",
        "default_desc": "Single-pass top-k vector chunks",
    },
    {
        "id": "a_generate",
        "step": "A.03",
        "title": "Vanilla LLM Prompt",
        "subtitle": "Single-Pass Baseline",
        "color": "#6366F1",
        "default_desc": "Direct prompt answer (Placeholder)",
    },
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


def _fmt_lat(ms: float) -> str:
    """Consistently format millisecond latency across all node badges."""
    if not ms or ms <= 0.0:
        return ""
    if ms < 1.0:
        return "<1ms"
    if ms < 1000.0:
        return f"{ms:.0f}ms"
    return f"{ms / 1000.0:.2f}s"


def _render_node_card(
    meta: Dict[str, str],
    tele_text: str,
    is_active: bool,
    is_visited: bool,
    is_skipped: bool,
    is_system_selected: bool,
) -> str:
    """Render an individual node box for SYS A, SYS B, or SYS C."""
    color = meta["color"]
    if not is_system_selected:
        state_cls = "node-box state-idle"
        inline_style = ""
        badge_html = '<span class="node-status-tag" style="background:rgba(148,163,184,0.1); color:#64748B;">STANDBY</span>'
    elif is_active:
        state_cls = "node-box state-active"
        inline_style = (
            f"border-color: {color}; border-left: 3.5px solid {color}; "
            f"box-shadow: 0 0 16px {color}33;"
        )
        badge_html = (
            f'<span class="node-status-tag" style="background:{color}24; color:{color}; '
            f'border:1px solid {color}; animation: quantActivePulse 1.2s infinite;">EXEC</span>'
        )
    elif is_visited:
        state_cls = "node-box state-completed"
        inline_style = f"border-left: 2.5px solid {color}AA;"
        badge_html = '<span class="node-status-tag" style="background:rgba(16,185,129,0.14); color:#10B981;">DONE</span>'
    elif is_skipped:
        state_cls = "node-box state-skipped"
        inline_style = ""
        badge_html = '<span class="node-status-tag" style="background:rgba(148,163,184,0.12); color:#64748B;">BYPASSED</span>'
    else:
        state_cls = "node-box state-idle"
        inline_style = ""
        badge_html = '<span class="node-status-tag" style="background:rgba(148,163,184,0.1); color:#64748B;">STANDBY</span>'

    return (
        f'<div class="{state_cls}" style="{inline_style}">'
        f'<div class="node-top">'
        f'<span class="node-step-num">[{html.escape(meta["step"])}]</span>'
        f"{badge_html}"
        f"</div>"
        f'<div class="node-name">{html.escape(meta["title"])} <span style="font-size:0.67rem; font-weight:600; opacity:0.72; display:block; font-family:var(--quant-mono);">({html.escape(meta.get("subtitle", ""))})</span></div>'
        f'<div class="node-telemetry">{html.escape(tele_text)}</div>'
        f"</div>"
    )


# ---------------------------------------------------------------------------
# REAL-TIME INTERACTIVE 3-SYSTEM COMPARATIVE STATE GRAPH RENDERER
# ---------------------------------------------------------------------------
def render_visual_state_graph(
    state: Dict[str, Any],
    active_node: Optional[str],
    visited_nodes: List[str],
    elapsed_sec: float = 0.0,
    is_finished: bool = False,
    loop_triggered: bool = False,
    selected_mode: Optional[str] = None,
    sys_b_mode: str = "hybrid_rerank",
    sys_b_alpha: float = 0.50,
    sys_b_top_k: int = 5,
) -> str:
    """
    Build the 3-System Comparative Architecture Topology (`SYS C`, `SYS B`, `SYS A`):
    - Lights up ONLY the currently selected system (`SYS C`, `SYS B`, or `SYS A`) at 100% opacity.
    - Greys out the other two unselected systems (`STANDBY // INACTIVE`) for instant architectural comparison.
    - Strictly isolates the `[C.04] Sufficiency Critic` and multi-hop reflection loop to `SYS C`.
    - Dynamically updates `SYS B`'s 5-node single-pass topology based on `sys_b_mode`, `sys_b_alpha`, and live timings.
    """
    eff_mode = selected_mode or str(state.get("mode", "v2_aamr"))
    if eff_mode.startswith("system_b"):
        active_sys = "B"
    elif eff_mode.startswith("system_a"):
        active_sys = "A"
    else:
        active_sys = "C"

    current_hop = max(1, int(state.get("current_hop", 1) or 1))
    max_hops = int(state.get("max_hops", 3) or 3)
    threshold = float(state.get("sufficiency_threshold", 0.85) or 0.85)
    suff_score = float(state.get("sufficiency_score", 0.0) or 0.0)
    is_sufficient = bool(state.get("is_sufficient", False))
    evidence = state.get("accumulated_evidence", []) or []
    tabular = state.get("tabular_evidence", []) or []
    intermediate = state.get("intermediate_answers", []) or []
    guard_report = state.get("guardrail_report", {}) or {}
    telemetry = state.get("telemetry", {}) or {}
    b_raw = state.get("system_b_raw", {}) or {}

    if b_raw.get("mode"):
        sys_b_mode = str(b_raw["mode"])
    if b_raw.get("alpha") is not None:
        sys_b_alpha = float(b_raw["alpha"])
    if b_raw.get("top_k") is not None:
        sys_b_top_k = int(b_raw["top_k"])

    # Score progression string (e.g. 0.62 ➔ 0.94) for SYS C
    score_history = [f"{float(item.get('sufficiency_score', 0.0)):.2f}" for item in intermediate]
    if score_history and active_sys == "C":
        score_prog_str = " ➔ ".join(score_history)
    elif "critic" in visited_nodes and active_sys == "C":
        score_prog_str = f"{suff_score:.2f}"
    else:
        score_prog_str = "Pending Audit"

    # Determine top banner
    missing_premises = state.get("missing_premises", []) or []
    if active_sys == "C":
        if loop_triggered or active_node == "generator":
            gap_preview = html.escape(str(missing_premises[0])[:56]) if missing_premises else "Targeted Follow-Up Sub-Query"
            hop_banner_cls = "hop-banner hop-banner-active"
            hop_banner_txt = f"[SYS C HOP {min(current_hop + (1 if active_node == 'generator' else 0), max_hops)} / {max_hops}: Resolving Missing Premises — {gap_preview}]"
        elif is_finished:
            early_stop = is_sufficient and current_hop < max_hops
            hop_banner_cls = "hop-banner hop-banner-complete"
            if early_stop:
                hop_banner_txt = f"[SYS C EARLY STOP AT HOP {current_hop} / {max_hops} — Critic Score {suff_score:.2f} >= {threshold:.2f}]"
            else:
                hop_banner_txt = f"[SYS C COMPLETE — {current_hop} / {max_hops} Hops | Latency {elapsed_sec:.2f}s]"
        elif active_node:
            hop_banner_cls = "hop-banner hop-banner-normal"
            hop_banner_txt = f"[SYS C HOP {current_hop} / {max_hops}: Executing `{active_node.upper()}`]"
        else:
            hop_banner_cls = "hop-banner hop-banner-normal"
            hop_banner_txt = f"[SYS C SELECTED — Max {max_hops} Hops | Critic Threshold >= {threshold:.2f}]"
    elif active_sys == "B":
        if is_finished:
            hop_banner_cls = "hop-banner hop-banner-complete"
            hop_banner_txt = f"[SYS B COMPLETE — Mode: {sys_b_mode.upper()} | Top-{len(evidence) or sys_b_top_k} Chunks | {elapsed_sec:.2f}s]"
        elif active_node:
            hop_banner_cls = "hop-banner hop-banner-active"
            hop_banner_txt = f"[SYS B EXECUTING — Single-Pass `{sys_b_mode.upper()}` (Alpha={sys_b_alpha:.2f})]"
        else:
            hop_banner_cls = "hop-banner hop-banner-normal"
            hop_banner_txt = f"[SYS B SELECTED — Mode: {sys_b_mode.upper()} | Alpha={sys_b_alpha:.2f} | Top-{sys_b_top_k} (No Critic Loop)]"
    else:
        if is_finished:
            hop_banner_cls = "hop-banner hop-banner-complete"
            hop_banner_txt = f"[SYS A COMPLETE — Single-Pass Dense Baseline | {elapsed_sec:.2f}s]"
        else:
            hop_banner_cls = "hop-banner hop-banner-normal"
            hop_banner_txt = "[SYS A SELECTED — Vanilla Single-Pass Dense RAG (Baseline Placeholder)]"

    sub_queries = state.get("sub_queries", []) or []
    tickers = state.get("target_tickers", []) or ([state.get("target_ticker")] if state.get("target_ticker") else [])
    citations = state.get("citations", []) or []
    verified_nums = guard_report.get("verified_numbers", []) or []
    ungrounded_nums = guard_report.get("ungrounded_numbers", []) or []
    repair_count = int(state.get("repair_count", 0) or 0)

    # -----------------------------------------------------------------------
    # 1. BUILD SYS C TIER (6 NODES + CRITIC NODE + CONDITIONAL REFLECTION LOOP)
    # -----------------------------------------------------------------------
    is_c_selected = active_sys == "C"
    c_visited = visited_nodes if is_c_selected else []
    c_active = active_node if is_c_selected else None
    c_v1_text_only = eff_mode in ("adaptive_v1", "fixed_1hop", "fixed_3hop", "v1_amr")
    c_latencies = telemetry.get("node_latencies_ms", {}) or {}

    dec_lat = _fmt_lat(float(c_latencies.get("decomposer", 0.0))) if (is_c_selected and "decomposer" in c_visited) else ""
    tab_lat = _fmt_lat(float(c_latencies.get("tabular_tool", 0.0))) if (is_c_selected and "tabular_tool" in c_visited) else ""
    ret_lat = _fmt_lat(float(c_latencies.get("retriever", 0.0))) if (is_c_selected and "retriever" in c_visited) else ""
    cri_lat = _fmt_lat(float(c_latencies.get("critic", 0.0))) if (is_c_selected and "critic" in c_visited) else ""
    syn_lat = _fmt_lat(float(c_latencies.get("synthesizer", 0.0))) if (is_c_selected and "synthesizer" in c_visited) else ""
    grd_lat = _fmt_lat(float(c_latencies.get("guardrail", 0.0))) if (is_c_selected and "guardrail" in c_visited) else ""

    node_tele_c = {
        "decomposer": (
            f"Tickers: {', '.join(tickers) if tickers else 'Auto'} | {len(sub_queries)} Sub-Q(s)" + (f" ({dec_lat})" if dec_lat else "")
            if "decomposer" in c_visited
            else "Ticker & Sub-Query Plan"
        ),
        "tabular_tool": (
            f"{len(tabular)} XBRL Table(s)" + (f" ({tab_lat})" if tab_lat else "")
            if "tabular_tool" in c_visited
            else ("Bypassed (Text Mode)" if c_v1_text_only else ("Bypassed (Text Route)" if ("retriever" in c_visited and "tabular_tool" not in c_visited) else "Deterministic SQL/XBRL"))
        ),
        "retriever": (
            f"{len(evidence)} Chunks (Hop {current_hop}/{max_hops})" + (f" ({ret_lat})" if ret_lat else "")
            if "retriever" in c_visited
            else f"Multi-Hop Search (Max {max_hops})"
        ),
        "critic": (
            f"Score: {suff_score:.2f} ({'PASS' if is_sufficient else 'LOOP'})" + (f" ({cri_lat})" if cri_lat else "")
            if "critic" in c_visited
            else f"Self-RAG Critic >= {threshold:.2f}"
        ),
        "synthesizer": (
            f"{len(citations)} Citations Mapped" + (f" ({syn_lat})" if syn_lat else "")
            if "synthesizer" in c_visited
            else "Inline Citation Mapper"
        ),
        "guardrail": (
            f"{len(verified_nums)} Verified | {len(ungrounded_nums)} Flagged" + (f" ({grd_lat})" if grd_lat else "")
            if "guardrail" in c_visited
            else "Scale Verifier + Self-Heal"
        ),
    }

    c_cards: List[str] = []
    for meta in NODE_META:
        nid = meta["id"]
        is_act = is_c_selected and (
            (c_active == nid)
            or (nid == "retriever" and c_active == "generator")
            or (nid == "guardrail" and c_active == "repair")
        )
        is_vis = is_c_selected and (nid in c_visited)
        is_skp = is_c_selected and (
            (nid == "tabular_tool" and c_v1_text_only)
            or (nid == "tabular_tool" and ("retriever" in c_visited) and ("tabular_tool" not in c_visited))
        )
        c_cards.append(_render_node_card(meta, node_tele_c.get(nid, meta["default_desc"]), is_act, is_vis, is_skp, is_c_selected))

    is_loop_live = is_c_selected and (loop_triggered or c_active == "generator")
    loop_stroke = "#F59E0B" if is_loop_live else ("#10B981" if (is_c_selected and is_finished and current_hop > 1) else "#64748B")
    if is_loop_live:
        loop_label = f"SYS C REFLECTION LOOP ACTIVE — Critic Score {suff_score:.2f} < {threshold:.2f} ➔ Formulating Hop {current_hop} Follow-Up Sub-Query"
    elif is_c_selected and current_hop > 1 and is_finished:
        loop_label = f"SYS C Multi-Hop Reflection Trace Executed ({current_hop} Hops Total — Sufficiency {score_prog_str})"
    else:
        loop_label = f"SYS C Exclusive Reflection Loop: [C.04 Sufficiency Critic] (< {threshold:.2f}) ➔ Sub-Query Generator ➔ [C.03 Retriever]"

    c_loop_bar = (
        f'<div class="loop-trace-bar" style="border-color:{loop_stroke}55;">'
        f'<div style="font-family:var(--quant-mono); font-size:0.71rem; color:{loop_stroke}; font-weight:700;">'
        f"{html.escape(loop_label)}"
        f"</div>"
        f'<div style="display:flex; align-items:center; gap:6px; font-family:var(--quant-mono); font-size:0.67rem; font-weight:800; flex-shrink:0;">'
        f'<span style="color:#F59E0B; background:rgba(245,158,11,0.15); padding:2px 6px; border-radius:3px; border:1px solid rgba(245,158,11,0.4);">[C.04 CRITIC]</span>'
        f'<span style="color:{loop_stroke};">➔</span>'
        f'<span style="color:#06B6D4; background:rgba(6,182,212,0.15); padding:2px 6px; border-radius:3px; border:1px solid rgba(6,182,212,0.4);">[SUB-QUERY GEN]</span>'
        f'<span style="color:{loop_stroke};">➔</span>'
        f'<span style="color:#3B82F6; background:rgba(59,130,246,0.15); padding:2px 6px; border-radius:3px; border:1px solid rgba(59,130,246,0.4);">[C.03 RETRIEVER]</span>'
        f"</div>"
        f"</div>"
    )

    c_tier_cls = "sys-tier-card sys-tier-active" if is_c_selected else "sys-tier-card sys-tier-inactive"
    c_status_pill = (
        '<span class="metric-badge badge-amber">ACTIVE ARCHITECTURE</span>'
        if is_c_selected
        else '<span class="metric-badge">STANDBY</span>'
    )
    sys_c_block = (
        f'<div class="{c_tier_cls}">'
        f'<div class="sys-tier-header">'
        f'<div class="sys-tier-title" style="color:{"#F59E0B" if is_c_selected else "var(--term-text-muted)"};">'
        f'SYS C // ADAPTIVE MULTI-HOP STATE MACHINE (LANGGRAPH + CRITIC LOOP + XBRL + GUARDRAIL)'
        f"</div>"
        f"{c_status_pill}"
        f"</div>"
        f'<div class="nodes-grid">{"".join(c_cards)}</div>'
        f"{c_loop_bar}"
        f"</div>"
    )

    # -----------------------------------------------------------------------
    # 2. BUILD SYS B TIER (5 NODES, DYNAMIC SUB-MODE, NO CRITIC NODE)
    # -----------------------------------------------------------------------
    is_b_selected = active_sys == "B"
    b_visited = visited_nodes if is_b_selected else []
    b_active = active_node if is_b_selected else None
    b_timings = b_raw.get("timings", {}) or {}
    b_chunks_total = int(b_raw.get("corpus_chunks", 0) or 0)
    b_hits_list = b_raw.get("hits", []) or []

    b_bm25_skipped = sys_b_mode == "dense"
    b_dense_skipped = sys_b_mode == "bm25"
    b_rerank_skipped = sys_b_mode in ("bm25", "dense")

    b_bm25_lat = _fmt_lat(float(b_timings.get("bm25_seconds", 0.0)) * 1000.0) if (is_b_selected and is_finished) else ""
    b_dense_lat = _fmt_lat(float(b_timings.get("dense_seconds", 0.0)) * 1000.0) if (is_b_selected and is_finished) else ""
    b_rerank_lat = _fmt_lat(float(b_timings.get("rerank_seconds", 0.0)) * 1000.0) if (is_b_selected and is_finished) else ""
    b_gen_lat = _fmt_lat(float(b_timings.get("generation_seconds", 0.0)) * 1000.0) if (is_b_selected and is_finished) else ""

    node_tele_b = {
        "b_scope": (
            f"Tickers: {', '.join(tickers) if tickers else 'Auto'} | {b_chunks_total:,} Chunks"
            if (is_b_selected and is_finished and b_chunks_total > 0)
            else "Ticker & Year Scope Filter"
        ),
        "b_bm25": (
            "Bypassed (Dense-Only)"
            if b_bm25_skipped
            else (
                f"30 Candidates" + (f" ({b_bm25_lat})" if b_bm25_lat else "")
                if (is_b_selected and is_finished)
                else "Okapi BM25 (30 Candidates)"
            )
        ),
        "b_dense": (
            "Bypassed (BM25-Only)"
            if b_dense_skipped
            else (
                f"30 Candidates" + (f" ({b_dense_lat})" if b_dense_lat else "")
                if (is_b_selected and is_finished)
                else "BGE Dense Cosine (30 Cand)"
            )
        ),
        "b_rerank": (
            f"Bypassed ({sys_b_mode.upper()})"
            if b_rerank_skipped
            else (
                f"Alpha={sys_b_alpha:.2f}" + (f" + Rerank ({b_rerank_lat})" if sys_b_mode == "hybrid_rerank" and b_rerank_lat else "")
                if (is_b_selected and is_finished)
                else f"Alpha={sys_b_alpha:.2f} + Cross-Encoder Top-{sys_b_top_k}"
            )
        ),
        "b_generator": (
            f"Top-{len(b_hits_list)} Context" + (f" ({b_gen_lat})" if b_gen_lat else "")
            if (is_b_selected and is_finished)
            else f"Single LLM Call (Top-{sys_b_top_k} Chunks)"
        ),
    }

    b_cards: List[str] = []
    for meta in NODE_META_SYS_B:
        nid = meta["id"]
        is_skp = (
            (nid == "b_bm25" and b_bm25_skipped)
            or (nid == "b_dense" and b_dense_skipped)
            or (nid == "b_rerank" and b_rerank_skipped)
        )
        is_act = is_b_selected and not is_skp and (
            (b_active == nid)
            or (b_active == "retriever" and nid in ("b_scope", "b_bm25", "b_dense", "b_rerank"))
            or (b_active == "synthesizer" and nid == "b_generator")
        )
        is_vis = is_b_selected and not is_skp and (
            (nid in b_visited)
            or (is_finished)
            or ("retriever" in b_visited and nid in ("b_scope", "b_bm25", "b_dense", "b_rerank"))
            or ("synthesizer" in b_visited and nid == "b_generator")
        )
        b_cards.append(_render_node_card(meta, node_tele_b.get(nid, meta["default_desc"]), is_act, is_vis, is_skp, is_b_selected))

    b_bar_col = "#38BDF8" if is_b_selected else "#64748B"
    b_flow_bar = (
        f'<div class="loop-trace-bar" style="border-color:{b_bar_col}55;">'
        f'<div style="font-family:var(--quant-mono); font-size:0.71rem; color:{b_bar_col}; font-weight:700;">'
        f"SYS B SINGLE-PASS PIPELINE (Mode: {html.escape(sys_b_mode.upper())} | Alpha={sys_b_alpha:.2f}) — Single-Pass Retrieval &amp; Generation (No Reflection Loop)"
        f"</div>"
        f'<div style="display:flex; align-items:center; gap:6px; font-family:var(--quant-mono); font-size:0.67rem; font-weight:800; flex-shrink:0;">'
        f'<span style="color:#10B981; background:rgba(16,185,129,0.14); padding:2px 6px; border-radius:3px;">[B.02 BM25]</span>'
        f'<span style="color:{b_bar_col};">+</span>'
        f'<span style="color:#3B82F6; background:rgba(59,130,246,0.14); padding:2px 6px; border-radius:3px;">[B.03 DENSE]</span>'
        f'<span style="color:{b_bar_col};">➔</span>'
        f'<span style="color:#EC4899; background:rgba(236,72,153,0.14); padding:2px 6px; border-radius:3px;">[B.04 FUSION/RERANK]</span>'
        f'<span style="color:{b_bar_col};">➔</span>'
        f'<span style="color:#6366F1; background:rgba(99,102,241,0.14); padding:2px 6px; border-radius:3px;">[B.05 GENERATE]</span>'
        f"</div>"
        f"</div>"
    )

    b_tier_cls = "sys-tier-card sys-tier-active" if is_b_selected else "sys-tier-card sys-tier-inactive"
    b_status_pill = (
        f'<span class="metric-badge badge-cyan">ACTIVE ARCHITECTURE ({html.escape(sys_b_mode.upper())})</span>'
        if is_b_selected
        else '<span class="metric-badge">STANDBY</span>'
    )
    sys_b_block = (
        f'<div class="{b_tier_cls}" style="{"border-left-color:#06B6D4;" if is_b_selected else ""}">'
        f'<div class="sys-tier-header">'
        f'<div class="sys-tier-title" style="color:{"#06B6D4" if is_b_selected else "var(--term-text-muted)"};">'
        f'SYS B // SINGLE-PASS HYBRID + CROSS-ENCODER RERANK RAG (NO CRITIC NODE)'
        f"</div>"
        f"{b_status_pill}"
        f"</div>"
        f'<div class="nodes-grid-5">{"".join(b_cards)}</div>'
        f"{b_flow_bar}"
        f"</div>"
    )

    # -----------------------------------------------------------------------
    # 3. BUILD SYS A TIER (3 NODES — VANILLA DENSE PLACEHOLDER, NO CRITIC)
    # -----------------------------------------------------------------------
    is_a_selected = active_sys == "A"
    a_lat = _fmt_lat(elapsed_sec * 1000.0) if (is_a_selected and is_finished) else ""
    node_tele_a = {
        "a_embed": "Query Vector Embedded" if (is_a_selected and is_finished) else "Query Embedding (bge-small-en-v1.5)",
        "a_lookup": "Top-4 Chunks Retrieved" if (is_a_selected and is_finished) else "Single-Pass Dense Cosine Search (Top-4)",
        "a_generate": f"Generated Synthesis" + (f" ({a_lat})" if a_lat else "") if (is_a_selected and is_finished) else "Direct Prompt Generation (Single Call)",
    }
    a_cards: List[str] = []
    for meta in NODE_META_SYS_A:
        nid = meta["id"]
        is_act = is_a_selected and (active_node == nid)
        is_vis = is_a_selected and (nid in visited_nodes or is_finished)
        a_cards.append(_render_node_card(meta, node_tele_a.get(nid, meta["default_desc"]), is_act, is_vis, False, is_a_selected))

    a_tier_cls = "sys-tier-card sys-tier-active" if is_a_selected else "sys-tier-card sys-tier-inactive"
    a_status_pill = (
        '<span class="metric-badge badge-blue">ACTIVE ARCHITECTURE (PLACEHOLDER)</span>'
        if is_a_selected
        else '<span class="metric-badge">STANDBY</span>'
    )
    sys_a_block = (
        f'<div class="{a_tier_cls}" style="{"border-left-color:#3B82F6;" if is_a_selected else ""}">'
        f'<div class="sys-tier-header">'
        f'<div class="sys-tier-title" style="color:{"#3B82F6" if is_a_selected else "var(--term-text-muted)"};">'
        f'SYS A // VANILLA SINGLE-PASS DENSE RAG (BASELINE PLACEHOLDER — NO BM25 / NO RERANK / NO CRITIC)'
        f"</div>"
        f"{a_status_pill}"
        f"</div>"
        f'<div class="nodes-grid-3">{"".join(a_cards)}</div>'
        f"</div>"
    )

    # Consolidated 5-Column Institutional Telemetry Ribbon
    if active_sys == "C":
        filled_blocks = min(current_hop, max_hops) if (visited_nodes or active_node) else 0
        empty_blocks = max(0, max_hops - filled_blocks)
        hop_blocks_str = "[" + ("■" * filled_blocks) + ("□" * empty_blocks) + "]"
        early_stop_flag = is_finished and is_sufficient and current_hop < max_hops
        hop_status_tag = "EARLY STOP" if early_stop_flag else ("COMPLETE" if is_finished else ("ACTIVE" if active_node else "READY"))
        hop_col = "#10B981" if early_stop_flag else ("#F59E0B" if is_loop_live else "var(--term-text-primary)")
        col1_label = "SYS C Hop Execution"
        col1_val = f'{current_hop} / {max_hops} <span style="font-size:0.72rem;">{html.escape(hop_blocks_str)} {hop_status_tag}</span>'

        suff_pct = int(round(min(max(suff_score, 0.0), 1.0) * 100))
        suff_bar_color = "#10B981" if suff_score >= threshold else ("#F59E0B" if suff_score > 0 else "#64748B")
        col2_label = "Critic Sufficiency (SYS C Only)"
        col2_val = f'{html.escape(score_prog_str)} <span style="font-size:0.70rem; opacity:0.75;">(≥{threshold:.2f})</span>'
    elif active_sys == "B":
        hop_col = "#06B6D4"
        col1_label = "SYS B Execution Pass"
        col1_val = f'1 / 1 <span style="font-size:0.72rem;">[■] SINGLE-PASS ({html.escape(sys_b_mode.upper())})</span>'
        suff_pct = int(round(sys_b_alpha * 100))
        suff_bar_color = "#06B6D4"
        col2_label = "SYS B Hybrid Fusion Alpha"
        col2_val = f'Alpha = {sys_b_alpha:.2f} <span style="font-size:0.70rem; opacity:0.75;">(No Critic Node)</span>'
    else:
        hop_col = "#3B82F6"
        col1_label = "SYS A Baseline Pass"
        col1_val = '1 / 1 <span style="font-size:0.72rem;">[■] VANILLA SINGLE-PASS</span>'
        suff_pct = 0
        suff_bar_color = "#64748B"
        col2_label = "Critic / Reranker"
        col2_val = 'None <span style="font-size:0.70rem; opacity:0.75;">(Baseline Placeholder)</span>'

    total_ver = len(verified_nums)
    total_ungr = len(ungrounded_nums)
    faith_score = float(guard_report.get("faithfulness_score", 1.0 if "guardrail" in visited_nodes else 0.0))
    faith_pct = int(round(faith_score * 100)) if ("guardrail" in visited_nodes or is_finished) else 0
    faith_color = "#10B981" if (total_ungr == 0 and ("guardrail" in visited_nodes or is_finished)) else ("#F43F5E" if total_ungr > 0 else "#64748B")

    total_tokens = int(telemetry.get("total_tokens", 0) or 0)
    est_cost = float(telemetry.get("estimated_cost_usd", 0.0) or 0.0)

    gauges_html = (
        f'<div class="telemetry-strip">'
        f'<div class="gauge-card">'
        f'<div class="gauge-label">{html.escape(col1_label)}</div>'
        f'<div class="gauge-val" style="color:{hop_col};">{col1_val}</div>'
        f"</div>"
        f'<div class="gauge-card">'
        f'<div class="gauge-label">{html.escape(col2_label)}</div>'
        f'<div class="gauge-val" style="color:{suff_bar_color};">{col2_val}</div>'
        f'<div class="gauge-bar-track"><div class="gauge-bar-fill" style="width:{suff_pct}%; background:{suff_bar_color};"></div></div>'
        f"</div>"
        f'<div class="gauge-card">'
        f'<div class="gauge-label">Retrieved Corpus (RQ1)</div>'
        f'<div class="gauge-val">{len(evidence)} Chunks <span style="font-size:0.74rem; color:#10B981;">| {len(tabular)} XBRL</span></div>'
        f"</div>"
        f'<div class="gauge-card">'
        f'<div class="gauge-label">Numerical Grounding (RQ2)</div>'
        f'<div class="gauge-val" style="color:{faith_color};">{total_ver} Verified / {total_ungr} Flagged</div>'
        f'<div class="gauge-bar-track"><div class="gauge-bar-fill" style="width:{faith_pct}%; background:{faith_color};"></div></div>'
        f"</div>"
        f'<div class="gauge-card">'
        f'<div class="gauge-label">Latency &amp; Economics (RQ3)</div>'
        f'<div class="gauge-val">{elapsed_sec:.2f}s <span style="font-size:0.72rem; opacity:0.8;">| {total_tokens:,} tok (${est_cost:.5f})</span></div>'
        f"</div>"
        f"</div>"
    )

    return (
        f'<div class="pipeline-shell">'
        f'<div class="pipeline-header-bar">'
        f'<div class="pipeline-title">3-SYSTEM COMPARATIVE ARCHITECTURE TOPOLOGY (ACTIVE: SYS {active_sys} // STANDBY: OTHERS)</div>'
        f'<div class="{hop_banner_cls}">{hop_banner_txt}</div>'
        f"</div>"
        f"{sys_c_block}"
        f"{sys_b_block}"
        f"{sys_a_block}"
        f"{gauges_html}"
        f"</div>"
    )


# ---------------------------------------------------------------------------
# HELPER: NUMERICAL GROUNDING PILL ATTRIBUTION & DOSSIER FORMATTING
# ---------------------------------------------------------------------------
def match_number_to_source_badge(
    num_token: str,
    citations: List[Dict[str, Any]],
    evidence_chunks: List[Dict[str, Any]],
    default_ticker: Optional[str] = None,
) -> Tuple[str, str]:
    """
    Find the best matching SEC 10-K source tag and tooltip excerpt for a verified number token.
    Returns (short_badge_label, tooltip_excerpt).
    """
    clean_tok = num_token.rstrip("%").replace(",", "")

    # 1. Check structured citations first
    for cit in citations:
        claim = str(cit.get("supported_claim", ""))
        if num_token in claim or clean_tok in claim.replace(",", ""):
            tkr = cit.get("ticker") or default_ticker or "SEC"
            fy = cit.get("fiscal_year") or ""
            sec = str(cit.get("section") or "10-K")
            short_sec = sec[:14] + ".." if len(sec) > 16 else sec
            fy_str = f" FY{str(fy)[-2:]}" if fy else ""
            label = f"{tkr}{fy_str} {short_sec}".strip()
            tooltip = f"Source Chunk: {cit.get('chunk_id', 'N/A')} | Claim: {claim[:160]}"
            return label, tooltip

    # 2. Check evidence chunks directly
    for ch in evidence_chunks:
        content = str(ch.get("content", ""))
        if num_token in content or clean_tok in content.replace(",", ""):
            meta = ch.get("metadata", {}) or {}
            cid = str(ch.get("chunk_id", ""))
            tkr = meta.get("ticker") or default_ticker or (cid.split("_")[0] if "_" in cid else "SEC")
            fy = meta.get("fiscal_year") or ""
            sec = str(meta.get("section") or ("XBRL Table" if cid.startswith("F-") else "10-K"))
            short_sec = sec[:14] + ".." if len(sec) > 16 else sec
            fy_str = f" FY{str(fy)[-2:]}" if fy else ""
            label = f"{tkr}{fy_str} {short_sec}".strip()
            tooltip = f"Chunk {cid} (Hop {ch.get('hop_retrieved', 1)}): {content[:160].replace(chr(10), ' ')}"
            return label, tooltip

    fallback_label = f"{default_ticker} 10-K Verified" if default_ticker else "SEC 10-K Verified"
    return fallback_label, "Scale-normalized match verified against retrieved SEC 10-K filing corpus."


def render_grounding_pills_html(
    verified_numbers: List[str],
    ungrounded_numbers: List[str],
    citations: List[Dict[str, Any]],
    evidence_chunks: List[Dict[str, Any]],
    default_ticker: Optional[str] = None,
) -> Tuple[str, str]:
    """Return HTML strings for (verified_pills_html, ungrounded_pills_html)."""
    if verified_numbers:
        v_pills: List[str] = []
        seen_v = set()
        for num in verified_numbers:
            if num in seen_v:
                continue
            seen_v.add(num)
            src_label, tooltip = match_number_to_source_badge(num, citations, evidence_chunks, default_ticker)
            v_pills.append(
                f'<span class="grounding-pill pill-verified" title="{html.escape(tooltip)}">'
                f"<span>✓ {html.escape(str(num))}</span>"
                f'<span class="pill-source">[{html.escape(src_label)}]</span>'
                f"</span>"
            )
        verified_html = f'<div class="pills-wrap">{"".join(v_pills)}</div>'
    else:
        verified_html = (
            '<div class="pills-wrap">'
            '<span class="grounding-pill pill-verified" title="Qualitative response or no numerical claims required verification.">'
            "<span>✓ Qualitative Synthesis (0 Unverified Figures)</span>"
            "</span></div>"
        )

    if ungrounded_numbers:
        u_pills: List[str] = []
        seen_u = set()
        for num in ungrounded_numbers:
            if num in seen_u:
                continue
            seen_u.add(num)
            tooltip = (
                f"Flagged by Active Guardrail: '{num}' could not be exact-matched or scale-normalized "
                f"against retrieved SEC 10-K chunks or XBRL tables."
            )
            u_pills.append(
                f'<span class="grounding-pill pill-ungrounded" title="{html.escape(tooltip)}">'
                f"<span>⚠</span>"
                f'<span class="strike-num">{html.escape(str(num))}</span>'
                f'<span class="pill-flag-tag">UNGROUNDED</span>'
                f"</span>"
            )
        ungrounded_html = f'<div class="pills-wrap">{"".join(u_pills)}</div>'
    else:
        ungrounded_html = (
            '<div class="pills-wrap">'
            '<span class="grounding-pill pill-verified" title="Every extracted numerical claim matched SEC ground-truth context.">'
            "<span>0 Hallucinated Figures — 100% Grounded</span>"
            "</span></div>"
        )

    return verified_html, ungrounded_html


def format_executive_synthesis_md(raw_answer: str) -> str:
    """
    Sanitize `$` signs before digits so Streamlit KaTeX does not turn financial prose into math mode,
    and style inline bracketed citations (`[NVDA ...]` or `[F-NVDA-2026]`) as compact `.citation-chip` badges.
    """
    safe_md = re.sub(r"\$(\d)", r"\\$\1", raw_answer)

    def _replace_citation(match: re.Match) -> str:
        inner = match.group(1)
        # Only style SEC/XBRL citations, not markdown links
        if any(k in inner for k in ("FY", "Item", "Note", "Chunk", "F-", "10-K", "202", "199")):
            return f'<span class="citation-chip">[{html.escape(inner)}]</span>'
        return match.group(0)

    return re.sub(r"\[([^\[\]]{3,80})\](?!\()", _replace_citation, safe_md)


def render_multihop_timeline_html(state: Dict[str, Any]) -> str:
    """Render Tab 3's vertical Institutional Quant audit timeline from `intermediate_answers` and `state`."""
    intermediate = state.get("intermediate_answers", []) or []
    evidence = state.get("accumulated_evidence", []) or []
    tabular = state.get("tabular_evidence", []) or []
    sub_queries = state.get("sub_queries", []) or []
    tickers = state.get("target_tickers", []) or ([state.get("target_ticker")] if state.get("target_ticker") else [])
    years = state.get("fiscal_years", []) or []
    threshold = float(state.get("sufficiency_threshold", 0.85) or 0.85)
    max_hops = int(state.get("max_hops", 3) or 3)
    curr_hop = int(state.get("current_hop", len(intermediate) or 1))
    is_early_stopped = bool(
        state.get("early_stopped")
        or state.get("telemetry", {}).get("early_stopped")
        or (state.get("is_sufficient") and curr_hop < max_hops)
    )

    blocks: List[str] = []

    # Executive "Why N Hops?" TL;DR Callout Card
    if curr_hop > 1 and intermediate:
        hop1_gaps = intermediate[0].get("missing_premises", []) or []
        gap_summary = html.escape(str(hop1_gaps[0])[:75]) if hop1_gaps else "additional disclosures required to complete premises"
        early_stop_txt = (
            f"<strong style='color:#10B981;'>Early Stopping Triggered</strong> — saved {max_hops - curr_hop} redundant retrieval hop(s) and compute budget."
            if is_early_stopped
            else f"Executed all {curr_hop} planned sequential hops."
        )
        blocks.append(
            f'<div class="timeline-card" style="border-left: 3.5px solid var(--quant-amber); background: rgba(245, 158, 11, 0.08); margin-bottom:12px;">'
            f'<div style="font-family:var(--quant-mono); font-weight:800; font-size:0.80rem; color:var(--quant-amber); margin-bottom:3px;">'
            f'EXECUTIVE TL;DR: WHY SYSTEM C EXECUTED {curr_hop} SEQUENTIAL HOPS'
            f'</div>'
            f'<div style="font-size:0.83rem; line-height:1.45;">'
            f'&bull; <strong>Hop 01 Audit:</strong> Sufficiency scored <code>{float(intermediate[0].get("sufficiency_score", 0.0)):.2f} &lt; {threshold:.2f}</code> because <em>{gap_summary}</em> was missing from initial retrieved chunks.<br/>'
            f'&bull; <strong>Adaptive Reflection:</strong> Generator formulated a laser-focused follow-up sub-query for Hop 02. Final sufficiency reached <code>{float(state.get("sufficiency_score", 0.0)):.2f} &ge; {threshold:.2f}</code> &bull; {early_stop_txt}'
            f'</div></div>'
        )
    else:
        blocks.append(
            f'<div class="timeline-card" style="border-left: 3.5px solid #10B981; background: rgba(16, 185, 129, 0.08); margin-bottom:12px;">'
            f'<div style="font-family:var(--quant-mono); font-weight:800; font-size:0.80rem; color:#10B981; margin-bottom:2px;">'
            f'EXECUTIVE TL;DR: DIRECT SINGLE-HOP RESOLUTION'
            f'</div>'
            f'<div style="font-size:0.83rem; line-height:1.45;">'
            f'All requested financial metrics and line-item premises were completely satisfied in Hop 01 (Sufficiency: <code>{float(state.get("sufficiency_score", 0.0)):.2f} &ge; {threshold:.2f}</code>). Zero extra retrieval hops needed.'
            f'</div></div>'
        )

    # Stage 0: Planner & Router Card
    tkr_str = ", ".join(tickers) if tickers else "Auto-Detected"
    yr_str = ", ".join(str(y) for y in years) if years else "All Relevant Years"
    tab_badge = (
        f'<span class="metric-badge badge-emerald">XBRL Router Active ({len(tabular)} tables)</span>'
        if tabular
        else '<span class="metric-badge badge-blue">10-K Text Hybrid Route</span>'
    )
    planned_list = "".join(
        f'<li style="margin-bottom:3px; font-family:var(--quant-mono); font-size:0.78rem;">{html.escape(str(sq))}</li>'
        for sq in sub_queries
    )
    blocks.append(
        f'<div class="timeline-card" style="border-left: 3px solid #06B6D4;">'
        f'<div class="timeline-dot" style="background:#06B6D4;"></div>'
        f'<div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:8px; margin-bottom:8px;">'
        f'<div style="font-family:var(--quant-mono); font-weight:800; font-size:0.86rem; color:#06B6D4;">STAGE 00 // QUERY DECOMPOSITION &amp; TOOL ROUTING</div>'
        f"{tab_badge}"
        f"</div>"
        f'<div style="font-size:0.82rem; margin-bottom:8px;">'
        f"<strong>Target Entities:</strong> <code>{html.escape(tkr_str)}</code> &nbsp;|&nbsp; "
        f"<strong>Fiscal Years:</strong> <code>{html.escape(yr_str)}</code> &nbsp;|&nbsp; "
        f"<strong>Complexity:</strong> <code>{html.escape(str(state.get('query_complexity', 'multi_hop')))}</code>"
        f"</div>"
        f'<div style="font-family:var(--quant-mono); font-size:0.72rem; font-weight:700; text-transform:uppercase; opacity:0.8; margin-bottom:4px;">Planned Atomic Sub-Queries:</div>'
        f'<ul style="margin:0; padding-left:18px;">{planned_list}</ul>'
        f"</div>"
    )

    # Hop Cards
    for idx, item in enumerate(intermediate):
        hop_num = int(item.get("hop", idx + 1))
        sub_q = str(item.get("sub_query_executed", ""))
        score = float(item.get("sufficiency_score", 0.0) or 0.0)
        is_suff = bool(item.get("is_sufficient", False))
        reasoning = str(item.get("critic_reasoning", ""))
        missing_p = item.get("missing_premises", []) or []
        missing_e = item.get("missing_entities", []) or []
        redundant_prev = bool(item.get("redundant_search_prevented", False))

        hop_chunks = [c for c in evidence if int(c.get("hop_retrieved", 1)) == hop_num]
        chunk_tags = "".join(
            f'<span class="citation-chip" style="margin-right:5px; margin-bottom:4px;">{html.escape(str(c.get("chunk_id", "")))}</span>'
            for c in hop_chunks[:8]
        )
        if len(hop_chunks) > 8:
            chunk_tags += f'<span class="citation-chip">+{len(hop_chunks) - 8} more</span>'

        border_col = "#10B981" if is_suff else "#F59E0B"
        status_badge = (
            f'<span class="metric-badge badge-emerald">✓ SUFFICIENT (Score {score:.2f} ≥ {threshold:.2f})</span>'
            if is_suff
            else f'<span class="metric-badge badge-amber">⚠ INSUFFICIENT (Score {score:.2f} &lt; {threshold:.2f})</span>'
        )

        gaps_html = ""
        if missing_p or missing_e:
            all_gaps = list(dict.fromkeys([*(str(x) for x in missing_e), *(str(x) for x in missing_p)]))
            gap_chips = "".join(
                f'<span class="metric-badge badge-amber" style="margin-right:6px; margin-bottom:4px; text-transform:none;">Missing: {html.escape(g)}</span>'
                for g in all_gaps
            )
            gaps_html = f'<div style="margin-top:8px;">{gap_chips}</div>'

        redundant_html = (
            '<div style="margin-top:6px; font-family:var(--quant-mono); font-size:0.74rem; color:#06B6D4; font-weight:700;">[Saturation Guard: Prevented duplicate retrieval loop]</div>'
            if redundant_prev
            else ""
        )

        blocks.append(
            f'<div class="timeline-card" style="border-left: 3px solid {border_col};">'
            f'<div class="timeline-dot" style="background:{border_col};"></div>'
            f'<div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:8px; margin-bottom:8px;">'
            f'<div style="font-family:var(--quant-mono); font-weight:800; font-size:0.88rem; color:{border_col};">HOP 0{hop_num} / 0{max_hops} // RETRIEVAL &amp; SUFFICIENCY AUDIT</div>'
            f"{status_badge}"
            f"</div>"
            f'<div style="font-size:0.83rem; margin-bottom:8px;">'
            f"<strong>Executed Sub-Query:</strong> <code>{html.escape(sub_q)}</code>"
            f"</div>"
            f'<div style="font-size:0.81rem; margin-bottom:8px;">'
            f"<strong>Chunks Retrieved in Hop {hop_num} ({len(hop_chunks)}):</strong> "
            f'{chunk_tags if chunk_tags else "<em>Cached / Tabular Context</em>"}'
            f"</div>"
            f'<div style="font-size:0.83rem; padding:8px 12px; border-radius:4px; background:var(--term-bg-elevated); border-left:3px solid {border_col};">'
            f"<strong>Critic Audit Verdict:</strong> {html.escape(reasoning)}"
            f"</div>"
            f"{gaps_html}"
            f"{redundant_html}"
            f"</div>"
        )

        if idx + 1 < len(intermediate):
            next_sub_q = str(intermediate[idx + 1].get("sub_query_executed", ""))
            blocks.append(
                f'<div class="timeline-loop-edge">'
                f"↻ CONDITIONAL REFLECTION EDGE (Hop {hop_num} ➔ Hop {hop_num + 1}): Critic detected missing premises. "
                f"Sub-Query Generator formulated targeted follow-up: <code>{html.escape(next_sub_q)}</code>"
                f"</div>"
            )

    # Terminal outcome banner
    final_suff = bool(state.get("is_sufficient", False))
    curr_hop = int(state.get("current_hop", len(intermediate) or 1))
    if final_suff and curr_hop < max_hops:
        blocks.append(
            f'<div class="timeline-card" style="border-left: 3px solid #10B981; background:rgba(16,185,129,0.07);">'
            f'<div class="timeline-dot" style="background:#10B981;"></div>'
            f'<div style="font-family:var(--quant-mono); font-weight:800; color:#10B981; font-size:0.84rem;">'
            f"[EARLY STOPPING TRIGGERED AT HOP {curr_hop} / {max_hops}] — Bypassed {max_hops - curr_hop} redundant hop(s), routing directly to Synthesizer &amp; Active Guardrail."
            f"</div></div>"
        )
    else:
        blocks.append(
            f'<div class="timeline-card" style="border-left: 3px solid #3B82F6; background:rgba(59,130,246,0.07);">'
            f'<div class="timeline-dot" style="background:#3B82F6;"></div>'
            f'<div style="font-family:var(--quant-mono); font-weight:800; color:#3B82F6; font-size:0.84rem;">'
            f"✓ RETRIEVAL CONCLUDED AT HOP {curr_hop} / {max_hops} — Evidence routed to Citation Synthesizer &amp; Scale-Normalized Guardrail."
            f"</div></div>"
        )

    return f'<div class="timeline-container">{"".join(blocks)}</div>'


if "active_sys_code" not in st.session_state:
    st.session_state["active_sys_code"] = "SYS_C"

def set_active_sys(code: str):
    st.session_state["active_sys_code"] = code


# ---------------------------------------------------------------------------
# SIDEBAR CONFIGURATION
# ---------------------------------------------------------------------------
with st.sidebar:
    brand_placeholder = st.empty()

    st.subheader("1. System Architecture")
    active_code = st.session_state.get("active_sys_code", "SYS_C")

    def on_side_sys_change():
        st.session_state["active_sys_code"] = st.session_state["side_sys_choice"]

    side_sys_options = {
        "SYS_C": "SYS C // Adaptive Multi-Hop RAG",
        "SYS_B": "SYS B // Single-Pass Hybrid + Rerank",
        "SYS_A": "SYS A // Vanilla Dense Baseline",
    }
    st.selectbox(
        "Active Pipeline:",
        options=["SYS_C", "SYS_B", "SYS_A"],
        index=["SYS_C", "SYS_B", "SYS_A"].index(active_code),
        format_func=lambda x: side_sys_options[x],
        key="side_sys_choice",
        on_change=on_side_sys_change,
        help="Select between SYS C (Adaptive Multi-Hop State Machine with Sufficiency Critic), SYS B (Single-Pass Okapi BM25 + BGE Dense + Cross-Encoder Reranker), and SYS A (Vanilla Dense Baseline).",
    )

    if active_code == "SYS_B":
        mode_selection = "system_b"
        active_sys_prefix = "SYS.B"
        active_sys_sub = "SINGLE-PASS HYBRID + RERANK"
    elif active_code == "SYS_A":
        mode_selection = "system_a"
        active_sys_prefix = "SYS.A"
        active_sys_sub = "VANILLA DENSE BASELINE"
    else:
        active_sys_prefix = "SYS.C"
        active_sys_sub = "ADAPTIVE MULTI-HOP RAG"
        mode_selection = st.selectbox(
            "SYS C Operating Mode",
            options=["v2_aamr", "adaptive_v1", "fixed_1hop", "fixed_3hop"],
            index=0,
            format_func=lambda x: {
                "v2_aamr": "Agentic AMR (v2: XBRL + 10-K Router)",
                "adaptive_v1": "Adaptive AMR (v1: Text Only)",
                "fixed_1hop": "Ablation: Fixed 1-Hop",
                "fixed_3hop": "Ablation: Fixed 3-Hop",
            }[x],
            help="Select SYS C variant: Adaptive Agentic (v2), Text-only Adaptive (v1), or Ablation hops.",
            key="side_sys_c_mode",
        )

    active_sys_prefix = "SYS.B" if mode_selection == "system_b" else ("SYS.A" if mode_selection == "system_a" else "SYS.C")
    active_sys_sub = (
        "SINGLE-PASS HYBRID + RERANK"
        if mode_selection == "system_b"
        else ("VANILLA DENSE BASELINE" if mode_selection == "system_a" else "ADAPTIVE MULTI-HOP RAG")
    )
    brand_placeholder.markdown(
        f"""
<div class="sidebar-brand-wrap">
<svg width="36" height="36" viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg" style="flex-shrink:0;">
<rect width="48" height="48" rx="6" fill="#0A0D12" stroke="#F59E0B" stroke-width="1.8"/>
<path d="M12 34V22M20 34V14M28 34V24M36 34V18" stroke="#10B981" stroke-width="3.5" stroke-linecap="round"/>
<circle cx="20" cy="14" r="3" fill="#F59E0B"/>
<circle cx="36" cy="18" r="3" fill="#10B981"/>
<path d="M20 14L28 20L36 18" stroke="#F59E0B" stroke-width="2" stroke-linecap="round" stroke-dasharray="2 2"/>
</svg>
<div>
<div class="sidebar-brand-title">{active_sys_prefix} // TERMINAL</div>
<div class="sidebar-brand-sub">{active_sys_sub}</div>
</div>
</div>
""",
        unsafe_allow_html=True,
    )

    if mode_selection == "system_b":
        sys_b_retrieval_mode = st.selectbox(
            "SYS B Retrieval Mode",
            options=["hybrid_rerank", "hybrid", "bm25", "dense"],
            index=0,
            format_func=lambda m: {
                "hybrid_rerank": "SYS B: Hybrid + Cross-Encoder Rerank (Full)",
                "hybrid": "SYS B: Weighted Hybrid Fusion (BM25 + Dense)",
                "bm25": "SYS B: Okapi BM25 Sparse Only",
                "dense": "SYS B: BGE Dense Vector Only",
            }[m],
            help="Dynamically updates the SYS B architecture diagram ([B.02], [B.03], [B.04]) and executes the selected retrieval mode.",
        )
        sys_b_alpha = st.slider(
            "SYS B Hybrid Fusion Alpha (Dense Weight)",
            min_value=0.0,
            max_value=1.0,
            value=0.50,
            step=0.05,
            help="Weight between normalized dense score (alpha) and normalized Okapi BM25 score (1 - alpha).",
        )
        sys_b_top_k = st.slider(
            "SYS B Top-K Retrieved Chunks",
            min_value=1,
            max_value=10,
            value=5,
            help="Number of final context chunks passed to the single-pass System B generator.",
        )
        max_hops = 1
        sufficiency_threshold = 1.0
    elif mode_selection == "system_a":
        st.info("**SYS A Baseline**: Vanilla single-pass dense vector lookup without BM25, Cross-Encoder reranking, or Critic reflection.")
        sys_b_retrieval_mode = "dense"
        sys_b_alpha = 1.0
        sys_b_top_k = 4
        max_hops = 1
        sufficiency_threshold = 1.0
    else:
        sys_b_retrieval_mode = "hybrid_rerank"
        sys_b_alpha = 0.50
        sys_b_top_k = 5
        max_hops = st.slider(
            "SYS C Max Retrieval Hops",
            min_value=1,
            max_value=10,
            value=3,
            help="Maximum sequential search-and-reasoning iterations allowed for the System C multi-hop agent.",
        )
        sufficiency_threshold = st.slider(
            "SYS C Critic Sufficiency Threshold",
            min_value=0.50,
            max_value=1.00,
            value=0.85,
            step=0.05,
            help="Quantitative sufficiency threshold ([0.0, 1.0]). If Critic score >= threshold, System C triggers Early Stopping.",
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

    if selected_provider == "groq":
        model_options = {
            "openai/gpt-oss-120b": "OpenAI GPT-OSS (120B) — Team Notebook Default",
            "llama-3.1-8b-instant": "Llama 3.1 (8B) — Universal Free (Instant)",
            "llama-3.3-70b-versatile": "Llama 3.3 (70B) — Flagship",
            "gemma2-9b-it": "Google Gemma 2 (9B)",
        }
    elif selected_provider == "gemini":
        model_options = {
            "gemini-1.5-flash": "Gemini 1.5 Flash (Fast & Free Tier)",
            "gemini-2.0-flash": "Gemini 2.0 Flash (Next-Gen)",
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

    user_api_key = st.text_input(
        "API Key (Optional)",
        type="password",
        placeholder="Enter key or set in .env / secrets",
        help="Paste your private Gemini, Groq, Cohere, or OpenAI key here. If left blank, the app checks .env or Streamlit secrets.",
    )
    active_env_key = (
        os.getenv(f"{selected_provider.upper()}_API_KEY")
        or (selected_provider == "gemini" and os.getenv("GOOGLE_API_KEY"))
    )
    if user_api_key.strip():
        st.markdown(
            '<span class="metric-badge badge-amber">● Custom User Key Active</span>',
            unsafe_allow_html=True,
        )
    elif active_env_key:
        st.markdown(
            '<span class="metric-badge badge-emerald">● Environment / Secret Key Active</span>',
            unsafe_allow_html=True,
        )
    elif selected_provider == "mock":
        st.markdown(
            '<span class="metric-badge badge-emerald">● Mock Mode (No Key Required)</span>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            '<span class="metric-badge badge-amber">⚠ Key Required (Paste above or set in .env)</span>',
            unsafe_allow_html=True,
        )

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

    st.divider()

    selected_tickers: List[str] = []

    st.divider()

    st.subheader("3. Benchmark Presets (Evaluation Suite)")
    st.caption("Verified SEC 10-K FinQA/TAT-QA evaluation queries (FY2015–FY2025):")
    all_pool = load_benchmark_pool()
    for group_label, recipe_key in BENCHMARK_RECIPE_GROUPS.items():
        group_items = [q for q in all_pool if q.get("recipe") == recipe_key]
        if not group_items:
            continue
        with st.expander(f"{group_label}", expanded=(recipe_key == "table")):
            for item in group_items:
                btn_label = f"[{item['id'].upper()}] {item['ticker']} FY{item['year']}: {item['question'][:45]}..."
                if st.button(btn_label, use_container_width=True, key=f"side_bm_{item['id']}"):
                    st.session_state["user_query_input"] = item["question"]
                    st.session_state["active_benchmark_item"] = item
                    st.rerun()

    st.divider()

    llm_info = get_llm_status()
    st.subheader("Cloud Infrastructure")
    st.markdown(
        f"""
* **Active System**: `{active_sys_prefix}` (`{mode_selection}`)
* **LLM Engine**: `{selected_provider.upper()}` (`{selected_model}`)
* **Cloud DB**: `Supabase PostgreSQL` (`ap-southeast-1`)
* **Relational Table**: `sec_financials` (272 XBRL rows)
* **Pre-Computed Chunks**: `sec_chunks` (20,125 rows)
* **3-System Topology**: `SYS A / SYS B / SYS C Live View`
"""
    )


# ---------------------------------------------------------------------------
# MAIN INSTITUTIONAL TERMINAL HEADER & STATUS BAR
# ---------------------------------------------------------------------------
header_title_map = {
    "SYS.C": (
        "SYS C: Adaptive Multi-Hop Financial RAG",
        "Autonomous Sub-Query Decomposition • Deterministic XBRL + Hybrid 10-K Routing • Sufficiency Critic & Self-Healing Guardrail",
    ),
    "SYS.B": (
        "SYS B: Single-Pass Hybrid + Cross-Encoder Rerank Baseline",
        f"Okapi BM25 + BGE-Small Dense Retrieval • Min-Max Weighted Fusion (Alpha={sys_b_alpha:.2f}) • Cross-Encoder Reranker (No Critic Loop)",
    ),
    "SYS.A": (
        "SYS A: Vanilla Single-Pass Dense RAG (Baseline Placeholder)",
        "Single-Pass Dense Vector Cosine Lookup • Direct Prompt Generation • Baseline Reference Architecture",
    ),
}
active_hdr_title, active_hdr_sub = header_title_map[active_sys_prefix]

st.markdown(
    f"""
<div class="terminal-top-bar">
<div>
<div class="terminal-eyebrow">{active_sys_prefix} // SEC FORM 10-K QUANTITATIVE &amp; QUALITATIVE INTELLIGENCE</div>
<div class="main-header">{html.escape(active_hdr_title)}</div>
<div class="sub-header">{html.escape(active_hdr_sub)}</div>
</div>
<div class="terminal-status-cluster">
<span class="metric-badge badge-emerald">● SUPABASE PG: ONLINE</span>
<span class="metric-badge badge-amber">ACTIVE: {active_sys_prefix}</span>
<span class="metric-badge">ENGINE: {html.escape(selected_provider.upper())}</span>
<span class="metric-badge badge-cyan">10 CORPORA (FY2010–FY2026)</span>
</div>
</div>
""",
    unsafe_allow_html=True,
)

# Top-Level System Architecture Switcher (Instant 1-click toggling between SYS C, SYS B, and SYS A)
top_col1, top_col2, top_col3 = st.columns(3)
with top_col1:
    st.button(
        "SYS C // ADAPTIVE MULTI-HOP" + (" [ACTIVE]" if active_sys_prefix == "SYS.C" else ""),
        type="primary" if active_sys_prefix == "SYS.C" else "secondary",
        use_container_width=True,
        key="nav_btn_sys_c",
        on_click=set_active_sys,
        args=("SYS_C",),
    )
with top_col2:
    st.button(
        "SYS B // HYBRID + RERANK" + (" [ACTIVE]" if active_sys_prefix == "SYS.B" else ""),
        type="primary" if active_sys_prefix == "SYS.B" else "secondary",
        use_container_width=True,
        key="nav_btn_sys_b",
        on_click=set_active_sys,
        args=("SYS_B",),
    )
with top_col3:
    st.button(
        "SYS A // DENSE BASELINE" + (" [ACTIVE]" if active_sys_prefix == "SYS.A" else ""),
        type="primary" if active_sys_prefix == "SYS.A" else "secondary",
        use_container_width=True,
        key="nav_btn_sys_a",
        on_click=set_active_sys,
        args=("SYS_A",),
    )

# Company Coverage Ticker Strip (Clean summary of data availability)
ticker_badges = "".join(
    f'<span class="metric-badge" title="{html.escape(COMPANIES[t]["name"])} &bull; {html.escape(COMPANIES[t]["sector"])}" style="cursor:help;">'
    f'<strong>{t}</strong>'
    f'</span>'
    for t in sorted(COMPANIES.keys())
)
st.markdown(
    f'<div style="display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:8px; margin-bottom:12px; padding:7px 12px; background:var(--term-bg-surface); border:1px solid var(--term-border); border-radius:var(--quant-radius);">'
    f'<div style="display:flex; align-items:center; gap:6px; flex-wrap:wrap;">'
    f'<span style="font-family:var(--quant-mono); font-size:0.68rem; font-weight:800; text-transform:uppercase; color:var(--quant-amber);">Indexed 10-K Filings:</span>'
    f'{ticker_badges}'
    f'</div>'
    f'<div style="font-family:var(--quant-mono); font-size:0.70rem; color:var(--text-muted);">'
    f'<strong>Available Corpus:</strong> <code>FY2010 – FY2026</code> &bull; 10 Large-Cap Filers'
    f'</div>'
    f'</div>',
    unsafe_allow_html=True,
)

# Main-Stage Quick-Start Preset Chips (FTUX 1-Click Action across 1, 2, and 3 Hops)
st.markdown(
    '<div style="font-family:var(--quant-mono); font-size:0.72rem; font-weight:800; text-transform:uppercase; color:var(--text-color); margin-bottom:6px;">'
    'FinQA Academic Benchmark Presets (1-Click Test across SYS A, SYS B, or SYS C):'
    '</div>',
    unsafe_allow_html=True,
)

featured_bms = get_featured_benchmark_questions()
if len(featured_bms) >= 4:
    col_q1, col_q2, col_q3, col_q4 = st.columns(4)
    with col_q1:
        f1 = featured_bms[0]
        if st.button(f"[T1] 1-HOP MATH // {f1['id'].upper()}\n{f1['ticker']} FY{f1['year']} Restructuring R&D", use_container_width=True, key="quick_bm1"):
            st.session_state["user_query_input"] = f1["question"]
            st.session_state["active_benchmark_item"] = f1
            st.rerun()
    with col_q2:
        f2 = featured_bms[1]
        years_s = "-".join(str(y)[2:] for y in f2.get("applicable_years", [f2["year"]]))
        if st.button(f"[T2] CROSS-YEAR // {f2['id'].upper()}\n{f2['ticker']} FY{years_s} Diluted EPS YoY", use_container_width=True, key="quick_bm2"):
            st.session_state["user_query_input"] = f2["question"]
            st.session_state["active_benchmark_item"] = f2
            st.rerun()
    with col_q3:
        f3 = featured_bms[2]
        if st.button(f"[T3] TABLE + FOOTNOTE // {f3['id'].upper()}\n{f3['ticker']} FY{f3['year']} Tegra Processor", use_container_width=True, key="quick_bm3"):
            st.session_state["user_query_input"] = f3["question"]
            st.session_state["active_benchmark_item"] = f3
            st.rerun()
    with col_q4:
        f4 = featured_bms[3]
        if st.button(f"[T4] CLOUD LEASES // {f4['id'].upper()}\n{f4['ticker']} FY{f4['year']} Cloud GPU Leases", use_container_width=True, key="quick_bm4"):
            st.session_state["user_query_input"] = f4["question"]
            st.session_state["active_benchmark_item"] = f4
            st.rerun()

# Query Input Console
default_query = st.session_state.get(
    "user_query_input",
    "What percentage of Meta Platforms' total restructuring charges for 2023 was recorded under research and development?",
)
query_text = st.text_area(
    "SEC 10-K Financial Intelligence Prompt (edit query or run any preset chip above):",
    value=default_query,
    height=75,
    placeholder="e.g. Compare NVIDIA and Microsoft cloud and data center performance in 2024...",
)

active_bm = st.session_state.get("active_benchmark_item")
if active_bm and query_text.strip() == active_bm.get("question", "").strip():
    qid = html.escape(str(active_bm.get("id", "")))
    tkr = html.escape(str(active_bm.get("ticker", "")))
    yrs_str = ", ".join(str(y) for y in active_bm.get("applicable_years", [active_bm.get("year", "")]))
    rcp = html.escape(str(active_bm.get("recipe", "")))
    ans = html.escape(str(active_bm.get("answer", "")))
    prog = str(active_bm.get("program", "")).strip()
    prog_val = run_finqa_program(prog) if prog else None
    prog_html = f'&nbsp;&bull;&nbsp; <strong>FinQA Formula:</strong> <code>{html.escape(prog)}</code>' if prog else ""
    if prog_val is not None:
        prog_html += f' ➔ <code>{prog_val:.4f}</code>'

    st.markdown(
        f'<div style="margin-top:4px; margin-bottom:12px; padding:9px 13px; background:var(--term-bg-surface); border:1px solid var(--term-border); border-left:4px solid #10B981; border-radius:var(--quant-radius);">'
        f'<div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:5px;">'
        f'<span style="font-family:var(--quant-mono); font-size:0.75rem; font-weight:800; color:#10B981;">'
        f'BENCHMARK SPECIFICATION // FINQA VERIFIED GROUND TRUTH // {qid.upper()} ({tkr} &bull; FY{yrs_str} &bull; {rcp.upper()})'
        f'</span>'
        f'<span class="metric-badge badge-emerald">VERIFIED FINQA / TAT-QA</span>'
        f'</div>'
        f'<div style="font-size:0.83rem; color:var(--text-color);">'
        f'<strong>Expected Ground Truth:</strong> <code style="color:#10B981; font-weight:bold;">{ans}</code>'
        f'{prog_html}'
        f'</div>'
        f'</div>',
        unsafe_allow_html=True,
    )
    gold_ev = active_bm.get("gold_evidence", [])
    if gold_ev:
        with st.expander(f"Ground-Truth SEC 10-K Evidence References ({len(gold_ev)} Filings / Sections Mapped)", expanded=False):
            for i, ev in enumerate(gold_ev):
                st.markdown(
                    f"**[{i+1}] {html.escape(str(ev.get('doc_id', '')))}** &bull; "
                    f"`{html.escape(str(ev.get('item', '')))}` &bull; "
                    f"*{html.escape(str(ev.get('heading', '')))}* ({html.escape(str(ev.get('kind', 'text')).upper())})"
                )
                st.code(ev.get("quote", ""), language="markdown")

col_run, col_hint = st.columns([1.5, 5.5])
with col_run:
    run_btn = st.button(f"EXECUTE // {active_sys_prefix} QUERY", type="primary", use_container_width=True)
with col_hint:
    profile_desc = (
        f"SYS B ({sys_b_retrieval_mode.upper()}) • Alpha: {sys_b_alpha:.2f} • Top-K: {sys_b_top_k} (No Critic)"
        if mode_selection == "system_b"
        else (
            "SYS A (VANILLA DENSE PLACEHOLDER) • Single-Pass Top-4"
            if mode_selection == "system_a"
            else f"SYS C ({mode_selection.upper()}) • Max Hops: {max_hops} • Critic Early Stop: ≥ {sufficiency_threshold:.2f}"
        )
    )
    st.markdown(
        f'<div style="display:flex; align-items:center; gap:8px; flex-wrap:wrap; margin-top:3px;">'
        f'<span class="metric-badge badge-emerald">{html.escape(selected_provider.upper())} ENGINE READY</span>'
        f'<span style="font-family:var(--quant-mono); font-size:0.70rem; opacity:0.85;">Active Profile: <code>{html.escape(profile_desc)}</code></span>'
        f'</div>',
        unsafe_allow_html=True,
    )

# Interactive Pipeline Slot (renders 3-system topology + 5-column telemetry ribbon above the fold)
pipeline_viz_slot = st.empty()
status_log_slot = st.empty()

if not run_btn and "last_system_c_result" not in st.session_state:
    pipeline_viz_slot.markdown(
        render_visual_state_graph(
            state={"max_hops": max_hops, "sufficiency_threshold": sufficiency_threshold, "current_hop": 1},
            active_node=None,
            visited_nodes=[],
            elapsed_sec=0.0,
            is_finished=False,
            selected_mode=mode_selection,
            sys_b_mode=sys_b_retrieval_mode,
            sys_b_alpha=sys_b_alpha,
            sys_b_top_k=sys_b_top_k,
        ),
        unsafe_allow_html=True,
    )

# ---------------------------------------------------------------------------
# REAL-TIME STREAMING EXECUTION ENGINE (BREAKING THE BLACK BOX)
# ---------------------------------------------------------------------------
if run_btn and query_text.strip():
    try:
        if mode_selection in ("system_b", "system_a"):
            from src.system_b.ui_bridge import execute_system_b_for_streamlit

            is_sys_a = mode_selection == "system_a"
            eff_b_mode = "dense" if is_sys_a else sys_b_retrieval_mode
            eff_b_alpha = 1.0 if is_sys_a else sys_b_alpha
            eff_b_topk = 4 if is_sys_a else sys_b_top_k
            first_node = "a_embed" if is_sys_a else "b_scope"

            pipeline_viz_slot.markdown(
                render_visual_state_graph(
                    state={"max_hops": 1, "sufficiency_threshold": 1.0, "current_hop": 1},
                    active_node=first_node,
                    visited_nodes=[],
                    elapsed_sec=0.0,
                    is_finished=False,
                    selected_mode=mode_selection,
                    sys_b_mode=eff_b_mode,
                    sys_b_alpha=eff_b_alpha,
                    sys_b_top_k=eff_b_topk,
                ),
                unsafe_allow_html=True,
            )
            label_title = (
                "Executing SYS A Single-Pass Vanilla Dense Baseline (Placeholder)..."
                if is_sys_a
                else f"Executing SYS B Single-Pass Pipeline ({eff_b_mode}, alpha={eff_b_alpha:.2f})..."
            )
            with status_log_slot.status(label_title, expanded=True) as status_box:
                status_box.write(
                    f"**[{active_sys_prefix} Retriever]** Running `{eff_b_mode}` (alpha=`{eff_b_alpha:.2f}`, top_k=`{eff_b_topk}`)..."
                )
                eff_b_tickers = list(selected_tickers) if selected_tickers else None
                active_bm = st.session_state.get("active_benchmark_item")
                if active_bm and query_text.strip() == active_bm.get("question", "").strip():
                    if not eff_b_tickers and active_bm.get("ticker"):
                        eff_b_tickers = [active_bm["ticker"]]

                live_state, visited_nodes, total_wall_time = execute_system_b_for_streamlit(
                    query=query_text.strip(),
                    selected_tickers=eff_b_tickers,
                    retrieval_mode=eff_b_mode,
                    alpha=eff_b_alpha,
                    top_k=eff_b_topk,
                )
                if is_sys_a:
                    live_state["mode"] = "system_a_dense"
                    visited_nodes = ["a_embed", "a_lookup", "a_generate"]
                else:
                    visited_nodes = ["b_scope", "b_bm25", "b_dense", "b_rerank", "b_generator"]

                b_raw = live_state.get("system_b_raw", {})
                b_timings = b_raw.get("timings", {})
                status_box.write(
                    f"**[{active_sys_prefix} Corpus: {b_raw.get('corpus_source')}]** Indexed `{b_raw.get('corpus_chunks', 0):,}` chunks ➔ "
                    f"Retrieved `{len(b_raw.get('hits', []))}` top hits in `{float(b_timings.get('retrieval_seconds', 0.0)):.2f}s`"
                )
                status_box.write(
                    f"**[{active_sys_prefix} Single-Pass Generator]** Generated answer in `{float(b_timings.get('generation_seconds', 0.0)):.2f}s` "
                    f"(Citations recognized: `{b_raw.get('has_citations')}`)"
                )
                status_box.update(
                    label=f"[DONE] {active_sys_prefix} ({eff_b_mode}) — Completed in {total_wall_time:.2f}s (Single-Pass | {len(b_raw.get('hits', []))} Chunks)",
                    state="complete",
                    expanded=False,
                )

            pipeline_viz_slot.markdown(
                render_visual_state_graph(
                    state=live_state,
                    active_node=None,
                    visited_nodes=visited_nodes,
                    elapsed_sec=total_wall_time,
                    is_finished=True,
                    loop_triggered=False,
                    selected_mode=mode_selection,
                    sys_b_mode=eff_b_mode,
                    sys_b_alpha=eff_b_alpha,
                    sys_b_top_k=eff_b_topk,
                ),
                unsafe_allow_html=True,
            )
            st.session_state["last_system_c_result"] = live_state
            st.session_state["last_system_c_visited"] = visited_nodes
            st.session_state["last_system_c_wall_time"] = total_wall_time
            st.session_state["last_executed_mode_selection"] = mode_selection
        else:
            from src.system_c.graph import build_system_c_graph
            from src.system_c.state import create_initial_state
            from src.system_c.telemetry import summarize_rq3_metrics

            effective_max_hops = max_hops
            force_max = False
            graph_mode = mode_selection
            if mode_selection == "fixed_1hop":
                effective_max_hops = 1
                force_max = True
                graph_mode = "v1_amr"
            elif mode_selection == "fixed_3hop":
                effective_max_hops = 3
                force_max = True
                graph_mode = "v1_amr"
            elif mode_selection == "adaptive_v1":
                graph_mode = "v1_amr"

            target_ticker_arg = selected_tickers[0] if len(selected_tickers) == 1 else None
            target_tickers_arg = list(selected_tickers) if selected_tickers else None

            # Propagate benchmark hints if executing an active benchmark QA
            active_bm = st.session_state.get("active_benchmark_item")
            bm_years_hint = []
            if active_bm and query_text.strip() == active_bm.get("question", "").strip():
                if not target_ticker_arg and active_bm.get("ticker"):
                    target_ticker_arg = active_bm["ticker"]
                    target_tickers_arg = [active_bm["ticker"]]
                bm_years_hint = active_bm.get("applicable_years") or ([active_bm["year"]] if active_bm.get("year") else [])

            live_state = dict(
                create_initial_state(
                    query=query_text.strip(),
                    max_hops=effective_max_hops,
                    mode=graph_mode,
                    target_ticker=target_ticker_arg,
                    target_tickers=target_tickers_arg,
                    force_max_hops=force_max,
                    sufficiency_threshold=sufficiency_threshold,
                )
            )
            if active_bm and query_text.strip() == active_bm.get("question", "").strip():
                live_state["ground_truth_answer"] = active_bm.get("answer")
                live_state["ground_truth_program"] = active_bm.get("program")
                live_state["benchmark_id"] = active_bm.get("id")
                if bm_years_hint and not live_state.get("target_fiscal_years"):
                    live_state["target_fiscal_years"] = bm_years_hint

            compiled_graph = build_system_c_graph()
            visited_nodes = []
            start_time = time.perf_counter()

            # Highlight Node C.01 (Decomposer) immediately upon click
            pipeline_viz_slot.markdown(
                render_visual_state_graph(
                    state=live_state,
                    active_node="decomposer",
                    visited_nodes=visited_nodes,
                    elapsed_sec=0.0,
                    is_finished=False,
                    selected_mode=mode_selection,
                    sys_b_mode=sys_b_retrieval_mode,
                    sys_b_alpha=sys_b_alpha,
                    sys_b_top_k=sys_b_top_k,
                ),
                unsafe_allow_html=True,
            )

            with status_log_slot.status("Executing SYS C Multi-Hop LangGraph State Machine...", expanded=True) as status_box:
                for step_event in compiled_graph.stream(live_state):
                    for node_name, node_update in step_event.items():
                        if isinstance(node_update, dict):
                            live_state.update(node_update)
                        if node_name not in visited_nodes:
                            visited_nodes.append(node_name)

                        elapsed = time.perf_counter() - start_time
                        cur_hop = int(live_state.get("current_hop", 1) or 1)

                        next_active: Optional[str] = None
                        loop_just_triggered = False
                        if node_name == "decomposer":
                            if live_state.get("mode") == "v2_aamr" and live_state.get("needs_tabular_tool"):
                                next_active = "tabular_tool"
                            else:
                                next_active = "retriever"
                            t_list = live_state.get("target_tickers") or []
                            sq_list = live_state.get("sub_queries") or []
                            status_box.write(
                                f"**[C.01 Planner / Decomposer]** Extracted tickers `{t_list}` & planned `{len(sq_list)}` atomic sub-queries ({elapsed:.2f}s)"
                            )
                        elif node_name == "tabular_tool":
                            next_active = "retriever"
                            tab_cnt = len(live_state.get("tabular_evidence", []) or [])
                            status_box.write(
                                f"**[C.02 Tabular XBRL Router]** Injected `{tab_cnt}` deterministic SEC XBRL financial block(s) ({elapsed:.2f}s)"
                            )
                        elif node_name == "retriever":
                            next_active = "critic"
                            ev_cnt = len(live_state.get("accumulated_evidence", []) or [])
                            status_box.write(
                                f"**[C.03 Hybrid 10-K Retriever — Hop {cur_hop}]** Accumulated `{ev_cnt}` total evidence chunks ({elapsed:.2f}s)"
                            )
                        elif node_name == "critic":
                            s_score = float(live_state.get("sufficiency_score", 0.0) or 0.0)
                            is_suff = bool(live_state.get("is_sufficient", False))
                            if is_suff or cur_hop >= effective_max_hops:
                                next_active = "synthesizer"
                                status_box.write(
                                    f"**[C.04 Sufficiency Critic — Hop {cur_hop}]** Score `{s_score:.2f}` ≥ `{sufficiency_threshold:.2f}` ➔ **Sufficient! Routing to Synthesizer** ({elapsed:.2f}s)"
                                )
                            else:
                                next_active = "generator"
                                loop_just_triggered = True
                                gaps = live_state.get("missing_premises", []) or []
                                status_box.write(
                                    f"**[C.04 Sufficiency Critic — Hop {cur_hop}]** Score `{s_score:.2f}` < `{sufficiency_threshold:.2f}` ➔ **Triggering Hop {cur_hop + 1} Reflection Loop** (Missing: `{gaps[:2]}`) ({elapsed:.2f}s)"
                                )
                        elif node_name == "generator":
                            next_active = "retriever"
                            loop_just_triggered = True
                            new_sq = live_state.get("current_sub_query", "")
                            status_box.write(
                                f"**[Hop {cur_hop} Sub-Query Generator]** Formulated targeted follow-up: `{new_sq}` ({elapsed:.2f}s)"
                            )
                        elif node_name == "synthesizer":
                            next_active = "guardrail"
                            c_cnt = len(live_state.get("citations", []) or [])
                            status_box.write(
                                f"**[C.05 Executive Synthesizer]** Drafted response with `{c_cnt}` inline SEC citations ({elapsed:.2f}s)"
                            )
                        elif node_name == "guardrail":
                            g_rep = live_state.get("guardrail_report", {}) or {}
                            passed = bool(live_state.get("guardrail_passed", True))
                            rep_cnt = int(live_state.get("repair_count", 0) or 0)
                            max_rep = int(live_state.get("max_repairs", 1) or 1)
                            if not passed and rep_cnt < max_rep:
                                next_active = "repair"
                                status_box.write(
                                    f"**[C.06 Active Guardrail]** Flagged `{len(g_rep.get('ungrounded_numbers', []))}` ungrounded figure(s) ➔ Routing to Self-Healing Repair ({elapsed:.2f}s)"
                                )
                            else:
                                next_active = None
                                status_box.write(
                                    f"**[C.06 Active Guardrail]** Verified `{len(g_rep.get('verified_numbers', []))}` financial figures (Faithfulness: `{g_rep.get('faithfulness_score', 1.0):.2f}`) ({elapsed:.2f}s)"
                                )
                        elif node_name == "repair":
                            next_active = "guardrail"
                            status_box.write(
                                f"**[Self-Healing Repair]** Completed closed-loop numerical grounding repair pass ({elapsed:.2f}s)"
                            )

                        pipeline_viz_slot.markdown(
                            render_visual_state_graph(
                                state=live_state,
                                active_node=next_active,
                                visited_nodes=visited_nodes,
                                elapsed_sec=elapsed,
                                is_finished=(next_active is None),
                                loop_triggered=loop_just_triggered,
                                selected_mode=mode_selection,
                                sys_b_mode=sys_b_retrieval_mode,
                                sys_b_alpha=sys_b_alpha,
                                sys_b_top_k=sys_b_top_k,
                            ),
                            unsafe_allow_html=True,
                        )

                total_wall_time = time.perf_counter() - start_time
                live_state.setdefault("telemetry", {})["rq3_summary"] = summarize_rq3_metrics(live_state)
                status_box.update(
                    label=f"[DONE] SYS C Execution Log — Completed in {total_wall_time:.2f}s ({live_state.get('current_hop', 1)}/{effective_max_hops} Hops | Sufficiency: {live_state.get('sufficiency_score', 0.0):.2f})",
                    state="complete",
                    expanded=False,
                )

            pipeline_viz_slot.markdown(
                render_visual_state_graph(
                    state=live_state,
                    active_node=None,
                    visited_nodes=visited_nodes,
                    elapsed_sec=total_wall_time,
                    is_finished=True,
                    loop_triggered=False,
                    selected_mode=mode_selection,
                    sys_b_mode=sys_b_retrieval_mode,
                    sys_b_alpha=sys_b_alpha,
                    sys_b_top_k=sys_b_top_k,
                ),
                unsafe_allow_html=True,
            )

            st.session_state["last_system_c_result"] = live_state
            st.session_state["last_system_c_visited"] = visited_nodes
            st.session_state["last_system_c_wall_time"] = total_wall_time
            st.session_state["last_executed_mode_selection"] = mode_selection

    except Exception as exc:
        import traceback

        st.error(f"Execution Error: {str(exc)}")
        st.markdown("**Error Details & Stack Trace** *(use copy button)*:")
        st.code(traceback.format_exc(), language="python")

# ---------------------------------------------------------------------------
# EXECUTIVE DOSSIER RESULTS PRESENTATION (IMMEDIATELY ABOVE THE FOLD)
# ---------------------------------------------------------------------------
if "last_system_c_result" in st.session_state:
    result: Dict[str, Any] = st.session_state["last_system_c_result"]
    visited_nodes_saved: List[str] = st.session_state.get("last_system_c_visited", [])
    total_wall_time: float = st.session_state.get("last_system_c_wall_time", 0.0)
    last_exec_mode: str = st.session_state.get("last_executed_mode_selection", "")

    if not run_btn:
        same_mode_family = (
            (mode_selection == "system_b" and last_exec_mode == "system_b")
            or (mode_selection == "system_a" and last_exec_mode == "system_a")
            or (mode_selection not in ("system_b", "system_a") and last_exec_mode not in ("system_b", "system_a"))
        )
        display_state = (
            dict(result, max_hops=max_hops, sufficiency_threshold=sufficiency_threshold)
            if same_mode_family
            else {"max_hops": max_hops, "sufficiency_threshold": sufficiency_threshold, "current_hop": 1}
        )
        if mode_selection == "system_b" and "system_b_raw" in display_state:
            display_state["system_b_raw"] = dict(
                display_state["system_b_raw"],
                mode=sys_b_retrieval_mode,
                alpha=sys_b_alpha,
                top_k=sys_b_top_k,
            )
        pipeline_viz_slot.markdown(
            render_visual_state_graph(
                state=display_state,
                active_node=None,
                visited_nodes=visited_nodes_saved if same_mode_family else [],
                elapsed_sec=total_wall_time if same_mode_family else 0.0,
                is_finished=same_mode_family,
                loop_triggered=False,
                selected_mode=mode_selection,
                sys_b_mode=sys_b_retrieval_mode,
                sys_b_alpha=sys_b_alpha,
                sys_b_top_k=sys_b_top_k,
            ),
            unsafe_allow_html=True,
        )

    guard_report = result.get("guardrail_report", {}) or {}
    verified_nums = guard_report.get("verified_numbers", []) or []
    ungrounded_nums = guard_report.get("ungrounded_numbers", []) or []
    citations = result.get("citations", []) or []
    evidence_chunks = result.get("accumulated_evidence", []) or []
    primary_tkr = result.get("target_ticker")
    all_tkrs = result.get("target_tickers") or ([primary_tkr] if primary_tkr else ["SEC"])
    f_years = result.get("fiscal_years") or []

    verified_pills_html, ungrounded_pills_html = render_grounding_pills_html(
        verified_numbers=verified_nums,
        ungrounded_numbers=ungrounded_nums,
        citations=citations,
        evidence_chunks=evidence_chunks,
        default_ticker=primary_tkr,
    )

    res_tab_brief, res_tab_rq1, res_tab_rq2, res_tab_rq3 = st.tabs(
        [
            "[01] Executive Brief & Citations",
            "[RQ1] Multi-Hop Trace (Adaptivity)",
            "[RQ2] Grounding Audit (Faithfulness)",
            "[RQ3] Latency & Economics (Pareto)",
        ]
    )

    with res_tab_brief:
        final_answer = result.get("final_answer") or ""
        tkr_display = ", ".join(str(t) for t in all_tkrs) if all_tkrs else "AUTO"
        yr_display = ", ".join(f"FY{y}" for y in f_years) if f_years else "MULTI-PERIOD"
        audit_status = "PASSED" if result.get("guardrail_passed", True) else "FLAGGED"
        audit_col = "#10B981" if result.get("guardrail_passed", True) else "#F59E0B"

        if final_answer:
            formatted_answer = format_executive_synthesis_md(final_answer)
            st.markdown(
                f'<div class="dossier-shell">'
                f'<div class="dossier-tape">'
                f"<span><strong>TICKER(S):</strong> {html.escape(tkr_display)} &nbsp;&bull;&nbsp; "
                f"<strong>FILING:</strong> SEC FORM 10-K ({html.escape(yr_display)}) &nbsp;&bull;&nbsp; "
                f"<strong>CITATIONS:</strong> {len(citations)} MAPPED</span>"
                f'<span style="color:{audit_col}; font-weight:800;">GUARDRAIL AUDIT: {audit_status} ({len(verified_nums)} VERIFIED)</span>'
                f"</div></div>",
                unsafe_allow_html=True,
            )
            st.markdown(formatted_answer, unsafe_allow_html=True)
            with st.expander("Copy Executive Brief (Markdown)", expanded=False):
                st.code(final_answer, language="markdown")
        else:
            st.info("No synthesis generated.")

        # Academic Benchmark Evaluation Summary
        bm_gt = result.get("ground_truth_answer") or (st.session_state.get("active_benchmark_item", {}).get("answer") if st.session_state.get("active_benchmark_item", {}).get("question", "").strip() == query_text.strip() else None)
        bm_prog = result.get("ground_truth_program") or (st.session_state.get("active_benchmark_item", {}).get("program") if st.session_state.get("active_benchmark_item", {}).get("question", "").strip() == query_text.strip() else None)
        if bm_gt:
            prog_part = f" &bull; <strong>FinQA Formula:</strong> <code>{html.escape(bm_prog)}</code>" if bm_prog else ""
            st.markdown(
                f'<div style="margin:10px 0; padding:8px 12px; background:rgba(16, 185, 129, 0.08); border:1px solid rgba(16, 185, 129, 0.35); border-radius:var(--quant-radius);">'
                f'<span style="font-family:var(--quant-mono); font-size:0.75rem; font-weight:800; color:#10B981;">'
                f'BENCHMARK GROUND TRUTH EVALUATION // Expected: <code style="color:#10B981;">{html.escape(bm_gt)}</code>{prog_part}'
                f'</span>'
                f'</div>',
                unsafe_allow_html=True,
            )

        st.markdown("##### Scale-Verified Numerical Claims *(hover pill for SEC chunk provenance)*")
        st.markdown(verified_pills_html, unsafe_allow_html=True)

        st.markdown("##### Ground-Truth SEC 10-K Citations Mapped (RQ2)")
        if citations:
            cit_cols = st.columns(2)
            for idx, cit in enumerate(citations):
                with cit_cols[idx % 2]:
                    with st.expander(
                        f"{cit.get('tag', '[Citation]')} — {cit.get('ticker', 'SEC')} FY{cit.get('fiscal_year', '')} ({cit.get('section', '10-K')})",
                        expanded=(idx < 2),
                    ):
                        st.markdown(f"**Chunk ID**: `{cit.get('chunk_id')}`")
                        st.markdown(f"**Ticker / Fiscal Year**: `{cit.get('ticker')}` | `FY{cit.get('fiscal_year')}`")
                        st.markdown("**Supported Claim / Excerpt**:")
                        st.caption(cit.get("supported_claim", ""))
        else:
            st.caption("No structured citation records logged for this run.")

    with res_tab_rq1:
        b_raw_info = result.get("system_b_raw")
        if b_raw_info:
            st.markdown("#### System B — Single-Pass Hybrid Retrieval & Cross-Encoder Rerank Breakdown")
            st.caption(
                f"Mode: `{b_raw_info.get('mode')}` | Alpha (Dense Weight): `{b_raw_info.get('alpha', 0.5):.2f}` | "
                f"Corpus Source: `{b_raw_info.get('corpus_source')}` (`{b_raw_info.get('corpus_chunks', 0):,}` chunks)"
            )
            b_hits = b_raw_info.get("hits", [])
            if b_hits:
                st.dataframe(pd.DataFrame(b_hits), use_container_width=True, hide_index=True)
            st.divider()
        else:
            st.markdown("#### Autonomous Multi-Hop Reflection & Retrieval Audit Timeline (RQ1)")
            st.caption(
                "Visualizing each hop's atomic sub-query, retrieved SEC 10-K evidence chunks, Critic sufficiency score, and conditional reflection loop edges."
            )
        st.markdown(render_multihop_timeline_html(result), unsafe_allow_html=True)

        with st.expander("System B Benchmark Summary (Published 60-Query Results)", expanded=bool(b_raw_info)):
            from src.system_b.ui_bridge import load_system_b_eval_summary

            b_summary = load_system_b_eval_summary()
            b_modes = b_summary.get("modes", {})
            if b_modes:
                rows_b = []
                for m_name, m_stats in b_modes.items():
                    rows_b.append({
                        "Retrieval Mode": m_name,
                        "Retrieval Attempts": m_stats.get("attempts", 60),
                        "Generated Answers": m_stats.get("completed", 35),
                        "Pure Abstentions": m_stats.get("pure_abstentions", 0),
                        "Answers w/ Valid Citations": m_stats.get("answers_with_recognized_citations", 0),
                        "Invalid Citation Labels": m_stats.get("answers_with_invalid_citation_labels", 0),
                        "Ref Token F1 Proxy": round(float(m_stats.get("mean_reference_token_f1_proxy", 0.0)), 4),
                        "Median Latency (s)": round(float(m_stats.get("latency_p50_seconds", 0.0)), 2),
                        "Reported Tokens": m_stats.get("total_reported_tokens", 0),
                    })
                st.dataframe(pd.DataFrame(rows_b), use_container_width=True, hide_index=True)
                st.caption(
                    "Source: `reports/system_b/full_eval_summary/summary.json` (240 retrieval runs across 60 Golden Benchmark questions; "
                    "35 generated per mode before provider daily token quota limit)."
                )

    with res_tab_rq2:
        st.markdown("#### Scale-Normalized Numerical Grounding & Hallucination Audit (RQ2)")
        passed = bool(result.get("guardrail_passed", True))
        if passed:
            st.success(
                "✓ Active Guardrail Passed: Every quantitative figure extracted from the synthesis matches SEC 10-K ground-truth tables or text chunks."
            )
        else:
            st.warning(
                "⚠ Active Guardrail Alert: One or more numerical figures could not be verified against retrieved SEC filings (hover over badges below for diagnostic details)."
            )

        col_g1, col_g2, col_g3, col_g4 = st.columns(4)
        col_g1.metric(
            "Faithfulness Score",
            f"{float(guard_report.get('faithfulness_score', 1.0)) * 100:.1f}%",
        )
        col_g2.metric(
            "Numerical Error Rate",
            f"{float(guard_report.get('numerical_grounding_error_rate', 0.0)) * 100:.1f}%",
        )
        col_g3.metric("Verified Claims", f"{len(verified_nums)}")
        col_g4.metric("Self-Healing Repairs", f"{result.get('repair_count', 0)}")

        st.divider()
        col_v1, col_v2 = st.columns(2)
        with col_v1:
            st.markdown("##### ✓ Verified Financial Figures *(hover for SEC chunk provenance)*")
            st.markdown(verified_pills_html, unsafe_allow_html=True)
        with col_v2:
            st.markdown("##### ⚠ Flagged / Ungrounded Figures *(hover for audit reason)*")
            st.markdown(ungrounded_pills_html, unsafe_allow_html=True)

        with st.expander("Full Grounding Audit Ledger (Touch / Mobile Inspector)", expanded=False):
            audit_rows = []
            for num in verified_nums:
                audit_rows.append({
                    "Status": "✓ VERIFIED",
                    "Value / Figure": str(num),
                    "SEC Provenance / Chunk ID": primary_tkr or "SEC Filing",
                    "Audit Diagnostic": "Matches extracted SEC 10-K filing or tabular XBRL entry exactly or within tolerance",
                })
            for num in ungrounded_nums:
                audit_rows.append({
                    "Status": "⚠ FLAGGED",
                    "Value / Figure": str(num),
                    "SEC Provenance / Chunk ID": "Unmatched in Retrieved Corpus",
                    "Audit Diagnostic": "Number appeared in synthesis without corresponding ground-truth citation in retrieved chunks",
                })
            if audit_rows:
                df_audit = pd.DataFrame(audit_rows)
                st.dataframe(df_audit, use_container_width=True, hide_index=True)
            else:
                st.caption("No quantitative figures detected in output.")

        if result.get("tabular_evidence"):
            st.divider()
            st.markdown("##### Deterministic XBRL Tabular Ground-Truth Injected (`tabular_tool`)")
            for blk in result.get("tabular_evidence", []):
                st.code(blk, language="markdown")

    with res_tab_rq3:
        st.markdown("#### Inference Economics & Pareto Telemetry (RQ3)")
        telemetry = result.get("telemetry", {}) or {}
        rq3_summary = telemetry.get("rq3_summary", {}) or {}

        e1, e2, e3, e4 = st.columns(4)
        e1.metric("Total Tokens", f"{int(telemetry.get('total_tokens', 0)):,}")
        e2.metric(
            "Prompt / Completion",
            f"{int(telemetry.get('total_prompt_tokens', 0)):,} / {int(telemetry.get('total_completion_tokens', 0)):,}",
        )
        e3.metric("Estimated Query Cost", f"${float(telemetry.get('estimated_cost_usd', 0.0)):.6f}")
        e4.metric("Cost per 1,000 Queries", f"${float(rq3_summary.get('cost_per_1k_queries_usd', 0.0)):.4f}")

        node_lats = telemetry.get("node_latencies_ms", {}) or {}
        if node_lats:
            st.markdown("##### Node-Level Execution Latency Breakdown (ms)")
            df_lat = pd.DataFrame(
                [{"Graph Node": k, "Latency (ms)": v} for k, v in node_lats.items()]
            )
            st.dataframe(df_lat, use_container_width=True, hide_index=True)

        calls = telemetry.get("calls", []) or []
        if calls:
            st.markdown("##### LLM Invocation Ledger")
            df_calls = pd.DataFrame(calls)
            st.dataframe(df_calls, use_container_width=True, hide_index=True)
        else:
            st.caption("No LLM calls recorded in telemetry.")

# ---------------------------------------------------------------------------
# SEC 10-K XBRL DATA EXPLORER
# ---------------------------------------------------------------------------
st.divider()
st.subheader("SEC 10-K XBRL Ground-Truth Explorer")
with st.expander("Explore Canonical SEC XBRL Financial Filings (`sec_financials` / `data/financials.csv`)", expanded=False):
    df_fin = load_financials_data()
    if not df_fin.empty:
        col_c1, col_c2 = st.columns([1, 3])
        with col_c1:
            explore_ticker = st.selectbox(
                "Select SEC Filer Ticker",
                options=sorted(df_fin["ticker"].unique()),
                index=0,
            )
            if explore_ticker in COMPANIES:
                st.caption(
                    f"**{COMPANIES[explore_ticker]['name']}**  \n"
                    f"Sector: {COMPANIES[explore_ticker]['sector']}  \n"
                    f"Coverage: {COMPANIES[explore_ticker]['filings']}"
                )
        df_filtered = df_fin[df_fin["ticker"] == explore_ticker].sort_values(
            "fiscal_year_end", ascending=False
        )
        display_cols = [
            c
            for c in [
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
            if c in df_filtered.columns
        ]
        st.dataframe(df_filtered[display_cols], use_container_width=True, hide_index=True)
    else:
        st.info("No local `data/financials.csv` found to display.")
