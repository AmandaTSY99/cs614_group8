# gold-038: Table + text (one filing)

[← all cases](../README.md) · company: MICROSOFT CORP (MSFT) · fiscal year: 2018 · recipe `table_text` · hop `multi` · answer type `mixed` · scope `single_doc` · RQ2 category `cross_section_multihop`

## Gold QA

**Question**

> By how many millions of dollars did Microsoft's sales and marketing expenses increase in fiscal year 2018 compared to fiscal year 2017, and what does the company state about the nature of its ongoing investments in products and services during this period?

**Gold answer**

> $2,008 million; The company states that it makes significant investments in new products and services that may not achieve expected returns, and that investments in new technology are speculative.

**Program**: `subtract(17469, 15461)` → `2008.0`

**Gold numbers** (RQ2 numeric_accuracy targets): $2,008 million

**Key points** (RQ3 keypoint_recall targets)

1. The increase in sales and marketing expenses was $2,008 million.
2. The company makes significant investments in new products and services.
3. These investments may not achieve expected returns.
4. Investments in new technology are described as speculative.

**Gold evidence**

1. `MSFT_FY2018_2018-06-30` · Item 7 › Sales and Marketing · table

   > | Sales and marketing | $17,469 | $15,461 | $14,635 | 13% | 6% |

2. `MSFT_FY2018_2018-06-30` · Item 1A › PART I · text

   > We make significant investments in new products and services that may not achieve expected returns.

3. `MSFT_FY2018_2018-06-30` · Item 1A › PART I · text

   > Investments in new technology are speculative.

## Scorecard

| Metric | A (vanilla dense) | B (hybrid + rerank) | C v1 (adaptive multi-hop) | C v2 (agentic multi-hop + XBRL) |
|---|---|---|---|---|
| **Retrieval (RQ1)** | | | | |
| chunks retrieved | 10 | 5 | 6 | 7 |
| recall@5 | 0.00 | 0.00 | 0.00 | 0.00 |
| recall@all | 0.33 | 0.00 | 0.00 | 0.00 |
| complete@all | 0 | 0 | 0 | 0 |
| average precision (lexical) | 0.12 | 0.00 | 0.00 | 0.00 |
| gold evidence first rank | #1: 8, #2: –, #3: – | #1: –, #2: –, #3: – | #1: –, #2: –, #3: – | #1: –, #2: –, #3: – |
| **Answer (RQ3 string match)** | | | | |
| numeric_correct | ✓ | ✓ | ✓ | ✓ |
| keypoint_recall | 0.50 | 0.25 | 0.25 | 0.25 |
| **Answer & citations (RQ2)** | | | | |
| numeric_accuracy | 1.00 | 1.00 | 1.00 | 1.00 |
| citation precision | 1.00 | 1.00 | 0.50 | 0.50 |
| citation recall | 0.50 | 0.50 | 0.50 | 0.50 |
| citation F1 | 0.67 | 0.67 | 0.50 | 0.50 |
| has a citation | 1 | 1 | 1 | 1 |
| grounding error rate | – | – | 0.00 | 0.00 |
| **Cost (RQ3)** | | | | |
| retrieval hops | 1 | 1 | 1 | 1 |
| tokens | 1821 | 1153 | 4645 | 4713 |
| cost (USD) | 0.0003 | 0.0002 | 0.0184 | 0.0195 |
| latency (s) | 2.3 | 6.3 | 10.3 | 11.0 |

