# gold-089: Cross-company table

[← all cases](../README.md) · company: AMAZON COM INC; Apple Inc. (AMZN, AAPL) · fiscal year: 2020 · recipe `cross_company_table` · hop `multi` · answer type `numeric` · scope `cross_company` · RQ2 category `cross_section_multihop`

## Gold QA

**Question**

> As of the end of fiscal year 2020, by how many millions of dollars did Apple's total term debt exceed Amazon's total long-term debt, based on each company's schedule of future principal payments?

**Gold answer**

> $72,904 million

**Program**: `subtract(106078, 33174)` → `72904.0`

**Gold numbers** (RQ2 numeric_accuracy targets): $72,904 million

**Gold evidence**

1. `AMZN_FY2020_2020-12-31` · Item 8. Financial Statements and Supplementary Data › Note 6 — DEBT · table

   > |  | $33,174 |

2. `AAPL_FY2020_2020-09-26` · Item 8. Financial Statements and Supplementary Data › Term Debt · table

   > | Total term debt | $106,078 |

## Scorecard

| Metric | A (vanilla dense) | B (hybrid + rerank) | C v1 (adaptive multi-hop) | C v2 (agentic multi-hop + XBRL) |
|---|---|---|---|---|
| **Retrieval (RQ1)** | | | | |
| chunks retrieved | 8 | 5 | 13 | 8 |
| recall@5 | 0.50 | 0.00 | 0.50 | 0.50 |
| recall@all | 0.50 | 0.00 | 1.00 | 0.50 |
| complete@all | 0 | 0 | 1 | 0 |
| average precision (lexical) | 0.89 | 0.00 | 0.89 | 0.48 |
| gold evidence first rank | #1: –, #2: 1 | #1: –, #2: – | #1: 7, #2: 1 | #1: –, #2: 3 |
| **Answer (RQ3 string match)** | | | | |
| numeric_correct | ✗ | ✗ | ✓ | ✗ |
| keypoint_recall | – | – | – | – |
| **Answer & citations (RQ2)** | | | | |
| numeric_accuracy | 0.00 | 0.00 | 1.00 | 0.00 |
| citation precision | 0.50 | 1.00 | 1.00 | 1.00 |
| citation recall | 1.00 | 1.00 | 1.00 | 1.00 |
| citation F1 | 0.67 | 1.00 | 1.00 | 1.00 |
| has a citation | 1 | 1 | 1 | 1 |
| grounding error rate | – | – | 0.00 | 0.00 |
| **Cost (RQ3)** | | | | |
| retrieval hops | 1 | 1 | 3 | 1 |
| tokens | 2337 | 1059 | 14047 | 7050 |
| cost (USD) | 0.0004 | 0.0002 | 0.0503 | 0.0242 |
| latency (s) | 2.8 | 7.2 | 21.4 | 11.0 |

