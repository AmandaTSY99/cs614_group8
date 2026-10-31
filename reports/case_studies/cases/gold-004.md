# gold-004: Multi-hop table (one filing)

[← all cases](../README.md) · company: Apple Inc. (AAPL) · fiscal year: 2019 · recipe `table` · hop `multi` · answer type `numeric` · scope `single_doc` · RQ2 category `quantitative_tabular`

## Gold QA

**Question**

> What is the ratio of Apple Inc.'s interest expense to its interest and dividend income for fiscal year 2019?

**Gold answer**

> 0.72

**Program**: `divide(3576, 4961)` → `0.7208224148357186`

**Gold numbers** (RQ2 numeric_accuracy targets): 0.72

**Gold evidence**

1. `AAPL_FY2019_2019-09-28` · Item 7. Management’s Discussion and Analysis of Financial Condition and Results of Operations › Other Income/(Expense), Net · table

   > | Interest and dividend income | $4,961 |  | $5,686 |  | $5,201 |

2. `AAPL_FY2019_2019-09-28` · Item 7. Management’s Discussion and Analysis of Financial Condition and Results of Operations › Other Income/(Expense), Net · table

   > | Interest expense | (3,576) |  | (3,240) |  | (2,323) |

## Scorecard

| Metric | A (vanilla dense) | B (hybrid + rerank) | C v1 (adaptive multi-hop) | C v2 (agentic multi-hop + XBRL) |
|---|---|---|---|---|
| **Retrieval (RQ1)** | | | | |
| chunks retrieved | 10 | 5 | 6 | 7 |
| recall@5 | 1.00 | 1.00 | 1.00 | 1.00 |
| recall@all | 1.00 | 1.00 | 1.00 | 1.00 |
| complete@all | 1 | 1 | 1 | 1 |
| average precision (lexical) | 1.00 | 0.50 | 1.00 | 0.58 |
| gold evidence first rank | #1: 1, #2: 1 | #1: 2, #2: 2 | #1: 1, #2: 1 | #1: 2, #2: 2 |
| **Answer (RQ3 string match)** | | | | |
| numeric_correct | ✓ | ✓ | ✓ | ✓ |
| keypoint_recall | – | – | – | – |
| **Answer & citations (RQ2)** | | | | |
| numeric_accuracy | 1.00 | 1.00 | 1.00 | 1.00 |
| citation precision | 0.00 | 1.00 | 0.50 | 0.00 |
| citation recall | 0.00 | 1.00 | 1.00 | 0.00 |
| citation F1 | 0.00 | 1.00 | 0.67 | 0.00 |
| has a citation | 1 | 1 | 1 | 1 |
| grounding error rate | – | – | 0.33 | 0.33 |
| **Cost (RQ3)** | | | | |
| retrieval hops | 1 | 1 | 1 | 1 |
| tokens | 2560 | 978 | 6395 | 6754 |
| cost (USD) | 0.0004 | 0.0002 | 0.0213 | 0.0215 |
| latency (s) | 2.1 | 7.4 | 7.6 | 7.0 |

