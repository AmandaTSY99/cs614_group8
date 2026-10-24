# Milestone 1 Demo: System C (Adaptive Multi-Hop RAG) Showcase

**Date:** 24-25 October 2026  
**Authors:** Anish (System Architecture & RQ3 Lead) & Aryan (Synthesizer, Citations & RQ2 Lead)  
**Target Milestone:** Milestone 1 — Team Sync & 3-System Comparative Demo  

---

## 1. Executive Summary Table

| Run ID | Architecture Mode | Query Intent | Hops Executed | Early Stopped? | Chunks Retrieved | Guardrail Status | Latency (ms) | Total Tokens | Cost/1k Queries |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | ---: | ---: | ---: |
| **Q1** | `v1_amr` | Single-Hop Factual (Early-Stopping Verification) | 1/3 | Yes (Hop 1) | 4 | Passed (0.0 err) | 24.6 | 2,184 | $0.2432 |
| **Q2** | `v1_amr` | Multi-Hop Cross-Section (MD&A + Financial Statement Footnotes) | 2/3 | Yes | 8 | Passed (0.0 err) | 13.8 | 4,405 | $0.4767 |
| **Q3_v1** | `v1_amr` | Quantitative Financial Comparison (v1_amr - Text RAG Only) | 2/3 | Yes | 8 | Passed (0.0 err) | 44.1 | 4,310 | $0.4674 |
| **Q3_v2** | `v2_aamr` | Quantitative Financial Comparison (v2_aamr - Agentic XBRL Tabular Tool) | 2/3 | Yes | 10 | Passed (0.0 err) | 37.4 | 4,419 | $0.4781 |

---

## 2. Detailed Query Traces & Walkthrough

### Case Q1: Single-Hop Factual (Early-Stopping Verification)
- **Target Ticker & Years:** `NVDA` ([2026])
- **Architecture Mode:** `v1_amr`
- **Original Query:** *"What was NVIDIA's fiscal year 2026 period end date, and what is the address of its principal executive office?"*

#### Iterative Multi-Hop Reflection Trace
- **Hop 1:** Sub-query `"What was NVIDIA's fiscal year 2026 period end date, and what is the address of its principal executive office?"`
  - Critic Decision: `is_sufficient = True`
  - Reasoning: Hop 1: All required entities and quantitative figures are present in accumulated evidence.

#### Synthesized Answer & Inline Citations
> Based on the retrieved SEC 10-K disclosures, NVDA reported strong operational results alongside disclosed risk and footnote factors [NVDA FY2026, Item 15. Exhibits and Financial Statement Schedules > Note 7 - Cash Equivalents and Marketable Securities, NVDA_FY2026_2026-01-25:365] [NVDA FY2026, Item 15. Exhibits and Financial Statement Schedules > Exhibit Index, NVDA_FY2026_2026-01-25:462].

#### RQ2 Citations & Guardrail Report
- **Guardrail Passed:** `True`
- **Numerical Grounding Error Rate:** `0.0`
- **Citations Formatted:** 2 inline citations mapped

#### RQ3 Inference Economics Breakdown
- **Total Latency:** 24.6 ms
- **Prompt Tokens:** 2,060
- **Completion Tokens:** 124
- **Estimated USD Cost:** $0.000243

---

### Case Q2: Multi-Hop Cross-Section (MD&A + Financial Statement Footnotes)
- **Target Ticker & Years:** `NVDA` ([2026])
- **Architecture Mode:** `v1_amr`
- **Original Query:** *"How did NVIDIA Data Center segment revenue perform in FY2026, and what specific customer concentration risks or purchase obligations were disclosed in the Notes to Consolidated Financial Statements?"*

#### Iterative Multi-Hop Reflection Trace
- **Hop 1:** Sub-query `"NVDA FY2026 primary business drivers and operational segment performance"`
  - Critic Decision: `is_sufficient = False`
  - Reasoning: Hop 1: Retrieved initial MD&A context, but missing specific quantitative footnote disclosures.
  - Missing Premises Identified: `['Specific quantitative footnote breakdown and risk factor disclosures referenced in Item 7']`
- **Hop 2:** Sub-query `"NVDA FY2026 Item 8 footnote table details for: Specific quantitative footnote breakdown and risk factor disclosures referenced in Item 7"`
  - Critic Decision: `is_sufficient = True`
  - Reasoning: Hop 2: All required entities and quantitative figures are present in accumulated evidence.

