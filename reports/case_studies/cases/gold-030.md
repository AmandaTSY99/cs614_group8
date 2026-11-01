# gold-030: Table + text (one filing)

[← all cases](../README.md) · company: Meta Platforms, Inc. (META) · fiscal year: 2021 · recipe `table_text` · hop `multi` · answer type `mixed` · scope `single_doc` · RQ2 category `cross_section_multihop`

## Gold QA

**Question**

> What is the percentage decrease in Meta Platforms, Inc.'s total finite-lived intangible assets net carrying amount from December 31, 2020 to December 31, 2021, and how does the company describe the materiality of the estimates associated with these assets in its critical accounting policies?

**Gold answer**

> 40.93% decrease (from $623 million to $368 million). Meta lists valuation of long-lived assets, including goodwill, intangible assets and property and equipment and their estimated useful lives, among the assumptions and estimates with the greatest potential impact on its consolidated financial statements, so it treats them as critical accounting policies and estimates.

**Program**: `subtract(623, 368), divide(#0, 623), multiply(#1, 100)` → `40.93097913322632`

**Gold numbers** (RQ2 numeric_accuracy targets): 40.93%

**Key points** (RQ3 keypoint_recall targets)

1. The net carrying amount of total finite-lived intangible assets decreased from $623 million in 2020 to $368 million in 2021.
2. The percentage decrease is approximately 40.93%.
3. The company identifies valuation of long-lived assets, including intangible assets, as a critical accounting policy due to the material impact of associated estimates and assumptions.

**Gold evidence**

1. `META_FY2021_2021-12-31` · Item 8.Financial Statements and Supplementary Data › Note 9.Goodwill and Intangible Assets · table

   > | Total finite-lived assets |  | 5,116 | (4,748) | 368 | 5,018 | (4,395) | 623 |

2. `META_FY2021_2021-12-31` · Item 7.Management's Discussion and Analysis of Financial Condition and Results of Operations › Critical Accounting Policies and Estimates · text

   > We believe that the assumptions and estimates associated with gross vs. net in revenue recognition, valuation of equity investments, income taxes, loss contingencies, and valuation of long-lived assets including goodwill, intangible assets, and property and equipment, and their associated estimated useful lives, when applicable, have the greatest potential impact on our consolidated financial statements.

## Scorecard

| Metric | A (vanilla dense) | B (hybrid + rerank) | C v1 (adaptive multi-hop) | C v2 (agentic multi-hop + XBRL) |
|---|---|---|---|---|
| **Retrieval (RQ1)** | | | | |
| chunks retrieved | 10 | 5 | 9 | 7 |
| recall@5 | 0.50 | 1.00 | 1.00 | 0.50 |
| recall@all | 0.50 | 1.00 | 1.00 | 1.00 |
| complete@all | 0 | 1 | 1 | 1 |
| average precision (lexical) | 0.50 | 1.00 | 0.42 | 0.33 |
| gold evidence first rank | #1: 2, #2: – | #1: 2, #2: 1 | #1: 2, #2: 5 | #1: 3, #2: 6 |
| **Answer (RQ3 string match)** | | | | |
| numeric_correct | ✓ | ✓ | ✓ | ✓ |
| keypoint_recall | 0.67 | 1.00 | 0.67 | 1.00 |
| **Answer & citations (RQ2)** | | | | |
| numeric_accuracy | 1.00 | 1.00 | 1.00 | 1.00 |
| citation precision | 1.00 | 1.00 | 1.00 | 1.00 |
| citation recall | 0.50 | 1.00 | 1.00 | 1.00 |
| citation F1 | 0.67 | 1.00 | 1.00 | 1.00 |
| has a citation | 1 | 1 | 1 | 1 |
| grounding error rate | – | – | 1.00 | 1.00 |
| **Cost (RQ3)** | | | | |
| retrieval hops | 1 | 1 | 3 | 1 |
| tokens | 2312 | 1333 | 15615 | 8960 |
| cost (USD) | 0.0004 | 0.0003 | 0.0597 | 0.0347 |
| latency (s) | 2.4 | 7.6 | 30.6 | 16.4 |

