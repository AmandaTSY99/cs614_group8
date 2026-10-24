# Active Task: System C Core Architecture & Aryan Handoff

**Current Focus:** Phase 1 & Phase 2 Complete! System C (`v1_amr` & `v2_aamr`) LangGraph state machine, RQ3 Inference Economics telemetry, and Aryan's integration modules are built, verified with `pytest` (6/6 passing), and tested live against `NVDA` FY2026 10-K filings using local Ollama (`qwen2.5:7b`).

---

## Task Checklist

- [x] **Phase 0: Workspace Isolation & Repo Sync**
  - [x] Isolated repo to `~/projects/cs614_group8` (non-OneDrive, non-iCloud).
  - [x] Synced latest `origin/feature/rag-baseline` (`build_vdb_base_RAG.ipynb` with RAG 1–5 & `lookup_financials`).
  - [x] Archived raw binary `.docx`/`.xlsx`/`.pdf` files into `docs/context/raw_archives/`.
  - [x] Created integration branch `feature/system-c-adaptive-rag` (`feat/system-c-core`) and working branch `feat/system-c-anish-state-graph`.

- [x] **Phase 1: System C Package Structure (`src/system_c/`)**
  - [x] [`src/system_c/state.py`](file:///Users/anishdobz/projects/cs614_group8/src/system_c/state.py) — `AdaptiveRAGState`, `EvidenceChunk`, and `CitationRecord` TypedDict contracts.
  - [x] [`src/system_c/llm.py`](file:///Users/anishdobz/projects/cs614_group8/src/system_c/llm.py) — Unified LLM client (`ollama` default `qwen2.5:7b`, `groq`, `openai`, `mock`) with automatic RQ3 telemetry logging.
  - [x] [`src/system_c/telemetry.py`](file:///Users/anishdobz/projects/cs614_group8/src/system_c/telemetry.py) — RQ3 latency, prompt/completion tokens, USD cost, early-stopping, and Hop Attribution tracker.
  - [x] [`src/system_c/corpus.py`](file:///Users/anishdobz/projects/cs614_group8/src/system_c/corpus.py) — 10-K loader & contextual table-preserving chunker (`chunk_by_structure` + `doc_header` matching Amanda's RAG 3–5).
  - [x] [`src/system_c/tools/tabular_tool.py`](file:///Users/anishdobz/projects/cs614_group8/src/system_c/tools/tabular_tool.py) — Autonomous agentic XBRL lookup tool (`[F-<ticker>-<year>]`) for System C v2 (`v2_aamr`).
  - [x] [`src/system_c/nodes/decomposer.py`](file:///Users/anishdobz/projects/cs614_group8/src/system_c/nodes/decomposer.py) — Query Decomposer & Complexity Planner node (Anish).
  - [x] [`src/system_c/nodes/retriever.py`](file:///Users/anishdobz/projects/cs614_group8/src/system_c/nodes/retriever.py) — Hybrid Retriever + Cross-Encoder Reranker node (Anish).
  - [x] [`src/system_c/nodes/critic.py`](file:///Users/anishdobz/projects/cs614_group8/src/system_c/nodes/critic.py) — Evidence Sufficiency Critic node with `max_hops=3` loop control (Anish).
  - [x] [`src/system_c/nodes/generator.py`](file:///Users/anishdobz/projects/cs614_group8/src/system_c/nodes/generator.py) — Conditioned Follow-Up Sub-Query Generator node (Aryan).
  - [x] [`src/system_c/nodes/synthesizer.py`](file:///Users/anishdobz/projects/cs614_group8/src/system_c/nodes/synthesizer.py) — Answer Synthesizer & Inline Table Citation Mapper node (Aryan).
  - [x] [`src/system_c/guardrails/verifier.py`](file:///Users/anishdobz/projects/cs614_group8/src/system_c/guardrails/verifier.py) — Active Numerical Grounding & Faithfulness Guardrail node (Aryan).
  - [x] [`src/system_c/graph.py`](file:///Users/anishdobz/projects/cs614_group8/src/system_c/graph.py) — LangGraph compiler & CLI entry point supporting `--mode v1_amr` and `--mode v2_aamr`.

- [x] **Phase 2: Validation & Milestone 1 Demo Script**
  - [x] Created [`tests/test_system_c.py`](file:///Users/anishdobz/projects/cs614_group8/tests/test_system_c.py) — 6/6 tests passing (`single_hop`, `multi_hop`, `max_hops=3` ceiling, `v2_aamr` tabular tool, and numerical guardrail verification).
  - [x] Verified live execution with local Ollama `qwen2.5:7b` on `NVDA` FY2026 10-K disclosures (`0.0` numerical grounding error, exact inline table citations).

- [x] **Phase 3: Aryan Handoff & Git Sync**
  - [x] Pushed integration branch `feature/system-c-adaptive-rag` to `origin` tracking remote.
  - [x] Updated [`ARYAN_HANDOFF.md`](file:///Users/anishdobz/projects/cs614_group8/ARYAN_HANDOFF.md) with plug-and-play contracts, `call_llm` telemetry wrapper usage, and Git branch workflow.

- [x] **Phase 4: Milestone 1 Showcase & RQ3 Inference Economics Ablation**
  - [x] Created [`scripts/demo_milestone1_system_c.py`](file:///Users/anishdobz/projects/cs614_group8/scripts/demo_milestone1_system_c.py) — Runs 3 curated SEC 10-K benchmark queries (Single-Hop early stopping, Multi-Hop MD&A + Footnotes, and Quantitative Tabular `v1_amr` vs `v2_aamr`) with formatted ANSI terminal table and markdown/JSON export.
  - [x] Created [`scripts/run_rq3_ablation.py`](file:///Users/anishdobz/projects/cs614_group8/scripts/run_rq3_ablation.py) — Benchmarks Fixed 1-Hop vs. Fixed 3-Hop vs. Adaptive AMR (v1) vs. Agentic AAMR (v2) across 12 SEC 10-K queries, exporting Pareto coordinates to `reports/rq3_ablation_summary.json`, `reports/rq3_ablation_metrics.csv`, and `reports/rq3_ablation_per_query.csv`.
  - [x] Updated [`tests/test_system_c.py`](file:///Users/anishdobz/projects/cs614_group8/tests/test_system_c.py) with `test_rq3_ablation_force_max_hops` — 7/7 tests passing in 0.56s.
