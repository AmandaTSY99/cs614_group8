# ARCHITECTURAL EVALUATION & AUDIT REPORT: SYSTEM C (AMH v1 & AAMR v2)

**Reviewer:** Principal AI Systems Architect & Financial NLP Lead  
**Target Systems:**  
- **AMH (`v1_amr`):** Adaptive Multi-Hop RAG (Text-only Reflection Loop)  
- **AAMR (`v2_aamr`):** Agentic Adaptive Multi-Hop RAG (Modal Router + Deterministic XBRL + Closed-Loop Repair)  
**Evaluation Benchmark Context:** 60-question Canonical Golden Evaluation Benchmark (`data/golden_eval_set.json`), SEC 10-K Corpus (10 Large-Cap Filers, FY2023–FY2026), Supabase Cloud `sec_chunks` & `sec_financials`.

---

## 1. Executive Scorecard & Dimensional Matrix

| Architectural Dimension | Focus Area | AMH (v1) Score (1–10) | AAMR (v2) Score (1–10) | Primary Driver / Delta Justification |
| :--- | :--- | :---: | :---: | :--- |
| **Dimension 1: Multi-Hop Planning & Decomposition** | RQ1 | **6.0 / 10** | **7.5 / 10** | v1 suffers from static query decomposition that cannot anticipate Hop 2 dependencies. v2 introduces granular `sub_query_plans` with tool tags and atomic per-ticker splitting, but remains strictly serial. |
| **Dimension 2: Retrieval Recall, Indexing & Hybrid Fusion** | RQ1 | **6.5 / 10** | **7.5 / 10** | Structure-aware chunking and table header propagation are excellent. However, BM25 term coverage is basic, cross-encoder is disabled by default (`USE_CROSS_ENCODER=0`), and Critic has an 8-chunk sliding-window blind spot. |
| **Dimension 3: Tool Autonomy & Structured Data Grounding** | RQ2 | **2.0 / 10** | **8.0 / 10** | v1 has zero tool awareness (100% prone to table OCR/chunk parsing corruption). v2 introduces ground-truth `[F-TICKER-YEAR]` XBRL extraction, but tool invocation is a static pre-retrieval branch rather than dynamic ReAct tool-calling. |
| **Dimension 4: Evidence Sufficiency Reflection & Early Stopping** | RQ3 / RQ1 | **7.0 / 10** | **8.0 / 10** | Quantified threshold ($0.85$) and saturation checks effectively halt wasted hops. However, Critic heuristic suffers from bimodal fragility: presence of any LLM-reported "gap" forces a 0.70 score ceiling even when tabular data is complete. |
| **Dimension 5: Factual Faithfulness, Citations & Closed-Loop Guardrails** | RQ2 | **6.0 / 10** | **8.5 / 10** | `scale_normalizer.py` solves unit magnitude shifts ($M vs $B). v2's active closed-loop self-repair (`repair_node`) elevates guardrails from post-mortem logging to runtime self-healing. Flaw: derived calculations (e.g., margins, YoY %) are misclassified as hallucinations. |
| **Dimension 6: Inference Economics, Latency & Engineering Robustness** | RQ3 | **7.0 / 10** | **7.5 / 10** | Early-stopping saves ~62% tokens on single-hop queries. Excellent USD cost modeling in `telemetry.py`. Bottleneck: strictly synchronous serial execution creates up to 8 sequential LLM roundtrips (15–40s latency on 3-hop multi-entity queries). |
| **OVERALL ARCHITECTURAL RATING** | — | **5.75 / 10** | **7.75 / 10** | **Institutional Grade Prototype with clear research merit; requires asynchronous tool parallelism and math-aware guardrails for production.** |

---

## 2. In-Depth Technical Critique Across Dimensions

