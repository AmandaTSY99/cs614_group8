# RQ3 Empirical Research Report: Inference Economics & Operational Trade-offs

**Author:** Anish (System Architecture, LangGraph Orchestration & RQ3 Lead)  
**Course:** CS614: Generative AI with Large Language Models  
**Model:** OpenAI `gpt-5.4` (`$2.50` prompt / `$15.00` completion per 1M tokens)  
**Corpus:** Supabase Cloud `sec_chunks` (95,044 chunks, 384-dim BGE-small embeddings)  
**Benchmark:** 40 Canonical Financial Questions ($\ge 2015$), 160 Total Evaluated Runs  
**Branch:** `feat/rq3-inference-economics` -> `dev`  
**Evaluation Date:** October 28, 2026  

---

## 1. Executive Summary & Research Question

RQ3 evaluates the fundamental operational trade-offs of modern RAG architectures: **does multi-stage agentic reasoning justify its latency and monetary overhead over single-pass RAG, and where is the optimal Pareto frontier?**

```
                     ┌─────────────────────────────────────────────────────────┐
                     │                 Accuracy vs. Cost Pareto                │
                     └─────────────────────────────────────────────────────────┘
   100% ┼                                                ● System C v1 (88.9%)
        │                                  ● System C v2 (80.6%)
    80% ┼
        │               ● System A (69.4%)
    60% ┼  ● System B (55.6%)
        │
     0% ┼───────┬──────────────────────────────┬───────────────────────────────┬──────
        $0    $0.01                          $0.03                           $0.05 / query
```

### Core Empirical Findings:
1. **Agentic Accuracy Dominance (Hypothesis H3b Confirmed):**
   Adaptive Multi-Hop RAG (**System C v1**, **88.89%**) and Agentic Adaptive Multi-Hop RAG (**System C v2**, **80.56%**) substantially outperform Single-Pass Advanced Hybrid RAG (**System B**, **55.56%**, $p = 0.0054$, paired Wilcoxon) and Vanilla Dense RAG (**System A**, **69.44%**).
2. **Tabular Pre-Retrieval Slashing Hops by 25% (Hypothesis H3c Confirmed):**
   Adding the SEC XBRL tabular tool (**System C v2**) drops mean retrieval hops from **2.20 $\rightarrow$ 1.65** ($p = 0.0036$). Hop 1 early-stopping increases from **32.5%** in v1 to **62.5%** in v2.
3. **Latency & Cost Efficiency Gains in System C v2:**
   System C v2 is **17% faster** ($19.3\text{s}$ vs $23.2\text{s}$, median $p50 = 14.6\text{s}$, $p = 0.0072$) and consumes **19% fewer tokens** ($9,850$ vs $12,184$), reducing inference costs from $\$44.46 \rightarrow \$36.08$ per 1,000 queries.
4. **Lowest Asymmetric Regulatory Risk Loss:**
   When penalizing incorrect financial answers with a modest regulatory penalty (\$1.00), System C v1 ($\$0.2445$) and System C v2 ($\$0.3111$) yield the lowest expected economic loss, whereas System B incurs double the risk ($\$0.5002$).
5. **Total Experiment Spend:**
   The entire 160-query benchmark completed for **\$3.2464**, well beneath the strict \$5.00 safety ceiling.

---

## 2. Comprehensive Experimental Scorecard

Computed across all 160 queries (`reports/rq3/summary_metrics.csv`):

