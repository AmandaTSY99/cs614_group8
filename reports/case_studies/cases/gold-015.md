# gold-015: Cross-year table

[← all cases](../README.md) · company: Meta Platforms, Inc. (META) · fiscal year: 2021 · recipe `cross_year_table` · hop `multi` · answer type `numeric` · scope `cross_year` · RQ2 category `multi_company_comparison`

## Gold QA

**Question**

> Calculate the percentage change in Meta Platforms' foreign income before provision for income taxes from fiscal year 2016 to fiscal year 2021. Use the values in millions of dollars.

**Gold answer**

> -41.22%

**Program**: `subtract(3615, 6150), divide(#0, 6150), multiply(#1, 100)` → `-41.21951219512195`

**Gold numbers** (RQ2 numeric_accuracy targets): -41.22%

**Gold evidence**

1. `META_FY2021_2021-12-31` · Item 8.Financial Statements and Supplementary Data › Note 14. Income Taxes · table

   > Foreign | 3,615 | 8,947 | 19,495

2. `META_FY2016_2016-12-31` · Item 8. Financial Statements and Supplementary Data › Share-based Compensation Plans · table

   > Foreign | 6,150 | 3,392 | (8)

## Scorecard

| Metric | A (vanilla dense) | B (hybrid + rerank) | C v1 (adaptive multi-hop) | C v2 (agentic multi-hop + XBRL) |
|---|---|---|---|---|
| **Retrieval (RQ1)** | | | | |
| chunks retrieved | 10 | 5 | 6 | 8 |
| recall@5 | 0.50 | 0.00 | 0.50 | 0.50 |
| recall@all | 0.50 | 0.00 | 1.00 | 1.00 |
| complete@all | 0 | 0 | 1 | 1 |
| average precision (lexical) | 1.00 | 0.00 | 0.42 | 0.25 |
| gold evidence first rank | #1: 1, #2: – | #1: –, #2: – | #1: 2, #2: 6 | #1: 4, #2: 8 |
| **Answer (RQ3 string match)** | | | | |
| numeric_correct | ✗ | ✗ | ✓ | ✓ |
| keypoint_recall | – | – | – | – |
| **Answer & citations (RQ2)** | | | | |
| numeric_accuracy | 0.00 | 0.00 | 0.00 | 0.00 |
| citation precision | – | – | 1.00 | 1.00 |
| citation recall | – | – | 1.00 | 1.00 |
| citation F1 | – | – | 1.00 | 1.00 |
| has a citation | 0 | 0 | 1 | 1 |
| grounding error rate | – | – | 0.00 | 0.00 |
| **Cost (RQ3)** | | | | |
| retrieval hops | 1 | 1 | 1 | 1 |
| tokens | 1859 | 866 | 3902 | 4672 |
| cost (USD) | 0.0003 | 0.0001 | 0.0149 | 0.0172 |
| latency (s) | 1.5 | 6.0 | 7.3 | 7.3 |

