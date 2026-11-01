# gold-002: Multi-hop table (one filing)

[← all cases](../README.md) · company: Meta Platforms, Inc. (META) · fiscal year: 2023 · recipe `table` · hop `multi` · answer type `numeric` · scope `single_doc` · RQ2 category `quantitative_tabular`

## Gold QA

**Question**

> What percentage of Meta Platforms' total restructuring charges for 2023 was recorded under research and development?

**Gold answer**

> 57.76%

**Program**: `divide(1994, 3452)` → `0.5776361529548089`

**Gold numbers** (RQ2 numeric_accuracy targets): 57.76%

**Gold evidence**

1. `META_FY2023_2023-12-31` · Item 7.Management's Discussion and Analysis of Financial Condition and Results of Operations › Restructuring · table

   > | Research and development | 1,581 | 413 | — | 1,994 |

2. `META_FY2023_2023-12-31` · Item 7.Management's Discussion and Analysis of Financial Condition and Results of Operations › Restructuring · table

   > | Total | $2,506 | $1,170 | $(224) | $3,452 |

## Scorecard

| Metric | A (vanilla dense) | B (hybrid + rerank) | C v1 (adaptive multi-hop) | C v2 (agentic multi-hop + XBRL) |
|---|---|---|---|---|
| **Retrieval (RQ1)** | | | | |
| chunks retrieved | 10 | 5 | 6 | 6 |
| recall@5 | 0.00 | 1.00 | 1.00 | 1.00 |
| recall@all | 1.00 | 1.00 | 1.00 | 1.00 |
| complete@all | 1 | 1 | 1 | 1 |
| average precision (lexical) | 0.17 | 0.33 | 0.33 | 0.33 |
| gold evidence first rank | #1: 8, #2: 9 | #1: 3, #2: 3 | #1: 4, #2: 5 | #1: 4, #2: 5 |
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
| tokens | 1735 | 895 | 3783 | 3767 |
| cost (USD) | 0.0003 | 0.0002 | 0.0132 | 0.0129 |
| latency (s) | 2.0 | 6.6 | 6.8 | 6.4 |

