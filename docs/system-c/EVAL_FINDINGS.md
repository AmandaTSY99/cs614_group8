# System C Evaluation Findings & Ablation Benchmark (RQ3)

**Document Status**: Official Milestone Report  
**Benchmark Suite**: 60-Question SEC 10-K Golden Evaluation Set (`data/golden_eval_set.json`)  
**Evaluation Date**: 2026-10-24  
**Run Artifacts Folder**: `reports/eval_runs/20261024_1720/`  

---

## 1. Executive Summary & Benchmark Results

This evaluation assesses the inference economics, latency profile, hop distribution, and factual grounding fidelity of System C across four distinct architectural configurations over the 60 curated SEC 10-K golden benchmark queries:

1. **Fixed 1-Hop Baseline**: Standard single-pass dense/sparse retrieval without follow-up iterative loops.
2. **Fixed 3-Hop Exhaustive**: Multi-hop pipeline running through 3 search iterations unconditionally without early stopping.
3. **Adaptive Multi-Hop (AMR v1)**: Self-RAG loop guided by the Evidence Sufficiency Critic that halts as soon as factual premises are satisfied.
4. **Agentic Adaptive (AAMR v2)**: Autonomous agentic routing integrating deterministic XBRL tabular querying (`[F-TICKER-YEAR]`) alongside text chunk retrieval.

### Performance Summary Table

| Architectural Condition | Mean Hops | Early-Stop % | Latency (p50) | Latency (p90) | Mean Total Tokens | Cost / 1k Queries | Grounding Error Rate | Faithfulness Score |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Fixed 1-Hop Baseline** | 1.00 | 0.0% | 31.9 ms | 259.4 ms | 3,010 | **\$0.3375** | 0.000 | 1.000 |
| **Fixed 3-Hop Exhaustive** | 3.00 | 0.0% | 58.4 ms | 127.0 ms | 8,219 | **\$0.8880** | 0.000 | 1.000 |
| **Adaptive Multi-Hop (AMR v1)** | **1.47** | **100.0%** | **22.0 ms** | **51.1 ms** | **4,604** | **\$0.5028** | 0.000 | 1.000 |
| **Agentic Adaptive (AAMR v2)** | **1.10** | **100.0%** | **88.97 ms** | **196.1 ms** | **3,426** | **\$0.3767** | 0.000 | 1.000 |

*Raw data stored at: [`docs/system-c/rq3_ablation_metrics.csv`](rq3_ablation_metrics.csv) and [`reports/eval_runs/20261024_1720/rq3_ablation_metrics.csv`](../../reports/eval_runs/20261024_1720/rq3_ablation_metrics.csv)*

---

## 2. Key Empirical Findings (RQ3 Research Questions)

### A. Inference Economics & Token Savings
- **~44% Cost Reduction via Adaptive Early Stopping**:
  - Fixed 3-Hop incurs \$0.8880 per 1,000 queries.
  - Adaptive AMR (v1) achieves **\$0.5028 per 1,000 queries**, reducing inference expenditure by 43.4% because single-hop and cover-page queries halt at Hop 1 (32 out of 60 queries early stopped at Hop 1; 28 required Hop 2; 0 exceeded Hop 2).
- **Tabular Agentic Routing (AAMR v2)**:
  - Agentic AAMR achieves near 1-hop expenditure (**\$0.3767 per 1,000 queries**) because quantitative questions (e.g. revenue, net income, R&D spend) are resolved deterministically via the XBRL tabular tool in 1 hop, bypassing multiple text chunk retrieval cycles.

### B. Latency Distribution
- **AMR v1 achieves the lowest median latency (22.0 ms p50)**:
  - By pruning unnecessary downstream generator, retriever, and cross-encoder calls once evidence is satisfied, median response time is faster than both Fixed 1-Hop (which processes full candidate chunks) and Fixed 3-Hop.
- **AAMR v2 latency (88.97 ms p50)** reflects the deterministic SQL/CSV table parsing step, which trades minor compute overhead for 100% numerical verification.

### C. Hop Attribution & Distribution
- **Fixed 1-Hop**: 60 queries at Hop 1 (100%).
- **Fixed 3-Hop**: 60 queries at Hop 3 (100%).
- **Adaptive AMR v1**: 
  - Hop 1: 32 queries (53.3%) — simple lookups, definitions, cover page metadata.
  - Hop 2: 28 queries (46.7%) — cross-statement footnotes, revenue segment breakdowns, credit covenants.
  - Hop 3: 0 queries (0.0%).
- **Agentic AAMR v2**:
  - Hop 1: 54 queries (90.0%) — direct XBRL tabular lookups + single-hop context.
  - Hop 2: 6 queries (10.0%) — complex multi-entity footnote synthesis.

---

## 3. Root Cause Analysis: The 4-Hop Runaway Trap & Bugfixes

During testing on Streamlit Cloud, queries consistently consumed all 4 hops even when answering simple factual questions. Investigation uncovered two compounding bugs in the retrieval and evaluation pipeline:

### 1. Retriever Substring False-Positive Trap (`retriever.py`)
- **Root Cause**: `_bm25_and_lexical_score` performed naive substring inclusion (`t in t_lower`).
- **Failure Mode**: For a query such as *"state of incorporation"*, the token `"state"` matched `"statements"` inside Item 8 *"Consolidated Statements of Operations"* dozens of times. The artificial term frequency gave financial statement chunks a high score (6.2+), burying the actual 1-page Cover Page metadata chunk containing the state and executive office address.
- **Resolution**: Replaced substring checking with whole-word regex tokenization (`re.findall(r'\b[a-z0-9]+\b')`), n-gram phrase matching (`"state of incorporation"` boost), and stopword filtering (`"what"`, `"was"`, `"where"`).

### 2. Critic Sentinel String Trap (`critic.py`)
- **Root Cause**: When the Critic LLM evaluated evidence and found no missing entities, it returned structured JSON with `"missing_entities": ["None"]` or `["N/A"]`.
- **Failure Mode**: In Python, `bool(["None"]) == True` (non-empty list of length 1). Line 198 evaluated `if score >= threshold and not missing_entities:`. The presence of `"None"` caused `not missing_entities` to evaluate to `False`, permanently suppressing `is_sufficient = True` until `max_hops` was reached.
- **Resolution**: Sanitized lists against sentinel tokens (`{"none", "n/a", "na", "null", "nothing", "[]"}`) and added explicit certification checks.

### 3. UI Disambiguation (`app.py`)
- Replaced ambiguous metric copy `Early Stopped: False` with `Stop Reason: Early Stopped (Hop X)` or `Max Hops Reached (X/X)`.
- Increased `max_hops` slider ceiling from 4 to 10.

---

## 4. Visualizations & Publication Figures

The following Pareto and latency breakdown charts were generated during the benchmark and are stored in `reports/eval_runs/20261024_1720/figures/`:

1. **`rq3_pareto_frontier.png`**: Compares Cost per 1,000 queries vs. Faithfulness and Latency across the 4 conditions.
2. **`rq3_hop_distribution.png`**: Stacked bar chart showing hop counts (Hop 1 vs. Hop 2 vs. Hop 3).
3. **`rq3_latency_breakdown.png`**: Box-and-whisker latency percentiles (p50, p90, p99).
4. **`rq3_executive_dashboard.png`**: 4-panel comprehensive publication dashboard.
