# CS614 Team Engineering Guide: Unified 4-System RAG Evaluation Harness

**Target Audience:** Team Engineers (Amanda, Aryan, Kevin, Anish) and their AI coding assistants (Claude, GPT, Gemini, Cursor).  
**Branch:** `dev`  
**Purpose:** Single source of truth for connecting to, querying, and evaluating the 4 core financial RAG systems across **RQ1 (Retrieval)**, **RQ2 (Grounding & Citations)**, and **RQ3 (Inference Economics)** without breaking interfaces or leaking ground truth.

---

## 1. Architecture Overview: The 4 Core RAG Systems

All systems are strictly standardized under a uniform adapter interface in `scripts/rq2/adapters.py`.

| System ID | System Name | Architectural Paradigm | LLM Calls | Retrieval Mechanism |
| :--- | :--- | :--- | :---: | :--- |
| **`system_a`** | Vanilla Dense Baseline | Single-pass dense RAG | 1 | Supabase Cloud `sec_chunks` (BGE-small, top-10 chunks) |
| **`system_b`** | Advanced Hybrid Single-Pass | Reciprocal Rank Fusion + Cross-Encoder | 1 | Supabase dense + BM25 keyword fusion + `BAAI/bge-reranker-large` |
| **`system_c_v1`** | Adaptive Multi-Hop RAG (AMR) | Dynamic iterative reflection DAG | 1 to 4 | Query Decomposer $\rightarrow$ 1–3 Hops $\rightarrow$ Sufficiency Critic $\rightarrow$ Guardrail |
| **`system_c_v2`** | Agentic Multi-Hop RAG (AAMR) | Deterministic Tools + Iterative DAG | 1 to 4 | SEC XBRL tabular tool $\rightarrow$ 1–3 Hops $\rightarrow$ Critic $\rightarrow$ Guardrail |

> **⚠️ NOTE FOR ALL AGENTS:** The ablation variant `system_c_fixed_3hop` has been deprecated and excluded from team evaluations. All research questions evaluate exclusively on these **4 core systems**.

---

## 2. Quickstart: 10-Line Python Invocation

Any AI agent or script can query all 4 systems uniformly using the following snippet:

```python
import os
from dotenv import load_dotenv
load_dotenv(override=True)

from scripts.rq2.adapters import get_adapters

# 1. Initialize the 4 systems
adapters = get_adapters(["system_a", "system_b", "system_c_v1", "system_c_v2"])

# 2. Formulate query record
query_payload = {
    "id": "query-001",
    "question": "What was Apple's total revenue in fiscal year 2021?",
    "ticker": "AAPL",
    "target_tickers": ["AAPL"],
    "year": 2021,
    "fiscal_years": [2021]
}

# 3. Execute and inspect outputs
for name, adapter in adapters.items():
    output = adapter.answer(query_payload)
    print(f"[{name}] Answer: {output['answer'][:80]}...")
    print(f"[{name}] Latency: {output['latency_ms']:.0f}ms | Tokens: {output['tokens']['total']}")
```

---

## 3. The Unified Output Schema (`ADAPTER_KEYS`)

Every call to `adapter.answer(payload)` returns a Python dictionary with guaranteed keys:

```python
{
    "answer": str,                  # Final generated answer with citation tags (e.g., "[1]" or "[AAPL FY2021, Item 8, chunk:123]")
    "retrieved_contexts": list[str],# Raw text strings of all retrieved chunks in production order
    "contexts_meta": list[dict],    # Chunk metadata: [{"chunk_id": str, "ticker": str, "fiscal_year": int, "section": str}, ...]
    "citations": list[dict],        # Explicit citation mappings: [{"tag": str, "chunk_id": str, ...}, ...]
    "guardrail_report": dict | None,# System C only: audit report (ungrounded numbers, unsupported sentences, severity score)
    "hops": int,                    # Number of retrieval hops executed (1 for single-pass, 1 to 3 for System C)
    "tokens": {                     # Exact token consumption from provider usage metadata
        "prompt": int,
        "completion": int,
        "total": int
    },
    "cost_usd": float,              # Estimated financial cost in USD using unified pricing
    "latency_ms": float,            # End-to-end wall-clock latency in milliseconds
    "stage_timings_ms": {           # Granular breakdown for ablation & bottleneck analysis
        "retrieval_ms": float,
        "rerank_ms": float,         # System B only
        "agent_critic_ms": float,   # System C only
        "synthesis_ms": float
    },
    "model": str,                   # Model used (e.g., "gpt-5.4")
    "provider": str                 # Provider used (e.g., "openai")
}
```

---

## 4. Benchmark Dataset & Strict Anti-Leakage Firewall

### Canonical Dataset
* **Path:** `data/benchmark_qa_pool_2015.json`
* **Size:** 40 canonical academic questions strictly filtered to fiscal years $\ge 2015$.
* **Schema per question:**
  ```json
  {
    "id": "amanda-001",
    "question": "For Johnson & Johnson's fiscal year 2022...",
    "ticker": "JNJ",
    "year": 2022,
    "recipe": "table",
    "hop": "single",
    "type": "numeric",
    "answer": "-25.64%",
    "program": "subtract(3.9, 2.9)...",
    "key_points": ["accumulated benefit obligation decreased..."],
    "gold_evidence": [{"chunk_id": "JNJ_FY2022_2023-01-01:381", "ticker": "JNJ", "year": 2022, "section": "Item 8"}]
  }
  ```

