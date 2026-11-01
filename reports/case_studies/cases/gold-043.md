# gold-043: Single-hop table

[← all cases](../README.md) · company: Alphabet Inc. (GOOGL) · fiscal year: 2020 · recipe `table` · hop `single` · answer type `numeric` · scope `single_doc` · RQ2 category `quantitative_tabular`

## Gold QA

**Question**

> By what percentage did Alphabet Inc.'s general and administrative expenses increase from fiscal year 2019 to fiscal year 2020?

**Gold answer**

> 15.72%

**Program**: `subtract(11052, 9551), divide(#0, 9551)` → `0.1571563187100827`

**Gold numbers** (RQ2 numeric_accuracy targets): 15.72%

**Gold evidence**

1. `GOOGL_FY2020_2020-12-31` · ITEM 7.MANAGEMENT’S DISCUSSION AND ANALYSIS OF FINANCIAL CONDITION AND RESULTS OF OPERATIONS › General and Administrative · table

   > | General and administrative expenses | $9,551 | $11,052 |

## Scorecard

| Metric | A (vanilla dense) | B (hybrid + rerank) | C v1 (adaptive multi-hop) | C v2 (agentic multi-hop + XBRL) |
|---|---|---|---|---|
| **Retrieval (RQ1)** | | | | |
| chunks retrieved | 10 | 5 | 6 | 7 |
| recall@5 | 1.00 | 1.00 | 1.00 | 1.00 |
| recall@all | 1.00 | 1.00 | 1.00 | 1.00 |
| complete@all | 1 | 1 | 1 | 1 |
| average precision (lexical) | 0.91 | 0.83 | 1.00 | 0.71 |
| gold evidence first rank | #1: 1 | #1: 1 | #1: 1 | #1: 2 |
| **Answer (RQ3 string match)** | | | | |
| numeric_correct | ✓ | ✓ | ✓ | ✓ |
| keypoint_recall | – | – | – | – |
| **Answer & citations (RQ2)** | | | | |
| numeric_accuracy | 1.00 | 1.00 | 1.00 | 1.00 |
| citation precision | 1.00 | 1.00 | 1.00 | 1.00 |
| citation recall | 1.00 | 1.00 | 1.00 | 1.00 |
| citation F1 | 1.00 | 1.00 | 1.00 | 1.00 |
| has a citation | 1 | 1 | 1 | 1 |
| grounding error rate | – | – | 0.00 | 0.00 |
| **Cost (RQ3)** | | | | |
| retrieval hops | 1 | 1 | 1 | 1 |
| tokens | 1890 | 1166 | 4345 | 4708 |
| cost (USD) | 0.0003 | 0.0002 | 0.0151 | 0.0157 |
| latency (s) | 2.2 | 6.9 | 5.7 | 6.5 |

