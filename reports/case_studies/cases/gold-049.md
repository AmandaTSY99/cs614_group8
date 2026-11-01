# gold-049: Single-hop table

[← all cases](../README.md) · company: Tesla, Inc. (TSLA) · fiscal year: 2021 · recipe `table` · hop `single` · answer type `numeric` · scope `single_doc` · RQ2 category `quantitative_tabular`

## Gold QA

**Question**

> What was the percentage increase in Tesla's foreign current income tax provision from fiscal year 2020 to fiscal year 2021?

**Gold answer**

> 238.31%

**Program**: `subtract(839, 248), divide(#0, 248), multiply(#1, 100)` → `238.30645161290326`

**Gold numbers** (RQ2 numeric_accuracy targets): 238.31%

**Gold evidence**

1. `TSLA_FY2021_2021-12-31` · ITEM 8. FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA › Note 14 – Income Taxes · table

   > | Foreign | 839 | 248 | 86 |

## Scorecard

| Metric | A (vanilla dense) | B (hybrid + rerank) | C v1 (adaptive multi-hop) | C v2 (agentic multi-hop + XBRL) |
|---|---|---|---|---|
| **Retrieval (RQ1)** | | | | |
| chunks retrieved | 10 | 5 | 6 | 7 |
| recall@5 | 0.00 | 1.00 | 0.00 | 0.00 |
| recall@all | 1.00 | 1.00 | 1.00 | 1.00 |
| complete@all | 1 | 1 | 1 | 1 |
| average precision (lexical) | 0.17 | 0.25 | 0.17 | 0.14 |
| gold evidence first rank | #1: 6 | #1: 4 | #1: 6 | #1: 7 |
| **Answer (RQ3 string match)** | | | | |
| numeric_correct | ✓ | ✓ | ✓ | ✓ |
| keypoint_recall | – | – | – | – |
| **Answer & citations (RQ2)** | | | | |
| numeric_accuracy | 1.00 | 1.00 | 1.00 | 1.00 |
| citation precision | 1.00 | 1.00 | 1.00 | 1.00 |
| citation recall | 1.00 | 1.00 | 1.00 | 1.00 |
| citation F1 | 1.00 | 1.00 | 1.00 | 1.00 |
| has a citation | 1 | 1 | 1 | 1 |
| grounding error rate | – | – | 1.00 | 1.00 |
| **Cost (RQ3)** | | | | |
| retrieval hops | 1 | 1 | 1 | 1 |
| tokens | 2251 | 1276 | 6434 | 7006 |
| cost (USD) | 0.0004 | 0.0002 | 0.0206 | 0.0229 |
| latency (s) | 1.6 | 6.5 | 9.4 | 8.9 |

