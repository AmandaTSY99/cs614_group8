# Golden Set Forensic Audit & Benchmark Findings Report

**Document:** `docs/golden_set_findings_and_eval.md`  
**Date:** October 31, 2026  
**System:** System C Architecture (v1 AMR, v2 AAMR, v3 AAMR-SG)  
**Database:** Supabase Cloud PostgreSQL (`sec_chunks`, 95,044 chunks, 384-dim BGE-small embeddings)  
**Corpus Scope:** 10 Companies, FY2010–FY2026 (All 16 years verified in DB)

---

## 1. Executive Summary & Forensic Audit Mandate

During empirical evaluation of System C across the benchmark dataset, several questions initially appeared to be failures or out-of-corpus items. To guarantee total scientific integrity and eliminate speculative assumptions, every single anomaly was subjected to direct PostgreSQL database inspection, raw chunk text extraction, and execution trace logging.

This document records the empirical findings, root-cause analyses, and architectural specifications resulting from this audit.

---

## 2. Deep Dive: `gold-074` (Alphabet Net Gain on Equity Securities)

### 2.1 Question Specification & Ground Truth
* **Query ID:** `gold-074` (legacy: `amanda-134`)
* **Question Text:**
  > *"By how many millions of dollars was Alphabet Inc.'s net gain on equity securities in fiscal year 2024 lower than in fiscal year 2018?"*
* **Ground Truth Answer:** `$1,746 million`
* **Program:** `subtract(5460, 3714)`

### 2.2 Direct Database Ground Truth Verification
An empirical query against Supabase Cloud PostgreSQL confirms that the data exists and the ground truth is **100% mathematically and factually correct**:

#### Alphabet FY2018 Filing (Chunk `GOOGL_FY2018_2018-12-31:346`):
```text
ITEM 8. FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA > Gains and losses on marketable and non-marketable equity securities (table)
| Twelve Months Ended December 31, 2018                          |
| Realized gain (loss) for equity securities sold                | $1,458 |
| Unrealized gain (loss) on equity securities held               | 4,002  |
| Total gain (loss) recognized in other income (expense), net    | $5,460 |
```
And in Chunk `GOOGL_FY2018_2018-12-31:394`:
```text
| Gain (loss) on equity securities, net | 5,460 |
```

#### Alphabet FY2024 Filing (Chunk `GOOGL_FY2024_2024-12-31:430`):
```text
ITEM 8. FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA > Other Income (Expense), Net (table)
|  | Year Ended December 31, |  |  |
|---|---|---|---|
|  | 2022 | 2023 | 2024 |
| Gain (loss) on equity securities, net | (3,455) | 392 | 3,714 |
```

#### Mathematical Verification:
$$\text{FY2018 Gain} = \$5,460\text{ million}$$
$$\text{FY2024 Gain} = \$3,714\text{ million}$$
$$\text{Decrease} = \$5,460\text{M} - \$3,714\text{M} = \mathbf{\$1,746\text{ million}}$$

Furthermore, executing dense vector retrieval on Supabase (`bge-small-en-v1.5`) targeting FY2018 for *"Alphabet net gain on equity securities 2018"* places Chunk `346` at **Rank #1 with 0.8207 cosine similarity**.

### 2.3 Why All Systems Failed: The Architectural Breakdown
All 5 systems (System A, System B, System C v1, v2, v3) failed on `gold-074`. The root cause is not data absence, but two interacting architectural bugs:

1. **Harness Metadata Poisoning:**
   The benchmark creator sourced the FY2018 data from the FY2020 filing (which reprinted 2018–2020), tagging the benchmark question with:
   ```json
   "fiscal_years": [2020, 2024]
   ```
   The evaluation adapter injected this array directly into `state["fiscal_years"]`. The decomposer did not override it with the years parsed from the query text (`2018` and `2024`), hard-locking the database retriever to:
   ```sql
   WHERE ticker = 'GOOGL' AND fiscal_year IN (2020, 2024)
   ```
   The system was physically barred by code from querying the 2018 filing.

2. **Static Year Filtering Across Retrieval Hops:**
   At Hop 1, the Critic correctly identified that the 2018 data was missing. At Hop 2, the sub-query generator created a targeted sub-query: *"Alphabet 2018 net gain on equity securities"*.  
   However, the retriever filter was static: it continued using `[2020, 2024]`, ignoring the Critic's `missing_years: [2018]`.

3. **Anti-Hallucination Guardrail Adherence:**
   Because 2018 was barred from retrieval and footnote chunks pushed table chunk 430 out of the 2020 window, System C strictly followed Rule 6 of the Synthesizer prompt:
   > *"The filing evidence provided does not disclose Alphabet Inc.'s net gain on equity securities for fiscal year 2018..."*
   System C gracefully refused to hallucinate.