Definitions: [README › Metrics](../README.md#metrics). `–` = not applicable (e.g. no gold number, no citations, no guardrail).

## System outputs

### System A (vanilla dense)

Model: `gpt-5.4-2026-03-05`. Hops: 1. Chunks retrieved: 10, cited: 1.

**Generated answer**

> Meta’s total finite-lived intangible assets net carrying amount decreased from **$623 million** at December 31, 2020 to **$368 million** at December 31, 2021 [2].
>
> Percentage decrease:
> \[
> \frac{623 - 368}{623} \times 100 \approx 40.9\%
> \]
>
> So, the decrease was **about 40.9%** [2].
>
> The second part of your question—**how the company describes the materiality of the estimates associated with these assets in its critical accounting policies**—is **not provided in the context**.

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `META_FY2021_2021-12-31:471` | Item 8 › Note 9.Goodwill and Intangible Assets |  |  | Amortization expense of intangible assets for the years ended December 31, 2021, 2020, and 2019 was $407 million, $473 million, and $562 million, respectively. As of December 31, 2021, expected amortization expense for t… |
| 2 | `META_FY2021_2021-12-31:470` | Item 8 › Note 9.Goodwill and Intangible Assets | ✓ | #1 | \| \| \| December 31, 2021 \| \| \| December 31, 2020 \| \| \| \|---\|---\|---\|---\|---\|---\|---\|---\| \| \| Weighted-Average Remaining Useful Lives (in years) \| Gross Carrying Amount \| Accumulated Amortization \| Net Carrying Amount \| Gr… |
| 3 | `META_FY2021_2021-12-31:472` | Item 8 › Note 9.Goodwill and Intangible Assets |  |  | \| 2022 \| $164 \| \|---\|---\| \| 2023 \| 103 \| \| 2024 \| 61 \| \| 2025 \| 18 \| \| 2026 \| 13 \| \| Thereafter \| 9 \| \| Total \| $368 \| |
| 4 | `META_FY2021_2021-12-31:469` | Item 8 › Note 9.Goodwill and Intangible Assets |  |  | _________________________ (1)Represents reallocation of goodwill as a result of our change in segments in the fourth quarter of 2021. See Note 15 — Segment and Geographical Information for further details. The following … |
| 5 | `META_FY2021_2021-12-31:324` | Item 7 › Interest and other income, net |  |  | \| \| Year Ended December 31, \| \| \| \| \| \|---\|---\|---\|---\|---\|---\| \| \| 2021 \| 2020 \| 2019 \| 2021 vs 2020 % Change \| 2020 vs 2019 % Change \| \| \| (dollars in millions) \| \| \| \| \| \| Interest income, net \| $461 \| $672 \| $904 \| (… |
| 6 | `META_FY2021_2021-12-31:508` | Item 8 › Note 14. Income Taxes |  |  | \| \| December 31, \| \| \|---\|---\|---\| \| \| 2021 \| 2020 \| \| Deferred tax assets: \| \| \| \| Net operating loss carryforward \| $2,443 \| $2,437 \| \| Tax credit carryforward \| 1,385 \| 1,055 \| \| Share-based compensation \| 319 \| 243 \|… |
| 7 | `META_FY2021_2021-12-31:522` | Item 8 › Note 15. Segment and Geographical Information |  |  | \| \| December 31, \| \| \|---\|---\|---\| \| \| 2021 \| 2020 \| \| United States \| $55,497 \| $43,128 \| \| Rest of the world(1) \| 14,467 \| 11,853 \| \| Total long-lived assets \| $69,964 \| $54,981 \| |
| 8 | `META_FY2021_2021-12-31:368` | Item 8 › CONSOLIDATED BALANCE SHEETS |  |  | \| \| December 31, \| \| \|---\|---\|---\| \| \| 2021 \| 2020 \| \| Assets \| \| \| \| Current assets: \| \| \| \| Cash and cash equivalents \| $16,601 \| $17,576 \| \| Marketable securities \| 31,397 \| 44,378 \| \| Accounts receivable, net \| 14,03… |
| 9 | `META_FY2021_2021-12-31:332` | Item 7 › Liquidity and Capital Resources |  |  | \| \| Year Ended December 31, \| \| \| \|---\|---\|---\|---\| \| \| 2021 \| 2020 \| 2019 \| \| Net cash provided by operating activities \| $57,683 \| $38,747 \| $36,314 \| \| Net cash used in investing activities \| $(7,570) \| $(30,059) \| $(… |
| 10 | `META_FY2021_2021-12-31:314` | Item 7 › Research and development |  |  | \| \| Year Ended December 31, \| \| \| \| \| \|---\|---\|---\|---\|---\|---\| \| \| 2021 \| 2020 \| 2019 \| 2021 vs 2020 % Change \| 2020 vs 2019 % Change \| \| \| (dollars in millions) \| \| \| \| \| \| Research and development \| $24,655 \| $18,447 … |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#2 `META_FY2021_2021-12-31:470`** (cited, gold #1)

````text
Item 8.Financial Statements and Supplementary Data > Note 9.Goodwill and Intangible Assets (table)
|  |  | December 31, 2021 |  |  | December 31, 2020 |  |  |
|---|---|---|---|---|---|---|---|
|  | Weighted-Average Remaining Useful Lives (in years) | Gross Carrying Amount | Accumulated Amortization | Net Carrying Amount | Gross Carrying Amount | Accumulated Amortization | Net Carrying Amount |
| Acquired users | 0.0 | $2,057 | $(2,057) | $— | $2,057 | $(1,840) | $217 |
| Acquired technology | 2.6 | 1,412 | (1,169) | 243 | 1,297 | (1,088) | 209 |
| Acquired patents | 3.4 | 827 | (722) | 105 | 805 | (677) | 128 |
| Trade names | 3.0 | 644 | (633) | 11 | 636 | (622) | 14 |
| Other | 12.1 | 176 | (167) | 9 | 223 | (168) | 55 |
| Total finite-lived assets |  | 5,116 | (4,748) | 368 | 5,018 | (4,395) | 623 |
| Total indefinite-lived assets | N/A | 266 | — | 266 | — | — | — |
| Total intangible assets, net |  | $5,382 | $(4,748) | $634 | $5,018 | $(4,395) | $623 |
````

</details>

RQ2 citation match (section level): `cited=[('META', 'Item 8')] gold=[(None, 'Item 8'), (None, 'Item 7')]`

### System B (hybrid + rerank)

Model: `gpt-5.4-2026-03-05`. Hops: 1. Chunks retrieved: 5, cited: 2.

**Generated answer**

> Meta’s total finite-lived intangible assets net carrying amount decreased from **$623 million** at December 31, 2020 to **$368 million** at December 31, 2021 [2].
>
> Percentage decrease:
> \[
> \frac{623 - 368}{623} \times 100 \approx 40.9\%
> \]
>
> So, the decrease was **approximately 40.9%** [2].
>
> Meta describes the estimates associated with long-lived assets, including **intangible assets**, as having **“the greatest potential impact”** on its consolidated financial statements, and says these assumptions and estimates are material because the **impact of the estimates and assumptions on the consolidated financial statements is material** [1].

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `META_FY2021_2021-12-31:277` | Item 7 › Critical Accounting Policies and Estimates | ✓ | #2 | An accounting policy is deemed to be critical if the nature of the estimates or assumptions is material due to the levels of subjectivity and judgment necessary to account for highly uncertain matters or the susceptibili… |
| 2 | `META_FY2021_2021-12-31:470` | Item 8 › Note 9.Goodwill and Intangible Assets | ✓ | #1 | \| \| \| December 31, 2021 \| \| \| December 31, 2020 \| \| \| \|---\|---\|---\|---\|---\|---\|---\|---\| \| \| Weighted-Average Remaining Useful Lives (in years) \| Gross Carrying Amount \| Accumulated Amortization \| Net Carrying Amount \| Gr… |
| 3 | `META_FY2021_2021-12-31:276` | Item 7 › Critical Accounting Policies and Estimates |  |  | Our consolidated financial statements are prepared in accordance with U.S. GAAP. The preparation of these consolidated financial statements requires us to make estimates and assumptions that affect the reported amounts o… |
| 4 | `META_FY2021_2021-12-31:350` | Item 7A › Equity Investment Risk |  |  | 31, 2021 and December 31, 2020, respectively. For additional information about our equity investments, see Note 1 — Summary of Significant Accounting Policies, Note 5 — Equity Investments, and Note 6 — Fair Value Measure… |
| 5 | `META_FY2021_2021-12-31:392` | Item 8 › Organization and Description of Business |  |  | We were incorporated in Delaware in July 2004. In October 2021, we changed our corporate name from Facebook, Inc. to Meta Platforms, Inc. Our mission is to give people the power to build community and bring the world clo… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#1 `META_FY2021_2021-12-31:277`** (cited, gold #2)

````text
Item 7.Management's Discussion and Analysis of Financial Condition and Results of Operations > Critical Accounting Policies and Estimates
An accounting policy is deemed to be critical if the nature of the estimates or assumptions is material due to the levels of subjectivity and judgment necessary to account for highly uncertain matters or the susceptibility of such matters to change, and the impact of the estimates and assumptions on our consolidated financial statements is material. We believe that the assumptions and estimates associated with gross vs. net in revenue recognition, valuation of equity investments, income taxes, loss contingencies, and valuation of long-lived assets including goodwill, intangible assets, and property and equipment, and their associated estimated useful lives, when applicable, have the greatest potential impact on our consolidated financial statements. Therefore, we consider these to be our critical accounting policies and estimates. For further information on all of our significant accounting policies, see Note 1 — Summary of Significant Accounting Policies in the accompanying notes to consolidated financial statements included in Part II, Item 8, "Financial Statements and Supplementary Data" of this Annual Report on Form 10-K.
````

**#2 `META_FY2021_2021-12-31:470`** (cited, gold #1)

````text
Item 8.Financial Statements and Supplementary Data > Note 9.Goodwill and Intangible Assets (table)
|  |  | December 31, 2021 |  |  | December 31, 2020 |  |  |
|---|---|---|---|---|---|---|---|
|  | Weighted-Average Remaining Useful Lives (in years) | Gross Carrying Amount | Accumulated Amortization | Net Carrying Amount | Gross Carrying Amount | Accumulated Amortization | Net Carrying Amount |
| Acquired users | 0.0 | $2,057 | $(2,057) | $— | $2,057 | $(1,840) | $217 |
| Acquired technology | 2.6 | 1,412 | (1,169) | 243 | 1,297 | (1,088) | 209 |
| Acquired patents | 3.4 | 827 | (722) | 105 | 805 | (677) | 128 |
| Trade names | 3.0 | 644 | (633) | 11 | 636 | (622) | 14 |
| Other | 12.1 | 176 | (167) | 9 | 223 | (168) | 55 |
| Total finite-lived assets |  | 5,116 | (4,748) | 368 | 5,018 | (4,395) | 623 |
| Total indefinite-lived assets | N/A | 266 | — | 266 | — | — | — |
| Total intangible assets, net |  | $5,382 | $(4,748) | $634 | $5,018 | $(4,395) | $623 |
````

</details>

RQ2 citation match (section level): `cited=[('META', 'Item 7'), ('META', 'Item 8')] gold=[(None, 'Item 8'), (None, 'Item 7')]`

### System C v1 (adaptive multi-hop)

Model: `gpt-5.4`. Hops: 3. Chunks retrieved: 9, cited: 2.

**Generated answer**

> Meta Platforms, Inc.'s total finite-lived intangible assets net carrying amount decreased from $623 million at December 31, 2020 to $368 million at December 31, 2021, a decrease of approximately 40.9% [META FY2021, Item 8, META_FY2021_2021-12-31:470].
>
> In its critical accounting policies, the company says these estimates are based upon assumptions believed to be reasonable, but inherently uncertain and unpredictable, and that actual results may differ from estimates [META FY2021, Item 7, META_FY2021_2021-12-31:287].
>
> > [Guardrail Audit Warning]: Manual verification required; these numerical figures could not be matched in their cited chunks: 623, 368; 1 sentence(s) are not supported by their cited chunks.

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `META_FY2021_2021-12-31:471` | Item 8 › Note 9.Goodwill and Intangible Assets |  |  | Amortization expense of intangible assets for the years ended December 31, 2021, 2020, and 2019 was $407 million, $473 million, and $562 million, respectively. As of December 31, 2021, expected amortization expense for t… |
| 2 | `META_FY2021_2021-12-31:470` | Item 8 › Note 9.Goodwill and Intangible Assets | ✓ | #1 | \| \| \| December 31, 2021 \| \| \| December 31, 2020 \| \| \| \|---\|---\|---\|---\|---\|---\|---\|---\| \| \| Weighted-Average Remaining Useful Lives (in years) \| Gross Carrying Amount \| Accumulated Amortization \| Net Carrying Amount \| Gr… |
| 3 | `META_FY2021_2021-12-31:430` | Item 8 › Goodwill and Intangibles Assets |  |  | Our finite-lived intangible assets are amortized on a straight-line basis over the estimated useful lives of the assets. Indefinite-lived intangible assets are not amortized. If an indefinite-lived intangible asset is su… |
| 4 | `META_FY2021_2021-12-31:429` | Item 8 › Goodwill and Intangibles Assets |  |  | We evaluate the recoverability of finite-lived intangible assets for possible impairment whenever events or circumstances indicate that the carrying amount of such assets may not be recoverable. The evaluation of these i… |
| 5 | `META_FY2021_2021-12-31:288` | Item 7 › Valuation of Long-lived Assets including Goodwill, Intangible Assets, and Property and Equipment and Estimated Useful Lives |  | #2 | Long-lived assets, including property and equipment and finite-lived intangible assets are reviewed for possible impairment whenever events or circumstances indicate that the carrying amount of such assets may not be rec… |
| 6 | `META_FY2021_2021-12-31:467` | Item 8 › Note 9.Goodwill and Intangible Assets |  |  | During the year ended December 31, 2021, we purchased certain intangible assets and completed several business acquisitions that were not material to our consolidated financial statements, individually and in aggregate. … |
| 7 | `META_FY2021_2021-12-31:469` | Item 8 › Note 9.Goodwill and Intangible Assets |  |  | _________________________ (1)Represents reallocation of goodwill as a result of our change in segments in the fourth quarter of 2021. See Note 15 — Segment and Geographical Information for further details. The following … |
| 8 | `META_FY2021_2021-12-31:287` | Item 7 › Valuation of Long-lived Assets including Goodwill, Intangible Assets, and Property and Equipment and Estimated Useful Lives | ✓ | #2 | upon assumptions believed to be reasonable, but which are inherently uncertain and unpredictable and, as a result, actual results may differ from estimates. Allocation of purchase consideration to identifiable assets and… |
| 9 | `META_FY2021_2021-12-31:472` | Item 8 › Note 9.Goodwill and Intangible Assets |  |  | \| 2022 \| $164 \| \|---\|---\| \| 2023 \| 103 \| \| 2024 \| 61 \| \| 2025 \| 18 \| \| 2026 \| 13 \| \| Thereafter \| 9 \| \| Total \| $368 \| |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#2 `META_FY2021_2021-12-31:470`** (cited, gold #1)

````text
Item 8.Financial Statements and Supplementary Data > Note 9.Goodwill and Intangible Assets (table)
|  |  | December 31, 2021 |  |  | December 31, 2020 |  |  |
|---|---|---|---|---|---|---|---|
|  | Weighted-Average Remaining Useful Lives (in years) | Gross Carrying Amount | Accumulated Amortization | Net Carrying Amount | Gross Carrying Amount | Accumulated Amortization | Net Carrying Amount |
| Acquired users | 0.0 | $2,057 | $(2,057) | $— | $2,057 | $(1,840) | $217 |
| Acquired technology | 2.6 | 1,412 | (1,169) | 243 | 1,297 | (1,088) | 209 |
| Acquired patents | 3.4 | 827 | (722) | 105 | 805 | (677) | 128 |
| Trade names | 3.0 | 644 | (633) | 11 | 636 | (622) | 14 |
| Other | 12.1 | 176 | (167) | 9 | 223 | (168) | 55 |
| Total finite-lived assets |  | 5,116 | (4,748) | 368 | 5,018 | (4,395) | 623 |
| Total indefinite-lived assets | N/A | 266 | — | 266 | — | — | — |
| Total intangible assets, net |  | $5,382 | $(4,748) | $634 | $5,018 | $(4,395) | $623 |
````

**#5 `META_FY2021_2021-12-31:288`** (gold #2)

````text
Item 7.Management's Discussion and Analysis of Financial Condition and Results of Operations > Valuation of Long-lived Assets including Goodwill, Intangible Assets, and Property and Equipment and Estimated Useful Lives
Long-lived assets, including property and equipment and finite-lived intangible assets are reviewed for possible impairment whenever events or circumstances indicate that the carrying amount of such assets may not be recoverable. The evaluation is performed at the lowest level for which identifiable cash flows are largely independent of the cash flows of other assets and liabilities. Recoverability of these assets is measured by a comparison of the carrying amounts to the future undiscounted cash flows the assets are expected to generate from the use and eventual disposition. If such review indicates that the carrying amount of property and equipment and intangible assets is not recoverable, the carrying amount of such assets is reduced to fair value. We have not recorded any material impairment charges during the years presented.
````

**#8 `META_FY2021_2021-12-31:287`** (cited, gold #2)

````text
Item 7.Management's Discussion and Analysis of Financial Condition and Results of Operations > Valuation of Long-lived Assets including Goodwill, Intangible Assets, and Property and Equipment and Estimated Useful Lives
upon assumptions believed to be reasonable, but which are inherently uncertain and unpredictable and, as a result, actual results may differ from estimates. Allocation of purchase consideration to identifiable assets and liabilities affects our amortization expense, as acquired finite-lived intangible assets are amortized over the useful life, whereas any indefinite-lived intangible assets, including goodwill, are not amortized. During the measurement period, which is not to exceed one year from the acquisition date, we may record adjustments to the assets acquired and liabilities assumed, with the corresponding offset to goodwill. Upon the conclusion of the measurement period, any subsequent adjustments are recorded to earnings. Goodwill is tested for impairment at the reporting unit level annually or more frequently if events or changes in circumstances would more likely than not reduce the fair value of a reporting unit below its carrying value. We have two reporting units subject to goodwill impairment testing. As of December 31, 2021, no impairment of goodwill has been identified.
````

</details>

RQ2 citation match (section level): `cited=[('META', 'Item 8'), ('META', 'Item 7')] gold=[(None, 'Item 8'), (None, 'Item 7')]`

**System C guardrail** (judge `gpt-5.4`): numerical claims 3, verified 1, ungrounded 2, uncited 0, derived 1; sentence verdicts: supported 1, partial 0, unsupported 0, unchecked 0.

- ungrounded numbers: 623, 368

<details><summary>Guardrail sentence verdicts</summary>

| sentence | verdict | judge reason |
|---|---|---|
| Meta Platforms, Inc.'s total finite-lived intangible assets net carrying amount decreased from $623 million at December 31, 2020 to $368 million at December 31, 2021, a decrease of approximately 40.9% [META FY2021, Item 8, META_FY2021_2021-12-31:470]. | None |  |
| In its critical accounting policies, the company says these estimates are based upon assumptions believed to be reasonable, but inherently uncertain and unpredictable, and that actual results may differ from estimates [META FY2021, Item 7, META_FY2021_2021-12-31:287]. | supported | The cited text explicitly says the estimates are based on assumptions believed reasonable but inherently uncertain and unpredictable, and actual results may differ from estimates. |

</details>

### System C v2 (agentic multi-hop + XBRL)

Model: `gpt-5.4`. Hops: 1. Chunks retrieved: 7, cited: 2.

**Generated answer**

> Meta Platforms, Inc.'s total finite-lived intangible assets net carrying amount decreased from $623 million at December 31, 2020 to $368 million at December 31, 2021, a decrease of approximately 40.9% (($623 million - $368 million) / $623 million). [META FY2021, Item 8, META_FY2021_2021-12-31:470]
>
> In its critical accounting policies, the company states that long-lived assets, including finite-lived intangible assets, are reviewed for possible impairment whenever events or circumstances indicate that the carrying amount may not be recoverable; the evaluation is performed at the lowest level for which identifiable cash flows are largely independent; recoverability is measured by comparing carrying amounts to future undiscounted cash flows expected from use and eventual disposition; and it had not recorded any material impairment charges during the years presented. [META FY2021, Item 7, META_FY2021_2021-12-31:288]
>
> > [Guardrail Audit Warning]: Manual verification required; these numerical figures could not be matched in their cited chunks: 623, 368, 623, 368, 623; 1 sentence(s) are not supported by their cited chunks.

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `F-META-2021` | SEC XBRL Reported Financials (financials.csv) |  |  | fiscal_year,fiscal_year_end,Revenue,NetIncome,OperatingIncome,TotalAssets,TotalLiabilities,StockholdersEquity,CashAndEquivalents,OperatingCashFlow,EPSDiluted 2021,2021-12-31,117929000000,39370000000,46753000000,165987000… |
| 2 | `META_FY2021_2021-12-31:471` | Item 8 › Note 9.Goodwill and Intangible Assets |  |  | Amortization expense of intangible assets for the years ended December 31, 2021, 2020, and 2019 was $407 million, $473 million, and $562 million, respectively. As of December 31, 2021, expected amortization expense for t… |
| 3 | `META_FY2021_2021-12-31:470` | Item 8 › Note 9.Goodwill and Intangible Assets | ✓ | #1 | \| \| \| December 31, 2021 \| \| \| December 31, 2020 \| \| \| \|---\|---\|---\|---\|---\|---\|---\|---\| \| \| Weighted-Average Remaining Useful Lives (in years) \| Gross Carrying Amount \| Accumulated Amortization \| Net Carrying Amount \| Gr… |
| 4 | `META_FY2021_2021-12-31:430` | Item 8 › Goodwill and Intangibles Assets |  |  | Our finite-lived intangible assets are amortized on a straight-line basis over the estimated useful lives of the assets. Indefinite-lived intangible assets are not amortized. If an indefinite-lived intangible asset is su… |
| 5 | `META_FY2021_2021-12-31:429` | Item 8 › Goodwill and Intangibles Assets |  |  | We evaluate the recoverability of finite-lived intangible assets for possible impairment whenever events or circumstances indicate that the carrying amount of such assets may not be recoverable. The evaluation of these i… |
| 6 | `META_FY2021_2021-12-31:288` | Item 7 › Valuation of Long-lived Assets including Goodwill, Intangible Assets, and Property and Equipment and Estimated Useful Lives | ✓ | #2 | Long-lived assets, including property and equipment and finite-lived intangible assets are reviewed for possible impairment whenever events or circumstances indicate that the carrying amount of such assets may not be rec… |
| 7 | `META_FY2021_2021-12-31:467` | Item 8 › Note 9.Goodwill and Intangible Assets |  |  | During the year ended December 31, 2021, we purchased certain intangible assets and completed several business acquisitions that were not material to our consolidated financial statements, individually and in aggregate. … |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#3 `META_FY2021_2021-12-31:470`** (cited, gold #1)

````text
Item 8.Financial Statements and Supplementary Data > Note 9.Goodwill and Intangible Assets (table)
|  |  | December 31, 2021 |  |  | December 31, 2020 |  |  |
|---|---|---|---|---|---|---|---|
|  | Weighted-Average Remaining Useful Lives (in years) | Gross Carrying Amount | Accumulated Amortization | Net Carrying Amount | Gross Carrying Amount | Accumulated Amortization | Net Carrying Amount |
| Acquired users | 0.0 | $2,057 | $(2,057) | $— | $2,057 | $(1,840) | $217 |
| Acquired technology | 2.6 | 1,412 | (1,169) | 243 | 1,297 | (1,088) | 209 |
| Acquired patents | 3.4 | 827 | (722) | 105 | 805 | (677) | 128 |
| Trade names | 3.0 | 644 | (633) | 11 | 636 | (622) | 14 |
| Other | 12.1 | 176 | (167) | 9 | 223 | (168) | 55 |
| Total finite-lived assets |  | 5,116 | (4,748) | 368 | 5,018 | (4,395) | 623 |
| Total indefinite-lived assets | N/A | 266 | — | 266 | — | — | — |
| Total intangible assets, net |  | $5,382 | $(4,748) | $634 | $5,018 | $(4,395) | $623 |
````

**#6 `META_FY2021_2021-12-31:288`** (cited, gold #2)

````text
Item 7.Management's Discussion and Analysis of Financial Condition and Results of Operations > Valuation of Long-lived Assets including Goodwill, Intangible Assets, and Property and Equipment and Estimated Useful Lives
Long-lived assets, including property and equipment and finite-lived intangible assets are reviewed for possible impairment whenever events or circumstances indicate that the carrying amount of such assets may not be recoverable. The evaluation is performed at the lowest level for which identifiable cash flows are largely independent of the cash flows of other assets and liabilities. Recoverability of these assets is measured by a comparison of the carrying amounts to the future undiscounted cash flows the assets are expected to generate from the use and eventual disposition. If such review indicates that the carrying amount of property and equipment and intangible assets is not recoverable, the carrying amount of such assets is reduced to fair value. We have not recorded any material impairment charges during the years presented.
````

</details>

RQ2 citation match (section level): `cited=[('META', 'Item 8'), ('META', 'Item 7')] gold=[(None, 'Item 8'), (None, 'Item 7')]`

**System C guardrail** (judge `gpt-5.4`): numerical claims 6, verified 1, ungrounded 5, uncited 0, derived 1; sentence verdicts: supported 1, partial 0, unsupported 0, unchecked 0.

- ungrounded numbers: 623, 368, 623, 368, 623

<details><summary>Guardrail sentence verdicts</summary>

| sentence | verdict | judge reason |
|---|---|---|
| Meta Platforms, Inc.'s total finite-lived intangible assets net carrying amount decreased from $623 million at December 31, 2020 to $368 million at December 31, 2021, a decrease of approximately 40.9% (($623 million - $368 million) / $623 million). [META FY2021, Item 8, META_FY2021_2021-12-31:470] | None |  |
| In its critical accounting policies, the company states that long-lived assets, including finite-lived intangible assets, are reviewed for possible impairment whenever events or circumstances indicate that the carrying amount may not be recoverable; the evaluation is performed at the lowest level for which identifiable cash flows are largely independent; recoverability is measured by comparing carrying amounts to future undiscounted cash flows expected from use and eventual disposition; and it had not recorded any material impairment charges during the years presented. [META FY2021, Item 7, META_FY2021_2021-12-31:288] | supported | The cited passage states each element of the sentence, including the impairment review trigger, asset-grouping level, undiscounted cash flow test, and no material impairment charges. |

</details>