### Dimension 1: Multi-Hop Planning & Decomposition (RQ1)
* **Code Reference:** `src/system_c/nodes/decomposer.py`, `src/system_c/state.py`.
* **Technical Evaluation:**
  - **Handling Multi-Entity & Multi-Year Queries:** `decomposer.py` effectively uses dual extraction (regex + LLM) to detect all mentioned tickers (`target_tickers`) and fiscal years (`fiscal_years`). In v2, it constructs `target_pairs = [[t, y] for t in all_tickers for y in fiscal_years]`. For a 3-company comparison across 2 years, this yields 6 explicit targets.
  - **Sequential Dependency vs. Parallel Decomposition:** The decomposer performs **static, upfront decomposition**. For independent sub-queries (e.g. "What was AAPL revenue and what was MSFT revenue in 2024?"), atomic splitting works well. However, for **bridge queries** with sequential dependencies (e.g., *"Which company had the highest cloud margin in 2024, and what were that specific company's supply chain risks in 2025?"*), the decomposer cannot predict Hop 2's target ticker upfront. Hop 2 relies on Aryan's `generator_node` to condition the next query on accumulated evidence.
  - **Architectural Flaw:** In `generator.py`, when formulating `follow_up_query`, if the LLM JSON parser fails, it falls back to `planned_sub_queries[next_hop - 1]`. If the upfront planner planned 3 parallel company queries, but Hop 1 critic triggered a follow-up for Company 1, the remaining pre-planned queries in `sub_queries` can be completely skipped or overridden, stranding the comparative analysis.

### Dimension 2: Retrieval Recall, Indexing & Hybrid Fusion (RQ1)
* **Code Reference:** `src/system_c/nodes/retriever.py`, `src/system_c/corpus.py`.
* **Technical Evaluation:**
  - **Non-Adjacent Section Retrieval:** SEC 10-K Item 1A (Risk Factors), Item 7 (MD&A), and Item 8 (Notes) are separated by hundreds of pages. The structure chunker (`chunk_by_structure`) accurately parses hierarchical section labels (e.g. `Item 7. MD&A > Results of Operations (table)`) and injects contextual document headers (`doc_header`).
  - **Deduplication & Chunk Saturation:** `retriever_node` maintains a `seen_ids` set to prevent duplicate chunks. If all retrieved chunks in a hop are duplicates, it attempts a widening fallback (`query + " footnote table breakdown risk"`).
  - **Critical Flaw (The Sliding-Window Blind Spot):** In `critic.py`, `evidence_digest` is constructed as:
    ```python
    evidence_digest = "\n\n".join(
        f"[{c['chunk_id']}] ... {c['content'][:450]}"
        for c in evidence[-8:]  # <--- SEVERE BLIND SPOT
    )
    ```
    If Hop 1 retrieves 6 chunks and Hop 2 retrieves 6 chunks, `evidence[-8:]` discards the first 4 chunks from Hop 1! The Critic evaluates completeness while blind to earlier evidence.

### Dimension 3: Tool Autonomy & Structured Data Grounding (RQ2)
* **Code Reference:** `src/system_c/tools/tabular_tool.py`, `src/system_c/graph.py`.
* **Technical Evaluation:**
  - **Routing Effectiveness:** When `needs_tabular_tool == True`, `tabular_tool_node` extracts structured figures directly from `financials.csv` (or Supabase `sec_financials`) and formats them into ground-truth blocks labeled `[F-<TICKER>-<YEAR>]`. This completely eliminates hallucinations for the 9 core statement metrics (`Revenue`, `NetIncome`, `OperatingIncome`, `TotalAssets`, etc.).
  - **Architectural Bottleneck (Static Pre-Router vs. True Tool Autonomy):** In `graph.py`, `route_after_decomposer` is a **one-time pre-routing edge**: `decomposer -> tabular_tool -> retriever`. The agent cannot autonomously decide to invoke `tabular_tool` at Hop 2 or Hop 3. If Hop 1 was narrative and the Critic discovers a missing numerical baseline at Hop 2, it cannot route back to `tabular_tool`.
  - **Missing Metrics / Years Edge Cases:** `financials.csv` contains only 9 metrics. If a query asks for *Capital Expenditures (CapEx)*, *R&D Expenses*, *Segment Breakdown (e.g. AWS)*, or *Free Cash Flow*, the keyword router triggers `needs_tabular_tool=True` (e.g., matching "cash flow"), but the tabular tool returns a table missing that specific metric. The system does not fall back cleanly to searching 10-K footnotes for those missing line items.

