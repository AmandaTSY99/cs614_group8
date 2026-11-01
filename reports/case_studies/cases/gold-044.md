# gold-044: Multi-hop table (one filing)

[← all cases](../README.md) · company: JOHNSON & JOHNSON (JNJ) · fiscal year: 2018 · recipe `table` · hop `multi` · answer type `numeric` · scope `single_doc` · RQ2 category `quantitative_tabular`

## Gold QA

**Question**

> For Johnson & Johnson's fiscal year 2018, what were net earnings as a percentage of sales to customers, using the amounts as reported?

**Gold answer**

> 18.75%

**Program**: `divide(15297, 81581), multiply(#0, 100)` → `18.750689498780353`

**Gold numbers** (RQ2 numeric_accuracy targets): 18.75%

**Gold evidence**

1. `JNJ_FY2018_2018-12-30` · Item 8. FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA › Recently Adopted Accounting Standards · table

   > | Net earnings | 15,297 | (28) | 15,269 |

2. `JNJ_FY2018_2018-12-30` · Item 8. FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA › Recently Adopted Accounting Standards · table

   > | Sales to customers | $81,581 | (35) | 81,546 |

## Scorecard

| Metric | A (vanilla dense) | B (hybrid + rerank) | C v1 (adaptive multi-hop) | C v2 (agentic multi-hop + XBRL) |
|---|---|---|---|---|
| **Retrieval (RQ1)** | | | | |
| chunks retrieved | 10 | 5 | 6 | 7 |
| recall@5 | 0.00 | 1.00 | 1.00 | 1.00 |
| recall@all | 0.50 | 1.00 | 1.00 | 1.00 |
| complete@all | 0 | 1 | 1 | 1 |
| average precision (lexical) | 0.17 | 0.42 | 0.50 | 0.37 |
| gold evidence first rank | #1: –, #2: 6 | #1: 4, #2: 3 | #1: 4, #2: 2 | #1: 5, #2: 3 |
| **Answer (RQ3 string match)** | | | | |
| numeric_correct | ✓ | ✓ | ✓ | ✓ |
| keypoint_recall | – | – | – | – |
| **Answer & citations (RQ2)** | | | | |
| numeric_accuracy | 1.00 | 1.00 | 1.00 | 1.00 |
| citation precision | 0.50 | 0.50 | 0.50 | 0.50 |
| citation recall | 1.00 | 1.00 | 1.00 | 1.00 |
| citation F1 | 0.67 | 0.67 | 0.67 | 0.67 |
| has a citation | 1 | 1 | 1 | 1 |
| grounding error rate | – | – | 0.00 | 0.00 |
| **Cost (RQ3)** | | | | |
| retrieval hops | 1 | 1 | 1 | 1 |
| tokens | 2522 | 1923 | 4904 | 5253 |
| cost (USD) | 0.0004 | 0.0003 | 0.0163 | 0.0171 |
| latency (s) | 2.7 | 6.8 | 7.2 | 5.6 |

