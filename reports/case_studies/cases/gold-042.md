# gold-042: Multi-hop table (one filing)

[← all cases](../README.md) · company: Meta Platforms, Inc. (META) · fiscal year: 2024 · recipe `table` · hop `multi` · answer type `numeric` · scope `single_doc` · RQ2 category `quantitative_tabular`

## Gold QA

**Question**

> In Meta Platforms' fiscal year 2024, what percentage of the total gross unrecognized tax benefits at the end of the period was attributable to increases related to current year tax positions?

**Gold answer**

> 19.05%

**Program**: `divide(2882, 15131), multiply(#0, 100)` → `19.04698962395083`

**Gold numbers** (RQ2 numeric_accuracy targets): 19.05%

**Gold evidence**

1. `META_FY2024_2024-12-31` · Item 8.Financial Statements and Supplementary Data › Note 15. Income Taxes · table

   > Increases related to current year tax positions | 2,882 | 1,204 | 1,166 |

2. `META_FY2024_2024-12-31` · Item 8.Financial Statements and Supplementary Data › Note 15. Income Taxes · table

   > Gross unrecognized tax benefits ‑ end of period | $15,131 | $11,666 | $10,757 |

## Scorecard

| Metric | A (vanilla dense) | B (hybrid + rerank) | C v1 (adaptive multi-hop) | C v2 (agentic multi-hop + XBRL) |
|---|---|---|---|---|
| **Retrieval (RQ1)** | | | | |
| chunks retrieved | 10 | 5 | 8 | 8 |
| recall@5 | 1.00 | 1.00 | 1.00 | 1.00 |
| recall@all | 1.00 | 1.00 | 1.00 | 1.00 |
| complete@all | 1 | 1 | 1 | 1 |
| average precision (lexical) | 1.00 | 1.00 | 0.50 | 1.00 |
| gold evidence first rank | #1: 1, #2: 1 | #1: 1, #2: 1 | #1: 2, #2: 2 | #1: 1, #2: 1 |
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
| retrieval hops | 1 | 1 | 3 | 3 |
| tokens | 2342 | 1376 | 10338 | 10292 |
| cost (USD) | 0.0004 | 0.0002 | 0.0391 | 0.0389 |
| latency (s) | 1.9 | 6.9 | 20.1 | 21.0 |