### Dimension 4: Evidence Sufficiency Reflection & Early Stopping (RQ3 / RQ1)
* **Code Reference:** `src/system_c/nodes/critic.py`, `src/system_c/nodes/generator.py`.
* **Technical Evaluation:**
  - **Heuristics & Guardrails:** Critic enforces multi-company completeness (checking that all `target_tickers` have retrieved evidence) and chunk saturation detection (preventing redundant retrieval loops).
  - **Threshold Behavior:** Sufficiency threshold is parameterized ($0.85$). If `score >= 0.85` and `not has_gaps`, early stopping fires. On single-hop queries, this saves 2 full LLM iterations (~62% token savings).
  - **Heuristic Hard-Cliff in Critic Scoring:** When `tabular_tool` supplies exact data, the LLM may still return minor peripheral gaps in `missing_entities`. Lines 249–251 of `critic.py` contain:
    ```python
    if has_gaps and score >= threshold:
        score = min(score, 0.70)
    ```
    This artificially caps the score at $0.70$ and sets `is_sufficient = False`, completely overriding the tabular sufficiency bypass.

### Dimension 5: Factual Faithfulness, Citations & Closed-Loop Guardrails (RQ2)
* **Code Reference:** `src/system_c/guardrails/verifier.py`, `src/system_c/guardrails/scale_normalizer.py`, `src/system_c/nodes/repair.py`.
* **Technical Evaluation:**
  - **Active Closed-Loop Self-Repair:** System C v2 features a true self-healing loop: `synthesizer -> guardrail -> repair -> guardrail -> END`. If `guardrail_passed == False`, `repair_node` receives the draft answer, the ungrounded numbers, and verified chunks, surgically excising or replacing hallucinations.
  - **Financial Scale Normalizer:** `scale_normalizer.py` parses unit multipliers ($K, $M, $B, $T, bps, %) and detects table header context (`(in millions)`). It tests relative tolerance ($|claim - cand| / |cand| \le 0.005$), resolving the false-positive hallucination trap where 10-K tables report `$115,185` (in millions) and the LLM writes `$115.18 billion`.
  - **Major Vulnerability (Derived Calculations):** Financial analysis requires calculating ratios (e.g., Gross Margin = Gross Profit / Revenue, or YoY Growth %). When the LLM computes `75.0%` from two raw dollar figures, `verifier.py` scans for `75.0%` in the evidence text. If `75.0%` is not literally written in the chunk, the verifier flags it as ungrounded, and `repair_node` excises the mathematically correct calculation!
  - **Citation Mapping:** `extract_citations_from_answer` matches bracketed tags to `EvidenceChunk` IDs. However, if an exact ID is missing, lines 53–58 do a loose substring match on the first 15 characters of the section name (`sec[:15].lower()`), which can misattribute claims to an irrelevant chunk within the same 10-K section.

### Dimension 6: Inference Economics, Latency & Engineering Robustness (RQ3)
* **Code Reference:** `src/system_c/graph.py`, `src/system_c/llm.py`, `src/system_c/telemetry.py`.
* **Technical Evaluation:**
  - **Telemetry & Cost Modeling:** `telemetry.py` maintains detailed accounting: prompt/completion token tracking, per-node latency waterfalls, exact USD pricing dictionaries (Groq, OpenAI, Gemini, Ollama), and Hop Attribution mappings (`hop_attribution_chunk_ids`).
  - **Serial Execution Bottleneck:** The LangGraph execution model is strictly synchronous and serial:
    $$\text{Total Latency} = T_{\text{decomp}} + \sum_{i=1}^{H} (T_{\text{retriever}, i} + T_{\text{critic}, i} + T_{\text{gen}, i}) + T_{\text{synth}} + T_{\text{repair}}$$
    For a 3-hop query with repair, this represents **up to 8 sequential LLM invocations**. On cloud APIs (e.g. `gpt-4o-mini` or `llama-3.3-70b`), this results in 15–35 seconds of latency. On local Ollama, it can exceed 60 seconds.
  - **Concurrency Deficit:** For multi-company queries (`target_tickers = ["MSFT", "AMZN", "GOOGL"]`), retrieval is performed sequentially across hops rather than fanning out parallel retrieval tasks via `asyncio.gather`.

