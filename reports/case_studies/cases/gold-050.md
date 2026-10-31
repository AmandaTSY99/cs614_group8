# gold-050: Multi-hop table (one filing)

[← all cases](../README.md) · company: JOHNSON & JOHNSON (JNJ) · fiscal year: 2016 · recipe `table` · hop `multi` · answer type `numeric` · scope `single_doc` · RQ2 category `quantitative_tabular`

## Gold QA

**Question**

> For Johnson & Johnson in fiscal year 2016, what was research and development expense as a percentage of sales to customers?

**Gold answer**

> 12.65%

**Program**: `divide(9095, 71890), multiply(#0, 100)` → `12.651272777855057`

**Gold numbers** (RQ2 numeric_accuracy targets): 12.65%

**Gold evidence**

1. `JNJ_FY2016_2017-01-01` · Item 8. FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA › (Dollars and Shares in Millions Except Per Share Amounts) (Note 1) · table

   > Research and development expense | 9,095 | 9,046 | 8,494

2. `JNJ_FY2016_2017-01-01` · Item 8. FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA › (Dollars and Shares in Millions Except Per Share Amounts) (Note 1) · table

   > | Sales to customers | $71,890 | 70,074 | 74,331 |

## Scorecard

| Metric | A (vanilla dense) | B (hybrid + rerank) | C v1 (adaptive multi-hop) | C v2 (agentic multi-hop + XBRL) |
|---|---|---|---|---|
| **Retrieval (RQ1)** | | | | |
| chunks retrieved | 10 | 5 | 6 | 7 |
| recall@5 | 0.00 | 1.00 | 1.00 | 1.00 |
| recall@all | 1.00 | 1.00 | 1.00 | 1.00 |
| complete@all | 1 | 1 | 1 | 1 |
| average precision (lexical) | 0.18 | 0.75 | 0.58 | 0.42 |
| gold evidence first rank | #1: 6, #2: 6 | #1: 1, #2: 4 | #1: 2, #2: 2 | #1: 3, #2: 3 |
| **Answer (RQ3 string match)** | | | | |
| numeric_correct | ✓ | ✓ | ✓ | ✓ |
| keypoint_recall | – | – | – | – |
| **Answer & citations (RQ2)** | | | | |
| numeric_accuracy | 1.00 | 1.00 | 1.00 | 1.00 |
| citation precision | 0.50 | 0.50 | 0.00 | 0.00 |
| citation recall | 1.00 | 1.00 | 0.00 | 0.00 |
| citation F1 | 0.67 | 0.67 | 0.00 | 0.00 |
| has a citation | 1 | 1 | 1 | 1 |
| grounding error rate | – | – | 0.00 | 0.00 |
| **Cost (RQ3)** | | | | |
| retrieval hops | 1 | 1 | 1 | 1 |
| tokens | 2085 | 1590 | 4543 | 5088 |
| cost (USD) | 0.0003 | 0.0003 | 0.0146 | 0.0157 |
| latency (s) | 2.6 | 6.9 | 5.4 | 5.9 |

