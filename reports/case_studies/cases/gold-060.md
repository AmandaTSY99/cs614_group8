# gold-060: Table + text (one filing)

[← all cases](../README.md) · company: JOHNSON & JOHNSON (JNJ) · fiscal year: 2022 · recipe `table_text` · hop `multi` · answer type `mixed` · scope `single_doc` · RQ2 category `cross_section_multihop`

## Gold QA

**Question**

> According to Johnson & Johnson's 2022 10-K, what was the percentage increase in total borrowings from 2021 to 2022, and what specific acquisition did the company identify as the driver for this increase?

**Gold answer**

> Total borrowings increased by 17.46% (from $33.8 billion at the end of 2021 to $39.7 billion at the end of 2022), driven by the acquisition of Abiomed, Inc.

**Program**: `subtract(39.7, 33.8), divide(#0, 33.8)` → `0.17455621301775165`

**Gold numbers** (RQ2 numeric_accuracy targets): 17.46%

**Key points** (RQ3 keypoint_recall targets)

1. 17.46%
2. Abiomed, Inc.

**Gold evidence**

1. `JNJ_FY2022_2023-01-01` · Item 7.MANAGEMENT’S DISCUSSION AND ANALYSIS OF RESULTS OF OPERATIONS AND FINANCIAL CONDITION › Financing and Market Risk · text

   > Total borrowings at the end of 2022 and 2021 were $39.7 billion and $33.8 billion, respectively.

2. `JNJ_FY2022_2023-01-01` · Item 7.MANAGEMENT’S DISCUSSION AND ANALYSIS OF RESULTS OF OPERATIONS AND FINANCIAL CONDITION › Financing and Market Risk · text

   > The increase in borrowings was due to the acquisition of Abiomed, Inc.

## Scorecard

| Metric | A (vanilla dense) | B (hybrid + rerank) | C v1 (adaptive multi-hop) | C v2 (agentic multi-hop + XBRL) |
|---|---|---|---|---|
| **Retrieval (RQ1)** | | | | |
| chunks retrieved | 10 | 5 | 10 | 11 |
| recall@5 | 1.00 | 1.00 | 1.00 | 1.00 |
| recall@all | 1.00 | 1.00 | 1.00 | 1.00 |
| complete@all | 1 | 1 | 1 | 1 |
| average precision (lexical) | 0.62 | 0.81 | 0.51 | 0.36 |
| gold evidence first rank | #1: 1, #2: 1 | #1: 1, #2: 1 | #1: 1, #2: 1 | #1: 2, #2: 2 |
| **Answer (RQ3 string match)** | | | | |
| numeric_correct | ✓ | ✓ | ✓ | ✓ |
| keypoint_recall | 0.50 | 0.50 | 0.50 | 0.50 |
| **Answer & citations (RQ2)** | | | | |
| numeric_accuracy | 1.00 | 1.00 | 1.00 | 1.00 |
| citation precision | 1.00 | 1.00 | 1.00 | 1.00 |
| citation recall | 1.00 | 1.00 | 1.00 | 1.00 |
| citation F1 | 1.00 | 1.00 | 1.00 | 1.00 |
| has a citation | 1 | 1 | 1 | 1 |
| grounding error rate | – | – | 0.00 | 0.00 |
| **Cost (RQ3)** | | | | |
| retrieval hops | 1 | 1 | 3 | 2 |
| tokens | 3411 | 1639 | 14860 | 11094 |
| cost (USD) | 0.0006 | 0.0003 | 0.0540 | 0.0390 |
| latency (s) | 2.4 | 7.0 | 24.2 | 18.0 |