#### Synthesized Answer & Inline Citations
> Based on the retrieved SEC 10-K disclosures, NVDA reported strong operational results alongside disclosed risk and footnote factors [NVDA FY2026, Item 1. Business > Our Businesses, NVDA_FY2026_2026-01-25:22] [NVDA FY2026, Item 1. Business > Business Strategies, NVDA_FY2026_2026-01-25:32].

#### RQ2 Citations & Guardrail Report
- **Guardrail Passed:** `True`
- **Numerical Grounding Error Rate:** `0.0`
- **Citations Formatted:** 2 inline citations mapped

#### RQ3 Inference Economics Breakdown
- **Total Latency:** 13.8 ms
- **Prompt Tokens:** 4,224
- **Completion Tokens:** 181
- **Estimated USD Cost:** $0.000477

---

### Case Q3_v1: Quantitative Financial Comparison (v1_amr - Text RAG Only)
- **Target Ticker & Years:** `NVDA` ([2025, 2026])
- **Architecture Mode:** `v1_amr`
- **Original Query:** *"Compare NVIDIA's total revenue, operating income, and net income between FY2025 and FY2026, and calculate the year-over-year revenue growth rate."*

#### Iterative Multi-Hop Reflection Trace
- **Hop 1:** Sub-query `"NVDA FY2025 primary business drivers and operational segment performance"`
  - Critic Decision: `is_sufficient = False`
  - Reasoning: Hop 1: Retrieved initial MD&A context, but missing specific quantitative footnote disclosures.
  - Missing Premises Identified: `['Specific quantitative footnote breakdown and risk factor disclosures referenced in Item 7']`
- **Hop 2:** Sub-query `"NVDA FY2025 Item 8 footnote table details for: Specific quantitative footnote breakdown and risk factor disclosures referenced in Item 7"`
  - Critic Decision: `is_sufficient = True`
  - Reasoning: Hop 2: All required entities and quantitative figures are present in accumulated evidence.

#### Synthesized Answer & Inline Citations
> Based on the retrieved SEC 10-K disclosures, NVDA reported strong operational results alongside disclosed risk and footnote factors [NVDA FY2026, Item 1. Business > Our Businesses, NVDA_FY2026_2026-01-25:22] [NVDA FY2025, Item 1. Business > Our Businesses, NVDA_FY2025_2025-01-26:21].

#### RQ2 Citations & Guardrail Report
- **Guardrail Passed:** `True`
- **Numerical Grounding Error Rate:** `0.0`
- **Citations Formatted:** 2 inline citations mapped

#### RQ3 Inference Economics Breakdown
- **Total Latency:** 44.1 ms
- **Prompt Tokens:** 4,128
- **Completion Tokens:** 182
- **Estimated USD Cost:** $0.000467

---

### Case Q3_v2: Quantitative Financial Comparison (v2_aamr - Agentic XBRL Tabular Tool)
- **Target Ticker & Years:** `NVDA` ([2025, 2026])
- **Architecture Mode:** `v2_aamr`
- **Original Query:** *"Compare NVIDIA's total revenue, operating income, and net income between FY2025 and FY2026, and calculate the year-over-year revenue growth rate."*

#### Iterative Multi-Hop Reflection Trace
- **Hop 1:** Sub-query `"NVDA FY2025 primary business drivers and operational segment performance"`
  - Critic Decision: `is_sufficient = False`
  - Reasoning: Hop 1: Retrieved initial MD&A context, but missing specific quantitative footnote disclosures.
  - Missing Premises Identified: `['Specific quantitative footnote breakdown and risk factor disclosures referenced in Item 7']`
- **Hop 2:** Sub-query `"NVDA FY2025 Item 8 footnote table details for: Specific quantitative footnote breakdown and risk factor disclosures referenced in Item 7"`
  - Critic Decision: `is_sufficient = True`
  - Reasoning: Hop 2: All required entities and quantitative figures are present in accumulated evidence.

#### Synthesized Answer & Inline Citations
> Based on the retrieved SEC 10-K disclosures, NVDA reported strong operational results alongside disclosed risk and footnote factors [NVDA FY2025, SEC XBRL Reported Financials (financials.csv), F-NVDA-2025] [NVDA FY2026, SEC XBRL Reported Financials (financials.csv), F-NVDA-2026] [F-NVDA-2025].

#### RQ2 Citations & Guardrail Report
- **Guardrail Passed:** `True`
- **Numerical Grounding Error Rate:** `0.0`
- **Citations Formatted:** 2 inline citations mapped

#### RQ3 Inference Economics Breakdown
- **Total Latency:** 37.4 ms
- **Prompt Tokens:** 4,238
- **Completion Tokens:** 181
- **Estimated USD Cost:** $0.000478

---
