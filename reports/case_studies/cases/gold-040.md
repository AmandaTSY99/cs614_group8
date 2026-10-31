# gold-040: Table + text (one filing)

[← all cases](../README.md) · company: Meta Platforms, Inc. (META) · fiscal year: 2025 · recipe `table_text` · hop `multi` · answer type `mixed` · scope `single_doc` · RQ2 category `cross_section_multihop`

## Gold QA

**Question**

> For Meta Platforms, Inc. in fiscal year 2025, calculate the total increase in the provision for income taxes compared to 2024, and according to the Income Taxes note, what specific legislative act drove the $15.93 billion charge recorded in the third quarter of 2025?

**Gold answer**

> $17,171 million. The $15.93 billion charge in the third quarter of 2025 resulted from the One Big Beautiful Bill Act (OBBBA), enacted in July 2025; $14.03 billion of it was a valuation allowance against Meta's U.S. federal deferred tax assets.

**Program**: `subtract(25474, 8303)` → `17171.0`

**Gold numbers** (RQ2 numeric_accuracy targets): $17,171 million

**Key points** (RQ3 keypoint_recall targets)

1. The provision for income taxes increased by $17,171 million (from $8,303 million to $25,474 million).
2. The $15.93 billion charge was driven by the One Big Beautiful Bill Act (OBBBA).
3. $14.03 billion of the charge was a valuation allowance against U.S. federal deferred tax assets.

**Gold evidence**

1. `META_FY2025_2025-12-31` · Item 7.Management's Discussion and Analysis of Financial Condition and Results of Operations › Provision for income taxes · table

   > | Provision for income taxes | $25,474 | $8,303 | $8,330 | 207% | —% |

2. `META_FY2025_2025-12-31` · Item 8.Financial Statements and Supplementary Data › Note 14. Income Taxes · text

   > As a result of the implementation of the One Big Beautiful Bill Act (OBBBA) enacted in July 2025, we expect to incur Corporate Alternative Minimum Tax (CAMT) beginning in 2025.

3. `META_FY2025_2025-12-31` · Item 7.Management's Discussion and Analysis of Financial Condition and Results of Operations › Provision for income taxes · text

   > We recorded a $15.93 billion charge in the third quarter of 2025, of which $14.03 billion was a valuation allowance against our U.S. federal deferred tax assets as of the enactment date of OBBBA, and the remaining was mostly related to the reduction of the benefit of the foreign-derived intangible income deduction.

## Scorecard

| Metric | A (vanilla dense) | B (hybrid + rerank) | C v1 (adaptive multi-hop) | C v2 (agentic multi-hop + XBRL) |
|---|---|---|---|---|
| **Retrieval (RQ1)** | | | | |
| chunks retrieved | 10 | 5 | 12 | 13 |
| recall@5 | 0.33 | 0.67 | 0.33 | 0.33 |
| recall@all | 0.33 | 0.67 | 1.00 | 1.00 |
| complete@all | 0 | 0 | 1 | 1 |
| average precision (lexical) | 0.45 | 1.00 | 0.30 | 0.26 |
| gold evidence first rank | #1: 2, #2: –, #3: – | #1: –, #2: 1, #3: 1 | #1: 4, #2: 7, #3: 7 | #1: 5, #2: 8, #3: 8 |
| **Answer (RQ3 string match)** | | | | |
| numeric_correct | ✓ | ✓ | ✓ | ✓ |
| keypoint_recall | 0.67 | 0.67 | 0.67 | 0.67 |
| **Answer & citations (RQ2)** | | | | |
| numeric_accuracy | 1.00 | 1.00 | 1.00 | 1.00 |
| citation precision | 1.00 | 1.00 | 1.00 | 1.00 |
| citation recall | 1.00 | 1.00 | 1.00 | 1.00 |
| citation F1 | 1.00 | 1.00 | 1.00 | 1.00 |
| has a citation | 1 | 1 | 1 | 1 |
| grounding error rate | – | – | 0.00 | 0.00 |
| **Cost (RQ3)** | | | | |
| retrieval hops | 1 | 1 | 2 | 2 |
| tokens | 2031 | 1472 | 9018 | 9144 |
| cost (USD) | 0.0004 | 0.0003 | 0.0319 | 0.0327 |
| latency (s) | 2.4 | 6.8 | 17.8 | 14.9 |

