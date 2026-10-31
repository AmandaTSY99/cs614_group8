# gold-016: Cross-year table

[← all cases](../README.md) · company: Meta Platforms, Inc. (META) · fiscal year: 2022 · recipe `cross_year_table` · hop `multi` · answer type `numeric` · scope `cross_year` · RQ2 category `multi_company_comparison`

## Gold QA

**Question**

> By what percentage did Meta Platforms' accrued compensation and benefits grow from December 31, 2016 to December 31, 2022?

**Gold answer**

> 621.86%

**Program**: `subtract(4591, 636), divide(#0, 636)` → `6.218553459119497`

**Gold numbers** (RQ2 numeric_accuracy targets): 621.86%

**Gold evidence**

1. `META_FY2022_2022-12-31` · Item 8.Financial Statements and Supplementary Data › Note 12. Liabilities · table

   > Accrued compensation and benefits | 4,591 | 3,152

2. `META_FY2016_2016-12-31` · Item 8. Financial Statements and Supplementary Data › Accounting Pronouncements Not Yet Adopted · table

   > Accrued compensation and benefits | $636 | $473

## Scorecard

| Metric | A (vanilla dense) | B (hybrid + rerank) | C v1 (adaptive multi-hop) | C v2 (agentic multi-hop + XBRL) |
|---|---|---|---|---|
| **Retrieval (RQ1)** | | | | |
| chunks retrieved | 10 | 5 | 6 | 8 |
| recall@5 | 0.00 | 1.00 | 1.00 | 1.00 |
| recall@all | 0.00 | 1.00 | 1.00 | 1.00 |
| complete@all | 0 | 1 | 1 | 1 |
| average precision (lexical) | 0.00 | 0.48 | 1.00 | 0.48 |
| gold evidence first rank | #1: –, #2: – | #1: 3, #2: 3 | #1: 1, #2: 1 | #1: 3, #2: 3 |
| **Answer (RQ3 string match)** | | | | |
| numeric_correct | ✗ | ✓ | ✓ | ✓ |
| keypoint_recall | – | – | – | – |
| **Answer & citations (RQ2)** | | | | |
| numeric_accuracy | 0.00 | 1.00 | 1.00 | 1.00 |
| citation precision | – | 1.00 | 1.00 | 1.00 |
| citation recall | – | 1.00 | 1.00 | 1.00 |
| citation F1 | – | 1.00 | 1.00 | 1.00 |
| has a citation | 0 | 1 | 1 | 1 |
| grounding error rate | – | – | 0.20 | 0.50 |
| **Cost (RQ3)** | | | | |
| retrieval hops | 1 | 1 | 1 | 1 |
| tokens | 2155 | 1282 | 6742 | 7718 |
| cost (USD) | 0.0003 | 0.0002 | 0.0233 | 0.0254 |
| latency (s) | 1.8 | 7.3 | 9.0 | 10.6 |

