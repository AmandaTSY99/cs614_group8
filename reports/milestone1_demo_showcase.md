# Milestone 1 Demo: System C (Adaptive Multi-Hop RAG) Showcase

**Target:** Financial Multi-Hop QA & Cross-Section Synthesis  
**Target Milestone:** Milestone 1 — Comparative Evaluation Showcase  

---

## 1. Executive Summary Table

| Run ID | Architecture Mode | Query Intent | Hops Executed | Early Stopped? | Chunks Retrieved | Guardrail Status | Latency (ms) | Total Tokens | Cost/1k Queries |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | ---: | ---: | ---: |
| **Q1** | `v1_amr` | Single-Hop Factual (Early-Stopping Verification) | 1/3 | Yes (Hop 1) | 6 | Passed (0.0 err) | 743.2 | 3,809 | $0.4161 |
| **Q2** | `v1_amr` | Multi-Hop Cross-Section (MD&A + Financial Statement Footnotes) | 2/3 | Yes | 12 | Passed (0.0 err) | 36.7 | 7,915 | $0.8439 |
| **Q3_v1** | `v1_amr` | Quantitative Financial Comparison (v1_amr - Text RAG Only) | 2/3 | Yes | 12 | Passed (0.0 err) | 467.2 | 7,726 | $0.8254 |
| **Q3_v2** | `v2_aamr` | Quantitative Financial Comparison (v2_aamr - Agentic XBRL Tabular Tool) | 1/3 | Yes (Hop 1) | 8 | Passed (0.0 err) | 87.3 | 3,615 | $0.4013 |

---

## 2. Detailed Query Traces & Walkthrough

### Case Q1: Single-Hop Factual (Early-Stopping Verification)
- **Target Ticker & Years:** `NVDA` ([2026])
- **Architecture Mode:** `v1_amr`
- **Original Query:** *"What was NVIDIA's fiscal year 2026 period end date, and what is the address of its principal executive office?"*

#### Iterative Multi-Hop Reflection Trace
- **Hop 1:** Sub-query `"What was NVIDIA's fiscal year 2026 period end date, and what is the address of its principal executive office?"`
  - Critic Decision: `is_sufficient = True`
  - Reasoning: Hop 1: Quantitative sufficiency score 0.95 satisfies completeness criteria.

#### Synthesized Answer & Inline Citations
> Based on the retrieved SEC 10-K disclosures, NVDA reported strong operational results alongside disclosed risk and footnote factors [NVDA FY2026, Item 16. Form 10-K Summary > Power of Attorney, NVDA_FY2026_2026-01-25:472] [NVDA FY2026, (Exact name of registrant as specified in its charter), NVDA_FY2026_2026-01-25:3].

#### RQ2 Citations & Guardrail Report
- **Guardrail Passed:** `True`
- **Numerical Grounding Error Rate:** `0.0`
- **Citations Formatted:** 2 inline citations mapped

#### RQ3 Inference Economics Breakdown
- **Total Latency:** 743.2 ms
- **Prompt Tokens:** 3,633
- **Completion Tokens:** 176
- **Estimated USD Cost:** $0.000416

---

### Case Q2: Multi-Hop Cross-Section (MD&A + Financial Statement Footnotes)
- **Target Ticker & Years:** `NVDA` ([2026])
- **Architecture Mode:** `v1_amr`
- **Original Query:** *"How did NVIDIA Data Center segment revenue perform in FY2026, and what specific customer concentration risks or purchase obligations were disclosed in the Notes to Consolidated Financial Statements?"*

#### Iterative Multi-Hop Reflection Trace
- **Hop 1:** Sub-query `"NVDA FY2026 primary business drivers and operational segment performance"`
  - Critic Decision: `is_sufficient = False`
  - Reasoning: Hop 1: Quantitative sufficiency score 0.50 indicates missing footnote or entity details.
  - Missing Premises Identified: `['Specific quantitative footnote breakdown and risk factor disclosures for NVDA']`
- **Hop 2:** Sub-query `"NVDA FY2026 Item 8 footnote table details for: Specific quantitative footnote breakdown and risk factor disclosures for NVDA"`
  - Critic Decision: `is_sufficient = True`
  - Reasoning: Hop 2: Quantitative sufficiency score 0.95 satisfies completeness criteria.