Definitions: [README › Metrics](../README.md#metrics). `–` = not applicable (e.g. no gold number, no citations, no guardrail).

## System outputs

### System A (vanilla dense)

Model: `gpt-5.4-2026-03-05`. Hops: 1. Chunks retrieved: 8, cited: 3.

**Generated answer**

> The context provides Apple’s total term debt as **$106,078 million** as of fiscal year 2020 [1][2][3]. However, it does **not** provide Amazon’s total long-term debt or its schedule of future principal payments, so the difference cannot be calculated from the provided context.
>
> Available part:
> - **Apple total term debt (FY2020): $106,078 million** [1][2][3]
>
> Missing from context:
> - **Amazon’s total long-term debt / schedule of future principal payments**

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `AAPL_FY2020_2020-09-26:270` | Item 8 › Term Debt | ✓ | #2 | \| 2021 \| $8,750 \| \|---\|---\| \| 2022 \| 9,569 \| \| 2023 \| 11,389 \| \| 2024 \| 10,115 \| \| 2025 \| 10,914 \| \| Thereafter \| 55,341 \| \| Total term debt \| $106,078 \| |
| 2 | `AAPL_FY2020_2020-09-26:267` | Item 8 › Term Debt | ✓ | #2 | \| \| Maturities (calendar year) \| 2020 \| \| 2019 \| \| \|---\|---\|---\|---\|---\|---\| \| \| Amount (in millions) \| Effective Interest Rate \| Amount (in millions) \| Effective Interest Rate \| \| \| Total term debt \| \| 106,078 \| \| 101,6… |
| 3 | `AAPL_FY2020_2020-09-26:143` | Item 7 › Contractual Obligations | ✓ | #2 | \| \| Payments due in 2021 \| Payments due in 2022–2023 \| Payments due in 2024–2025 \| Payments due after 2025 \| Total \| \|---\|---\|---\|---\|---\|---\| \| Term debt \| $8,750 \| $20,958 \| $21,029 \| $55,341 \| $106,078 \| \| Leases \| 1,… |
| 4 | `AAPL_FY2020_2020-09-26:266` | Item 8 › Term Debt |  |  | \| \| Maturities (calendar year) \| 2020 \| \| 2019 \| \| \|---\|---\|---\|---\|---\|---\| \| \| Amount (in millions) \| Effective Interest Rate \| Amount (in millions) \| Effective Interest Rate \| \| \| 2013 – 2019 debt issuances: \| \| \| \| \|… |
| 5 | `AAPL_FY2020_2020-09-26:265` | Item 8 › Term Debt |  |  | As of September 26, 2020, the Company had outstanding floating- and fixed-rate notes with varying maturities for an aggregate principal amount of $106.1 billion (collectively the “Notes”). The Notes are senior unsecured … |
| 6 | `AAPL_FY2020_2020-09-26:269` | Item 8 › Term Debt |  |  | The effective interest rates for the Notes include the interest on the Notes, amortization of the discount or premium and, if applicable, adjustments related to hedging. The Company recognized $2.8 billion, $3.2 billion … |
| 7 | `AAPL_FY2020_2020-09-26:106` | Item 6 |  | #2 | \| \| 2020 \| 2019 \| 2018 \| 2017 \| 2016 \| \|---\|---\|---\|---\|---\|---\| \| Total net sales \| $274,515 \| $260,174 \| $265,595 \| $229,234 \| $215,639 \| \| Net income \| $57,411 \| $55,256 \| $59,531 \| $48,351 \| $45,687 \| \| Earnings per … |
| 8 | `AAPL_FY2020_2020-09-26:165` | Item 8 › CONSOLIDATED STATEMENTS OF OPERATIONS |  |  | \| \| Years ended \| \| \| \|---\|---\|---\|---\| \| \| September 26, 2020 \| September 28, 2019 \| September 29, 2018 \| \| Net sales: \| \| \| \| \| Products \| $220,747 \| $213,883 \| $225,847 \| \| Services \| 53,768 \| 46,291 \| 39,748 \| \| Tota… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#1 `AAPL_FY2020_2020-09-26:270`** (cited, gold #2)

````text
Item 8. Financial Statements and Supplementary Data > Term Debt (table)
| 2021 | $8,750 |
|---|---|
| 2022 | 9,569 |
| 2023 | 11,389 |
| 2024 | 10,115 |
| 2025 | 10,914 |
| Thereafter | 55,341 |
| Total term debt | $106,078 |
````

**#2 `AAPL_FY2020_2020-09-26:267`** (cited, gold #2)

````text
Item 8. Financial Statements and Supplementary Data > Term Debt (table)
|  | Maturities (calendar year) | 2020 |  | 2019 |  |
|---|---|---|---|---|---|
|  | Amount (in millions) | Effective Interest Rate | Amount (in millions) | Effective Interest Rate |  |
| Total term debt |  | 106,078 |  | 101,679 |  |
| Unamortized premium/(discount) and issuance costs, net |  | (314) |  | (224) |  |
| Hedge accounting fair value adjustments |  | 1,676 |  | 612 |  |
| Less: Current portion of term debt |  | (8,773) |  | (10,260) |  |
| Total non-current portion of term debt |  | $98,667 |  | $91,807 |  |
````

**#3 `AAPL_FY2020_2020-09-26:143`** (cited, gold #2)

````text
Item 7. Management’s Discussion and Analysis of Financial Condition and Results of Operations > Contractual Obligations (table)
|  | Payments due in 2021 | Payments due in 2022–2023 | Payments due in 2024–2025 | Payments due after 2025 | Total |
|---|---|---|---|---|---|
| Term debt | $8,750 | $20,958 | $21,029 | $55,341 | $106,078 |
| Leases | 1,622 | 3,097 | 2,352 | 5,888 | 12,959 |
| Manufacturing purchase obligations (1) | 47,961 | 1,849 | 61 | 40 | 49,911 |
| Other purchase obligations | 6,178 | 2,736 | 400 | 90 | 9,404 |
| Deemed repatriation tax payable | 1,533 | 5,923 | 12,955 | 9,254 | 29,665 |
| Total | $66,044 | $34,563 | $36,797 | $70,613 | $208,017 |
````

**#7 `AAPL_FY2020_2020-09-26:106`** (gold #2)

````text
Item 6. Selected Financial Data (table)
|  | 2020 | 2019 | 2018 | 2017 | 2016 |
|---|---|---|---|---|---|
| Total net sales | $274,515 | $260,174 | $265,595 | $229,234 | $215,639 |
| Net income | $57,411 | $55,256 | $59,531 | $48,351 | $45,687 |
| Earnings per share: |  |  |  |  |  |
| Basic | $3.31 | $2.99 | $3.00 | $2.32 | $2.09 |
| Diluted | $3.28 | $2.97 | $2.98 | $2.30 | $2.08 |
| Cash dividends declared per share | $0.795 | $0.75 | $0.68 | $0.60 | $0.545 |
| Shares used in computing earnings per share: |  |  |  |  |  |
| Basic | 17,352,119 | 18,471,336 | 19,821,510 | 20,868,968 | 21,883,281 |
| Diluted | 17,528,214 | 18,595,651 | 20,000,435 | 21,006,767 | 22,001,126 |
| Total cash, cash equivalents and marketable securities | $191,830 | $205,898 | $237,100 | $268,895 | $237,585 |
| Total assets | $323,888 | $338,516 | $365,725 | $375,319 | $321,686 |
| Non-current portion of term debt | $98,667 | $91,807 | $93,735 | $97,207 | $75,427 |
| Other non-current liabilities | $54,490 | $50,503 | $48,914 | $44,212 | $39,986 |
````

</details>

RQ2 citation match (section level): `cited=[('AAPL', 'Item 8'), ('AAPL', 'Item 7')] gold=[(None, 'Item 8')]`

### System B (hybrid + rerank)

Model: `gpt-5.4-2026-03-05`. Hops: 1. Chunks retrieved: 5, cited: 2.

**Generated answer**

> Apple’s total term debt was $106.1 billion, and Amazon’s total long-term debt was $31.816 billion as of fiscal year 2020 [4][3].
>
> Difference = $106.1 billion − $31.816 billion = $74.284 billion, or **$74,284 million** [4][3].

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `AAPL_FY2020_2020-09-26:269` | Item 8 › Term Debt |  |  | The effective interest rates for the Notes include the interest on the Notes, amortization of the discount or premium and, if applicable, adjustments related to hedging. The Company recognized $2.8 billion, $3.2 billion … |
| 2 | `AMZN_FY2020_2020-12-31:280` | Item 8 › Note 6 — DEBT |  |  | Other long-term debt, including the current portion, had a weighted-average interest rate of 4.1% and 2.9% as of December 31, 2019 and 2020. We used the net proceeds from the issuance of this debt primarily to fund certa… |
| 3 | `AMZN_FY2020_2020-12-31:187` | Item 8 › (in millions, except per share data) | ✓ |  | \| \| December 31, \| \| \|---\|---\|---\| \| \| 2019 \| 2020 \| \| ASSETS \| \| \| \| Current assets: \| \| \| \| Cash and cash equivalents \| $36,092 \| $42,122 \| \| Marketable securities \| 18,929 \| 42,274 \| \| Inventories \| 20,497 \| 23,795 \| … |
| 4 | `AAPL_FY2020_2020-09-26:265` | Item 8 › Term Debt | ✓ |  | As of September 26, 2020, the Company had outstanding floating- and fixed-rate notes with varying maturities for an aggregate principal amount of $106.1 billion (collectively the “Notes”). The Notes are senior unsecured … |
| 5 | `AAPL_FY2020_2020-09-26:271` | Item 8 › Term Debt |  |  | As of September 26, 2020 and September 28, 2019, the fair value of the Company’s Notes, based on Level 2 inputs, was $117.1 billion and $107.5 billion, respectively. Apple Inc. \| 2020 Form 10-K \| 49 |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#3 `AMZN_FY2020_2020-12-31:187`** (cited)

````text
Item 8. Financial Statements and Supplementary Data > (in millions, except per share data) (table)
|  | December 31, |  |
|---|---|---|
|  | 2019 | 2020 |
| ASSETS |  |  |
| Current assets: |  |  |
| Cash and cash equivalents | $36,092 | $42,122 |
| Marketable securities | 18,929 | 42,274 |
| Inventories | 20,497 | 23,795 |
| Accounts receivable, net and other | 20,816 | 24,542 |
| Total current assets | 96,334 | 132,733 |
| Property and equipment, net | 72,705 | 113,114 |
| Operating leases | 25,141 | 37,553 |
| Goodwill | 14,754 | 15,017 |
| Other assets | 16,314 | 22,778 |
| Total assets | $225,248 | $321,195 |
| LIABILITIES AND STOCKHOLDERS’ EQUITY |  |  |
| Current liabilities: |  |  |
| Accounts payable | $47,183 | $72,539 |
| Accrued expenses and other | 32,439 | 44,138 |
| Unearned revenue | 8,190 | 9,708 |
| Total current liabilities | 87,812 | 126,385 |
| Long-term lease liabilities | 39,791 | 52,573 |
| Long-term debt | 23,414 | 31,816 |
| Other long-term liabilities | 12,171 | 17,017 |
| Commitments and contingencies (Note 7) |  |  |
| Stockholders’ equity: |  |  |
````

**#4 `AAPL_FY2020_2020-09-26:265`** (cited)

````text
Item 8. Financial Statements and Supplementary Data > Term Debt
As of September 26, 2020, the Company had outstanding floating- and fixed-rate notes with varying maturities for an aggregate principal amount of $106.1 billion (collectively the “Notes”). The Notes are senior unsecured obligations and interest is payable in arrears. The following table provides a summary of the Company’s term debt as of September 26, 2020 and September 28, 2019:
````

</details>

RQ2 citation match (section level): `cited=[('AMZN', 'Item 8'), ('AAPL', 'Item 8')] gold=[(None, 'Item 8')]`

### System C v1 (adaptive multi-hop)

Model: `gpt-5.4`. Hops: 3. Chunks retrieved: 13, cited: 2.

**Generated answer**

> Apple’s schedule of future principal payments showed total term debt of $106,078 million as of September 26, 2020, while Amazon’s schedule of future principal payments showed total face value of long-term debt of $33,174 million as of December 31, 2020 [AAPL FY2020, Item 8, AAPL_FY2020_2020-09-26:270] [AMZN FY2020, Item 8, AMZN_FY2020_2020-12-31:277].  
> Therefore, Apple’s total term debt exceeded Amazon’s total long-term debt by $72,904 million [AAPL FY2020, Item 8, AAPL_FY2020_2020-09-26:270] [AMZN FY2020, Item 8, AMZN_FY2020_2020-12-31:277].

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `AAPL_FY2020_2020-09-26:270` | Item 8 › Term Debt | ✓ | #2 | \| 2021 \| $8,750 \| \|---\|---\| \| 2022 \| 9,569 \| \| 2023 \| 11,389 \| \| 2024 \| 10,115 \| \| 2025 \| 10,914 \| \| Thereafter \| 55,341 \| \| Total term debt \| $106,078 \| |
| 2 | `AAPL_FY2020_2020-09-26:143` | Item 7 › Contractual Obligations |  | #2 | \| \| Payments due in 2021 \| Payments due in 2022–2023 \| Payments due in 2024–2025 \| Payments due after 2025 \| Total \| \|---\|---\|---\|---\|---\|---\| \| Term debt \| $8,750 \| $20,958 \| $21,029 \| $55,341 \| $106,078 \| \| Leases \| 1,… |
| 3 | `AAPL_FY2020_2020-09-26:267` | Item 8 › Term Debt |  | #2 | \| \| Maturities (calendar year) \| 2020 \| \| 2019 \| \| \|---\|---\|---\|---\|---\|---\| \| \| Amount (in millions) \| Effective Interest Rate \| Amount (in millions) \| Effective Interest Rate \| \| \| Total term debt \| \| 106,078 \| \| 101,6… |
| 4 | `AAPL_FY2020_2020-09-26:266` | Item 8 › Term Debt |  |  | \| \| Maturities (calendar year) \| 2020 \| \| 2019 \| \| \|---\|---\|---\|---\|---\|---\| \| \| Amount (in millions) \| Effective Interest Rate \| Amount (in millions) \| Effective Interest Rate \| \| \| 2013 – 2019 debt issuances: \| \| \| \| \|… |
| 5 | `AAPL_FY2020_2020-09-26:269` | Item 8 › Term Debt |  |  | The effective interest rates for the Notes include the interest on the Notes, amortization of the discount or premium and, if applicable, adjustments related to hedging. The Company recognized $2.8 billion, $3.2 billion … |
| 6 | `AAPL_FY2020_2020-09-26:265` | Item 8 › Term Debt |  |  | As of September 26, 2020, the Company had outstanding floating- and fixed-rate notes with varying maturities for an aggregate principal amount of $106.1 billion (collectively the “Notes”). The Notes are senior unsecured … |
| 7 | `AMZN_FY2020_2020-12-31:277` | Item 8 › Note 6 — DEBT | ✓ | #1 | \| \| Maturities (1) \| Stated Interest Rates \| Effective Interest Rates \| December 31, 2019 \| December 31, 2020 \| \|---\|---\|---\|---\|---\|---\| \| 2012 Notes issuance of $3.0 billion \| 2022 \| 2.50% \| 2.66% \| 1,250 \| 1,250 \| \| 2… |
| 8 | `AMZN_FY2020_2020-12-31:285` | Item 8 › Commitments |  |  | \| \| Year Ended December 31, \| \| \| \| \| \| \| \|---\|---\|---\|---\|---\|---\|---\|---\| \| \| 2021 \| 2022 \| 2023 \| 2024 \| 2025 \| Thereafter \| Total \| \| Long-term debt principal and interest \| $2,187 \| $2,622 \| $3,219 \| $4,272 \| $3,058… |
| 9 | `AMZN_FY2020_2020-12-31:276` | Item 8 › Note 6 — DEBT |  |  | As of December 31, 2020, we had $32.2 billion of unsecured senior notes outstanding (the “Notes”), including $10.0 billion issued in June 2020 for general corporate purposes. We also have other long-term debt and borrowi… |
| 10 | `AMZN_FY2020_2020-12-31:280` | Item 8 › Note 6 — DEBT |  |  | Other long-term debt, including the current portion, had a weighted-average interest rate of 4.1% and 2.9% as of December 31, 2019 and 2020. We used the net proceeds from the issuance of this debt primarily to fund certa… |
| 11 | `AMZN_FY2020_2020-12-31:187` | Item 8 › (in millions, except per share data) |  |  | \| \| December 31, \| \| \|---\|---\|---\| \| \| 2019 \| 2020 \| \| ASSETS \| \| \| \| Current assets: \| \| \| \| Cash and cash equivalents \| $36,092 \| $42,122 \| \| Marketable securities \| 18,929 \| 42,274 \| \| Inventories \| 20,497 \| 23,795 \| … |
| 12 | `AMZN_FY2020_2020-12-31:178` | Item 8 › (in millions) |  |  | \| \| Year Ended December 31, \| \| \| \|---\|---\|---\|---\| \| \| 2018 \| 2019 \| 2020 \| \| Unearned revenue \| 1,151 \| 1,711 \| 1,265 \| \| Net cash provided by (used in) operating activities \| 30,723 \| 38,514 \| 66,064 \| \| INVESTING ACT… |
| 13 | `AMZN_FY2020_2020-12-31:164` | Item 7A › Interest Rate Risk |  |  | As of December 31, 2020, we had long-term debt with a face value of $33.2 billion, including the current portion, primarily consisting of fixed rate unsecured senior notes. See Item 8 of Part II, “Financial Statements an… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#1 `AAPL_FY2020_2020-09-26:270`** (cited, gold #2)

````text
Item 8. Financial Statements and Supplementary Data > Term Debt (table)
| 2021 | $8,750 |
|---|---|
| 2022 | 9,569 |
| 2023 | 11,389 |
| 2024 | 10,115 |
| 2025 | 10,914 |
| Thereafter | 55,341 |
| Total term debt | $106,078 |
````

**#2 `AAPL_FY2020_2020-09-26:143`** (gold #2)

````text
Item 7. Management’s Discussion and Analysis of Financial Condition and Results of Operations > Contractual Obligations (table)
|  | Payments due in 2021 | Payments due in 2022–2023 | Payments due in 2024–2025 | Payments due after 2025 | Total |
|---|---|---|---|---|---|
| Term debt | $8,750 | $20,958 | $21,029 | $55,341 | $106,078 |
| Leases | 1,622 | 3,097 | 2,352 | 5,888 | 12,959 |
| Manufacturing purchase obligations (1) | 47,961 | 1,849 | 61 | 40 | 49,911 |
| Other purchase obligations | 6,178 | 2,736 | 400 | 90 | 9,404 |
| Deemed repatriation tax payable | 1,533 | 5,923 | 12,955 | 9,254 | 29,665 |
| Total | $66,044 | $34,563 | $36,797 | $70,613 | $208,017 |
````

**#3 `AAPL_FY2020_2020-09-26:267`** (gold #2)

````text
Item 8. Financial Statements and Supplementary Data > Term Debt (table)
|  | Maturities (calendar year) | 2020 |  | 2019 |  |
|---|---|---|---|---|---|
|  | Amount (in millions) | Effective Interest Rate | Amount (in millions) | Effective Interest Rate |  |
| Total term debt |  | 106,078 |  | 101,679 |  |
| Unamortized premium/(discount) and issuance costs, net |  | (314) |  | (224) |  |
| Hedge accounting fair value adjustments |  | 1,676 |  | 612 |  |
| Less: Current portion of term debt |  | (8,773) |  | (10,260) |  |
| Total non-current portion of term debt |  | $98,667 |  | $91,807 |  |
````

**#7 `AMZN_FY2020_2020-12-31:277`** (cited, gold #1)

````text
Item 8. Financial Statements and Supplementary Data > Note 6 — DEBT (table)
|  | Maturities (1) | Stated Interest Rates | Effective Interest Rates | December 31, 2019 | December 31, 2020 |
|---|---|---|---|---|---|
| 2012 Notes issuance of $3.0 billion | 2022 | 2.50% | 2.66% | 1,250 | 1,250 |
| 2014 Notes issuance of $6.0 billion | 2021 - 2044 | 3.30% - 4.95% | 3.43% - 5.11% | 5,000 | 5,000 |
| 2017 Notes issuance of $17.0 billion | 2023 - 2057 | 2.40% - 5.20% | 2.56% - 4.33% | 17,000 | 16,000 |
| 2020 Notes issuance of $10.0 billion | 2023 - 2060 | 0.40% - 2.70% | 0.56% - 2.77% | — | 10,000 |
| Credit Facility |  |  |  | 740 | 338 |
| Other long-term debt |  |  |  | 830 | 586 |
| Total face value of long-term debt |  |  |  | 24,820 | 33,174 |
| Unamortized discount and issuance costs, net |  |  |  | (101) | (203) |
| Less current portion of long-term debt |  |  |  | (1,305) | (1,155) |
| Long-term debt |  |  |  | $23,414 | $31,816 |
````

</details>

RQ2 citation match (section level): `cited=[('AAPL', 'Item 8'), ('AMZN', 'Item 8')] gold=[(None, 'Item 8')]`

**System C guardrail** (judge `gpt-5.4`): numerical claims 3, verified 3, ungrounded 0, uncited 0, derived 1; sentence verdicts: supported 0, partial 0, unsupported 0, unchecked 0.


<details><summary>Guardrail sentence verdicts</summary>

| sentence | verdict | judge reason |
|---|---|---|
| Apple’s schedule of future principal payments showed total term debt of $106,078 million as of September 26, 2020, while Amazon’s schedule of future principal payments showed total face value of long-term debt of $33,174 million as of December 31, 2020 [AAPL FY2020, Item 8, AAPL_FY2020_2020-09-26:270] [AMZN FY2020, Item 8, AMZN_FY2020_2020-12-31:277]. | None |  |
| Therefore, Apple’s total term debt exceeded Amazon’s total long-term debt by $72,904 million [AAPL FY2020, Item 8, AAPL_FY2020_2020-09-26:270] [AMZN FY2020, Item 8, AMZN_FY2020_2020-12-31:277]. | None |  |

</details>

### System C v2 (agentic multi-hop + XBRL)

Model: `gpt-5.4`. Hops: 1. Chunks retrieved: 8, cited: 1.

**Generated answer**

> Apple’s total term debt was $106,078 million as of September 26, 2020, based on its schedule of future principal payments [AAPL FY2020, Item 8, AAPL_FY2020_2020-09-26:270].  
>
> The filing does not disclose Amazon’s total long-term debt or a schedule of future principal payments, so the difference cannot be determined from the provided evidence.

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `F-AAPL-2020` | SEC XBRL Reported Financials (financials.csv) |  |  | fiscal_year,fiscal_year_end,Revenue,NetIncome,OperatingIncome,TotalAssets,TotalLiabilities,StockholdersEquity,CashAndEquivalents,OperatingCashFlow,EPSDiluted 2020,2020-09-26,274515000000,57411000000,66288000000,323888000… |
| 2 | `F-AMZN-2020` | SEC XBRL Reported Financials (financials.csv) |  |  | fiscal_year,fiscal_year_end,Revenue,NetIncome,OperatingIncome,TotalAssets,TotalLiabilities,StockholdersEquity,CashAndEquivalents,OperatingCashFlow,EPSDiluted 2020,2020-12-31,386064000000,21331000000,22899000000,321195000… |
| 3 | `AAPL_FY2020_2020-09-26:270` | Item 8 › Term Debt | ✓ | #2 | \| 2021 \| $8,750 \| \|---\|---\| \| 2022 \| 9,569 \| \| 2023 \| 11,389 \| \| 2024 \| 10,115 \| \| 2025 \| 10,914 \| \| Thereafter \| 55,341 \| \| Total term debt \| $106,078 \| |
| 4 | `AAPL_FY2020_2020-09-26:143` | Item 7 › Contractual Obligations |  | #2 | \| \| Payments due in 2021 \| Payments due in 2022–2023 \| Payments due in 2024–2025 \| Payments due after 2025 \| Total \| \|---\|---\|---\|---\|---\|---\| \| Term debt \| $8,750 \| $20,958 \| $21,029 \| $55,341 \| $106,078 \| \| Leases \| 1,… |
| 5 | `AAPL_FY2020_2020-09-26:267` | Item 8 › Term Debt |  | #2 | \| \| Maturities (calendar year) \| 2020 \| \| 2019 \| \| \|---\|---\|---\|---\|---\|---\| \| \| Amount (in millions) \| Effective Interest Rate \| Amount (in millions) \| Effective Interest Rate \| \| \| Total term debt \| \| 106,078 \| \| 101,6… |
| 6 | `AAPL_FY2020_2020-09-26:266` | Item 8 › Term Debt |  |  | \| \| Maturities (calendar year) \| 2020 \| \| 2019 \| \| \|---\|---\|---\|---\|---\|---\| \| \| Amount (in millions) \| Effective Interest Rate \| Amount (in millions) \| Effective Interest Rate \| \| \| 2013 – 2019 debt issuances: \| \| \| \| \|… |
| 7 | `AAPL_FY2020_2020-09-26:269` | Item 8 › Term Debt |  |  | The effective interest rates for the Notes include the interest on the Notes, amortization of the discount or premium and, if applicable, adjustments related to hedging. The Company recognized $2.8 billion, $3.2 billion … |
| 8 | `AAPL_FY2020_2020-09-26:265` | Item 8 › Term Debt |  |  | As of September 26, 2020, the Company had outstanding floating- and fixed-rate notes with varying maturities for an aggregate principal amount of $106.1 billion (collectively the “Notes”). The Notes are senior unsecured … |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#3 `AAPL_FY2020_2020-09-26:270`** (cited, gold #2)

````text
Item 8. Financial Statements and Supplementary Data > Term Debt (table)
| 2021 | $8,750 |
|---|---|
| 2022 | 9,569 |
| 2023 | 11,389 |
| 2024 | 10,115 |
| 2025 | 10,914 |
| Thereafter | 55,341 |
| Total term debt | $106,078 |
````

**#4 `AAPL_FY2020_2020-09-26:143`** (gold #2)

````text
Item 7. Management’s Discussion and Analysis of Financial Condition and Results of Operations > Contractual Obligations (table)
|  | Payments due in 2021 | Payments due in 2022–2023 | Payments due in 2024–2025 | Payments due after 2025 | Total |
|---|---|---|---|---|---|
| Term debt | $8,750 | $20,958 | $21,029 | $55,341 | $106,078 |
| Leases | 1,622 | 3,097 | 2,352 | 5,888 | 12,959 |
| Manufacturing purchase obligations (1) | 47,961 | 1,849 | 61 | 40 | 49,911 |
| Other purchase obligations | 6,178 | 2,736 | 400 | 90 | 9,404 |
| Deemed repatriation tax payable | 1,533 | 5,923 | 12,955 | 9,254 | 29,665 |
| Total | $66,044 | $34,563 | $36,797 | $70,613 | $208,017 |
````

**#5 `AAPL_FY2020_2020-09-26:267`** (gold #2)

````text
Item 8. Financial Statements and Supplementary Data > Term Debt (table)
|  | Maturities (calendar year) | 2020 |  | 2019 |  |
|---|---|---|---|---|---|
|  | Amount (in millions) | Effective Interest Rate | Amount (in millions) | Effective Interest Rate |  |
| Total term debt |  | 106,078 |  | 101,679 |  |
| Unamortized premium/(discount) and issuance costs, net |  | (314) |  | (224) |  |
| Hedge accounting fair value adjustments |  | 1,676 |  | 612 |  |
| Less: Current portion of term debt |  | (8,773) |  | (10,260) |  |
| Total non-current portion of term debt |  | $98,667 |  | $91,807 |  |
````

</details>

RQ2 citation match (section level): `cited=[('AAPL', 'Item 8')] gold=[(None, 'Item 8')]`

**System C guardrail** (judge `gpt-5.4`): numerical claims 1, verified 1, ungrounded 0, uncited 0, derived 0; sentence verdicts: supported 1, partial 0, unsupported 0, unchecked 0.


<details><summary>Guardrail sentence verdicts</summary>

| sentence | verdict | judge reason |
|---|---|---|
| Apple’s total term debt was $106,078 million as of September 26, 2020, based on its schedule of future principal payments [AAPL FY2020, Item 8, AAPL_FY2020_2020-09-26:270]. | None |  |
| The filing does not disclose Amazon’s total long-term debt or a schedule of future principal payments, so the difference cannot be determined from the provided evidence. | supported | The retrieved evidence contains Amazon summary financials but no disclosure of Amazon long-term debt or future principal payment schedule. |

</details>