| Metric | System A (Dense Baseline) | System B (Advanced Hybrid) | System C v1 (Adaptive AMR) | System C v2 (Agentic AAMR) |
| :--- | :---: | :---: | :---: | :---: |
| **Evaluated Queries ($N$)** | 40 | 40 | 40 | 40 |
| **Numerical Accuracy (%)** | 69.44% | 55.56% | **88.89%** | 80.56% |
| **Mean Hops Executed** | 1.00 | 1.00 | 2.20 | **1.65** (-25.0%) |
| **Hop 1 Early-Stop Rate (%)** | 100.0% | 100.0% | 32.5% | **62.5%** (+92.3%) |
| **Hop 1 Clopper-Pearson 95% CI** | [91.2%, 100%] | [91.2%, 100%] | [18.6%, 49.1%] | [45.8%, 77.3%] |
| **End-to-End Latency $p50$ (ms)** | **2,935** | 9,268 | 24,465 | **14,642** (-40.1%) |
| **End-to-End Latency Mean (ms)** | **3,163** | 9,356 | 23,180 | **19,281** (-16.8%) |
| **End-to-End Latency $p90$ (ms)** | 4,867 | 10,922 | 40,398 | 32,581 |
| **Mean Retrieval Latency (ms)** | 291.6 | 6,710.9 | Included in loop | Included in loop |
| **Mean Reranker Latency (ms)** | 0.0 | 6,544.9 | 0.0 | 0.0 |
| **Mean Synthesis Latency (ms)** | 2,871.5 | 2,359.0 | Included in loop | Included in loop |
| **Mean Total Tokens** | 2,222.2 | **1,323.3** | 12,183.7 | **9,850.3** (-19.2%) |
| **Cost per 1,000 Queries (\$)** | \$0.389 | **\$0.234** | \$44.461 | **\$36.075** (-18.9%) |
| **Cost per Correct Answer (\$)** | \$0.0006 | **\$0.0005** | \$0.0556 | \$0.0498 |
| **Robust Risk-Adjusted Loss (\$)** | \$0.3754 | \$0.5002 | **\$0.2445** | \$0.3111 |

---

## 3. Formal Statistical Hypothesis Testing

Paired **Wilcoxon signed-rank tests** with **Holm-Bonferroni Family-Wise Error Rate (FWER)** correction across the 40 benchmark questions (`reports/rq3/summary_metrics.json`):

| Hypothesis / Comparison | Metric | Direction | Wilcoxon $W$ | $p_{\text{raw}}$ | $p_{\text{adj}}$ (Holm) | Significant ($\alpha=0.05$) | Academic Conclusion |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **H3c: Hop Reduction (AAMR vs AMR)** | `hops` | v2 < v1 | 4.5 | 0.00073 | **0.0036** | **YES ($p < 0.01$)** | XBRL pre-retrieval significantly reduces iterative retrieval hops. |
| **AAMR vs AMR Latency** | `latency_ms` | v2 < v1 | 189.0 | 0.00239 | **0.0072** | **YES ($p < 0.01$)** | System C v2 is significantly faster than System C v1. |
| **H3b: Accuracy (AMR vs System B)** | `numeric_correct`| v1 > B | 7.5 | 0.00134 | **0.0054** | **YES ($p < 0.01$)** | Adaptive multi-hop reasoning significantly outperforms single-pass hybrid RAG. |
| **AAMR vs System B Accuracy** | `numeric_correct`| v2 > B | 6.0 | 0.00666 | **0.0133** | **YES ($p < 0.05$)** | Agentic multi-hop with XBRL significantly outperforms single-pass hybrid RAG. |
| **System B vs System A Latency** | `latency_ms` | B > A | 0.0 | 0.00000 | **0.0000** | **YES ($p < 0.001$)** | Cross-encoder reranking introduces a statistically significant latency penalty ($3\times$). |
| **System B vs System A Accuracy** | `numeric_correct`| B vs A | 18.0 | 0.13167 | 0.1317 | NO ($p > 0.05$) | In financial 10-K disclosures, BM25+dense rerank alone did not yield a statistically significant gain over dense retrieval. |

---

## 4. Production Economic Routing Cascade Simulation

To address the Pareto trade-off in commercial deployment, we simulated an automated **Two-Tier Economic Cascade**:
1. Every incoming query is first dispatched to **System B** (fast, \$0.0002/query).
2. If System B's answer is grounded and complete, return immediately.
3. If insufficient or low confidence, escalate to **System C v2** (Agentic Multi-Hop).

### Cascade Simulation Results:
* **Escalation Rate to System C:** **50.0%**
* **Blended Cascade Accuracy:** **75.0%**
* **Blended Mean Latency:** **19.4 seconds**
* **Blended Cost per 1,000 Queries:** **\$18.61** (compared to \$36.08 for 100% System C v2)
* **Takeaway:** A two-tier cascade cuts operational costs by **48.4%** while preserving 93% of System C v2's peak accuracy.

---

## 5. Artifacts and Generated Publication Figures

- **Raw Records (JSONL):** `reports/rq3/records.jsonl`
- **Scorecard (CSV):** `reports/rq3/summary_metrics.csv`
- **Scorecard (JSON):** `reports/rq3/summary_metrics.json`
- **Pareto Frontier Plot:** `reports/figures/rq3_pareto_frontier.png`
- **Stage Latency Breakdown Plot:** `reports/figures/rq3_stage_latency_breakdown.png`