Definitions: [README › Metrics](../README.md#metrics). `–` = not applicable (e.g. no gold number, no citations, no guardrail).

## System outputs

### System A (vanilla dense)

Model: `gpt-5.4-2026-03-05`. Hops: 1. Chunks retrieved: 10, cited: 0.

**Generated answer**

> Not found in the provided context.

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `META_FY2016_2016-12-31:408` | Item 8 › Share-based Compensation Plans |  |  | \| \| Year Ended December 31, \| \| \| \|---\|---\|---\|---\| \| \| 2016 \| 2015 \| 2014 \| \| U.S. federal statutory income tax rate \| 35.0% \| 35.0% \| 35.0% \| \| State income taxes, net of federal benefit \| 1.0 \| 2.0 \| 1.4 \| \| Research … |
| 2 | `META_FY2016_2016-12-31:417` | Item 8 › Share-based Compensation Plans |  |  | \| \| Year Ended December 31, \| \| \| \|---\|---\|---\|---\| \| \| 2016 \| 2015 \| 2014 \| \| Revenue: \| \| \| \| \| United States \| $12,579 \| $8,513 \| $5,649 \| \| Rest of the world(1) \| 15,059 \| 9,415 \| 6,817 \| \| Total revenue \| $27,638 \| … |
| 3 | `META_FY2016_2016-12-31:413` | Item 8 › Share-based Compensation Plans |  |  | \| \| Year Ended December 31, \| \| \| \|---\|---\|---\|---\| \| \| 2016 \| 2015 \| 2014 \| \| Gross unrecognized tax benefits-beginning of period \| $3,017 \| $1,682 \| $1,316 \| \| Increases related to prior year tax positions \| 32 \| 322 \|… |
| 4 | `META_FY2022_2022-12-31:553` | Item 8 › Note 16. Income Taxes |  |  | \| \| Year Ended December 31, \| \| \| \|---\|---\|---\|---\| \| \| 2022 \| 2021 \| 2020 \| \| U.S. federal statutory income tax rate \| 21.0% \| 21.0% \| 21.0% \| \| State income taxes, net of federal benefit \| 1.0 \| 1.0 \| 0.8 \| \| Share-bas… |
| 5 | `META_FY2016_2016-12-31:404` | Item 8 › Share-based Compensation Plans |  |  | \| \| Year Ended December 31, \| \| \| \|---\|---\|---\|---\| \| \| 2016 \| 2015 \| 2014 \| \| Domestic \| $6,368 \| $2,802 \| $4,918 \| \| Foreign \| 6,150 \| 3,392 \| (8) \| \| Income before provision for income taxes \| $12,518 \| $6,194 \| $4,91… |
| 6 | `META_FY2022_2022-12-31:544` | Item 8 › Share-based Compensation Plan |  |  | \| \| Number of Shares \| Weighted-Average Grant Date Fair Value Per Share \| \|---\|---\|---\| \| \| (in thousands) \| \| \| Unvested at December 31, 2021 \| 98,848 \| $244.32 \| \| Granted \| 106,693 \| $195.66 \| \| Vested \| (54,013) \| $2… |
| 7 | `META_FY2022_2022-12-31:323` | Item 7 › Revenue |  |  | \| \| Year Ended December 31, \| \| \| \| \| \|---\|---\|---\|---\|---\|---\| \| \| 2022 \| 2021 \| 2020 \| 2022 vs 2021 % change \| 2021 vs 2020 % change \| \| \| (in millions, except percentages) \| \| \| \| \| \| Advertising \| $113,642 \| $114,934… |
| 8 | `META_FY2022_2022-12-31:460` | Item 8 › Note 2. Revenue |  |  | \| \| Year Ended December 31, \| \| \| \|---\|---\|---\|---\| \| \| 2022 \| 2021 \| 2020 \| \| United States and Canada (1) \| $50,150 \| $51,541 \| $38,433 \| \| Europe (2) \| 26,681 \| 29,057 \| 20,349 \| \| Asia-Pacific \| 27,760 \| 26,739 \| 19,… |
| 9 | `META_FY2022_2022-12-31:339` | Item 7 › Segment profitability |  |  | \| \| Year Ended December 31, \| \| \| \| \| \|---\|---\|---\|---\|---\|---\| \| \| 2022 \| 2021 \| 2020 \| 2022 vs 2021 % change \| 2021 vs 2020 % change \| \| \| (in millions, except percentages) \| \| \| \| \| \| Family of Apps \| $42,661 \| $56,94… |
| 10 | `META_FY2016_2016-12-31:406` | Item 8 › Share-based Compensation Plans |  |  | \| \| Year Ended December 31, \| \| \| \|---\|---\|---\|---\| \| \| 2016 \| 2015 \| 2014 \| \| Current: \| \| \| \| \| Federal \| $2,384 \| $3,012 \| $1,999 \| \| State \| 179 \| 183 \| 130 \| \| Foreign \| 195 \| 123 \| 96 \| \| Total current tax expense … |

RQ2 citation match (section level): `no citations`

### System B (hybrid + rerank)

Model: `gpt-5.4-2026-03-05`. Hops: 1. Chunks retrieved: 5, cited: 2.

**Generated answer**

> Meta Platforms' accrued compensation and benefits increased from $636 million in 2016 to $4,591 million in 2022 [4][3].
>
> Percentage growth = \(\frac{4,591 - 636}{636} \times 100 \approx 621.9\%\)
>
> So, the accrued compensation and benefits grew by approximately **622%** [4][3].

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `META_FY2016_2016-12-31:221` | Item 7 › Research and development |  |  | 2016 Compared to 2015. Research and development expenses in 2016 increased $1.10 billion, or 23%, compared to 2015. The majority of the increase was due to an increase in payroll and benefits as a result of a 34% growth … |
| 2 | `META_FY2016_2016-12-31:225` | Item 7 › General and administrative |  |  | 2016 Compared to 2015. General and administrative expenses in 2016 increased $436 million, or 34%, compared to 2015. The majority of the increase was due to an increase in payroll and benefits expenses as a result of a 4… |
| 3 | `META_FY2022_2022-12-31:513` | Item 8 › Note 12. Liabilities | ✓ | #1, #2 | \| \| December 31, \| \| \|---\|---\|---\| \| \| 2022 \| 2021 \| \| Legal-related accruals (1) \| $4,795 \| $3,254 \| \| Accrued compensation and benefits \| 4,591 \| 3,152 \| \| Accrued property and equipment \| 2,921 \| 1,392 \| \| Accrued tax… |
| 4 | `META_FY2016_2016-12-31:374` | Item 8 › Accounting Pronouncements Not Yet Adopted | ✓ | #1, #2 | \| \| December 31, \| \| \|---\|---\|---\| \| \| 2016 \| 2015 \| \| Accrued compensation and benefits \| $636 \| $473 \| \| Accrued property and equipment \| 331 \| 192 \| \| Promissory note payable \| — \| 201 \| \| Contingent consideration lia… |
| 5 | `META_FY2016_2016-12-31:414` | Item 8 › Share-based Compensation Plans |  | #1, #2 | During all years presented, we recognized interest and penalties related to unrecognized tax benefits within the provision for income taxes on the consolidated statements of income. The amount of interest and penalties a… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#3 `META_FY2022_2022-12-31:513`** (cited, gold #1, gold #2)

````text
Item 8.Financial Statements and Supplementary Data > Note 12. Liabilities (table)
|  | December 31, |  |
|---|---|---|
|  | 2022 | 2021 |
| Legal-related accruals (1) | $4,795 | $3,254 |
| Accrued compensation and benefits | 4,591 | 3,152 |
| Accrued property and equipment | 2,921 | 1,392 |
| Accrued taxes | 2,339 | 1,256 |
| Other current liabilities | 4,906 | 5,819 |
| Accrued expenses and other current liabilities | $19,552 | $14,873 |
````

**#4 `META_FY2016_2016-12-31:374`** (cited, gold #1, gold #2)

````text
Item 8. Financial Statements and Supplementary Data > Accounting Pronouncements Not Yet Adopted (table)
|  | December 31, |  |
|---|---|---|
|  | 2016 | 2015 |
| Accrued compensation and benefits | $636 | $473 |
| Accrued property and equipment | 331 | 192 |
| Promissory note payable | — | 201 |
| Contingent consideration liability | 242 | — |
| Other current liabilities | 994 | 583 |
| Accrued expenses and other current liabilities | $2,203 | $1,449 |
````

**#5 `META_FY2016_2016-12-31:414`** (gold #1, gold #2)

````text
Item 8. Financial Statements and Supplementary Data > Share-based Compensation Plans
During all years presented, we recognized interest and penalties related to unrecognized tax benefits within the provision for income taxes on the consolidated statements of income. The amount of interest and penalties accrued as of December 31, 2016 and 2015 was $80 million and $36 million, respectively. If the balance of gross unrecognized tax benefits of $3.31 billion as of December 31, 2016 were realized in a future period, this would result in a tax benefit of $2.58 billion within our provision of income taxes at such time. We are subject to taxation in the United States and various other state and foreign jurisdictions. The material jurisdictions in which we are subject to potential examination include the United States and Ireland. We are under examination by the Internal Revenue Service (IRS) for our 2010 through 2013 tax years. Our 2014 and subsequent years remain open to examination by the IRS. Our 2011 and subsequent years remain open to examination in Ireland.
````

</details>

RQ2 citation match (section level): `cited=[('META', 'Item 8')] gold=[(None, 'Item 8')]`

### System C v1 (adaptive multi-hop)

Model: `gpt-5.4`. Hops: 1. Chunks retrieved: 6, cited: 2.

**Generated answer**

> Meta Platforms' accrued compensation and benefits increased from $636 million at December 31, 2016 to $4,591 million at December 31, 2022 [META FY2016, Item 8, META_FY2016_2016-12-31:374] [META FY2022, Item 8, META_FY2022_2022-12-31:513].
>
> The percentage growth over that period was approximately 621.9%, calculated as (($4,591 - $636) / $636) × 100 [META FY2016, Item 8, META_FY2016_2016-12-31:374] [META FY2022, Item 8, META_FY2022_2022-12-31:513].
>
> > [Guardrail Audit Warning]: Manual verification required; these numerical figures could not be matched in their cited chunks: 636; 1 sentence(s) are not supported by their cited chunks.

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `META_FY2016_2016-12-31:414` | Item 8 › Share-based Compensation Plans |  | #1, #2 | During all years presented, we recognized interest and penalties related to unrecognized tax benefits within the provision for income taxes on the consolidated statements of income. The amount of interest and penalties a… |
| 2 | `META_FY2022_2022-12-31:513` | Item 8 › Note 12. Liabilities | ✓ | #1, #2 | \| \| December 31, \| \| \|---\|---\|---\| \| \| 2022 \| 2021 \| \| Legal-related accruals (1) \| $4,795 \| $3,254 \| \| Accrued compensation and benefits \| 4,591 \| 3,152 \| \| Accrued property and equipment \| 2,921 \| 1,392 \| \| Accrued tax… |
| 3 | `META_FY2016_2016-12-31:374` | Item 8 › Accounting Pronouncements Not Yet Adopted | ✓ | #1, #2 | \| \| December 31, \| \| \|---\|---\|---\| \| \| 2016 \| 2015 \| \| Accrued compensation and benefits \| $636 \| $473 \| \| Accrued property and equipment \| 331 \| 192 \| \| Promissory note payable \| — \| 201 \| \| Contingent consideration lia… |
| 4 | `META_FY2022_2022-12-31:543` | Item 8 › Share-based Compensation Plan |  |  | December 31st or (ii) a number of shares determined by our board of directors. Pursuant to this automatic increase provision, our board of directors approved an increase of 56 million shares of Class A common stock reser… |
| 5 | `META_FY2022_2022-12-31:542` | Item 8 › Share-based Compensation Plan |  |  | We have one active share-based employee compensation plan, the 2012 Equity Incentive Plan (Amended 2012 Plan), which was amended in each of June 2016, February 2018, and December 2022. Our Amended 2012 Plan provides for … |
| 6 | `META_FY2016_2016-12-31:413` | Item 8 › Share-based Compensation Plans |  |  | \| \| Year Ended December 31, \| \| \| \|---\|---\|---\|---\| \| \| 2016 \| 2015 \| 2014 \| \| Gross unrecognized tax benefits-beginning of period \| $3,017 \| $1,682 \| $1,316 \| \| Increases related to prior year tax positions \| 32 \| 322 \|… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#1 `META_FY2016_2016-12-31:414`** (gold #1, gold #2)

````text
Item 8. Financial Statements and Supplementary Data > Share-based Compensation Plans
During all years presented, we recognized interest and penalties related to unrecognized tax benefits within the provision for income taxes on the consolidated statements of income. The amount of interest and penalties accrued as of December 31, 2016 and 2015 was $80 million and $36 million, respectively. If the balance of gross unrecognized tax benefits of $3.31 billion as of December 31, 2016 were realized in a future period, this would result in a tax benefit of $2.58 billion within our provision of income taxes at such time. We are subject to taxation in the United States and various other state and foreign jurisdictions. The material jurisdictions in which we are subject to potential examination include the United States and Ireland. We are under examination by the Internal Revenue Service (IRS) for our 2010 through 2013 tax years. Our 2014 and subsequent years remain open to examination by the IRS. Our 2011 and subsequent years remain open to examination in Ireland.
````

**#2 `META_FY2022_2022-12-31:513`** (cited, gold #1, gold #2)

````text
Item 8.Financial Statements and Supplementary Data > Note 12. Liabilities (table)
|  | December 31, |  |
|---|---|---|
|  | 2022 | 2021 |
| Legal-related accruals (1) | $4,795 | $3,254 |
| Accrued compensation and benefits | 4,591 | 3,152 |
| Accrued property and equipment | 2,921 | 1,392 |
| Accrued taxes | 2,339 | 1,256 |
| Other current liabilities | 4,906 | 5,819 |
| Accrued expenses and other current liabilities | $19,552 | $14,873 |
````

**#3 `META_FY2016_2016-12-31:374`** (cited, gold #1, gold #2)

````text
Item 8. Financial Statements and Supplementary Data > Accounting Pronouncements Not Yet Adopted (table)
|  | December 31, |  |
|---|---|---|
|  | 2016 | 2015 |
| Accrued compensation and benefits | $636 | $473 |
| Accrued property and equipment | 331 | 192 |
| Promissory note payable | — | 201 |
| Contingent consideration liability | 242 | — |
| Other current liabilities | 994 | 583 |
| Accrued expenses and other current liabilities | $2,203 | $1,449 |
````

</details>

RQ2 citation match (section level): `cited=[('META', 'Item 8')] gold=[(None, 'Item 8')]`

**System C guardrail** (judge `gpt-5.4`): numerical claims 6, verified 5, ungrounded 1, uncited 0, derived 1; sentence verdicts: supported 0, partial 0, unsupported 0, unchecked 0.

- ungrounded numbers: 636

<details><summary>Guardrail sentence verdicts</summary>

| sentence | verdict | judge reason |
|---|---|---|
| Meta Platforms' accrued compensation and benefits increased from $636 million at December 31, 2016 to $4,591 million at December 31, 2022 [META FY2016, Item 8, META_FY2016_2016-12-31:374] [META FY2022, Item 8, META_FY2022_2022-12-31:513]. | None |  |
| The percentage growth over that period was approximately 621.9%, calculated as (($4,591 - $636) / $636) × 100 [META FY2016, Item 8, META_FY2016_2016-12-31:374] [META FY2022, Item 8, META_FY2022_2022-12-31:513]. | None |  |

</details>

### System C v2 (agentic multi-hop + XBRL)

Model: `gpt-5.4`. Hops: 1. Chunks retrieved: 8, cited: 2.

**Generated answer**

> Meta Platforms' accrued compensation and benefits increased from $636 million at December 31, 2016 to $4,591 million at December 31, 2022. [META FY2016, Item 8, META_FY2016_2016-12-31:374] [META FY2022, Item 8, META_FY2022_2022-12-31:513]
>
> That represents growth of approximately 621.9% from 2016 to 2022. [META FY2016, Item 8, META_FY2016_2016-12-31:374] [META FY2022, Item 8, META_FY2022_2022-12-31:513]
>
> > [Guardrail Audit Warning]: Manual verification required; these numerical figures could not be matched in their cited chunks: 636; 1 sentence(s) are not supported by their cited chunks.

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `F-META-2016` | SEC XBRL Reported Financials (financials.csv) |  |  | fiscal_year,fiscal_year_end,Revenue,NetIncome,OperatingIncome,TotalAssets,TotalLiabilities,StockholdersEquity,CashAndEquivalents,OperatingCashFlow,EPSDiluted 2016,2016-12-31,27638000000,10217000000,12427000000,6496100000… |
| 2 | `F-META-2022` | SEC XBRL Reported Financials (financials.csv) |  |  | fiscal_year,fiscal_year_end,Revenue,NetIncome,OperatingIncome,TotalAssets,TotalLiabilities,StockholdersEquity,CashAndEquivalents,OperatingCashFlow,EPSDiluted 2022,2022-12-31,116609000000,23200000000,28944000000,185727000… |
| 3 | `META_FY2016_2016-12-31:414` | Item 8 › Share-based Compensation Plans |  | #1, #2 | During all years presented, we recognized interest and penalties related to unrecognized tax benefits within the provision for income taxes on the consolidated statements of income. The amount of interest and penalties a… |
| 4 | `META_FY2022_2022-12-31:513` | Item 8 › Note 12. Liabilities | ✓ | #1, #2 | \| \| December 31, \| \| \|---\|---\|---\| \| \| 2022 \| 2021 \| \| Legal-related accruals (1) \| $4,795 \| $3,254 \| \| Accrued compensation and benefits \| 4,591 \| 3,152 \| \| Accrued property and equipment \| 2,921 \| 1,392 \| \| Accrued tax… |
| 5 | `META_FY2016_2016-12-31:374` | Item 8 › Accounting Pronouncements Not Yet Adopted | ✓ | #1, #2 | \| \| December 31, \| \| \|---\|---\|---\| \| \| 2016 \| 2015 \| \| Accrued compensation and benefits \| $636 \| $473 \| \| Accrued property and equipment \| 331 \| 192 \| \| Promissory note payable \| — \| 201 \| \| Contingent consideration lia… |
| 6 | `META_FY2022_2022-12-31:543` | Item 8 › Share-based Compensation Plan |  |  | December 31st or (ii) a number of shares determined by our board of directors. Pursuant to this automatic increase provision, our board of directors approved an increase of 56 million shares of Class A common stock reser… |
| 7 | `META_FY2022_2022-12-31:542` | Item 8 › Share-based Compensation Plan |  |  | We have one active share-based employee compensation plan, the 2012 Equity Incentive Plan (Amended 2012 Plan), which was amended in each of June 2016, February 2018, and December 2022. Our Amended 2012 Plan provides for … |
| 8 | `META_FY2016_2016-12-31:413` | Item 8 › Share-based Compensation Plans |  |  | \| \| Year Ended December 31, \| \| \| \|---\|---\|---\|---\| \| \| 2016 \| 2015 \| 2014 \| \| Gross unrecognized tax benefits-beginning of period \| $3,017 \| $1,682 \| $1,316 \| \| Increases related to prior year tax positions \| 32 \| 322 \|… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#3 `META_FY2016_2016-12-31:414`** (gold #1, gold #2)

````text
Item 8. Financial Statements and Supplementary Data > Share-based Compensation Plans
During all years presented, we recognized interest and penalties related to unrecognized tax benefits within the provision for income taxes on the consolidated statements of income. The amount of interest and penalties accrued as of December 31, 2016 and 2015 was $80 million and $36 million, respectively. If the balance of gross unrecognized tax benefits of $3.31 billion as of December 31, 2016 were realized in a future period, this would result in a tax benefit of $2.58 billion within our provision of income taxes at such time. We are subject to taxation in the United States and various other state and foreign jurisdictions. The material jurisdictions in which we are subject to potential examination include the United States and Ireland. We are under examination by the Internal Revenue Service (IRS) for our 2010 through 2013 tax years. Our 2014 and subsequent years remain open to examination by the IRS. Our 2011 and subsequent years remain open to examination in Ireland.
````

**#4 `META_FY2022_2022-12-31:513`** (cited, gold #1, gold #2)

````text
Item 8.Financial Statements and Supplementary Data > Note 12. Liabilities (table)
|  | December 31, |  |
|---|---|---|
|  | 2022 | 2021 |
| Legal-related accruals (1) | $4,795 | $3,254 |
| Accrued compensation and benefits | 4,591 | 3,152 |
| Accrued property and equipment | 2,921 | 1,392 |
| Accrued taxes | 2,339 | 1,256 |
| Other current liabilities | 4,906 | 5,819 |
| Accrued expenses and other current liabilities | $19,552 | $14,873 |
````

**#5 `META_FY2016_2016-12-31:374`** (cited, gold #1, gold #2)

````text
Item 8. Financial Statements and Supplementary Data > Accounting Pronouncements Not Yet Adopted (table)
|  | December 31, |  |
|---|---|---|
|  | 2016 | 2015 |
| Accrued compensation and benefits | $636 | $473 |
| Accrued property and equipment | 331 | 192 |
| Promissory note payable | — | 201 |
| Contingent consideration liability | 242 | — |
| Other current liabilities | 994 | 583 |
| Accrued expenses and other current liabilities | $2,203 | $1,449 |
````

</details>

RQ2 citation match (section level): `cited=[('META', 'Item 8')] gold=[(None, 'Item 8')]`

**System C guardrail** (judge `gpt-5.4`): numerical claims 3, verified 2, ungrounded 1, uncited 0, derived 1; sentence verdicts: supported 0, partial 0, unsupported 0, unchecked 0.

- ungrounded numbers: 636

<details><summary>Guardrail sentence verdicts</summary>

| sentence | verdict | judge reason |
|---|---|---|
| Meta Platforms' accrued compensation and benefits increased from $636 million at December 31, 2016 to $4,591 million at December 31, 2022. [META FY2016, Item 8, META_FY2016_2016-12-31:374] [META FY2022, Item 8, META_FY2022_2022-12-31:513] | None |  |
| That represents growth of approximately 621.9% from 2016 to 2022. [META FY2016, Item 8, META_FY2016_2016-12-31:374] [META FY2022, Item 8, META_FY2022_2022-12-31:513] | None |  |

</details>
