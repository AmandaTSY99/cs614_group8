# System C Engineering Handoff: Module Contracts & Integration Guidelines

**Module:** Citations, Numerical Guardrails & Research Question 2 (RQ2) Specification  
**Architecture:** Adaptive Multi-Hop LangGraph State Machine (`v1_amr` & `v2_aamr`)  

---

## 1. System C Baseline Capabilities

The complete LangGraph state machine (`v1_amr` and `v2_aamr`) is implemented under [`src/system_c/`](file:///Users/anishdobz/projects/cs614_group8/src/system_c):

1. **[`src/system_c/state.py`](file:///Users/anishdobz/projects/cs614_group8/src/system_c/state.py)**: Defines `AdaptiveRAGState`, `EvidenceChunk`, and `CitationRecord`.
2. **[`src/system_c/llm.py`](file:///Users/anishdobz/projects/cs614_group8/src/system_c/llm.py)**: Unified LLM wrapper (`call_llm(state, node_name, messages)`).
   * Supports local Ollama (`qwen2.5:7b`), Groq, OpenAI (`gpt-4o-mini`, `gpt-5.4`), and Mock mode (`LLM_PROVIDER=mock`) for rapid deterministic unit tests.
   * Automatically records prompt/completion tokens, latency (`ms`), and USD cost into `state["telemetry"]` for **RQ3 Inference Economics**.
3. **[`src/system_c/corpus.py`](file:///Users/anishdobz/projects/cs614_group8/src/system_c/corpus.py) & [`src/system_c/tools/tabular_tool.py`](file:///Users/anishdobz/projects/cs614_group8/src/system_c/tools/tabular_tool.py)**:
   * Uses structure-preserving chunking (`chunk_by_structure`), contextual headers (`doc_header`), and XBRL `financials.csv` citation tags (`[F-<ticker>-<year>]`).
4. **[`src/system_c/nodes/decomposer.py`](file:///Users/anishdobz/projects/cs614_group8/src/system_c/nodes/decomposer.py), [`retriever.py`](file:///Users/anishdobz/projects/cs614_group8/src/system_c/nodes/retriever.py), [`critic.py`](file:///Users/anishdobz/projects/cs614_group8/src/system_c/nodes/critic.py), & [`graph.py`](file:///Users/anishdobz/projects/cs614_group8/src/system_c/graph.py)**:
   * Implements Query Decomposer, Hybrid Retriever + Cross-Encoder Reranker, Evidence Sufficiency Critic, and conditional reflection loop (`max_hops = 3`).

---

## 2. RQ2 Module Specifications & Contracts

### Deliverable A: Conditioned Sub-Query Generator ([`src/system_c/nodes/generator.py`](file:///Users/anishdobz/projects/cs614_group8/src/system_c/nodes/generator.py))
* **When it runs:** Triggered when `critic_node` sets `is_sufficient = False` and `current_hop < max_hops`.
* **Inputs from `state`:** `original_query`, `accumulated_evidence`, `missing_entities`, `missing_years`, `missing_premises` (gaps flagged by the Critic), and `critic_reasoning`.
* **As built (four changes):**
  1. **Critic gaps:** `missing_entities`, `missing_years` and `missing_premises` go to the LLM as separate prompt fields; sentinel values (`None`, `N/A`, `null`, `[]`, blanks) count as empty and `FY2026`-style years are normalised.
  2. **Full evidence summary:** the prompt lists every accumulated chunk as one line (`chunk_id | TICKER FYyear | short section`), capped at the 40 most recent (previously only the last 4 chunks).
  3. **Near-duplicate guard:** a follow-up whose word overlap with any earlier sub-query is >= 0.8 (after removing section words such as `Item 7` / `MD&A` and stopwords) is rejected.
  4. **Short fallback:** a rejected or unparseable reply is replaced by `<ticker> <first missing entity or premise>` (at most 15 words).
* The node still makes exactly one `call_llm(state, "generator", ...)` call.
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
* **Per-sentence citations:** every factual sentence ends with the tag(s) of the evidence block(s) that state the fact; a sentence combining figures from two blocks cites both. If the evidence does not cover part of the question, the answer says the filing does not disclose it (no tag).
* **`[E#]` labels, expanded by code:** the synthesizer prompt labels each evidence block `[E1]`, `[E2]`, … with a header (ticker, fiscal year, section). The model cites with those labels (`[E1]`, `[E1][E3]` or `[E1, E3]`); code expands them into the handoff-format tags above (short section = top-level item such as `Item 7`; at most 80 characters, so `app.py` styles them as chips; grouped labels become separate adjacent tags; backticks are stripped). An unknown label (e.g. `[E99]`) is left in place so the guardrail reports it as an invalid citation. `draft_answer` / `final_answer` contain only expanded tags.
* **Shared strict resolver:** `src/system_c/guardrails/citations.py` holds the sentence splitter and the tag → `chunk_id` resolver used by both the synthesizer and the guardrail. A tag resolves only if an evidence `chunk_id` appears in it as a whole token (or it is `F-<TICKER>-<YEAR>`); there is no section-name fallback and unresolved tags are never dropped.
* **`CitationRecord` granularity:** one record per (sentence, chunk) pair, with `supported_claim` = the sentence with its tags removed; the same chunk cited by two sentences gives two records. `repair_node` rebuilds `citations` from the repaired answer, so the list always matches the text the user reads (with no repair, the synthesizer's list already matches).
* **Outputs to return:** `draft_answer`, `final_answer`, `citations` (`List[CitationRecord]`), and `telemetry`.

### Deliverable C: Active Hallucination & Numerical Guardrail ([`src/system_c/guardrails/verifier.py`](file:///Users/anishdobz/projects/cs614_group8/src/system_c/guardrails/verifier.py))
* **Purpose:** Supports **RQ2 (Factual Faithfulness & Numerical Grounding Error Rate)**.
* **What it does:** Splits `draft_answer` into sentences and checks each one against **only the chunks that sentence cites** (not the pooled evidence):
  * **Numeric check (deterministic, always on):** extracts dollar amounts with scale words (`$500 million`, `$61.2 billion`), percentages (`12%`, `12 percent`), basis points and comma/decimal numbers (skipping 4-digit years, small counts and citation tags). Scale-aware matching lets `$60.9 billion` verify against `60,922` in an "(in millions)" table. Each number is `verified`, `derived` (computed from cited figures, e.g. a growth %; not an error), `ungrounded`, or `uncited` (in a sentence with no valid citation; an error).
  * **Semantic check (LLM, on by default):** one batched `call_llm(state, "guardrail_semantic", ...)` judges number-free factual sentences, cited or uncited (including refusals, which are supported only if the evidence really lacks the information) as `supported`, `partial` or `unsupported`. `partial` fails the guardrail.
* **Judge configuration (env vars):** `GUARDRAIL_SEMANTIC_CHECK` (`1` default; `0` disables the semantic check); `GUARDRAIL_JUDGE_PROVIDER` and `GUARDRAIL_JUDGE_MODEL` run the judge on a different provider/model than the answer model (via the optional `provider` / `model` arguments of `call_llm`; in `mock` mode the judge stays mock). Unset = same provider/model as the rest of System C.
* **Outputs to return:** exactly `final_answer`, `guardrail_passed` (`bool`), `guardrail_report` and `telemetry` (unchanged contract). `guardrail_report` keeps the original keys (`verified_numbers`, `ungrounded_numbers`, `numerical_grounding_error_rate`, `faithfulness_score`, `total_numerical_claims`, `has_inline_citations`) and adds:
  * `sentences`: per sentence `text`, `citations`, `chunk_ids`, `numbers` (`value` + `status`), `semantic_verdict`, `reason`
  * `unverified_sentences`, `unchecked_sentences`, `uncited_claim_sentences`: sentences that failed / could not be judged / are uncited factual claims
  * `derived_numbers`, `uncited_numbers`, `invalid_citations` (tags that map to no retrieved chunk)
  * `semantic_check_enabled`, `semantic_judge_provider`, `semantic_judge_model`, `semantic_verdict_counts`
  * `ungrounded_numbers` includes uncited numbers (for `app.py` compatibility) and `verified_numbers` includes derived figures (also listed in `derived_numbers`); the error rate is (ungrounded + uncited) / checked numbers excluding derived.
* If the guardrail fails and repairs remain, the graph routes to `repair_node` (below); if it still fails afterwards, a warning is appended to `final_answer`.

### Repair ([`src/system_c/nodes/repair.py`](file:///Users/anishdobz/projects/cs614_group8/src/system_c/nodes/repair.py))
* **When it runs:** `route_after_guardrail` sends a failed answer to `repair_node` while `repair_count < max_repairs` (default `max_repairs=1`, set via `run_system_c(..., max_repairs=N)`); the repaired answer always goes back through `guardrail_node`.
* **What it fixes:** flagged numbers (ungrounded or uncited), unverified sentences (sent with the text of the chunks they cite), invalid citation tags, and uncited sentences (it is shown the exact tag of the block that holds the figure). Computed figures get a hint naming both input blocks. Each claim is fixed from the evidence or the sentence is removed; valid tags are kept.
* **One LLM call:** `call_llm(state, "repair", ...)`.
* **Outputs to return:** `draft_answer`, `final_answer`, `citations` (rebuilt from the repaired text with `build_citation_records`), `repair_count`, `repair_history` and `telemetry`.

### RQ2 evaluation ([`scripts/rq2/`](../../scripts/rq2))
* Two stages: `generate.py` runs the systems in the `cs614` env and writes `records.jsonl`; `score.py` and `report.py` run in the `cs614-eval` env (ragas 0.4.3) and read only the JSONL files.
* Metrics: RAGAS faithfulness, answer relevancy, context recall/precision and factual correctness, plus custom citation precision/recall/F1 (section-level), numeric accuracy and the guardrail's numerical grounding error rate.
* Usage: `python scripts/rq2/generate.py --systems system_c_v1,system_c_v3 --run-id smoke --limit 3`, then `python scripts/rq2/score.py --run reports/rq2/smoke` and `python scripts/rq2/report.py --run reports/rq2/smoke`. Docker: the `rq2-eval` service (`Dockerfile.eval`, untested).
* Status: smoke run only (`reports/rq2/smoke/`); the full run is pending and the System A / B adapters are stubs.

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
   LLM_PROVIDER=ollama LLM_MODEL=qwen2.5:7b python -m src.system_c.graph --mode v3_aamr_sg --max-hops 2 \
     --query "What was NVIDIA total revenue and operating income in FY2026, and what key Data Center trends drove that performance?"

   # Or using Groq (with GROQ_API_KEY in .env):
   LLM_PROVIDER=groq python -m src.system_c.graph --mode v1_amr --max-hops 3 \
     --query "How did foreign exchange headwinds impact gross margin, and what debt covenants applied?"
   ```
4. **Merge back to `feature/system-c-adaptive-rag` once `pytest` passes:**
   * Always merge into `feature/system-c-adaptive-rag` first (never directly into `feature/rag-baseline` or `main` until we run our joint integration check).