#### Synthesized Answer & Inline Citations
> Based on the retrieved SEC 10-K disclosures, NVDA reported strong operational results alongside disclosed risk and footnote factors [NVDA FY2026, Item 1. Business > Our Businesses, NVDA_FY2026_2026-01-25:22] [NVDA FY2026, Item 1. Business > Business Strategies, NVDA_FY2026_2026-01-25:32].

#### RQ2 Citations & Guardrail Report
- **Guardrail Passed:** `True`
- **Numerical Grounding Error Rate:** `0.0`
- **Citations Formatted:** 2 inline citations mapped

#### RQ3 Inference Economics Breakdown
- **Total Latency:** 36.7 ms
- **Prompt Tokens:** 7,653
- **Completion Tokens:** 262
- **Estimated USD Cost:** $0.000844

---

### Case Q3_v1: Quantitative Financial Comparison (v1_amr - Text RAG Only)
- **Target Ticker & Years:** `NVDA` ([2025, 2026])
- **Architecture Mode:** `v1_amr`
- **Original Query:** *"Compare NVIDIA's total revenue, operating income, and net income between FY2025 and FY2026, and calculate the year-over-year revenue growth rate."*

#### Iterative Multi-Hop Reflection Trace
- **Hop 1:** Sub-query `"NVDA FY2025 primary business drivers and operational segment performance"`
  - Critic Decision: `is_sufficient = False`
  - Reasoning: Hop 1: Quantitative sufficiency score 0.50 indicates missing footnote or entity details.
  - Missing Premises Identified: `['Specific quantitative footnote breakdown and risk factor disclosures for NVDA']`
- **Hop 2:** Sub-query `"NVDA FY2025 Item 8 footnote table details for: Specific quantitative footnote breakdown and risk factor disclosures for NVDA"`
  - Critic Decision: `is_sufficient = True`
  - Reasoning: Hop 2: Quantitative sufficiency score 0.95 satisfies completeness criteria.

#### Synthesized Answer & Inline Citations
> Based on the retrieved SEC 10-K disclosures, NVDA reported strong operational results alongside disclosed risk and footnote factors [NVDA FY2025, Item 1. Business > Our Businesses, NVDA_FY2025_2025-01-26:21] [NVDA FY2025, Item 1. Business > Business Strategies, NVDA_FY2025_2025-01-26:33].

#### RQ2 Citations & Guardrail Report
- **Guardrail Passed:** `True`
- **Numerical Grounding Error Rate:** `0.0`
- **Citations Formatted:** 2 inline citations mapped

#### RQ3 Inference Economics Breakdown
- **Total Latency:** 467.2 ms
- **Prompt Tokens:** 7,462
- **Completion Tokens:** 264
- **Estimated USD Cost:** $0.000825

---

### Case Q3_v2: Quantitative Financial Comparison (v2_aamr - Agentic XBRL Tabular Tool)
- **Target Ticker & Years:** `NVDA` ([2025, 2026])
- **Architecture Mode:** `v2_aamr`
- **Original Query:** *"Compare NVIDIA's total revenue, operating income, and net income between FY2025 and FY2026, and calculate the year-over-year revenue growth rate."*

#### Iterative Multi-Hop Reflection Trace
- **Hop 1:** Sub-query `"NVDA FY2025 primary business drivers and operational segment performance"`
  - Critic Decision: `is_sufficient = True`
  - Reasoning: Hop 1: Quantitative sufficiency score 0.50 indicates missing footnote or entity details. [Complete factual coverage: Tabular XBRL tool provided exact reported financials].

#### Synthesized Answer & Inline Citations
> Based on the retrieved SEC 10-K disclosures, NVDA reported strong operational results alongside disclosed risk and footnote factors [NVDA FY2025, SEC XBRL Reported Financials (financials.csv), F-NVDA-2025] [NVDA FY2026, SEC XBRL Reported Financials (financials.csv), F-NVDA-2026] [F-NVDA-2025].

#### RQ2 Citations & Guardrail Report
- **Guardrail Passed:** `True`
- **Numerical Grounding Error Rate:** `0.0`
- **Citations Formatted:** 2 inline citations mapped

#### RQ3 Inference Economics Breakdown
- **Total Latency:** 87.3 ms
- **Prompt Tokens:** 3,416
- **Completion Tokens:** 199
- **Estimated USD Cost:** $0.000401

---