Definitions: [README › Metrics](../README.md#metrics). `–` = not applicable (e.g. no gold number, no citations, no guardrail).

## System outputs

### System A (vanilla dense)

Model: `gpt-5.4-2026-03-05`. Hops: 1. Chunks retrieved: 10, cited: 1.

**Generated answer**

> For fiscal year 2019, Apple reported interest expense of $3,576 million and interest and dividend income of $4,961 million [1].
>
> Ratio = 3,576 / 4,961 ≈ 0.72
>
> So, the ratio of interest expense to interest and dividend income was approximately 0.72:1, or about 72% [1].

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `AAPL_FY2019_2019-09-28:242` | Item 8 › Other Income/(Expense), Net | ✓ | #1, #2 | \| \| 2019 \| 2018 \| 2017 \| \|---\|---\|---\|---\| \| Interest and dividend income \| $4,961 \| $5,686 \| $5,201 \| \| Interest expense \| (3,576) \| (3,240) \| (2,323) \| \| Other income/(expense), net \| 422 \| (441) \| (133) \| \| Total othe… |
| 2 | `AAPL_FY2019_2019-09-28:123` | Item 7 › Other Income/(Expense), Net |  | #1, #2 | \| \| 2019 \| Change \| 2018 \| Change \| 2017 \| \|---\|---\|---\|---\|---\|---\| \| Interest and dividend income \| $4,961 \| \| $5,686 \| \| $5,201 \| \| Interest expense \| (3,576) \| \| (3,240) \| \| (2,323) \| \| Other income/(expense), net \| … |
| 3 | `AAPL_FY2019_2019-09-28:255` | Item 8 › Interest and Penalties |  |  | The Company includes interest and penalties related to income tax matters within the provision for income taxes. As of September 28, 2019 and September 29, 2018, the total amount of gross interest and penalties accrued w… |
| 4 | `AAPL_FY2019_2019-09-28:124` | Item 7 › Other Income/(Expense), Net |  |  | The year-over-year decrease in OI&E during 2019 was due primarily to lower interest income and higher interest expense, partially offset by the impact of foreign exchange–related items. The weighted-average interest rate… |
| 5 | `AAPL_FY2019_2019-09-28:314` | Item 8 › Note 12 – Selected Quarterly Financial Information (Unaudited) |  |  | \| \| Fourth Quarter \| Third Quarter \| Second Quarter \| First Quarter \| \|---\|---\|---\|---\|---\| \| 2019: \| \| \| \| \| \| Total net sales \| $64,040 \| $53,809 \| $58,015 \| $84,310 \| \| Gross margin \| $24,313 \| $20,227 \| $21,821 \| $32… |
| 6 | `AAPL_FY2019_2019-09-28:315` | Item 8 › Note 12 – Selected Quarterly Financial Information (Unaudited) |  |  | \| \| Fourth Quarter \| Third Quarter \| Second Quarter \| First Quarter \| \|---\|---\|---\|---\|---\| \| 2018: \| \| \| \| \| \| Total net sales \| $62,900 \| $53,265 \| $61,137 \| $88,293 \| \| Gross margin \| $24,084 \| $20,421 \| $23,422 \| $33… |
| 7 | `AAPL_FY2019_2019-09-28:308` | Item 8 › Note 11 – Segment Information and Geographic Data |  |  | \| \| 2019 \| 2018 \| 2017 \| \|---\|---\|---\|---\| \| Segment operating income \| $85,950 \| $90,242 \| $77,631 \| \| Research and development expense \| (16,217) \| (14,236) \| (11,581) \| \| Other corporate expenses, net \| (5,803) \| (5,1… |
| 8 | `AAPL_FY2019_2019-09-28:179` | Item 8 › CONSOLIDATED STATEMENTS OF CASH FLOWS |  |  | \| \| Years ended \| \| \| \|---\|---\|---\|---\| \| \| September 28, 2019 \| September 29, 2018 \| September 30, 2017 \| \| Payments for taxes related to net share settlement of equity awards \| (2,817) \| (2,527) \| (1,874) \| \| Payments … |
| 9 | `AAPL_FY2019_2019-09-28:102` | Item 6 |  |  | \| \| 2019 \| 2018 \| 2017 \| 2016 \| 2015 \| \|---\|---\|---\|---\|---\|---\| \| Total net sales \| $260,174 \| $265,595 \| $229,234 \| $215,639 \| $233,715 \| \| Net income \| $55,256 \| $59,531 \| $48,351 \| $45,687 \| $53,394 \| \| Earnings per … |
| 10 | `AAPL_FY2019_2019-09-28:273` | Item 8 › Note 8 – Comprehensive Income |  |  | \| \| Cumulative Foreign Currency Translation \| Unrealized Gains/Losses on Derivative Instruments \| Unrealized Gains/Losses on Marketable Securities \| Total \| \|---\|---\|---\|---\|---\| \| Balances as of September 30, 2017 \| $(3… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#1 `AAPL_FY2019_2019-09-28:242`** (cited, gold #1, gold #2)

````text
Item 8. Financial Statements and Supplementary Data > Other Income/(Expense), Net (table)
|  | 2019 | 2018 | 2017 |
|---|---|---|---|
| Interest and dividend income | $4,961 | $5,686 | $5,201 |
| Interest expense | (3,576) | (3,240) | (2,323) |
| Other income/(expense), net | 422 | (441) | (133) |
| Total other income/(expense), net | $1,807 | $2,005 | $2,745 |
````

**#2 `AAPL_FY2019_2019-09-28:123`** (gold #1, gold #2)

````text
Item 7. Management’s Discussion and Analysis of Financial Condition and Results of Operations > Other Income/(Expense), Net (table)
|  | 2019 | Change | 2018 | Change | 2017 |
|---|---|---|---|---|---|
| Interest and dividend income | $4,961 |  | $5,686 |  | $5,201 |
| Interest expense | (3,576) |  | (3,240) |  | (2,323) |
| Other income/(expense), net | 422 |  | (441) |  | (133) |
| Total other income/(expense), net | $1,807 | (10)% | $2,005 | (27)% | $2,745 |
````

</details>

RQ2 citation match (section level): `cited=[('AAPL', 'Item 8')] gold=[(None, 'Item 7')]`

### System B (hybrid + rerank)

Model: `gpt-5.4-2026-03-05`. Hops: 1. Chunks retrieved: 5, cited: 1.

**Generated answer**

> For fiscal year 2019, Apple reported interest expense of $3,576 million and interest and dividend income of $4,961 million. The ratio of interest expense to interest and dividend income is:
>
> 3,576 / 4,961 ≈ 0.72
>
> So the ratio is approximately 0.72:1, or about 72% [2].

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `AAPL_FY2019_2019-09-28:106` | Item 7 › Fiscal 2019 Highlights |  |  | Total net sales decreased 2% or $5.4 billion during 2019 compared to 2018, driven by lower net sales of iPhone, partially offset by higher net sales of Wearables, Home and Accessories and Services in all geographic opera… |
| 2 | `AAPL_FY2019_2019-09-28:123` | Item 7 › Other Income/(Expense), Net | ✓ | #1, #2 | \| \| 2019 \| Change \| 2018 \| Change \| 2017 \| \|---\|---\|---\|---\|---\|---\| \| Interest and dividend income \| $4,961 \| \| $5,686 \| \| $5,201 \| \| Interest expense \| (3,576) \| \| (3,240) \| \| (2,323) \| \| Other income/(expense), net \| … |
| 3 | `AAPL_FY2019_2019-09-28:264` | Item 8 › Term Debt |  |  | The effective interest rates for the Notes include the interest on the Notes, amortization of the discount or premium and, if applicable, adjustments related to hedging. The Company recognized $3.2 billion, $3.0 billion … |
| 4 | `AAPL_FY2019_2019-09-28:242` | Item 8 › Other Income/(Expense), Net |  | #1, #2 | \| \| 2019 \| 2018 \| 2017 \| \|---\|---\|---\|---\| \| Interest and dividend income \| $4,961 \| $5,686 \| $5,201 \| \| Interest expense \| (3,576) \| (3,240) \| (2,323) \| \| Other income/(expense), net \| 422 \| (441) \| (133) \| \| Total othe… |
| 5 | `AAPL_FY2019_2019-09-28:151` | Item 7A › Interest Rate Risk |  |  | The Company’s exposure to changes in interest rates relates primarily to the Company’s investment portfolio and outstanding debt. While the Company is exposed to global interest rate fluctuations, the Company’s interest … |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#2 `AAPL_FY2019_2019-09-28:123`** (cited, gold #1, gold #2)

````text
Item 7. Management’s Discussion and Analysis of Financial Condition and Results of Operations > Other Income/(Expense), Net (table)
|  | 2019 | Change | 2018 | Change | 2017 |
|---|---|---|---|---|---|
| Interest and dividend income | $4,961 |  | $5,686 |  | $5,201 |
| Interest expense | (3,576) |  | (3,240) |  | (2,323) |
| Other income/(expense), net | 422 |  | (441) |  | (133) |
| Total other income/(expense), net | $1,807 | (10)% | $2,005 | (27)% | $2,745 |
````

**#4 `AAPL_FY2019_2019-09-28:242`** (gold #1, gold #2)

````text
Item 8. Financial Statements and Supplementary Data > Other Income/(Expense), Net (table)
|  | 2019 | 2018 | 2017 |
|---|---|---|---|
| Interest and dividend income | $4,961 | $5,686 | $5,201 |
| Interest expense | (3,576) | (3,240) | (2,323) |
| Other income/(expense), net | 422 | (441) | (133) |
| Total other income/(expense), net | $1,807 | $2,005 | $2,745 |
````

</details>

RQ2 citation match (section level): `cited=[('AAPL', 'Item 7')] gold=[(None, 'Item 7')]`

### System C v1 (adaptive multi-hop)

Model: `gpt-5.4`. Hops: 1. Chunks retrieved: 6, cited: 2.

**Generated answer**

> Apple Inc.'s interest expense was $(3,576) and its interest and dividend income was $4,961 in fiscal year 2019, so the ratio of interest expense to interest and dividend income was approximately 0.72:1.00 [AAPL FY2019, Item 8, AAPL_FY2019_2019-09-28:242] [AAPL FY2019, Item 7, AAPL_FY2019_2019-09-28:123]
>
> > [Guardrail Audit Warning]: Manual verification required; these numerical figures could not be matched in their cited chunks: 0.72; 1 sentence(s) are not supported by their cited chunks.

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `AAPL_FY2019_2019-09-28:242` | Item 8 › Other Income/(Expense), Net | ✓ | #1, #2 | \| \| 2019 \| 2018 \| 2017 \| \|---\|---\|---\|---\| \| Interest and dividend income \| $4,961 \| $5,686 \| $5,201 \| \| Interest expense \| (3,576) \| (3,240) \| (2,323) \| \| Other income/(expense), net \| 422 \| (441) \| (133) \| \| Total othe… |
| 2 | `AAPL_FY2019_2019-09-28:123` | Item 7 › Other Income/(Expense), Net | ✓ | #1, #2 | \| \| 2019 \| Change \| 2018 \| Change \| 2017 \| \|---\|---\|---\|---\|---\|---\| \| Interest and dividend income \| $4,961 \| \| $5,686 \| \| $5,201 \| \| Interest expense \| (3,576) \| \| (3,240) \| \| (2,323) \| \| Other income/(expense), net \| … |
| 3 | `AAPL_FY2019_2019-09-28:124` | Item 7 › Other Income/(Expense), Net |  |  | The year-over-year decrease in OI&E during 2019 was due primarily to lower interest income and higher interest expense, partially offset by the impact of foreign exchange–related items. The weighted-average interest rate… |
| 4 | `AAPL_FY2019_2019-09-28:271` | Item 8 › Note 8 – Comprehensive Income |  |  | \| Comprehensive Income Components \| Financial Statement Line Item \| 2019 \| 2018 \| \|---\|---\|---\|---\| \| Unrealized (gains)/losses on derivative instruments: \| \| \| \| \| Foreign exchange contracts \| Total net sales \| $(206) \|… |
| 5 | `AAPL_FY2019_2019-09-28:179` | Item 8 › CONSOLIDATED STATEMENTS OF CASH FLOWS |  |  | \| \| Years ended \| \| \| \|---\|---\|---\|---\| \| \| September 28, 2019 \| September 29, 2018 \| September 30, 2017 \| \| Payments for taxes related to net share settlement of equity awards \| (2,817) \| (2,527) \| (1,874) \| \| Payments … |
| 6 | `AAPL_FY2019_2019-09-28:255` | Item 8 › Interest and Penalties |  |  | The Company includes interest and penalties related to income tax matters within the provision for income taxes. As of September 28, 2019 and September 29, 2018, the total amount of gross interest and penalties accrued w… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#1 `AAPL_FY2019_2019-09-28:242`** (cited, gold #1, gold #2)

````text
Item 8. Financial Statements and Supplementary Data > Other Income/(Expense), Net (table)
|  | 2019 | 2018 | 2017 |
|---|---|---|---|
| Interest and dividend income | $4,961 | $5,686 | $5,201 |
| Interest expense | (3,576) | (3,240) | (2,323) |
| Other income/(expense), net | 422 | (441) | (133) |
| Total other income/(expense), net | $1,807 | $2,005 | $2,745 |
````

**#2 `AAPL_FY2019_2019-09-28:123`** (cited, gold #1, gold #2)

````text
Item 7. Management’s Discussion and Analysis of Financial Condition and Results of Operations > Other Income/(Expense), Net (table)
|  | 2019 | Change | 2018 | Change | 2017 |
|---|---|---|---|---|---|
| Interest and dividend income | $4,961 |  | $5,686 |  | $5,201 |
| Interest expense | (3,576) |  | (3,240) |  | (2,323) |
| Other income/(expense), net | 422 |  | (441) |  | (133) |
| Total other income/(expense), net | $1,807 | (10)% | $2,005 | (27)% | $2,745 |
````

</details>

RQ2 citation match (section level): `cited=[('AAPL', 'Item 8'), ('AAPL', 'Item 7')] gold=[(None, 'Item 7')]`

**System C guardrail** (judge `gpt-5.4`): numerical claims 4, verified 3, ungrounded 1, uncited 0, derived 1; sentence verdicts: supported 0, partial 0, unsupported 0, unchecked 0.

- ungrounded numbers: 0.72

<details><summary>Guardrail sentence verdicts</summary>

| sentence | verdict | judge reason |
|---|---|---|
| Apple Inc.'s interest expense was $(3,576) and its interest and dividend income was $4,961 in fiscal year 2019, so the ratio of interest expense to interest and dividend income was approximately 0.72:1.00 [AAPL FY2019, Item 8, AAPL_FY2019_2019-09-28:242] [AAPL FY2019, Item 7, AAPL_FY2019_2019-09-28:123] | None |  |

</details>

### System C v2 (agentic multi-hop + XBRL)

Model: `gpt-5.4`. Hops: 1. Chunks retrieved: 7, cited: 1.

**Generated answer**

> Apple Inc.'s interest expense was $(3,576) and its interest and dividend income was $4,961 in fiscal year 2019, so the ratio of interest expense to interest and dividend income was approximately 0.72:1. [AAPL FY2019, Item 8, AAPL_FY2019_2019-09-28:242]
>
> > [Guardrail Audit Warning]: Manual verification required; these numerical figures could not be matched in their cited chunks: 0.72; 1 sentence(s) are not supported by their cited chunks.

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `F-AAPL-2019` | SEC XBRL Reported Financials (financials.csv) |  |  | fiscal_year,fiscal_year_end,Revenue,NetIncome,OperatingIncome,TotalAssets,TotalLiabilities,StockholdersEquity,CashAndEquivalents,OperatingCashFlow,EPSDiluted 2019,2019-09-28,260174000000,55256000000,63930000000,338516000… |
| 2 | `AAPL_FY2019_2019-09-28:242` | Item 8 › Other Income/(Expense), Net | ✓ | #1, #2 | \| \| 2019 \| 2018 \| 2017 \| \|---\|---\|---\|---\| \| Interest and dividend income \| $4,961 \| $5,686 \| $5,201 \| \| Interest expense \| (3,576) \| (3,240) \| (2,323) \| \| Other income/(expense), net \| 422 \| (441) \| (133) \| \| Total othe… |
| 3 | `AAPL_FY2019_2019-09-28:123` | Item 7 › Other Income/(Expense), Net |  | #1, #2 | \| \| 2019 \| Change \| 2018 \| Change \| 2017 \| \|---\|---\|---\|---\|---\|---\| \| Interest and dividend income \| $4,961 \| \| $5,686 \| \| $5,201 \| \| Interest expense \| (3,576) \| \| (3,240) \| \| (2,323) \| \| Other income/(expense), net \| … |
| 4 | `AAPL_FY2019_2019-09-28:124` | Item 7 › Other Income/(Expense), Net |  |  | The year-over-year decrease in OI&E during 2019 was due primarily to lower interest income and higher interest expense, partially offset by the impact of foreign exchange–related items. The weighted-average interest rate… |
| 5 | `AAPL_FY2019_2019-09-28:271` | Item 8 › Note 8 – Comprehensive Income |  |  | \| Comprehensive Income Components \| Financial Statement Line Item \| 2019 \| 2018 \| \|---\|---\|---\|---\| \| Unrealized (gains)/losses on derivative instruments: \| \| \| \| \| Foreign exchange contracts \| Total net sales \| $(206) \|… |
| 6 | `AAPL_FY2019_2019-09-28:179` | Item 8 › CONSOLIDATED STATEMENTS OF CASH FLOWS |  |  | \| \| Years ended \| \| \| \|---\|---\|---\|---\| \| \| September 28, 2019 \| September 29, 2018 \| September 30, 2017 \| \| Payments for taxes related to net share settlement of equity awards \| (2,817) \| (2,527) \| (1,874) \| \| Payments … |
| 7 | `AAPL_FY2019_2019-09-28:255` | Item 8 › Interest and Penalties |  |  | The Company includes interest and penalties related to income tax matters within the provision for income taxes. As of September 28, 2019 and September 29, 2018, the total amount of gross interest and penalties accrued w… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#2 `AAPL_FY2019_2019-09-28:242`** (cited, gold #1, gold #2)

````text
Item 8. Financial Statements and Supplementary Data > Other Income/(Expense), Net (table)
|  | 2019 | 2018 | 2017 |
|---|---|---|---|
| Interest and dividend income | $4,961 | $5,686 | $5,201 |
| Interest expense | (3,576) | (3,240) | (2,323) |
| Other income/(expense), net | 422 | (441) | (133) |
| Total other income/(expense), net | $1,807 | $2,005 | $2,745 |
````

**#3 `AAPL_FY2019_2019-09-28:123`** (gold #1, gold #2)

````text
Item 7. Management’s Discussion and Analysis of Financial Condition and Results of Operations > Other Income/(Expense), Net (table)
|  | 2019 | Change | 2018 | Change | 2017 |
|---|---|---|---|---|---|
| Interest and dividend income | $4,961 |  | $5,686 |  | $5,201 |
| Interest expense | (3,576) |  | (3,240) |  | (2,323) |
| Other income/(expense), net | 422 |  | (441) |  | (133) |
| Total other income/(expense), net | $1,807 | (10)% | $2,005 | (27)% | $2,745 |
````

</details>

RQ2 citation match (section level): `cited=[('AAPL', 'Item 8')] gold=[(None, 'Item 7')]`

**System C guardrail** (judge `gpt-5.4`): numerical claims 3, verified 2, ungrounded 1, uncited 0, derived 0; sentence verdicts: supported 0, partial 0, unsupported 0, unchecked 0.

- ungrounded numbers: 0.72

<details><summary>Guardrail sentence verdicts</summary>

| sentence | verdict | judge reason |
|---|---|---|
| Apple Inc.'s interest expense was $(3,576) and its interest and dividend income was $4,961 in fiscal year 2019, so the ratio of interest expense to interest and dividend income was approximately 0.72:1. [AAPL FY2019, Item 8, AAPL_FY2019_2019-09-28:242] | None |  |

</details>