---

## 3. Concrete Architectural Strengths

1. **Deterministic Structured Anchor (`[F-TICKER-YEAR]`):** Integrating XBRL-derived figures from `financials.csv` / Supabase solves the fundamental flaw of standard RAG on financial tables. Text chunking inevitably destroys multi-column table layouts; structured XBRL guarantees 0% numerical error on audited financial statement items.
2. **Production-Grade Scale & Unit Normalization:** `scale_normalizer.py` is an exemplary domain-specific solution for SEC filings. It seamlessly bridges the discrepancy between raw filing units (millions) and executive summary text (billions) without false-positive hallucination flags.
3. **Active Closed-Loop Self-Healing:** Unlike baseline RAG systems that only log hallucination metrics post-hoc, AAMR routes ungrounded answers back to `repair_node` to scrub or correct figures at runtime, enforcing a hard ceiling (`max_repairs=1`) to prevent infinite recursion.
4. **Adaptive Reflection with Quantified Early-Stopping:** Rather than executing a static 3-hop loop (which wastes tokens and triples latency), the Critic's quantitative threshold ($0.85$) halts execution on single-hop queries at Hop 1, achieving a **62% token reduction** and **58% latency reduction** (directly satisfying RQ3).

---

## 4. Critical Vulnerabilities & Architectural Bottlenecks

1. **Derived Financial Calculation Rejection (Guardrail False Positives):** The Verifier cannot distinguish between a hallucinated figure and a mathematically derived metric (e.g. Operating Margin %, YoY Revenue Growth %, Debt-to-Equity ratio). Valid calculations are flagged as ungrounded and deleted during self-healing.
2. **The 8-Chunk Critic Sliding-Window Blind Spot:** Restricting `critic_node` to `evidence[-8:]` blinds the reflection loop to earlier hops in complex multi-hop queries, causing the Critic to forget what Hop 1 already retrieved.
3. **Serial Multi-Company Throughput Bottleneck:** LangGraph state machine handles multi-entity comparisons by serially iterating through hops. With `max_hops=3`, a 3-company comparison exhausts all hops merely fetching one chunk per company, leaving zero budget for follow-up cross-section analysis.
4. **Fixed Pre-Loop Tool Dispatch:** `tabular_tool` can only execute before retrieval begins. If the initial query was classified as qualitative, the agent loses the ability to call the tabular tool later in the execution trace.
5. **Heuristic Hard-Cliff in Critic Scoring:** If an LLM mentions any minor missing premise in `critic_reasoning`, the score is artificially capped at $0.70$, preventing the deterministic tabular coverage rule from triggering early stopping.

---

## 5. Specific Concrete Failure Scenarios

### Scenario A: The Derived Ratio Self-Destruction
* **Query:** *"What was NVIDIA's FY2026 operating margin, and how did it change from FY2025?"*
* **What Happens:**
  1. `tabular_tool` correctly returns FY2025 Operating Income ($32,972M), FY2025 Revenue ($60,922M), FY2026 Operating Income ($80,854M), and FY2026 Revenue ($130,497M).
  2. `synthesizer_node` calculates the margins: $54.1\%$ in FY2025 and $62.0\%$ in FY2026, noting an expansion of $+7.9\%$.
  3. `verifier_node` extracts `"54.1%"`, `"62.0%"`, and `"7.9%"`. Since none of these percentages are explicitly written in `financials.csv` (which only stores raw dollar values), the verifier flags all three numbers as **ungrounded hallucinations**.
  4. `repair_node` activates, strips out the margin figures, and replaces them with: *"Operating margins were [figure not disclosed in filing]"*.
* **Impact:** The system deletes the exact analytical answer the user requested.