Definitions: [README › Metrics](../README.md#metrics). `–` = not applicable (e.g. no gold number, no citations, no guardrail).

## System outputs

### System A (vanilla dense)

Model: `gpt-5.4-2026-03-05`. Hops: 1. Chunks retrieved: 10, cited: 1.

**Generated answer**

> In FY2024, increases related to current year tax positions were **$2,882 million**, and total gross unrecognized tax benefits at the end of the period were **$15,131 million** [1].
>
> So the percentage is:
>
> \[
> \frac{2,882}{15,131} \times 100 \approx 19.0\%
> \]
>
> **Answer: approximately 19.0%** [1]

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `META_FY2024_2024-12-31:599` | Item 8 › Note 15. Income Taxes | ✓ | #1, #2 | \| \| Year Ended December 31, \| \| \| \|---\|---\|---\|---\| \| \| 2024 \| 2023 \| 2022 \| \| Gross unrecognized tax benefits ‑ beginning of period \| $11,666 \| $10,757 \| $9,807 \| \| Increases related to prior year tax positions \| 685 \| … |
| 2 | `META_FY2024_2024-12-31:383` | Item 7 › Provision for income taxes |  |  | Unrecognized Tax Benefits. As of December 31, 2024, we had net uncertain tax positions of $9.99 billion which was included in long-term income taxes on our consolidated balance sheets. These unrecognized tax benefits wer… |
| 3 | `META_FY2024_2024-12-31:600` | Item 8 › Note 15. Income Taxes |  |  | These unrecognized tax benefits were primarily accrued for the uncertainties with our research tax credits and transfer pricing with our foreign subsidiaries, which include licensing of intellectual property, providing s… |
| 4 | `META_FY2024_2024-12-31:595` | Item 8 › Note 15. Income Taxes |  |  | \| \| Year Ended December 31, \| \| \| \|---\|---\|---\|---\| \| \| 2024 \| 2023 \| 2022 \| \| U.S. federal statutory income tax rate \| 21.0% \| 21.0% \| 21.0% \| \| State income taxes, net of federal benefit \| 0.7 \| 1.1 \| 1.0 \| \| Share-bas… |
| 5 | `META_FY2024_2024-12-31:379` | Item 7 › Provision for income taxes |  |  | \| \| Year Ended December 31, \| \| \| \| \| \|---\|---\|---\|---\|---\|---\| \| \| 2024 \| 2023 \| 2022 \| 2024 vs 2023 % change \| 2023 vs 2022 % change \| \| \| (in millions, except percentages) \| \| \| \| \| \| Provision for income taxes \| $8,3… |
| 6 | `META_FY2024_2024-12-31:605` | Item 8 › Note 15. Income Taxes |  |  | We have previously accrued an estimated unrecognized tax benefit consistent with the guidance in ASC 740, Income Taxes (ASC 740), that is lower than the potential additional federal tax liability from the positions taken… |
| 7 | `META_FY2024_2024-12-31:593` | Item 8 › Note 15. Income Taxes |  |  | \| \| Year Ended December 31, \| \| \| \|---\|---\|---\|---\| \| \| 2024 \| 2023 \| 2022 \| \| Current: \| \| \| \| \| Federal \| $9,569 \| $4,934 \| $6,094 \| \| State \| 775 \| 577 \| 874 \| \| Foreign \| 2,696 \| 2,688 \| 1,928 \| \| Total current tax e… |
| 8 | `META_FY2024_2024-12-31:591` | Item 8 › Note 15. Income Taxes |  |  | \| \| Year Ended December 31, \| \| \| \|---\|---\|---\|---\| \| \| 2024 \| 2023 \| 2022 \| \| Domestic \| $66,342 \| $43,499 \| $25,025 \| \| Foreign \| 4,321 \| 3,929 \| 3,794 \| \| Income before provision for income taxes \| $70,663 \| $47,428 \|… |
| 9 | `META_FY2024_2024-12-31:396` | Item 7 › Taxes |  |  | Cash paid for income taxes was $10.55 billion for the year ended December 31, 2024. As of December 31, 2024, we had taxes payable of $718 million related to a one-time transition tax payable incurred as a result of the T… |
| 10 | `META_FY2024_2024-12-31:597` | Item 8 › Note 15. Income Taxes |  |  | \| \| December 31, \| \| \|---\|---\|---\| \| \| 2024 \| 2023 \| \| Deferred tax assets: \| \| \| \| Loss carryforwards \| $289 \| $353 \| \| Tax credit carryforwards \| 2,771 \| 2,028 \| \| Share-based compensation \| 520 \| 459 \| \| Accrued expen… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#1 `META_FY2024_2024-12-31:599`** (cited, gold #1, gold #2)

````text
Item 8.Financial Statements and Supplementary Data > Note 15. Income Taxes (table)
|  | Year Ended December 31, |  |  |
|---|---|---|---|
|  | 2024 | 2023 | 2022 |
| Gross unrecognized tax benefits ‑ beginning of period | $11,666 | $10,757 | $9,807 |
| Increases related to prior year tax positions | 685 | 168 | 210 |
| Decreases related to prior year tax positions | (6) | (263) | (172) |
| Increases related to current year tax positions | 2,882 | 1,204 | 1,166 |
| Decreases related to settlements of prior year tax positions | (9) | (199) | (254) |
| Decreases related to lapses of statute of limitations | (87) | (1) | — |
| Gross unrecognized tax benefits ‑ end of period | $15,131 | $11,666 | $10,757 |
````

</details>

RQ2 citation match (section level): `cited=[('META', 'Item 8')] gold=[(None, 'Item 8')]`

### System B (hybrid + rerank)

Model: `gpt-5.4-2026-03-05`. Hops: 1. Chunks retrieved: 5, cited: 1.

**Generated answer**

> In 2024, increases related to current year tax positions were $2,882 million, and gross unrecognized tax benefits at the end of the period were $15,131 million [1].
>
> Percentage = 2,882 / 15,131 × 100 ≈ 19.0% [1]

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `META_FY2024_2024-12-31:599` | Item 8 › Note 15. Income Taxes | ✓ | #1, #2 | \| \| Year Ended December 31, \| \| \| \|---\|---\|---\|---\| \| \| 2024 \| 2023 \| 2022 \| \| Gross unrecognized tax benefits ‑ beginning of period \| $11,666 \| $10,757 \| $9,807 \| \| Increases related to prior year tax positions \| 685 \| … |
| 2 | `META_FY2024_2024-12-31:383` | Item 7 › Provision for income taxes |  |  | Unrecognized Tax Benefits. As of December 31, 2024, we had net uncertain tax positions of $9.99 billion which was included in long-term income taxes on our consolidated balance sheets. These unrecognized tax benefits wer… |
| 3 | `META_FY2024_2024-12-31:600` | Item 8 › Note 15. Income Taxes |  |  | These unrecognized tax benefits were primarily accrued for the uncertainties with our research tax credits and transfer pricing with our foreign subsidiaries, which include licensing of intellectual property, providing s… |
| 4 | `META_FY2024_2024-12-31:598` | Item 8 › Note 15. Income Taxes |  |  | The valuation allowance was approximately $3.51 billion and $2.88 billion as of December 31, 2024 and 2023, respectively, mostly related to U.S. state tax credit carryforwards, U.S. foreign tax credits, and unrealized lo… |
| 5 | `META_FY2024_2024-12-31:595` | Item 8 › Note 15. Income Taxes |  |  | \| \| Year Ended December 31, \| \| \| \|---\|---\|---\|---\| \| \| 2024 \| 2023 \| 2022 \| \| U.S. federal statutory income tax rate \| 21.0% \| 21.0% \| 21.0% \| \| State income taxes, net of federal benefit \| 0.7 \| 1.1 \| 1.0 \| \| Share-bas… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#1 `META_FY2024_2024-12-31:599`** (cited, gold #1, gold #2)

````text
Item 8.Financial Statements and Supplementary Data > Note 15. Income Taxes (table)
|  | Year Ended December 31, |  |  |
|---|---|---|---|
|  | 2024 | 2023 | 2022 |
| Gross unrecognized tax benefits ‑ beginning of period | $11,666 | $10,757 | $9,807 |
| Increases related to prior year tax positions | 685 | 168 | 210 |
| Decreases related to prior year tax positions | (6) | (263) | (172) |
| Increases related to current year tax positions | 2,882 | 1,204 | 1,166 |
| Decreases related to settlements of prior year tax positions | (9) | (199) | (254) |
| Decreases related to lapses of statute of limitations | (87) | (1) | — |
| Gross unrecognized tax benefits ‑ end of period | $15,131 | $11,666 | $10,757 |
````

</details>

RQ2 citation match (section level): `cited=[('META', 'Item 8')] gold=[(None, 'Item 8')]`

### System C v1 (adaptive multi-hop)

Model: `gpt-5.4`. Hops: 3. Chunks retrieved: 8, cited: 1.

**Generated answer**

> Gross unrecognized tax benefits at the end of 2024 were $15,131, and increases related to current year tax positions were $2,882 [META FY2024, Item 8, META_FY2024_2024-12-31:599].  
> Therefore, increases related to current year tax positions were approximately 19.0% of total gross unrecognized tax benefits at the end of the period ($2,882 ÷ $15,131) [META FY2024, Item 8, META_FY2024_2024-12-31:599].

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `META_FY2024_2024-12-31:606` | Item 8 › Note 15. Income Taxes |  |  | We believe that adequate amounts have been reserved in accordance with ASC 740 for any adjustments to the provision for income taxes or other tax items that may ultimately result from these examinations. The timing of th… |
| 2 | `META_FY2024_2024-12-31:599` | Item 8 › Note 15. Income Taxes | ✓ | #1, #2 | \| \| Year Ended December 31, \| \| \| \|---\|---\|---\|---\| \| \| 2024 \| 2023 \| 2022 \| \| Gross unrecognized tax benefits ‑ beginning of period \| $11,666 \| $10,757 \| $9,807 \| \| Increases related to prior year tax positions \| 685 \| … |
| 3 | `META_FY2024_2024-12-31:600` | Item 8 › Note 15. Income Taxes |  |  | These unrecognized tax benefits were primarily accrued for the uncertainties with our research tax credits and transfer pricing with our foreign subsidiaries, which include licensing of intellectual property, providing s… |
| 4 | `META_FY2024_2024-12-31:383` | Item 7 › Provision for income taxes |  |  | Unrecognized Tax Benefits. As of December 31, 2024, we had net uncertain tax positions of $9.99 billion which was included in long-term income taxes on our consolidated balance sheets. These unrecognized tax benefits wer… |
| 5 | `META_FY2024_2024-12-31:605` | Item 8 › Note 15. Income Taxes |  |  | We have previously accrued an estimated unrecognized tax benefit consistent with the guidance in ASC 740, Income Taxes (ASC 740), that is lower than the potential additional federal tax liability from the positions taken… |
| 6 | `META_FY2024_2024-12-31:461` | Item 8 › Income Taxes |  |  | We record a valuation allowance to reduce our deferred tax assets to the net amount that we believe is more likely than not to be realized. We consider all available evidence, both positive and negative, including histor… |
| 7 | `META_FY2024_2024-12-31:593` | Item 8 › Note 15. Income Taxes |  |  | \| \| Year Ended December 31, \| \| \| \|---\|---\|---\|---\| \| \| 2024 \| 2023 \| 2022 \| \| Current: \| \| \| \| \| Federal \| $9,569 \| $4,934 \| $6,094 \| \| State \| 775 \| 577 \| 874 \| \| Foreign \| 2,696 \| 2,688 \| 1,928 \| \| Total current tax e… |
| 8 | `META_FY2024_2024-12-31:595` | Item 8 › Note 15. Income Taxes |  |  | \| \| Year Ended December 31, \| \| \| \|---\|---\|---\|---\| \| \| 2024 \| 2023 \| 2022 \| \| U.S. federal statutory income tax rate \| 21.0% \| 21.0% \| 21.0% \| \| State income taxes, net of federal benefit \| 0.7 \| 1.1 \| 1.0 \| \| Share-bas… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#2 `META_FY2024_2024-12-31:599`** (cited, gold #1, gold #2)

````text
Item 8.Financial Statements and Supplementary Data > Note 15. Income Taxes (table)
|  | Year Ended December 31, |  |  |
|---|---|---|---|
|  | 2024 | 2023 | 2022 |
| Gross unrecognized tax benefits ‑ beginning of period | $11,666 | $10,757 | $9,807 |
| Increases related to prior year tax positions | 685 | 168 | 210 |
| Decreases related to prior year tax positions | (6) | (263) | (172) |
| Increases related to current year tax positions | 2,882 | 1,204 | 1,166 |
| Decreases related to settlements of prior year tax positions | (9) | (199) | (254) |
| Decreases related to lapses of statute of limitations | (87) | (1) | — |
| Gross unrecognized tax benefits ‑ end of period | $15,131 | $11,666 | $10,757 |
````

</details>

RQ2 citation match (section level): `cited=[('META', 'Item 8')] gold=[(None, 'Item 8')]`

**System C guardrail** (judge `gpt-5.4`): numerical claims 5, verified 5, ungrounded 0, uncited 0, derived 1; sentence verdicts: supported 0, partial 0, unsupported 0, unchecked 0.


<details><summary>Guardrail sentence verdicts</summary>

| sentence | verdict | judge reason |
|---|---|---|
| Gross unrecognized tax benefits at the end of 2024 were $15,131, and increases related to current year tax positions were $2,882 [META FY2024, Item 8, META_FY2024_2024-12-31:599]. | None |  |
| Therefore, increases related to current year tax positions were approximately 19.0% of total gross unrecognized tax benefits at the end of the period ($2,882 ÷ $15,131) [META FY2024, Item 8, META_FY2024_2024-12-31:599]. | None |  |

</details>

### System C v2 (agentic multi-hop + XBRL)

Model: `gpt-5.4`. Hops: 3. Chunks retrieved: 8, cited: 1.

**Generated answer**

> In fiscal year 2024, increases related to current year tax positions were $2,882 million and gross unrecognized tax benefits at the end of the period were $15,131 million, so the percentage was approximately 19.0% [META FY2024, Item 8, META_FY2024_2024-12-31:599].

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `META_FY2024_2024-12-31:599` | Item 8 › Note 15. Income Taxes | ✓ | #1, #2 | \| \| Year Ended December 31, \| \| \| \|---\|---\|---\|---\| \| \| 2024 \| 2023 \| 2022 \| \| Gross unrecognized tax benefits ‑ beginning of period \| $11,666 \| $10,757 \| $9,807 \| \| Increases related to prior year tax positions \| 685 \| … |
| 2 | `META_FY2024_2024-12-31:383` | Item 7 › Provision for income taxes |  |  | Unrecognized Tax Benefits. As of December 31, 2024, we had net uncertain tax positions of $9.99 billion which was included in long-term income taxes on our consolidated balance sheets. These unrecognized tax benefits wer… |
| 3 | `META_FY2024_2024-12-31:600` | Item 8 › Note 15. Income Taxes |  |  | These unrecognized tax benefits were primarily accrued for the uncertainties with our research tax credits and transfer pricing with our foreign subsidiaries, which include licensing of intellectual property, providing s… |
| 4 | `META_FY2024_2024-12-31:606` | Item 8 › Note 15. Income Taxes |  |  | We believe that adequate amounts have been reserved in accordance with ASC 740 for any adjustments to the provision for income taxes or other tax items that may ultimately result from these examinations. The timing of th… |
| 5 | `META_FY2024_2024-12-31:605` | Item 8 › Note 15. Income Taxes |  |  | We have previously accrued an estimated unrecognized tax benefit consistent with the guidance in ASC 740, Income Taxes (ASC 740), that is lower than the potential additional federal tax liability from the positions taken… |
| 6 | `META_FY2024_2024-12-31:379` | Item 7 › Provision for income taxes |  |  | \| \| Year Ended December 31, \| \| \| \| \| \|---\|---\|---\|---\|---\|---\| \| \| 2024 \| 2023 \| 2022 \| 2024 vs 2023 % change \| 2023 vs 2022 % change \| \| \| (in millions, except percentages) \| \| \| \| \| \| Provision for income taxes \| $8,3… |
| 7 | `META_FY2024_2024-12-31:591` | Item 8 › Note 15. Income Taxes |  |  | \| \| Year Ended December 31, \| \| \| \|---\|---\|---\|---\| \| \| 2024 \| 2023 \| 2022 \| \| Domestic \| $66,342 \| $43,499 \| $25,025 \| \| Foreign \| 4,321 \| 3,929 \| 3,794 \| \| Income before provision for income taxes \| $70,663 \| $47,428 \|… |
| 8 | `META_FY2024_2024-12-31:598` | Item 8 › Note 15. Income Taxes |  |  | The valuation allowance was approximately $3.51 billion and $2.88 billion as of December 31, 2024 and 2023, respectively, mostly related to U.S. state tax credit carryforwards, U.S. foreign tax credits, and unrealized lo… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#1 `META_FY2024_2024-12-31:599`** (cited, gold #1, gold #2)

````text
Item 8.Financial Statements and Supplementary Data > Note 15. Income Taxes (table)
|  | Year Ended December 31, |  |  |
|---|---|---|---|
|  | 2024 | 2023 | 2022 |
| Gross unrecognized tax benefits ‑ beginning of period | $11,666 | $10,757 | $9,807 |
| Increases related to prior year tax positions | 685 | 168 | 210 |
| Decreases related to prior year tax positions | (6) | (263) | (172) |
| Increases related to current year tax positions | 2,882 | 1,204 | 1,166 |
| Decreases related to settlements of prior year tax positions | (9) | (199) | (254) |
| Decreases related to lapses of statute of limitations | (87) | (1) | — |
| Gross unrecognized tax benefits ‑ end of period | $15,131 | $11,666 | $10,757 |
````

</details>

RQ2 citation match (section level): `cited=[('META', 'Item 8')] gold=[(None, 'Item 8')]`

**System C guardrail** (judge `gpt-5.4`): numerical claims 3, verified 3, ungrounded 0, uncited 0, derived 1; sentence verdicts: supported 0, partial 0, unsupported 0, unchecked 0.


<details><summary>Guardrail sentence verdicts</summary>

| sentence | verdict | judge reason |
|---|---|---|
| In fiscal year 2024, increases related to current year tax positions were $2,882 million and gross unrecognized tax benefits at the end of the period were $15,131 million, so the percentage was approximately 19.0% [META FY2024, Item 8, META_FY2024_2024-12-31:599]. | None |  |

</details>
