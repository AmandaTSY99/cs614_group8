# Master Engineering Prompt: Implementing & Benchmarking System C v3 (AAMR-SG)

Copy and execute the prompt below to implement System C v3, run the phased smoke tests, and execute the comparative evaluation.

---

```text
You are an expert distributed systems engineer and financial RAG architect working on the CS614 enterprise financial analysis project.

OBJECTIVE:
Implement System C v3 ("v3_aamr_sg": Agentic Adaptive Multi-Hop with Semantic Grounding & Schema-Aware Sufficiency) to resolve the operational trade-off between System C v1 (89.7% peak footnote accuracy) and System C v2 (37% faster median latency and continuous multi-year XBRL time-series lookback).

GIT BRANCH REQUIREMENT:
You MUST work strictly on the System C integration branch:
- Checkout branch: `git checkout feature/system-c-adaptive-rag` (or create feature branch off it: `git checkout -b feat/system-c-v3-adaptive-aamr feature/system-c-adaptive-rag`).
- Ensure the working tree is clean and up to date before making changes.

PRIMARY SPECIFICATION DOCUMENT:
Read and strictly follow: `docs/system-c/SYSTEM_C_V3_SPECIFICATION.md` and `docs/context/ARCHITECTURAL_INSIGHTS_V1_VS_V2.md`.

IMPLEMENTATION STEPS:

1. Update State Schema (`src/system_c/state.py`):
   - Add `mode: Literal["v1_amr", "v2_aamr", "v3_aamr_sg"]`.
   - Ensure `create_initial_state` accepts `mode="v3_aamr_sg"`.

2. Upgrade Query Decomposer (`src/system_c/nodes/decomposer.py`):
   - Define `XBRL_CORE_METRICS` mapping standard columns: `revenue`, `net_income`, `operating_income`, `total_assets`, `total_liabilities`, `stockholders_equity`, `cash_and_equivalents`, `operating_cash_flow`, `eps_diluted`.
   - In `mode="v3_aamr_sg"`, only set `needs_tabular_tool = True` if the query explicitly targets one of these 10 headline metrics. If the question asks for Gross Margin, Segment Revenue, Debt Maturity Schedules, or Footnotes, set `needs_tabular_tool = False`.

3. Upgrade Evidence Sufficiency Critic (`src/system_c/nodes/critic.py`):
   - Remove the brittle negative keyword list (`has_narrative_need`) that caused premature early-stopping at Hop 1 in v2.
   - In `mode="v3_aamr_sg"`, check if the requested line-item is actually present in the tabular schema. If not present, DO NOT force `score = max(score, 0.95)`. Allow the LLM Critic's organic sufficiency score to govern early-stopping so the pipeline continues to Hops 2 and 3 for footnote disclosures.

4. Update Graph Router (`src/system_c/graph.py`):
   - In `route_after_decomposer`, allow `mode in ("v2_aamr", "v3_aamr_sg") and state.get("needs_tabular_tool")` to route to `tabular_tool`.
   - Register `system_c_v3` in `run_system_c` CLI arguments.

5. Update Evaluation Adapters (`scripts/rq2/adapters.py` & `scripts/rq3/run_rq3_experiment.py`):
   - Register `SystemCAdapter(mode="v3_aamr_sg")` with name `"system_c_v3"`.
   - Ensure `system_c_v3` outputs match the standardized `ADAPTER_KEYS` schema.

---

TESTING PROTOCOL:

Step A: Unit Test Gate
Run: `pytest tests/test_system_c.py -v`
Ensure all existing unit tests continue to pass with 0 regressions.

Step B: Phase 1 Single-Query Smoke Test (`gold-073`)
Run:
`python -m scripts.rq3.run_rq3_experiment --systems system_c_v3 --benchmark data/benchmark_qa_pool_2015.json --query-ids gold-073`
Target Outcome: System C v3 MUST NOT early-stop at Hop 1. It must execute 2 hops and correctly retrieve NVIDIA's Gross Margin (8.8 percentage points increase), fixing the failure that occurred in v2!

Step C: Phase 2 Two-Query Dual-Path Smoke Test (`gold-066` + `gold-073`)
Run:
`python -m scripts.rq3.run_rq3_experiment --systems system_c_v3 --benchmark data/benchmark_qa_pool_2015.json --query-ids gold-066,gold-073`
Target Outcome:
- `gold-066` (Tesla Total Assets FY21 to FY25): Must early-stop at Hop 1 via XBRL, achieving the $75,675 million answer in <10 seconds.
- `gold-073` (NVIDIA Gross Margin): Must continue to Hop 2 and retrieve the Item 7 text chunk.
This proves that System C v3 successfully executes the dual-path without premature early-stopping!

Step D: Phase 3 Full 97-Question Benchmark Evaluation
Run:
`python -m scripts.rq3.run_rq3_experiment --systems system_c_v1,system_c_v2,system_c_v3 --benchmark data/benchmark_qa_pool_2015.json`
Run evaluator:
`python -m scripts.rq3.evaluate_rq3 --records reports/rq3/records.jsonl --output reports/rq3/summary_metrics.json`

Verify that:
1. `system_c_v3` recovers the 9 lost footnote questions from v2.
2. Accuracy reaches $\ge 93\%$, outperforming both v1 (89.7%) and v2 (82.8%).
3. Median latency remains sub-15s, preserving the operational speedup.
```