Definitions: [README › Metrics](../README.md#metrics). `–` = not applicable (e.g. no gold number, no citations, no guardrail).

## System outputs

### System A (vanilla dense)

Model: `gpt-5.4-2026-03-05`. Hops: 1. Chunks retrieved: 10, cited: 2.

**Generated answer**

> Alphabet Inc.'s general and administrative expenses increased from **$9,551 million in 2019** to **$11,052 million in 2020** [1].
>
> Percentage increase = \(\frac{11,052 - 9,551}{9,551} \times 100\) = **about 15.7%** [1].
>
> This is also described as an increase of **$1,501 million** [2].

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `GOOGL_FY2020_2020-12-31:202` | Item 7 › General and Administrative | ✓ | #1 | \| \| Year Ended December 31, \| \| \|---\|---\|---\| \| \| 2019 \| 2020 \| \| General and administrative expenses \| $9,551 \| $11,052 \| \| General and administrative expenses as a percentage of revenues \| 5.9% \| 6.1% \| |
| 2 | `GOOGL_FY2020_2020-12-31:203` | Item 7 › General and Administrative | ✓ | #1 | General and administrative expenses consist primarily of: •Compensation expenses (including SBC) for employees in our finance, human resources, information technology, and legal organizations; •Depreciation; Table of Con… |
| 3 | `GOOGL_FY2020_2020-12-31:201` | Item 7 › General and Administrative |  | #1 | The following table presents our general and administrative expenses (in millions, except percentages): |
| 4 | `GOOGL_FY2020_2020-12-31:20` | NOTE ABOUT FORWARD-LOOKING STATEMENTS |  | #1 | •our expectation that our cost of revenues, research and development ("R&D") expenses, sales and marketing expenses, and general and administrative expenses may increase in amount and/or may increase as a percentage of r… |
| 5 | `GOOGL_FY2020_2020-12-31:0` | Washington, D.C. 20549 |  |  | ___________________________________________ |
| 6 | `GOOGL_FY2020_2020-12-31:164` | Item 7 › Executive Overview |  |  | \| \| Year Ended December 31, \| \| \|---\|---\|---\| \| \| 2019 \| 2020 \| \| Revenues \| $161,857 \| $182,527 \| \| Increase in revenues year over year \| 18% \| 13% \| \| Increase in constant currency revenues year over year \| 20% \| 14% \|… |
| 7 | `GOOGL_FY2020_2020-12-31:166` | Item 7 › Executive Overview |  |  | •Operating expenses were $56.6 billion, an increase of 5% year over year primarily driven by headcount growth and partially offset by declines in advertising and promotional expenses and travel and entertainment expenses… |
| 8 | `GOOGL_FY2020_2020-12-31:196` | Item 7 › Research and Development |  |  | \| \| Year Ended December 31, \| \| \|---\|---\|---\| \| \| 2019 \| 2020 \| \| Research and development expenses \| $26,018 \| $27,573 \| \| Research and development expenses as a percentage of revenues \| 16.1% \| 15.1% \| |
| 9 | `GOOGL_FY2020_2020-12-31:283` | Item 8 › (In millions, except per share amounts) |  | #1 | \| \| Year Ended December 31, \| \| \| \|---\|---\|---\|---\| \| \| 2018 \| 2019 \| 2020 \| \| Revenues \| $136,819 \| $161,857 \| $182,527 \| \| Costs and expenses: \| \| \| \| \| Cost of revenues \| 59,549 \| 71,896 \| 84,732 \| \| Research and deve… |
| 10 | `GOOGL_FY2020_2020-12-31:199` | Item 7 › Sales and Marketing |  |  | \| \| Year Ended December 31, \| \| \|---\|---\|---\| \| \| 2019 \| 2020 \| \| Sales and marketing expenses \| $18,464 \| $17,946 \| \| Sales and marketing expenses as a percentage of revenues \| 11.4% \| 9.8% \| |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#1 `GOOGL_FY2020_2020-12-31:202`** (cited, gold #1)

````text
ITEM 7.MANAGEMENT’S DISCUSSION AND ANALYSIS OF FINANCIAL CONDITION AND RESULTS OF OPERATIONS > General and Administrative (table)
|  | Year Ended December 31, |  |
|---|---|---|
|  | 2019 | 2020 |
| General and administrative expenses | $9,551 | $11,052 |
| General and administrative expenses as a percentage of revenues | 5.9% | 6.1% |
````

**#2 `GOOGL_FY2020_2020-12-31:203`** (cited, gold #1)

````text
ITEM 7.MANAGEMENT’S DISCUSSION AND ANALYSIS OF FINANCIAL CONDITION AND RESULTS OF OPERATIONS > General and Administrative
General and administrative expenses consist primarily of: •Compensation expenses (including SBC) for employees in our finance, human resources, information technology, and legal organizations; •Depreciation; Table of Contents Alphabet Inc. •Equipment-related expenses; •Legal-related expenses; and •Professional services fees primarily related to audit, information technology consulting, outside legal, and outsourcing services. General and administrative expenses increased $1,501 million from 2019 to 2020. The increase was primarily due to an increase in compensation expenses of $887 million, largely resulting from a 16% increase in headcount. In addition, there was an increase of $440 million related to allowance for credit losses for accounts receivable. The increase was partially offset by a $554 million charge recognized in 2019 relating to a legal settlement. Over time, general and administrative expenses as a percentage of revenues may fluctuate due to certain expenses that are generally less variable in nature and may not correlate to the changes in revenues, the effect of discrete items such as legal settlements, or allowances for credit losses for accounts receivable.
````

**#3 `GOOGL_FY2020_2020-12-31:201`** (gold #1)

````text
ITEM 7.MANAGEMENT’S DISCUSSION AND ANALYSIS OF FINANCIAL CONDITION AND RESULTS OF OPERATIONS > General and Administrative
The following table presents our general and administrative expenses (in millions, except percentages):
````

**#4 `GOOGL_FY2020_2020-12-31:20`** (gold #1)

````text
NOTE ABOUT FORWARD-LOOKING STATEMENTS
•our expectation that our cost of revenues, research and development ("R&D") expenses, sales and marketing expenses, and general and administrative expenses may increase in amount and/or may increase as a percentage of revenues and may be affected by a number of factors; •estimates of our future compensation expenses; •our expectation that our other income (expense), net ("OI&E"), will fluctuate in the future, as it is largely driven by market dynamics; •fluctuations in our effective tax rate; •seasonal fluctuations in internet usage and advertiser expenditures, underlying business trends such as traditional retail seasonality (including developments and volatility arising from COVID-19), which are likely to cause fluctuations in our quarterly results; •the sufficiency of our sources of funding; •our potential exposure in connection with new and pending investigations, proceedings, and other contingencies; Table of Contents Alphabet Inc. •the sufficiency and timing of our proposed remedies in response to decisions from the European Commission ("EC") and other regulators and governmental entities; •our expectations regarding the timing, design and implementation of our new global enterprise resource planning ("ERP") system; •the expected timing and amount of Alphabet Inc.'s share repurchases; •our long-term sustainability and diversity goals;
````

**#9 `GOOGL_FY2020_2020-12-31:283`** (gold #1)

````text
ITEM 8.FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA > (In millions, except per share amounts) (table)
|  | Year Ended December 31, |  |  |
|---|---|---|---|
|  | 2018 | 2019 | 2020 |
| Revenues | $136,819 | $161,857 | $182,527 |
| Costs and expenses: |  |  |  |
| Cost of revenues | 59,549 | 71,896 | 84,732 |
| Research and development | 21,419 | 26,018 | 27,573 |
| Sales and marketing | 16,333 | 18,464 | 17,946 |
| General and administrative | 6,923 | 9,551 | 11,052 |
| European Commission fines | 5,071 | 1,697 | 0 |
| Total costs and expenses | 109,295 | 127,626 | 141,303 |
| Income from operations | 27,524 | 34,231 | 41,224 |
| Other income (expense), net | 7,389 | 5,394 | 6,858 |
| Income before income taxes | 34,913 | 39,625 | 48,082 |
| Provision for income taxes | 4,177 | 5,282 | 7,813 |
| Net income | $30,736 | $34,343 | $40,269 |
| Basic net income per share of Class A and B common stock and Class C capital stock | $44.22 | $49.59 | $59.15 |
````

</details>

RQ2 citation match (section level): `cited=[('GOOGL', 'Item 7')] gold=[(None, 'Item 7')]`

### System B (hybrid + rerank)

Model: `gpt-5.4-2026-03-05`. Hops: 1. Chunks retrieved: 5, cited: 2.

**Generated answer**

> Alphabet Inc.'s general and administrative expenses increased from $9,551 million in 2019 to $11,052 million in 2020, an increase of $1,501 million. That is an increase of about **15.7%** (($1,501 ÷ $9,551) × 100). [1][3]

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `GOOGL_FY2020_2020-12-31:203` | Item 7 › General and Administrative | ✓ | #1 | General and administrative expenses consist primarily of: •Compensation expenses (including SBC) for employees in our finance, human resources, information technology, and legal organizations; •Depreciation; Table of Con… |
| 2 | `GOOGL_FY2020_2020-12-31:165` | Item 7 › Executive Overview |  |  | (1) Results for 2019 include the effect of the $1.7 billion EC fine. See Note 10 of the Notes to Consolidated Financial Statements included in Part II, Item 8 of this Annual Report on Form 10-K for further information. •… |
| 3 | `GOOGL_FY2020_2020-12-31:202` | Item 7 › General and Administrative | ✓ | #1 | \| \| Year Ended December 31, \| \| \|---\|---\|---\| \| \| 2019 \| 2020 \| \| General and administrative expenses \| $9,551 \| $11,052 \| \| General and administrative expenses as a percentage of revenues \| 5.9% \| 6.1% \| |
| 4 | `GOOGL_FY2020_2020-12-31:210` | Item 7 › Other Bets |  |  | Other Bets operating loss decreased $348 million from 2019 to 2020 and increased $1,466 million from 2018 to 2019. The fluctuations were primarily driven by compensation expenses (including SBC). Table of Contents Alphab… |
| 5 | `GOOGL_FY2020_2020-12-31:189` | Item 7 › Use of Constant Currency Revenues and Constant Currency Revenue Percentage Change |  |  | (1) Total revenues and hedging gains (losses) for the year ended December 31, 2018 were $136,819 million and $(138) million, respectively. EMEA revenue percentage change from 2019 to 2020 was not significantly affected b… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#1 `GOOGL_FY2020_2020-12-31:203`** (cited, gold #1)

````text
ITEM 7.MANAGEMENT’S DISCUSSION AND ANALYSIS OF FINANCIAL CONDITION AND RESULTS OF OPERATIONS > General and Administrative
General and administrative expenses consist primarily of: •Compensation expenses (including SBC) for employees in our finance, human resources, information technology, and legal organizations; •Depreciation; Table of Contents Alphabet Inc. •Equipment-related expenses; •Legal-related expenses; and •Professional services fees primarily related to audit, information technology consulting, outside legal, and outsourcing services. General and administrative expenses increased $1,501 million from 2019 to 2020. The increase was primarily due to an increase in compensation expenses of $887 million, largely resulting from a 16% increase in headcount. In addition, there was an increase of $440 million related to allowance for credit losses for accounts receivable. The increase was partially offset by a $554 million charge recognized in 2019 relating to a legal settlement. Over time, general and administrative expenses as a percentage of revenues may fluctuate due to certain expenses that are generally less variable in nature and may not correlate to the changes in revenues, the effect of discrete items such as legal settlements, or allowances for credit losses for accounts receivable.
````

**#3 `GOOGL_FY2020_2020-12-31:202`** (cited, gold #1)

````text
ITEM 7.MANAGEMENT’S DISCUSSION AND ANALYSIS OF FINANCIAL CONDITION AND RESULTS OF OPERATIONS > General and Administrative (table)
|  | Year Ended December 31, |  |
|---|---|---|
|  | 2019 | 2020 |
| General and administrative expenses | $9,551 | $11,052 |
| General and administrative expenses as a percentage of revenues | 5.9% | 6.1% |
````

</details>

RQ2 citation match (section level): `cited=[('GOOGL', 'Item 7')] gold=[(None, 'Item 7')]`

### System C v1 (adaptive multi-hop)

Model: `gpt-5.4`. Hops: 1. Chunks retrieved: 6, cited: 2.

**Generated answer**

> Alphabet Inc.'s general and administrative expenses increased from $9,551 million in 2019 to $11,052 million in 2020, an increase of $1,501 million, which equals approximately 15.7% (($1,501 ÷ $9,551) × 100). [GOOGL FY2020, Item 7, GOOGL_FY2020_2020-12-31:202] [GOOGL FY2020, Item 7, GOOGL_FY2020_2020-12-31:203]

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `GOOGL_FY2020_2020-12-31:201` | Item 7 › General and Administrative |  | #1 | The following table presents our general and administrative expenses (in millions, except percentages): |
| 2 | `GOOGL_FY2020_2020-12-31:203` | Item 7 › General and Administrative | ✓ | #1 | General and administrative expenses consist primarily of: •Compensation expenses (including SBC) for employees in our finance, human resources, information technology, and legal organizations; •Depreciation; Table of Con… |
| 3 | `GOOGL_FY2020_2020-12-31:202` | Item 7 › General and Administrative | ✓ | #1 | \| \| Year Ended December 31, \| \| \|---\|---\|---\| \| \| 2019 \| 2020 \| \| General and administrative expenses \| $9,551 \| $11,052 \| \| General and administrative expenses as a percentage of revenues \| 5.9% \| 6.1% \| |
| 4 | `GOOGL_FY2020_2020-12-31:20` | NOTE ABOUT FORWARD-LOOKING STATEMENTS |  | #1 | •our expectation that our cost of revenues, research and development ("R&D") expenses, sales and marketing expenses, and general and administrative expenses may increase in amount and/or may increase as a percentage of r… |
| 5 | `GOOGL_FY2020_2020-12-31:219` | Item 7 › Quarterly Results of Operations |  | #1 | \| \| Quarter Ended \| \| \| \| \| \| \| \| \|---\|---\|---\|---\|---\|---\|---\|---\|---\| \| \| Mar 31, 2019 \| Jun 30, 2019 \| Sept 30, 2019 \| Dec 31, 2019 \| Mar 31, 2020 \| Jun 30, 2020 \| Sept 30, 2020 \| Dec 31, 2020 \| \| \| (In millions, exce… |
| 6 | `GOOGL_FY2020_2020-12-31:197` | Item 7 › Research and Development |  |  | R&D expenses consist primarily of: •Compensation expenses (including SBC) for engineering and technical employees responsible for R&D of our existing and new products and services; •Depreciation expenses; •Equipment-rela… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#1 `GOOGL_FY2020_2020-12-31:201`** (gold #1)

````text
ITEM 7.MANAGEMENT’S DISCUSSION AND ANALYSIS OF FINANCIAL CONDITION AND RESULTS OF OPERATIONS > General and Administrative
The following table presents our general and administrative expenses (in millions, except percentages):
````

**#2 `GOOGL_FY2020_2020-12-31:203`** (cited, gold #1)

````text
ITEM 7.MANAGEMENT’S DISCUSSION AND ANALYSIS OF FINANCIAL CONDITION AND RESULTS OF OPERATIONS > General and Administrative
General and administrative expenses consist primarily of: •Compensation expenses (including SBC) for employees in our finance, human resources, information technology, and legal organizations; •Depreciation; Table of Contents Alphabet Inc. •Equipment-related expenses; •Legal-related expenses; and •Professional services fees primarily related to audit, information technology consulting, outside legal, and outsourcing services. General and administrative expenses increased $1,501 million from 2019 to 2020. The increase was primarily due to an increase in compensation expenses of $887 million, largely resulting from a 16% increase in headcount. In addition, there was an increase of $440 million related to allowance for credit losses for accounts receivable. The increase was partially offset by a $554 million charge recognized in 2019 relating to a legal settlement. Over time, general and administrative expenses as a percentage of revenues may fluctuate due to certain expenses that are generally less variable in nature and may not correlate to the changes in revenues, the effect of discrete items such as legal settlements, or allowances for credit losses for accounts receivable.
````

**#3 `GOOGL_FY2020_2020-12-31:202`** (cited, gold #1)

````text
ITEM 7.MANAGEMENT’S DISCUSSION AND ANALYSIS OF FINANCIAL CONDITION AND RESULTS OF OPERATIONS > General and Administrative (table)
|  | Year Ended December 31, |  |
|---|---|---|
|  | 2019 | 2020 |
| General and administrative expenses | $9,551 | $11,052 |
| General and administrative expenses as a percentage of revenues | 5.9% | 6.1% |
````

**#4 `GOOGL_FY2020_2020-12-31:20`** (gold #1)

````text
NOTE ABOUT FORWARD-LOOKING STATEMENTS
•our expectation that our cost of revenues, research and development ("R&D") expenses, sales and marketing expenses, and general and administrative expenses may increase in amount and/or may increase as a percentage of revenues and may be affected by a number of factors; •estimates of our future compensation expenses; •our expectation that our other income (expense), net ("OI&E"), will fluctuate in the future, as it is largely driven by market dynamics; •fluctuations in our effective tax rate; •seasonal fluctuations in internet usage and advertiser expenditures, underlying business trends such as traditional retail seasonality (including developments and volatility arising from COVID-19), which are likely to cause fluctuations in our quarterly results; •the sufficiency of our sources of funding; •our potential exposure in connection with new and pending investigations, proceedings, and other contingencies; Table of Contents Alphabet Inc. •the sufficiency and timing of our proposed remedies in response to decisions from the European Commission ("EC") and other regulators and governmental entities; •our expectations regarding the timing, design and implementation of our new global enterprise resource planning ("ERP") system; •the expected timing and amount of Alphabet Inc.'s share repurchases; •our long-term sustainability and diversity goals;
````

**#5 `GOOGL_FY2020_2020-12-31:219`** (gold #1)

````text
ITEM 7.MANAGEMENT’S DISCUSSION AND ANALYSIS OF FINANCIAL CONDITION AND RESULTS OF OPERATIONS > Quarterly Results of Operations (table)
|  | Quarter Ended |  |  |  |  |  |  |  |
|---|---|---|---|---|---|---|---|---|
|  | Mar 31, 2019 | Jun 30, 2019 | Sept 30, 2019 | Dec 31, 2019 | Mar 31, 2020 | Jun 30, 2020 | Sept 30, 2020 | Dec 31, 2020 |
|  | (In millions, except per share amounts) (unaudited) |  |  |  |  |  |  |  |
| Consolidated Statements of Income Data: |  |  |  |  |  |  |  |  |
| Revenues | $36,339 | $38,944 | $40,499 | $46,075 | $41,159 | $38,297 | $46,173 | 56,898 |
| Costs and expenses: |  |  |  |  |  |  |  |  |
| Cost of revenues | 16,012 | 17,296 | 17,568 | 21,020 | 18,982 | 18,553 | 21,117 | 26,080 |
| Research and development | 6,029 | 6,213 | 6,554 | 7,222 | 6,820 | 6,875 | 6,856 | 7,022 |
| Sales and marketing | 3,905 | 4,212 | 4,609 | 5,738 | 4,500 | 3,901 | 4,231 | 5,314 |
| General and administrative | 2,088 | 2,043 | 2,591 | 2,829 | 2,880 | 2,585 | 2,756 | 2,831 |
````

</details>

RQ2 citation match (section level): `cited=[('GOOGL', 'Item 7')] gold=[(None, 'Item 7')]`

**System C guardrail** (judge `gpt-5.4`): numerical claims 6, verified 6, ungrounded 0, uncited 0, derived 2; sentence verdicts: supported 0, partial 0, unsupported 0, unchecked 0.


<details><summary>Guardrail sentence verdicts</summary>

| sentence | verdict | judge reason |
|---|---|---|
| Alphabet Inc.'s general and administrative expenses increased from $9,551 million in 2019 to $11,052 million in 2020, an increase of $1,501 million, which equals approximately 15.7% (($1,501 ÷ $9,551) × 100). [GOOGL FY2020, Item 7, GOOGL_FY2020_2020-12-31:202] [GOOGL FY2020, Item 7, GOOGL_FY2020_2020-12-31:203] | None |  |

</details>

### System C v2 (agentic multi-hop + XBRL)

Model: `gpt-5.4`. Hops: 1. Chunks retrieved: 7, cited: 1.

**Generated answer**

> Alphabet Inc.'s general and administrative expenses increased from $9,551 million in 2019 to $11,052 million in 2020, an increase of approximately 15.7% [GOOGL FY2020, Item 7, GOOGL_FY2020_2020-12-31:202].

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `F-GOOGL-2020` | SEC XBRL Reported Financials (financials.csv) |  |  | fiscal_year,fiscal_year_end,Revenue,NetIncome,OperatingIncome,TotalAssets,TotalLiabilities,StockholdersEquity,CashAndEquivalents,OperatingCashFlow,EPSDiluted 2020,2020-12-31,182527000000,40269000000,41224000000,319616000… |
| 2 | `GOOGL_FY2020_2020-12-31:201` | Item 7 › General and Administrative |  | #1 | The following table presents our general and administrative expenses (in millions, except percentages): |
| 3 | `GOOGL_FY2020_2020-12-31:203` | Item 7 › General and Administrative |  | #1 | General and administrative expenses consist primarily of: •Compensation expenses (including SBC) for employees in our finance, human resources, information technology, and legal organizations; •Depreciation; Table of Con… |
| 4 | `GOOGL_FY2020_2020-12-31:202` | Item 7 › General and Administrative | ✓ | #1 | \| \| Year Ended December 31, \| \| \|---\|---\|---\| \| \| 2019 \| 2020 \| \| General and administrative expenses \| $9,551 \| $11,052 \| \| General and administrative expenses as a percentage of revenues \| 5.9% \| 6.1% \| |
| 5 | `GOOGL_FY2020_2020-12-31:20` | NOTE ABOUT FORWARD-LOOKING STATEMENTS |  | #1 | •our expectation that our cost of revenues, research and development ("R&D") expenses, sales and marketing expenses, and general and administrative expenses may increase in amount and/or may increase as a percentage of r… |
| 6 | `GOOGL_FY2020_2020-12-31:219` | Item 7 › Quarterly Results of Operations |  | #1 | \| \| Quarter Ended \| \| \| \| \| \| \| \| \|---\|---\|---\|---\|---\|---\|---\|---\|---\| \| \| Mar 31, 2019 \| Jun 30, 2019 \| Sept 30, 2019 \| Dec 31, 2019 \| Mar 31, 2020 \| Jun 30, 2020 \| Sept 30, 2020 \| Dec 31, 2020 \| \| \| (In millions, exce… |
| 7 | `GOOGL_FY2020_2020-12-31:197` | Item 7 › Research and Development |  |  | R&D expenses consist primarily of: •Compensation expenses (including SBC) for engineering and technical employees responsible for R&D of our existing and new products and services; •Depreciation expenses; •Equipment-rela… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#2 `GOOGL_FY2020_2020-12-31:201`** (gold #1)

````text
ITEM 7.MANAGEMENT’S DISCUSSION AND ANALYSIS OF FINANCIAL CONDITION AND RESULTS OF OPERATIONS > General and Administrative
The following table presents our general and administrative expenses (in millions, except percentages):
````

**#3 `GOOGL_FY2020_2020-12-31:203`** (gold #1)

````text
ITEM 7.MANAGEMENT’S DISCUSSION AND ANALYSIS OF FINANCIAL CONDITION AND RESULTS OF OPERATIONS > General and Administrative
General and administrative expenses consist primarily of: •Compensation expenses (including SBC) for employees in our finance, human resources, information technology, and legal organizations; •Depreciation; Table of Contents Alphabet Inc. •Equipment-related expenses; •Legal-related expenses; and •Professional services fees primarily related to audit, information technology consulting, outside legal, and outsourcing services. General and administrative expenses increased $1,501 million from 2019 to 2020. The increase was primarily due to an increase in compensation expenses of $887 million, largely resulting from a 16% increase in headcount. In addition, there was an increase of $440 million related to allowance for credit losses for accounts receivable. The increase was partially offset by a $554 million charge recognized in 2019 relating to a legal settlement. Over time, general and administrative expenses as a percentage of revenues may fluctuate due to certain expenses that are generally less variable in nature and may not correlate to the changes in revenues, the effect of discrete items such as legal settlements, or allowances for credit losses for accounts receivable.
````

**#4 `GOOGL_FY2020_2020-12-31:202`** (cited, gold #1)

````text
ITEM 7.MANAGEMENT’S DISCUSSION AND ANALYSIS OF FINANCIAL CONDITION AND RESULTS OF OPERATIONS > General and Administrative (table)
|  | Year Ended December 31, |  |
|---|---|---|
|  | 2019 | 2020 |
| General and administrative expenses | $9,551 | $11,052 |
| General and administrative expenses as a percentage of revenues | 5.9% | 6.1% |
````

**#5 `GOOGL_FY2020_2020-12-31:20`** (gold #1)

````text
NOTE ABOUT FORWARD-LOOKING STATEMENTS
•our expectation that our cost of revenues, research and development ("R&D") expenses, sales and marketing expenses, and general and administrative expenses may increase in amount and/or may increase as a percentage of revenues and may be affected by a number of factors; •estimates of our future compensation expenses; •our expectation that our other income (expense), net ("OI&E"), will fluctuate in the future, as it is largely driven by market dynamics; •fluctuations in our effective tax rate; •seasonal fluctuations in internet usage and advertiser expenditures, underlying business trends such as traditional retail seasonality (including developments and volatility arising from COVID-19), which are likely to cause fluctuations in our quarterly results; •the sufficiency of our sources of funding; •our potential exposure in connection with new and pending investigations, proceedings, and other contingencies; Table of Contents Alphabet Inc. •the sufficiency and timing of our proposed remedies in response to decisions from the European Commission ("EC") and other regulators and governmental entities; •our expectations regarding the timing, design and implementation of our new global enterprise resource planning ("ERP") system; •the expected timing and amount of Alphabet Inc.'s share repurchases; •our long-term sustainability and diversity goals;
````

**#6 `GOOGL_FY2020_2020-12-31:219`** (gold #1)

````text
ITEM 7.MANAGEMENT’S DISCUSSION AND ANALYSIS OF FINANCIAL CONDITION AND RESULTS OF OPERATIONS > Quarterly Results of Operations (table)
|  | Quarter Ended |  |  |  |  |  |  |  |
|---|---|---|---|---|---|---|---|---|
|  | Mar 31, 2019 | Jun 30, 2019 | Sept 30, 2019 | Dec 31, 2019 | Mar 31, 2020 | Jun 30, 2020 | Sept 30, 2020 | Dec 31, 2020 |
|  | (In millions, except per share amounts) (unaudited) |  |  |  |  |  |  |  |
| Consolidated Statements of Income Data: |  |  |  |  |  |  |  |  |
| Revenues | $36,339 | $38,944 | $40,499 | $46,075 | $41,159 | $38,297 | $46,173 | 56,898 |
| Costs and expenses: |  |  |  |  |  |  |  |  |
| Cost of revenues | 16,012 | 17,296 | 17,568 | 21,020 | 18,982 | 18,553 | 21,117 | 26,080 |
| Research and development | 6,029 | 6,213 | 6,554 | 7,222 | 6,820 | 6,875 | 6,856 | 7,022 |
| Sales and marketing | 3,905 | 4,212 | 4,609 | 5,738 | 4,500 | 3,901 | 4,231 | 5,314 |
| General and administrative | 2,088 | 2,043 | 2,591 | 2,829 | 2,880 | 2,585 | 2,756 | 2,831 |
````

</details>

RQ2 citation match (section level): `cited=[('GOOGL', 'Item 7')] gold=[(None, 'Item 7')]`

**System C guardrail** (judge `gpt-5.4`): numerical claims 3, verified 3, ungrounded 0, uncited 0, derived 1; sentence verdicts: supported 0, partial 0, unsupported 0, unchecked 0.


<details><summary>Guardrail sentence verdicts</summary>

| sentence | verdict | judge reason |
|---|---|---|
| Alphabet Inc.'s general and administrative expenses increased from $9,551 million in 2019 to $11,052 million in 2020, an increase of approximately 15.7% [GOOGL FY2020, Item 7, GOOGL_FY2020_2020-12-31:202]. | None |  |

</details>
