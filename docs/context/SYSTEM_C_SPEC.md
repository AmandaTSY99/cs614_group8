# System C Specification: Adaptive Multi-Hop RAG via LangGraph

## 1. System Overview
System C is an agentic, iterative retrieval-augmented generation pipeline tailored for SEC 10-K financial disclosures. It handles cross-statement, footnoted, and multi-year financial questions that fail under standard single-pass retrieval.

```
                     ┌───────────────────────────────┐
                     │          User Query           │
                     └───────────────┬───────────────┘
                                     │
                                     ▼
                     ┌───────────────────────────────┐
                     │   Query Decomposer & Planner  │  ◄── (LLM Sub-goal planning)
                     └───────────────┬───────────────┘
                                     │
                ┌────────────────────┴────────────────────┐
                ▼                                         ▼
   [Hop 1: Entity / Definition Retrieval]    [Hop 2: Target Metric / Statement Retrieval]
                │                                         │
                └────────────────────┬────────────────────┘
                                     │
                                     ▼
                     ┌───────────────────────────────┐
                     │       Hybrid Retriever        │
                     │  (Dense BGE-m3 + Sparse BM25) │
                     └───────────────┬───────────────┘
                                     │
                                     ▼
                     ┌───────────────────────────────┐
                     │    Cross-Encoder Reranker     │  (e.g., bge-reranker-large)
                     │        Top-5 Chunks           │
                     └───────────────┬───────────────┘
                                     │
                                     ▼
                     ┌───────────────────────────────┐
                     │  Evidence Sufficiency Critic  │  ◄── Evaluates missing premises
                     │     (Self-RAG / Adaptive)     │
                     └───────────────┬───────────────┘
                                     │
                    ┌────────────────┴────────────────┐
          [Gaps Detected & Hop < Max]            [Evidence Sufficient]
                    │                                         │
                    ▼                                         ▼
         ┌─────────────────────┐                   ┌─────────────────────┐
         │ Follow-up Sub-query │                   │ Answer Synthesizer  │
         │     Generator       │                   │ + Precise Citations │
         │ (Conditioned Hop 2) │                   └──────────┬──────────┘
         └──────────┬──────────┘                              │
                    │                                         ▼
                    └───────────► (Loop back)      ┌─────────────────────┐
                                                   │ Faithfulness Guard  │
                                                   │ (Hallucination Cut) │
                                                   └─────────────────────┘
```

---

## 2. State Machine Schema (`AdaptiveRAGState`)

```python
from typing import List, Dict, Any, Optional
from typing_extensions import TypedDict

class EvidenceChunk(TypedDict):
    chunk_id: str
    content: str
    metadata: Dict[str, Any]  # fiscal_year, item_type, company, section, table_id
    relevance_score: float
    hop_retrieved: int

class AdaptiveRAGState(TypedDict):
    original_query: str
    target_ticker: Optional[str]
    fiscal_years: List[str]
    
    # Planning & Decomposition
    sub_queries: List[str]
    current_sub_query: str
    
    # Retrieval Evidence Accumulator
    accumulated_evidence: List[EvidenceChunk]
    intermediate_answers: List[Dict[str, str]]
    
    # Loop Control
    current_hop: int
    max_hops: int
    is_sufficient: bool
    critic_reasoning: str
    
    # Final Output & Telemetry
    final_answer: Optional[str]
    citations: List[Dict[str, Any]]
    telemetry: Dict[str, Any]  # latency_per_node, token_usage, hop_count
```

---

## 3. Node Specifications & Division of Labor

### A. Anish's Module (Core Graph & Orchestration)
1. **`decomposer_node`**:
   - Takes `original_query`.
   - Extracts companies/tickers, fiscal periods, and splits into atomic sub-questions (e.g., Definition / Context $\rightarrow$ Metric retrieval).
2. **`retriever_node`**:
   - Executes dense + sparse retrieval and invokes reranker.
   - Appends deduplicated chunks to `accumulated_evidence`.
3. **`critic_node` (Evidence Sufficiency Critic)**:
   - Evaluates whether current `accumulated_evidence` contains all necessary facts/figures to answer `original_query`.
   - If `sufficient == True` or `current_hop >= max_hops`, routes to synthesis.
   - If `sufficient == False`, routes to `generator_node`.
4. **`telemetry_node` / RQ3 Hooks**:
   - Records latency per hop, prompt tokens, completion tokens, and dollar cost for empirical analysis.

### B. Aryan's Module (Generation, Citations & Guardrails)
1. **`generator_node` (Conditioned Sub-query Generator)**:
   - Takes what was learned in Hop $N$ and formulates a precise, conditioned query for Hop $N+1$ (e.g., targeting a specific footnote or credit agreement discovered in Hop 1).
2. **`synthesizer_node`**:
   - Generates the comprehensive final answer.
3. **`citation_mapper`**:
   - Maps every factual assertion to an exact chunk ID, section, and table row.
4. **`guardrail_node` (Faithfulness & Hallucination Defense)**:
   - Re-checks every generated dollar value and metric against the cited text. Drops or flags ungrounded claims.

---

## 4. Empirical Evaluation & RQ3 Ablation Benchmark Findings

*Evaluated on the 60-Question SEC 10-K Golden Benchmark Set (`data/golden_eval_set.json`). Full report and raw logs at [`docs/system-c/EVAL_FINDINGS.md`](../system-c/EVAL_FINDINGS.md) and [`reports/eval_runs/20261024_1720/`](../../reports/eval_runs/20261024_1720/).*

### Performance Summary Table

| Architectural Condition | Mean Hops | Early-Stop % | Latency (p50) | Latency (p90) | Mean Total Tokens | Cost / 1k Queries | Grounding Error Rate |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Fixed 1-Hop Baseline** | 1.00 | 0.0% | 31.9 ms | 259.4 ms | 3,010 | **\$0.3375** | 0.000 |
| **Fixed 3-Hop Exhaustive** | 3.00 | 0.0% | 58.4 ms | 127.0 ms | 8,219 | **\$0.8880** | 0.000 |
| **Adaptive Multi-Hop (AMR v1)** | **1.47** | **100.0%** | **22.0 ms** | **51.1 ms** | **4,604** | **\$0.5028** | 0.000 |
| **Agentic Adaptive (AAMR v2)** | **1.10** | **100.0%** | **88.97 ms** | **196.1 ms** | **3,426** | **\$0.3767** | 0.000 |

### Key Takeaways
1. **Adaptive AMR (v1)** reduces token costs by **~43.4%** compared to Fixed 3-Hop (\$0.5028 vs. \$0.8880 / 1k queries) by halting 53.3% of queries at Hop 1 as soon as factual sufficiency is verified.
2. **Agentic AAMR (v2)** converges in **1.10 mean hops** with near 1-hop pricing (\$0.3767 / 1k queries) by deterministically retrieving XBRL financial table metrics (`financials.csv` / Supabase SQL) in 1 hop.
3. **Pipeline Bugfixes**: Resolved retriever substring false-positives (`state in statements`) and LLM critic sentinel strings (`"missing_entities": ["None"]`) that previously caused simple factual queries to exhaust all hops.

