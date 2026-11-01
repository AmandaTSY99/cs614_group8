# gold-064: Table + text (one filing)

[← all cases](../README.md) · company: AMAZON COM INC (AMZN) · fiscal year: 2023 · recipe `table_text` · hop `multi` · answer type `mixed` · scope `single_doc` · RQ2 category `cross_section_multihop`

## Gold QA

**Question**

> For Amazon.com Inc. in fiscal year 2023, calculate the percentage increase in cash paid for income taxes compared to 2022, and identify the primary operational factor cited in the Management's Discussion and Analysis that drove the increase in operating cash flows for the same period.

**Gold answer**

> The cash paid for income taxes increased by 86.67% from $6.0 billion in 2022 to $11.2 billion in 2023. The primary operational factor driving the increase in operating cash flows in 2023 was an increase in net income (loss), excluding non-cash expenses, and changes in working capital.

**Program**: `subtract(11.2, 6.0), divide(#0, 6.0), multiply(#1, 100)` → `86.66666666666666`

**Gold numbers** (RQ2 numeric_accuracy targets): 86.67%

**Key points** (RQ3 keypoint_recall targets)

1. Cash paid for income taxes was $11.2 billion in 2023 and $6.0 billion in 2022.
2. The percentage increase in cash paid for income taxes is 86.67%.
3. The increase in operating cash flow was due to an increase in net income (excluding non-cash expenses) and changes in working capital.

**Gold evidence**

1. `AMZN_FY2023_2023-12-31` · Item 8. Financial Statements and Supplementary Data › Note 9 — INCOME TAXES · text

   > Cash paid for income taxes, net of refunds, was $3.7 billion, $6.0 billion, and $11.2 billion for 2021, 2022, and 2023.

2. `AMZN_FY2023_2023-12-31` · Item 7. Management’s Discussion and Analysis of Financial Condition and Results of Operations › Liquidity and Capital Resources · text

   > The increase in operating cash flow in 2023, compared to the prior year, was due to an increase in net income (loss), excluding non-cash expenses, and changes in working capital.

## Scorecard

| Metric | A (vanilla dense) | B (hybrid + rerank) | C v1 (adaptive multi-hop) | C v2 (agentic multi-hop + XBRL) |
|---|---|---|---|---|
| **Retrieval (RQ1)** | | | | |
| chunks retrieved | 10 | 5 | 13 | 7 |
| recall@5 | 1.00 | 1.00 | 0.50 | 0.50 |
| recall@all | 1.00 | 1.00 | 1.00 | 0.50 |
| complete@all | 1 | 1 | 1 | 0 |
| average precision (lexical) | 0.59 | 0.64 | 0.37 | 0.29 |
| gold evidence first rank | #1: 5, #2: 1 | #1: 4, #2: 2 | #1: 3, #2: 8 | #1: 4, #2: – |
| **Answer (RQ3 string match)** | | | | |
| numeric_correct | ✓ | ✓ | ✓ | ✓ |
| keypoint_recall | 1.00 | 1.00 | 1.00 | 0.67 |
| **Answer & citations (RQ2)** | | | | |
| numeric_accuracy | 1.00 | 1.00 | 1.00 | 1.00 |
| citation precision | 1.00 | 1.00 | 1.00 | 1.00 |
| citation recall | 1.00 | 0.50 | 0.50 | 1.00 |
| citation F1 | 1.00 | 0.67 | 0.67 | 1.00 |
| has a citation | 1 | 1 | 1 | 1 |
| grounding error rate | – | – | 0.00 | 0.00 |
| **Cost (RQ3)** | | | | |
| retrieval hops | 1 | 1 | 3 | 1 |
| tokens | 2368 | 1454 | 13973 | 7065 |
| cost (USD) | 0.0004 | 0.0003 | 0.0510 | 0.0241 |
| latency (s) | 2.5 | 6.5 | 22.8 | 9.4 |