### 2.4 Decision: Do NOT Prune `gold-074`
Because the data exists in the database and the math is 100% sound, **`gold-074` is retained in the benchmark**. System C v3 will be upgraded to support dynamic multi-year hopping.

---

## 3. Deep Dive: `gold-011` (Microsoft Intangible Amortization)

### 3.1 Question Specification & Ground Truth
* **Query ID:** `gold-011`
* **Question Text:**
  > *"What is the percentage decrease in Microsoft's total estimated future amortization expense for intangible assets from June 30, 2017, to June 30, 2020?"*
* **Ground Truth:** `-30.36%` (from \$10,106M to \$7,038M)

### 3.2 Database Verification: The "Orphaned Table" Chunking Pathology
Querying Supabase reveals that the data exists across consecutive chunks:
* **Chunk `MSFT_FY2017_2017-06-30:379` (Narrative):**
  > *"Intangible assets amortization expense was $1.7 billion... The following table outlines the estimated future amortization expense related to intangible assets held as of June 30, 2017:"*
* **Chunk `MSFT_FY2017_2017-06-30:380` (Table):**
  > `| Year Ending June 30, | ... | Total | $10,106 |`
* **Chunk `MSFT_FY2020_2020-06-30:387` (Narrative):**
  > *"The following table outlines the estimated future amortization expense related to intangible assets held as of June 30, 2020:"*
* **Chunk `MSFT_FY2020_2020-06-30:388` (Table):**
  > `| Year Ending June 30, | ... | Total | $7,038 |`

**Pathology:** The document chunker split the lead-in sentence (which contains 100% of the query keywords) into chunks 379 and 387, while the tables (chunks 380 and 388) contain zero keywords (*"amortization"*, *"intangible"*, *"expense"* do not appear inside the table cells). Retrieval fetched the narrative lead-ins, leaving the tables orphaned.

### 3.3 Decision: Do NOT Prune `gold-011`
Because the data exists in the database and the ground truth (-30.36%) is 100% mathematically and factually sound, **`gold-011` is retained in the benchmark pool**. 

### 3.4 The Architectural Fix: Adjacent Table Chunk Stitching
Whenever `retriever_node` retrieves a chunk whose trailing text contains a forward lead-in reference to an upcoming table (e.g. matching regex `r"(?:following table|summarized below)\s*:"`), it automatically fetches the immediate adjacent chunk (`chunk_id + 1`). This deterministically links the descriptive text header to the numerical table with zero extra LLM calls.

---

## 4. Deep Dive: `gold-006` (Amazon FY16 Long-Term Debt Principal Payments)

### 4.1 Question Specification & Ground Truth
* **Query ID:** `gold-006` (legacy: `amanda-010`)
* **Question Text:**
  > *"What is the percentage of Amazon.com's total future principal payments due after 2021 relative to the total future principal payments due in 2017, based on the data provided in the 10-K for fiscal year 2016?"*
* **Ground Truth Answer:** `497.16%`
* **Program:** `divide(5250, 1056), multiply(#0, 100)`

### 4.2 Direct Database Ground Truth Verification
Inspection of Supabase Cloud PostgreSQL confirms that the ground truth of **497.16%** is **100% mathematically and factually sound** and exists cleanly in the database:

#### Chunk `AMZN_FY2016_2016-12-31:273` (Narrative Lead-In):
```text
Item 8. Financial Statements and Supplementary Data > Note 5—LONG-TERM DEBT
The other debt, including the current portion, had a weighted-average interest rate of 3.7% and 3.4% as of December 31, 2015 and 2016... As of December 31, 2016, future principal payments for our total debt were as follows (in millions):
```

#### Chunk `AMZN_FY2016_2016-12-31:274` (Principal Payment Schedule Table):
```text
Item 8. Financial Statements and Supplementary Data > Note 5—LONG-TERM DEBT (table)
| Year Ended December 31, |         |
|---|---|
| 2017                    | $1,056  |
| 2018                    | 37      |
| 2019                    | 1,278   |
| 2020                    | 217     |
| 2021                    | 1,000   |
| Thereafter              | 5,250   |
| Total                   | $8,838  |
```

#### Mathematical Verification:
$$\text{Due in 2017} = \$1,056\text{ million}$$
$$\text{Due after 2021 (Thereafter)} = \$5,250\text{ million}$$
$$\text{Ratio} = \frac{\$5,250\text{M}}{\$1,056\text{M}} \times 100\% = \mathbf{497.159...\% \approx 497.16\%}$$

### 4.3 Multi-System Performance & The Distractor Table Breakdown
Empirical evaluation logs across all 5 benchmarked systems reveal a stark division:

| System | Result | Outputted Value | Retrieved Chunks | Verdict |
| :--- | :--- | :--- | :--- | :--- |
| **System A** | **PASSED** (`numeric_correct: True`) | **497.2%** | Note 5 Long-Term Debt table | Correctly extracted Note 5 |
| **System C v1** | **PASSED** (`numeric_correct: True`) | **497.2%** | `AMZN_FY2016_2016-12-31:274` | Correctly extracted Note 5 |
| **System B** | **FAILED** (`numeric_correct: False`) | *"Not found"* | Item 15 Exhibits (irrelevant chunks) | Missed both tables |
| **System C v2** | **FAILED** (`numeric_correct: False`) | **589.1%** | `AMZN_FY2016_2016-12-31:285` | Conflated with Commitments table |

#### The Pathology: Note 5 (Principal) vs Note 6 (Principal + Interest)
In Amazon's FY2016 10-K, two distinct tables report future debt commitments:
1. **Note 5 — Long-Term Debt (Chunk 274):**
   Reports **principal-only payments** on total debt ($2017: \$1,056\text{M}$; Thereafter: $\$5,250\text{M}$ $\to$ **497.16%**).
2. **Note 6 — Commitments (Chunk 285):**
   Reports **debt principal AND interest** ($2017: \$1,343\text{M}$; Thereafter: $\$7,911\text{M}$ $\to$ **589.1%**):
   ```text
   Item 8. Financial Statements and Supplementary Data > Commitments (table)
   |                             | 2017   | 2018 | 2019   | 2020 | 2021   | Thereafter | Total    |
   | Debt principal and interest | $1,343 | $312 | $1,551 | $463 | $1,246 | $7,911     | $12,826  |
   ```

Because Chunk 285 contains the explicit row name *"Debt principal and interest"*, dense retrieval ranked Chunk 285 at Rank #2 (score: 0.7337) and Chunk 274 at Rank #4 (score: 0.7192). System C v2's synthesizer selected the Commitments table, failing to discriminate between *pure principal* and *principal + interest*. System C v1, however, correctly selected Chunk 274.

### 4.4 Decision: Do NOT Prune `gold-006`
* `gold-006` is a **100% valid, solvable, real-world benchmark question**.
* Both **System A** and **System C v1** passed it with zero errors.
* It directly tests whether an advanced financial RAG system can disambiguate pure principal amortization schedules from broad contractual commitment tables.
* **`gold-006` is retained in the benchmark pool** (pool count restored to 96).

---

## 5. Deep Dive: `gold-091` (Amazon vs JNJ Debt Principal Commitments in FY2019)

### 5.1 Question Specification & Ground Truth
* **Query ID:** `gold-091` (legacy: `amanda-154`)
* **Question Text:**
  > *"According to their fiscal year 2019 10-Ks, how many millions of dollars more debt principal was Amazon scheduled to repay in 2020 than Johnson & Johnson?"*
* **Ground Truth Answer:** `$207 million`
* **Program:** `subtract(1307, 1100)`

### 5.2 Direct Database Ground Truth Verification
Querying Supabase Cloud PostgreSQL demonstrates that the ground truth is **100% mathematically and factually sound** across both corporate filings:

#### 1. Amazon FY2019 Filing (Chunk `AMZN_FY2019_2019-12-31:288`):
```text
Item 8. Financial Statements and Supplementary Data > Note 6 — DEBT (table)
| Year Ended December 31, |         |
|---|---|
| 2020                    | $1,307  |
| 2021                    | 1,141   |
| 2022                    | 1,773   |
| 2023                    | 1,510   |
| 2024                    | 3,339   |
| Thereafter              | 15,750  |
| Total                   | $24,820 |
```
(Also explicitly corroborated in Chunk `AMZN_FY2019_2019-12-31:283`: *"Less current portion of long-term debt: $(1,307)"*).
$$\text{Amazon 2020 Debt Principal} = \mathbf{\$1,307\text{ million}}$$

#### 2. Johnson & Johnson FY2019 Filing (Chunk `JNJ_FY2019_2019-12-29:300` & Chunk `163`):
```text
Item 8. FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA > Note 7 (Borrowings / Debt) (table)
| (Dollars in Millions) |       |       |       |       |            |
|---|---|---|---|---|---|
| 2020                  | 2021  | 2022  | 2023  | 2024  | After 2024 |
| $1,100                | 1,797 | 2,106 | 1,552 | 1,474 | 19,565     |
```
And in Item 7 Contractual Obligations (Chunk `JNJ_FY2019_2019-12-29:163`):
```text
| (Dollars in Millions) | Tax Legislation (TCJA) | Debt Obligations | Interest on Debt Obligations | ...
| 2020                  | $528                   | 1,100            | 886                          | ...
```
And in Note 7 Current Portion (Chunk `JNJ_FY2019_2019-12-29:297`): *"Less current portion: 1,100"*.
$$\text{Johnson & Johnson 2020 Debt Principal} = \mathbf{\$1,100\text{ million}}$$

