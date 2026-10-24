# Aryan Handoff: System C Integration, Contracts & Git Workflow

**To:** Aryan (Citations, Guardrails & RQ2 Lead)  
**From:** Anish (System Architect, Orchestration & RQ3 Lead)  
**Shared Integration Branch:** `feature/system-c-adaptive-rag` (aliased as `feat/system-c-core`)  
**Your Working Branch:** `feat/system-c-aryan-citations`  
**Target Milestones:** Milestone 1 Demo (Sun, 25 Oct) & Checkpoint 2 Empirical Runs (Thu, 29 Oct)

---

## 1. What Is Already Built & Working Out-of-the-Box

I have built and verified the complete LangGraph state machine (`v1_amr` and `v2_aamr`) under [`src/system_c/`](file:///Users/anishdobz/projects/cs614_group8/src/system_c) and synced our branch with Amanda's latest `origin/feature/rag-baseline` (`build_vdb_base_RAG.ipynb` RAG 1–5):

1. **[`src/system_c/state.py`](file:///Users/anishdobz/projects/cs614_group8/src/system_c/state.py)**: Defines `AdaptiveRAGState`, `EvidenceChunk`, and `CitationRecord`.
2. **[`src/system_c/llm.py`](file:///Users/anishdobz/projects/cs614_group8/src/system_c/llm.py)**: Unified LLM wrapper (`call_llm(state, node_name, messages)`).
   * Supports **local Ollama (`qwen2.5:7b`) with zero API key**, **Groq (`openai/gpt-oss-120b`)**, **OpenAI (`gpt-4o-mini`)**, and **Mock mode (`LLM_PROVIDER=mock`)** for instant unit tests.
   * **CRITICAL RULE:** Always use `call_llm(state, node_name, messages)` inside your nodes! It automatically records prompt/completion tokens, latency (`ms`), and USD cost into `state["telemetry"]` for our **RQ3 Inference Economics** benchmark.
3. **[`src/system_c/corpus.py`](file:///Users/anishdobz/projects/cs614_group8/src/system_c/corpus.py) & [`src/system_c/tools/tabular_tool.py`](file:///Users/anishdobz/projects/cs614_group8/src/system_c/tools/tabular_tool.py)**:
   * Uses the exact same structure-preserving chunker (`chunk_by_structure`), contextual headers (`doc_header`), and XBRL `financials.csv` citation tags (`[F-<ticker>-<year>]`) as Amanda's `build_vdb_base_RAG.ipynb`.
4. **[`src/system_c/nodes/decomposer.py`](file:///Users/anishdobz/projects/cs614_group8/src/system_c/nodes/decomposer.py), [`retriever.py`](file:///Users/anishdobz/projects/cs614_group8/src/system_c/nodes/retriever.py), [`critic.py`](file:///Users/anishdobz/projects/cs614_group8/src/system_c/nodes/critic.py), & [`graph.py`](file:///Users/anishdobz/projects/cs614_group8/src/system_c/graph.py)**:
   * Implements Anish's Query Decomposer, Hybrid Retriever + Cross-Encoder Reranker, Evidence Sufficiency Critic, and conditional loop (`max_hops = 3`).

---

## 2. Your 3 Plug-and-Play Files (Aryan's Module Ownership)

I have put functional baseline implementations in your 3 files so the full pipeline passes all tests today. You own refining, stress-testing, and benchmarking these 3 modules + **RQ2 (Faithfulness & Citation Grounding)**:

### Deliverable A: Conditioned Sub-Query Generator ([`src/system_c/nodes/generator.py`](file:///Users/anishdobz/projects/cs614_group8/src/system_c/nodes/generator.py))
* **When it runs:** Triggered when `critic_node` sets `is_sufficient = False` and `current_hop < max_hops`.
* **Inputs from `state`:** `original_query`, `accumulated_evidence`, `missing_premises` (explicit list of missing facts flagged by the Critic), and `critic_reasoning`.
* **Outputs to return:**
  ```python
  {
      "current_hop": next_hop,
      "current_sub_query": follow_up_query,
      "sub_queries": updated_sub_queries,
      "telemetry": updated_telemetry,
  }
  ```

### Deliverable B: Answer Synthesizer & Inline Table Citation Mapper ([`src/system_c/nodes/synthesizer.py`](file:///Users/anishdobz/projects/cs614_group8/src/system_c/nodes/synthesizer.py))
* **When it runs:** Triggered when `is_sufficient == True` or `current_hop == max_hops`.
* **Citation Format Requirement:**
  * For 10-K text & markdown table chunks: `[<TICKER> FY<YEAR>, <SECTION>, <CHUNK_ID>]` (e.g., `[NVDA FY2026, Item 7, NVDA_FY2026_2026-01-25:220]`).
  * For XBRL `financials.csv` blocks (in `v2_aamr`): `[F-<TICKER>-<YEAR>]` (e.g., `[F-NVDA-2026]`).
* **Outputs to return:** `draft_answer`, `final_answer`, `citations` (`List[CitationRecord]`), and `telemetry`.

### Deliverable C: Active Hallucination & Numerical Guardrail ([`src/system_c/guardrails/verifier.py`](file:///Users/anishdobz/projects/cs614_group8/src/system_c/guardrails/verifier.py))
* **Purpose:** Supports **RQ2 (Factual Faithfulness & Numerical Grounding Error Rate)**.
* **What it does:** Extracts every dollar figure, decimal, and percentage in `draft_answer` (excluding citation tags and 4-digit years) and verifies exact grounding in `accumulated_evidence`.
* **Outputs to return:** `final_answer`, `guardrail_passed` (`bool`), `guardrail_report` (`verified_numbers`, `ungrounded_numbers`, `numerical_grounding_error_rate`, `faithfulness_score`), and `telemetry`.

---

## 3. Git Branching Workflow (How We Work Without Stepping on Each Other)

1. **Fetch and checkout your personal feature branch off our System C integration branch:**
   ```bash
   git fetch origin
   git checkout -b feat/system-c-aryan-citations origin/feature/system-c-adaptive-rag
   ```
2. **Run the fast unit test suite (`< 1 second` in mock mode):**
   ```bash
   pytest tests/test_system_c.py -v
   ```
3. **Run a live end-to-end query using Local Ollama (`qwen2.5:7b`) or Groq (`LLM_PROVIDER=groq`):**
   ```bash
   # Using local Ollama (no API key needed):
   LLM_PROVIDER=ollama LLM_MODEL=qwen2.5:7b python -m src.system_c.graph --mode v2_aamr --max-hops 2 \
     --query "What was NVIDIA total revenue and operating income in FY2026, and what key Data Center trends drove that performance?"

   # Or using Groq (with GROQ_API_KEY in .env):
   LLM_PROVIDER=groq python -m src.system_c.graph --mode v1_amr --max-hops 3 \
     --query "How did foreign exchange headwinds impact gross margin, and what debt covenants applied?"
   ```
4. **Merge back to `feature/system-c-adaptive-rag` once `pytest` passes:**
   * Always merge into `feature/system-c-adaptive-rag` first (never directly into `feature/rag-baseline` or `main` until we run our joint integration check).