Definitions: [README › Metrics](../README.md#metrics). `–` = not applicable (e.g. no gold number, no citations, no guardrail).

## System outputs

### System A (vanilla dense)

Model: `gpt-5.4-2026-03-05`. Hops: 1. Chunks retrieved: 10, cited: 1.

**Generated answer**

> Johnson & Johnson’s total borrowings increased from **$33.8 billion in 2021** to **$39.7 billion in 2022** [1].
>
> The percentage increase was approximately:
>
> \[
> \frac{39.7 - 33.8}{33.8} \times 100 \approx 17.5\%
> \]
>
> So, the increase was **about 17.5%** [1].
>
> The company said this increase was due to **the acquisition of Abiomed, Inc.** [1]

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `JNJ_FY2022_2023-01-01:200` | Item 7 › Financing and Market Risk | ✓ | #1, #2 | The Company has access to substantial sources of funds at numerous banks worldwide. In September 2022, the Company secured a new 364-day Credit Facility of $10 billion, which expires on September 7, 2023. In November 202… |
| 2 | `JNJ_FY2022_2023-01-01:341` | Item 8 › 7.Borrowings |  |  | \| (Dollars in Millions) \| 2022 \| \| Effective Rate % \| \| 2021 \| \| Effective Rate % \| \| \|---\|---\|---\|---\|---\|---\|---\|---\|---\| \| 4.85% Notes due 2041 \| 297 \| \| 4.89 \| \| 297 \| \| 4.89 \| \| \| 4.50% Notes due 2043 \| 496 \| \| 4.52… |
| 3 | `JNJ_FY2022_2023-01-01:344` | Item 8 › 7.Borrowings |  | #1 | Throughout fiscal years 2022 and 2021, the Company continued to have access to liquidity through the commercial paper market. Short-term borrowings and the current portion of long-term debt amounted to approximately $12.… |
| 4 | `JNJ_FY2022_2023-01-01:338` | Item 8 › 7.Borrowings |  |  | \| (Dollars in Millions) \| 2022 \| \| Effective Rate % \| \| 2021 \| \| Effective Rate % \| \| \|---\|---\|---\|---\|---\|---\|---\|---\|---\| \| 0.250% Notes due 2022 (1B Euro 1.1311)(3) \| $— \| \| —% \| \| $1,131 \| (3) \| 0.26% \| \| \| 2.25% Not… |
| 5 | `JNJ_FY2022_2023-01-01:339` | Item 8 › 7.Borrowings |  |  | \| (Dollars in Millions) \| 2022 \| \| Effective Rate % \| \| 2021 \| \| Effective Rate % \| \| \|---\|---\|---\|---\|---\|---\|---\|---\|---\| \| 0.55% Notes due 2025 \| 918 \| \| 0.57 \| \| 983 \| \| 0.57 \| \| \| 2.45% Notes due 2026 \| 1,996 \| \| 2.… |
| 6 | `JNJ_FY2022_2023-01-01:342` | Item 8 › 7.Borrowings |  |  | \| (Dollars in Millions) \| 2022 \| \| Effective Rate % \| \| 2021 \| \| Effective Rate % \| \| \|---\|---\|---\|---\|---\|---\|---\|---\|---\| \| Total long-term debt \| $26,888 \| \| \| \| $29,985 \| \| \| \| |
| 7 | `JNJ_FY2022_2023-01-01:340` | Item 8 › 7.Borrowings |  |  | \| (Dollars in Millions) \| 2022 \| \| Effective Rate % \| \| 2021 \| \| Effective Rate % \| \| \|---\|---\|---\|---\|---\|---\|---\|---\|---\| \| 4.375% Notes due 2033 \| 854 \| \| 4.24 \| \| 854 \| \| 4.24 \| \| \| 1.650% Notes due 2035 (1.5B Euro 1… |
| 8 | `JNJ_FY2022_2023-01-01:343` | Item 8 › 7.Borrowings |  | #1 | (1)Weighted average effective rate. (2)Translation rate at January 1, 2023. (3)Translation rate at January 2, 2022. (4)The excess of the carrying value over the fair value of debt was $1.6 billion at the end of fiscal ye… |
| 9 | `JNJ_FY2022_2023-01-01:192` | Item 7 › Liquidity & Cash Flows |  | #1, #2 | As of January 1, 2023, the Company's notes payable and long-term debt was in excess of cash, cash equivalents and marketable securities. As of January 1, 2023, the net debt position was $16.1 billion as compared to the p… |
| 10 | `JNJ_FY2022_2023-01-01:142` | Item 7 › Analysis of Consolidated Sales |  |  | \| Sales increase/(decrease) due to: \| 2022 \| 2021 \| \|---\|---\|---\| \| Volume \| 6.9% \| 12.9% \| \| Price \| (0.8) \| (0.7) \| \| Currency \| (4.8) \| 1.4 \| \| Total \| 1.3% \| 13.6% \| |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#1 `JNJ_FY2022_2023-01-01:200`** (cited, gold #1, gold #2)

````text
Item 7.MANAGEMENT’S DISCUSSION AND ANALYSIS OF RESULTS OF OPERATIONS AND FINANCIAL CONDITION > Financing and Market Risk
The Company has access to substantial sources of funds at numerous banks worldwide. In September 2022, the Company secured a new 364-day Credit Facility of $10 billion, which expires on September 7, 2023. In November 2022, the Company secured an additional 364-day revolving Credit Facility of $10 billion, which has an expiration of November 21, 2023. Interest charged on borrowings under the credit line agreement is based on either Secured Overnight Financing Rate (SOFR) Reference Rate or other applicable market rate as allowed plus applicable margins. Commitment fees under the agreement are not material. Total borrowings at the end of 2022 and 2021 were $39.7 billion and $33.8 billion, respectively. The increase in borrowings was due to the acquisition of Abiomed, Inc. In 2022, net debt (cash and current marketable securities, net of debt) was $16.1 billion compared to net debt of $2.1 billion in 2021. Total debt represented 34.1% of total capital (shareholders’ equity and total debt) in 2022 and 31.3% of total capital in 2021. Shareholders’ equity per share at the end of 2022 was $29.39 compared to $28.16 at year-end 2021. A summary of borrowings can be found in Note 7 to the Consolidated Financial Statements.
````

**#3 `JNJ_FY2022_2023-01-01:344`** (gold #1)

````text
Item 8. FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA > 7.Borrowings
Throughout fiscal years 2022 and 2021, the Company continued to have access to liquidity through the commercial paper market. Short-term borrowings and the current portion of long-term debt amounted to approximately $12.8 billion and $3.8 billion at the end of fiscal years 2022 and 2021, respectively. The current portion of the long term debt was $1.6 billion and $2.1 billion in 2022 and 2021, respectively, and the remainder is commercial paper and local borrowing by international subsidiaries. The current debt balance as of January 1, 2023 includes $11.2 billion of commercial paper which has a weighted average interest rate of 4.23% and a weighted average maturity of approximately two months. Aggregate maturities of long-term debt obligations commencing in 2023 are:
````

**#8 `JNJ_FY2022_2023-01-01:343`** (gold #1)

````text
Item 8. FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA > 7.Borrowings
(1)Weighted average effective rate. (2)Translation rate at January 1, 2023. (3)Translation rate at January 2, 2022. (4)The excess of the carrying value over the fair value of debt was $1.6 billion at the end of fiscal year 2022 and the excess of the fair value over the carrying value of debt was $3.2 billion at the end of fiscal year 2021. Fair value of the long-term debt was estimated using market prices, which were corroborated by quoted broker prices and significant other observable inputs. The Company has access to substantial sources of funds at numerous banks worldwide. In September 2022, the Company secured a new 364-day Credit Facility of $10 billion, which expires on September 7, 2023. In November 2022, the Company secured an additional 364-day Credit Facility of $10 billion, which expires on November 21, 2023. Interest charged on borrowings under the credit line agreement is based on either the Term SOFR Reference Rate or other applicable market rates as allowed under the terms of the agreement, plus applicable margins. Commitment fees under the agreements are not material.
````

**#9 `JNJ_FY2022_2023-01-01:192`** (gold #1, gold #2)

````text
Item 7.MANAGEMENT’S DISCUSSION AND ANALYSIS OF RESULTS OF OPERATIONS AND FINANCIAL CONDITION > Liquidity & Cash Flows
As of January 1, 2023, the Company's notes payable and long-term debt was in excess of cash, cash equivalents and marketable securities. As of January 1, 2023, the net debt position was $16.1 billion as compared to the prior year of $2.1 billion. The increase was primarily due to the acquisition of Abiomed, Inc. in December 2022. The debt balance at the end of 2022 was $39.7 billion as compared to $33.8 billion in 2021. Considering recent market conditions, the Company has re-evaluated its operating cash flows and liquidity profile and does not foresee any significant incremental risk. The Company anticipates that operating cash flows, the ability to raise funds from external sources, borrowing capacity from existing committed credit facilities and access to the commercial paper markets will continue to provide sufficient resources to fund operating needs, including the Company's remaining balance to be paid on the agreement to settle opioid litigation for approximately $2.7 billion and the establishment of the $2.0 billion trust for talc related liabilities (See Note 19 to the Consolidated Financial Statements for additional details). In addition, the Company monitors the global capital markets on an ongoing basis and from time to time may raise capital
````

</details>

RQ2 citation match (section level): `cited=[('JNJ', 'Item 7')] gold=[(None, 'Item 7')]`

### System B (hybrid + rerank)

Model: `gpt-5.4-2026-03-05`. Hops: 1. Chunks retrieved: 5, cited: 1.

**Generated answer**

> Total borrowings increased from $33.8 billion in 2021 to $39.7 billion in 2022, an increase of about 17.5% \[((39.7 - 33.8) / 33.8) × 100\]. The company said this increase was due to the acquisition of Abiomed, Inc. [1]

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `JNJ_FY2022_2023-01-01:200` | Item 7 › Financing and Market Risk | ✓ | #1, #2 | The Company has access to substantial sources of funds at numerous banks worldwide. In September 2022, the Company secured a new 364-day Credit Facility of $10 billion, which expires on September 7, 2023. In November 202… |
| 2 | `JNJ_FY2022_2023-01-01:141` | Item 7 › Analysis of Consolidated Sales |  |  | For discussion on results of operations and financial condition pertaining to the fiscal years 2021 and 2020 see the Company’s Annual Report on Form 10-K for the fiscal year ended January 2, 2022, Item 7. Management's Di… |
| 3 | `JNJ_FY2022_2023-01-01:192` | Item 7 › Liquidity & Cash Flows |  | #1, #2 | As of January 1, 2023, the Company's notes payable and long-term debt was in excess of cash, cash equivalents and marketable securities. As of January 1, 2023, the net debt position was $16.1 billion as compared to the p… |
| 4 | `JNJ_FY2022_2023-01-01:344` | Item 8 › 7.Borrowings |  | #1 | Throughout fiscal years 2022 and 2021, the Company continued to have access to liquidity through the commercial paper market. Short-term borrowings and the current portion of long-term debt amounted to approximately $12.… |
| 5 | `JNJ_FY2022_2023-01-01:339` | Item 8 › 7.Borrowings |  |  | \| (Dollars in Millions) \| 2022 \| \| Effective Rate % \| \| 2021 \| \| Effective Rate % \| \| \|---\|---\|---\|---\|---\|---\|---\|---\|---\| \| 0.55% Notes due 2025 \| 918 \| \| 0.57 \| \| 983 \| \| 0.57 \| \| \| 2.45% Notes due 2026 \| 1,996 \| \| 2.… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#1 `JNJ_FY2022_2023-01-01:200`** (cited, gold #1, gold #2)

````text
Item 7.MANAGEMENT’S DISCUSSION AND ANALYSIS OF RESULTS OF OPERATIONS AND FINANCIAL CONDITION > Financing and Market Risk
The Company has access to substantial sources of funds at numerous banks worldwide. In September 2022, the Company secured a new 364-day Credit Facility of $10 billion, which expires on September 7, 2023. In November 2022, the Company secured an additional 364-day revolving Credit Facility of $10 billion, which has an expiration of November 21, 2023. Interest charged on borrowings under the credit line agreement is based on either Secured Overnight Financing Rate (SOFR) Reference Rate or other applicable market rate as allowed plus applicable margins. Commitment fees under the agreement are not material. Total borrowings at the end of 2022 and 2021 were $39.7 billion and $33.8 billion, respectively. The increase in borrowings was due to the acquisition of Abiomed, Inc. In 2022, net debt (cash and current marketable securities, net of debt) was $16.1 billion compared to net debt of $2.1 billion in 2021. Total debt represented 34.1% of total capital (shareholders’ equity and total debt) in 2022 and 31.3% of total capital in 2021. Shareholders’ equity per share at the end of 2022 was $29.39 compared to $28.16 at year-end 2021. A summary of borrowings can be found in Note 7 to the Consolidated Financial Statements.
````

**#3 `JNJ_FY2022_2023-01-01:192`** (gold #1, gold #2)

````text
Item 7.MANAGEMENT’S DISCUSSION AND ANALYSIS OF RESULTS OF OPERATIONS AND FINANCIAL CONDITION > Liquidity & Cash Flows
As of January 1, 2023, the Company's notes payable and long-term debt was in excess of cash, cash equivalents and marketable securities. As of January 1, 2023, the net debt position was $16.1 billion as compared to the prior year of $2.1 billion. The increase was primarily due to the acquisition of Abiomed, Inc. in December 2022. The debt balance at the end of 2022 was $39.7 billion as compared to $33.8 billion in 2021. Considering recent market conditions, the Company has re-evaluated its operating cash flows and liquidity profile and does not foresee any significant incremental risk. The Company anticipates that operating cash flows, the ability to raise funds from external sources, borrowing capacity from existing committed credit facilities and access to the commercial paper markets will continue to provide sufficient resources to fund operating needs, including the Company's remaining balance to be paid on the agreement to settle opioid litigation for approximately $2.7 billion and the establishment of the $2.0 billion trust for talc related liabilities (See Note 19 to the Consolidated Financial Statements for additional details). In addition, the Company monitors the global capital markets on an ongoing basis and from time to time may raise capital
````

**#4 `JNJ_FY2022_2023-01-01:344`** (gold #1)

````text
Item 8. FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA > 7.Borrowings
Throughout fiscal years 2022 and 2021, the Company continued to have access to liquidity through the commercial paper market. Short-term borrowings and the current portion of long-term debt amounted to approximately $12.8 billion and $3.8 billion at the end of fiscal years 2022 and 2021, respectively. The current portion of the long term debt was $1.6 billion and $2.1 billion in 2022 and 2021, respectively, and the remainder is commercial paper and local borrowing by international subsidiaries. The current debt balance as of January 1, 2023 includes $11.2 billion of commercial paper which has a weighted average interest rate of 4.23% and a weighted average maturity of approximately two months. Aggregate maturities of long-term debt obligations commencing in 2023 are:
````

</details>

RQ2 citation match (section level): `cited=[('JNJ', 'Item 7')] gold=[(None, 'Item 7')]`

### System C v1 (adaptive multi-hop)

Model: `gpt-5.4`. Hops: 3. Chunks retrieved: 10, cited: 1.

**Generated answer**

> Total borrowings increased from $33.8 billion in 2021 to $39.7 billion in 2022, which represents an increase of approximately 17.5% [JNJ FY2022, Item 7, JNJ_FY2022_2023-01-01:200].  
> The company identified the acquisition of Abiomed, Inc. as the driver of this increase [JNJ FY2022, Item 7, JNJ_FY2022_2023-01-01:200].

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `JNJ_FY2022_2023-01-01:200` | Item 7 › Financing and Market Risk | ✓ | #1, #2 | The Company has access to substantial sources of funds at numerous banks worldwide. In September 2022, the Company secured a new 364-day Credit Facility of $10 billion, which expires on September 7, 2023. In November 202… |
| 2 | `JNJ_FY2022_2023-01-01:342` | Item 8 › 7.Borrowings |  |  | \| (Dollars in Millions) \| 2022 \| \| Effective Rate % \| \| 2021 \| \| Effective Rate % \| \| \|---\|---\|---\|---\|---\|---\|---\|---\|---\| \| Total long-term debt \| $26,888 \| \| \| \| $29,985 \| \| \| \| |
| 3 | `JNJ_FY2022_2023-01-01:341` | Item 8 › 7.Borrowings |  |  | \| (Dollars in Millions) \| 2022 \| \| Effective Rate % \| \| 2021 \| \| Effective Rate % \| \| \|---\|---\|---\|---\|---\|---\|---\|---\|---\| \| 4.85% Notes due 2041 \| 297 \| \| 4.89 \| \| 297 \| \| 4.89 \| \| \| 4.50% Notes due 2043 \| 496 \| \| 4.52… |
| 4 | `JNJ_FY2022_2023-01-01:345` | Item 8 › 7.Borrowings |  |  | \| (Dollars in Millions) \| \| \| \| \| \| \|---\|---\|---\|---\|---\|---\| \| 2023 \| 2024 \| 2025 \| 2026 \| 2027 \| After 2026 \| \| $1,551 \| 1,392 \| 1,667 \| 1,996 \| 2,271 \| 19,562 \| |
| 5 | `JNJ_FY2022_2023-01-01:339` | Item 8 › 7.Borrowings |  |  | \| (Dollars in Millions) \| 2022 \| \| Effective Rate % \| \| 2021 \| \| Effective Rate % \| \| \|---\|---\|---\|---\|---\|---\|---\|---\|---\| \| 0.55% Notes due 2025 \| 918 \| \| 0.57 \| \| 983 \| \| 0.57 \| \| \| 2.45% Notes due 2026 \| 1,996 \| \| 2.… |
| 6 | `JNJ_FY2022_2023-01-01:340` | Item 8 › 7.Borrowings |  |  | \| (Dollars in Millions) \| 2022 \| \| Effective Rate % \| \| 2021 \| \| Effective Rate % \| \| \|---\|---\|---\|---\|---\|---\|---\|---\|---\| \| 4.375% Notes due 2033 \| 854 \| \| 4.24 \| \| 854 \| \| 4.24 \| \| \| 1.650% Notes due 2035 (1.5B Euro 1… |
| 7 | `JNJ_FY2022_2023-01-01:337` | Item 8 › 7.Borrowings |  |  | The components of long-term debt are as follows: |
| 8 | `JNJ_FY2022_2023-01-01:338` | Item 8 › 7.Borrowings |  |  | \| (Dollars in Millions) \| 2022 \| \| Effective Rate % \| \| 2021 \| \| Effective Rate % \| \| \|---\|---\|---\|---\|---\|---\|---\|---\|---\| \| 0.250% Notes due 2022 (1B Euro 1.1311)(3) \| $— \| \| —% \| \| $1,131 \| (3) \| 0.26% \| \| \| 2.25% Not… |
| 9 | `JNJ_FY2022_2023-01-01:344` | Item 8 › 7.Borrowings |  | #1 | Throughout fiscal years 2022 and 2021, the Company continued to have access to liquidity through the commercial paper market. Short-term borrowings and the current portion of long-term debt amounted to approximately $12.… |
| 10 | `JNJ_FY2022_2023-01-01:192` | Item 7 › Liquidity & Cash Flows |  | #1, #2 | As of January 1, 2023, the Company's notes payable and long-term debt was in excess of cash, cash equivalents and marketable securities. As of January 1, 2023, the net debt position was $16.1 billion as compared to the p… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#1 `JNJ_FY2022_2023-01-01:200`** (cited, gold #1, gold #2)

````text
Item 7.MANAGEMENT’S DISCUSSION AND ANALYSIS OF RESULTS OF OPERATIONS AND FINANCIAL CONDITION > Financing and Market Risk
The Company has access to substantial sources of funds at numerous banks worldwide. In September 2022, the Company secured a new 364-day Credit Facility of $10 billion, which expires on September 7, 2023. In November 2022, the Company secured an additional 364-day revolving Credit Facility of $10 billion, which has an expiration of November 21, 2023. Interest charged on borrowings under the credit line agreement is based on either Secured Overnight Financing Rate (SOFR) Reference Rate or other applicable market rate as allowed plus applicable margins. Commitment fees under the agreement are not material. Total borrowings at the end of 2022 and 2021 were $39.7 billion and $33.8 billion, respectively. The increase in borrowings was due to the acquisition of Abiomed, Inc. In 2022, net debt (cash and current marketable securities, net of debt) was $16.1 billion compared to net debt of $2.1 billion in 2021. Total debt represented 34.1% of total capital (shareholders’ equity and total debt) in 2022 and 31.3% of total capital in 2021. Shareholders’ equity per share at the end of 2022 was $29.39 compared to $28.16 at year-end 2021. A summary of borrowings can be found in Note 7 to the Consolidated Financial Statements.
````

**#9 `JNJ_FY2022_2023-01-01:344`** (gold #1)

````text
Item 8. FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA > 7.Borrowings
Throughout fiscal years 2022 and 2021, the Company continued to have access to liquidity through the commercial paper market. Short-term borrowings and the current portion of long-term debt amounted to approximately $12.8 billion and $3.8 billion at the end of fiscal years 2022 and 2021, respectively. The current portion of the long term debt was $1.6 billion and $2.1 billion in 2022 and 2021, respectively, and the remainder is commercial paper and local borrowing by international subsidiaries. The current debt balance as of January 1, 2023 includes $11.2 billion of commercial paper which has a weighted average interest rate of 4.23% and a weighted average maturity of approximately two months. Aggregate maturities of long-term debt obligations commencing in 2023 are:
````

**#10 `JNJ_FY2022_2023-01-01:192`** (gold #1, gold #2)

````text
Item 7.MANAGEMENT’S DISCUSSION AND ANALYSIS OF RESULTS OF OPERATIONS AND FINANCIAL CONDITION > Liquidity & Cash Flows
As of January 1, 2023, the Company's notes payable and long-term debt was in excess of cash, cash equivalents and marketable securities. As of January 1, 2023, the net debt position was $16.1 billion as compared to the prior year of $2.1 billion. The increase was primarily due to the acquisition of Abiomed, Inc. in December 2022. The debt balance at the end of 2022 was $39.7 billion as compared to $33.8 billion in 2021. Considering recent market conditions, the Company has re-evaluated its operating cash flows and liquidity profile and does not foresee any significant incremental risk. The Company anticipates that operating cash flows, the ability to raise funds from external sources, borrowing capacity from existing committed credit facilities and access to the commercial paper markets will continue to provide sufficient resources to fund operating needs, including the Company's remaining balance to be paid on the agreement to settle opioid litigation for approximately $2.7 billion and the establishment of the $2.0 billion trust for talc related liabilities (See Note 19 to the Consolidated Financial Statements for additional details). In addition, the Company monitors the global capital markets on an ongoing basis and from time to time may raise capital
````

</details>

RQ2 citation match (section level): `cited=[('JNJ', 'Item 7')] gold=[(None, 'Item 7')]`

**System C guardrail** (judge `gpt-5.4`): numerical claims 3, verified 3, ungrounded 0, uncited 0, derived 1; sentence verdicts: supported 1, partial 0, unsupported 0, unchecked 0.


<details><summary>Guardrail sentence verdicts</summary>

| sentence | verdict | judge reason |
|---|---|---|
| Total borrowings increased from $33.8 billion in 2021 to $39.7 billion in 2022, which represents an increase of approximately 17.5% [JNJ FY2022, Item 7, JNJ_FY2022_2023-01-01:200]. | None |  |
| The company identified the acquisition of Abiomed, Inc. as the driver of this increase [JNJ FY2022, Item 7, JNJ_FY2022_2023-01-01:200]. | supported | The cited text explicitly says the increase in borrowings was due to the acquisition of Abiomed, Inc. |

</details>

### System C v2 (agentic multi-hop + XBRL)

Model: `gpt-5.4`. Hops: 2. Chunks retrieved: 11, cited: 1.

**Generated answer**

> Johnson & Johnson reported total borrowings of $39.7 billion at the end of 2022 and $33.8 billion at the end of 2021. [JNJ FY2022, Item 7, JNJ_FY2022_2023-01-01:200]  
>
> The percentage increase in total borrowings from 2021 to 2022 was approximately 17.5% (($39.7 billion - $33.8 billion) / $33.8 billion). [JNJ FY2022, Item 7, JNJ_FY2022_2023-01-01:200]  
>
> The company identified the acquisition of Abiomed, Inc. as the driver of the increase in borrowings. [JNJ FY2022, Item 7, JNJ_FY2022_2023-01-01:200]

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `F-JNJ-2022` | SEC XBRL Reported Financials (financials.csv) |  |  | fiscal_year,fiscal_year_end,Revenue,NetIncome,OperatingIncome,TotalAssets,TotalLiabilities,StockholdersEquity,CashAndEquivalents,OperatingCashFlow,EPSDiluted 2022,2023-01-01,94943000000,17941000000,,187378000000,11057400… |
| 2 | `JNJ_FY2022_2023-01-01:200` | Item 7 › Financing and Market Risk | ✓ | #1, #2 | The Company has access to substantial sources of funds at numerous banks worldwide. In September 2022, the Company secured a new 364-day Credit Facility of $10 billion, which expires on September 7, 2023. In November 202… |
| 3 | `JNJ_FY2022_2023-01-01:342` | Item 8 › 7.Borrowings |  |  | \| (Dollars in Millions) \| 2022 \| \| Effective Rate % \| \| 2021 \| \| Effective Rate % \| \| \|---\|---\|---\|---\|---\|---\|---\|---\|---\| \| Total long-term debt \| $26,888 \| \| \| \| $29,985 \| \| \| \| |
| 4 | `JNJ_FY2022_2023-01-01:341` | Item 8 › 7.Borrowings |  |  | \| (Dollars in Millions) \| 2022 \| \| Effective Rate % \| \| 2021 \| \| Effective Rate % \| \| \|---\|---\|---\|---\|---\|---\|---\|---\|---\| \| 4.85% Notes due 2041 \| 297 \| \| 4.89 \| \| 297 \| \| 4.89 \| \| \| 4.50% Notes due 2043 \| 496 \| \| 4.52… |
| 5 | `JNJ_FY2022_2023-01-01:345` | Item 8 › 7.Borrowings |  |  | \| (Dollars in Millions) \| \| \| \| \| \| \|---\|---\|---\|---\|---\|---\| \| 2023 \| 2024 \| 2025 \| 2026 \| 2027 \| After 2026 \| \| $1,551 \| 1,392 \| 1,667 \| 1,996 \| 2,271 \| 19,562 \| |
| 6 | `JNJ_FY2022_2023-01-01:339` | Item 8 › 7.Borrowings |  |  | \| (Dollars in Millions) \| 2022 \| \| Effective Rate % \| \| 2021 \| \| Effective Rate % \| \| \|---\|---\|---\|---\|---\|---\|---\|---\|---\| \| 0.55% Notes due 2025 \| 918 \| \| 0.57 \| \| 983 \| \| 0.57 \| \| \| 2.45% Notes due 2026 \| 1,996 \| \| 2.… |
| 7 | `JNJ_FY2022_2023-01-01:340` | Item 8 › 7.Borrowings |  |  | \| (Dollars in Millions) \| 2022 \| \| Effective Rate % \| \| 2021 \| \| Effective Rate % \| \| \|---\|---\|---\|---\|---\|---\|---\|---\|---\| \| 4.375% Notes due 2033 \| 854 \| \| 4.24 \| \| 854 \| \| 4.24 \| \| \| 1.650% Notes due 2035 (1.5B Euro 1… |
| 8 | `JNJ_FY2022_2023-01-01:344` | Item 8 › 7.Borrowings |  | #1 | Throughout fiscal years 2022 and 2021, the Company continued to have access to liquidity through the commercial paper market. Short-term borrowings and the current portion of long-term debt amounted to approximately $12.… |
| 9 | `JNJ_FY2022_2023-01-01:192` | Item 7 › Liquidity & Cash Flows |  | #1, #2 | As of January 1, 2023, the Company's notes payable and long-term debt was in excess of cash, cash equivalents and marketable securities. As of January 1, 2023, the net debt position was $16.1 billion as compared to the p… |
| 10 | `JNJ_FY2022_2023-01-01:337` | Item 8 › 7.Borrowings |  |  | The components of long-term debt are as follows: |
| 11 | `JNJ_FY2022_2023-01-01:295` | Item 8 › 2.Cash, Cash Equivalents and Current Marketable Securities |  |  | \| (Dollars in Millions) \| Cost Basis \| Fair Value \| \|---\|---\|---\| \| Due within one year \| $10,430 \| 10,399 \| \| Due after one year through five years \| 91 \| 88 \| \| Due after five years through ten years \| — \| — \| \| Total … |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#2 `JNJ_FY2022_2023-01-01:200`** (cited, gold #1, gold #2)

````text
Item 7.MANAGEMENT’S DISCUSSION AND ANALYSIS OF RESULTS OF OPERATIONS AND FINANCIAL CONDITION > Financing and Market Risk
The Company has access to substantial sources of funds at numerous banks worldwide. In September 2022, the Company secured a new 364-day Credit Facility of $10 billion, which expires on September 7, 2023. In November 2022, the Company secured an additional 364-day revolving Credit Facility of $10 billion, which has an expiration of November 21, 2023. Interest charged on borrowings under the credit line agreement is based on either Secured Overnight Financing Rate (SOFR) Reference Rate or other applicable market rate as allowed plus applicable margins. Commitment fees under the agreement are not material. Total borrowings at the end of 2022 and 2021 were $39.7 billion and $33.8 billion, respectively. The increase in borrowings was due to the acquisition of Abiomed, Inc. In 2022, net debt (cash and current marketable securities, net of debt) was $16.1 billion compared to net debt of $2.1 billion in 2021. Total debt represented 34.1% of total capital (shareholders’ equity and total debt) in 2022 and 31.3% of total capital in 2021. Shareholders’ equity per share at the end of 2022 was $29.39 compared to $28.16 at year-end 2021. A summary of borrowings can be found in Note 7 to the Consolidated Financial Statements.
````

**#8 `JNJ_FY2022_2023-01-01:344`** (gold #1)

````text
Item 8. FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA > 7.Borrowings
Throughout fiscal years 2022 and 2021, the Company continued to have access to liquidity through the commercial paper market. Short-term borrowings and the current portion of long-term debt amounted to approximately $12.8 billion and $3.8 billion at the end of fiscal years 2022 and 2021, respectively. The current portion of the long term debt was $1.6 billion and $2.1 billion in 2022 and 2021, respectively, and the remainder is commercial paper and local borrowing by international subsidiaries. The current debt balance as of January 1, 2023 includes $11.2 billion of commercial paper which has a weighted average interest rate of 4.23% and a weighted average maturity of approximately two months. Aggregate maturities of long-term debt obligations commencing in 2023 are:
````

**#9 `JNJ_FY2022_2023-01-01:192`** (gold #1, gold #2)

````text
Item 7.MANAGEMENT’S DISCUSSION AND ANALYSIS OF RESULTS OF OPERATIONS AND FINANCIAL CONDITION > Liquidity & Cash Flows
As of January 1, 2023, the Company's notes payable and long-term debt was in excess of cash, cash equivalents and marketable securities. As of January 1, 2023, the net debt position was $16.1 billion as compared to the prior year of $2.1 billion. The increase was primarily due to the acquisition of Abiomed, Inc. in December 2022. The debt balance at the end of 2022 was $39.7 billion as compared to $33.8 billion in 2021. Considering recent market conditions, the Company has re-evaluated its operating cash flows and liquidity profile and does not foresee any significant incremental risk. The Company anticipates that operating cash flows, the ability to raise funds from external sources, borrowing capacity from existing committed credit facilities and access to the commercial paper markets will continue to provide sufficient resources to fund operating needs, including the Company's remaining balance to be paid on the agreement to settle opioid litigation for approximately $2.7 billion and the establishment of the $2.0 billion trust for talc related liabilities (See Note 19 to the Consolidated Financial Statements for additional details). In addition, the Company monitors the global capital markets on an ongoing basis and from time to time may raise capital
````

</details>

RQ2 citation match (section level): `cited=[('JNJ', 'Item 7')] gold=[(None, 'Item 7')]`

**System C guardrail** (judge `gpt-5.4`): numerical claims 6, verified 6, ungrounded 0, uncited 0, derived 1; sentence verdicts: supported 1, partial 0, unsupported 0, unchecked 0.


<details><summary>Guardrail sentence verdicts</summary>

| sentence | verdict | judge reason |
|---|---|---|
| Johnson & Johnson reported total borrowings of $39.7 billion at the end of 2022 and $33.8 billion at the end of 2021. [JNJ FY2022, Item 7, JNJ_FY2022_2023-01-01:200] | None |  |
| The percentage increase in total borrowings from 2021 to 2022 was approximately 17.5% (($39.7 billion - $33.8 billion) / $33.8 billion). [JNJ FY2022, Item 7, JNJ_FY2022_2023-01-01:200] | None |  |
| The company identified the acquisition of Abiomed, Inc. as the driver of the increase in borrowings. [JNJ FY2022, Item 7, JNJ_FY2022_2023-01-01:200] | supported | The cited text explicitly states that the increase in borrowings was due to the acquisition of Abiomed, Inc. |

</details>
