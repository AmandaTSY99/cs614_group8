# gold-059: Table + text (one filing)

[← all cases](../README.md) · company: NVIDIA CORP (NVDA) · fiscal year: 2023 · recipe `table_text` · hop `multi` · answer type `mixed` · scope `single_doc` · RQ2 category `cross_section_multihop`

## Gold QA

**Question**

> Calculate the percentage decrease in NVIDIA's total liquidity (cash, cash equivalents, and marketable securities) from fiscal year 2022 to fiscal year 2023. Additionally, according to the risk factors, what is the total amount of outstanding notes the company had as of January 29, 2023, and how does the company describe the potential impact of maintaining this indebtedness on its cash flows?

**Gold answer**

> The percentage decrease was 37.31%. As of January 29, 2023, NVIDIA had $11 billion in outstanding notes. The company states that maintaining this indebtedness could cause it to dedicate a substantial portion of its cash flows from operations towards debt service obligations and principal repayments.

**Program**: `subtract(21208, 13296), divide(#0, 21208), multiply(#1, 100)` → `37.306676725763865`

**Gold numbers** (RQ2 numeric_accuracy targets): 37.31%

**Key points** (RQ3 keypoint_recall targets)

1. Percentage decrease is 37.31%
2. Outstanding notes amount is $11 billion
3. Debt maintenance could dedicate a substantial portion of cash flows from operations to debt service

**Gold evidence**

1. `NVDA_FY2023_2023-01-29` · ITEM 7. MANAGEMENT’S DISCUSSION AND ANALYSIS OF FINANCIAL CONDITION AND RESULTS OF OPERATIONS › Liquidity and Capital Resources · table

   > Cash, cash equivalents, and marketable securities | $13,296 | $21,208

2. `NVDA_FY2023_2023-01-29` · ITEM 1A. RISK FACTORS › Our business is exposed to the risks associated with litigation, investigations and regulatory proceedings. · text

   > As of January 29, 2023, we had outstanding a total of $11 billion in notes due by 2060.

3. `NVDA_FY2023_2023-01-29` · ITEM 1A. RISK FACTORS › Our business is exposed to the risks associated with litigation, investigations and regulatory proceedings. · text

   > Maintenance of our current and future indebtedness and contractual restrictions could cause us to dedicate a substantial portion of our cash flows from operations towards debt service obligations and principal repayments

## Scorecard

| Metric | A (vanilla dense) | B (hybrid + rerank) | C v1 (adaptive multi-hop) | C v2 (agentic multi-hop + XBRL) |
|---|---|---|---|---|
| **Retrieval (RQ1)** | | | | |
| chunks retrieved | 10 | 5 | 12 | 13 |
| recall@5 | 0.67 | 1.00 | 0.67 | 0.33 |
| recall@all | 1.00 | 1.00 | 1.00 | 1.00 |
| complete@all | 1 | 1 | 1 | 1 |
| average precision (lexical) | 0.79 | 0.92 | 1.00 | 0.75 |
| gold evidence first rank | #1: 1, #2: 1, #3: 8 | #1: 2, #2: 1, #3: 1 | #1: 1, #2: 5, #3: 7 | #1: 2, #2: 6, #3: 8 |
| **Answer (RQ3 string match)** | | | | |
| numeric_correct | ✓ | ✓ | ✓ | ✓ |
| keypoint_recall | 1.00 | 1.00 | 1.00 | 1.00 |
| **Answer & citations (RQ2)** | | | | |
| numeric_accuracy | 1.00 | 1.00 | 1.00 | 1.00 |
| citation precision | 1.00 | 1.00 | 1.00 | 1.00 |
| citation recall | 1.00 | 1.00 | 1.00 | 1.00 |
| citation F1 | 1.00 | 1.00 | 1.00 | 1.00 |
| has a citation | 1 | 1 | 1 | 1 |
| grounding error rate | – | – | 0.00 | 0.00 |
| **Cost (RQ3)** | | | | |
| retrieval hops | 1 | 1 | 2 | 2 |
| tokens | 2434 | 1293 | 10190 | 10730 |
| cost (USD) | 0.0004 | 0.0003 | 0.0369 | 0.0388 |
| latency (s) | 3.1 | 7.5 | 17.6 | 17.3 |

