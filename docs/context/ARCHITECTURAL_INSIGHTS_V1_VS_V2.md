# Architectural Insights & Trade-Offs: System C v1 (AMR) vs. System C v2 (AAMR)

**Module:** System C Core Architecture & Evaluation  
**Benchmark:** 97 Canonical Financial Questions ($\ge$ FY2015)  
**Evaluation Scope:** 388 Total Precomputed Runs across Systems A, B, C v1, C v2  
**Date Added:** October 30, 2026  

---

## 1. The Core Empirical Finding

Across the 97-question benchmark:
* **System C v1 (Adaptive Multi-Hop RAG):** Achieves **89.66% numerical accuracy**, with a mean of **2.24 hops**, median latency of **21.4 seconds**, and **$45.39** cost per 1,000 queries.
* **System C v2 (Agentic Adaptive Multi-Hop RAG):** Achieves **82.76% numerical accuracy**, with a mean of **1.77 hops** (-21%), median latency of **13.6 seconds** (-36.7%), and **$39.10** cost per 1,000 queries (-13.8%).
* **Hop 1 Early-Stopping Rate:** Jumps from **28.87%** in v1 to **54.64%** in v2 ($p < 0.0001$, paired Wilcoxon $W=21.0$).

---

## 2. Critical Insight A: The 10-K "Lookback Barrier" (Why v2 Crushes Macro Time-Series)

### The Domain Constraint:
Under SEC Form 10-K reporting regulations, a company's Consolidated Balance Sheet only reports comparative figures for the **current fiscal year and the immediately preceding fiscal year** (or at most two prior years).
* Example (`gold-066`): *"By how many million dollars did Tesla's total assets increase from fiscal year 2021 to fiscal year 2025?"*
* Ground truth: **$75,675 million** ($137,806M in FY25 $-$ $62,131M in FY21).

### Failure of Pure Textual RAG (System C v1):
* In Tesla's FY2025 10-K, the balance sheet only reports FY2025 and FY2024.
* FY2021 figures reside solely in the FY2021 10-K filing from four years earlier.
* System C v1's multi-hop text retrieval focused on the FY2025 filing chunks. Even after executing all 3 allowed hops (taking 22.1 seconds), it failed to retrieve the 2021 balance sheet chunk, reporting: *"The filing does not disclose Tesla’s total assets for fiscal year 2021 in the provided evidence..."*

### Triumph of Agentic Tabular Pre-Retrieval (System C v2):
* The Query Decomposer identified the multi-year quantitative metric and triggered `tabular_tool_node` before Hop 1.
* The tabular tool queried the structured XBRL database (`financials.csv` / Supabase `sec_financials`), which maintains continuous multi-year financial statement time-series spanning all years.
* System C v2 extracted both figures and synthesized the exact answer in **1 single hop** (8.4 seconds), yielding a **62% latency reduction and 50% cost reduction**.

---

## 3. Critical Insight B: The "Premature Stopping" Trade-off on Footnotes (Why v1 Won on 9 Questions)

### The Mechanism:
In 9 out of 97 benchmark questions (`gold-089`, `gold-014`, `gold-091`, `gold-003`, `gold-031`, `gold-037`, `gold-073`, `gold-006`, `gold-010`), System C v1 answered correctly while System C v2 failed.

Every single one of these 9 questions required **granular line-item footnotes** rather than macro statement totals:
* `gold-037`: NVIDIA Tegra Processor segment revenue (Item 8 Note 17).
* `gold-006`: Amazon scheduled principal debt repayments due after 2021 (Item 8 Note 7 Debt Schedule).
* `gold-031`: Alphabet gains/losses from non-hedging FX forward contracts (Item 8 Note 4 Derivatives).
* `gold-003`: Microsoft long-lived assets in Finland (Item 8 Note 20 Geographic Information).

### The Root Cause:
1. In System C v2, `tabular_tool_node` injected macro financial statements (`[F-...]`) before Hop 1.
2. In Hop 1, the **Evidence Sufficiency Critic** saw high-level financial tables already present in `accumulated_evidence`.
3. The Critic was **tricked into premature sufficiency**: it believed the financial figures were already retrieved, terminating the graph at Hop 1!
4. Consequently, System C v2 never executed Hop 2 or Hop 3 to fetch the granular footnote text chunks.
5. In contrast, **System C v1 had no tabular shortcut**. Because it had no summary table, the Critic accurately judged evidence as insufficient at Hop 1, forcing the state machine into Hops 2 and 3, which successfully retrieved the exact footnote tables.

---

## 4. Architectural Work Needed / Action Items

To achieve the best of both worlds (combining v2's 37% speedup with v1's 89.7% peak accuracy):
1. **Granularity-Aware Critic Prompting:** Update `critic_node` so that if a question asks for a specific *segment*, *footnote*, *covenant*, or *sub-schedule*, macro XBRL blocks (`[F-...]`) are explicitly marked as insufficient to satisfy granular segment premises.
2. **Dynamic Tool Re-Invocation:** Allow `generator_node` in Hop 2 to re-invoke the tabular tool if a new entity or year is discovered during multi-hop reasoning.
3. **Hybrid Routing Cascade:** In production, route macro balance sheet/income statement queries to System C v2 (fast 1-hop), while routing footnote/disclosure queries to System C v1 or allowing full 3-hop depth.
