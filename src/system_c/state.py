"""
State Machine Schema for System C (Adaptive Multi-Hop RAG - AMR v1 & Agentic AAMR v2).

Owned by: Anish (System Architect & Orchestration Lead)
Shared Contract with: Aryan (Citations, Guardrails & Sub-Query Generator Lead)
"""

from typing import Any, Dict, List, Optional
from typing_extensions import TypedDict


class EvidenceChunk(TypedDict):
    """Normalized chunk schema compatible with Amanda/Xavier's 10-K corpus & Aryan's Citation Mapper."""
    chunk_id: str                # e.g. "NVDA_FY2026_2026-01-25:42" or "F-NVDA-2026"
    content: str                 # Markdown chunk text (including repeated table headers if table)
    metadata: Dict[str, Any]     # doc_id, ticker, filer, fiscal_year, section, chunk, source_type
    relevance_score: float       # Reranker or hybrid similarity score
    hop_retrieved: int           # Which hop (1, 2, or 3) retrieved this chunk (for RQ1 Hop Attribution)


class CitationRecord(TypedDict):
    """Structured inline citation mapping for RQ2 Faithfulness & Citation F1."""
    tag: str                     # Inline citation tag, e.g. "[NVDA FY2026, Item 7, Chunk 42]" or "[F-NVDA-2026]"
    chunk_id: str                # Exact EvidenceChunk.chunk_id
    ticker: str
    fiscal_year: Any
    section: str
    supported_claim: str         # The sentence or numerical figure supported by this citation


class AdaptiveRAGState(TypedDict):
    """
    Central LangGraph State Schema for System C.
    All nodes accept `state: AdaptiveRAGState` and return a partial dictionary updating fields.
    """
    # --- 1. Input & Extracted Metadata ---
    original_query: str
    mode: str                                  # "v1_amr" (Adaptive Multi-Hop) or "v2_aamr" (Agentic with Tabular Tool + Auditor)
    target_ticker: Optional[str]               # Primary ticker (e.g. "NVDA")
    target_tickers: List[str]                  # All tickers mentioned (e.g. ["AAPL", "MSFT"] for comparative queries)
    target_pairs: List[ List[Any] ]            # List of [ticker, fiscal_year] pairs (compatible with build_vdb_base_RAG.ipynb)
    fiscal_years: List[int]

    # --- 2. Planning & Decomposition (Anish: decomposer.py / Aryan: generator.py) ---
    query_complexity: str                      # "single_hop", "multi_hop", or "tabular_quant" (used in v2 AAMR pre-router)
    sub_queries: List[str]                     # Planned sub-queries from decomposer + follow-ups
    sub_query_plans: List[Dict[str, Any]]      # Granular sub-query routing plans (query, target_tool, ticker, fiscal_year)
    current_sub_query: str                     # Active sub-query for the current retrieval hop
    needs_tabular_tool: bool                   # v2 AAMR flag: whether deterministic financials.csv tool should run

    # --- 3. Retrieval Evidence Accumulator (Anish: retriever.py & tools/tabular_tool.py) ---
    accumulated_evidence: List[EvidenceChunk]
    tabular_evidence: List[str]                # Formatted [F-<ticker>-<year>] XBRL blocks from financials.csv (v2 AAMR)
    intermediate_answers: List[Dict[str, Any]] # Hop-by-hop reasoning trace

    # --- 4. Loop Control & Sufficiency Reflection (Anish: critic.py) ---
    current_hop: int                           # 1-indexed hop counter
    max_hops: int                              # Hard ceiling (default = 3)
    force_max_hops: bool                       # If True, disable early-stopping to benchmark Fixed Max-Hops in RQ3 ablation
    is_sufficient: bool                        # True if evidence covers all premises of original_query
    sufficiency_score: float                   # Quantitative evidence sufficiency score (0.0 to 1.0)
    sufficiency_threshold: float               # Early-stopping threshold (default = 0.85)
    missing_premises: List[str]                # Explicit gaps identified by Critic (passed to Aryan's generator.py)
    missing_entities: List[str]                # Laser-focused missing financial entities/metrics (e.g. ["2022 R&D spending"])
    missing_years: List[int]                   # Laser-focused missing fiscal years (e.g. [2022])
    redundant_search_prevented: bool           # True if loop halted early to prevent redundant duplicate retrieval
    critic_reasoning: str                      # Detailed explanation from Evidence Sufficiency Critic

    # --- 5. Synthesis, Citations & Guardrails (Aryan: synthesizer.py & guardrails/verifier.py) ---
    draft_answer: Optional[str]                # Initial synthesized answer before guardrail audit
    final_answer: Optional[str]                # Verified, citation-grounded final response
    citations: List[CitationRecord]            # Structured list of citations extracted/mapped
    guardrail_passed: bool                     # True if all numerical claims exist in accumulated_evidence
    guardrail_report: Dict[str, Any]           # RQ2 metrics: verified_numbers, ungrounded_numbers, faithfulness_score
    repair_count: int                          # Number of self-correction hallucination repair passes executed
    max_repairs: int                           # Hard ceiling on self-correction repairs (default = 1)
    repair_history: List[Dict[str, Any]]       # Iteration-by-iteration repair diffs for RQ2 faithfulness ablation

    # --- 6. Telemetry & Inference Economics (Anish: telemetry.py - RQ3 Lead) ---
    telemetry: Dict[str, Any]                  # Node latencies, prompt/completion tokens, USD cost, hop attribution