Definitions: [README › Metrics](../README.md#metrics). `–` = not applicable (e.g. no gold number, no citations, no guardrail).

## System outputs

### System A (vanilla dense)

Model: `gpt-5.4-2026-03-05`. Hops: 1. Chunks retrieved: 10, cited: 1.

**Generated answer**

> Tesla’s foreign current income tax provision increased from **$248 million in 2020** to **$839 million in 2021** [6].
>
> Percentage increase = \(\frac{839 - 248}{248} \times 100\) = **about 238.3%** [6].

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `TSLA_FY2021_2021-12-31:246` | Item 7 › Provision for Income Taxes |  |  | Our provision for income taxes increased by $407 million, or 139%, in the year ended December 31, 2021 as compared to the year ended December 31, 2020, primarily due to the increases in taxable profits within our foreign… |
| 2 | `TSLA_FY2021_2021-12-31:494` | Item 8 › Note 14 – Income Taxes |  |  | A provision for income taxes of $699 million, $292 million and $110 million has been recognized for the years ended December 31, 2021, 2020 and 2019, respectively, related primarily to our subsidiaries located outside of… |
| 3 | `TSLA_FY2021_2021-12-31:245` | Item 7 › Provision for Income Taxes |  |  | \| \| Year Ended December 31, \| \| 2021 vs. 2020 Change \| \| 2020 vs. 2019 Change \| \| \| \|---\|---\|---\|---\|---\|---\|---\|---\| \| (Dollars in millions) \| 2021 \| 2020 \| 2019 \| $% \| \| $% \| \| \| Provision for income taxes \| $699 \| $29… |
| 4 | `TSLA_FY2021_2021-12-31:503` | Item 8 › Note 14 – Income Taxes |  |  | \| \| Year Ended December 31, \| \| \| \|---\|---\|---\|---\| \| \| 2021 \| 2020 \| 2019 \| \| Tax at statutory federal rate \| $1,332 \| $242 \| $(139) \| \| State tax, net of federal benefit \| 6 \| 4 \| 5 \| \| Nondeductible executive compensa… |
| 5 | `TSLA_FY2021_2021-12-31:495` | Item 8 › Note 14 – Income Taxes |  |  | \| \| Year Ended December 31, \| \| \| \|---\|---\|---\|---\| \| \| 2021 \| 2020 \| 2019 \| \| Domestic \| $(130) \| $(198) \| $(287) \| \| Noncontrolling interest and redeemable noncontrolling interest \| 125 \| 141 \| 87 \| \| Foreign \| 6,348 \|… |
| 6 | `TSLA_FY2021_2021-12-31:497` | Item 8 › Note 14 – Income Taxes | ✓ | #1 | \| \| Year Ended December 31, \| \| \| \|---\|---\|---\|---\| \| \| 2021 \| 2020 \| 2019 \| \| Current: \| \| \| \| \| Federal \| $— \| $— \| $— \| \| State \| 9 \| 4 \| 5 \| \| Foreign \| 839 \| 248 \| 86 \| \| Total current \| 848 \| 252 \| 91 \| \| Deferred:… |
| 7 | `TSLA_FY2021_2021-12-31:501` | Item 8 › Note 14 – Income Taxes |  |  | As of December 31, 2021, we recorded a valuation allowance of $9.07 billion for the portion of the deferred tax asset that we do not expect to be realized. The valuation allowance on our net deferred taxes increased by $… |
| 8 | `TSLA_FY2021_2021-12-31:542` | Item 8 › Note 18 – Segment Reporting and Information about Geographic Areas |  |  | \| \| December 31, \| December 31, \| \|---\|---\|---\| \| \| 2021 \| 2020 \| \| United States \| $19,026 \| $15,989 \| \| Germany \| 2,606 \| 894 \| \| China \| 2,415 \| 1,479 \| \| Other International \| 602 \| 364 \| \| Total \| $24,649 \| $18,726 … |
| 9 | `TSLA_FY2021_2021-12-31:218` | Item 7 › Revenues |  |  | \| \| Year Ended December 31, \| \| 2021 vs. 2020 Change \| \| 2020 vs. 2019 Change \| \| \| \|---\|---\|---\|---\|---\|---\|---\|---\| \| (Dollars in millions) \| 2021 \| 2020 \| 2019 \| $% \| \| $% \| \| \| Automotive sales \| $44,125 \| $24,604 \| … |
| 10 | `TSLA_FY2021_2021-12-31:496` | Item 8 › Note 14 – Income Taxes |  |  | The components of the provision for income taxes for the years ended December 31, 2021, 2020 and 2019 consisted of the following (in millions): |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#6 `TSLA_FY2021_2021-12-31:497`** (cited, gold #1)

````text
ITEM 8. FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA > Note 14 – Income Taxes (table)
|  | Year Ended December 31, |  |  |
|---|---|---|---|
|  | 2021 | 2020 | 2019 |
| Current: |  |  |  |
| Federal | $— | $— | $— |
| State | 9 | 4 | 5 |
| Foreign | 839 | 248 | 86 |
| Total current | 848 | 252 | 91 |
| Deferred: |  |  |  |
| Federal | — | — | (4) |
| State | — | — | — |
| Foreign | (149) | 40 | 23 |
| Total deferred | (149) | 40 | 19 |
| Total provision for income taxes | $699 | $292 | $110 |
````

</details>

RQ2 citation match (section level): `cited=[('TSLA', 'Item 8')] gold=[(None, 'Item 8')]`

### System B (hybrid + rerank)

Model: `gpt-5.4-2026-03-05`. Hops: 1. Chunks retrieved: 5, cited: 1.

**Generated answer**

> Tesla’s foreign current income tax provision increased from $248 million in 2020 to $839 million in 2021 [4].
>
> Percentage increase = \(\frac{839 - 248}{248} \times 100 \approx 238.3\%\) [4]
>
> So, the increase was approximately **238%** [4].

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `TSLA_FY2021_2021-12-31:246` | Item 7 › Provision for Income Taxes |  |  | Our provision for income taxes increased by $407 million, or 139%, in the year ended December 31, 2021 as compared to the year ended December 31, 2020, primarily due to the increases in taxable profits within our foreign… |
| 2 | `TSLA_FY2021_2021-12-31:229` | Item 7 › Cost of Revenues and Gross Margin |  |  | Cost of automotive leasing revenue increased $415 million, or 74%, in the year ended December 31, 2021 as compared to the year ended December 31, 2020, primarily due to an increase in cumulative vehicles under our direct… |
| 3 | `TSLA_FY2021_2021-12-31:245` | Item 7 › Provision for Income Taxes |  |  | \| \| Year Ended December 31, \| \| 2021 vs. 2020 Change \| \| 2020 vs. 2019 Change \| \| \| \|---\|---\|---\|---\|---\|---\|---\|---\| \| (Dollars in millions) \| 2021 \| 2020 \| 2019 \| $% \| \| $% \| \| \| Provision for income taxes \| $699 \| $29… |
| 4 | `TSLA_FY2021_2021-12-31:497` | Item 8 › Note 14 – Income Taxes | ✓ | #1 | \| \| Year Ended December 31, \| \| \| \|---\|---\|---\|---\| \| \| 2021 \| 2020 \| 2019 \| \| Current: \| \| \| \| \| Federal \| $— \| $— \| $— \| \| State \| 9 \| 4 \| 5 \| \| Foreign \| 839 \| 248 \| 86 \| \| Total current \| 848 \| 252 \| 91 \| \| Deferred:… |
| 5 | `TSLA_FY2021_2021-12-31:503` | Item 8 › Note 14 – Income Taxes |  |  | \| \| Year Ended December 31, \| \| \| \|---\|---\|---\|---\| \| \| 2021 \| 2020 \| 2019 \| \| Tax at statutory federal rate \| $1,332 \| $242 \| $(139) \| \| State tax, net of federal benefit \| 6 \| 4 \| 5 \| \| Nondeductible executive compensa… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#4 `TSLA_FY2021_2021-12-31:497`** (cited, gold #1)

````text
ITEM 8. FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA > Note 14 – Income Taxes (table)
|  | Year Ended December 31, |  |  |
|---|---|---|---|
|  | 2021 | 2020 | 2019 |
| Current: |  |  |  |
| Federal | $— | $— | $— |
| State | 9 | 4 | 5 |
| Foreign | 839 | 248 | 86 |
| Total current | 848 | 252 | 91 |
| Deferred: |  |  |  |
| Federal | — | — | (4) |
| State | — | — | — |
| Foreign | (149) | 40 | 23 |
| Total deferred | (149) | 40 | 19 |
| Total provision for income taxes | $699 | $292 | $110 |
````

</details>

RQ2 citation match (section level): `cited=[('TSLA', 'Item 8')] gold=[(None, 'Item 8')]`

### System C v1 (adaptive multi-hop)

Model: `gpt-5.4`. Hops: 1. Chunks retrieved: 6, cited: 1.

**Generated answer**

> Tesla's foreign current income tax provision increased from $248 million in fiscal year 2020 to $839 million in fiscal year 2021, an increase of approximately 238.3% [TSLA FY2021, Item 8, TSLA_FY2021_2021-12-31:497] [TSLA FY2021, Item 8, TSLA_FY2021_2021-12-31:497].
>
> > [Guardrail Audit Warning]: Manual verification required; these numerical figures could not be matched in their cited chunks: 248, 839; 1 sentence(s) are not supported by their cited chunks.

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `TSLA_FY2021_2021-12-31:494` | Item 8 › Note 14 – Income Taxes |  |  | A provision for income taxes of $699 million, $292 million and $110 million has been recognized for the years ended December 31, 2021, 2020 and 2019, respectively, related primarily to our subsidiaries located outside of… |
| 2 | `TSLA_FY2021_2021-12-31:246` | Item 7 › Provision for Income Taxes |  |  | Our provision for income taxes increased by $407 million, or 139%, in the year ended December 31, 2021 as compared to the year ended December 31, 2020, primarily due to the increases in taxable profits within our foreign… |
| 3 | `TSLA_FY2021_2021-12-31:245` | Item 7 › Provision for Income Taxes |  |  | \| \| Year Ended December 31, \| \| 2021 vs. 2020 Change \| \| 2020 vs. 2019 Change \| \| \| \|---\|---\|---\|---\|---\|---\|---\|---\| \| (Dollars in millions) \| 2021 \| 2020 \| 2019 \| $% \| \| $% \| \| \| Provision for income taxes \| $699 \| $29… |
| 4 | `TSLA_FY2021_2021-12-31:503` | Item 8 › Note 14 – Income Taxes |  |  | \| \| Year Ended December 31, \| \| \| \|---\|---\|---\|---\| \| \| 2021 \| 2020 \| 2019 \| \| Tax at statutory federal rate \| $1,332 \| $242 \| $(139) \| \| State tax, net of federal benefit \| 6 \| 4 \| 5 \| \| Nondeductible executive compensa… |
| 5 | `TSLA_FY2021_2021-12-31:495` | Item 8 › Note 14 – Income Taxes |  |  | \| \| Year Ended December 31, \| \| \| \|---\|---\|---\|---\| \| \| 2021 \| 2020 \| 2019 \| \| Domestic \| $(130) \| $(198) \| $(287) \| \| Noncontrolling interest and redeemable noncontrolling interest \| 125 \| 141 \| 87 \| \| Foreign \| 6,348 \|… |
| 6 | `TSLA_FY2021_2021-12-31:497` | Item 8 › Note 14 – Income Taxes | ✓ | #1 | \| \| Year Ended December 31, \| \| \| \|---\|---\|---\|---\| \| \| 2021 \| 2020 \| 2019 \| \| Current: \| \| \| \| \| Federal \| $— \| $— \| $— \| \| State \| 9 \| 4 \| 5 \| \| Foreign \| 839 \| 248 \| 86 \| \| Total current \| 848 \| 252 \| 91 \| \| Deferred:… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#6 `TSLA_FY2021_2021-12-31:497`** (cited, gold #1)

````text
ITEM 8. FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA > Note 14 – Income Taxes (table)
|  | Year Ended December 31, |  |  |
|---|---|---|---|
|  | 2021 | 2020 | 2019 |
| Current: |  |  |  |
| Federal | $— | $— | $— |
| State | 9 | 4 | 5 |
| Foreign | 839 | 248 | 86 |
| Total current | 848 | 252 | 91 |
| Deferred: |  |  |  |
| Federal | — | — | (4) |
| State | — | — | — |
| Foreign | (149) | 40 | 23 |
| Total deferred | (149) | 40 | 19 |
| Total provision for income taxes | $699 | $292 | $110 |
````

</details>

RQ2 citation match (section level): `cited=[('TSLA', 'Item 8')] gold=[(None, 'Item 8')]`

**System C guardrail** (judge `gpt-5.4`): numerical claims 3, verified 1, ungrounded 2, uncited 0, derived 1; sentence verdicts: supported 0, partial 0, unsupported 0, unchecked 0.

- ungrounded numbers: 248, 839

<details><summary>Guardrail sentence verdicts</summary>

| sentence | verdict | judge reason |
|---|---|---|
| Tesla's foreign current income tax provision increased from $248 million in fiscal year 2020 to $839 million in fiscal year 2021, an increase of approximately 238.3% [TSLA FY2021, Item 8, TSLA_FY2021_2021-12-31:497] [TSLA FY2021, Item 8, TSLA_FY2021_2021-12-31:497]. | None |  |

</details>

### System C v2 (agentic multi-hop + XBRL)

Model: `gpt-5.4`. Hops: 1. Chunks retrieved: 7, cited: 1.

**Generated answer**

> Tesla's foreign current income tax provision increased from $248 million in 2020 to $839 million in 2021, an increase of approximately 238.3% [TSLA FY2021, Item 8, TSLA_FY2021_2021-12-31:497] [TSLA FY2021, Item 8, TSLA_FY2021_2021-12-31:497].
>
> > [Guardrail Audit Warning]: Manual verification required; these numerical figures could not be matched in their cited chunks: 248, 839; 1 sentence(s) are not supported by their cited chunks.

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `F-TSLA-2021` | SEC XBRL Reported Financials (financials.csv) |  |  | fiscal_year,fiscal_year_end,Revenue,NetIncome,OperatingIncome,TotalAssets,TotalLiabilities,StockholdersEquity,CashAndEquivalents,OperatingCashFlow,EPSDiluted 2021,2021-12-31,53823000000,5519000000,6523000000,62131000000,… |
| 2 | `TSLA_FY2021_2021-12-31:494` | Item 8 › Note 14 – Income Taxes |  |  | A provision for income taxes of $699 million, $292 million and $110 million has been recognized for the years ended December 31, 2021, 2020 and 2019, respectively, related primarily to our subsidiaries located outside of… |
| 3 | `TSLA_FY2021_2021-12-31:246` | Item 7 › Provision for Income Taxes |  |  | Our provision for income taxes increased by $407 million, or 139%, in the year ended December 31, 2021 as compared to the year ended December 31, 2020, primarily due to the increases in taxable profits within our foreign… |
| 4 | `TSLA_FY2021_2021-12-31:503` | Item 8 › Note 14 – Income Taxes |  |  | \| \| Year Ended December 31, \| \| \| \|---\|---\|---\|---\| \| \| 2021 \| 2020 \| 2019 \| \| Tax at statutory federal rate \| $1,332 \| $242 \| $(139) \| \| State tax, net of federal benefit \| 6 \| 4 \| 5 \| \| Nondeductible executive compensa… |
| 5 | `TSLA_FY2021_2021-12-31:245` | Item 7 › Provision for Income Taxes |  |  | \| \| Year Ended December 31, \| \| 2021 vs. 2020 Change \| \| 2020 vs. 2019 Change \| \| \| \|---\|---\|---\|---\|---\|---\|---\|---\| \| (Dollars in millions) \| 2021 \| 2020 \| 2019 \| $% \| \| $% \| \| \| Provision for income taxes \| $699 \| $29… |
| 6 | `TSLA_FY2021_2021-12-31:495` | Item 8 › Note 14 – Income Taxes |  |  | \| \| Year Ended December 31, \| \| \| \|---\|---\|---\|---\| \| \| 2021 \| 2020 \| 2019 \| \| Domestic \| $(130) \| $(198) \| $(287) \| \| Noncontrolling interest and redeemable noncontrolling interest \| 125 \| 141 \| 87 \| \| Foreign \| 6,348 \|… |
| 7 | `TSLA_FY2021_2021-12-31:497` | Item 8 › Note 14 – Income Taxes | ✓ | #1 | \| \| Year Ended December 31, \| \| \| \|---\|---\|---\|---\| \| \| 2021 \| 2020 \| 2019 \| \| Current: \| \| \| \| \| Federal \| $— \| $— \| $— \| \| State \| 9 \| 4 \| 5 \| \| Foreign \| 839 \| 248 \| 86 \| \| Total current \| 848 \| 252 \| 91 \| \| Deferred:… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#7 `TSLA_FY2021_2021-12-31:497`** (cited, gold #1)

````text
ITEM 8. FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA > Note 14 – Income Taxes (table)
|  | Year Ended December 31, |  |  |
|---|---|---|---|
|  | 2021 | 2020 | 2019 |
| Current: |  |  |  |
| Federal | $— | $— | $— |
| State | 9 | 4 | 5 |
| Foreign | 839 | 248 | 86 |
| Total current | 848 | 252 | 91 |
| Deferred: |  |  |  |
| Federal | — | — | (4) |
| State | — | — | — |
| Foreign | (149) | 40 | 23 |
| Total deferred | (149) | 40 | 19 |
| Total provision for income taxes | $699 | $292 | $110 |
````

</details>

RQ2 citation match (section level): `cited=[('TSLA', 'Item 8')] gold=[(None, 'Item 8')]`

**System C guardrail** (judge `gpt-5.4`): numerical claims 3, verified 1, ungrounded 2, uncited 0, derived 1; sentence verdicts: supported 0, partial 0, unsupported 0, unchecked 0.

- ungrounded numbers: 248, 839

<details><summary>Guardrail sentence verdicts</summary>

| sentence | verdict | judge reason |
|---|---|---|
| Tesla's foreign current income tax provision increased from $248 million in 2020 to $839 million in 2021, an increase of approximately 238.3% [TSLA FY2021, Item 8, TSLA_FY2021_2021-12-31:497] [TSLA FY2021, Item 8, TSLA_FY2021_2021-12-31:497]. | None |  |

</details>
