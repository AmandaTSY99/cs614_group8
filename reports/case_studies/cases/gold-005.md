# gold-005: Single-hop table

[← all cases](../README.md) · company: Apple Inc. (AAPL) · fiscal year: 2024 · recipe `table` · hop `single` · answer type `numeric` · scope `single_doc` · RQ2 category `quantitative_tabular`

## Gold QA

**Question**

> What was the year-over-year percentage change in the weighted-average interest rate of Apple Inc.'s commercial paper from fiscal year 2023 to fiscal year 2024?

**Gold answer**

> -5.30%

**Program**: `subtract(5.00, 5.28), divide(#0, 5.28), multiply(#1, 100)` → `-5.303030303030307`

**Gold numbers** (RQ2 numeric_accuracy targets): -5.30%

**Gold evidence**

1. `AAPL_FY2024_2024-09-28` · Item 8. Financial Statements and Supplementary Data › Commercial Paper · text

   > The weighted-average interest rate of the Company’s commercial paper was 5.00% and 5.28% as of September 28, 2024 and September 30, 2023, respectively.

## Scorecard

| Metric | A (vanilla dense) | B (hybrid + rerank) | C v1 (adaptive multi-hop) | C v2 (agentic multi-hop + XBRL) |
|---|---|---|---|---|
| **Retrieval (RQ1)** | | | | |
| chunks retrieved | 10 | 5 | 10 | 11 |
| recall@5 | 1.00 | 1.00 | 1.00 | 1.00 |
| recall@all | 1.00 | 1.00 | 1.00 | 1.00 |
| complete@all | 1 | 1 | 1 | 1 |
| average precision (lexical) | 0.64 | 0.75 | 0.70 | 0.70 |
| gold evidence first rank | #1: 1 | #1: 1 | #1: 1 | #1: 1 |
| **Answer (RQ3 string match)** | | | | |
| numeric_correct | ✓ | ✓ | ✓ | ✓ |
| keypoint_recall | – | – | – | – |
| **Answer & citations (RQ2)** | | | | |
| numeric_accuracy | 0.00 | 0.00 | 0.00 | 0.00 |
| citation precision | 1.00 | 1.00 | 1.00 | 1.00 |
| citation recall | 1.00 | 1.00 | 1.00 | 1.00 |
| citation F1 | 1.00 | 1.00 | 1.00 | 1.00 |
| has a citation | 1 | 1 | 1 | 1 |
| grounding error rate | – | – | 0.00 | 0.00 |
| **Cost (RQ3)** | | | | |
| retrieval hops | 1 | 1 | 3 | 3 |
| tokens | 2461 | 1228 | 12305 | 11740 |
| cost (USD) | 0.0004 | 0.0002 | 0.0462 | 0.0437 |
| latency (s) | 2.6 | 6.6 | 21.6 | 20.1 |