Definitions: [README › Metrics](../README.md#metrics). `–` = not applicable (e.g. no gold number, no citations, no guardrail).

## System outputs

### System A (vanilla dense)

Model: `gpt-5.4-2026-03-05`. Hops: 1. Chunks retrieved: 10, cited: 2.

**Generated answer**

> For Johnson & Johnson in fiscal year 2016, research and development expense was **12.7% of sales to customers** [10].
>
> This is consistent with research and development expense of **$9,095 million** and sales to customers of **$71,890 million** [6][10].

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `JNJ_FY2016_2017-01-01:141` | Item 7 › Analysis of Consolidated Earnings Before Provision for Taxes on Income |  |  | As a percent to segment sales Research and development activities represent a significant part of the Company's business. These expenditures relate to the processes of discovering, testing and developing new products, up… |
| 2 | `JNJ_FY2016_2017-01-01:136` | Item 7 › Analysis of Consolidated Earnings Before Provision for Taxes on Income |  |  | Cost of Products Sold and Selling, Marketing and Administrative Expenses: Cost of products sold and selling, marketing and administrative expenses as a percent to sales were as follows: |
| 3 | `JNJ_FY2016_2017-01-01:138` | Item 7 › Analysis of Consolidated Earnings Before Provision for Taxes on Income |  |  | In 2016, cost of products sold as a percent to sales decreased to 30.2% from 30.7% as compared to the same period a year ago. Favorable mix in the business and cost improvement programs was partially offset by the unfavo… |
| 4 | `JNJ_FY2016_2017-01-01:39` | Item 1 › Research and Development |  |  | Research activities represent a significant part of the Company’s businesses. Research and development expenditures relate to the processes of discovering, testing and developing new products, improving existing products… |
| 5 | `JNJ_FY2016_2017-01-01:137` | Item 7 › Analysis of Consolidated Earnings Before Provision for Taxes on Income |  |  | \| % of Sales \| 2016 \| 2015 \| 2014 \| \|---\|---\|---\|---\| \| Cost of products sold \| 30.2% \| 30.7 \| 30.6 \| \| Percent point increase/(decrease) over the prior year \| (0.5) \| 0.1 \| (0.7) \| \| Selling, marketing and administrativ… |
| 6 | `JNJ_FY2016_2017-01-01:212` | Item 8 › (Dollars and Shares in Millions Except Per Share Amounts) (Note 1) | ✓ | #1, #2 | \| \| 2016 \| 2015 \| 2014 \| \|---\|---\|---\|---\| \| Sales to customers \| $71,890 \| 70,074 \| 74,331 \| \| Cost of products sold \| 21,685 \| 21,536 \| 22,746 \| \| Gross profit \| 50,205 \| 48,538 \| 51,585 \| \| Selling, marketing and admi… |
| 7 | `JNJ_FY2016_2017-01-01:262` | Item 8 › Research and Development |  |  | \| Nature/Type of Collaboration \| Statement of Earnings Presentation \| \|---\|---\| \| Third-party sale of product \| Sales to customers \| \| Royalties/milestones paid to collaborative partner (post-regulatory approval)* \| Cost… |
| 8 | `JNJ_FY2016_2017-01-01:106` | Item 7 › Analysis of Consolidated Sales |  |  | In 2016, worldwide sales increased 2.6% to $71.9 billion, compared to a decrease of 5.7% in 2015 and an increase of 4.2% in 2014. These sales changes consisted of the following: |
| 9 | `JNJ_FY2016_2017-01-01:263` | Item 8 › Research and Development |  |  | Milestones are capitalized as intangible assets and amortized to cost of goods sold over the useful life. For all years presented, there was no individual project that represented greater than 5% of the total annual cons… |
| 10 | `JNJ_FY2016_2017-01-01:140` | Item 7 › Analysis of Consolidated Earnings Before Provision for Taxes on Income | ✓ | #1 | \| \| 2016 \| \| 2015 \| \| 2014 \| \| \|---\|---\|---\|---\|---\|---\|---\| \| (Dollars in Millions) \| Amount \| % of Sales* \| Amount \| % of Sales* \| Amount \| % of Sales* \| \| Consumer \| $580 \| 4.4% \| 625 \| 4.6 \| 629 \| 4.3 \| \| Pharmaceuti… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#6 `JNJ_FY2016_2017-01-01:212`** (cited, gold #1, gold #2)

````text
Item 8. FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA > (Dollars and Shares in Millions Except Per Share Amounts) (Note 1) (table)
|  | 2016 | 2015 | 2014 |
|---|---|---|---|
| Sales to customers | $71,890 | 70,074 | 74,331 |
| Cost of products sold | 21,685 | 21,536 | 22,746 |
| Gross profit | 50,205 | 48,538 | 51,585 |
| Selling, marketing and administrative expenses | 19,945 | 21,203 | 21,954 |
| Research and development expense | 9,095 | 9,046 | 8,494 |
| In-process research and development | 29 | 224 | 178 |
| Interest income | (368) | (128) | (67) |
| Interest expense, net of portion capitalized (Note 4) | 726 | 552 | 533 |
| Other (income) expense, net | 484 | (2,064) | (70) |
| Restructuring (Note 22) | 491 | 509 | — |
| Earnings before provision for taxes on income | 19,803 | 19,196 | 20,563 |
| Provision for taxes on income (Note 8) | 3,263 | 3,787 | 4,240 |
| Net earnings | $16,540 | 15,409 | 16,323 |
| Net earnings per share (Notes 1 and 15) |  |  |  |
| Basic | $6.04 | 5.56 | 5.80 |
| Diluted | $5.93 | 5.48 | 5.70 |
````

**#10 `JNJ_FY2016_2017-01-01:140`** (cited, gold #1)

````text
Item 7. MANAGEMENT’S DISCUSSION AND ANALYSIS OF RESULTS OF OPERATIONS AND FINANCIAL CONDITION > Analysis of Consolidated Earnings Before Provision for Taxes on Income (table)
|  | 2016 |  | 2015 |  | 2014 |  |
|---|---|---|---|---|---|---|
| (Dollars in Millions) | Amount | % of Sales* | Amount | % of Sales* | Amount | % of Sales* |
| Consumer | $580 | 4.4% | 625 | 4.6 | 629 | 4.3 |
| Pharmaceutical | 6,967 | 20.8 | 6,821 | 21.7 | 6,213 | 19.2 |
| Medical Devices | 1,548 | 6.2 | 1,600 | 6.4 | 1,652 | 6.0 |
| Total research and development expense | $9,095 | 12.7% | 9,046 | 12.9 | 8,494 | 11.4 |
| Percent increase/(decrease) over the prior year | 0.5% |  | 6.5 |  | 3.8 |  |
````

</details>

RQ2 citation match (section level): `cited=[('JNJ', 'Item 8'), ('JNJ', 'Item 7')] gold=[(None, 'Item 8')]`

### System B (hybrid + rerank)

Model: `gpt-5.4-2026-03-05`. Hops: 1. Chunks retrieved: 5, cited: 2.

**Generated answer**

> For Johnson & Johnson in fiscal year 2016, research and development expense was **12.7% of sales to customers** [1].
>
> Using the figures directly: R&D expense was **$9,095 million** and sales to customers were **$71,890 million**, which is about **12.7%** [4].

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `JNJ_FY2016_2017-01-01:140` | Item 7 › Analysis of Consolidated Earnings Before Provision for Taxes on Income | ✓ | #1 | \| \| 2016 \| \| 2015 \| \| 2014 \| \| \|---\|---\|---\|---\|---\|---\|---\| \| (Dollars in Millions) \| Amount \| % of Sales* \| Amount \| % of Sales* \| Amount \| % of Sales* \| \| Consumer \| $580 \| 4.4% \| 625 \| 4.6 \| 629 \| 4.3 \| \| Pharmaceuti… |
| 2 | `JNJ_FY2016_2017-01-01:141` | Item 7 › Analysis of Consolidated Earnings Before Provision for Taxes on Income |  |  | As a percent to segment sales Research and development activities represent a significant part of the Company's business. These expenditures relate to the processes of discovering, testing and developing new products, up… |
| 3 | `JNJ_FY2016_2017-01-01:39` | Item 1 › Research and Development |  |  | Research activities represent a significant part of the Company’s businesses. Research and development expenditures relate to the processes of discovering, testing and developing new products, improving existing products… |
| 4 | `JNJ_FY2016_2017-01-01:212` | Item 8 › (Dollars and Shares in Millions Except Per Share Amounts) (Note 1) | ✓ | #1, #2 | \| \| 2016 \| 2015 \| 2014 \| \|---\|---\|---\|---\| \| Sales to customers \| $71,890 \| 70,074 \| 74,331 \| \| Cost of products sold \| 21,685 \| 21,536 \| 22,746 \| \| Gross profit \| 50,205 \| 48,538 \| 51,585 \| \| Selling, marketing and admi… |
| 5 | `JNJ_FY2016_2017-01-01:143` | Item 7 › Analysis of Consolidated Earnings Before Provision for Taxes on Income |  |  | Other (Income) Expense, Net: Other (income) expense, net is the account where the Company records gains and losses related to the sale and write-down of certain investments in equity securities held by Johnson & Johnson … |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#1 `JNJ_FY2016_2017-01-01:140`** (cited, gold #1)

````text
Item 7. MANAGEMENT’S DISCUSSION AND ANALYSIS OF RESULTS OF OPERATIONS AND FINANCIAL CONDITION > Analysis of Consolidated Earnings Before Provision for Taxes on Income (table)
|  | 2016 |  | 2015 |  | 2014 |  |
|---|---|---|---|---|---|---|
| (Dollars in Millions) | Amount | % of Sales* | Amount | % of Sales* | Amount | % of Sales* |
| Consumer | $580 | 4.4% | 625 | 4.6 | 629 | 4.3 |
| Pharmaceutical | 6,967 | 20.8 | 6,821 | 21.7 | 6,213 | 19.2 |
| Medical Devices | 1,548 | 6.2 | 1,600 | 6.4 | 1,652 | 6.0 |
| Total research and development expense | $9,095 | 12.7% | 9,046 | 12.9 | 8,494 | 11.4 |
| Percent increase/(decrease) over the prior year | 0.5% |  | 6.5 |  | 3.8 |  |
````

**#4 `JNJ_FY2016_2017-01-01:212`** (cited, gold #1, gold #2)

````text
Item 8. FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA > (Dollars and Shares in Millions Except Per Share Amounts) (Note 1) (table)
|  | 2016 | 2015 | 2014 |
|---|---|---|---|
| Sales to customers | $71,890 | 70,074 | 74,331 |
| Cost of products sold | 21,685 | 21,536 | 22,746 |
| Gross profit | 50,205 | 48,538 | 51,585 |
| Selling, marketing and administrative expenses | 19,945 | 21,203 | 21,954 |
| Research and development expense | 9,095 | 9,046 | 8,494 |
| In-process research and development | 29 | 224 | 178 |
| Interest income | (368) | (128) | (67) |
| Interest expense, net of portion capitalized (Note 4) | 726 | 552 | 533 |
| Other (income) expense, net | 484 | (2,064) | (70) |
| Restructuring (Note 22) | 491 | 509 | — |
| Earnings before provision for taxes on income | 19,803 | 19,196 | 20,563 |
| Provision for taxes on income (Note 8) | 3,263 | 3,787 | 4,240 |
| Net earnings | $16,540 | 15,409 | 16,323 |
| Net earnings per share (Notes 1 and 15) |  |  |  |
| Basic | $6.04 | 5.56 | 5.80 |
| Diluted | $5.93 | 5.48 | 5.70 |
````

</details>

RQ2 citation match (section level): `cited=[('JNJ', 'Item 7'), ('JNJ', 'Item 8')] gold=[(None, 'Item 8')]`

### System C v1 (adaptive multi-hop)

Model: `gpt-5.4`. Hops: 1. Chunks retrieved: 6, cited: 1.

**Generated answer**

> For Johnson & Johnson in fiscal year 2016, research and development expense was 12.7% of sales to customers. [JNJ FY2016, Item 7, JNJ_FY2016_2017-01-01:140]

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `JNJ_FY2016_2017-01-01:262` | Item 8 › Research and Development |  |  | \| Nature/Type of Collaboration \| Statement of Earnings Presentation \| \|---\|---\| \| Third-party sale of product \| Sales to customers \| \| Royalties/milestones paid to collaborative partner (post-regulatory approval)* \| Cost… |
| 2 | `JNJ_FY2016_2017-01-01:212` | Item 8 › (Dollars and Shares in Millions Except Per Share Amounts) (Note 1) |  | #1, #2 | \| \| 2016 \| 2015 \| 2014 \| \|---\|---\|---\|---\| \| Sales to customers \| $71,890 \| 70,074 \| 74,331 \| \| Cost of products sold \| 21,685 \| 21,536 \| 22,746 \| \| Gross profit \| 50,205 \| 48,538 \| 51,585 \| \| Selling, marketing and admi… |
| 3 | `JNJ_FY2016_2017-01-01:140` | Item 7 › Analysis of Consolidated Earnings Before Provision for Taxes on Income | ✓ | #1 | \| \| 2016 \| \| 2015 \| \| 2014 \| \| \|---\|---\|---\|---\|---\|---\|---\| \| (Dollars in Millions) \| Amount \| % of Sales* \| Amount \| % of Sales* \| Amount \| % of Sales* \| \| Consumer \| $580 \| 4.4% \| 625 \| 4.6 \| 629 \| 4.3 \| \| Pharmaceuti… |
| 4 | `JNJ_FY2016_2017-01-01:260` | Item 8 › Research and Development |  |  | Research and development expenses are expensed as incurred. Upfront and milestone payments made to third parties in connection with research and development collaborations are expensed as incurred up to the point of regu… |
| 5 | `JNJ_FY2016_2017-01-01:382` | Item 8 › Restricted Share Units and Performance Share Units |  |  | ­ See Note 1 for a description of the segments in which the Company operates. Export sales are not significant. In 2016, the Company had two wholesalers distributing products for all three segments that represented appro… |
| 6 | `JNJ_FY2016_2017-01-01:292` | Item 8 › Reclassification |  |  | \| (Dollars in Millions) \| Gain/(Loss) Recognized In Accumulated OCI(1) \| \| Gain/(Loss) Reclassified From Accumulated OCI Into Income(1) \| \| Gain/(Loss) Recognized In Other Income/Expense(2) \| \| \|---\|---\|---\|---\|---\|---\|-… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#2 `JNJ_FY2016_2017-01-01:212`** (gold #1, gold #2)

````text
Item 8. FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA > (Dollars and Shares in Millions Except Per Share Amounts) (Note 1) (table)
|  | 2016 | 2015 | 2014 |
|---|---|---|---|
| Sales to customers | $71,890 | 70,074 | 74,331 |
| Cost of products sold | 21,685 | 21,536 | 22,746 |
| Gross profit | 50,205 | 48,538 | 51,585 |
| Selling, marketing and administrative expenses | 19,945 | 21,203 | 21,954 |
| Research and development expense | 9,095 | 9,046 | 8,494 |
| In-process research and development | 29 | 224 | 178 |
| Interest income | (368) | (128) | (67) |
| Interest expense, net of portion capitalized (Note 4) | 726 | 552 | 533 |
| Other (income) expense, net | 484 | (2,064) | (70) |
| Restructuring (Note 22) | 491 | 509 | — |
| Earnings before provision for taxes on income | 19,803 | 19,196 | 20,563 |
| Provision for taxes on income (Note 8) | 3,263 | 3,787 | 4,240 |
| Net earnings | $16,540 | 15,409 | 16,323 |
| Net earnings per share (Notes 1 and 15) |  |  |  |
| Basic | $6.04 | 5.56 | 5.80 |
| Diluted | $5.93 | 5.48 | 5.70 |
````

**#3 `JNJ_FY2016_2017-01-01:140`** (cited, gold #1)

````text
Item 7. MANAGEMENT’S DISCUSSION AND ANALYSIS OF RESULTS OF OPERATIONS AND FINANCIAL CONDITION > Analysis of Consolidated Earnings Before Provision for Taxes on Income (table)
|  | 2016 |  | 2015 |  | 2014 |  |
|---|---|---|---|---|---|---|
| (Dollars in Millions) | Amount | % of Sales* | Amount | % of Sales* | Amount | % of Sales* |
| Consumer | $580 | 4.4% | 625 | 4.6 | 629 | 4.3 |
| Pharmaceutical | 6,967 | 20.8 | 6,821 | 21.7 | 6,213 | 19.2 |
| Medical Devices | 1,548 | 6.2 | 1,600 | 6.4 | 1,652 | 6.0 |
| Total research and development expense | $9,095 | 12.7% | 9,046 | 12.9 | 8,494 | 11.4 |
| Percent increase/(decrease) over the prior year | 0.5% |  | 6.5 |  | 3.8 |  |
````

</details>

RQ2 citation match (section level): `cited=[('JNJ', 'Item 7')] gold=[(None, 'Item 8')]`

**System C guardrail** (judge `gpt-5.4`): numerical claims 1, verified 1, ungrounded 0, uncited 0, derived 0; sentence verdicts: supported 0, partial 0, unsupported 0, unchecked 0.


<details><summary>Guardrail sentence verdicts</summary>

| sentence | verdict | judge reason |
|---|---|---|
| For Johnson & Johnson in fiscal year 2016, research and development expense was 12.7% of sales to customers. [JNJ FY2016, Item 7, JNJ_FY2016_2017-01-01:140] | None |  |

</details>

### System C v2 (agentic multi-hop + XBRL)

Model: `gpt-5.4`. Hops: 1. Chunks retrieved: 7, cited: 1.

**Generated answer**

> For Johnson & Johnson in fiscal year 2016, research and development expense was 12.7% of sales to customers. [JNJ FY2016, Item 7, JNJ_FY2016_2017-01-01:140]

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `F-JNJ-2016` | SEC XBRL Reported Financials (financials.csv) |  |  | fiscal_year,fiscal_year_end,Revenue,NetIncome,OperatingIncome,TotalAssets,TotalLiabilities,StockholdersEquity,CashAndEquivalents,OperatingCashFlow,EPSDiluted 2016,2017-01-01,,16540000000,,141208000000,70790000000,,189720… |
| 2 | `JNJ_FY2016_2017-01-01:262` | Item 8 › Research and Development |  |  | \| Nature/Type of Collaboration \| Statement of Earnings Presentation \| \|---\|---\| \| Third-party sale of product \| Sales to customers \| \| Royalties/milestones paid to collaborative partner (post-regulatory approval)* \| Cost… |
| 3 | `JNJ_FY2016_2017-01-01:212` | Item 8 › (Dollars and Shares in Millions Except Per Share Amounts) (Note 1) |  | #1, #2 | \| \| 2016 \| 2015 \| 2014 \| \|---\|---\|---\|---\| \| Sales to customers \| $71,890 \| 70,074 \| 74,331 \| \| Cost of products sold \| 21,685 \| 21,536 \| 22,746 \| \| Gross profit \| 50,205 \| 48,538 \| 51,585 \| \| Selling, marketing and admi… |
| 4 | `JNJ_FY2016_2017-01-01:140` | Item 7 › Analysis of Consolidated Earnings Before Provision for Taxes on Income | ✓ | #1 | \| \| 2016 \| \| 2015 \| \| 2014 \| \| \|---\|---\|---\|---\|---\|---\|---\| \| (Dollars in Millions) \| Amount \| % of Sales* \| Amount \| % of Sales* \| Amount \| % of Sales* \| \| Consumer \| $580 \| 4.4% \| 625 \| 4.6 \| 629 \| 4.3 \| \| Pharmaceuti… |
| 5 | `JNJ_FY2016_2017-01-01:292` | Item 8 › Reclassification |  |  | \| (Dollars in Millions) \| Gain/(Loss) Recognized In Accumulated OCI(1) \| \| Gain/(Loss) Reclassified From Accumulated OCI Into Income(1) \| \| Gain/(Loss) Recognized In Other Income/Expense(2) \| \| \|---\|---\|---\|---\|---\|---\|-… |
| 6 | `JNJ_FY2016_2017-01-01:260` | Item 8 › Research and Development |  |  | Research and development expenses are expensed as incurred. Upfront and milestone payments made to third parties in connection with research and development collaborations are expensed as incurred up to the point of regu… |
| 7 | `JNJ_FY2016_2017-01-01:93` | Item 6 › Summary of Operations and Statistical Data 2006-2016 |  | #1 | \| (Dollars in Millions Except Per Share Amounts) \| 2016 \| 2015 \| 2014 \| 2013 \| 2012 \| 2011 \| 2010 \| 2009 \| 2008 \| 2007 \| 2006 \| \|---\|---\|---\|---\|---\|---\|---\|---\|---\|---\|---\|---\| \| Research and development expense \| 9,095… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#3 `JNJ_FY2016_2017-01-01:212`** (gold #1, gold #2)

````text
Item 8. FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA > (Dollars and Shares in Millions Except Per Share Amounts) (Note 1) (table)
|  | 2016 | 2015 | 2014 |
|---|---|---|---|
| Sales to customers | $71,890 | 70,074 | 74,331 |
| Cost of products sold | 21,685 | 21,536 | 22,746 |
| Gross profit | 50,205 | 48,538 | 51,585 |
| Selling, marketing and administrative expenses | 19,945 | 21,203 | 21,954 |
| Research and development expense | 9,095 | 9,046 | 8,494 |
| In-process research and development | 29 | 224 | 178 |
| Interest income | (368) | (128) | (67) |
| Interest expense, net of portion capitalized (Note 4) | 726 | 552 | 533 |
| Other (income) expense, net | 484 | (2,064) | (70) |
| Restructuring (Note 22) | 491 | 509 | — |
| Earnings before provision for taxes on income | 19,803 | 19,196 | 20,563 |
| Provision for taxes on income (Note 8) | 3,263 | 3,787 | 4,240 |
| Net earnings | $16,540 | 15,409 | 16,323 |
| Net earnings per share (Notes 1 and 15) |  |  |  |
| Basic | $6.04 | 5.56 | 5.80 |
| Diluted | $5.93 | 5.48 | 5.70 |
````

**#4 `JNJ_FY2016_2017-01-01:140`** (cited, gold #1)

````text
Item 7. MANAGEMENT’S DISCUSSION AND ANALYSIS OF RESULTS OF OPERATIONS AND FINANCIAL CONDITION > Analysis of Consolidated Earnings Before Provision for Taxes on Income (table)
|  | 2016 |  | 2015 |  | 2014 |  |
|---|---|---|---|---|---|---|
| (Dollars in Millions) | Amount | % of Sales* | Amount | % of Sales* | Amount | % of Sales* |
| Consumer | $580 | 4.4% | 625 | 4.6 | 629 | 4.3 |
| Pharmaceutical | 6,967 | 20.8 | 6,821 | 21.7 | 6,213 | 19.2 |
| Medical Devices | 1,548 | 6.2 | 1,600 | 6.4 | 1,652 | 6.0 |
| Total research and development expense | $9,095 | 12.7% | 9,046 | 12.9 | 8,494 | 11.4 |
| Percent increase/(decrease) over the prior year | 0.5% |  | 6.5 |  | 3.8 |  |
````

**#7 `JNJ_FY2016_2017-01-01:93`** (gold #1)

````text
Item 6. SELECTED FINANCIAL DATA > Summary of Operations and Statistical Data 2006-2016 (table)
| (Dollars in Millions Except Per Share Amounts) | 2016 | 2015 | 2014 | 2013 | 2012 | 2011 | 2010 | 2009 | 2008 | 2007 | 2006 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Research and development expense | 9,095 | 9,046 | 8,494 | 8,183 | 7,665 | 7,548 | 6,844 | 6,986 | 7,577 | 7,680 | 7,125 |
| In-process research and development | 29 | 224 | 178 | 580 | 1,163 | — | — | — | 181 | 807 | 559 |
| Interest income | (368) | (128) | (67) | (74) | (64) | (91) | (107) | (90) | (361) | (452) | (829) |
| Interest expense, net of portion capitalized | 726 | 552 | 533 | 482 | 532 | 571 | 455 | 451 | 435 | 296 | 63 |
| Other (income) expense, net | 484 | (2,064) | (70) | 2,498 | 1,626 | 2,743 | (768) | (526) | (1,015) | 534 | (671) |
| Restructuring | 491 | 509 | — | — | — | 569 | — | 1,073 | — | 745 | — |
````

</details>

RQ2 citation match (section level): `cited=[('JNJ', 'Item 7')] gold=[(None, 'Item 8')]`

**System C guardrail** (judge `gpt-5.4`): numerical claims 1, verified 1, ungrounded 0, uncited 0, derived 0; sentence verdicts: supported 0, partial 0, unsupported 0, unchecked 0.


<details><summary>Guardrail sentence verdicts</summary>

| sentence | verdict | judge reason |
|---|---|---|
| For Johnson & Johnson in fiscal year 2016, research and development expense was 12.7% of sales to customers. [JNJ FY2016, Item 7, JNJ_FY2016_2017-01-01:140] | None |  |

</details>