Definitions: [README › Metrics](../README.md#metrics). `–` = not applicable (e.g. no gold number, no citations, no guardrail).

## System outputs

### System A (vanilla dense)

Model: `gpt-5.4-2026-03-05`. Hops: 1. Chunks retrieved: 10, cited: 2.

**Generated answer**

> Cash paid for income taxes, net of refunds, increased from **$6.0 billion in 2022** to **$11.2 billion in 2023** [5].
>
> Percentage increase:
> \[
> \frac{11.2 - 6.0}{6.0} \times 100 \approx 86.7\%
> \]
>
> So, the cash paid for income taxes increased by **about 86.7%** [5].
>
> The primary factor cited for the increase in operating cash flows in 2023 was **an increase in net income (loss), excluding non-cash expenses, and changes in working capital** [1].

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `AMZN_FY2023_2023-12-31:127` | Item 7 › Liquidity and Capital Resources | ✓ | #2 | Cash provided by (used in) operating activities was $46.8 billion and $84.9 billion in 2022 and 2023. Our operating cash flows result primarily from cash received from our consumer, seller, developer, enterprise, and con… |
| 2 | `AMZN_FY2023_2023-12-31:154` | Item 7 › Results of Operations |  |  | We recorded a provision (benefit) for income taxes of $(3.2) billion and $7.1 billion in 2022 and 2023. See Item 8 of Part II, “Financial Statements and Supplementary Data — Note 9 — Income Taxes” for additional informat… |
| 3 | `AMZN_FY2023_2023-12-31:340` | Item 8 › Note 9 — INCOME TAXES |  |  | We recorded a provision for income taxes in 2023 as compared to an income tax benefit in 2022 primarily due to an increase in pretax income, a decrease in the tax impact of foreign earnings and losses driven by a decline… |
| 4 | `AMZN_FY2023_2023-12-31:338` | Item 8 › Note 9 — INCOME TAXES |  |  | \| \| Year Ended December 31, \| \| \| \|---\|---\|---\|---\| \| \| 2021 \| 2022 \| 2023 \| \| Income taxes computed at the federal statutory rate \| $8,012 \| $(1,246) \| $7,887 \| \| Effect of: \| \| \| \| \| Tax impact of foreign earnings and … |
| 5 | `AMZN_FY2023_2023-12-31:333` | Item 8 › Note 9 — INCOME TAXES | ✓ | #1 | In 2021, 2022, and 2023, we recorded a net tax provision (benefit) of $4.8 billion, $(3.2) billion, and $7.1 billion. Our U.S. taxable income is reduced by accelerated depreciation deductions and increased by the impact … |
| 6 | `AMZN_FY2023_2023-12-31:184` | Item 8 › (in millions) |  |  | \| \| Year Ended December 31, \| \| \| \|---\|---\|---\|---\| \| \| 2021 \| 2022 \| 2023 \| \| CASH, CASH EQUIVALENTS, AND RESTRICTED CASH, BEGINNING OF PERIOD \| $42,377 \| $36,477 \| $54,253 \| \| OPERATING ACTIVITIES: \| \| \| \| \| Net income… |
| 7 | `AMZN_FY2023_2023-12-31:166` | Item 7 › Guidance |  |  | •Operating income is expected to be between $8.0 billion and $12.0 billion, compared with $4.8 billion in first quarter 2023. This guidance includes approximately $0.9 billion lower depreciation expense due to an increas… |
| 8 | `AMZN_FY2023_2023-12-31:140` | Item 7 › Results of Operations |  | #2 | Operating income was $12.2 billion and $36.9 billion for 2022 and 2023. We believe that operating income is a more meaningful measure than gross profit and gross margin due to the diversity of our product categories and … |
| 9 | `AMZN_FY2023_2023-12-31:125` | Item 7 › Liquidity and Capital Resources |  |  | \| \| Year Ended December 31, \| \| \|---\|---\|---\| \| \| 2022 \| 2023 \| \| Cash provided by (used in): \| \| \| \| Operating activities \| $46,752 \| $84,946 \| \| Investing activities \| (37,601) \| (49,833) \| \| Financing activities \| 9,7… |
| 10 | `AMZN_FY2023_2023-12-31:91` | Item 1A › We Face Additional Tax Liabilities and Collection Obligations |  |  | tax accruals. |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#1 `AMZN_FY2023_2023-12-31:127`** (cited, gold #2)

````text
Item 7. Management’s Discussion and Analysis of Financial Condition and Results of Operations > Liquidity and Capital Resources
Cash provided by (used in) operating activities was $46.8 billion and $84.9 billion in 2022 and 2023. Our operating cash flows result primarily from cash received from our consumer, seller, developer, enterprise, and content creator customers, and advertisers, offset by cash payments we make for products and services, employee compensation, payment processing and related transaction costs, operating leases, and interest payments. Cash received from our customers and other activities generally corresponds to our net sales. The increase in operating cash flow in 2023, compared to the prior year, was due to an increase in net income (loss), excluding non-cash expenses, and changes in working capital. Working capital at any specific point in time is subject to many variables, including variability in demand, inventory management and category expansion, the timing of cash receipts and payments, customer and vendor payment terms, and fluctuations in foreign exchange rates. Cash provided by (used in) investing activities corresponds with cash capital expenditures, including leasehold improvements, incentives received from property and equipment vendors, proceeds from asset sales, cash outlays for
````

**#5 `AMZN_FY2023_2023-12-31:333`** (cited, gold #1)

````text
Item 8. Financial Statements and Supplementary Data > Note 9 — INCOME TAXES
In 2021, 2022, and 2023, we recorded a net tax provision (benefit) of $4.8 billion, $(3.2) billion, and $7.1 billion. Our U.S. taxable income is reduced by accelerated depreciation deductions and increased by the impact of capitalized research and development expenses. Cash paid for income taxes, net of refunds, was $3.7 billion, $6.0 billion, and $11.2 billion for 2021, 2022, and 2023. Certain foreign subsidiary earnings and losses are subject to current U.S. taxation and the subsequent repatriation of those earnings is not subject to tax in the U.S. The U.S. tax rules also provide for enhanced accelerated depreciation deductions by allowing us to expense a portion of qualified property, primarily equipment. These enhanced deductions are scheduled to phase out annually from 2023 through 2026. Our federal tax provision included a partial accelerated depreciation deduction election for 2021, and a full election for 2022 and 2023. Effective January 1, 2022, research and development expenses are required to be capitalized and amortized for U.S. tax purposes. The components of the provision (benefit) for income taxes, net are as follows (in millions):
````

**#8 `AMZN_FY2023_2023-12-31:140`** (gold #2)

````text
Item 7. Management’s Discussion and Analysis of Financial Condition and Results of Operations > Results of Operations
Operating income was $12.2 billion and $36.9 billion for 2022 and 2023. We believe that operating income is a more meaningful measure than gross profit and gross margin due to the diversity of our product categories and services. The North America operating income in 2023, as compared to the operating loss in the prior year, is primarily due to increased unit sales and increased advertising sales, partially offset by increased shipping and fulfillment costs and increased technology and infrastructure costs. The decrease in International operating loss in absolute dollars in 2023, compared to the prior year, is primarily due to increased unit sales and increased advertising sales, partially offset by increased fulfillment and shipping costs and increased technology and infrastructure costs. Changes in foreign exchange rates positively impacted operating loss by $246 million in 2023. The increase in AWS operating income in absolute dollars in 2023, compared to the prior year, is primarily due to increased sales, partially offset by increased payroll and related expenses and spending on technology infrastructure, both of which were primarily driven by additional investments to support AWS business growth. Changes in foreign exchange rates positively impacted operating income by $220 million in 2023. Operating Expenses
````

</details>

RQ2 citation match (section level): `cited=[('AMZN', 'Item 7'), ('AMZN', 'Item 8')] gold=[(None, 'Item 8'), (None, 'Item 7')]`

### System B (hybrid + rerank)

Model: `gpt-5.4-2026-03-05`. Hops: 1. Chunks retrieved: 5, cited: 2.

**Generated answer**

> Cash paid for income taxes increased from $6.0 billion in 2022 to $11.2 billion in 2023 [4].
>
> Percentage increase:
> \[
> \frac{11.2 - 6.0}{6.0} \times 100 \approx 86.7\%
> \]
>
> So, the increase was approximately **86.7%** [4].
>
> The primary operational factor cited for the increase in operating cash flows in 2023 was **an increase in net income (loss), excluding non-cash expenses, and changes in working capital** [2].

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `AMZN_FY2023_2023-12-31:112` | Item 7 › Overview |  |  | Our financial focus is on long-term, sustainable growth in free cash flows. Free cash flows are driven primarily by increasing operating income and efficiently managing accounts receivable, inventory, accounts payable, a… |
| 2 | `AMZN_FY2023_2023-12-31:127` | Item 7 › Liquidity and Capital Resources | ✓ | #2 | Cash provided by (used in) operating activities was $46.8 billion and $84.9 billion in 2022 and 2023. Our operating cash flows result primarily from cash received from our consumer, seller, developer, enterprise, and con… |
| 3 | `AMZN_FY2023_2023-12-31:140` | Item 7 › Results of Operations |  | #2 | Operating income was $12.2 billion and $36.9 billion for 2022 and 2023. We believe that operating income is a more meaningful measure than gross profit and gross margin due to the diversity of our product categories and … |
| 4 | `AMZN_FY2023_2023-12-31:130` | Item 7 › Liquidity and Capital Resources | ✓ | #1 | As of December 31, 2023, cash, cash equivalents, and marketable securities held by foreign subsidiaries were $4.7 billion. We intend to invest substantially all of our foreign subsidiary earnings, as well as our capital … |
| 5 | `AMZN_FY2023_2023-12-31:123` | Item 7 › Critical Accounting Estimates |  |  | We are also currently subject to tax controversies in various jurisdictions, and these jurisdictions may assess additional income tax liabilities against us. Developments in an audit, investigation, or other tax controve… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#2 `AMZN_FY2023_2023-12-31:127`** (cited, gold #2)

````text
Item 7. Management’s Discussion and Analysis of Financial Condition and Results of Operations > Liquidity and Capital Resources
Cash provided by (used in) operating activities was $46.8 billion and $84.9 billion in 2022 and 2023. Our operating cash flows result primarily from cash received from our consumer, seller, developer, enterprise, and content creator customers, and advertisers, offset by cash payments we make for products and services, employee compensation, payment processing and related transaction costs, operating leases, and interest payments. Cash received from our customers and other activities generally corresponds to our net sales. The increase in operating cash flow in 2023, compared to the prior year, was due to an increase in net income (loss), excluding non-cash expenses, and changes in working capital. Working capital at any specific point in time is subject to many variables, including variability in demand, inventory management and category expansion, the timing of cash receipts and payments, customer and vendor payment terms, and fluctuations in foreign exchange rates. Cash provided by (used in) investing activities corresponds with cash capital expenditures, including leasehold improvements, incentives received from property and equipment vendors, proceeds from asset sales, cash outlays for
````

**#3 `AMZN_FY2023_2023-12-31:140`** (gold #2)

````text
Item 7. Management’s Discussion and Analysis of Financial Condition and Results of Operations > Results of Operations
Operating income was $12.2 billion and $36.9 billion for 2022 and 2023. We believe that operating income is a more meaningful measure than gross profit and gross margin due to the diversity of our product categories and services. The North America operating income in 2023, as compared to the operating loss in the prior year, is primarily due to increased unit sales and increased advertising sales, partially offset by increased shipping and fulfillment costs and increased technology and infrastructure costs. The decrease in International operating loss in absolute dollars in 2023, compared to the prior year, is primarily due to increased unit sales and increased advertising sales, partially offset by increased fulfillment and shipping costs and increased technology and infrastructure costs. Changes in foreign exchange rates positively impacted operating loss by $246 million in 2023. The increase in AWS operating income in absolute dollars in 2023, compared to the prior year, is primarily due to increased sales, partially offset by increased payroll and related expenses and spending on technology infrastructure, both of which were primarily driven by additional investments to support AWS business growth. Changes in foreign exchange rates positively impacted operating income by $220 million in 2023. Operating Expenses
````

**#4 `AMZN_FY2023_2023-12-31:130`** (cited, gold #1)

````text
Item 7. Management’s Discussion and Analysis of Financial Condition and Results of Operations > Liquidity and Capital Resources
As of December 31, 2023, cash, cash equivalents, and marketable securities held by foreign subsidiaries were $4.7 billion. We intend to invest substantially all of our foreign subsidiary earnings, as well as our capital in our foreign subsidiaries, indefinitely outside of the U.S. in those jurisdictions in which we would incur significant, additional costs upon repatriation of such amounts. Our U.S. taxable income is reduced by accelerated depreciation deductions and increased by the impact of capitalized research and development expenses. U.S. tax rules provide for enhanced accelerated depreciation deductions by allowing us to expense a portion of qualified property, primarily equipment. These enhanced deductions are scheduled to phase out annually from 2023 through 2026. Our federal tax provision included a partial accelerated depreciation deduction election for 2021, and a full election for 2022 and 2023. Additionally, effective January 1, 2022, research and development expenses are required to be capitalized and amortized for U.S. tax purposes, which delays the deductibility of these expenses. Cash paid for U.S. (federal and state) and foreign income taxes (net of refunds) totaled $6.0 billion and $11.2 billion for 2022 and 2023.
````

</details>

RQ2 citation match (section level): `cited=[('AMZN', 'Item 7')] gold=[(None, 'Item 8'), (None, 'Item 7')]`

### System C v1 (adaptive multi-hop)

Model: `gpt-5.4`. Hops: 3. Chunks retrieved: 13, cited: 2.

**Generated answer**

> Cash paid for income taxes, net of refunds, increased from $6.0 billion in 2022 to $11.2 billion in 2023, which represents an 86.7% increase compared to 2022 [AMZN FY2023, Item 7, AMZN_FY2023_2023-12-31:130].  
>
> The Management’s Discussion and Analysis states that the increase in operating cash flow in 2023 compared to 2022 was due to an increase in net income (loss), excluding non-cash expenses, and changes in working capital [AMZN FY2023, Item 7, AMZN_FY2023_2023-12-31:127].

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `AMZN_FY2023_2023-12-31:337` | Item 8 › Note 9 — INCOME TAXES |  |  | The items accounting for differences between income taxes computed at the federal statutory rate and the provision (benefit) recorded for income taxes are as follows (in millions): |
| 2 | `AMZN_FY2023_2023-12-31:336` | Item 8 › Note 9 — INCOME TAXES |  |  | \| \| Year Ended December 31, \| \| \| \|---\|---\|---\|---\| \| \| 2021 \| 2022 \| 2023 \| \| U.S. \| $35,879 \| $(8,225) \| $32,328 \| \| International \| 2,272 \| 2,289 \| 5,229 \| \| Income (loss) before income taxes \| $38,151 \| $(5,936) \| $3… |
| 3 | `AMZN_FY2023_2023-12-31:130` | Item 7 › Liquidity and Capital Resources | ✓ | #1 | As of December 31, 2023, cash, cash equivalents, and marketable securities held by foreign subsidiaries were $4.7 billion. We intend to invest substantially all of our foreign subsidiary earnings, as well as our capital … |
| 4 | `AMZN_FY2023_2023-12-31:334` | Item 8 › Note 9 — INCOME TAXES |  |  | \| \| Year Ended December 31, \| \| \| \|---\|---\|---\|---\| \| \| 2021 \| 2022 \| 2023 \| \| U.S. Federal: \| \| \| \| \| Current \| $2,129 \| $2,175 \| $8,652 \| \| Deferred \| 155 \| (6,686) \| (5,505) \| \| Total \| 2,284 \| (4,511) \| 3,147 \| \| U.S… |
| 5 | `AMZN_FY2023_2023-12-31:333` | Item 8 › Note 9 — INCOME TAXES |  | #1 | In 2021, 2022, and 2023, we recorded a net tax provision (benefit) of $4.8 billion, $(3.2) billion, and $7.1 billion. Our U.S. taxable income is reduced by accelerated depreciation deductions and increased by the impact … |
| 6 | `AMZN_FY2023_2023-12-31:184` | Item 8 › (in millions) |  |  | \| \| Year Ended December 31, \| \| \| \|---\|---\|---\|---\| \| \| 2021 \| 2022 \| 2023 \| \| CASH, CASH EQUIVALENTS, AND RESTRICTED CASH, BEGINNING OF PERIOD \| $42,377 \| $36,477 \| $54,253 \| \| OPERATING ACTIVITIES: \| \| \| \| \| Net income… |
| 7 | `AMZN_FY2023_2023-12-31:124` | Item 7 › Liquidity and Capital Resources |  |  | Cash flow information is as follows (in millions): |
| 8 | `AMZN_FY2023_2023-12-31:127` | Item 7 › Liquidity and Capital Resources | ✓ | #2 | Cash provided by (used in) operating activities was $46.8 billion and $84.9 billion in 2022 and 2023. Our operating cash flows result primarily from cash received from our consumer, seller, developer, enterprise, and con… |
| 9 | `AMZN_FY2023_2023-12-31:125` | Item 7 › Liquidity and Capital Resources |  |  | \| \| Year Ended December 31, \| \| \|---\|---\|---\| \| \| 2022 \| 2023 \| \| Cash provided by (used in): \| \| \| \| Operating activities \| $46,752 \| $84,946 \| \| Investing activities \| (37,601) \| (49,833) \| \| Financing activities \| 9,7… |
| 10 | `AMZN_FY2023_2023-12-31:128` | Item 7 › Liquidity and Capital Resources |  |  | acquisitions, investments in other companies and intellectual property rights, and purchases, sales, and maturities of marketable securities. Cash provided by (used in) investing activities was $(37.6) billion and $(49.8… |
| 11 | `AMZN_FY2023_2023-12-31:129` | Item 7 › Liquidity and Capital Resources |  |  | Cash provided by (used in) financing activities was $9.7 billion and $(15.9) billion in 2022 and 2023. Cash inflows from financing activities resulted from proceeds from short-term debt, and other and long-term-debt of $… |
| 12 | `AMZN_FY2023_2023-12-31:126` | Item 7 › Liquidity and Capital Resources |  |  | Our principal sources of liquidity are cash flows generated from operations and our cash, cash equivalents, and marketable securities balances, which, at fair value, were $70.0 billion and $86.8 billion as of December 31… |
| 13 | `AMZN_FY2023_2023-12-31:132` | Item 7 › Liquidity and Capital Resources |  |  | We believe that cash flows generated from operations and our cash, cash equivalents, and marketable securities balances, as well as our borrowing arrangements, will be sufficient to meet our anticipated operating cash ne… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#3 `AMZN_FY2023_2023-12-31:130`** (cited, gold #1)

````text
Item 7. Management’s Discussion and Analysis of Financial Condition and Results of Operations > Liquidity and Capital Resources
As of December 31, 2023, cash, cash equivalents, and marketable securities held by foreign subsidiaries were $4.7 billion. We intend to invest substantially all of our foreign subsidiary earnings, as well as our capital in our foreign subsidiaries, indefinitely outside of the U.S. in those jurisdictions in which we would incur significant, additional costs upon repatriation of such amounts. Our U.S. taxable income is reduced by accelerated depreciation deductions and increased by the impact of capitalized research and development expenses. U.S. tax rules provide for enhanced accelerated depreciation deductions by allowing us to expense a portion of qualified property, primarily equipment. These enhanced deductions are scheduled to phase out annually from 2023 through 2026. Our federal tax provision included a partial accelerated depreciation deduction election for 2021, and a full election for 2022 and 2023. Additionally, effective January 1, 2022, research and development expenses are required to be capitalized and amortized for U.S. tax purposes, which delays the deductibility of these expenses. Cash paid for U.S. (federal and state) and foreign income taxes (net of refunds) totaled $6.0 billion and $11.2 billion for 2022 and 2023.
````

**#5 `AMZN_FY2023_2023-12-31:333`** (gold #1)

````text
Item 8. Financial Statements and Supplementary Data > Note 9 — INCOME TAXES
In 2021, 2022, and 2023, we recorded a net tax provision (benefit) of $4.8 billion, $(3.2) billion, and $7.1 billion. Our U.S. taxable income is reduced by accelerated depreciation deductions and increased by the impact of capitalized research and development expenses. Cash paid for income taxes, net of refunds, was $3.7 billion, $6.0 billion, and $11.2 billion for 2021, 2022, and 2023. Certain foreign subsidiary earnings and losses are subject to current U.S. taxation and the subsequent repatriation of those earnings is not subject to tax in the U.S. The U.S. tax rules also provide for enhanced accelerated depreciation deductions by allowing us to expense a portion of qualified property, primarily equipment. These enhanced deductions are scheduled to phase out annually from 2023 through 2026. Our federal tax provision included a partial accelerated depreciation deduction election for 2021, and a full election for 2022 and 2023. Effective January 1, 2022, research and development expenses are required to be capitalized and amortized for U.S. tax purposes. The components of the provision (benefit) for income taxes, net are as follows (in millions):
````

**#8 `AMZN_FY2023_2023-12-31:127`** (cited, gold #2)

````text
Item 7. Management’s Discussion and Analysis of Financial Condition and Results of Operations > Liquidity and Capital Resources
Cash provided by (used in) operating activities was $46.8 billion and $84.9 billion in 2022 and 2023. Our operating cash flows result primarily from cash received from our consumer, seller, developer, enterprise, and content creator customers, and advertisers, offset by cash payments we make for products and services, employee compensation, payment processing and related transaction costs, operating leases, and interest payments. Cash received from our customers and other activities generally corresponds to our net sales. The increase in operating cash flow in 2023, compared to the prior year, was due to an increase in net income (loss), excluding non-cash expenses, and changes in working capital. Working capital at any specific point in time is subject to many variables, including variability in demand, inventory management and category expansion, the timing of cash receipts and payments, customer and vendor payment terms, and fluctuations in foreign exchange rates. Cash provided by (used in) investing activities corresponds with cash capital expenditures, including leasehold improvements, incentives received from property and equipment vendors, proceeds from asset sales, cash outlays for
````

</details>

RQ2 citation match (section level): `cited=[('AMZN', 'Item 7')] gold=[(None, 'Item 8'), (None, 'Item 7')]`

**System C guardrail** (judge `gpt-5.4`): numerical claims 3, verified 3, ungrounded 0, uncited 0, derived 1; sentence verdicts: supported 1, partial 0, unsupported 0, unchecked 0.


<details><summary>Guardrail sentence verdicts</summary>

| sentence | verdict | judge reason |
|---|---|---|
| Cash paid for income taxes, net of refunds, increased from $6.0 billion in 2022 to $11.2 billion in 2023, which represents an 86.7% increase compared to 2022 [AMZN FY2023, Item 7, AMZN_FY2023_2023-12-31:130]. | None |  |
| The Management’s Discussion and Analysis states that the increase in operating cash flow in 2023 compared to 2022 was due to an increase in net income (loss), excluding non-cash expenses, and changes in working capital [AMZN FY2023, Item 7, AMZN_FY2023_2023-12-31:127]. | supported | The cited MD&A text explicitly states the increase in 2023 operating cash flow was due to higher net income (loss), excluding non-cash expenses, and changes in working capital. |

</details>

### System C v2 (agentic multi-hop + XBRL)

Model: `gpt-5.4`. Hops: 1. Chunks retrieved: 7, cited: 2.

**Generated answer**

> Cash paid for income taxes, net of refunds, increased from $6.0 billion in 2022 to $11.2 billion in 2023, which was an increase of 86.7% (($11.2 billion - $6.0 billion) / $6.0 billion) [AMZN FY2023, Item 7, AMZN_FY2023_2023-12-31:130] [AMZN FY2023, Item 8, AMZN_FY2023_2023-12-31:333].  
>
> The filing does not disclose in the provided evidence the primary operational factor cited in Management’s Discussion and Analysis that drove the increase in operating cash flows for the same period.

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `F-AMZN-2023` | SEC XBRL Reported Financials (financials.csv) |  |  | fiscal_year,fiscal_year_end,Revenue,NetIncome,OperatingIncome,TotalAssets,TotalLiabilities,StockholdersEquity,CashAndEquivalents,OperatingCashFlow,EPSDiluted 2023,2023-12-31,574785000000,30425000000,36852000000,527854000… |
| 2 | `AMZN_FY2023_2023-12-31:337` | Item 8 › Note 9 — INCOME TAXES |  |  | The items accounting for differences between income taxes computed at the federal statutory rate and the provision (benefit) recorded for income taxes are as follows (in millions): |
| 3 | `AMZN_FY2023_2023-12-31:336` | Item 8 › Note 9 — INCOME TAXES |  |  | \| \| Year Ended December 31, \| \| \| \|---\|---\|---\|---\| \| \| 2021 \| 2022 \| 2023 \| \| U.S. \| $35,879 \| $(8,225) \| $32,328 \| \| International \| 2,272 \| 2,289 \| 5,229 \| \| Income (loss) before income taxes \| $38,151 \| $(5,936) \| $3… |
| 4 | `AMZN_FY2023_2023-12-31:130` | Item 7 › Liquidity and Capital Resources | ✓ | #1 | As of December 31, 2023, cash, cash equivalents, and marketable securities held by foreign subsidiaries were $4.7 billion. We intend to invest substantially all of our foreign subsidiary earnings, as well as our capital … |
| 5 | `AMZN_FY2023_2023-12-31:334` | Item 8 › Note 9 — INCOME TAXES |  |  | \| \| Year Ended December 31, \| \| \| \|---\|---\|---\|---\| \| \| 2021 \| 2022 \| 2023 \| \| U.S. Federal: \| \| \| \| \| Current \| $2,129 \| $2,175 \| $8,652 \| \| Deferred \| 155 \| (6,686) \| (5,505) \| \| Total \| 2,284 \| (4,511) \| 3,147 \| \| U.S… |
| 6 | `AMZN_FY2023_2023-12-31:333` | Item 8 › Note 9 — INCOME TAXES | ✓ | #1 | In 2021, 2022, and 2023, we recorded a net tax provision (benefit) of $4.8 billion, $(3.2) billion, and $7.1 billion. Our U.S. taxable income is reduced by accelerated depreciation deductions and increased by the impact … |
| 7 | `AMZN_FY2023_2023-12-31:184` | Item 8 › (in millions) |  |  | \| \| Year Ended December 31, \| \| \| \|---\|---\|---\|---\| \| \| 2021 \| 2022 \| 2023 \| \| CASH, CASH EQUIVALENTS, AND RESTRICTED CASH, BEGINNING OF PERIOD \| $42,377 \| $36,477 \| $54,253 \| \| OPERATING ACTIVITIES: \| \| \| \| \| Net income… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#4 `AMZN_FY2023_2023-12-31:130`** (cited, gold #1)

````text
Item 7. Management’s Discussion and Analysis of Financial Condition and Results of Operations > Liquidity and Capital Resources
As of December 31, 2023, cash, cash equivalents, and marketable securities held by foreign subsidiaries were $4.7 billion. We intend to invest substantially all of our foreign subsidiary earnings, as well as our capital in our foreign subsidiaries, indefinitely outside of the U.S. in those jurisdictions in which we would incur significant, additional costs upon repatriation of such amounts. Our U.S. taxable income is reduced by accelerated depreciation deductions and increased by the impact of capitalized research and development expenses. U.S. tax rules provide for enhanced accelerated depreciation deductions by allowing us to expense a portion of qualified property, primarily equipment. These enhanced deductions are scheduled to phase out annually from 2023 through 2026. Our federal tax provision included a partial accelerated depreciation deduction election for 2021, and a full election for 2022 and 2023. Additionally, effective January 1, 2022, research and development expenses are required to be capitalized and amortized for U.S. tax purposes, which delays the deductibility of these expenses. Cash paid for U.S. (federal and state) and foreign income taxes (net of refunds) totaled $6.0 billion and $11.2 billion for 2022 and 2023.
````

**#6 `AMZN_FY2023_2023-12-31:333`** (cited, gold #1)

````text
Item 8. Financial Statements and Supplementary Data > Note 9 — INCOME TAXES
In 2021, 2022, and 2023, we recorded a net tax provision (benefit) of $4.8 billion, $(3.2) billion, and $7.1 billion. Our U.S. taxable income is reduced by accelerated depreciation deductions and increased by the impact of capitalized research and development expenses. Cash paid for income taxes, net of refunds, was $3.7 billion, $6.0 billion, and $11.2 billion for 2021, 2022, and 2023. Certain foreign subsidiary earnings and losses are subject to current U.S. taxation and the subsequent repatriation of those earnings is not subject to tax in the U.S. The U.S. tax rules also provide for enhanced accelerated depreciation deductions by allowing us to expense a portion of qualified property, primarily equipment. These enhanced deductions are scheduled to phase out annually from 2023 through 2026. Our federal tax provision included a partial accelerated depreciation deduction election for 2021, and a full election for 2022 and 2023. Effective January 1, 2022, research and development expenses are required to be capitalized and amortized for U.S. tax purposes. The components of the provision (benefit) for income taxes, net are as follows (in millions):
````

</details>

RQ2 citation match (section level): `cited=[('AMZN', 'Item 7'), ('AMZN', 'Item 8')] gold=[(None, 'Item 8'), (None, 'Item 7')]`

**System C guardrail** (judge `gpt-5.4`): numerical claims 6, verified 6, ungrounded 0, uncited 0, derived 1; sentence verdicts: supported 1, partial 0, unsupported 0, unchecked 0.


<details><summary>Guardrail sentence verdicts</summary>

| sentence | verdict | judge reason |
|---|---|---|
| Cash paid for income taxes, net of refunds, increased from $6.0 billion in 2022 to $11.2 billion in 2023, which was an increase of 86.7% (($11.2 billion - $6.0 billion) / $6.0 billion) [AMZN FY2023, Item 7, AMZN_FY2023_2023-12-31:130] [AMZN FY2023, Item 8, AMZN_FY2023_2023-12-31:333]. | None |  |
| The filing does not disclose in the provided evidence the primary operational factor cited in Management’s Discussion and Analysis that drove the increase in operating cash flows for the same period. | supported | The provided evidence includes cash flow figures and components but does not disclose an MD&A statement identifying the primary operational factor driving the increase in operating cash flows. |

</details>