Definitions: [README › Metrics](../README.md#metrics). `–` = not applicable (e.g. no gold number, no citations, no guardrail).

## System outputs

### System A (vanilla dense)

Model: `gpt-5.4-2026-03-05`. Hops: 1. Chunks retrieved: 10, cited: 1.

**Generated answer**

> Apple’s weighted-average commercial paper interest rate decreased from 5.28% in 2023 to 5.00% in 2024 [1].
>
> Year-over-year percentage change:
>
> \[
> \frac{5.00\% - 5.28\%}{5.28\%} \times 100 \approx -5.3\%
> \]
>
> So, the weighted-average interest rate **decreased by approximately 5.3% year over year** [1].

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `AAPL_FY2024_2024-09-28:239` | Item 8 › Commercial Paper | ✓ | #1 | The Company issues unsecured short-term promissory notes pursuant to a commercial paper program. The Company uses net proceeds from the commercial paper program for general corporate purposes, including dividends and sha… |
| 2 | `AAPL_FY2024_2024-09-28:242` | Item 8 › Term Debt |  |  | \| \| Maturities (calendar year) \| 2024 \| \| 2023 \| \| \|---\|---\|---\|---\|---\|---\| \| \| Amount (in millions) \| Effective Interest Rate \| Amount (in millions) \| Effective Interest Rate \| \| \| 2013 – 2023 debt issuances: \| \| \| \| \|… |
| 3 | `AAPL_FY2024_2024-09-28:153` | Item 7A › Interest Rate Risk |  |  | \| Interest Rate Sensitive Instrument \| Hypothetical Interest Rate Increase \| Potential Impact \| 2024 \| 2023 \| \|---\|---\|---\|---\|---\| \| Investment portfolio \| 100 basis points, all tenors \| Decline in fair value \| $2,755 \|… |
| 4 | `AAPL_FY2024_2024-09-28:240` | Item 8 › Commercial Paper |  |  | \| \| 2024 \| 2023 \| 2022 \| \|---\|---\|---\|---\| \| Maturities 90 days or less: \| \| \| \| \| Proceeds from/(Repayments of) commercial paper, net \| $3,960 \| $(1,333) \| $5,264 \| \| Maturities greater than 90 days: \| \| \| \| \| Proceeds … |
| 5 | `AAPL_FY2024_2024-09-28:245` | Item 8 › Term Debt |  |  | Apple Inc. \| 2024 Form 10-K \| 43 As of September 28, 2024 and September 30, 2023, the fair value of the Company’s Notes, based on Level 2 inputs, was $88.4 billion and $90.8 billion, respectively. |
| 6 | `AAPL_FY2024_2024-09-28:232` | Item 8 › Uncertain Tax Positions |  |  | \| \| 2024 \| 2023 \| 2022 \| \|---\|---\|---\|---\| \| Beginning balances \| $19,454 \| $16,758 \| $15,477 \| \| Increases related to tax positions taken during a prior year \| 1,727 \| 2,044 \| 2,284 \| \| Decreases related to tax position… |
| 7 | `AAPL_FY2024_2024-09-28:238` | Item 8 › Note 8 – Leases |  | #1 | The weighted-average remaining lease term related to the Company’s lease liabilities as of September 28, 2024 and September 30, 2023 was 10.3 years and 10.6 years, respectively. The discount rate related to the Company’s… |
| 8 | `AAPL_FY2024_2024-09-28:163` | Item 8 › CONSOLIDATED STATEMENTS OF COMPREHENSIVE INCOME |  |  | \| \| Years ended \| \| \| \|---\|---\|---\|---\| \| \| September 28, 2024 \| September 30, 2023 \| September 24, 2022 \| \| Net income \| $93,736 \| $96,995 \| $99,803 \| \| Other comprehensive income/(loss): \| \| \| \| \| Change in foreign cur… |
| 9 | `AAPL_FY2024_2024-09-28:139` | Item 7 › Operating Expenses |  |  | Research and Development The growth in R&D expense during 2024 compared to 2023 was driven primarily by increases in headcount-related expenses. Selling, General and Administrative Selling, general and administrative exp… |
| 10 | `AAPL_FY2024_2024-09-28:204` | Item 8 › Cash, Cash Equivalents and Marketable Securities |  |  | \| \| 2023 \| \| \| \| \| \| \| \|---\|---\|---\|---\|---\|---\|---\|---\| \| \| Adjusted Cost \| Unrealized Gains \| Unrealized Losses \| Fair Value \| Cash and Cash Equivalents \| Current Marketable Securities \| Non-Current Marketable Securiti… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#1 `AAPL_FY2024_2024-09-28:239`** (cited, gold #1)

````text
Item 8. Financial Statements and Supplementary Data > Commercial Paper
The Company issues unsecured short-term promissory notes pursuant to a commercial paper program. The Company uses net proceeds from the commercial paper program for general corporate purposes, including dividends and share repurchases. As of September 28, 2024 and September 30, 2023, the Company had $10.0 billion and $6.0 billion of commercial paper outstanding, respectively, with maturities generally less than nine months. The weighted-average interest rate of the Company’s commercial paper was 5.00% and 5.28% as of September 28, 2024 and September 30, 2023, respectively. The following table provides a summary of cash flows associated with the issuance and maturities of commercial paper for 2024, 2023 and 2022 (in millions):
````

**#7 `AAPL_FY2024_2024-09-28:238`** (gold #1)

````text
Item 8. Financial Statements and Supplementary Data > Note 8 – Leases
The weighted-average remaining lease term related to the Company’s lease liabilities as of September 28, 2024 and September 30, 2023 was 10.3 years and 10.6 years, respectively. The discount rate related to the Company’s lease liabilities as of September 28, 2024 and September 30, 2023 was 3.1% and 3.0%, respectively. The discount rates related to the Company’s lease liabilities are generally based on estimates of the Company’s incremental borrowing rate, as the discount rates implicit in the Company’s leases cannot be readily determined. As of September 28, 2024, the Company had $849 million of fixed payment obligations under additional leases, primarily for corporate facilities and retail space, that had not yet commenced. These leases will commence between 2025 and 2026, with lease terms ranging from less than 1 year to 21 years. Apple Inc. | 2024 Form 10-K | 42
````

</details>

RQ2 citation match (section level): `cited=[('AAPL', 'Item 8')] gold=[(None, 'Item 8')]`

### System B (hybrid + rerank)

Model: `gpt-5.4-2026-03-05`. Hops: 1. Chunks retrieved: 5, cited: 1.

**Generated answer**

> Apple’s weighted-average commercial paper interest rate decreased from 5.28% in 2023 to 5.00% in 2024 [1].
>
> Year-over-year percentage change:
> \[
> \frac{5.00\% - 5.28\%}{5.28\%} \times 100 \approx -5.3\%
> \]
>
> So, the weighted-average interest rate decreased by approximately **5.3% year over year** [1].

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `AAPL_FY2024_2024-09-28:239` | Item 8 › Commercial Paper | ✓ | #1 | The Company issues unsecured short-term promissory notes pursuant to a commercial paper program. The Company uses net proceeds from the commercial paper program for general corporate purposes, including dividends and sha… |
| 2 | `AAPL_FY2024_2024-09-28:139` | Item 7 › Operating Expenses |  |  | Research and Development The growth in R&D expense during 2024 compared to 2023 was driven primarily by increases in headcount-related expenses. Selling, General and Administrative Selling, general and administrative exp… |
| 3 | `AAPL_FY2024_2024-09-28:129` | Item 7 › Segment Operating Performance |  |  | Americas Americas net sales increased during 2024 compared to 2023 due primarily to higher net sales of Services. Europe Europe net sales increased during 2024 compared to 2023 due primarily to higher net sales of Servic… |
| 4 | `AAPL_FY2024_2024-09-28:238` | Item 8 › Note 8 – Leases |  | #1 | The weighted-average remaining lease term related to the Company’s lease liabilities as of September 28, 2024 and September 30, 2023 was 10.3 years and 10.6 years, respectively. The discount rate related to the Company’s… |
| 5 | `AAPL_FY2024_2024-09-28:179` | Item 8 › Basis of Presentation and Preparation |  |  | The consolidated financial statements include the accounts of Apple Inc. and its wholly owned subsidiaries. The preparation of these consolidated financial statements and accompanying notes in conformity with GAAP requir… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#1 `AAPL_FY2024_2024-09-28:239`** (cited, gold #1)

````text
Item 8. Financial Statements and Supplementary Data > Commercial Paper
The Company issues unsecured short-term promissory notes pursuant to a commercial paper program. The Company uses net proceeds from the commercial paper program for general corporate purposes, including dividends and share repurchases. As of September 28, 2024 and September 30, 2023, the Company had $10.0 billion and $6.0 billion of commercial paper outstanding, respectively, with maturities generally less than nine months. The weighted-average interest rate of the Company’s commercial paper was 5.00% and 5.28% as of September 28, 2024 and September 30, 2023, respectively. The following table provides a summary of cash flows associated with the issuance and maturities of commercial paper for 2024, 2023 and 2022 (in millions):
````

**#4 `AAPL_FY2024_2024-09-28:238`** (gold #1)

````text
Item 8. Financial Statements and Supplementary Data > Note 8 – Leases
The weighted-average remaining lease term related to the Company’s lease liabilities as of September 28, 2024 and September 30, 2023 was 10.3 years and 10.6 years, respectively. The discount rate related to the Company’s lease liabilities as of September 28, 2024 and September 30, 2023 was 3.1% and 3.0%, respectively. The discount rates related to the Company’s lease liabilities are generally based on estimates of the Company’s incremental borrowing rate, as the discount rates implicit in the Company’s leases cannot be readily determined. As of September 28, 2024, the Company had $849 million of fixed payment obligations under additional leases, primarily for corporate facilities and retail space, that had not yet commenced. These leases will commence between 2025 and 2026, with lease terms ranging from less than 1 year to 21 years. Apple Inc. | 2024 Form 10-K | 42
````

</details>

RQ2 citation match (section level): `cited=[('AAPL', 'Item 8')] gold=[(None, 'Item 8')]`

### System C v1 (adaptive multi-hop)

Model: `gpt-5.4`. Hops: 3. Chunks retrieved: 10, cited: 1.

**Generated answer**

> Apple Inc.’s weighted-average interest rate on commercial paper was 5.28% as of September 30, 2023 and 5.00% as of September 28, 2024 [AAPL FY2024, Item 8, AAPL_FY2024_2024-09-28:239].  
> The year-over-year percentage change from 2023 to 2024 was approximately -5.3%, calculated as (5.00% - 5.28%) / 5.28% [AAPL FY2024, Item 8, AAPL_FY2024_2024-09-28:239].

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `AAPL_FY2024_2024-09-28:239` | Item 8 › Commercial Paper | ✓ | #1 | The Company issues unsecured short-term promissory notes pursuant to a commercial paper program. The Company uses net proceeds from the commercial paper program for general corporate purposes, including dividends and sha… |
| 2 | `AAPL_FY2024_2024-09-28:240` | Item 8 › Commercial Paper |  |  | \| \| 2024 \| 2023 \| 2022 \| \|---\|---\|---\|---\| \| Maturities 90 days or less: \| \| \| \| \| Proceeds from/(Repayments of) commercial paper, net \| $3,960 \| $(1,333) \| $5,264 \| \| Maturities greater than 90 days: \| \| \| \| \| Proceeds … |
| 3 | `AAPL_FY2024_2024-09-28:153` | Item 7A › Interest Rate Risk |  |  | \| Interest Rate Sensitive Instrument \| Hypothetical Interest Rate Increase \| Potential Impact \| 2024 \| 2023 \| \|---\|---\|---\|---\|---\| \| Investment portfolio \| 100 basis points, all tenors \| Decline in fair value \| $2,755 \|… |
| 4 | `AAPL_FY2024_2024-09-28:242` | Item 8 › Term Debt |  |  | \| \| Maturities (calendar year) \| 2024 \| \| 2023 \| \| \|---\|---\|---\|---\|---\|---\| \| \| Amount (in millions) \| Effective Interest Rate \| Amount (in millions) \| Effective Interest Rate \| \| \| 2013 – 2023 debt issuances: \| \| \| \| \|… |
| 5 | `AAPL_FY2024_2024-09-28:238` | Item 8 › Note 8 – Leases |  | #1 | The weighted-average remaining lease term related to the Company’s lease liabilities as of September 28, 2024 and September 30, 2023 was 10.3 years and 10.6 years, respectively. The discount rate related to the Company’s… |
| 6 | `AAPL_FY2024_2024-09-28:143` | Item 7 › Liquidity and Capital Resources |  |  | The Company believes its balances of unrestricted cash, cash equivalents and marketable securities, which totaled $140.8 billion as of September 28, 2024, along with cash generated by ongoing operations and continued acc… |
| 7 | `AAPL_FY2024_2024-09-28:204` | Item 8 › Cash, Cash Equivalents and Marketable Securities |  |  | \| \| 2023 \| \| \| \| \| \| \| \|---\|---\|---\|---\|---\|---\|---\|---\| \| \| Adjusted Cost \| Unrealized Gains \| Unrealized Losses \| Fair Value \| Cash and Cash Equivalents \| Current Marketable Securities \| Non-Current Marketable Securiti… |
| 8 | `AAPL_FY2024_2024-09-28:201` | Item 8 › Cash, Cash Equivalents and Marketable Securities |  |  | \| \| 2024 \| \| \| \| \| \| \| \|---\|---\|---\|---\|---\|---\|---\|---\| \| \| Adjusted Cost \| Unrealized Gains \| Unrealized Losses \| Fair Value \| Cash and Cash Equivalents \| Current Marketable Securities \| Non-Current Marketable Securiti… |
| 9 | `AAPL_FY2024_2024-09-28:243` | Item 8 › Term Debt |  |  | To manage interest rate risk on certain of its U.S. dollar–denominated fixed-rate notes, the Company uses interest rate swaps to effectively convert the fixed interest rates to floating interest rates on a portion of the… |
| 10 | `AAPL_FY2024_2024-09-28:208` | Item 8 › Derivative Instruments and Hedging |  |  | To protect the Company’s foreign currency–denominated term debt or marketable securities from fluctuations in foreign exchange rates, the Company may use forwards, cross-currency swaps or other instruments. The Company d… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#1 `AAPL_FY2024_2024-09-28:239`** (cited, gold #1)

````text
Item 8. Financial Statements and Supplementary Data > Commercial Paper
The Company issues unsecured short-term promissory notes pursuant to a commercial paper program. The Company uses net proceeds from the commercial paper program for general corporate purposes, including dividends and share repurchases. As of September 28, 2024 and September 30, 2023, the Company had $10.0 billion and $6.0 billion of commercial paper outstanding, respectively, with maturities generally less than nine months. The weighted-average interest rate of the Company’s commercial paper was 5.00% and 5.28% as of September 28, 2024 and September 30, 2023, respectively. The following table provides a summary of cash flows associated with the issuance and maturities of commercial paper for 2024, 2023 and 2022 (in millions):
````

**#5 `AAPL_FY2024_2024-09-28:238`** (gold #1)

````text
Item 8. Financial Statements and Supplementary Data > Note 8 – Leases
The weighted-average remaining lease term related to the Company’s lease liabilities as of September 28, 2024 and September 30, 2023 was 10.3 years and 10.6 years, respectively. The discount rate related to the Company’s lease liabilities as of September 28, 2024 and September 30, 2023 was 3.1% and 3.0%, respectively. The discount rates related to the Company’s lease liabilities are generally based on estimates of the Company’s incremental borrowing rate, as the discount rates implicit in the Company’s leases cannot be readily determined. As of September 28, 2024, the Company had $849 million of fixed payment obligations under additional leases, primarily for corporate facilities and retail space, that had not yet commenced. These leases will commence between 2025 and 2026, with lease terms ranging from less than 1 year to 21 years. Apple Inc. | 2024 Form 10-K | 42
````

</details>

RQ2 citation match (section level): `cited=[('AAPL', 'Item 8')] gold=[(None, 'Item 8')]`

**System C guardrail** (judge `gpt-5.4`): numerical claims 6, verified 6, ungrounded 0, uncited 0, derived 0; sentence verdicts: supported 0, partial 0, unsupported 0, unchecked 0.


<details><summary>Guardrail sentence verdicts</summary>

| sentence | verdict | judge reason |
|---|---|---|
| Apple Inc.’s weighted-average interest rate on commercial paper was 5.28% as of September 30, 2023 and 5.00% as of September 28, 2024 [AAPL FY2024, Item 8, AAPL_FY2024_2024-09-28:239]. | None |  |
| The year-over-year percentage change from 2023 to 2024 was approximately -5.3%, calculated as (5.00% - 5.28%) / 5.28% [AAPL FY2024, Item 8, AAPL_FY2024_2024-09-28:239]. | None |  |

</details>

### System C v2 (agentic multi-hop + XBRL)

Model: `gpt-5.4`. Hops: 3. Chunks retrieved: 11, cited: 1.

**Generated answer**

> Apple Inc.’s weighted-average interest rate on commercial paper decreased from 5.28% in fiscal year 2023 to 5.00% in fiscal year 2024 [AAPL FY2024, Item 8, AAPL_FY2024_2024-09-28:239].  
> The year-over-year percentage change was approximately -5.3%, calculated as (5.00% - 5.28%) / 5.28% [AAPL FY2024, Item 8, AAPL_FY2024_2024-09-28:239].

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `AAPL_FY2024_2024-09-28:239` | Item 8 › Commercial Paper | ✓ | #1 | The Company issues unsecured short-term promissory notes pursuant to a commercial paper program. The Company uses net proceeds from the commercial paper program for general corporate purposes, including dividends and sha… |
| 2 | `AAPL_FY2024_2024-09-28:240` | Item 8 › Commercial Paper |  |  | \| \| 2024 \| 2023 \| 2022 \| \|---\|---\|---\|---\| \| Maturities 90 days or less: \| \| \| \| \| Proceeds from/(Repayments of) commercial paper, net \| $3,960 \| $(1,333) \| $5,264 \| \| Maturities greater than 90 days: \| \| \| \| \| Proceeds … |
| 3 | `AAPL_FY2024_2024-09-28:153` | Item 7A › Interest Rate Risk |  |  | \| Interest Rate Sensitive Instrument \| Hypothetical Interest Rate Increase \| Potential Impact \| 2024 \| 2023 \| \|---\|---\|---\|---\|---\| \| Investment portfolio \| 100 basis points, all tenors \| Decline in fair value \| $2,755 \|… |
| 4 | `AAPL_FY2024_2024-09-28:242` | Item 8 › Term Debt |  |  | \| \| Maturities (calendar year) \| 2024 \| \| 2023 \| \| \|---\|---\|---\|---\|---\|---\| \| \| Amount (in millions) \| Effective Interest Rate \| Amount (in millions) \| Effective Interest Rate \| \| \| 2013 – 2023 debt issuances: \| \| \| \| \|… |
| 5 | `AAPL_FY2024_2024-09-28:238` | Item 8 › Note 8 – Leases |  | #1 | The weighted-average remaining lease term related to the Company’s lease liabilities as of September 28, 2024 and September 30, 2023 was 10.3 years and 10.6 years, respectively. The discount rate related to the Company’s… |
| 6 | `AAPL_FY2024_2024-09-28:143` | Item 7 › Liquidity and Capital Resources |  |  | The Company believes its balances of unrestricted cash, cash equivalents and marketable securities, which totaled $140.8 billion as of September 28, 2024, along with cash generated by ongoing operations and continued acc… |
| 7 | `AAPL_FY2024_2024-09-28:169` | Item 8 › CONSOLIDATED BALANCE SHEETS |  |  | See accompanying Notes to Consolidated Financial Statements. Apple Inc. \| 2024 Form 10-K \| 31 |
| 8 | `AAPL_FY2024_2024-09-28:165` | Item 8 › CONSOLIDATED STATEMENTS OF COMPREHENSIVE INCOME |  |  | See accompanying Notes to Consolidated Financial Statements. Apple Inc. \| 2024 Form 10-K \| 30 |
| 9 | `AAPL_FY2024_2024-09-28:156` | Item 8 |  |  | \| Index to Consolidated Financial Statements \| Page \| \|---\|---\| \| Consolidated Statements of Operations for the years ended September 28, 2024, September 30, 2023 and September 24, 2022 \| 29 \| \| Consolidated Statements o… |
| 10 | `AAPL_FY2024_2024-09-28:178` | Item 8 › CONSOLIDATED STATEMENTS OF CASH FLOWS |  |  | See accompanying Notes to Consolidated Financial Statements. Apple Inc. \| 2024 Form 10-K \| 33 |
| 11 | `AAPL_FY2024_2024-09-28:243` | Item 8 › Term Debt |  |  | To manage interest rate risk on certain of its U.S. dollar–denominated fixed-rate notes, the Company uses interest rate swaps to effectively convert the fixed interest rates to floating interest rates on a portion of the… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#1 `AAPL_FY2024_2024-09-28:239`** (cited, gold #1)

````text
Item 8. Financial Statements and Supplementary Data > Commercial Paper
The Company issues unsecured short-term promissory notes pursuant to a commercial paper program. The Company uses net proceeds from the commercial paper program for general corporate purposes, including dividends and share repurchases. As of September 28, 2024 and September 30, 2023, the Company had $10.0 billion and $6.0 billion of commercial paper outstanding, respectively, with maturities generally less than nine months. The weighted-average interest rate of the Company’s commercial paper was 5.00% and 5.28% as of September 28, 2024 and September 30, 2023, respectively. The following table provides a summary of cash flows associated with the issuance and maturities of commercial paper for 2024, 2023 and 2022 (in millions):
````

**#5 `AAPL_FY2024_2024-09-28:238`** (gold #1)

````text
Item 8. Financial Statements and Supplementary Data > Note 8 – Leases
The weighted-average remaining lease term related to the Company’s lease liabilities as of September 28, 2024 and September 30, 2023 was 10.3 years and 10.6 years, respectively. The discount rate related to the Company’s lease liabilities as of September 28, 2024 and September 30, 2023 was 3.1% and 3.0%, respectively. The discount rates related to the Company’s lease liabilities are generally based on estimates of the Company’s incremental borrowing rate, as the discount rates implicit in the Company’s leases cannot be readily determined. As of September 28, 2024, the Company had $849 million of fixed payment obligations under additional leases, primarily for corporate facilities and retail space, that had not yet commenced. These leases will commence between 2025 and 2026, with lease terms ranging from less than 1 year to 21 years. Apple Inc. | 2024 Form 10-K | 42
````

</details>

RQ2 citation match (section level): `cited=[('AAPL', 'Item 8')] gold=[(None, 'Item 8')]`

**System C guardrail** (judge `gpt-5.4`): numerical claims 6, verified 6, ungrounded 0, uncited 0, derived 0; sentence verdicts: supported 0, partial 0, unsupported 0, unchecked 0.


<details><summary>Guardrail sentence verdicts</summary>

| sentence | verdict | judge reason |
|---|---|---|
| Apple Inc.’s weighted-average interest rate on commercial paper decreased from 5.28% in fiscal year 2023 to 5.00% in fiscal year 2024 [AAPL FY2024, Item 8, AAPL_FY2024_2024-09-28:239]. | None |  |
| The year-over-year percentage change was approximately -5.3%, calculated as (5.00% - 5.28%) / 5.28% [AAPL FY2024, Item 8, AAPL_FY2024_2024-09-28:239]. | None |  |

</details>