Definitions: [README › Metrics](../README.md#metrics). `–` = not applicable (e.g. no gold number, no citations, no guardrail).

## System outputs

### System A (vanilla dense)

Model: `gpt-5.4-2026-03-05`. Hops: 1. Chunks retrieved: 10, cited: 1.

**Generated answer**

> Meta’s total 2023 restructuring charges were **$3,452 million**, and **$1,994 million** of that was recorded under **research and development** [9].
>
> So the percentage is:
>
> **1,994 / 3,452 ≈ 57.8%**
>
> Therefore, **about 57.8%** of Meta Platforms’ total 2023 restructuring charges was recorded under research and development [9].

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `META_FY2023_2023-12-31:309` | Item 7 › Restructuring |  |  | During 2023 and 2022, we recognized total pre-tax restructuring charges of $2.84 billion and $4.10 billion under our FoA segment, and $612 million and $515 million under our RL segment, respectively. See Note 3 — Restruc… |
| 2 | `META_FY2023_2023-12-31:369` | Item 7 › Research and development |  |  | Research and development expenses in 2023 increased $3.15 billion, or 9%, compared to 2022. The increase was primarily from higher payroll and related expenses driven by an increase in share-based compensation expenses. |
| 3 | `META_FY2023_2023-12-31:498` | Item 8 › 2023 Restructuring |  |  | \| \| Year Ended December 31, 2023 \| \|---\|---\| \| Research and development \| $422 \| \| Marketing and sales \| 308 \| \| General and administrative \| 467 \| \| Total (1) \| $1,197 \| |
| 4 | `META_FY2023_2023-12-31:503` | Item 8 › 2022 Restructuring |  |  | ____________________________________ (1)Relates to changes in estimates in our data center restructuring charges recorded during 2022. Total restructuring charges recorded under our FoA segment were $1.74 billion and $4.… |
| 5 | `META_FY2023_2023-12-31:307` | Item 7 › Restructuring |  |  | Beginning in 2022, we initiated several measures to pursue greater efficiency and to realign our business and strategic priorities. As of December 31, 2023, we have completed the data center initiatives and the employee … |
| 6 | `META_FY2023_2023-12-31:501` | Item 8 › 2022 Restructuring |  |  | In 2022, we initiated several measures to pursue greater efficiency and to realign our business and strategic priorities. These measures included a facilities consolidation strategy to sublease, early terminate, or aband… |
| 7 | `META_FY2023_2023-12-31:368` | Item 7 › Research and development |  |  | \| \| Year Ended December 31, \| \| \| \| \| \|---\|---\|---\|---\|---\|---\| \| \| 2023 \| 2022 \| 2021 \| 2023 vs 2022 % change \| 2022 vs 2021 % change \| \| \| (in millions, except percentages) \| \| \| \| \| \| Research and development \| $38,48… |
| 8 | `META_FY2023_2023-12-31:502` | Item 8 › 2022 Restructuring |  | #1 | \| \| Year Ended December 31, 2023 \| \| \| \| Year Ended December 31, 2022 \| \| \| \| \|---\|---\|---\|---\|---\|---\|---\|---\|---\| \| \| Facilities Consolidation \| Severance and Other Personnel Costs \| Data Center Assets (1) \| Total \| Fa… |
| 9 | `META_FY2023_2023-12-31:308` | Item 7 › Restructuring | ✓ | #1, #2 | \| \| Year Ended December 31, 2023 \| \| \| \| \|---\|---\|---\|---\|---\| \| \| Facilities Consolidation \| Severance and Other Personnel Costs \| Data Center Assets \| Total \| \| Cost of revenue \| $177 \| $— \| $(224) \| $(47) \| \| Research… |
| 10 | `META_FY2023_2023-12-31:367` | Item 7 › Cost of revenue |  |  | Cost of revenue in 2023 increased $710 million, or 3%, compared to 2022. The increase was primarily driven by higher operational expenses related to our data centers and technical infrastructure, partially offset by a de… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#8 `META_FY2023_2023-12-31:502`** (gold #1)

````text
Item 8.Financial Statements and Supplementary Data > 2022 Restructuring (table)
|  | Year Ended December 31, 2023 |  |  |  | Year Ended December 31, 2022 |  |  |  |
|---|---|---|---|---|---|---|---|---|
|  | Facilities Consolidation | Severance and Other Personnel Costs | Data Center Assets (1) | Total | Facilities Consolidation | Severance and Other Personnel Costs | Data Center Assets | Total |
| Cost of revenue | $177 | $— | $(224) | $(47) | $154 | $— | $1,341 | $1,495 |
| Research and development | 1,581 | (9) | — | 1,572 | 1,311 | 408 | — | 1,719 |
| Marketing and sales | 396 | (1) | — | 395 | 404 | 234 | — | 638 |
| General and administrative | 352 | (17) | — | 335 | 426 | 333 | — | 759 |
| Total | $2,506 | $(27) | $(224) | $2,255 | $2,295 | $975 | $1,341 | $4,611 |
````

**#9 `META_FY2023_2023-12-31:308`** (cited, gold #1, gold #2)

````text
Item 7.Management's Discussion and Analysis of Financial Condition and Results of Operations > Restructuring (table)
|  | Year Ended December 31, 2023 |  |  |  |
|---|---|---|---|---|
|  | Facilities Consolidation | Severance and Other Personnel Costs | Data Center Assets | Total |
| Cost of revenue | $177 | $— | $(224) | $(47) |
| Research and development | 1,581 | 413 | — | 1,994 |
| Marketing and sales | 396 | 307 | — | 703 |
| General and administrative | 352 | 450 | — | 802 |
| Total | $2,506 | $1,170 | $(224) | $3,452 |
````

</details>

RQ2 citation match (section level): `cited=[('META', 'Item 7')] gold=[(None, 'Item 7')]`

### System B (hybrid + rerank)

Model: `gpt-5.4-2026-03-05`. Hops: 1. Chunks retrieved: 5, cited: 1.

**Generated answer**

> Meta recorded total 2023 restructuring charges of **$3,452 million**, of which **$1,994 million** was under **research and development** [3].
>
> So the percentage is:
>
> **1,994 / 3,452 × 100 ≈ 57.8%** [3]
>
> **Answer: approximately 57.8%** [3]

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `META_FY2023_2023-12-31:499` | Item 8 › 2023 Restructuring |  |  | ____________________________ (1) Includes $101 million of share-based compensation expense recognized for the 2023 layoffs during the year ended December 31, 2023. The 2023 Restructuring charges recorded under our FoA se… |
| 2 | `META_FY2023_2023-12-31:498` | Item 8 › 2023 Restructuring |  |  | \| \| Year Ended December 31, 2023 \| \|---\|---\| \| Research and development \| $422 \| \| Marketing and sales \| 308 \| \| General and administrative \| 467 \| \| Total (1) \| $1,197 \| |
| 3 | `META_FY2023_2023-12-31:308` | Item 7 › Restructuring | ✓ | #1, #2 | \| \| Year Ended December 31, 2023 \| \| \| \| \|---\|---\|---\|---\|---\| \| \| Facilities Consolidation \| Severance and Other Personnel Costs \| Data Center Assets \| Total \| \| Cost of revenue \| $177 \| $— \| $(224) \| $(47) \| \| Research… |
| 4 | `META_FY2023_2023-12-31:497` | Item 8 › 2023 Restructuring |  |  | In March 2023, we announced three rounds of planned layoffs to further reduce our company size by approximately 10,000 employees across the Family of Apps (FoA) and Reality Labs (RL) segments (the 2023 Restructuring). Im… |
| 5 | `META_FY2023_2023-12-31:369` | Item 7 › Research and development |  |  | Research and development expenses in 2023 increased $3.15 billion, or 9%, compared to 2022. The increase was primarily from higher payroll and related expenses driven by an increase in share-based compensation expenses. |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#3 `META_FY2023_2023-12-31:308`** (cited, gold #1, gold #2)

````text
Item 7.Management's Discussion and Analysis of Financial Condition and Results of Operations > Restructuring (table)
|  | Year Ended December 31, 2023 |  |  |  |
|---|---|---|---|---|
|  | Facilities Consolidation | Severance and Other Personnel Costs | Data Center Assets | Total |
| Cost of revenue | $177 | $— | $(224) | $(47) |
| Research and development | 1,581 | 413 | — | 1,994 |
| Marketing and sales | 396 | 307 | — | 703 |
| General and administrative | 352 | 450 | — | 802 |
| Total | $2,506 | $1,170 | $(224) | $3,452 |
````

</details>

RQ2 citation match (section level): `cited=[('META', 'Item 7')] gold=[(None, 'Item 7')]`

### System C v1 (adaptive multi-hop)

Model: `gpt-5.4`. Hops: 1. Chunks retrieved: 6, cited: 1.

**Generated answer**

> Meta Platforms recorded total 2023 restructuring charges of $3,452 million, of which $1,994 million was under research and development, so research and development represented approximately 57.8% of total 2023 restructuring charges [META FY2023, Item 7, META_FY2023_2023-12-31:308].

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `META_FY2023_2023-12-31:503` | Item 8 › 2022 Restructuring |  |  | ____________________________________ (1)Relates to changes in estimates in our data center restructuring charges recorded during 2022. Total restructuring charges recorded under our FoA segment were $1.74 billion and $4.… |
| 2 | `META_FY2023_2023-12-31:309` | Item 7 › Restructuring |  |  | During 2023 and 2022, we recognized total pre-tax restructuring charges of $2.84 billion and $4.10 billion under our FoA segment, and $612 million and $515 million under our RL segment, respectively. See Note 3 — Restruc… |
| 3 | `META_FY2023_2023-12-31:498` | Item 8 › 2023 Restructuring |  |  | \| \| Year Ended December 31, 2023 \| \|---\|---\| \| Research and development \| $422 \| \| Marketing and sales \| 308 \| \| General and administrative \| 467 \| \| Total (1) \| $1,197 \| |
| 4 | `META_FY2023_2023-12-31:502` | Item 8 › 2022 Restructuring |  | #1 | \| \| Year Ended December 31, 2023 \| \| \| \| Year Ended December 31, 2022 \| \| \| \| \|---\|---\|---\|---\|---\|---\|---\|---\|---\| \| \| Facilities Consolidation \| Severance and Other Personnel Costs \| Data Center Assets (1) \| Total \| Fa… |
| 5 | `META_FY2023_2023-12-31:308` | Item 7 › Restructuring | ✓ | #1, #2 | \| \| Year Ended December 31, 2023 \| \| \| \| \|---\|---\|---\|---\|---\| \| \| Facilities Consolidation \| Severance and Other Personnel Costs \| Data Center Assets \| Total \| \| Cost of revenue \| $177 \| $— \| $(224) \| $(47) \| \| Research… |
| 6 | `META_FY2023_2023-12-31:307` | Item 7 › Restructuring |  |  | Beginning in 2022, we initiated several measures to pursue greater efficiency and to realign our business and strategic priorities. As of December 31, 2023, we have completed the data center initiatives and the employee … |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#4 `META_FY2023_2023-12-31:502`** (gold #1)

````text
Item 8.Financial Statements and Supplementary Data > 2022 Restructuring (table)
|  | Year Ended December 31, 2023 |  |  |  | Year Ended December 31, 2022 |  |  |  |
|---|---|---|---|---|---|---|---|---|
|  | Facilities Consolidation | Severance and Other Personnel Costs | Data Center Assets (1) | Total | Facilities Consolidation | Severance and Other Personnel Costs | Data Center Assets | Total |
| Cost of revenue | $177 | $— | $(224) | $(47) | $154 | $— | $1,341 | $1,495 |
| Research and development | 1,581 | (9) | — | 1,572 | 1,311 | 408 | — | 1,719 |
| Marketing and sales | 396 | (1) | — | 395 | 404 | 234 | — | 638 |
| General and administrative | 352 | (17) | — | 335 | 426 | 333 | — | 759 |
| Total | $2,506 | $(27) | $(224) | $2,255 | $2,295 | $975 | $1,341 | $4,611 |
````

**#5 `META_FY2023_2023-12-31:308`** (cited, gold #1, gold #2)

````text
Item 7.Management's Discussion and Analysis of Financial Condition and Results of Operations > Restructuring (table)
|  | Year Ended December 31, 2023 |  |  |  |
|---|---|---|---|---|
|  | Facilities Consolidation | Severance and Other Personnel Costs | Data Center Assets | Total |
| Cost of revenue | $177 | $— | $(224) | $(47) |
| Research and development | 1,581 | 413 | — | 1,994 |
| Marketing and sales | 396 | 307 | — | 703 |
| General and administrative | 352 | 450 | — | 802 |
| Total | $2,506 | $1,170 | $(224) | $3,452 |
````

</details>

RQ2 citation match (section level): `cited=[('META', 'Item 7')] gold=[(None, 'Item 7')]`

**System C guardrail** (judge `gpt-5.4`): numerical claims 3, verified 3, ungrounded 0, uncited 0, derived 1; sentence verdicts: supported 0, partial 0, unsupported 0, unchecked 0.


<details><summary>Guardrail sentence verdicts</summary>

| sentence | verdict | judge reason |
|---|---|---|
| Meta Platforms recorded total 2023 restructuring charges of $3,452 million, of which $1,994 million was under research and development, so research and development represented approximately 57.8% of total 2023 restructuring charges [META FY2023, Item 7, META_FY2023_2023-12-31:308]. | None |  |

</details>

### System C v2 (agentic multi-hop + XBRL)

Model: `gpt-5.4`. Hops: 1. Chunks retrieved: 6, cited: 1.

**Generated answer**

> Meta Platforms recorded total 2023 restructuring charges of $3,452 million, of which $1,994 million was under research and development, so research and development represented approximately 57.8% of total 2023 restructuring charges [META FY2023, Item 7, META_FY2023_2023-12-31:308].

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `META_FY2023_2023-12-31:503` | Item 8 › 2022 Restructuring |  |  | ____________________________________ (1)Relates to changes in estimates in our data center restructuring charges recorded during 2022. Total restructuring charges recorded under our FoA segment were $1.74 billion and $4.… |
| 2 | `META_FY2023_2023-12-31:309` | Item 7 › Restructuring |  |  | During 2023 and 2022, we recognized total pre-tax restructuring charges of $2.84 billion and $4.10 billion under our FoA segment, and $612 million and $515 million under our RL segment, respectively. See Note 3 — Restruc… |
| 3 | `META_FY2023_2023-12-31:498` | Item 8 › 2023 Restructuring |  |  | \| \| Year Ended December 31, 2023 \| \|---\|---\| \| Research and development \| $422 \| \| Marketing and sales \| 308 \| \| General and administrative \| 467 \| \| Total (1) \| $1,197 \| |
| 4 | `META_FY2023_2023-12-31:502` | Item 8 › 2022 Restructuring |  | #1 | \| \| Year Ended December 31, 2023 \| \| \| \| Year Ended December 31, 2022 \| \| \| \| \|---\|---\|---\|---\|---\|---\|---\|---\|---\| \| \| Facilities Consolidation \| Severance and Other Personnel Costs \| Data Center Assets (1) \| Total \| Fa… |
| 5 | `META_FY2023_2023-12-31:308` | Item 7 › Restructuring | ✓ | #1, #2 | \| \| Year Ended December 31, 2023 \| \| \| \| \|---\|---\|---\|---\|---\| \| \| Facilities Consolidation \| Severance and Other Personnel Costs \| Data Center Assets \| Total \| \| Cost of revenue \| $177 \| $— \| $(224) \| $(47) \| \| Research… |
| 6 | `META_FY2023_2023-12-31:307` | Item 7 › Restructuring |  |  | Beginning in 2022, we initiated several measures to pursue greater efficiency and to realign our business and strategic priorities. As of December 31, 2023, we have completed the data center initiatives and the employee … |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#4 `META_FY2023_2023-12-31:502`** (gold #1)

````text
Item 8.Financial Statements and Supplementary Data > 2022 Restructuring (table)
|  | Year Ended December 31, 2023 |  |  |  | Year Ended December 31, 2022 |  |  |  |
|---|---|---|---|---|---|---|---|---|
|  | Facilities Consolidation | Severance and Other Personnel Costs | Data Center Assets (1) | Total | Facilities Consolidation | Severance and Other Personnel Costs | Data Center Assets | Total |
| Cost of revenue | $177 | $— | $(224) | $(47) | $154 | $— | $1,341 | $1,495 |
| Research and development | 1,581 | (9) | — | 1,572 | 1,311 | 408 | — | 1,719 |
| Marketing and sales | 396 | (1) | — | 395 | 404 | 234 | — | 638 |
| General and administrative | 352 | (17) | — | 335 | 426 | 333 | — | 759 |
| Total | $2,506 | $(27) | $(224) | $2,255 | $2,295 | $975 | $1,341 | $4,611 |
````

**#5 `META_FY2023_2023-12-31:308`** (cited, gold #1, gold #2)

````text
Item 7.Management's Discussion and Analysis of Financial Condition and Results of Operations > Restructuring (table)
|  | Year Ended December 31, 2023 |  |  |  |
|---|---|---|---|---|
|  | Facilities Consolidation | Severance and Other Personnel Costs | Data Center Assets | Total |
| Cost of revenue | $177 | $— | $(224) | $(47) |
| Research and development | 1,581 | 413 | — | 1,994 |
| Marketing and sales | 396 | 307 | — | 703 |
| General and administrative | 352 | 450 | — | 802 |
| Total | $2,506 | $1,170 | $(224) | $3,452 |
````

</details>

RQ2 citation match (section level): `cited=[('META', 'Item 7')] gold=[(None, 'Item 7')]`

**System C guardrail** (judge `gpt-5.4`): numerical claims 3, verified 3, ungrounded 0, uncited 0, derived 1; sentence verdicts: supported 0, partial 0, unsupported 0, unchecked 0.


<details><summary>Guardrail sentence verdicts</summary>

| sentence | verdict | judge reason |
|---|---|---|
| Meta Platforms recorded total 2023 restructuring charges of $3,452 million, of which $1,994 million was under research and development, so research and development represented approximately 57.8% of total 2023 restructuring charges [META FY2023, Item 7, META_FY2023_2023-12-31:308]. | None |  |

</details>