Definitions: [README › Metrics](../README.md#metrics). `–` = not applicable (e.g. no gold number, no citations, no guardrail).

## System outputs

### System A (vanilla dense)

Model: `gpt-5.4-2026-03-05`. Hops: 1. Chunks retrieved: 10, cited: 2.

**Generated answer**

> NVIDIA’s total liquidity decreased from **$21,208 million** in fiscal year 2022 to **$13,296 million** in fiscal year 2023 [3].
>
> Percentage decrease:
>
> \[
> \frac{21{,}208 - 13{,}296}{21{,}208} \times 100 \approx 37.3\%
> \]
>
> So, the total liquidity **decreased by approximately 37.3%** [3].
>
> According to the risk factors, as of **January 29, 2023**, NVIDIA had **$11 billion in outstanding notes** due by 2060 [8]. The company says that maintaining its current and future indebtedness could cause it to **dedicate a substantial portion of its cash flows from operations toward debt service obligations and principal repayments** [8].

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `NVDA_FY2023_2023-01-29:215` | Item 7 › Liquidity and Capital Resources |  | #1, #2 | As of January 29, 2023, we had $13.30 billion in cash, cash equivalents and marketable securities, a decrease of $7.91 billion from the end of fiscal year 2022. Our investment policy requires the purchase of highly rated… |
| 2 | `NVDA_FY2023_2023-01-29:216` | Item 7 › Liquidity |  | #1 | Our primary sources of liquidity are our cash and cash equivalents, our marketable securities, and cash generated by our operations. At the end of fiscal year 2023, we had $13.30 billion in cash, cash equivalents and mar… |
| 3 | `NVDA_FY2023_2023-01-29:213` | Item 7 › Liquidity and Capital Resources | ✓ | #1 | \| \| January 29, 2023 \| January 30, 2022 \| \|---\|---\|---\| \| \| (In millions) \| \| \| Cash and cash equivalents \| $3,389 \| $1,990 \| \| Marketable securities \| 9,907 \| 19,218 \| \| Cash, cash equivalents, and marketable securities… |
| 4 | `NVDA_FY2023_2023-01-29:214` | Item 7 › Liquidity and Capital Resources |  |  | \| \| Year Ended \| \| \|---\|---\|---\| \| \| January 29, 2023 \| January 30, 2022 \| \| \| (In millions) \| \| \| Net cash provided by operating activities \| $5,641 \| $9,108 \| \| Net cash provided by (used in) investing activities \| $7,… |
| 5 | `NVDA_FY2023_2023-01-29:225` | Item 7A › Investment and Interest Rate Risk |  |  | We are exposed to interest rate risk related to our fixed-rate investment portfolio and outstanding debt. The investment portfolio is managed consistent with our overall liquidity strategy in support of both working capi… |
| 6 | `NVDA_FY2023_2023-01-29:219` | Item 7 › Outstanding Indebtedness and Commercial Paper Program |  |  | Our aggregate debt maturities as of January 29, 2023, by year payable, are as follows: |
| 7 | `NVDA_FY2023_2023-01-29:364` | Item 15 › (Continued) |  | #1 | The gross unrealized losses are related to fixed income securities, driven primarily by changes in interest rates. Net realized gains and losses were not significant for all periods presented. The amortized cost and esti… |
| 8 | `NVDA_FY2023_2023-01-29:158` | Item 1A › Our business is exposed to the risks associated with litigation, investigations and regulatory proceedings. | ✓ | #2, #3 | As of January 29, 2023, we had outstanding a total of $11 billion in notes due by 2060. As each series of senior notes matures, unless redeemed or repurchased, we must repay or refinance the notes. If we decide to refina… |
| 9 | `NVDA_FY2023_2023-01-29:217` | Item 7 › Liquidity |  | #1 | During fiscal year 2024, we expect to use our existing cash and cash equivalents, our marketable securities, and the cash generated by our operations to fund our capital investments of approximately $1.10 billion to $1.3… |
| 10 | `NVDA_FY2023_2023-01-29:360` | Item 15 › Note 8 - Cash Equivalents and Marketable Securities |  | #1 | \| \| January 30, 2022 \| \| \| \| \| \| \|---\|---\|---\|---\|---\|---\|---\| \| \| Amortized Cost \| Unrealized Gain \| Unrealized Loss \| Estimated Fair Value \| Reported as \| \| \| \| \| \| Cash Equivalents \| Marketable Securities \| \| \| \| \| (I… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#1 `NVDA_FY2023_2023-01-29:215`** (gold #1, gold #2)

````text
ITEM 7. MANAGEMENT’S DISCUSSION AND ANALYSIS OF FINANCIAL CONDITION AND RESULTS OF OPERATIONS > Liquidity and Capital Resources
As of January 29, 2023, we had $13.30 billion in cash, cash equivalents and marketable securities, a decrease of $7.91 billion from the end of fiscal year 2022. Our investment policy requires the purchase of highly rated fixed income securities, the diversification of investment types and credit exposures, and certain maturity limits on our portfolio. Cash provided by operating activities decreased in fiscal year 2023 compared to fiscal year 2022, primarily due to a decrease in net income adjusted for certain non-cash items, such as the Arm acquisition termination cost of $1.35 billion, and higher tax payments, partially offset by changes in working capital. Changes in working capital were primarily driven by lower accounts receivable due to strong collections partially offset by timing of supplier payments and inventory deliveries. Cash provided by investing activities increased in fiscal year 2023 compared to fiscal year 2022, primarily driven by lower purchases and higher sales and maturities of marketable securities, offset by higher capital expenditures. Cash used in financing activities increased in fiscal year 2023 compared to fiscal year 2022, due to share repurchases and the absence of debt issuance proceeds in fiscal year 2023, offset by absence of debt repayment.
````

**#2 `NVDA_FY2023_2023-01-29:216`** (gold #1)

````text
ITEM 7. MANAGEMENT’S DISCUSSION AND ANALYSIS OF FINANCIAL CONDITION AND RESULTS OF OPERATIONS > Liquidity
Our primary sources of liquidity are our cash and cash equivalents, our marketable securities, and cash generated by our operations. At the end of fiscal year 2023, we had $13.30 billion in cash, cash equivalents and marketable securities. We believe that we have sufficient liquidity to meet our operating requirements for at least the next twelve months, and for the foreseeable future, including our future supply obligations and $1.25 billion of debt repayment due in fiscal year 2024. We continuously evaluate our liquidity and capital resources, including our access to external capital, to ensure we can finance future capital requirements. Our marketable securities consist of debt securities issued by the U.S. government and its agencies, highly rated corporations and financial institutions, and foreign government entities, as well as certificates of deposit issued by highly rated financial institutions. These marketable securities are primarily denominated in U.S. dollars. Refer to Note 8 of the Notes to the Consolidated Financial Statements in Part IV, Item 15 of this Annual Report on Form 10-K for additional information.
````

**#3 `NVDA_FY2023_2023-01-29:213`** (cited, gold #1)

````text
ITEM 7. MANAGEMENT’S DISCUSSION AND ANALYSIS OF FINANCIAL CONDITION AND RESULTS OF OPERATIONS > Liquidity and Capital Resources (table)
|  | January 29, 2023 | January 30, 2022 |
|---|---|---|
|  | (In millions) |  |
| Cash and cash equivalents | $3,389 | $1,990 |
| Marketable securities | 9,907 | 19,218 |
| Cash, cash equivalents, and marketable securities | $13,296 | $21,208 |
````

**#7 `NVDA_FY2023_2023-01-29:364`** (gold #1)

````text
ITEM 15. EXHIBIT AND FINANCIAL STATEMENT SCHEDULES > (Continued)
The gross unrealized losses are related to fixed income securities, driven primarily by changes in interest rates. Net realized gains and losses were not significant for all periods presented. The amortized cost and estimated fair value of cash equivalents and marketable securities as of January 29, 2023 and January 30, 2022 are shown below by contractual maturity.
````

**#8 `NVDA_FY2023_2023-01-29:158`** (cited, gold #2, gold #3)

````text
ITEM 1A. RISK FACTORS > Our business is exposed to the risks associated with litigation, investigations and regulatory proceedings.
As of January 29, 2023, we had outstanding a total of $11 billion in notes due by 2060. As each series of senior notes matures, unless redeemed or repurchased, we must repay or refinance the notes. If we decide to refinance, we may receive less favorable terms, or we may be unable to refinance at all, which may adversely affect our financial condition. We also have a $575 million commercial paper program. Maintenance of our current and future indebtedness and contractual restrictions could cause us to dedicate a substantial portion of our cash flows from operations towards debt service obligations and principal repayments; increase our vulnerability to adverse changes in general economic, industry and competitive conditions; limit our flexibility regarding changes in our business and our industry; impair our ability to obtain future financing; and restrict our ability to grant liens on property, enter into certain mergers, dispose of our assets, or materially change our business.
````

**#9 `NVDA_FY2023_2023-01-29:217`** (gold #1)

````text
ITEM 7. MANAGEMENT’S DISCUSSION AND ANALYSIS OF FINANCIAL CONDITION AND RESULTS OF OPERATIONS > Liquidity
During fiscal year 2024, we expect to use our existing cash and cash equivalents, our marketable securities, and the cash generated by our operations to fund our capital investments of approximately $1.10 billion to $1.30 billion related to property and equipment. Except for approximately $1.38 billion of cash, cash equivalents, and marketable securities held outside the U.S. for which we have not accrued any related foreign or state taxes if we repatriate these amounts to the U.S., substantially all of our cash, cash equivalents and marketable securities held outside of the U.S. at the end of fiscal year 2023 are available for use in the U.S. without incurring additional U.S. federal income taxes. Beginning in fiscal year 2023, the TCJA requires taxpayers to capitalize research and development expenditures and to amortize domestic expenditures over five years and foreign expenditures over fifteen years. The adverse cash flow impact of mandatory capitalization will be reduced in future years as capitalized research and development expenditures continue to amortize. Refer to Note 14 of the Notes to the Consolidated Financial Statements in Part IV, Item 15 of this Annual Report on Form 10-K for additional information.
````

**#10 `NVDA_FY2023_2023-01-29:360`** (gold #1)

````text
ITEM 15. EXHIBIT AND FINANCIAL STATEMENT SCHEDULES > Note 8 - Cash Equivalents and Marketable Securities (table)
|  | January 30, 2022 |  |  |  |  |  |
|---|---|---|---|---|---|---|
|  | Amortized Cost | Unrealized Gain | Unrealized Loss | Estimated Fair Value | Reported as |  |
|  |  |  | Cash Equivalents | Marketable Securities |  |  |
|  | (In millions) |  |  |  |  |  |
| Corporate debt securities | $9,977 | $— | $(3) | $9,974 | $1,102 | $8,872 |
| Debt securities issued by the United States Treasury | 7,314 | — | (14) | 7,300 | — | 7,300 |
| Debt securities issued by United States government agencies | 1,612 | — | — | 1,612 | 256 | 1,356 |
| Certificates of deposit | 1,561 | — | — | 1,561 | 21 | 1,540 |
| Money market funds | 316 | — | — | 316 | 316 | — |
| Foreign government bonds | 150 | — | — | 150 | — | 150 |
| Total | $20,930 | $— | $(17) | $20,913 | $1,695 | $19,218 |
````

</details>

RQ2 citation match (section level): `cited=[('NVDA', 'Item 7'), ('NVDA', 'Item 1A')] gold=[(None, 'Item 7'), (None, 'Item 1A')]`

### System B (hybrid + rerank)

Model: `gpt-5.4-2026-03-05`. Hops: 1. Chunks retrieved: 5, cited: 2.

**Generated answer**

> NVIDIA’s total liquidity decreased from approximately $21.21 billion in fiscal year 2022 to $13.30 billion in fiscal year 2023, a decrease of $7.91 billion. The percentage decrease is:
>
> \[
> \frac{7.91}{21.21} \times 100 \approx 37.3\%
> \]
>
> So, the decrease was approximately **37.3%** [2].
>
> As of January 29, 2023, NVIDIA had **$11 billion in outstanding notes due by 2060** [1].
>
> The company states that maintaining its current and future indebtedness and contractual restrictions could cause it to **dedicate a substantial portion of its cash flows from operations toward debt service obligations and principal repayments** [1].

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `NVDA_FY2023_2023-01-29:158` | Item 1A › Our business is exposed to the risks associated with litigation, investigations and regulatory proceedings. | ✓ | #2, #3 | As of January 29, 2023, we had outstanding a total of $11 billion in notes due by 2060. As each series of senior notes matures, unless redeemed or repurchased, we must repay or refinance the notes. If we decide to refina… |
| 2 | `NVDA_FY2023_2023-01-29:215` | Item 7 › Liquidity and Capital Resources | ✓ | #1, #2 | As of January 29, 2023, we had $13.30 billion in cash, cash equivalents and marketable securities, a decrease of $7.91 billion from the end of fiscal year 2022. Our investment policy requires the purchase of highly rated… |
| 3 | `NVDA_FY2023_2023-01-29:159` | Item 1A › Our business is exposed to the risks associated with litigation, investigations and regulatory proceedings. |  |  | Our ability to comply with the covenants in our indenture may be affected by events beyond our control. If we breach any of the covenants without a waiver from the note holders or lenders, then any outstanding indebtedne… |
| 4 | `NVDA_FY2023_2023-01-29:183` | Item 7 › Fiscal Year 2023 Summary |  | #1 | Automotive revenue was up 60% from a year ago reflecting growth in sales of self-driving solutions, computing solutions for electric vehicle makers and strength in sales of AI cockpit solutions. The increase also include… |
| 5 | `NVDA_FY2023_2023-01-29:219` | Item 7 › Outstanding Indebtedness and Commercial Paper Program |  |  | Our aggregate debt maturities as of January 29, 2023, by year payable, are as follows: |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#1 `NVDA_FY2023_2023-01-29:158`** (cited, gold #2, gold #3)

````text
ITEM 1A. RISK FACTORS > Our business is exposed to the risks associated with litigation, investigations and regulatory proceedings.
As of January 29, 2023, we had outstanding a total of $11 billion in notes due by 2060. As each series of senior notes matures, unless redeemed or repurchased, we must repay or refinance the notes. If we decide to refinance, we may receive less favorable terms, or we may be unable to refinance at all, which may adversely affect our financial condition. We also have a $575 million commercial paper program. Maintenance of our current and future indebtedness and contractual restrictions could cause us to dedicate a substantial portion of our cash flows from operations towards debt service obligations and principal repayments; increase our vulnerability to adverse changes in general economic, industry and competitive conditions; limit our flexibility regarding changes in our business and our industry; impair our ability to obtain future financing; and restrict our ability to grant liens on property, enter into certain mergers, dispose of our assets, or materially change our business.
````

**#2 `NVDA_FY2023_2023-01-29:215`** (cited, gold #1, gold #2)

````text
ITEM 7. MANAGEMENT’S DISCUSSION AND ANALYSIS OF FINANCIAL CONDITION AND RESULTS OF OPERATIONS > Liquidity and Capital Resources
As of January 29, 2023, we had $13.30 billion in cash, cash equivalents and marketable securities, a decrease of $7.91 billion from the end of fiscal year 2022. Our investment policy requires the purchase of highly rated fixed income securities, the diversification of investment types and credit exposures, and certain maturity limits on our portfolio. Cash provided by operating activities decreased in fiscal year 2023 compared to fiscal year 2022, primarily due to a decrease in net income adjusted for certain non-cash items, such as the Arm acquisition termination cost of $1.35 billion, and higher tax payments, partially offset by changes in working capital. Changes in working capital were primarily driven by lower accounts receivable due to strong collections partially offset by timing of supplier payments and inventory deliveries. Cash provided by investing activities increased in fiscal year 2023 compared to fiscal year 2022, primarily driven by lower purchases and higher sales and maturities of marketable securities, offset by higher capital expenditures. Cash used in financing activities increased in fiscal year 2023 compared to fiscal year 2022, due to share repurchases and the absence of debt issuance proceeds in fiscal year 2023, offset by absence of debt repayment.
````

**#4 `NVDA_FY2023_2023-01-29:183`** (gold #1)

````text
ITEM 7. MANAGEMENT’S DISCUSSION AND ANALYSIS OF FINANCIAL CONDITION AND RESULTS OF OPERATIONS > Fiscal Year 2023 Summary
Automotive revenue was up 60% from a year ago reflecting growth in sales of self-driving solutions, computing solutions for electric vehicle makers and strength in sales of AI cockpit solutions. The increase also included growth in automotive development arrangements. OEM and Other revenue was down 61% from a year ago driven by notebook OEM and CMP. CMP revenue was nominal in fiscal year 2023 and $550 million in fiscal year 2022. Gross margin for fiscal year 2023 declined from a year ago, driven by $2.17 billion of inventory charges largely relating to excess supply of NVIDIA Ampere architecture Gaming and Data Center products as compared to the demand expectations for these products, particularly for the expected demand in China. The inventory charges were comprised of $1.04 billion for inventory on hand and $1.13 billion for inventory purchase obligations in excess of our demand expectations. Operating expenses, which included a $1.35 billion acquisition termination charge related to the Arm transaction, were up 50% from a year ago. The increase also reflected compensation, data center infrastructure, and engineering development costs. Cash, cash equivalents and marketable securities were $13.30 billion.
````

</details>

RQ2 citation match (section level): `cited=[('NVDA', 'Item 1A'), ('NVDA', 'Item 7')] gold=[(None, 'Item 7'), (None, 'Item 1A')]`

### System C v1 (adaptive multi-hop)

Model: `gpt-5.4`. Hops: 2. Chunks retrieved: 12, cited: 2.

**Generated answer**

> NVIDIA’s total liquidity, defined as cash, cash equivalents, and marketable securities, decreased from $21,208 million on January 30, 2022 to $13,296 million on January 29, 2023, a decrease of approximately 37.3% [NVDA FY2023, Item 7, NVDA_FY2023_2023-01-29:213].  
>
> As of January 29, 2023, NVIDIA had outstanding a total of $11 billion in notes due by 2060 [NVDA FY2023, Item 1A, NVDA_FY2023_2023-01-29:158].  
>
> The company states that maintenance of its current and future indebtedness and contractual restrictions could cause it to dedicate a substantial portion of its cash flows from operations towards debt service obligations and principal repayments [NVDA FY2023, Item 1A, NVDA_FY2023_2023-01-29:158].

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `NVDA_FY2023_2023-01-29:300` | Item 15 › Cash and Cash Equivalents and Marketable Securities |  | #1 | We consider all highly liquid investments that are readily convertible into cash and have an original maturity of three months or less at the time of purchase to be cash equivalents. Marketable securities consist of high… |
| 2 | `NVDA_FY2023_2023-01-29:358` | Item 15 › Note 8 - Cash Equivalents and Marketable Securities |  | #1 | Our cash equivalents and marketable securities related to debt securities are classified as “available-for-sale” debt securities. The following is a summary of cash equivalents and marketable securities as of January 29,… |
| 3 | `NVDA_FY2023_2023-01-29:216` | Item 7 › Liquidity |  | #1 | Our primary sources of liquidity are our cash and cash equivalents, our marketable securities, and cash generated by our operations. At the end of fiscal year 2023, we had $13.30 billion in cash, cash equivalents and mar… |
| 4 | `NVDA_FY2023_2023-01-29:213` | Item 7 › Liquidity and Capital Resources | ✓ | #1 | \| \| January 29, 2023 \| January 30, 2022 \| \|---\|---\|---\| \| \| (In millions) \| \| \| Cash and cash equivalents \| $3,389 \| $1,990 \| \| Marketable securities \| 9,907 \| 19,218 \| \| Cash, cash equivalents, and marketable securities… |
| 5 | `NVDA_FY2023_2023-01-29:215` | Item 7 › Liquidity and Capital Resources |  | #1, #2 | As of January 29, 2023, we had $13.30 billion in cash, cash equivalents and marketable securities, a decrease of $7.91 billion from the end of fiscal year 2022. Our investment policy requires the purchase of highly rated… |
| 6 | `NVDA_FY2023_2023-01-29:301` | Item 15 › Cash and Cash Equivalents and Marketable Securities |  | #1 | Available-for-sale debt investments are subject to a periodic impairment review. If the estimated fair value of available-for-sale debt securities is less than its amortized cost basis, we determine if the difference, if… |
| 7 | `NVDA_FY2023_2023-01-29:158` | Item 1A › Our business is exposed to the risks associated with litigation, investigations and regulatory proceedings. | ✓ | #2, #3 | As of January 29, 2023, we had outstanding a total of $11 billion in notes due by 2060. As each series of senior notes matures, unless redeemed or repurchased, we must repay or refinance the notes. If we decide to refina… |
| 8 | `NVDA_FY2023_2023-01-29:159` | Item 1A › Our business is exposed to the risks associated with litigation, investigations and regulatory proceedings. |  |  | Our ability to comply with the covenants in our indenture may be affected by events beyond our control. If we breach any of the covenants without a waiver from the note holders or lenders, then any outstanding indebtedne… |
| 9 | `NVDA_FY2023_2023-01-29:10` | TABLE OF CONTENTS |  |  | \| \| \| Page \| \|---\|---\|---\| \| \| PART I \| \| \| Item 1. \| Business \| 4 \| \| Item 1A. \| Risk Factors \| 15 \| \| Item 1B. \| Unresolved Staff Comments \| 33 \| \| Item 2. \| Properties \| 33 \| \| Item 3. \| Legal Proceedings \| 34 \| \| Ite… |
| 10 | `NVDA_FY2023_2023-01-29:172` | Item 7 |  |  | The following discussion and analysis of our financial condition and results of operations should be read in conjunction with “Item 1A. Risk Factors”, our Consolidated Financial Statements and related Notes thereto, as w… |
| 11 | `NVDA_FY2023_2023-01-29:333` | Item 15 › Note 3 - Leases |  |  | \| \| Year Ended \| \| \| \|---\|---\|---\|---\| \| \| January 29, 2023 \| January 30, 2022 \| January 31, 2021 \| \| \| (In millions) \| \| \| \| Supplemental cash flows information \| \| \| \| \| Operating cash flows used for operating leases \|… |
| 12 | `NVDA_FY2023_2023-01-29:249` | Item 15 |  |  | \| \| \| \| Page \| \|---\|---\|---\|---\| \| (a) \| 1. \| Financial Statements \| \| \| \| \| Report of Independent Registered Public Accounting Firm (PCAOB ID: 238) \| 52 \| \| \| \| Consolidated Statements of Income for the years ended Janu… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#1 `NVDA_FY2023_2023-01-29:300`** (gold #1)

````text
ITEM 15. EXHIBIT AND FINANCIAL STATEMENT SCHEDULES > Cash and Cash Equivalents and Marketable Securities
We consider all highly liquid investments that are readily convertible into cash and have an original maturity of three months or less at the time of purchase to be cash equivalents. Marketable securities consist of highly liquid debt investments with maturities of greater than three months when purchased. We currently classify our investments as current based on the nature of the investments and their availability for use in current operations. We classify our cash equivalents and marketable securities related to debt securities at the date of acquisition as available-for-sale. These available-for-sale debt securities are reported at fair value with the related unrealized gains and losses included in accumulated other comprehensive income or loss, a component of shareholders’ equity, net of tax. The fair value of interest-bearing debt securities includes accrued interest. Realized gains and losses on the sale of marketable securities are determined using the specific-identification method and recorded in the other income (expense), net, section of our Consolidated Statements of Income.
````

**#2 `NVDA_FY2023_2023-01-29:358`** (gold #1)

````text
ITEM 15. EXHIBIT AND FINANCIAL STATEMENT SCHEDULES > Note 8 - Cash Equivalents and Marketable Securities
Our cash equivalents and marketable securities related to debt securities are classified as “available-for-sale” debt securities. The following is a summary of cash equivalents and marketable securities as of January 29, 2023 and January 30, 2022:
````

**#3 `NVDA_FY2023_2023-01-29:216`** (gold #1)

````text
ITEM 7. MANAGEMENT’S DISCUSSION AND ANALYSIS OF FINANCIAL CONDITION AND RESULTS OF OPERATIONS > Liquidity
Our primary sources of liquidity are our cash and cash equivalents, our marketable securities, and cash generated by our operations. At the end of fiscal year 2023, we had $13.30 billion in cash, cash equivalents and marketable securities. We believe that we have sufficient liquidity to meet our operating requirements for at least the next twelve months, and for the foreseeable future, including our future supply obligations and $1.25 billion of debt repayment due in fiscal year 2024. We continuously evaluate our liquidity and capital resources, including our access to external capital, to ensure we can finance future capital requirements. Our marketable securities consist of debt securities issued by the U.S. government and its agencies, highly rated corporations and financial institutions, and foreign government entities, as well as certificates of deposit issued by highly rated financial institutions. These marketable securities are primarily denominated in U.S. dollars. Refer to Note 8 of the Notes to the Consolidated Financial Statements in Part IV, Item 15 of this Annual Report on Form 10-K for additional information.
````

**#4 `NVDA_FY2023_2023-01-29:213`** (cited, gold #1)

````text
ITEM 7. MANAGEMENT’S DISCUSSION AND ANALYSIS OF FINANCIAL CONDITION AND RESULTS OF OPERATIONS > Liquidity and Capital Resources (table)
|  | January 29, 2023 | January 30, 2022 |
|---|---|---|
|  | (In millions) |  |
| Cash and cash equivalents | $3,389 | $1,990 |
| Marketable securities | 9,907 | 19,218 |
| Cash, cash equivalents, and marketable securities | $13,296 | $21,208 |
````

**#5 `NVDA_FY2023_2023-01-29:215`** (gold #1, gold #2)

````text
ITEM 7. MANAGEMENT’S DISCUSSION AND ANALYSIS OF FINANCIAL CONDITION AND RESULTS OF OPERATIONS > Liquidity and Capital Resources
As of January 29, 2023, we had $13.30 billion in cash, cash equivalents and marketable securities, a decrease of $7.91 billion from the end of fiscal year 2022. Our investment policy requires the purchase of highly rated fixed income securities, the diversification of investment types and credit exposures, and certain maturity limits on our portfolio. Cash provided by operating activities decreased in fiscal year 2023 compared to fiscal year 2022, primarily due to a decrease in net income adjusted for certain non-cash items, such as the Arm acquisition termination cost of $1.35 billion, and higher tax payments, partially offset by changes in working capital. Changes in working capital were primarily driven by lower accounts receivable due to strong collections partially offset by timing of supplier payments and inventory deliveries. Cash provided by investing activities increased in fiscal year 2023 compared to fiscal year 2022, primarily driven by lower purchases and higher sales and maturities of marketable securities, offset by higher capital expenditures. Cash used in financing activities increased in fiscal year 2023 compared to fiscal year 2022, due to share repurchases and the absence of debt issuance proceeds in fiscal year 2023, offset by absence of debt repayment.
````

**#6 `NVDA_FY2023_2023-01-29:301`** (gold #1)

````text
ITEM 15. EXHIBIT AND FINANCIAL STATEMENT SCHEDULES > Cash and Cash Equivalents and Marketable Securities
Available-for-sale debt investments are subject to a periodic impairment review. If the estimated fair value of available-for-sale debt securities is less than its amortized cost basis, we determine if the difference, if any, is caused by expected credit losses and write-down the amortized cost basis of the securities if it is more likely than not we will be required or we intend to sell the securities before recovery of its amortized cost basis. Allowances for credit losses and write-downs are recognized in the other income (expense), net section of our Consolidated Statements of Income.
````

**#7 `NVDA_FY2023_2023-01-29:158`** (cited, gold #2, gold #3)

````text
ITEM 1A. RISK FACTORS > Our business is exposed to the risks associated with litigation, investigations and regulatory proceedings.
As of January 29, 2023, we had outstanding a total of $11 billion in notes due by 2060. As each series of senior notes matures, unless redeemed or repurchased, we must repay or refinance the notes. If we decide to refinance, we may receive less favorable terms, or we may be unable to refinance at all, which may adversely affect our financial condition. We also have a $575 million commercial paper program. Maintenance of our current and future indebtedness and contractual restrictions could cause us to dedicate a substantial portion of our cash flows from operations towards debt service obligations and principal repayments; increase our vulnerability to adverse changes in general economic, industry and competitive conditions; limit our flexibility regarding changes in our business and our industry; impair our ability to obtain future financing; and restrict our ability to grant liens on property, enter into certain mergers, dispose of our assets, or materially change our business.
````

</details>

RQ2 citation match (section level): `cited=[('NVDA', 'Item 7'), ('NVDA', 'Item 1A')] gold=[(None, 'Item 7'), (None, 'Item 1A')]`

**System C guardrail** (judge `gpt-5.4`): numerical claims 5, verified 5, ungrounded 0, uncited 0, derived 1; sentence verdicts: supported 1, partial 0, unsupported 0, unchecked 0.


<details><summary>Guardrail sentence verdicts</summary>

| sentence | verdict | judge reason |
|---|---|---|
| NVIDIA’s total liquidity, defined as cash, cash equivalents, and marketable securities, decreased from $21,208 million on January 30, 2022 to $13,296 million on January 29, 2023, a decrease of approximately 37.3% [NVDA FY2023, Item 7, NVDA_FY2023_2023-01-29:213]. | None |  |
| As of January 29, 2023, NVIDIA had outstanding a total of $11 billion in notes due by 2060 [NVDA FY2023, Item 1A, NVDA_FY2023_2023-01-29:158]. | None |  |
| The company states that maintenance of its current and future indebtedness and contractual restrictions could cause it to dedicate a substantial portion of its cash flows from operations towards debt service obligations and principal repayments [NVDA FY2023, Item 1A, NVDA_FY2023_2023-01-29:158]. | supported | The cited risk factor states this verbatim, including dedicating substantial operating cash flows to debt service and principal repayments. |

</details>

### System C v2 (agentic multi-hop + XBRL)

Model: `gpt-5.4`. Hops: 2. Chunks retrieved: 13, cited: 2.

**Generated answer**

> NVIDIA’s cash, cash equivalents, and marketable securities decreased from $21,208 million at January 30, 2022 to $13,296 million at January 29, 2023, a decrease of approximately 37.3% [NVDA FY2023, Item 7, NVDA_FY2023_2023-01-29:213].  
> As of January 29, 2023, NVIDIA had outstanding a total of $11 billion in notes due by 2060 [NVDA FY2023, Item 1A, NVDA_FY2023_2023-01-29:158].  
> The company states that maintenance of its current and future indebtedness and contractual restrictions could cause it to dedicate a substantial portion of its cash flows from operations towards debt service obligations and principal repayments [NVDA FY2023, Item 1A, NVDA_FY2023_2023-01-29:158].

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `F-NVDA-2023` | SEC XBRL Reported Financials (financials.csv) |  |  | fiscal_year,fiscal_year_end,Revenue,NetIncome,OperatingIncome,TotalAssets,TotalLiabilities,StockholdersEquity,CashAndEquivalents,OperatingCashFlow,EPSDiluted 2023,2023-01-29,26974000000,4368000000,4224000000,41182000000,… |
| 2 | `NVDA_FY2023_2023-01-29:300` | Item 15 › Cash and Cash Equivalents and Marketable Securities |  | #1 | We consider all highly liquid investments that are readily convertible into cash and have an original maturity of three months or less at the time of purchase to be cash equivalents. Marketable securities consist of high… |
| 3 | `NVDA_FY2023_2023-01-29:358` | Item 15 › Note 8 - Cash Equivalents and Marketable Securities |  | #1 | Our cash equivalents and marketable securities related to debt securities are classified as “available-for-sale” debt securities. The following is a summary of cash equivalents and marketable securities as of January 29,… |
| 4 | `NVDA_FY2023_2023-01-29:216` | Item 7 › Liquidity |  | #1 | Our primary sources of liquidity are our cash and cash equivalents, our marketable securities, and cash generated by our operations. At the end of fiscal year 2023, we had $13.30 billion in cash, cash equivalents and mar… |
| 5 | `NVDA_FY2023_2023-01-29:213` | Item 7 › Liquidity and Capital Resources | ✓ | #1 | \| \| January 29, 2023 \| January 30, 2022 \| \|---\|---\|---\| \| \| (In millions) \| \| \| Cash and cash equivalents \| $3,389 \| $1,990 \| \| Marketable securities \| 9,907 \| 19,218 \| \| Cash, cash equivalents, and marketable securities… |
| 6 | `NVDA_FY2023_2023-01-29:215` | Item 7 › Liquidity and Capital Resources |  | #1, #2 | As of January 29, 2023, we had $13.30 billion in cash, cash equivalents and marketable securities, a decrease of $7.91 billion from the end of fiscal year 2022. Our investment policy requires the purchase of highly rated… |
| 7 | `NVDA_FY2023_2023-01-29:359` | Item 15 › Note 8 - Cash Equivalents and Marketable Securities |  | #1 | \| \| January 29, 2023 \| \| \| \| \| \| \|---\|---\|---\|---\|---\|---\|---\| \| \| Amortized Cost \| Unrealized Gain \| Unrealized Loss \| Estimated Fair Value \| Reported as \| \| \| \| \| \| Cash Equivalents \| Marketable Securities \| \| \| \| \| (I… |
| 8 | `NVDA_FY2023_2023-01-29:158` | Item 1A › Our business is exposed to the risks associated with litigation, investigations and regulatory proceedings. | ✓ | #2, #3 | As of January 29, 2023, we had outstanding a total of $11 billion in notes due by 2060. As each series of senior notes matures, unless redeemed or repurchased, we must repay or refinance the notes. If we decide to refina… |
| 9 | `NVDA_FY2023_2023-01-29:388` | Item 15 › Long-Term Debt |  |  | In June 2021, March 2020, and September 2016, we issued a total of $5.00 billion, $5.00 billion, and $2.00 billion aggregate principal of senior notes, respectively. The net proceeds from these offerings were $4.98 billi… |
| 10 | `NVDA_FY2023_2023-01-29:390` | Item 15 › (Continued) |  |  | \| \| Expected Remaining Term (years) \| Effective Interest Rate \| January 29, 2023 \| January 30, 2022 \| \|---\|---\|---\|---\|---\| \| \| \| \| (In millions) \| \| \| 0.309% Notes Due 2023 \| 0.4 \| 0.41% \| $1,250 \| $1,250 \| \| 0.584% Not… |
| 11 | `NVDA_FY2023_2023-01-29:159` | Item 1A › Our business is exposed to the risks associated with litigation, investigations and regulatory proceedings. |  |  | Our ability to comply with the covenants in our indenture may be affected by events beyond our control. If we breach any of the covenants without a waiver from the note holders or lenders, then any outstanding indebtedne… |
| 12 | `NVDA_FY2023_2023-01-29:222` | Item 7 › Material Cash Requirements and Other Obligations |  |  | For a description of our long-term debt, purchase obligations, and operating lease obligations, refer to Note 12, Note 13, and Note 3 of the Notes to the Consolidated Financial Statements in Part IV, Item 15 of this Annu… |
| 13 | `NVDA_FY2023_2023-01-29:333` | Item 15 › Note 3 - Leases |  |  | \| \| Year Ended \| \| \| \|---\|---\|---\|---\| \| \| January 29, 2023 \| January 30, 2022 \| January 31, 2021 \| \| \| (In millions) \| \| \| \| Supplemental cash flows information \| \| \| \| \| Operating cash flows used for operating leases \|… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#2 `NVDA_FY2023_2023-01-29:300`** (gold #1)

````text
ITEM 15. EXHIBIT AND FINANCIAL STATEMENT SCHEDULES > Cash and Cash Equivalents and Marketable Securities
We consider all highly liquid investments that are readily convertible into cash and have an original maturity of three months or less at the time of purchase to be cash equivalents. Marketable securities consist of highly liquid debt investments with maturities of greater than three months when purchased. We currently classify our investments as current based on the nature of the investments and their availability for use in current operations. We classify our cash equivalents and marketable securities related to debt securities at the date of acquisition as available-for-sale. These available-for-sale debt securities are reported at fair value with the related unrealized gains and losses included in accumulated other comprehensive income or loss, a component of shareholders’ equity, net of tax. The fair value of interest-bearing debt securities includes accrued interest. Realized gains and losses on the sale of marketable securities are determined using the specific-identification method and recorded in the other income (expense), net, section of our Consolidated Statements of Income.
````

**#3 `NVDA_FY2023_2023-01-29:358`** (gold #1)

````text
ITEM 15. EXHIBIT AND FINANCIAL STATEMENT SCHEDULES > Note 8 - Cash Equivalents and Marketable Securities
Our cash equivalents and marketable securities related to debt securities are classified as “available-for-sale” debt securities. The following is a summary of cash equivalents and marketable securities as of January 29, 2023 and January 30, 2022:
````

**#4 `NVDA_FY2023_2023-01-29:216`** (gold #1)

````text
ITEM 7. MANAGEMENT’S DISCUSSION AND ANALYSIS OF FINANCIAL CONDITION AND RESULTS OF OPERATIONS > Liquidity
Our primary sources of liquidity are our cash and cash equivalents, our marketable securities, and cash generated by our operations. At the end of fiscal year 2023, we had $13.30 billion in cash, cash equivalents and marketable securities. We believe that we have sufficient liquidity to meet our operating requirements for at least the next twelve months, and for the foreseeable future, including our future supply obligations and $1.25 billion of debt repayment due in fiscal year 2024. We continuously evaluate our liquidity and capital resources, including our access to external capital, to ensure we can finance future capital requirements. Our marketable securities consist of debt securities issued by the U.S. government and its agencies, highly rated corporations and financial institutions, and foreign government entities, as well as certificates of deposit issued by highly rated financial institutions. These marketable securities are primarily denominated in U.S. dollars. Refer to Note 8 of the Notes to the Consolidated Financial Statements in Part IV, Item 15 of this Annual Report on Form 10-K for additional information.
````

**#5 `NVDA_FY2023_2023-01-29:213`** (cited, gold #1)

````text
ITEM 7. MANAGEMENT’S DISCUSSION AND ANALYSIS OF FINANCIAL CONDITION AND RESULTS OF OPERATIONS > Liquidity and Capital Resources (table)
|  | January 29, 2023 | January 30, 2022 |
|---|---|---|
|  | (In millions) |  |
| Cash and cash equivalents | $3,389 | $1,990 |
| Marketable securities | 9,907 | 19,218 |
| Cash, cash equivalents, and marketable securities | $13,296 | $21,208 |
````

**#6 `NVDA_FY2023_2023-01-29:215`** (gold #1, gold #2)

````text
ITEM 7. MANAGEMENT’S DISCUSSION AND ANALYSIS OF FINANCIAL CONDITION AND RESULTS OF OPERATIONS > Liquidity and Capital Resources
As of January 29, 2023, we had $13.30 billion in cash, cash equivalents and marketable securities, a decrease of $7.91 billion from the end of fiscal year 2022. Our investment policy requires the purchase of highly rated fixed income securities, the diversification of investment types and credit exposures, and certain maturity limits on our portfolio. Cash provided by operating activities decreased in fiscal year 2023 compared to fiscal year 2022, primarily due to a decrease in net income adjusted for certain non-cash items, such as the Arm acquisition termination cost of $1.35 billion, and higher tax payments, partially offset by changes in working capital. Changes in working capital were primarily driven by lower accounts receivable due to strong collections partially offset by timing of supplier payments and inventory deliveries. Cash provided by investing activities increased in fiscal year 2023 compared to fiscal year 2022, primarily driven by lower purchases and higher sales and maturities of marketable securities, offset by higher capital expenditures. Cash used in financing activities increased in fiscal year 2023 compared to fiscal year 2022, due to share repurchases and the absence of debt issuance proceeds in fiscal year 2023, offset by absence of debt repayment.
````

**#7 `NVDA_FY2023_2023-01-29:359`** (gold #1)

````text
ITEM 15. EXHIBIT AND FINANCIAL STATEMENT SCHEDULES > Note 8 - Cash Equivalents and Marketable Securities (table)
|  | January 29, 2023 |  |  |  |  |  |
|---|---|---|---|---|---|---|
|  | Amortized Cost | Unrealized Gain | Unrealized Loss | Estimated Fair Value | Reported as |  |
|  |  |  | Cash Equivalents | Marketable Securities |  |  |
|  | (In millions) |  |  |  |  |  |
| Corporate debt securities | $4,809 | $— | $(12) | $4,797 | $1,087 | $3,710 |
| Debt securities issued by the United States Treasury | 4,185 | 1 | (44) | 4,142 | — | 4,142 |
| Debt securities issued by United States government agencies | 1,836 | — | (2) | 1,834 | 50 | 1,784 |
| Money market funds | 1,777 | — | — | 1,777 | 1,777 | — |
| Certificates of deposit | 365 | — | — | 365 | 134 | 231 |
| Foreign government bonds | 140 | — | — | 140 | 100 | 40 |
| Total | $13,112 | $1 | $(58) | $13,055 | $3,148 | $9,907 |
````

**#8 `NVDA_FY2023_2023-01-29:158`** (cited, gold #2, gold #3)

````text
ITEM 1A. RISK FACTORS > Our business is exposed to the risks associated with litigation, investigations and regulatory proceedings.
As of January 29, 2023, we had outstanding a total of $11 billion in notes due by 2060. As each series of senior notes matures, unless redeemed or repurchased, we must repay or refinance the notes. If we decide to refinance, we may receive less favorable terms, or we may be unable to refinance at all, which may adversely affect our financial condition. We also have a $575 million commercial paper program. Maintenance of our current and future indebtedness and contractual restrictions could cause us to dedicate a substantial portion of our cash flows from operations towards debt service obligations and principal repayments; increase our vulnerability to adverse changes in general economic, industry and competitive conditions; limit our flexibility regarding changes in our business and our industry; impair our ability to obtain future financing; and restrict our ability to grant liens on property, enter into certain mergers, dispose of our assets, or materially change our business.
````

</details>

RQ2 citation match (section level): `cited=[('NVDA', 'Item 7'), ('NVDA', 'Item 1A')] gold=[(None, 'Item 7'), (None, 'Item 1A')]`

**System C guardrail** (judge `gpt-5.4`): numerical claims 5, verified 5, ungrounded 0, uncited 0, derived 1; sentence verdicts: supported 1, partial 0, unsupported 0, unchecked 0.


<details><summary>Guardrail sentence verdicts</summary>

| sentence | verdict | judge reason |
|---|---|---|
| NVIDIA’s cash, cash equivalents, and marketable securities decreased from $21,208 million at January 30, 2022 to $13,296 million at January 29, 2023, a decrease of approximately 37.3% [NVDA FY2023, Item 7, NVDA_FY2023_2023-01-29:213]. | None |  |
| As of January 29, 2023, NVIDIA had outstanding a total of $11 billion in notes due by 2060 [NVDA FY2023, Item 1A, NVDA_FY2023_2023-01-29:158]. | None |  |
| The company states that maintenance of its current and future indebtedness and contractual restrictions could cause it to dedicate a substantial portion of its cash flows from operations towards debt service obligations and principal repayments [NVDA FY2023, Item 1A, NVDA_FY2023_2023-01-29:158]. | supported | The cited risk factor states this almost verbatim, including dedicating substantial operating cash flows to debt service and principal repayments. |

</details>