Definitions: [README › Metrics](../README.md#metrics). `–` = not applicable (e.g. no gold number, no citations, no guardrail).

## System outputs

### System A (vanilla dense)

Model: `gpt-5.4-2026-03-05`. Hops: 1. Chunks retrieved: 10, cited: 3.

**Generated answer**

> Meta’s provision for income taxes increased from **$8.303 billion in 2024** to **$25.474 billion in 2025**, an increase of **$17.171 billion** [2][5].
>
> According to the Income Taxes note/context provided, the **$15.93 billion charge** recorded in the third quarter of 2025 was driven by the implementation of the **One Big Beautiful Bill Act** [8].
>
> Calculation:
> - 2025 provision: **$25.474 billion**
> - 2024 provision: **$8.303 billion**
> - Increase: **$17.171 billion** [2][5]

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `META_FY2025_2025-12-31:595` | Item 8 › Note 14. Income Taxes |  |  | \| \| Year Ended December 31, \| \| \|---\|---\|---\| \| \| 2024 \| 2023 \| \| U.S. federal statutory income tax rate \| 21.0% \| 21.0% \| \| State income taxes, net of federal benefit \| 0.7 \| 1.1 \| \| Share-based compensation \| (3.7) \| (… |
| 2 | `META_FY2025_2025-12-31:368` | Item 7 › Provision for income taxes | ✓ | #1 | \| \| Year Ended December 31, \| \| \| \| \| \|---\|---\|---\|---\|---\|---\| \| \| 2025 \| 2024 \| 2023 \| 2025 vs 2024 % change \| 2024 vs 2023 % change \| \| \| (in millions, except percentages) \| \| \| \| \| \| Provision for income taxes \| $25,… |
| 3 | `META_FY2025_2025-12-31:593` | Item 8 › Note 14. Income Taxes |  |  | \| \| Year Ended December 31, 2025 \| \| \|---\|---\|---\| \| U.S. federal statutory income tax rate \| $18,046 \| 21.0% \| \| State and local income taxes, net of federal income tax effect (1) \| (202) \| (0.2) \| \| Foreign tax effects… |
| 4 | `META_FY2025_2025-12-31:589` | Item 8 › Note 14. Income Taxes |  |  | \| \| Year Ended December 31, \| \| \| \|---\|---\|---\|---\| \| \| 2025 \| 2024 \| 2023 \| \| Domestic \| $79,644 \| $66,342 \| $43,499 \| \| Foreign \| 6,288 \| 4,321 \| 3,929 \| \| Income before provision for income taxes \| $85,932 \| $70,663 \|… |
| 5 | `META_FY2025_2025-12-31:591` | Item 8 › Note 14. Income Taxes | ✓ | #1 | \| \| Year Ended December 31, \| \| \| \|---\|---\|---\|---\| \| \| 2025 \| 2024 \| 2023 \| \| Current: \| \| \| \| \| Federal \| $2,820 \| $9,569 \| $4,934 \| \| State \| 745 \| 775 \| 577 \| \| Foreign \| 3,154 \| 2,696 \| 2,688 \| \| Total current tax e… |
| 6 | `META_FY2025_2025-12-31:602` | Item 8 › Note 14. Income Taxes |  |  | \| \| Year Ended December 31, \| \| \| \|---\|---\|---\|---\| \| \| 2025 \| 2024 \| 2023 \| \| Gross unrecognized tax benefits ‑ beginning of period \| $15,131 \| $11,666 \| $10,757 \| \| Increases related to prior year tax positions \| 900 \|… |
| 7 | `META_FY2025_2025-12-31:387` | Item 7 › Taxes |  |  | Cash paid for income taxes was $7.58 billion for the year ended December 31, 2025. Our long-term income tax liabilities include $11.23 billion related to the uncertain tax positions and $9.78 billion related to deferred … |
| 8 | `META_FY2025_2025-12-31:306` | Item 7 › Consolidated and Segment Results | ✓ |  | •Net income was $60.46 billion, with diluted earnings per share (EPS) of $23.49 for the year ended December 31, 2025. •Capital expenditures, including principal payments on finance leases, were $72.22 billion for the yea… |
| 9 | `META_FY2025_2025-12-31:0` | Washington, D.C. 20549 |  |  | __________________________ |
| 10 | `META_FY2025_2025-12-31:590` | Item 8 › Note 14. Income Taxes |  |  | The provision for income taxes consists of the following (in millions): |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#2 `META_FY2025_2025-12-31:368`** (cited, gold #1)

````text
Item 7.Management's Discussion and Analysis of Financial Condition and Results of Operations > Provision for income taxes (table)
|  | Year Ended December 31, |  |  |  |  |
|---|---|---|---|---|---|
|  | 2025 | 2024 | 2023 | 2025 vs 2024 % change | 2024 vs 2023 % change |
|  | (in millions, except percentages) |  |  |  |  |
| Provision for income taxes | $25,474 | $8,303 | $8,330 | 207% | —% |
| Effective tax rate | 30% | 12% | 18% |  |  |
````

**#5 `META_FY2025_2025-12-31:591`** (cited, gold #1)

````text
Item 8.Financial Statements and Supplementary Data > Note 14. Income Taxes (table)
|  | Year Ended December 31, |  |  |
|---|---|---|---|
|  | 2025 | 2024 | 2023 |
| Current: |  |  |  |
| Federal | $2,820 | $9,569 | $4,934 |
| State | 745 | 775 | 577 |
| Foreign | 3,154 | 2,696 | 2,688 |
| Total current tax expense | 6,719 | 13,040 | 8,199 |
| Deferred: |  |  |  |
| Federal | 18,379 | (4,709) | 67 |
| State | 395 | (43) | 123 |
| Foreign | (19) | 15 | (59) |
| Total deferred tax (benefits) expense | 18,755 | (4,737) | 131 |
| Provision for income taxes | $25,474 | $8,303 | $8,330 |
````

**#8 `META_FY2025_2025-12-31:306`** (cited)

````text
Item 7.Management's Discussion and Analysis of Financial Condition and Results of Operations > Consolidated and Segment Results
•Net income was $60.46 billion, with diluted earnings per share (EPS) of $23.49 for the year ended December 31, 2025. •Capital expenditures, including principal payments on finance leases, were $72.22 billion for the year ended December 31, 2025. •Share repurchases of our Class A common stock were $26.26 billion and total dividend and dividend equivalent payments were $5.32 billion for the year ended December 31, 2025. •Cash, cash equivalents, and marketable securities were $81.59 billion as of December 31, 2025. •Long-term debt was $58.74 billion as of December 31, 2025. •Effective tax rate was 30% for the year ended December 31, 2025. This includes the effects of the implementation of the One Big Beautiful Bill Act during the third quarter of 2025. Absent the valuation allowance charge as of the enactment date, our 2025 effective tax rate would have decreased by 17 percentage points to 13%. •Headcount was 78,865 as of December 31, 2025, an increase of 6% year-over-year.
````

</details>

RQ2 citation match (section level): `cited=[('META', 'Item 7'), ('META', 'Item 8')] gold=[(None, 'Item 7'), (None, 'Item 8')]`

### System B (hybrid + rerank)

Model: `gpt-5.4-2026-03-05`. Hops: 1. Chunks retrieved: 5, cited: 2.

**Generated answer**

> Meta’s provision for income taxes increased by **$17.17 billion** in 2025 compared to 2024 [3].  
>
> According to the Income Taxes note, the **$15.93 billion charge** recorded in the third quarter of 2025 was driven by the implementation of the **One Big Beautiful Bill Act (OBBBA)**, enacted in July 2025 [2].

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `META_FY2025_2025-12-31:369` | Item 7 › Provision for income taxes |  | #2, #3 | On July 4, 2025, the One Big Beautiful Bill Act (OBBBA) was enacted, introducing several significant U.S. income tax provisions that reduced our U.S. federal cash tax payments for the remainder of 2025 and future years. … |
| 2 | `META_FY2025_2025-12-31:592` | Item 8 › Note 14. Income Taxes | ✓ | #2, #3 | As a result of the implementation of the One Big Beautiful Bill Act (OBBBA) enacted in July 2025, we expect to incur Corporate Alternative Minimum Tax (CAMT) beginning in 2025. We recorded a $15.93 billion charge in the … |
| 3 | `META_FY2025_2025-12-31:370` | Item 7 › Provision for income taxes | ✓ |  | Our provision for income taxes in 2025 increased $17.17 billion or 207% compared to 2024, primarily due to an increase in the effective tax rate. Our effective tax rate in 2025 increased compared to 2024, mostly due to t… |
| 4 | `META_FY2025_2025-12-31:299` | Item 5 › Stock Performance Graph |  |  | This performance graph shall not be deemed "soliciting material" or to be "filed" with the SEC for purposes of Section 18 of the Exchange Act, or otherwise subject to the liabilities under that Section, and shall not be … |
| 5 | `META_FY2025_2025-12-31:306` | Item 7 › Consolidated and Segment Results |  |  | •Net income was $60.46 billion, with diluted earnings per share (EPS) of $23.49 for the year ended December 31, 2025. •Capital expenditures, including principal payments on finance leases, were $72.22 billion for the yea… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#1 `META_FY2025_2025-12-31:369`** (gold #2, gold #3)

````text
Item 7.Management's Discussion and Analysis of Financial Condition and Results of Operations > Provision for income taxes
On July 4, 2025, the One Big Beautiful Bill Act (OBBBA) was enacted, introducing several significant U.S. income tax provisions that reduced our U.S. federal cash tax payments for the remainder of 2025 and future years. The provisions include the immediate expensing of domestic research and development costs and certain capital expenditures beginning in 2025, as well as an enhanced deduction for foreign-derived intangible income effective in 2026. The benefits from these provisions are limited by the 15% Corporate Alternative Minimum Tax (CAMT). As a result, we recorded a $15.93 billion charge in the third quarter of 2025, of which $14.03 billion was a valuation allowance against our U.S. federal deferred tax assets as of the enactment date of OBBBA, and the remaining was mostly related to the reduction of the benefit of the foreign-derived intangible income deduction. In determining the valuation allowance, our accounting policy incorporates the expected impact of future years’ CAMT in assessing the realizability of our deferred tax assets.
````

**#2 `META_FY2025_2025-12-31:592`** (cited, gold #2, gold #3)

````text
Item 8.Financial Statements and Supplementary Data > Note 14. Income Taxes
As a result of the implementation of the One Big Beautiful Bill Act (OBBBA) enacted in July 2025, we expect to incur Corporate Alternative Minimum Tax (CAMT) beginning in 2025. We recorded a $15.93 billion charge in the third quarter of 2025, of which $14.03 billion was a valuation allowance against our U.S. federal deferred tax assets as of the enactment date of OBBBA, and the remaining was mostly related to the reduction of the benefit of the foreign-derived intangible income deduction. In determining the valuation allowance, our accounting policy incorporates the expected impact of future years’ CAMT in assessing the realizability of our deferred tax assets. Beginning in 2025 annual reporting, we adopted ASU 2023-09 prospectively. See Note 1 — Summary of Significant Accounting Policies – Recently Adopted Accounting Pronouncements for additional details on the adoption of ASU 2023-09. A reconciliation of the U.S. federal statutory income tax rate to our effective tax rate pursuant to the disclosure requirements of ASU 2023-09 for the year ended December 31, 2025 is as follows (in millions, except percentages):
````

**#3 `META_FY2025_2025-12-31:370`** (cited)

````text
Item 7.Management's Discussion and Analysis of Financial Condition and Results of Operations > Provision for income taxes
Our provision for income taxes in 2025 increased $17.17 billion or 207% compared to 2024, primarily due to an increase in the effective tax rate. Our effective tax rate in 2025 increased compared to 2024, mostly due to the effects of OBBBA. Effective Tax Rate Items. Our effective tax rate in the future will depend upon the proportion between the following items and income before provision for income taxes: the effects of changes in tax law, changes in valuation allowance due to the effects of CAMT, U.S. tax benefits from foreign-derived intangible income, tax effects from share-based compensation, research tax credit, tax effects from capital losses not expected to be utilized, settlement of tax contingency items, and tax effects of changes in our business.
````

</details>

RQ2 citation match (section level): `cited=[('META', 'Item 8'), ('META', 'Item 7')] gold=[(None, 'Item 7'), (None, 'Item 8')]`

### System C v1 (adaptive multi-hop)

Model: `gpt-5.4`. Hops: 2. Chunks retrieved: 12, cited: 3.

**Generated answer**

> Meta’s provision for income taxes increased by $17.17 billion in 2025 compared to 2024, rising from $8,303 million in 2024 to $25,474 million in 2025. [META FY2025, Item 7, META_FY2025_2025-12-31:368] [META FY2025, Item 7, META_FY2025_2025-12-31:370]
>
> According to the Income Taxes note, the $15.93 billion charge recorded in the third quarter of 2025 was driven by the implementation of the One Big Beautiful Bill Act (OBBBA), enacted in July 2025. [META FY2025, Item 8, META_FY2025_2025-12-31:592]

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `META_FY2025_2025-12-31:590` | Item 8 › Note 14. Income Taxes |  |  | The provision for income taxes consists of the following (in millions): |
| 2 | `META_FY2025_2025-12-31:371` | Item 7 › Provision for income taxes |  |  | A number of countries have enacted legislation to implement the Organization for Economic Cooperation and Development’s 15% global minimum tax regime. These changes did not have a material impact on our consolidated fina… |
| 3 | `META_FY2025_2025-12-31:588` | Item 8 › Note 14. Income Taxes |  |  | The components of income before provision for income taxes are as follows (in millions): |
| 4 | `META_FY2025_2025-12-31:368` | Item 7 › Provision for income taxes | ✓ | #1 | \| \| Year Ended December 31, \| \| \| \| \| \|---\|---\|---\|---\|---\|---\| \| \| 2025 \| 2024 \| 2023 \| 2025 vs 2024 % change \| 2024 vs 2023 % change \| \| \| (in millions, except percentages) \| \| \| \| \| \| Provision for income taxes \| $25,… |
| 5 | `META_FY2025_2025-12-31:589` | Item 8 › Note 14. Income Taxes |  |  | \| \| Year Ended December 31, \| \| \| \|---\|---\|---\|---\| \| \| 2025 \| 2024 \| 2023 \| \| Domestic \| $79,644 \| $66,342 \| $43,499 \| \| Foreign \| 6,288 \| 4,321 \| 3,929 \| \| Income before provision for income taxes \| $85,932 \| $70,663 \|… |
| 6 | `META_FY2025_2025-12-31:370` | Item 7 › Provision for income taxes | ✓ |  | Our provision for income taxes in 2025 increased $17.17 billion or 207% compared to 2024, primarily due to an increase in the effective tax rate. Our effective tax rate in 2025 increased compared to 2024, mostly due to t… |
| 7 | `META_FY2025_2025-12-31:369` | Item 7 › Provision for income taxes |  | #2, #3 | On July 4, 2025, the One Big Beautiful Bill Act (OBBBA) was enacted, introducing several significant U.S. income tax provisions that reduced our U.S. federal cash tax payments for the remainder of 2025 and future years. … |
| 8 | `META_FY2025_2025-12-31:592` | Item 8 › Note 14. Income Taxes | ✓ | #2, #3 | As a result of the implementation of the One Big Beautiful Bill Act (OBBBA) enacted in July 2025, we expect to incur Corporate Alternative Minimum Tax (CAMT) beginning in 2025. We recorded a $15.93 billion charge in the … |
| 9 | `META_FY2025_2025-12-31:306` | Item 7 › Consolidated and Segment Results |  |  | •Net income was $60.46 billion, with diluted earnings per share (EPS) of $23.49 for the year ended December 31, 2025. •Capital expenditures, including principal payments on finance leases, were $72.22 billion for the yea… |
| 10 | `META_FY2025_2025-12-31:593` | Item 8 › Note 14. Income Taxes |  |  | \| \| Year Ended December 31, 2025 \| \| \|---\|---\|---\| \| U.S. federal statutory income tax rate \| $18,046 \| 21.0% \| \| State and local income taxes, net of federal income tax effect (1) \| (202) \| (0.2) \| \| Foreign tax effects… |
| 11 | `META_FY2025_2025-12-31:602` | Item 8 › Note 14. Income Taxes |  |  | \| \| Year Ended December 31, \| \| \| \|---\|---\|---\|---\| \| \| 2025 \| 2024 \| 2023 \| \| Gross unrecognized tax benefits ‑ beginning of period \| $15,131 \| $11,666 \| $10,757 \| \| Increases related to prior year tax positions \| 900 \|… |
| 12 | `META_FY2025_2025-12-31:595` | Item 8 › Note 14. Income Taxes |  |  | \| \| Year Ended December 31, \| \| \|---\|---\|---\| \| \| 2024 \| 2023 \| \| U.S. federal statutory income tax rate \| 21.0% \| 21.0% \| \| State income taxes, net of federal benefit \| 0.7 \| 1.1 \| \| Share-based compensation \| (3.7) \| (… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#4 `META_FY2025_2025-12-31:368`** (cited, gold #1)

````text
Item 7.Management's Discussion and Analysis of Financial Condition and Results of Operations > Provision for income taxes (table)
|  | Year Ended December 31, |  |  |  |  |
|---|---|---|---|---|---|
|  | 2025 | 2024 | 2023 | 2025 vs 2024 % change | 2024 vs 2023 % change |
|  | (in millions, except percentages) |  |  |  |  |
| Provision for income taxes | $25,474 | $8,303 | $8,330 | 207% | —% |
| Effective tax rate | 30% | 12% | 18% |  |  |
````

**#6 `META_FY2025_2025-12-31:370`** (cited)

````text
Item 7.Management's Discussion and Analysis of Financial Condition and Results of Operations > Provision for income taxes
Our provision for income taxes in 2025 increased $17.17 billion or 207% compared to 2024, primarily due to an increase in the effective tax rate. Our effective tax rate in 2025 increased compared to 2024, mostly due to the effects of OBBBA. Effective Tax Rate Items. Our effective tax rate in the future will depend upon the proportion between the following items and income before provision for income taxes: the effects of changes in tax law, changes in valuation allowance due to the effects of CAMT, U.S. tax benefits from foreign-derived intangible income, tax effects from share-based compensation, research tax credit, tax effects from capital losses not expected to be utilized, settlement of tax contingency items, and tax effects of changes in our business.
````

**#7 `META_FY2025_2025-12-31:369`** (gold #2, gold #3)

````text
Item 7.Management's Discussion and Analysis of Financial Condition and Results of Operations > Provision for income taxes
On July 4, 2025, the One Big Beautiful Bill Act (OBBBA) was enacted, introducing several significant U.S. income tax provisions that reduced our U.S. federal cash tax payments for the remainder of 2025 and future years. The provisions include the immediate expensing of domestic research and development costs and certain capital expenditures beginning in 2025, as well as an enhanced deduction for foreign-derived intangible income effective in 2026. The benefits from these provisions are limited by the 15% Corporate Alternative Minimum Tax (CAMT). As a result, we recorded a $15.93 billion charge in the third quarter of 2025, of which $14.03 billion was a valuation allowance against our U.S. federal deferred tax assets as of the enactment date of OBBBA, and the remaining was mostly related to the reduction of the benefit of the foreign-derived intangible income deduction. In determining the valuation allowance, our accounting policy incorporates the expected impact of future years’ CAMT in assessing the realizability of our deferred tax assets.
````

**#8 `META_FY2025_2025-12-31:592`** (cited, gold #2, gold #3)

````text
Item 8.Financial Statements and Supplementary Data > Note 14. Income Taxes
As a result of the implementation of the One Big Beautiful Bill Act (OBBBA) enacted in July 2025, we expect to incur Corporate Alternative Minimum Tax (CAMT) beginning in 2025. We recorded a $15.93 billion charge in the third quarter of 2025, of which $14.03 billion was a valuation allowance against our U.S. federal deferred tax assets as of the enactment date of OBBBA, and the remaining was mostly related to the reduction of the benefit of the foreign-derived intangible income deduction. In determining the valuation allowance, our accounting policy incorporates the expected impact of future years’ CAMT in assessing the realizability of our deferred tax assets. Beginning in 2025 annual reporting, we adopted ASU 2023-09 prospectively. See Note 1 — Summary of Significant Accounting Policies – Recently Adopted Accounting Pronouncements for additional details on the adoption of ASU 2023-09. A reconciliation of the U.S. federal statutory income tax rate to our effective tax rate pursuant to the disclosure requirements of ASU 2023-09 for the year ended December 31, 2025 is as follows (in millions, except percentages):
````

</details>

RQ2 citation match (section level): `cited=[('META', 'Item 7'), ('META', 'Item 8')] gold=[(None, 'Item 7'), (None, 'Item 8')]`

**System C guardrail** (judge `gpt-5.4`): numerical claims 4, verified 4, ungrounded 0, uncited 0, derived 0; sentence verdicts: supported 0, partial 0, unsupported 0, unchecked 0.


<details><summary>Guardrail sentence verdicts</summary>

| sentence | verdict | judge reason |
|---|---|---|
| Meta’s provision for income taxes increased by $17.17 billion in 2025 compared to 2024, rising from $8,303 million in 2024 to $25,474 million in 2025. [META FY2025, Item 7, META_FY2025_2025-12-31:368] [META FY2025, Item 7, META_FY2025_2025-12-31:370] | None |  |
| According to the Income Taxes note, the $15.93 billion charge recorded in the third quarter of 2025 was driven by the implementation of the One Big Beautiful Bill Act (OBBBA), enacted in July 2025. [META FY2025, Item 8, META_FY2025_2025-12-31:592] | None |  |

</details>

### System C v2 (agentic multi-hop + XBRL)

Model: `gpt-5.4`. Hops: 2. Chunks retrieved: 13, cited: 2.

**Generated answer**

> Meta’s provision for income taxes increased by $17,171 million in 2025 compared to 2024, calculated from $25,474 million in 2025 minus $8,303 million in 2024 [META FY2025, Item 7, META_FY2025_2025-12-31:368].  
> According to the Income Taxes note, the $15.93 billion charge recorded in the third quarter of 2025 was driven by the implementation of the One Big Beautiful Bill Act (OBBBA) enacted in July 2025 [META FY2025, Item 8, META_FY2025_2025-12-31:592].

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `F-META-2025` | SEC XBRL Reported Financials (financials.csv) |  |  | fiscal_year,fiscal_year_end,Revenue,NetIncome,OperatingIncome,TotalAssets,TotalLiabilities,StockholdersEquity,CashAndEquivalents,OperatingCashFlow,EPSDiluted 2025,2025-12-31,200966000000,60458000000,83276000000,366021000… |
| 2 | `META_FY2025_2025-12-31:590` | Item 8 › Note 14. Income Taxes |  |  | The provision for income taxes consists of the following (in millions): |
| 3 | `META_FY2025_2025-12-31:371` | Item 7 › Provision for income taxes |  |  | A number of countries have enacted legislation to implement the Organization for Economic Cooperation and Development’s 15% global minimum tax regime. These changes did not have a material impact on our consolidated fina… |
| 4 | `META_FY2025_2025-12-31:588` | Item 8 › Note 14. Income Taxes |  |  | The components of income before provision for income taxes are as follows (in millions): |
| 5 | `META_FY2025_2025-12-31:368` | Item 7 › Provision for income taxes | ✓ | #1 | \| \| Year Ended December 31, \| \| \| \| \| \|---\|---\|---\|---\|---\|---\| \| \| 2025 \| 2024 \| 2023 \| 2025 vs 2024 % change \| 2024 vs 2023 % change \| \| \| (in millions, except percentages) \| \| \| \| \| \| Provision for income taxes \| $25,… |
| 6 | `META_FY2025_2025-12-31:589` | Item 8 › Note 14. Income Taxes |  |  | \| \| Year Ended December 31, \| \| \| \|---\|---\|---\|---\| \| \| 2025 \| 2024 \| 2023 \| \| Domestic \| $79,644 \| $66,342 \| $43,499 \| \| Foreign \| 6,288 \| 4,321 \| 3,929 \| \| Income before provision for income taxes \| $85,932 \| $70,663 \|… |
| 7 | `META_FY2025_2025-12-31:370` | Item 7 › Provision for income taxes |  |  | Our provision for income taxes in 2025 increased $17.17 billion or 207% compared to 2024, primarily due to an increase in the effective tax rate. Our effective tax rate in 2025 increased compared to 2024, mostly due to t… |
| 8 | `META_FY2025_2025-12-31:369` | Item 7 › Provision for income taxes |  | #2, #3 | On July 4, 2025, the One Big Beautiful Bill Act (OBBBA) was enacted, introducing several significant U.S. income tax provisions that reduced our U.S. federal cash tax payments for the remainder of 2025 and future years. … |
| 9 | `META_FY2025_2025-12-31:592` | Item 8 › Note 14. Income Taxes | ✓ | #2, #3 | As a result of the implementation of the One Big Beautiful Bill Act (OBBBA) enacted in July 2025, we expect to incur Corporate Alternative Minimum Tax (CAMT) beginning in 2025. We recorded a $15.93 billion charge in the … |
| 10 | `META_FY2025_2025-12-31:306` | Item 7 › Consolidated and Segment Results |  |  | •Net income was $60.46 billion, with diluted earnings per share (EPS) of $23.49 for the year ended December 31, 2025. •Capital expenditures, including principal payments on finance leases, were $72.22 billion for the yea… |
| 11 | `META_FY2025_2025-12-31:593` | Item 8 › Note 14. Income Taxes |  |  | \| \| Year Ended December 31, 2025 \| \| \|---\|---\|---\| \| U.S. federal statutory income tax rate \| $18,046 \| 21.0% \| \| State and local income taxes, net of federal income tax effect (1) \| (202) \| (0.2) \| \| Foreign tax effects… |
| 12 | `META_FY2025_2025-12-31:602` | Item 8 › Note 14. Income Taxes |  |  | \| \| Year Ended December 31, \| \| \| \|---\|---\|---\|---\| \| \| 2025 \| 2024 \| 2023 \| \| Gross unrecognized tax benefits ‑ beginning of period \| $15,131 \| $11,666 \| $10,757 \| \| Increases related to prior year tax positions \| 900 \|… |
| 13 | `META_FY2025_2025-12-31:595` | Item 8 › Note 14. Income Taxes |  |  | \| \| Year Ended December 31, \| \| \|---\|---\|---\| \| \| 2024 \| 2023 \| \| U.S. federal statutory income tax rate \| 21.0% \| 21.0% \| \| State income taxes, net of federal benefit \| 0.7 \| 1.1 \| \| Share-based compensation \| (3.7) \| (… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#5 `META_FY2025_2025-12-31:368`** (cited, gold #1)

````text
Item 7.Management's Discussion and Analysis of Financial Condition and Results of Operations > Provision for income taxes (table)
|  | Year Ended December 31, |  |  |  |  |
|---|---|---|---|---|---|
|  | 2025 | 2024 | 2023 | 2025 vs 2024 % change | 2024 vs 2023 % change |
|  | (in millions, except percentages) |  |  |  |  |
| Provision for income taxes | $25,474 | $8,303 | $8,330 | 207% | —% |
| Effective tax rate | 30% | 12% | 18% |  |  |
````

**#8 `META_FY2025_2025-12-31:369`** (gold #2, gold #3)

````text
Item 7.Management's Discussion and Analysis of Financial Condition and Results of Operations > Provision for income taxes
On July 4, 2025, the One Big Beautiful Bill Act (OBBBA) was enacted, introducing several significant U.S. income tax provisions that reduced our U.S. federal cash tax payments for the remainder of 2025 and future years. The provisions include the immediate expensing of domestic research and development costs and certain capital expenditures beginning in 2025, as well as an enhanced deduction for foreign-derived intangible income effective in 2026. The benefits from these provisions are limited by the 15% Corporate Alternative Minimum Tax (CAMT). As a result, we recorded a $15.93 billion charge in the third quarter of 2025, of which $14.03 billion was a valuation allowance against our U.S. federal deferred tax assets as of the enactment date of OBBBA, and the remaining was mostly related to the reduction of the benefit of the foreign-derived intangible income deduction. In determining the valuation allowance, our accounting policy incorporates the expected impact of future years’ CAMT in assessing the realizability of our deferred tax assets.
````

**#9 `META_FY2025_2025-12-31:592`** (cited, gold #2, gold #3)

````text
Item 8.Financial Statements and Supplementary Data > Note 14. Income Taxes
As a result of the implementation of the One Big Beautiful Bill Act (OBBBA) enacted in July 2025, we expect to incur Corporate Alternative Minimum Tax (CAMT) beginning in 2025. We recorded a $15.93 billion charge in the third quarter of 2025, of which $14.03 billion was a valuation allowance against our U.S. federal deferred tax assets as of the enactment date of OBBBA, and the remaining was mostly related to the reduction of the benefit of the foreign-derived intangible income deduction. In determining the valuation allowance, our accounting policy incorporates the expected impact of future years’ CAMT in assessing the realizability of our deferred tax assets. Beginning in 2025 annual reporting, we adopted ASU 2023-09 prospectively. See Note 1 — Summary of Significant Accounting Policies – Recently Adopted Accounting Pronouncements for additional details on the adoption of ASU 2023-09. A reconciliation of the U.S. federal statutory income tax rate to our effective tax rate pursuant to the disclosure requirements of ASU 2023-09 for the year ended December 31, 2025 is as follows (in millions, except percentages):
````

</details>

RQ2 citation match (section level): `cited=[('META', 'Item 7'), ('META', 'Item 8')] gold=[(None, 'Item 7'), (None, 'Item 8')]`

**System C guardrail** (judge `gpt-5.4`): numerical claims 4, verified 4, ungrounded 0, uncited 0, derived 1; sentence verdicts: supported 0, partial 0, unsupported 0, unchecked 0.


<details><summary>Guardrail sentence verdicts</summary>

| sentence | verdict | judge reason |
|---|---|---|
| Meta’s provision for income taxes increased by $17,171 million in 2025 compared to 2024, calculated from $25,474 million in 2025 minus $8,303 million in 2024 [META FY2025, Item 7, META_FY2025_2025-12-31:368]. | None |  |
| According to the Income Taxes note, the $15.93 billion charge recorded in the third quarter of 2025 was driven by the implementation of the One Big Beautiful Bill Act (OBBBA) enacted in July 2025 [META FY2025, Item 8, META_FY2025_2025-12-31:592]. | None |  |

</details>