Definitions: [README › Metrics](../README.md#metrics). `–` = not applicable (e.g. no gold number, no citations, no guardrail).

## System outputs

### System A (vanilla dense)

Model: `gpt-5.4-2026-03-05`. Hops: 1. Chunks retrieved: 10, cited: 4.

**Generated answer**

> Microsoft’s sales and marketing expenses increased by **$2.0 billion**, or **$2,008 million**, in fiscal year 2018 compared with fiscal year 2017 [1][8].
>
> As to the “nature of its ongoing investments in products and services,” the provided context only states that the increase was driven primarily by **LinkedIn expenses** and **investments in commercial sales capacity**, with R&D also increasing due to **investments in cloud engineering** [1][3][4]. It does **not** provide a broader statement specifically describing the nature of the company’s ongoing investments in products and services beyond those points.

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `MSFT_FY2018_2018-06-30:195` | Item 7 › Fiscal Year 2018 Compared with Fiscal Year 2017 | ✓ |  | Sales and marketing expenses increased $2.0 billion or 13%, primarily due to LinkedIn expenses and investments in commercial sales capacity, offset in part by a decrease in Windows marketing expenses. LinkedIn expenses i… |
| 2 | `MSFT_FY2018_2018-06-30:196` | Item 7 › Fiscal Year 2017 Compared with Fiscal Year 2016 |  |  | Sales and marketing expenses increased $826 million or 6%, primarily due to LinkedIn expenses and increased investments in sales capacity for our commercial cloud, offset in part by a reduction in Phone expenses and prio… |
| 3 | `MSFT_FY2018_2018-06-30:171` | Item 7 › Fiscal Year 2018 Compared with Fiscal Year 2017 | ✓ |  | • Sales and marketing expenses increased $2.0 billion or 13%, primarily due to LinkedIn expenses and investments in commercial sales capacity, offset in part by a decrease in Windows marketing expenses. • Research and de… |
| 4 | `MSFT_FY2018_2018-06-30:191` | Item 7 › Fiscal Year 2018 Compared with Fiscal Year 2017 | ✓ |  | Research and development expenses increased $1.7 billion or 13%, primarily due to investments in cloud engineering and LinkedIn expenses. LinkedIn expenses increased $762 million to $1.5 billion. |
| 5 | `MSFT_FY2018_2018-06-30:159` | Item 7 |  |  | Highlights from fiscal year 2018 compared with fiscal year 2017 included: • Commercial cloud revenue, which primarily comprises Microsoft Office 365 commercial, Microsoft Azure, Microsoft Dynamics 365, and other cloud pr… |
| 6 | `MSFT_FY2018_2018-06-30:177` | Item 7 › Fiscal Year 2018 Compared with Fiscal Year 2017 |  |  | Productivity and Business Processes Revenue increased $6.0 billion or 20%. • LinkedIn revenue increased $3.0 billion to $5.3 billion. Fiscal year 2018 includes a full period of results, whereas fiscal year 2017 only incl… |
| 7 | `MSFT_FY2018_2018-06-30:199` | Item 7 › Fiscal Year 2018 Compared with Fiscal Year 2017 |  |  | General and administrative expenses increased $273 million or 6%, primarily due to LinkedIn expenses. LinkedIn expenses increased $234 million to $528 million. |
| 8 | `MSFT_FY2018_2018-06-30:193` | Item 7 › Sales and Marketing | ✓ | #1 | \| (In millions, except percentages) \| 2018 \| 2017 \| 2016 \| Percentage Change 2018 Versus 2017 \| Percentage Change 2017 Versus 2016 \| \|---\|---\|---\|---\|---\|---\| \| Sales and marketing \| $17,469 \| $15,461 \| $14,635 \| 13% \| 6… |
| 9 | `MSFT_FY2018_2018-06-30:192` | Item 7 › Fiscal Year 2017 Compared with Fiscal Year 2016 |  |  | Research and development expenses increased $1.0 billion or 9%, primarily due to LinkedIn expenses and increased investments in cloud engineering, offset in part by a reduction in Phone expenses. Expenses included $745 m… |
| 10 | `MSFT_FY2018_2018-06-30:170` | Item 7 › Fiscal Year 2018 Compared with Fiscal Year 2017 |  |  | Revenue increased $13.8 billion or 14%, driven by growth across each of our segments. Productivity and Business Processes revenue increased, driven by LinkedIn and higher revenue from Office. Intelligent Cloud revenue in… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#1 `MSFT_FY2018_2018-06-30:195`** (cited)

````text
Item 7 > Fiscal Year 2018 Compared with Fiscal Year 2017
Sales and marketing expenses increased $2.0 billion or 13%, primarily due to LinkedIn expenses and investments in commercial sales capacity, offset in part by a decrease in Windows marketing expenses. LinkedIn expenses increased $1.2 billion to $2.5 billion, including $617 million of amortization of acquired intangible assets.
````

**#3 `MSFT_FY2018_2018-06-30:171`** (cited)

````text
Item 7 > Fiscal Year 2018 Compared with Fiscal Year 2017
• Sales and marketing expenses increased $2.0 billion or 13%, primarily due to LinkedIn expenses and investments in commercial sales capacity, offset in part by a decrease in Windows marketing expenses. • Research and development expenses increased $1.7 billion or 13%, primarily due to investments in cloud engineering and LinkedIn expenses. • General and administrative expenses increased $273 million or 6%, primarily due to LinkedIn expenses. Current year net income and diluted EPS were negatively impacted by the net charge related to TCJA, which resulted in a decrease to net income and diluted earnings per share of $13.7 billion and $1.75, respectively. Prior year diluted EPS was negatively impacted by restructuring expenses, which resulted in a decrease in operating income, net income, and diluted EPS of $306 million, $243 million, and $0.04, respectively.
````

**#4 `MSFT_FY2018_2018-06-30:191`** (cited)

````text
Item 7 > Fiscal Year 2018 Compared with Fiscal Year 2017
Research and development expenses increased $1.7 billion or 13%, primarily due to investments in cloud engineering and LinkedIn expenses. LinkedIn expenses increased $762 million to $1.5 billion.
````

**#8 `MSFT_FY2018_2018-06-30:193`** (cited, gold #1)

````text
Item 7 > Sales and Marketing (table)
| (In millions, except percentages) | 2018 | 2017 | 2016 | Percentage Change 2018 Versus 2017 | Percentage Change 2017 Versus 2016 |
|---|---|---|---|---|---|
| Sales and marketing | $17,469 | $15,461 | $14,635 | 13% | 6% |
| As a percent of revenue | 16% | 16% | 16% | 0ppt | 0ppt |
````

</details>

RQ2 citation match (section level): `cited=[('MSFT', 'Item 7')] gold=[(None, 'Item 7'), (None, 'Item 1A')]`

### System B (hybrid + rerank)

Model: `gpt-5.4-2026-03-05`. Hops: 1. Chunks retrieved: 5, cited: 2.

**Generated answer**

> Microsoft’s sales and marketing expenses increased by **$2.0 billion**, or **$2,000 million**, in fiscal year 2018 compared with fiscal year 2017 [1][2].
>
> During this period, Microsoft said the increase was driven primarily by **LinkedIn expenses and investments in commercial sales capacity**, indicating ongoing investment in its offerings and go-to-market capabilities [1][2].

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `MSFT_FY2018_2018-06-30:171` | Item 7 › Fiscal Year 2018 Compared with Fiscal Year 2017 | ✓ |  | • Sales and marketing expenses increased $2.0 billion or 13%, primarily due to LinkedIn expenses and investments in commercial sales capacity, offset in part by a decrease in Windows marketing expenses. • Research and de… |
| 2 | `MSFT_FY2018_2018-06-30:195` | Item 7 › Fiscal Year 2018 Compared with Fiscal Year 2017 | ✓ |  | Sales and marketing expenses increased $2.0 billion or 13%, primarily due to LinkedIn expenses and investments in commercial sales capacity, offset in part by a decrease in Windows marketing expenses. LinkedIn expenses i… |
| 3 | `MSFT_FY2018_2018-06-30:179` | Item 7 › Fiscal Year 2018 Compared with Fiscal Year 2017 |  |  | • Enterprise Services revenue increased $304 million or 5%, driven by higher revenue from Premier Support Services and Microsoft Consulting Services, offset in part by a decline in revenue from custom support agreements.… |
| 4 | `MSFT_FY2018_2018-06-30:196` | Item 7 › Fiscal Year 2017 Compared with Fiscal Year 2016 |  |  | Sales and marketing expenses increased $826 million or 6%, primarily due to LinkedIn expenses and increased investments in sales capacity for our commercial cloud, offset in part by a reduction in Phone expenses and prio… |
| 5 | `MSFT_FY2018_2018-06-30:159` | Item 7 |  |  | Highlights from fiscal year 2018 compared with fiscal year 2017 included: • Commercial cloud revenue, which primarily comprises Microsoft Office 365 commercial, Microsoft Azure, Microsoft Dynamics 365, and other cloud pr… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#1 `MSFT_FY2018_2018-06-30:171`** (cited)

````text
Item 7 > Fiscal Year 2018 Compared with Fiscal Year 2017
• Sales and marketing expenses increased $2.0 billion or 13%, primarily due to LinkedIn expenses and investments in commercial sales capacity, offset in part by a decrease in Windows marketing expenses. • Research and development expenses increased $1.7 billion or 13%, primarily due to investments in cloud engineering and LinkedIn expenses. • General and administrative expenses increased $273 million or 6%, primarily due to LinkedIn expenses. Current year net income and diluted EPS were negatively impacted by the net charge related to TCJA, which resulted in a decrease to net income and diluted earnings per share of $13.7 billion and $1.75, respectively. Prior year diluted EPS was negatively impacted by restructuring expenses, which resulted in a decrease in operating income, net income, and diluted EPS of $306 million, $243 million, and $0.04, respectively.
````

**#2 `MSFT_FY2018_2018-06-30:195`** (cited)

````text
Item 7 > Fiscal Year 2018 Compared with Fiscal Year 2017
Sales and marketing expenses increased $2.0 billion or 13%, primarily due to LinkedIn expenses and investments in commercial sales capacity, offset in part by a decrease in Windows marketing expenses. LinkedIn expenses increased $1.2 billion to $2.5 billion, including $617 million of amortization of acquired intangible assets.
````

</details>

RQ2 citation match (section level): `cited=[('MSFT', 'Item 7')] gold=[(None, 'Item 7'), (None, 'Item 1A')]`

### System C v1 (adaptive multi-hop)

Model: `gpt-5.4`. Hops: 1. Chunks retrieved: 6, cited: 4.

**Generated answer**

> Microsoft's sales and marketing expenses increased $2.0 billion in fiscal year 2018 compared to fiscal year 2017, which is $2,000 million. [MSFT FY2018, Item 7, MSFT_FY2018_2018-06-30:195] [MSFT FY2018, Item 7, MSFT_FY2018_2018-06-30:171]
>
> The company stated that this increase was primarily due to LinkedIn expenses and investments in commercial sales capacity, offset in part by a decrease in Windows marketing expenses. [MSFT FY2018, Item 7, MSFT_FY2018_2018-06-30:195] [MSFT FY2018, Item 7, MSFT_FY2018_2018-06-30:171]
>
> Microsoft also stated that sales and marketing expenses include costs associated with sales and marketing personnel and the costs of advertising, promotions, trade shows, seminars, and other programs. [MSFT FY2018, Item 7, MSFT_FY2018_2018-06-30:194] [MSFT FY2018, Item 8, MSFT_FY2018_2018-06-30:296]

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `MSFT_FY2018_2018-06-30:194` | Item 7 › Sales and Marketing | ✓ |  | Sales and marketing expenses include payroll, employee benefits, stock-based compensation expense, and other headcount-related expenses associated with sales and marketing personnel, and the costs of advertising, promoti… |
| 2 | `MSFT_FY2018_2018-06-30:196` | Item 7 › Fiscal Year 2017 Compared with Fiscal Year 2016 |  |  | Sales and marketing expenses increased $826 million or 6%, primarily due to LinkedIn expenses and increased investments in sales capacity for our commercial cloud, offset in part by a reduction in Phone expenses and prio… |
| 3 | `MSFT_FY2018_2018-06-30:195` | Item 7 › Fiscal Year 2018 Compared with Fiscal Year 2017 | ✓ |  | Sales and marketing expenses increased $2.0 billion or 13%, primarily due to LinkedIn expenses and investments in commercial sales capacity, offset in part by a decrease in Windows marketing expenses. LinkedIn expenses i… |
| 4 | `MSFT_FY2018_2018-06-30:296` | Item 8 › Sales and Marketing | ✓ |  | Sales and marketing expenses include payroll, employee benefits, stock-based compensation expense, and other headcount-related expenses associated with sales and marketing personnel, and the costs of advertising, promoti… |
| 5 | `MSFT_FY2018_2018-06-30:171` | Item 7 › Fiscal Year 2018 Compared with Fiscal Year 2017 | ✓ |  | • Sales and marketing expenses increased $2.0 billion or 13%, primarily due to LinkedIn expenses and investments in commercial sales capacity, offset in part by a decrease in Windows marketing expenses. • Research and de… |
| 6 | `MSFT_FY2018_2018-06-30:185` | Item 7 › PART II |  |  | • Phone revenue decreased $2.8 billion. Operating income increased $2.6 billion or 43%, including an unfavorable foreign currency impact of 3%. • Operating expenses decreased $1.5 billion or 12%, driven by a reduction in… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#1 `MSFT_FY2018_2018-06-30:194`** (cited)

````text
Item 7 > Sales and Marketing
Sales and marketing expenses include payroll, employee benefits, stock-based compensation expense, and other headcount-related expenses associated with sales and marketing personnel, and the costs of advertising, promotions, trade shows, seminars, and other programs.
````

**#3 `MSFT_FY2018_2018-06-30:195`** (cited)

````text
Item 7 > Fiscal Year 2018 Compared with Fiscal Year 2017
Sales and marketing expenses increased $2.0 billion or 13%, primarily due to LinkedIn expenses and investments in commercial sales capacity, offset in part by a decrease in Windows marketing expenses. LinkedIn expenses increased $1.2 billion to $2.5 billion, including $617 million of amortization of acquired intangible assets.
````

**#4 `MSFT_FY2018_2018-06-30:296`** (cited)

````text
Item 8 > Sales and Marketing
Sales and marketing expenses include payroll, employee benefits, stock-based compensation expense, and other headcount-related expenses associated with sales and marketing personnel, and the costs of advertising, promotions, trade shows, seminars, and other programs. Advertising costs are expensed as incurred. Advertising expense was $1.6 billion, $1.5 billion, and $1.6 billion in fiscal years 2018, 2017, and 2016, respectively.
````

**#5 `MSFT_FY2018_2018-06-30:171`** (cited)

````text
Item 7 > Fiscal Year 2018 Compared with Fiscal Year 2017
• Sales and marketing expenses increased $2.0 billion or 13%, primarily due to LinkedIn expenses and investments in commercial sales capacity, offset in part by a decrease in Windows marketing expenses. • Research and development expenses increased $1.7 billion or 13%, primarily due to investments in cloud engineering and LinkedIn expenses. • General and administrative expenses increased $273 million or 6%, primarily due to LinkedIn expenses. Current year net income and diluted EPS were negatively impacted by the net charge related to TCJA, which resulted in a decrease to net income and diluted earnings per share of $13.7 billion and $1.75, respectively. Prior year diluted EPS was negatively impacted by restructuring expenses, which resulted in a decrease in operating income, net income, and diluted EPS of $306 million, $243 million, and $0.04, respectively.
````

</details>

RQ2 citation match (section level): `cited=[('MSFT', 'Item 7'), ('MSFT', 'Item 8')] gold=[(None, 'Item 7'), (None, 'Item 1A')]`

**System C guardrail** (judge `gpt-5.4`): numerical claims 2, verified 2, ungrounded 0, uncited 0, derived 0; sentence verdicts: supported 2, partial 0, unsupported 0, unchecked 0.


<details><summary>Guardrail sentence verdicts</summary>

| sentence | verdict | judge reason |
|---|---|---|
| Microsoft's sales and marketing expenses increased $2.0 billion in fiscal year 2018 compared to fiscal year 2017, which is $2,000 million. [MSFT FY2018, Item 7, MSFT_FY2018_2018-06-30:195] [MSFT FY2018, Item 7, MSFT_FY2018_2018-06-30:171] | None |  |
| The company stated that this increase was primarily due to LinkedIn expenses and investments in commercial sales capacity, offset in part by a decrease in Windows marketing expenses. [MSFT FY2018, Item 7, MSFT_FY2018_2018-06-30:195] [MSFT FY2018, Item 7, MSFT_FY2018_2018-06-30:171] | supported | The cited passages state this increase was primarily due to LinkedIn expenses and investments in commercial sales capacity, partly offset by lower Windows marketing expenses. |
| Microsoft also stated that sales and marketing expenses include costs associated with sales and marketing personnel and the costs of advertising, promotions, trade shows, seminars, and other programs. [MSFT FY2018, Item 7, MSFT_FY2018_2018-06-30:194] [MSFT FY2018, Item 8, MSFT_FY2018_2018-06-30:296] | supported | The cited evidence explicitly says sales and marketing expenses include personnel-related costs and advertising, promotions, trade shows, seminars, and other programs. |

</details>

### System C v2 (agentic multi-hop + XBRL)

Model: `gpt-5.4`. Hops: 1. Chunks retrieved: 7, cited: 4.

**Generated answer**

> Microsoft stated that sales and marketing expenses increased by $2.0 billion, which is $2,000 million, in fiscal year 2018 compared with fiscal year 2017 [MSFT FY2018, Item 7, MSFT_FY2018_2018-06-30:195] [MSFT FY2018, Item 7, MSFT_FY2018_2018-06-30:171].  
>
> The filing states that sales and marketing expenses include ongoing investments such as payroll, employee benefits, stock-based compensation expense, and other headcount-related expenses associated with sales and marketing personnel, as well as the costs of advertising, promotions, trade shows, seminars, and other programs [MSFT FY2018, Item 7, MSFT_FY2018_2018-06-30:194] [MSFT FY2018, Item 8, MSFT_FY2018_2018-06-30:296].

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `F-MSFT-2018` | SEC XBRL Reported Financials (financials.csv) |  |  | fiscal_year,fiscal_year_end,Revenue,NetIncome,OperatingIncome,TotalAssets,TotalLiabilities,StockholdersEquity,CashAndEquivalents,OperatingCashFlow,EPSDiluted 2018,2018-06-30,110360000000,16571000000,35058000000,258848000… |
| 2 | `MSFT_FY2018_2018-06-30:194` | Item 7 › Sales and Marketing | ✓ |  | Sales and marketing expenses include payroll, employee benefits, stock-based compensation expense, and other headcount-related expenses associated with sales and marketing personnel, and the costs of advertising, promoti… |
| 3 | `MSFT_FY2018_2018-06-30:196` | Item 7 › Fiscal Year 2017 Compared with Fiscal Year 2016 |  |  | Sales and marketing expenses increased $826 million or 6%, primarily due to LinkedIn expenses and increased investments in sales capacity for our commercial cloud, offset in part by a reduction in Phone expenses and prio… |
| 4 | `MSFT_FY2018_2018-06-30:195` | Item 7 › Fiscal Year 2018 Compared with Fiscal Year 2017 | ✓ |  | Sales and marketing expenses increased $2.0 billion or 13%, primarily due to LinkedIn expenses and investments in commercial sales capacity, offset in part by a decrease in Windows marketing expenses. LinkedIn expenses i… |
| 5 | `MSFT_FY2018_2018-06-30:296` | Item 8 › Sales and Marketing | ✓ |  | Sales and marketing expenses include payroll, employee benefits, stock-based compensation expense, and other headcount-related expenses associated with sales and marketing personnel, and the costs of advertising, promoti… |
| 6 | `MSFT_FY2018_2018-06-30:171` | Item 7 › Fiscal Year 2018 Compared with Fiscal Year 2017 | ✓ |  | • Sales and marketing expenses increased $2.0 billion or 13%, primarily due to LinkedIn expenses and investments in commercial sales capacity, offset in part by a decrease in Windows marketing expenses. • Research and de… |
| 7 | `MSFT_FY2018_2018-06-30:185` | Item 7 › PART II |  |  | • Phone revenue decreased $2.8 billion. Operating income increased $2.6 billion or 43%, including an unfavorable foreign currency impact of 3%. • Operating expenses decreased $1.5 billion or 12%, driven by a reduction in… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#2 `MSFT_FY2018_2018-06-30:194`** (cited)

````text
Item 7 > Sales and Marketing
Sales and marketing expenses include payroll, employee benefits, stock-based compensation expense, and other headcount-related expenses associated with sales and marketing personnel, and the costs of advertising, promotions, trade shows, seminars, and other programs.
````

**#4 `MSFT_FY2018_2018-06-30:195`** (cited)

````text
Item 7 > Fiscal Year 2018 Compared with Fiscal Year 2017
Sales and marketing expenses increased $2.0 billion or 13%, primarily due to LinkedIn expenses and investments in commercial sales capacity, offset in part by a decrease in Windows marketing expenses. LinkedIn expenses increased $1.2 billion to $2.5 billion, including $617 million of amortization of acquired intangible assets.
````

**#5 `MSFT_FY2018_2018-06-30:296`** (cited)

````text
Item 8 > Sales and Marketing
Sales and marketing expenses include payroll, employee benefits, stock-based compensation expense, and other headcount-related expenses associated with sales and marketing personnel, and the costs of advertising, promotions, trade shows, seminars, and other programs. Advertising costs are expensed as incurred. Advertising expense was $1.6 billion, $1.5 billion, and $1.6 billion in fiscal years 2018, 2017, and 2016, respectively.
````

**#6 `MSFT_FY2018_2018-06-30:171`** (cited)

````text
Item 7 > Fiscal Year 2018 Compared with Fiscal Year 2017
• Sales and marketing expenses increased $2.0 billion or 13%, primarily due to LinkedIn expenses and investments in commercial sales capacity, offset in part by a decrease in Windows marketing expenses. • Research and development expenses increased $1.7 billion or 13%, primarily due to investments in cloud engineering and LinkedIn expenses. • General and administrative expenses increased $273 million or 6%, primarily due to LinkedIn expenses. Current year net income and diluted EPS were negatively impacted by the net charge related to TCJA, which resulted in a decrease to net income and diluted earnings per share of $13.7 billion and $1.75, respectively. Prior year diluted EPS was negatively impacted by restructuring expenses, which resulted in a decrease in operating income, net income, and diluted EPS of $306 million, $243 million, and $0.04, respectively.
````

</details>

RQ2 citation match (section level): `cited=[('MSFT', 'Item 7'), ('MSFT', 'Item 8')] gold=[(None, 'Item 7'), (None, 'Item 1A')]`

**System C guardrail** (judge `gpt-5.4`): numerical claims 2, verified 2, ungrounded 0, uncited 0, derived 0; sentence verdicts: supported 1, partial 0, unsupported 0, unchecked 0.


<details><summary>Guardrail sentence verdicts</summary>

| sentence | verdict | judge reason |
|---|---|---|
| Microsoft stated that sales and marketing expenses increased by $2.0 billion, which is $2,000 million, in fiscal year 2018 compared with fiscal year 2017 [MSFT FY2018, Item 7, MSFT_FY2018_2018-06-30:195] [MSFT FY2018, Item 7, MSFT_FY2018_2018-06-30:171]. | None |  |
| The filing states that sales and marketing expenses include ongoing investments such as payroll, employee benefits, stock-based compensation expense, and other headcount-related expenses associated with sales and marketing personnel, as well as the costs of advertising, promotions, trade shows, seminars, and other programs [MSFT FY2018, Item 7, MSFT_FY2018_2018-06-30:194] [MSFT FY2018, Item 8, MSFT_FY2018_2018-06-30:296]. | supported | Both cited passages state that sales and marketing expenses include those listed personnel-related costs and advertising, promotions, trade shows, seminars, and other programs. |

</details>