### 🛑 Anti-Leakage Firewall (Mandatory for All RQs)
To ensure scientific validity, systems must **never** receive ground-truth answers, reasoning programs, or gold evidence chunks. Always use the built-in sanitizer from `scripts/rq3/run_rq3_experiment.py`:

```python
from scripts.rq3/run_rq3_experiment import sanitize_input_for_system

# Strips 'answer', 'program', 'key_points', 'gold_evidence', and quotes
clean_query = sanitize_input_for_system(raw_benchmark_record)
output = adapter.answer(clean_query)
```

---

## 5. How to Evaluate Each Research Question

### For Amanda & Kevin: Evaluating RQ1 (Retrieval & Evidence Sufficiency)
* **Goal:** Evaluate chunk precision, chunk recall, Mean Reciprocal Rank (MRR), and early stopping vs. saturation.
* **Extraction:**
  ```python
  retrieved_ids = [m["chunk_id"] for m in output["contexts_meta"]]
  gold_ids = [e["chunk_id"] for e in raw_record["gold_evidence"]]
  
  hit = any(gid in retrieved_ids for gid in gold_ids)
  precision = len(set(retrieved_ids).intersection(set(gold_ids))) / max(1, len(retrieved_ids))
  recall = len(set(retrieved_ids).intersection(set(gold_ids))) / max(1, len(gold_ids))
  ```
* **Early Stopping Metric:**
  Check `output["hops"]`. For single-hop questions, verify whether System C stopped at Hop 1 or executed redundant hops.

---

### For Aryan: Evaluating RQ2 (Grounding, Faithfulness & Citations)
* **Goal:** Measure numerical correctness, keypoint recall, citation precision, and hallucination rates.
* **Extraction:**
  ```python
  from src.system_a.evaluate import numeric_correct, keypoint_recall

  is_correct = numeric_correct(raw_record["answer"], output["answer"])
  kp_score = keypoint_recall(raw_record.get("key_points", []), output["answer"])
  citations = output["citations"]
  guardrail = output["guardrail_report"] # Check ungrounded_numbers and unsupported_sentences
  ```
* **Automated LLM Judge:**
  Use `scripts/rq2/score.py` or `scripts/rq2/judge.py` to evaluate semantic faithfulness against retrieved contexts.

---

### For Anish: Evaluating RQ3 (Inference Economics & Pareto Frontier)
* **Pre-Built Runner & Evaluator:**
  ```bash
  # Run batch experiment with live spend tracker and $5 budget guardrail
  python scripts/rq3/run_rq3_experiment.py --warmup 1 --max-budget-usd 5.0

  # Compute scorecard, Wilcoxon tests, and publication figures
  python scripts/rq3/evaluate_rq3.py
  ```
* **Outputs:**
  - `reports/rq3/summary_metrics.csv`
  - `reports/rq3/summary_metrics.json`
  - `reports/figures/rq3_pareto_frontier.png`
  - `reports/figures/rq3_stage_latency_breakdown.png`

---

## 6. Environment Setup & Key Configurations

Ensure `.env` in the repository root has the following verified keys:

```dotenv
# Supabase Cloud pgvector connection pooler (Port 5432)
SUPABASE_DB_URL="postgresql://postgres.jfhpjggjoabgpoxwezuc:ue%21K8zrd.%26%26SMub@aws-0-ap-southeast-1.pooler.supabase.com:5432/postgres"

# OpenAI Provider & Model Configuration
LLM_PROVIDER="openai"
LLM_MODEL="gpt-5.4"
OPENAI_API_KEY="sk-proj-..."
SYSTEM_B_API_KEY="sk-proj-..."

# Financial Guardrail Cutoff Ceiling
MAX_BUDGET_USD="5.0"
```

---

## 7. Critical Pitfalls & Resolved Gotchas (Must Read for AIs)

1. **`max_completion_tokens` vs `max_tokens`:**
   OpenAI's newer models (e.g., `gpt-5.4`, `o1`, `o3`) reject requests containing `max_tokens` with HTTP 400. All adapters in `scripts/rq2/adapters.py` and `src/system_*/llm.py` have been patched to pass `max_completion_tokens`. Do **not** revert these parameters to `max_tokens`.

2. **Brotli Decompression on Python 3.13 (`httpx2`):**
   If you encounter `TypeError: process() takes no keyword arguments` in `httpx2/_decoders.py`, it is caused by Google's C-based `brotli` module not accepting `output_buffer_limit`. This has been resolved in the virtual environment via:
   ```python
   self._decompress = lambda data, **kwargs: self.decompressor.process(data)
   ```

3. **Supabase Database Pooler:**
   Always use the pooled connection URL (`aws-0-ap-southeast-1.pooler.supabase.com`) on port 5432. Direct database connections may exceed concurrent connection limits when multi-hop agents launch parallel sub-queries.

4. **Zero Silent Fails (Loud Stops):**
   The benchmark harness runs in `fail_fast=True` mode by default. If any adapter throws an unhandled exception or breaches the budget limit, it dumps a stack trace banner to `stderr` and terminates immediately (`exit(1)`). Do not wrap errors with generic `try...except: pass`.

5. **Streaming Resumability:**
   Results stream line-by-line to `reports/rq3/records.jsonl`. If an experiment process is halted, re-running the script without `--clean` will automatically skip already completed `(system, question_id)` pairs and resume seamlessly.

---

## 8. Summary of Branches & Maintenance
* **Production Core Branch:** `dev`
* **Inference Economics Feature Branch:** `feat/rq3-inference-economics`
* **UI Invariant:** Front-end code in `app.py` must remain completely untouched by CLI evaluation scripts.