def create_initial_state(
    query: str,
    max_hops: int = 3,
    mode: str = "v1_amr",
    target_ticker: Optional[str] = None,
    fiscal_years: Optional[List[int]] = None,
    force_max_hops: bool = False,
    target_tickers: Optional[List[str]] = None,
    sufficiency_threshold: float = 0.85,
    max_repairs: int = 1,
) -> AdaptiveRAGState:
    """Factory helper to initialize a clean AdaptiveRAGState for a new query execution."""
    f_years = fiscal_years or []
    all_tickers = target_tickers or ([target_ticker] if target_ticker else [])
    
    pairs = []
    if all_tickers and f_years:
        pairs = [[t, y] for t in all_tickers for y in f_years]
    elif all_tickers:
        pairs = [[t, None] for t in all_tickers]
    elif f_years:
        pairs = [[None, y] for y in f_years]

    primary_ticker = target_ticker or (all_tickers[0] if all_tickers else None)

    return AdaptiveRAGState(
        original_query=query,
        mode=mode,
        target_ticker=primary_ticker,
        target_tickers=all_tickers,
        target_pairs=pairs,
        fiscal_years=f_years,
        query_complexity="multi_hop",
        sub_queries=[],
        sub_query_plans=[],
        current_sub_query=query,
        needs_tabular_tool=False,
        accumulated_evidence=[],
        tabular_evidence=[],
        intermediate_answers=[],
        current_hop=0,
        max_hops=max_hops,
        force_max_hops=force_max_hops,
        is_sufficient=False,
        sufficiency_score=0.0,
        sufficiency_threshold=sufficiency_threshold,
        missing_premises=[],
        missing_entities=[],
        missing_years=[],
        redundant_search_prevented=False,
        critic_reasoning="",
        draft_answer=None,
        final_answer=None,
        citations=[],
        guardrail_passed=True,
        guardrail_report={},
        repair_count=0,
        max_repairs=max_repairs,
        repair_history=[],
        telemetry={
            "mode": mode,
            "calls": [],
            "node_latencies_ms": {},
            "total_prompt_tokens": 0,
            "total_completion_tokens": 0,
            "total_tokens": 0,
            "estimated_cost_usd": 0.0,
            "hop_count": 0,
            "early_stopped": False,
        },
    )