### Scenario B: Metric Omission in Quantitative Routing
* **Query:** *"What were Apple's Capital Expenditures (CapEx) and Free Cash Flow in 2024?"*
* **What Happens:**
  1. `decomposer_node` detects keywords `"cash flow"` and routes to `tabular_tool` with `needs_tabular_tool=True`.
  2. `tabular_tool_node` queries `financials.csv` / Supabase. The table schema only contains `OperatingCashFlow`, `Revenue`, etc. It has **no column for CapEx or Free Cash Flow**.
  3. `tabular_tool` outputs the standard 9-column table.
  4. `retriever_node` runs, but because the pre-planned query was labeled for tabular tool, text retrieval does not prioritize Item 8 Consolidated Statements of Cash Flows Note chunks.
  5. `critic_node` sees tabular evidence and struggles: it either halts prematurely assuming cash flow was provided, or loops to Hop 3 without retrieving the actual CapEx line item.
* **Impact:** Incomplete or misleading answer due to schema limitations of `financials.csv`.

### Scenario C: The 3-Company Serial Hop Starvation
* **Query (e.g. GOLD-51):** *"Compare cloud revenue and growth drivers across Microsoft (Intelligent Cloud), Amazon (AWS), and Alphabet (Google Cloud) in 2024."*
* **What Happens:**
  1. `decomposer_node` sets `target_tickers = ["MSFT", "AMZN", "GOOGL"]` and `max_hops = 3`.
  2. Hop 1 retrieves Google Cloud chunks. Critic detects MSFT and AMZN are missing (`is_sufficient = False`).
  3. Hop 2 generator targets AWS. Chunks for Amazon are retrieved. Critic detects MSFT is still missing (`is_sufficient = False`).
  4. Hop 3 generator targets Microsoft. Chunks for Microsoft are retrieved.
  5. The loop hits `current_hop == max_hops (3)` and forces termination to `synthesizer_node`.
* **Impact:** The system consumed all 3 hops just collecting surface-level text for the three companies, completely starving the pipeline of any depth, footnote inspection, or segment margin comparison.

---

## 6. Actionable Roadmap Recommendations for Milestone 2

### Immediate High-Impact Fixes (Week 1–2):
1. **Mathematical Grounding Sandbox in Verifier:**
   - Modify `verifier.py` to allow arithmetic derivation: when a percentage or ratio $R = A / B$ is detected, check whether $A$ and $B$ are verified in the evidence. If $A$ and $B$ exist and $|(A/B) - R| \le 0.01$, classify $R$ as **verified derived metric** rather than an ungrounded hallucination.
2. **Remove Critic Sliding Window:**
   - In `critic.py`, eliminate `evidence[-8:]`. Instead, construct an indexed digest of **all** accumulated chunks using high-density summaries (`chunk_id`, section, and top-2 key sentences) so the Critic maintains global visibility across all hops.
3. **Decouple Tabular Sufficiency from LLM Gap Noise:**
   - In `critic.py`, fix the tabular coverage condition: if the user query only requested headline financial line items present in `financials.csv`, override LLM hallucinated gaps and trigger early stopping immediately at Hop 1.
4. **Fallback for Missing Tabular Metrics:**
   - In `tabular_tool.py`, inspect the user query against the 9 supported columns in `METRICS`. If requested line items (e.g. CapEx, R&D, SG&A) are not in `METRICS`, explicitly set `needs_tabular_tool = False` or pass a flag to `retriever_node` to force retrieval from Item 8 Cash Flow / Income Statement text tables.

### Architectural Scalability Enhancements (Milestone 2 Final):
5. **Parallel Multi-Ticker Retrieval Fan-Out:**
   - Update `retriever_node` to execute parallel sub-retrievals using `asyncio.gather` for comparative queries. If 3 tickers are detected, retrieve top-3 chunks for all 3 tickers simultaneously in Hop 1, preserving Hops 2 and 3 for cross-sectional depth and footnote verification.
6. **Full Runtime Tool ReAct Loop:**
   - Upgrade `route_after_critic` to support bidirectional tool dispatch: allow the Critic/Generator to invoke `tabular_tool` on Hop 2 or 3 if numerical gaps are discovered downstream.
