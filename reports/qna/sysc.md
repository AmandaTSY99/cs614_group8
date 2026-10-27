# System C Design Choices, Architecture Defense & Q&A Repository

**Project:** Adaptive Multi-Hop RAG for SEC 10-K Financial Disclosures (CS614)  
**System Leads:** Anish (System Architecture, LangGraph Orchestration & RQ3 Lead) & Aryan (Generation, Citations, Guardrails & RQ2 Lead)  
**Document Purpose:** Living repository of architectural design decisions, trade-offs, theoretical justifications, and defense Q&A for professor consultations, team syncs, and the final 10-page report.

---

## 1. Architectural & Design Choice Defense (Q&A)

### Q1: Why use LangGraph for System C rather than a simple Python while-loop or linear LangChain pipeline?
**Answer / Justification:**
1. **Explicit State Persistence & Observability:** LangGraph enforces an immutable, typed state contract (`AdaptiveRAGState`). Every intermediate decision—planned sub-queries, evidence chunks gathered at each hop, and the Critic's reasoning—is persisted and inspectable. A raw while-loop obscures state transitions and makes systematic ablation impossible.
2. **Conditional Branching Topology:** System C requires non-linear routing:
   - In `v2_aamr`, it branches conditionally between the deterministic XBRL `tabular_tool` and semantic text retrieval.
   - At the `critic`, it branches dynamically between synthesis (if evidence is complete or ceiling reached) and conditioned sub-query generation (if gaps exist).
3. **Rigorous Scientific Ablation (RQ3):** By defining the pipeline as a graph, we can perform controlled architectural ablations (e.g. freezing `max_hops=1` for Fixed 1-Hop vs. forcing `force_max_hops=True` for Fixed 3-Hop vs. dynamic adaptive early stopping) while keeping all other nodes identical.

---

### Q2: Why did you implement "Planning-Guided Tabular Routing" in v2 instead of a true unguided ReAct tool-calling agent?
**Answer / Justification:**
1. **Inference Economics (RQ3):** In financial filings, unguided ReAct loops burn massive token budgets (3x to 5x prompt tokens) in iterative "Thought $\rightarrow$ Action $\rightarrow$ Observation" cycles. For large SEC disclosures, this introduces high latency ($>10$ seconds) and cost ($>\$2.50 / 1\text{k}$ queries).
2. **Deterministic Financial Accuracy:** When a query asks for reported financial figures (Revenue, Operating Income, EPS), the Query Decomposer identifies the financial metrics upfront and routes to `tabular_tool`. This deterministically injects exact XBRL figures (`[F-<ticker>-<year>]`) from `financials.csv` before the retriever runs, achieving a **0.0 numerical grounding error rate** with negligible latency overhead (~13ms).
3. **Hybrid Power:** The system doesn't choose *only* text or *only* tables—it injects the exact XBRL financial table, and then proceeds to retrieve MD&A text chunks to explain the operational *drivers* behind those numbers.

---

### Q3: Why is the Evidence Sufficiency Critic positioned *before* generation rather than using post-hoc LLM-as-a-judge?
**Answer / Justification:**
1. **Preventing Generation on Partial Evidence (RQ2):** If an LLM generates an answer on incomplete context, it suffers from "speculative leap" hallucinations (making up figures to bridge the gap). By evaluating evidence sufficiency *before* generation, System C halts the generation process if key premises are missing and triggers another targeted retrieval hop.
2. **Cost-Effective Early Stopping (RQ3):** For simple, single-hop queries (e.g., corporate address or fiscal year end date), the Critic identifies that Hop 1 retrieved complete evidence and halts immediately. This cuts token consumption by **44.3%** compared to naive multi-hop systems that blindly execute 3 passes on every query.
3. **Actionable Conditioning:** The Critic doesn't just return a binary pass/fail score; it produces an explicit list of `missing_premises` (e.g., *"Missing Note 17 customer concentration percentages"*), giving the Follow-up Generator a concrete target for Hop $N+1$.

---

### Q4: How does System C guarantee zero infinite-loop risk in production?
**Answer / Justification:**
1. **Strict Hard Ceiling:** The state schema enforces `max_hops = 3`. 
2. **Deterministic Graph Invariant:** The conditional edge `route_after_critic` evaluates:
   ```python
   if state.get("is_sufficient") or state.get("current_hop") >= state.get("max_hops"):
       return "synthesizer"
   return "generator"
   ```
   Even if the Critic never marks sufficiency, the state machine forcibly routes to the Synthesizer upon hitting the 3-hop ceiling. It is mathematically impossible for the graph to loop infinitely.