Definitions: [README › Metrics](../README.md#metrics). `–` = not applicable (e.g. no gold number, no citations, no guardrail).

## System outputs

### System A (vanilla dense)

Model: `gpt-5.4-2026-03-05`. Hops: 1. Chunks retrieved: 10, cited: 0.

**Generated answer**

> Not found in the provided context.

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `META_FY2021_2021-12-31:502` | Item 8 › Note 14. Income Taxes |  | #1 | \| \| Year Ended December 31, \| \| \| \|---\|---\|---\|---\| \| \| 2021 \| 2020 \| 2019 \| \| Domestic \| $43,669 \| $24,233 \| $5,317 \| \| Foreign \| 3,615 \| 8,947 \| 19,495 \| \| Income before provision for income taxes \| $47,284 \| $33,180 \|… |
| 2 | `META_FY2021_2021-12-31:326` | Item 7 › Provision for income taxes |  |  | \| \| Year Ended December 31, \| \| \| \| \| \|---\|---\|---\|---\|---\|---\| \| \| 2021 \| 2020 \| 2019 \| 2021 vs 2020 % Change \| 2020 vs 2019 % Change \| \| \| (dollars in millions) \| \| \| \| \| \| Provision for income taxes \| $7,914 \| $4,034 … |
| 3 | `META_FY2021_2021-12-31:327` | Item 7 › Provision for income taxes |  |  | Our provision for income taxes in 2021 increased $3.88 billion, or 96%, compared to 2020, primarily due to an increase in income from operations and the effects of the tax election described below. Our effective tax rate… |
| 4 | `META_FY2016_2016-12-31:229` | Item 7 › Provision for income taxes |  |  | 2016 Compared to 2015. Our provision for income taxes in 2016 decreased $205 million, or 8%, compared to 2015, primarily due to the impact of the adoption of ASU 2016-09, and was partially offset by an increase in income… |
| 5 | `META_FY2016_2016-12-31:232` | Item 7 › Provision for income taxes |  |  | flows. 2015 Compared to 2014. Our provision for income taxes in 2015 increased $536 million, or 27%, compared to 2014, primarily due to an increase in income before provision for income taxes. Our effective tax rate in 2… |
| 6 | `META_FY2021_2021-12-31:506` | Item 8 › Note 14. Income Taxes |  |  | \| \| Year Ended December 31, \| \| \| \|---\|---\|---\|---\| \| \| 2021 \| 2020 \| 2019 \| \| U.S. federal statutory income tax rate \| 21.0% \| 21.0% \| 21.0% \| \| State income taxes, net of federal benefit \| 1.0 \| 0.8 \| 1.8 \| \| Share-bas… |
| 7 | `META_FY2016_2016-12-31:228` | Item 7 › Provision for income taxes |  |  | \| \| Year Ended December 31, \| \| \| \| \| \|---\|---\|---\|---\|---\|---\| \| \| 2016 \| 2015 \| 2014 \| 2016 vs 2015 % Change \| 2015 vs 2014 % Change \| \| \| (dollars in millions) \| \| \| \| \| \| Provision for income taxes \| $2,301 \| $2,506 … |
| 8 | `META_FY2021_2021-12-31:504` | Item 8 › Note 14. Income Taxes |  |  | \| \| Year Ended December 31, \| \| \| \|---\|---\|---\|---\| \| \| 2021 \| 2020 \| 2019 \| \| Current: \| \| \| \| \| Federal \| $4,971 \| $3,297 \| $4,321 \| \| State \| 548 \| 523 \| 565 \| \| Foreign \| 1,786 \| 1,211 \| 1,481 \| \| Total current tax e… |
| 9 | `META_FY2021_2021-12-31:505` | Item 8 › Note 14. Income Taxes |  |  | A reconciliation of the U.S. federal statutory income tax rates to our effective tax rate is as follows (in percentages): |
| 10 | `META_FY2021_2021-12-31:501` | Item 8 › Note 14. Income Taxes |  |  | The components of income before provision for income taxes are as follows (in millions): |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#1 `META_FY2021_2021-12-31:502`** (gold #1)

````text
Item 8.Financial Statements and Supplementary Data > Note 14. Income Taxes (table)
|  | Year Ended December 31, |  |  |
|---|---|---|---|
|  | 2021 | 2020 | 2019 |
| Domestic | $43,669 | $24,233 | $5,317 |
| Foreign | 3,615 | 8,947 | 19,495 |
| Income before provision for income taxes | $47,284 | $33,180 | $24,812 |
````

</details>

RQ2 citation match (section level): `no citations`

### System B (hybrid + rerank)

Model: `gpt-5.4-2026-03-05`. Hops: 1. Chunks retrieved: 5, cited: 0.

**Generated answer**

> Not found in the provided context.

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `META_FY2016_2016-12-31:412` | Item 8 › Share-based Compensation Plans |  |  | Our foreign income before provision for income taxes of $6.15 billion resulted in certain of our foreign jurisdictions moving from a position of having cumulative losses to cumulative earnings. In accordance with ASC 740… |
| 2 | `META_FY2021_2021-12-31:327` | Item 7 › Provision for income taxes |  |  | Our provision for income taxes in 2021 increased $3.88 billion, or 96%, compared to 2020, primarily due to an increase in income from operations and the effects of the tax election described below. Our effective tax rate… |
| 3 | `META_FY2021_2021-12-31:503` | Item 8 › Note 14. Income Taxes |  |  | The provision for income taxes consists of the following (in millions): |
| 4 | `META_FY2021_2021-12-31:326` | Item 7 › Provision for income taxes |  |  | \| \| Year Ended December 31, \| \| \| \| \| \|---\|---\|---\|---\|---\|---\| \| \| 2021 \| 2020 \| 2019 \| 2021 vs 2020 % Change \| 2020 vs 2019 % Change \| \| \| (dollars in millions) \| \| \| \| \| \| Provision for income taxes \| $7,914 \| $4,034 … |
| 5 | `META_FY2021_2021-12-31:501` | Item 8 › Note 14. Income Taxes |  |  | The components of income before provision for income taxes are as follows (in millions): |

RQ2 citation match (section level): `no citations`

### System C v1 (adaptive multi-hop)

Model: `gpt-5.4`. Hops: 1. Chunks retrieved: 6, cited: 2.

**Generated answer**

> Meta Platforms' foreign income before provision for income taxes increased from $6,150 million in fiscal year 2016 to $3,615 million in fiscal year 2021 [META FY2016, Item 8, META_FY2016_2016-12-31:404] [META FY2021, Item 8, META_FY2021_2021-12-31:502].
>
> The percentage change from 2016 to 2021 was -41.2%, calculated as (($3,615 - $6,150) / $6,150) × 100 [META FY2016, Item 8, META_FY2016_2016-12-31:404] [META FY2021, Item 8, META_FY2021_2021-12-31:502].

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `META_FY2016_2016-12-31:412` | Item 8 › Share-based Compensation Plans |  |  | Our foreign income before provision for income taxes of $6.15 billion resulted in certain of our foreign jurisdictions moving from a position of having cumulative losses to cumulative earnings. In accordance with ASC 740… |
| 2 | `META_FY2021_2021-12-31:502` | Item 8 › Note 14. Income Taxes | ✓ | #1 | \| \| Year Ended December 31, \| \| \| \|---\|---\|---\|---\| \| \| 2021 \| 2020 \| 2019 \| \| Domestic \| $43,669 \| $24,233 \| $5,317 \| \| Foreign \| 3,615 \| 8,947 \| 19,495 \| \| Income before provision for income taxes \| $47,284 \| $33,180 \|… |
| 3 | `META_FY2016_2016-12-31:229` | Item 7 › Provision for income taxes |  |  | 2016 Compared to 2015. Our provision for income taxes in 2016 decreased $205 million, or 8%, compared to 2015, primarily due to the impact of the adoption of ASU 2016-09, and was partially offset by an increase in income… |
| 4 | `META_FY2021_2021-12-31:501` | Item 8 › Note 14. Income Taxes |  |  | The components of income before provision for income taxes are as follows (in millions): |
| 5 | `META_FY2021_2021-12-31:327` | Item 7 › Provision for income taxes |  |  | Our provision for income taxes in 2021 increased $3.88 billion, or 96%, compared to 2020, primarily due to an increase in income from operations and the effects of the tax election described below. Our effective tax rate… |
| 6 | `META_FY2016_2016-12-31:404` | Item 8 › Share-based Compensation Plans | ✓ | #2 | \| \| Year Ended December 31, \| \| \| \|---\|---\|---\|---\| \| \| 2016 \| 2015 \| 2014 \| \| Domestic \| $6,368 \| $2,802 \| $4,918 \| \| Foreign \| 6,150 \| 3,392 \| (8) \| \| Income before provision for income taxes \| $12,518 \| $6,194 \| $4,91… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#2 `META_FY2021_2021-12-31:502`** (cited, gold #1)

````text
Item 8.Financial Statements and Supplementary Data > Note 14. Income Taxes (table)
|  | Year Ended December 31, |  |  |
|---|---|---|---|
|  | 2021 | 2020 | 2019 |
| Domestic | $43,669 | $24,233 | $5,317 |
| Foreign | 3,615 | 8,947 | 19,495 |
| Income before provision for income taxes | $47,284 | $33,180 | $24,812 |
````

**#6 `META_FY2016_2016-12-31:404`** (cited, gold #2)

````text
Item 8. Financial Statements and Supplementary Data > Share-based Compensation Plans (table)
|  | Year Ended December 31, |  |  |
|---|---|---|---|
|  | 2016 | 2015 | 2014 |
| Domestic | $6,368 | $2,802 | $4,918 |
| Foreign | 6,150 | 3,392 | (8) |
| Income before provision for income taxes | $12,518 | $6,194 | $4,910 |
````

</details>

RQ2 citation match (section level): `cited=[('META', 'Item 8')] gold=[(None, 'Item 8')]`

**System C guardrail** (judge `gpt-5.4`): numerical claims 6, verified 6, ungrounded 0, uncited 0, derived 1; sentence verdicts: supported 0, partial 0, unsupported 0, unchecked 0.


<details><summary>Guardrail sentence verdicts</summary>

| sentence | verdict | judge reason |
|---|---|---|
| Meta Platforms' foreign income before provision for income taxes increased from $6,150 million in fiscal year 2016 to $3,615 million in fiscal year 2021 [META FY2016, Item 8, META_FY2016_2016-12-31:404] [META FY2021, Item 8, META_FY2021_2021-12-31:502]. | None |  |
| The percentage change from 2016 to 2021 was -41.2%, calculated as (($3,615 - $6,150) / $6,150) × 100 [META FY2016, Item 8, META_FY2016_2016-12-31:404] [META FY2021, Item 8, META_FY2021_2021-12-31:502]. | None |  |

</details>

### System C v2 (agentic multi-hop + XBRL)

Model: `gpt-5.4`. Hops: 1. Chunks retrieved: 8, cited: 2.

**Generated answer**

> Meta Platforms' foreign income before provision for income taxes increased from $6,150 million in fiscal year 2016 to $3,615 million in fiscal year 2021 [META FY2016, Item 8, META_FY2016_2016-12-31:404] [META FY2021, Item 8, META_FY2021_2021-12-31:502].  
> The percentage change from 2016 to 2021 was (($3,615 - $6,150) / $6,150) × 100 = -41.2%, which means foreign income before provision for income taxes decreased by 41.2% [META FY2016, Item 8, META_FY2016_2016-12-31:404] [META FY2021, Item 8, META_FY2021_2021-12-31:502].

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `F-META-2016` | SEC XBRL Reported Financials (financials.csv) |  |  | fiscal_year,fiscal_year_end,Revenue,NetIncome,OperatingIncome,TotalAssets,TotalLiabilities,StockholdersEquity,CashAndEquivalents,OperatingCashFlow,EPSDiluted 2016,2016-12-31,27638000000,10217000000,12427000000,6496100000… |
| 2 | `F-META-2021` | SEC XBRL Reported Financials (financials.csv) |  |  | fiscal_year,fiscal_year_end,Revenue,NetIncome,OperatingIncome,TotalAssets,TotalLiabilities,StockholdersEquity,CashAndEquivalents,OperatingCashFlow,EPSDiluted 2021,2021-12-31,117929000000,39370000000,46753000000,165987000… |
| 3 | `META_FY2016_2016-12-31:412` | Item 8 › Share-based Compensation Plans |  |  | Our foreign income before provision for income taxes of $6.15 billion resulted in certain of our foreign jurisdictions moving from a position of having cumulative losses to cumulative earnings. In accordance with ASC 740… |
| 4 | `META_FY2021_2021-12-31:502` | Item 8 › Note 14. Income Taxes | ✓ | #1 | \| \| Year Ended December 31, \| \| \| \|---\|---\|---\|---\| \| \| 2021 \| 2020 \| 2019 \| \| Domestic \| $43,669 \| $24,233 \| $5,317 \| \| Foreign \| 3,615 \| 8,947 \| 19,495 \| \| Income before provision for income taxes \| $47,284 \| $33,180 \|… |
| 5 | `META_FY2016_2016-12-31:229` | Item 7 › Provision for income taxes |  |  | 2016 Compared to 2015. Our provision for income taxes in 2016 decreased $205 million, or 8%, compared to 2015, primarily due to the impact of the adoption of ASU 2016-09, and was partially offset by an increase in income… |
| 6 | `META_FY2021_2021-12-31:501` | Item 8 › Note 14. Income Taxes |  |  | The components of income before provision for income taxes are as follows (in millions): |
| 7 | `META_FY2021_2021-12-31:327` | Item 7 › Provision for income taxes |  |  | Our provision for income taxes in 2021 increased $3.88 billion, or 96%, compared to 2020, primarily due to an increase in income from operations and the effects of the tax election described below. Our effective tax rate… |
| 8 | `META_FY2016_2016-12-31:404` | Item 8 › Share-based Compensation Plans | ✓ | #2 | \| \| Year Ended December 31, \| \| \| \|---\|---\|---\|---\| \| \| 2016 \| 2015 \| 2014 \| \| Domestic \| $6,368 \| $2,802 \| $4,918 \| \| Foreign \| 6,150 \| 3,392 \| (8) \| \| Income before provision for income taxes \| $12,518 \| $6,194 \| $4,91… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#4 `META_FY2021_2021-12-31:502`** (cited, gold #1)

````text
Item 8.Financial Statements and Supplementary Data > Note 14. Income Taxes (table)
|  | Year Ended December 31, |  |  |
|---|---|---|---|
|  | 2021 | 2020 | 2019 |
| Domestic | $43,669 | $24,233 | $5,317 |
| Foreign | 3,615 | 8,947 | 19,495 |
| Income before provision for income taxes | $47,284 | $33,180 | $24,812 |
````

**#8 `META_FY2016_2016-12-31:404`** (cited, gold #2)

````text
Item 8. Financial Statements and Supplementary Data > Share-based Compensation Plans (table)
|  | Year Ended December 31, |  |  |
|---|---|---|---|
|  | 2016 | 2015 | 2014 |
| Domestic | $6,368 | $2,802 | $4,918 |
| Foreign | 6,150 | 3,392 | (8) |
| Income before provision for income taxes | $12,518 | $6,194 | $4,910 |
````

</details>

RQ2 citation match (section level): `cited=[('META', 'Item 8')] gold=[(None, 'Item 8')]`

**System C guardrail** (judge `gpt-5.4`): numerical claims 7, verified 7, ungrounded 0, uncited 0, derived 2; sentence verdicts: supported 0, partial 0, unsupported 0, unchecked 0.


<details><summary>Guardrail sentence verdicts</summary>

| sentence | verdict | judge reason |
|---|---|---|
| Meta Platforms' foreign income before provision for income taxes increased from $6,150 million in fiscal year 2016 to $3,615 million in fiscal year 2021 [META FY2016, Item 8, META_FY2016_2016-12-31:404] [META FY2021, Item 8, META_FY2021_2021-12-31:502]. | None |  |
| The percentage change from 2016 to 2021 was (($3,615 - $6,150) / $6,150) × 100 = -41.2%, which means foreign income before provision for income taxes decreased by 41.2% [META FY2016, Item 8, META_FY2016_2016-12-31:404] [META FY2021, Item 8, META_FY2021_2021-12-31:502]. | None |  |

</details>