Definitions: [README › Metrics](../README.md#metrics). `–` = not applicable (e.g. no gold number, no citations, no guardrail).

## System outputs

### System A (vanilla dense)

Model: `gpt-5.4-2026-03-05`. Hops: 1. Chunks retrieved: 10, cited: 2.

**Generated answer**

> For fiscal year 2018, Johnson & Johnson’s net earnings as a percentage of sales to customers was **18.8%** [5].
>
> Using the reported amounts:
> - **Net earnings:** **$15,297 million** [6]
> - **Sales to customers:** **$81,581 million** [6]
>
> Calculation:
> - \( 15,297 \div 81,581 \approx 18.8\% \) [5][6]

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `JNJ_FY2018_2018-12-30:135` | Item 7 › Analysis of Consolidated Earnings Before Provision for Taxes on Income |  |  | \| % of Sales \| 2018 \| 2017 \| 2016 \| \|---\|---\|---\|---\| \| Cost of products sold* \| 33.2% \| 33.3 \| 30.3 \| \| Percent point increase/(decrease) over the prior year \| (0.1) \| 3.0 \| (0.3) \| \| Selling, marketing and administrati… |
| 2 | `JNJ_FY2018_2018-12-30:139` | Item 7 › Analysis of Consolidated Earnings Before Provision for Taxes on Income |  |  | Prior years amounts were reclassified to conform to current year presentation (adoption of ASU 2017-07) **As a percent to segment sales |
| 3 | `JNJ_FY2018_2018-12-30:134` | Item 7 › Analysis of Consolidated Earnings Before Provision for Taxes on Income |  |  | Consolidated earnings before provision for taxes on income was $18.0 billion, $17.7 billion and $19.8 billion for the fiscal years ended 2018, 2017 and 2016, respectively. As a percent to sales, consolidated earnings bef… |
| 4 | `JNJ_FY2018_2018-12-30:138` | Item 7 › Analysis of Consolidated Earnings Before Provision for Taxes on Income |  |  | \| \| 2018 \| \| 2017 \| \| 2016 \| \| \|---\|---\|---\|---\|---\|---\|---\| \| (Dollars in Millions) \| Amount \| % of Sales** \| Amount \| % of Sales** \| Amount \| % of Sales** \| \| Consumer \| $565 \| 4.1% \| 586 \| 4.3 \| 585 \| 4.4 \| \| Pharmace… |
| 5 | `JNJ_FY2018_2018-12-30:99` | Item 6 › Summary of Operations and Statistical Data 2008-2018 | ✓ |  | \| (Dollars in Millions Except Per Share Amounts) \| 2018 \| 2017 \| 2016 \| 2015 \| 2014 \| 2013 \| 2012 \| 2011 \| 2010 \| 2009 \| 2008 \| \|---\|---\|---\|---\|---\|---\|---\|---\|---\|---\|---\|---\| \| Net earnings attributable to Johnson & J… |
| 6 | `JNJ_FY2018_2018-12-30:209` | Item 8 › (Dollars and Shares in Millions Except Per Share Amounts) (Note 1) | ✓ | #2 | \| \| 2018 \| 2017 \| 2016 \| \|---\|---\|---\|---\| \| Sales to customers \| $81,581 \| 76,450 \| 71,890 \| \| Cost of products sold \| 27,091 \| 25,439 \| 21,789 \| \| Gross profit \| 54,490 \| 51,011 \| 50,101 \| \| Selling, marketing and admi… |
| 7 | `JNJ_FY2018_2018-12-30:148` | Item 7 › Income Before Tax by Segment |  |  | \| \| Income Before Tax \| \| Segment Sales \| \| Percent of Segment Sales \| \| \|---\|---\|---\|---\|---\|---\|---\| \| (Dollars in Millions) \| 2018 \| 2017 \| 2018 \| 2017 \| 2018 \| 2017 \| \| Consumer \| $2,320 \| 2,524 \| 13,853 \| 13,602 \| 1… |
| 8 | `JNJ_FY2018_2018-12-30:413` | Item 8 › Restricted Share Units and Performance Share Units |  |  | \| \| 2018 \| \| \| \| 2017 \| \| \| \| \|---\|---\|---\|---\|---\|---\|---\|---\|---\| \| Net earnings (loss) \| 4,367 \| 3,954 \| 3,934 \| 3,042 \| 4,422 \| 3,827 \| 3,764 \| (10,713) \| \| Basic net earnings (loss) per share \| $1.63 \| 1.47 \| 1.47 \|… |
| 9 | `JNJ_FY2018_2018-12-30:109` | Item 7 › Analysis of Consolidated Sales |  |  | In 2018, worldwide sales increased 6.7% to $81.6 billion, compared to an increases of 6.3% and 2.6% in 2017 and 2016, respectively. These sales changes consisted of the following: |
| 10 | `JNJ_FY2018_2018-12-30:370` | Item 8 › Valuation Hierarchy |  |  | Net currency transaction gains and losses included in Other (income) expense were losses of $265 million, $216 million and $289 million in 2018, 2017 and 2016, respectively. 15. Earnings Per Share The following is a reco… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#5 `JNJ_FY2018_2018-12-30:99`** (cited)

````text
Item 6. SELECTED FINANCIAL DATA > Summary of Operations and Statistical Data 2008-2018 (table)
| (Dollars in Millions Except Per Share Amounts) | 2018 | 2017 | 2016 | 2015 | 2014 | 2013 | 2012 | 2011 | 2010 | 2009 | 2008 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Net earnings attributable to Johnson & Johnson | 15,297 | 1,300 | 16,540 | 15,409 | 16,323 | 13,831 | 10,853 | 9,672 | 13,334 | 12,266 | 12,949 |
| Percent of sales to customers | 18.8% | 1.7 | 23.0 | 22.0 | 22.0 | 19.4 | 16.1 | 14.9 | 21.7 | 19.8 | 20.3 |
| Diluted net earnings per share of common stock (1) | $5.61 | 0.47 | 5.93 | 5.48 | 5.70 | 4.81 | 3.86 | 3.49 | 4.78 | 4.40 | 4.57 |
| Percent return on average shareholders’ equity | 25.5% | 2.0 | 23.4 | 21.9 | 22.7 | 19.9 | 17.8 | 17.0 | 24.9 | 26.4 | 30.2 |
| Percent increase (decrease) over previous year: |  |  |  |  |  |  |  |  |  |  |  |
````

**#6 `JNJ_FY2018_2018-12-30:209`** (cited, gold #2)

````text
Item 8. FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA > (Dollars and Shares in Millions Except Per Share Amounts) (Note 1) (table)
|  | 2018 | 2017 | 2016 |
|---|---|---|---|
| Sales to customers | $81,581 | 76,450 | 71,890 |
| Cost of products sold | 27,091 | 25,439 | 21,789 |
| Gross profit | 54,490 | 51,011 | 50,101 |
| Selling, marketing and administrative expenses | 22,540 | 21,520 | 20,067 |
| Research and development expense | 10,775 | 10,594 | 9,143 |
| In-process research and development | 1,126 | 408 | 29 |
| Interest income | (611) | (385) | (368) |
| Interest expense, net of portion capitalized (Note 4) | 1,005 | 934 | 726 |
| Other (income) expense, net | 1,405 | (42) | 210 |
| Restructuring (Note 22) | 251 | 309 | 491 |
| Earnings before provision for taxes on income | 17,999 | 17,673 | 19,803 |
| Provision for taxes on income (Note 8) | 2,702 | 16,373 | 3,263 |
| Net earnings | $15,297 | 1,300 | 16,540 |
| Net earnings per share (Notes 1 and 15) |  |  |  |
| Basic | $5.70 | 0.48 | 6.04 |
| Diluted | $5.61 | 0.47 | 5.93 |
````

</details>

RQ2 citation match (section level): `cited=[('JNJ', 'Item 6'), ('JNJ', 'Item 8')] gold=[(None, 'Item 8')]`

### System B (hybrid + rerank)

Model: `gpt-5.4-2026-03-05`. Hops: 1. Chunks retrieved: 5, cited: 2.

**Generated answer**

> For fiscal year 2018, Johnson & Johnson’s net earnings as a percentage of sales to customers was **18.8%** [1].
>
> Using the as-reported amounts:
> - Net earnings = **$15,297 million** [3]
> - Sales to customers = **$81,581 million** [3]
>
> Calculation: 15,297 / 81,581 ≈ **18.8%** [1][3]

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `JNJ_FY2018_2018-12-30:99` | Item 6 › Summary of Operations and Statistical Data 2008-2018 | ✓ |  | \| (Dollars in Millions Except Per Share Amounts) \| 2018 \| 2017 \| 2016 \| 2015 \| 2014 \| 2013 \| 2012 \| 2011 \| 2010 \| 2009 \| 2008 \| \|---\|---\|---\|---\|---\|---\|---\|---\|---\|---\|---\|---\| \| Net earnings attributable to Johnson & J… |
| 2 | `JNJ_FY2018_2018-12-30:100` | Item 6 › Summary of Operations and Statistical Data 2008-2018 |  |  | \| (Dollars in Millions Except Per Share Amounts) \| 2018 \| 2017 \| 2016 \| 2015 \| 2014 \| 2013 \| 2012 \| 2011 \| 2010 \| 2009 \| 2008 \| \|---\|---\|---\|---\|---\|---\|---\|---\|---\|---\|---\|---\| \| Sales to customers \| 6.7% \| 6.3 \| 2.6 \| … |
| 3 | `JNJ_FY2018_2018-12-30:209` | Item 8 › (Dollars and Shares in Millions Except Per Share Amounts) (Note 1) | ✓ | #2 | \| \| 2018 \| 2017 \| 2016 \| \|---\|---\|---\|---\| \| Sales to customers \| $81,581 \| 76,450 \| 71,890 \| \| Cost of products sold \| 27,091 \| 25,439 \| 21,789 \| \| Gross profit \| 54,490 \| 51,011 \| 50,101 \| \| Selling, marketing and admi… |
| 4 | `JNJ_FY2018_2018-12-30:228` | Item 8 › Recently Adopted Accounting Standards |  | #1, #2 | \| Statement of Earnings - For the fiscal year ended December 30, 2018 \| \| \| \| \|---\|---\|---\|---\| \| (Dollars in millions) \| As Reported \| Effect of change \| Balance without adoption of ASC 606 \| \| Sales to customers \| $81,… |
| 5 | `JNJ_FY2018_2018-12-30:149` | Item 7 › Income Before Tax by Segment |  |  | (1) See Note 18 to the Consolidated Financial Statements for more details. (2) Amounts not allocated to segments include interest (income) expense and general corporate (income) expense. Consumer Segment: In 2018, the Co… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#1 `JNJ_FY2018_2018-12-30:99`** (cited)

````text
Item 6. SELECTED FINANCIAL DATA > Summary of Operations and Statistical Data 2008-2018 (table)
| (Dollars in Millions Except Per Share Amounts) | 2018 | 2017 | 2016 | 2015 | 2014 | 2013 | 2012 | 2011 | 2010 | 2009 | 2008 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Net earnings attributable to Johnson & Johnson | 15,297 | 1,300 | 16,540 | 15,409 | 16,323 | 13,831 | 10,853 | 9,672 | 13,334 | 12,266 | 12,949 |
| Percent of sales to customers | 18.8% | 1.7 | 23.0 | 22.0 | 22.0 | 19.4 | 16.1 | 14.9 | 21.7 | 19.8 | 20.3 |
| Diluted net earnings per share of common stock (1) | $5.61 | 0.47 | 5.93 | 5.48 | 5.70 | 4.81 | 3.86 | 3.49 | 4.78 | 4.40 | 4.57 |
| Percent return on average shareholders’ equity | 25.5% | 2.0 | 23.4 | 21.9 | 22.7 | 19.9 | 17.8 | 17.0 | 24.9 | 26.4 | 30.2 |
| Percent increase (decrease) over previous year: |  |  |  |  |  |  |  |  |  |  |  |
````

**#3 `JNJ_FY2018_2018-12-30:209`** (cited, gold #2)

````text
Item 8. FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA > (Dollars and Shares in Millions Except Per Share Amounts) (Note 1) (table)
|  | 2018 | 2017 | 2016 |
|---|---|---|---|
| Sales to customers | $81,581 | 76,450 | 71,890 |
| Cost of products sold | 27,091 | 25,439 | 21,789 |
| Gross profit | 54,490 | 51,011 | 50,101 |
| Selling, marketing and administrative expenses | 22,540 | 21,520 | 20,067 |
| Research and development expense | 10,775 | 10,594 | 9,143 |
| In-process research and development | 1,126 | 408 | 29 |
| Interest income | (611) | (385) | (368) |
| Interest expense, net of portion capitalized (Note 4) | 1,005 | 934 | 726 |
| Other (income) expense, net | 1,405 | (42) | 210 |
| Restructuring (Note 22) | 251 | 309 | 491 |
| Earnings before provision for taxes on income | 17,999 | 17,673 | 19,803 |
| Provision for taxes on income (Note 8) | 2,702 | 16,373 | 3,263 |
| Net earnings | $15,297 | 1,300 | 16,540 |
| Net earnings per share (Notes 1 and 15) |  |  |  |
| Basic | $5.70 | 0.48 | 6.04 |
| Diluted | $5.61 | 0.47 | 5.93 |
````

**#4 `JNJ_FY2018_2018-12-30:228`** (gold #1, gold #2)

````text
Item 8. FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA > Recently Adopted Accounting Standards (table)
| Statement of Earnings - For the fiscal year ended December 30, 2018 |  |  |  |
|---|---|---|---|
| (Dollars in millions) | As Reported | Effect of change | Balance without adoption of ASC 606 |
| Sales to customers | $81,581 | (35) | 81,546 |
| Net earnings | 15,297 | (28) | 15,269 |
| Balance Sheet - As of December 30, 2018 |  |  |  |
|  | As Reported | Effect of change | Balance without adoption of ASC 606 |
| Assets | 152,954 | 23 | 152,977 |
| Liabilities | 93,202 | 4 | 93,206 |
| Equity | $59,752 | 19 | 59,771 |
````

</details>

RQ2 citation match (section level): `cited=[('JNJ', 'Item 6'), ('JNJ', 'Item 8')] gold=[(None, 'Item 8')]`

### System C v1 (adaptive multi-hop)

Model: `gpt-5.4`. Hops: 1. Chunks retrieved: 6, cited: 2.

**Generated answer**

> For fiscal year 2018, Johnson & Johnson reported net earnings of $15,297 million and sales to customers of $81,581 million, so net earnings as a percentage of sales to customers was 18.8%. [JNJ FY2018, Item 8, JNJ_FY2018_2018-12-30:209] [JNJ FY2018, Item 6, JNJ_FY2018_2018-12-30:99]

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `JNJ_FY2018_2018-12-30:413` | Item 8 › Restricted Share Units and Performance Share Units |  |  | \| \| 2018 \| \| \| \| 2017 \| \| \| \| \|---\|---\|---\|---\|---\|---\|---\|---\|---\| \| Net earnings (loss) \| 4,367 \| 3,954 \| 3,934 \| 3,042 \| 4,422 \| 3,827 \| 3,764 \| (10,713) \| \| Basic net earnings (loss) per share \| $1.63 \| 1.47 \| 1.47 \|… |
| 2 | `JNJ_FY2018_2018-12-30:209` | Item 8 › (Dollars and Shares in Millions Except Per Share Amounts) (Note 1) | ✓ | #2 | \| \| 2018 \| 2017 \| 2016 \| \|---\|---\|---\|---\| \| Sales to customers \| $81,581 \| 76,450 \| 71,890 \| \| Cost of products sold \| 27,091 \| 25,439 \| 21,789 \| \| Gross profit \| 54,490 \| 51,011 \| 50,101 \| \| Selling, marketing and admi… |
| 3 | `JNJ_FY2018_2018-12-30:99` | Item 6 › Summary of Operations and Statistical Data 2008-2018 | ✓ |  | \| (Dollars in Millions Except Per Share Amounts) \| 2018 \| 2017 \| 2016 \| 2015 \| 2014 \| 2013 \| 2012 \| 2011 \| 2010 \| 2009 \| 2008 \| \|---\|---\|---\|---\|---\|---\|---\|---\|---\|---\|---\|---\| \| Net earnings attributable to Johnson & J… |
| 4 | `JNJ_FY2018_2018-12-30:228` | Item 8 › Recently Adopted Accounting Standards |  | #1, #2 | \| Statement of Earnings - For the fiscal year ended December 30, 2018 \| \| \| \| \|---\|---\|---\|---\| \| (Dollars in millions) \| As Reported \| Effect of change \| Balance without adoption of ASC 606 \| \| Sales to customers \| $81,… |
| 5 | `JNJ_FY2018_2018-12-30:371` | Item 8 › Valuation Hierarchy |  |  | \| (In Millions Except Per Share Amounts) \| 2018 \| 2017 \| 2016 \| \|---\|---\|---\|---\| \| Basic net earnings per share \| $5.70 \| 0.48 \| 6.04 \| \| Average shares outstanding — basic \| 2,681.5 \| 2,692.0 \| 2,737.3 \| \| Potential sh… |
| 6 | `JNJ_FY2018_2018-12-30:370` | Item 8 › Valuation Hierarchy |  |  | Net currency transaction gains and losses included in Other (income) expense were losses of $265 million, $216 million and $289 million in 2018, 2017 and 2016, respectively. 15. Earnings Per Share The following is a reco… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#2 `JNJ_FY2018_2018-12-30:209`** (cited, gold #2)

````text
Item 8. FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA > (Dollars and Shares in Millions Except Per Share Amounts) (Note 1) (table)
|  | 2018 | 2017 | 2016 |
|---|---|---|---|
| Sales to customers | $81,581 | 76,450 | 71,890 |
| Cost of products sold | 27,091 | 25,439 | 21,789 |
| Gross profit | 54,490 | 51,011 | 50,101 |
| Selling, marketing and administrative expenses | 22,540 | 21,520 | 20,067 |
| Research and development expense | 10,775 | 10,594 | 9,143 |
| In-process research and development | 1,126 | 408 | 29 |
| Interest income | (611) | (385) | (368) |
| Interest expense, net of portion capitalized (Note 4) | 1,005 | 934 | 726 |
| Other (income) expense, net | 1,405 | (42) | 210 |
| Restructuring (Note 22) | 251 | 309 | 491 |
| Earnings before provision for taxes on income | 17,999 | 17,673 | 19,803 |
| Provision for taxes on income (Note 8) | 2,702 | 16,373 | 3,263 |
| Net earnings | $15,297 | 1,300 | 16,540 |
| Net earnings per share (Notes 1 and 15) |  |  |  |
| Basic | $5.70 | 0.48 | 6.04 |
| Diluted | $5.61 | 0.47 | 5.93 |
````

**#3 `JNJ_FY2018_2018-12-30:99`** (cited)

````text
Item 6. SELECTED FINANCIAL DATA > Summary of Operations and Statistical Data 2008-2018 (table)
| (Dollars in Millions Except Per Share Amounts) | 2018 | 2017 | 2016 | 2015 | 2014 | 2013 | 2012 | 2011 | 2010 | 2009 | 2008 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Net earnings attributable to Johnson & Johnson | 15,297 | 1,300 | 16,540 | 15,409 | 16,323 | 13,831 | 10,853 | 9,672 | 13,334 | 12,266 | 12,949 |
| Percent of sales to customers | 18.8% | 1.7 | 23.0 | 22.0 | 22.0 | 19.4 | 16.1 | 14.9 | 21.7 | 19.8 | 20.3 |
| Diluted net earnings per share of common stock (1) | $5.61 | 0.47 | 5.93 | 5.48 | 5.70 | 4.81 | 3.86 | 3.49 | 4.78 | 4.40 | 4.57 |
| Percent return on average shareholders’ equity | 25.5% | 2.0 | 23.4 | 21.9 | 22.7 | 19.9 | 17.8 | 17.0 | 24.9 | 26.4 | 30.2 |
| Percent increase (decrease) over previous year: |  |  |  |  |  |  |  |  |  |  |  |
````

**#4 `JNJ_FY2018_2018-12-30:228`** (gold #1, gold #2)

````text
Item 8. FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA > Recently Adopted Accounting Standards (table)
| Statement of Earnings - For the fiscal year ended December 30, 2018 |  |  |  |
|---|---|---|---|
| (Dollars in millions) | As Reported | Effect of change | Balance without adoption of ASC 606 |
| Sales to customers | $81,581 | (35) | 81,546 |
| Net earnings | 15,297 | (28) | 15,269 |
| Balance Sheet - As of December 30, 2018 |  |  |  |
|  | As Reported | Effect of change | Balance without adoption of ASC 606 |
| Assets | 152,954 | 23 | 152,977 |
| Liabilities | 93,202 | 4 | 93,206 |
| Equity | $59,752 | 19 | 59,771 |
````

</details>

RQ2 citation match (section level): `cited=[('JNJ', 'Item 8'), ('JNJ', 'Item 6')] gold=[(None, 'Item 8')]`

**System C guardrail** (judge `gpt-5.4`): numerical claims 3, verified 3, ungrounded 0, uncited 0, derived 0; sentence verdicts: supported 0, partial 0, unsupported 0, unchecked 0.


<details><summary>Guardrail sentence verdicts</summary>

| sentence | verdict | judge reason |
|---|---|---|
| For fiscal year 2018, Johnson & Johnson reported net earnings of $15,297 million and sales to customers of $81,581 million, so net earnings as a percentage of sales to customers was 18.8%. [JNJ FY2018, Item 8, JNJ_FY2018_2018-12-30:209] [JNJ FY2018, Item 6, JNJ_FY2018_2018-12-30:99] | None |  |

</details>

### System C v2 (agentic multi-hop + XBRL)

Model: `gpt-5.4`. Hops: 1. Chunks retrieved: 7, cited: 2.

**Generated answer**

> For fiscal year 2018, Johnson & Johnson reported net earnings of $15,297 million and sales to customers of $81,581 million, so net earnings as a percentage of sales to customers was 18.8%. [JNJ FY2018, Item 8, JNJ_FY2018_2018-12-30:209] [JNJ FY2018, Item 6, JNJ_FY2018_2018-12-30:99]

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `F-JNJ-2018` | SEC XBRL Reported Financials (financials.csv) |  |  | fiscal_year,fiscal_year_end,Revenue,NetIncome,OperatingIncome,TotalAssets,TotalLiabilities,StockholdersEquity,CashAndEquivalents,OperatingCashFlow,EPSDiluted 2018,2018-12-30,81581000000,15297000000,,152954000000,93202000… |
| 2 | `JNJ_FY2018_2018-12-30:413` | Item 8 › Restricted Share Units and Performance Share Units |  |  | \| \| 2018 \| \| \| \| 2017 \| \| \| \| \|---\|---\|---\|---\|---\|---\|---\|---\|---\| \| Net earnings (loss) \| 4,367 \| 3,954 \| 3,934 \| 3,042 \| 4,422 \| 3,827 \| 3,764 \| (10,713) \| \| Basic net earnings (loss) per share \| $1.63 \| 1.47 \| 1.47 \|… |
| 3 | `JNJ_FY2018_2018-12-30:209` | Item 8 › (Dollars and Shares in Millions Except Per Share Amounts) (Note 1) | ✓ | #2 | \| \| 2018 \| 2017 \| 2016 \| \|---\|---\|---\|---\| \| Sales to customers \| $81,581 \| 76,450 \| 71,890 \| \| Cost of products sold \| 27,091 \| 25,439 \| 21,789 \| \| Gross profit \| 54,490 \| 51,011 \| 50,101 \| \| Selling, marketing and admi… |
| 4 | `JNJ_FY2018_2018-12-30:99` | Item 6 › Summary of Operations and Statistical Data 2008-2018 | ✓ |  | \| (Dollars in Millions Except Per Share Amounts) \| 2018 \| 2017 \| 2016 \| 2015 \| 2014 \| 2013 \| 2012 \| 2011 \| 2010 \| 2009 \| 2008 \| \|---\|---\|---\|---\|---\|---\|---\|---\|---\|---\|---\|---\| \| Net earnings attributable to Johnson & J… |
| 5 | `JNJ_FY2018_2018-12-30:228` | Item 8 › Recently Adopted Accounting Standards |  | #1, #2 | \| Statement of Earnings - For the fiscal year ended December 30, 2018 \| \| \| \| \|---\|---\|---\|---\| \| (Dollars in millions) \| As Reported \| Effect of change \| Balance without adoption of ASC 606 \| \| Sales to customers \| $81,… |
| 6 | `JNJ_FY2018_2018-12-30:371` | Item 8 › Valuation Hierarchy |  |  | \| (In Millions Except Per Share Amounts) \| 2018 \| 2017 \| 2016 \| \|---\|---\|---\|---\| \| Basic net earnings per share \| $5.70 \| 0.48 \| 6.04 \| \| Average shares outstanding — basic \| 2,681.5 \| 2,692.0 \| 2,737.3 \| \| Potential sh… |
| 7 | `JNJ_FY2018_2018-12-30:370` | Item 8 › Valuation Hierarchy |  |  | Net currency transaction gains and losses included in Other (income) expense were losses of $265 million, $216 million and $289 million in 2018, 2017 and 2016, respectively. 15. Earnings Per Share The following is a reco… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#3 `JNJ_FY2018_2018-12-30:209`** (cited, gold #2)

````text
Item 8. FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA > (Dollars and Shares in Millions Except Per Share Amounts) (Note 1) (table)
|  | 2018 | 2017 | 2016 |
|---|---|---|---|
| Sales to customers | $81,581 | 76,450 | 71,890 |
| Cost of products sold | 27,091 | 25,439 | 21,789 |
| Gross profit | 54,490 | 51,011 | 50,101 |
| Selling, marketing and administrative expenses | 22,540 | 21,520 | 20,067 |
| Research and development expense | 10,775 | 10,594 | 9,143 |
| In-process research and development | 1,126 | 408 | 29 |
| Interest income | (611) | (385) | (368) |
| Interest expense, net of portion capitalized (Note 4) | 1,005 | 934 | 726 |
| Other (income) expense, net | 1,405 | (42) | 210 |
| Restructuring (Note 22) | 251 | 309 | 491 |
| Earnings before provision for taxes on income | 17,999 | 17,673 | 19,803 |
| Provision for taxes on income (Note 8) | 2,702 | 16,373 | 3,263 |
| Net earnings | $15,297 | 1,300 | 16,540 |
| Net earnings per share (Notes 1 and 15) |  |  |  |
| Basic | $5.70 | 0.48 | 6.04 |
| Diluted | $5.61 | 0.47 | 5.93 |
````

**#4 `JNJ_FY2018_2018-12-30:99`** (cited)

````text
Item 6. SELECTED FINANCIAL DATA > Summary of Operations and Statistical Data 2008-2018 (table)
| (Dollars in Millions Except Per Share Amounts) | 2018 | 2017 | 2016 | 2015 | 2014 | 2013 | 2012 | 2011 | 2010 | 2009 | 2008 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Net earnings attributable to Johnson & Johnson | 15,297 | 1,300 | 16,540 | 15,409 | 16,323 | 13,831 | 10,853 | 9,672 | 13,334 | 12,266 | 12,949 |
| Percent of sales to customers | 18.8% | 1.7 | 23.0 | 22.0 | 22.0 | 19.4 | 16.1 | 14.9 | 21.7 | 19.8 | 20.3 |
| Diluted net earnings per share of common stock (1) | $5.61 | 0.47 | 5.93 | 5.48 | 5.70 | 4.81 | 3.86 | 3.49 | 4.78 | 4.40 | 4.57 |
| Percent return on average shareholders’ equity | 25.5% | 2.0 | 23.4 | 21.9 | 22.7 | 19.9 | 17.8 | 17.0 | 24.9 | 26.4 | 30.2 |
| Percent increase (decrease) over previous year: |  |  |  |  |  |  |  |  |  |  |  |
````

**#5 `JNJ_FY2018_2018-12-30:228`** (gold #1, gold #2)

````text
Item 8. FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA > Recently Adopted Accounting Standards (table)
| Statement of Earnings - For the fiscal year ended December 30, 2018 |  |  |  |
|---|---|---|---|
| (Dollars in millions) | As Reported | Effect of change | Balance without adoption of ASC 606 |
| Sales to customers | $81,581 | (35) | 81,546 |
| Net earnings | 15,297 | (28) | 15,269 |
| Balance Sheet - As of December 30, 2018 |  |  |  |
|  | As Reported | Effect of change | Balance without adoption of ASC 606 |
| Assets | 152,954 | 23 | 152,977 |
| Liabilities | 93,202 | 4 | 93,206 |
| Equity | $59,752 | 19 | 59,771 |
````

</details>

RQ2 citation match (section level): `cited=[('JNJ', 'Item 8'), ('JNJ', 'Item 6')] gold=[(None, 'Item 8')]`

**System C guardrail** (judge `gpt-5.4`): numerical claims 3, verified 3, ungrounded 0, uncited 0, derived 0; sentence verdicts: supported 0, partial 0, unsupported 0, unchecked 0.


<details><summary>Guardrail sentence verdicts</summary>

| sentence | verdict | judge reason |
|---|---|---|
| For fiscal year 2018, Johnson & Johnson reported net earnings of $15,297 million and sales to customers of $81,581 million, so net earnings as a percentage of sales to customers was 18.8%. [JNJ FY2018, Item 8, JNJ_FY2018_2018-12-30:209] [JNJ FY2018, Item 6, JNJ_FY2018_2018-12-30:99] | None |  |

</details>