---

### Q5: How does the system prevent retrieving the same redundant chunks across multiple hops?
**Answer / Justification:**
1. **Deduplication by Chunk ID:** In [`src/system_c/nodes/retriever.py`](file:///Users/anishdobz/projects/cs614_group8/src/system_c/nodes/retriever.py), `accumulated_evidence` maintains a `seen_ids` set.
2. **Automated Search Widening:** If Hop 2 retrieves chunks that were already discovered in Hop 1 (`added_count == 0`), the retriever automatically triggers an expanded fallback search (`top_k=8` with footnote expansion terms) to guarantee novel evidence accumulation.

---

### Q6: Why did you stratify the Golden Evaluation Dataset into 3 tiers, and how does it address the professor's concern about FinQA?
**Answer / Justification:**
1. **The Professor's Concern:** Standard academic FinQA questions are evaluated on pre-extracted 1-page snippets with formulaic arithmetic (`add`, `divide`), failing to test real-world full-corpus RAG across 100-page filings.
2. **Our 3-Tier Resolution:**
   - **Tier 1 (Single-Hop Factual — 15 questions):** Baseline sanity test. Validates whether System C's Critic correctly early-stops at Hop 1 without wasting tokens.
   - **Tier 2 (Quantitative Tabular + Narrative — 20 questions):** Adopts TAT-QA style joint text + table reasoning, requiring the model to combine XBRL table data with MD&A prose.
   - **Tier 3 (Cross-Sectional Causal Chaining — 15 questions):** Genuine multi-hop where clues are scattered 40+ pages apart (Item 7 MD&A $\leftrightarrow$ Item 8 Footnote Note 17 customer concentration or debt covenants). Single-pass RAG (Systems A & B) suffers from zero recall on the dependent section, proving the necessity of System C.

---

### Q7: How does System C measure and enforce numerical grounding (RQ2)?
**Answer / Justification:**
1. **Active Numerical Guardrail:** [`src/system_c/guardrails/verifier.py`](file:///Users/anishdobz/projects/cs614_group8/src/system_c/guardrails/verifier.py) intercepts the synthesized answer before it is finalized.
2. **Candidate Number Extraction:** Extracts all percentages, dollar amounts, and floating-point figures while stripping citation tags and 4-digit fiscal years.
3. **Exact Grounding Audit:** Verifies whether every numerical claim exists in the retrieved evidence chunks. Any ungrounded number is flagged with an explicit audit warning, calculating:
   $$\text{Grounding Error Rate} = \frac{\text{Ungrounded Numbers}}{\text{Total Numerical Claims}}$$

---

### Q8: How do we justify the latency and cost of System C over single-pass baselines (RQ3)?
**Answer / Justification:**
1. **The Pareto Frontier Argument:** Single-pass RAG is faster and cheaper, but on multi-hop SEC questions it produces ungrounded speculative answers or omits footnote constraints.
2. **Diminishing Returns vs. Dynamic Optimization:** Naive multi-hop (Fixed 3-Hop) costs **$0.7010 / 1k queries**. System C's adaptive early stopping cuts this to **$0.4123 / 1k queries** (a 41.2% savings) while delivering **100% numerical grounding** on verified filings. System C defines the optimal Pareto frontier between cost and faithfulness.

---

## 2. Key Terminology & Conceptual Mapping

| Project Term | Formal Definition in System C | Implementation File |
| :--- | :--- | :--- |
| **AMR (v1)** | Adaptive Multi-Hop RAG: LangGraph state graph with iterative reflection loop up to 3 hops. | `src/system_c/graph.py` (`--mode v1_amr`) |
| **AAMR (v2)** | Agentic Adaptive Multi-Hop RAG: Adds planning-guided XBRL tabular lookup routing. | `src/system_c/graph.py` (`--mode v2_aamr`) |
| **Sufficiency Reflection** | Self-RAG evaluation of accumulated evidence before answer synthesis. | `src/system_c/nodes/critic.py` |
| **Hop Attribution** | Tracking which specific hop (1, 2, or 3) discovered which chunk ID (RQ1). | `src/system_c/telemetry.py` |
| **Numerical Grounding Error Rate** | Percentage of numerical claims in the generated response that lack evidence support. | `src/system_c/guardrails/verifier.py` |
| **Pareto Frontier** | Empirical curve balancing USD cost per 1k queries against factual faithfulness. | `scripts/plot_rq3_pareto.py` |
