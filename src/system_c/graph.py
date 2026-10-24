"""
LangGraph State Machine Compiler & CLI Runner for System C.

Owned by: Anish (System Architect & Orchestration Lead)

Supports both architectural evolutions:
1. `mode="v1_amr"`  (Adaptive Multi-Hop RAG):
   `decomposer -> retriever -> critic -> (generator -> retriever [up to max_hops=3]) -> synthesizer -> guardrail`
2. `mode="v2_aamr"` (Agentic Adaptive Multi-Hop RAG):
   Adds autonomous routing to `tabular_tool` (`financials.csv` XBRL lookup) when `needs_tabular_tool`
   is flagged by the planner, plus complexity-aware early routing.
"""

import argparse
import json
from typing import Any, Dict, Literal, Optional

from langgraph.graph import END, START, StateGraph

from src.system_c.guardrails.verifier import guardrail_node
from src.system_c.nodes.critic import critic_node
from src.system_c.nodes.decomposer import decomposer_node
from src.system_c.nodes.generator import generator_node
from src.system_c.nodes.retriever import retriever_node
from src.system_c.nodes.synthesizer import synthesizer_node
from src.system_c.state import AdaptiveRAGState, create_initial_state
from src.system_c.telemetry import summarize_rq3_metrics
from src.system_c.tools.tabular_tool import tabular_tool_node


def route_after_decomposer(
    state: AdaptiveRAGState,
) -> Literal["tabular_tool", "retriever"]:
    """
    In `v2_aamr` mode, if the planner detects a quantitative financial metric query
    (`needs_tabular_tool == True`), first invoke `tabular_tool` to inject deterministic
    `[F-<ticker>-<year>]` XBRL figures before running text/table chunk retrieval.
    """
    if state.get("mode") == "v2_aamr" and state.get("needs_tabular_tool"):
        return "tabular_tool"
    return "retriever"


def route_after_critic(
    state: AdaptiveRAGState,
) -> Literal["generator", "synthesizer"]:
    """
    Conditional Reflection Edge (Anish's Core Loop Control):
    - If `is_sufficient == True` OR `current_hop >= max_hops`, route to Aryan's `synthesizer`.
    - Otherwise (`is_sufficient == False` and `current_hop < max_hops`), route to Aryan's
      `generator` to formulate a conditioned Hop N+1 sub-query.
    """
    hop = state.get("current_hop", 1)
    max_hops = state.get("max_hops", 3)
    if state.get("is_sufficient") or hop >= max_hops:
        return "synthesizer"
    return "generator"


def build_system_c_graph():
    """Compile and return the executable LangGraph state machine for System C."""
    workflow = StateGraph(AdaptiveRAGState)

    # Register nodes (Anish's Orchestration + Aryan's Generation/Citations/Guardrails + v2 Tooling)
    workflow.add_node("decomposer", decomposer_node)
    workflow.add_node("tabular_tool", tabular_tool_node)
    workflow.add_node("retriever", retriever_node)
    workflow.add_node("critic", critic_node)
    workflow.add_node("generator", generator_node)
    workflow.add_node("synthesizer", synthesizer_node)
    workflow.add_node("guardrail", guardrail_node)

    # Wire edges
    workflow.add_edge(START, "decomposer")
    workflow.add_conditional_edges(
        "decomposer",
        route_after_decomposer,
        {
            "tabular_tool": "tabular_tool",
            "retriever": "retriever",
        },
    )
    workflow.add_edge("tabular_tool", "retriever")
    workflow.add_edge("retriever", "critic")

    workflow.add_conditional_edges(
        "critic",
        route_after_critic,
        {
            "generator": "generator",
            "synthesizer": "synthesizer",
        },
    )
    workflow.add_edge("generator", "retriever")
    workflow.add_edge("synthesizer", "guardrail")
    workflow.add_edge("guardrail", END)

    return workflow.compile()


def run_system_c(
    query: str,
    max_hops: int = 3,
    mode: str = "v1_amr",
    target_ticker: Optional[str] = None,
    fiscal_years: Optional[list[int]] = None,
    mock_sufficient_at_hop: Optional[int] = None,
    force_max_hops: bool = False,
) -> AdaptiveRAGState:
    """
    Execute a query end-to-end through System C and return the final `AdaptiveRAGState`.
    """
    initial_state = create_initial_state(
        query=query,
        max_hops=max_hops,
        mode=mode,
        target_ticker=target_ticker,
        fiscal_years=fiscal_years,
        force_max_hops=force_max_hops,
    )
    if mock_sufficient_at_hop is not None:
        initial_state["telemetry"]["mock_sufficient_at_hop"] = mock_sufficient_at_hop

    app = build_system_c_graph()
    final_state: AdaptiveRAGState = app.invoke(initial_state)
    final_state["telemetry"]["rq3_summary"] = summarize_rq3_metrics(final_state)
    return final_state


def main() -> None:
    parser = argparse.ArgumentParser(description="Run System C (Adaptive Multi-Hop RAG) via LangGraph.")
    parser.add_argument(
        "--query",
        type=str,
        default="How did NVIDIA data center revenue perform in FY2026, and what supply or risk factors impacted gross margins?",
        help="Financial question to run through System C.",
    )
    parser.add_argument(
        "--mode",
        type=str,
        default="v1_amr",
        choices=["v1_amr", "v2_aamr"],
        help="System C version: v1_amr (Adaptive Multi-Hop) or v2_aamr (Agentic AMR with Tabular XBRL tool).",
    )
    parser.add_argument("--max-hops", type=int, default=3, help="Maximum retrieval hops (default: 3).")
    args = parser.parse_args()

    result = run_system_c(query=args.query, max_hops=args.max_hops, mode=args.mode)
    print("\n" + "=" * 80)
    print(f"SYSTEM C ({args.mode.upper()}) EXECUTION SUMMARY")
    print("=" * 80)
    print(f"Query:          {result['original_query']}")
    print(f"Ticker / Years: {result['target_ticker']} / {result['fiscal_years']}")
    print(f"Hops Executed:  {result['current_hop']} / {result['max_hops']} (Sufficient: {result['is_sufficient']})")
    print(f"Sub-Queries:    {json.dumps(result['sub_queries'], indent=2)}")
    print(f"Chunks Fetched: {len(result['accumulated_evidence'])}")
    print("-" * 80)
    print("FINAL ANSWER:")
    print(result["final_answer"])
    print("-" * 80)
    print("CITATIONS MAPPED (RQ2):")
    print(json.dumps(result["citations"], indent=2))
    print("-" * 80)
    print("GUARDRAIL REPORT (RQ2):")
    print(json.dumps(result["guardrail_report"], indent=2))
    print("-" * 80)
    print("RQ3 INFERENCE ECONOMICS SUMMARY (Anish):")
    print(json.dumps(result["telemetry"].get("rq3_summary", {}), indent=2))


if __name__ == "__main__":
    main()