#### Mathematical Verification:
$$\text{Difference} = \$1,307\text{M} - \$1,100\text{M} = \mathbf{\$207\text{ million}}$$

### 5.3 Multi-System Performance & Retrieval Pathology

| System | Metric | Outputted Value | Retrieved Citations | Verdict |
| :--- | :--- | :--- | :--- | :--- |
| **System C v1** | **`numeric_correct: True`** | **$207 million** | `AMZN_FY2019:288`, `JNJ_FY2019:297` | **PASSED** (100% precision) |
| **System C v2** | `numeric_correct: False` | Unanswered (partial) | `AMZN_FY2019:288` (JNJ missed) | FAILED (cross-company hop failure) |
| **System A** | `numeric_correct: False` | *"Not found"* | Missing cross-company | FAILED |
| **System B** | `numeric_correct: False` | *"Not found"* | Missing cross-company | FAILED |

#### The Pathology: Cross-Company Retrieval Failure in System C v2
* **System C v1 passed this question with flying colors:** Its multi-hop loop retrieved the Amazon debt table on Hop 1, detected that JNJ debt information was missing, formed a follow-up sub-query for JNJ, and retrieved Chunk `297` on Hop 2, successfully synthesizing the correct subtraction (\$207M).
* **System C v2 regressed:** On Hop 1 it retrieved Amazon, but its tabular tool routing failed to expand retrieval to Johnson & Johnson's debt footnote, causing it to conclude that JNJ's data was unavailable.
* **Flawed Conclusion:** Labeling this question as an "unsolvable/ambiguous benchmark error" was completely erroneous. System C v1 had already solved it. The failure was purely a retrieval routing regression in System C v2.

### 5.4 Decision: Do NOT Prune `gold-091`
* `gold-091` is a **100% valid, verified, and solvable cross-company multi-hop question**.
* System C v1 already proved it can be answered with full numerical correctness and exact chunk citations.
* **`gold-091` is retained in the canonical benchmark pool**, restoring the total audited benchmark pool to all **97 questions**.

---

## 6. Audit Conclusion & Benchmark Integrity Summary

All 4 questions proposed for pruning were subjected to direct PostgreSQL database inspection and execution trace auditing:
1. **`gold-074`**: Ground truth (\$1,746M) is **100% sound**. Data exists across FY18 & FY24 filings. Pruning was caused by evaluation harness metadata poisoning. **RETAINED.**
2. **`gold-011`**: Ground truth (-30.36%) is **100% sound**. Data exists across FY17 & FY20 filings. Pruning was caused by an orphaned narrative/table chunk split. **RETAINED.**
3. **`gold-006`**: Ground truth (497.16%) is **100% sound**. **System A and System C v1 passed it.** Pruning was caused by System C v2 confusing Note 5 principal with Note 6 interest. **RETAINED.**
4. **`gold-091`**: Ground truth (\$207M) is **100% sound**. **System C v1 passed it.** Pruning was caused by System C v2 missing the Hop 2 cross-company retrieval to JNJ. **RETAINED.**

**Final Benchmark Status:** **0 questions pruned.** The audited benchmark pool stands at **97 / 97 valid questions**.

---

## 7. Architectural Upgrade Specifications for System C v3

To resolve multi-year hopping and harness decoupling, the following changes are specified:

1. **Query Text Year Extraction Priority (`decomposer.py`):**
   The decomposer must parse years from the user query via regex and LLM. It must union or prioritize query-extracted years over static state metadata:
   ```python
   regex_tickers, regex_years = extract_all_tickers_and_years_from_query(query)
   parsed_years = list(set((state.get("fiscal_years") or []) + regex_years + llm_years))
   ```
2. **Dynamic Hop Year Expansion (`generator.py` & `retriever.py`):**
   When the Critic identifies `missing_years`, the state machine must expand the retriever's year filter on subsequent hops:
   ```python
   if state.get("missing_years"):
       state["fiscal_years"] = sorted(list(set((state.get("fiscal_years") or []) + state["missing_years"])))
   ```
3. **Table Adjacency Stitching (Chunker & Retriever Enhancement):**
   When a retrieved chunk terminates with lead-in phrasing (*"The following table outlines..."*), the retriever should opportunistically fetch the immediate adjacent chunk `chunk_id + 1` to prevent table orphaning.
