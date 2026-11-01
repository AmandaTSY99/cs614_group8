# gold-036: Table + text (one filing)

[← all cases](../README.md) · company: JOHNSON & JOHNSON (JNJ) · fiscal year: 2025 · recipe `table_text` · hop `multi` · answer type `mixed` · scope `single_doc` · RQ2 category `cross_section_multihop`

## Gold QA

**Question**

> For Johnson & Johnson's fiscal year 2025, calculate the percentage change in the valuation allowance for continuing operations from 2024 to 2025. Additionally, identify the specific countries the company accounted for as having highly inflationary economic conditions in 2025.

**Gold answer**

> The valuation allowance increased by 12.15%. The countries accounted for as having highly inflationary economic conditions are Argentina, Venezuela, Turkey, and Egypt.

**Program**: `subtract(1837, 1638), divide(#0, 1638), multiply(#1, 100)` → `12.148962148962148`

**Gold numbers** (RQ2 numeric_accuracy targets): 12.15%

**Key points** (RQ3 keypoint_recall targets)

1. The valuation allowance for continuing operations ended at $1,837 million in 2025 and $1,638 million in 2024.
2. The percentage change in the valuation allowance is 12.15%.
3. Argentina, Venezuela, Turkey, and Egypt were accounted for as highly inflationary.

**Gold evidence**

1. `JNJ_FY2025_2025-12-28` · Item 8. Financial statements and supplementary data › 8. Income taxes · table

   > | End of year | $1,837 | $1,638 |

2. `JNJ_FY2025_2025-12-28` · Item 7. Management’s discussion and analysis of results of operations and financial condition › Economic and market factors · text

   > The Company has accounted for operations in Argentina, Venezuela, Turkey and Egypt (beginning in the fiscal fourth quarter of 2024) as highly inflationary, as the prior three-year cumulative inflation rate surpassed 100%.

## Scorecard

| Metric | A (vanilla dense) | B (hybrid + rerank) | C v1 (adaptive multi-hop) | C v2 (agentic multi-hop + XBRL) |
|---|---|---|---|---|
| **Retrieval (RQ1)** | | | | |
| chunks retrieved | 10 | 5 | 13 | 10 |
| recall@5 | 0.00 | 0.50 | 0.00 | 0.00 |
| recall@all | 0.00 | 0.50 | 1.00 | 0.50 |
| complete@all | 0 | 0 | 1 | 0 |
| average precision (lexical) | 0.00 | 1.00 | 0.24 | 0.14 |
| gold evidence first rank | #1: –, #2: – | #1: –, #2: 1 | #1: 7, #2: 10 | #1: 7, #2: – |
| **Answer (RQ3 string match)** | | | | |
| numeric_correct | ✗ | ✗ | ✓ | ✓ |
| keypoint_recall | 0.00 | 0.00 | 1.00 | 0.67 |
| **Answer & citations (RQ2)** | | | | |
| numeric_accuracy | 0.00 | 0.00 | 1.00 | 1.00 |
| citation precision | – | – | 0.67 | 1.00 |
| citation recall | – | – | 1.00 | 0.50 |
| citation F1 | – | – | 0.80 | 0.67 |
| has a citation | 0 | 0 | 1 | 1 |
| grounding error rate | – | – | 0.00 | 0.00 |
| **Cost (RQ3)** | | | | |
| retrieval hops | 1 | 1 | 3 | 2 |
| tokens | 1492 | 1538 | 13465 | 10330 |
| cost (USD) | 0.0002 | 0.0002 | 0.0485 | 0.0362 |
| latency (s) | 1.3 | 5.4 | 22.6 | 16.5 |

Definitions: [README › Metrics](../README.md#metrics). `–` = not applicable (e.g. no gold number, no citations, no guardrail).

## System outputs

### System A (vanilla dense)

Model: `gpt-5.4-2026-03-05`. Hops: 1. Chunks retrieved: 10, cited: 0.

**Generated answer**

> Not found in the provided context.

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `JNJ_FY2025_2025-12-28:158` | Item 7 › Earnings before provision for taxes |  |  | (Dollars in billions. Percentages in chart are as a percent to total sales) |
| 2 | `JNJ_FY2025_2025-12-28:343` | Item 8 › 8. Income taxes |  |  | 2025 Annual Report 67 Below is a tabular rate reconciliation of the U.S. statutory income tax rate of 21% to the Company's effective income tax rate for the fiscal year 2025, pursuant to the new disclosure requirements o… |
| 3 | `JNJ_FY2025_2025-12-28:177` | Item 7 › MedTech segment: |  |  | Provision for Taxes on Income: The worldwide effective income tax rate from continuing operations was 17.7% in 2025 and 15.7% in 2024. For discussion related to the fiscal year 2025 provision for taxes refer to Note 8 to… |
| 4 | `JNJ_FY2025_2025-12-28:350` | Item 8 › 8. Income taxes |  |  | Additionally in the fiscal year 2024, the effective tax rate was unfavorably impacted by legislative changes that went into effect for Pillar Two in some of the Company's foreign jurisdictions which are reflected in Inte… |
| 5 | `JNJ_FY2025_2025-12-28:215` | Item 7 › Economic and market factors |  |  | The Company is exposed to fluctuations in currency exchange rates. A 1% change in the value of the U.S. Dollar as compared to all foreign currencies in which the Company had sales, income or expense in 2025 would have in… |
| 6 | `JNJ_FY2025_2025-12-28:352` | Item 8 › 8. Income taxes |  |  | \| \| 2025 Deferred Tax \| \| 2024 Deferred Tax \| \| \|---\|---\|---\|---\|---\| \| Total deferred income taxes net of valuation allowances \| $12,630 \| (12,547) \| 15,188 \| (7,175) \| |
| 7 | `JNJ_FY2025_2025-12-28:137` | Item 7 › 2025 Sales by segment (in billions) |  |  | Note: values may have been rounded operational excludes the effect of translational currency |
| 8 | `JNJ_FY2025_2025-12-28:347` | Item 8 › 8. Income taxes |  |  | The Company’s 2025 effective tax rate was also unfavorably impacted by more income in higher tax jurisdictions, specifically in the U.S. In fiscal year 2025, the Company reversed previously accrued reserves of approximat… |
| 9 | `JNJ_FY2025_2025-12-28:133` | Item 7 › Analysis of consolidated sales |  |  | For discussion on results of operations and financial condition pertaining to the fiscal years 2024 and 2023 see the Company’s Annual Report on Form 10-K for the fiscal year ended December 29, 2024, Item 7. Management's … |
| 10 | `JNJ_FY2025_2025-12-28:169` | Item 7 › Income before tax by segment |  |  | Income before tax by segment of business was as follows: |

RQ2 citation match (section level): `no citations`

### System B (hybrid + rerank)

Model: `gpt-5.4-2026-03-05`. Hops: 1. Chunks retrieved: 5, cited: 0.

**Generated answer**

> Not found in the provided context.

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `JNJ_FY2025_2025-12-28:213` | Item 7 › Economic and market factors |  | #2 | The Company is aware that its products are used in an environment where, for more than a decade, policymakers, consumers and businesses have expressed concerns about the rising cost of healthcare. In response to these co… |
| 2 | `JNJ_FY2025_2025-12-28:89` | Item 1A › The Company faces a variety of financial, economic, legal, social and political risks associated with conducting business internationally. |  | #2 | Inflation and currency devaluation risks: The Company faces challenges in maintaining profitability of operations in economies experiencing high inflation rates. Specifically, the Company has accounted for operations in … |
| 3 | `JNJ_FY2025_2025-12-28:399` | Item 8 › 14. International currency translation |  | #2 | For translation of its subsidiaries operating in non-U.S. Dollar currencies, the Company has determined that the local currencies of its international subsidiaries are the functional currencies except those in highly inf… |
| 4 | `JNJ_FY2025_2025-12-28:165` | Item 7 › Research and Development expense: |  |  | In-Process Research and Development Impairments (IPR&D): In the fiscal year 2025, the Company recorded a charge of approximately $0.1 billion primarily related to a non-strategic asset acquired with Abiomed in 2022. In t… |
| 5 | `JNJ_FY2025_2025-12-28:177` | Item 7 › MedTech segment: |  |  | Provision for Taxes on Income: The worldwide effective income tax rate from continuing operations was 17.7% in 2025 and 15.7% in 2024. For discussion related to the fiscal year 2025 provision for taxes refer to Note 8 to… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#1 `JNJ_FY2025_2025-12-28:213`** (gold #2)

````text
Item 7. Management’s discussion and analysis of results of operations and financial condition > Economic and market factors
The Company is aware that its products are used in an environment where, for more than a decade, policymakers, consumers and businesses have expressed concerns about the rising cost of healthcare. In response to these concerns, the Company has a long-standing policy of pricing products responsibly. For the period 2015 - 2025, in the U.S., the weighted average compound annual growth rate of the Company’s net price increases for healthcare products (prescription and over-the-counter drugs, hospital and professional products) was below the U.S. Consumer Price Index (CPI). The Company operates in certain countries where the economic conditions continue to present significant challenges. The Company continues to monitor these situations and take appropriate actions. Inflation rates continue to have an effect on worldwide economies and, consequently, on the way companies operate. The Company has accounted for operations in Argentina, Venezuela, Turkey and Egypt (beginning in the fiscal fourth quarter of 2024) as highly inflationary, as the prior three-year cumulative inflation rate surpassed 100%. This did not have a material impact to the Company's results in the period. In the face of increasing costs, the Company strives to maintain its profit margins through cost reduction programs, productivity improvements and periodic price increases.
````

**#2 `JNJ_FY2025_2025-12-28:89`** (gold #2)

````text
Item 1A. Risk factors > The Company faces a variety of financial, economic, legal, social and political risks associated with conducting business internationally.
Inflation and currency devaluation risks: The Company faces challenges in maintaining profitability of operations in economies experiencing high inflation rates. Specifically, the Company has accounted for operations in Argentina, Turkey, Venezuela and Egypt as highly inflationary, as the prior three-year cumulative inflation rate surpassed 100%. While the Company strives to maintain profit margins in these areas through cost reduction programs, productivity improvements and periodic price increases, it might experience operating losses as a result of continued inflation. 2025 Annual Report 13 In addition, the impact of currency devaluations in countries experiencing high inflation rates or significant currency exchange fluctuations could negatively impact the Company’s operating results. Illegal importation of pharmaceutical products: The illegal importation of pharmaceutical products from countries where government price controls or other market dynamics result in lower prices may adversely affect the Company’s sales and profitability in the U.S. and other countries in which the Company operates. With the exception of limited quantities of prescription drugs for personal use, foreign imports of pharmaceutical products are illegal under current U.S. law. However, the volume of illegal imports continues to rise as the ability of patients and other customers to obtain the lower-priced imports has grown significantly.
````

**#3 `JNJ_FY2025_2025-12-28:399`** (gold #2)

````text
Item 8. Financial statements and supplementary data > 14. International currency translation
For translation of its subsidiaries operating in non-U.S. Dollar currencies, the Company has determined that the local currencies of its international subsidiaries are the functional currencies except those in highly inflationary economies, which are defined as those which have had compound cumulative rates of inflation of 100% or more during the past three years, or where a substantial portion of its cash flows are not in the local currency. For the majority of the Company's subsidiaries the local currency is the functional currency. In consolidating international subsidiaries, balance sheet currency effects are recorded as a component of accumulated other comprehensive income. The other current and non-current assets line within the Statement of Cash flows includes the impact of foreign currency translation. This equity account includes the results of translating certain balance sheet assets and liabilities at current exchange rates and some accounts at historical rates, except for those located in highly inflationary economies (Argentina, Egypt, Turkey and Venezuela). The translation of balance sheet accounts for highly inflationary economies are reflected in the operating results. A rollforward of the changes during fiscal years 2025, 2024 and 2023 for foreign currency translation adjustments is included in Note 13.
````

</details>

RQ2 citation match (section level): `no citations`

### System C v1 (adaptive multi-hop)

Model: `gpt-5.4`. Hops: 3. Chunks retrieved: 13, cited: 4.

**Generated answer**

> The valuation allowance for continuing operations increased from $1,638 million at the end of 2024 to $1,837 million at the end of 2025, an increase of approximately 12.1% (($1,837 - $1,638) / $1,638) [JNJ FY2025, Item 8, JNJ_FY2025_2025-12-28:354].  
>
> In 2025, Johnson & Johnson accounted for operations in Argentina, Venezuela, Turkey and Egypt as having highly inflationary economic conditions [JNJ FY2025, Item 7, JNJ_FY2025_2025-12-28:213] [JNJ FY2025, Item 8, JNJ_FY2025_2025-12-28:399] [JNJ FY2025, Item 1A, JNJ_FY2025_2025-12-28:89].

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `JNJ_FY2025_2025-12-28:243` | Item 8 › (Dollars in Millions) (Note 1) |  |  | \| \| 2025 \| 2024 \| 2023 \| \|---\|---\|---\|---\| \| Cash and cash equivalents from continuing operations, end of period \| 19,709 \| 24,105 \| 21,859 \| \| Cash and cash equivalents from discontinued operations, end of period \| — \| … |
| 2 | `JNJ_FY2025_2025-12-28:353` | Item 8 › 8. Income taxes |  |  | The Company has wholly-owned international subsidiaries that have cumulative losses that result in deferred tax assets. The Company believes that it is more likely than not that these subsidiaries will generate future ta… |
| 3 | `JNJ_FY2025_2025-12-28:352` | Item 8 › 8. Income taxes |  |  | \| \| 2025 Deferred Tax \| \| 2024 Deferred Tax \| \| \|---\|---\|---\|---\|---\| \| Total deferred income taxes net of valuation allowances \| $12,630 \| (12,547) \| 15,188 \| (7,175) \| |
| 4 | `JNJ_FY2025_2025-12-28:357` | Item 8 › 8. Income taxes |  |  | (1)Includes TCJA foreign undistributed earnings payments of $2.5 billion, $2.0 billion and $1.5 billion in fiscal years 2025, 2024 and 2023, respectively (2)Included in foreign income taxes paid net of refunds are paymen… |
| 5 | `JNJ_FY2025_2025-12-28:341` | Item 8 › 8. Income taxes |  |  | The provision for taxes on income on continuing operations consists of: |
| 6 | `JNJ_FY2025_2025-12-28:234` | Item 8 › (Dollars in Millions) (Note 1) |  |  | The tax cost/(benefit) effects in other comprehensive income for the fiscal years 2025, 2024 and 2023 respectively: Foreign Currency Translation; $2.5 billion, $(1.1) billion and $797 million; Employee Benefit Plans: $21… |
| 7 | `JNJ_FY2025_2025-12-28:354` | Item 8 › 8. Income taxes | ✓ | #1 | \| (Dollars in Millions) \| 2025 \| 2024 \| \|---\|---\|---\| \| Beginning of year \| $1,638 \| 1,149 \| \| Provision \| 129 \| 451 \| \| Utilization \| (70) \| — \| \| Foreign currency translation \| 90 \| (46) \| \| Net acquisitions / (disposi… |
| 8 | `JNJ_FY2025_2025-12-28:342` | Item 8 › 8. Income taxes |  |  | \| (Dollars in Millions) \| 2025 \| 2024 \| 2023 \| \|---\|---\|---\|---\| \| Currently payable: \| \| \| \| \| U.S. taxes \| $1,163 \| 2,200 \| 2,705 \| \| International taxes \| 3,076 \| 2,604 \| 3,090 \| \| Total currently payable \| 4,239 \| 4,… |
| 9 | `JNJ_FY2025_2025-12-28:348` | Item 8 › 8. Income taxes |  |  | \| (Dollars in Millions) \| 2024 \| 2023 \| \|---\|---\|---\| \| U.S. \| $(458) \| (2,033) \| \| International \| 17,145 \| 17,095 \| \| Earnings before taxes on income: \| $16,687 \| 15,062 \| \| Tax rates: \| \| \| \| U.S. statutory rate \| 21.… |
| 10 | `JNJ_FY2025_2025-12-28:213` | Item 7 › Economic and market factors | ✓ | #2 | The Company is aware that its products are used in an environment where, for more than a decade, policymakers, consumers and businesses have expressed concerns about the rising cost of healthcare. In response to these co… |
| 11 | `JNJ_FY2025_2025-12-28:399` | Item 8 › 14. International currency translation | ✓ | #2 | For translation of its subsidiaries operating in non-U.S. Dollar currencies, the Company has determined that the local currencies of its international subsidiaries are the functional currencies except those in highly inf… |
| 12 | `JNJ_FY2025_2025-12-28:89` | Item 1A › The Company faces a variety of financial, economic, legal, social and political risks associated with conducting business internationally. | ✓ | #2 | Inflation and currency devaluation risks: The Company faces challenges in maintaining profitability of operations in economies experiencing high inflation rates. Specifically, the Company has accounted for operations in … |
| 13 | `JNJ_FY2025_2025-12-28:345` | Item 8 › 8. Income taxes |  |  | \| (Dollars in Millions) \| 2025 \| \| \|---\|---\|---\| \| NCTI foreign tax credits(2) \| (1,324) \| (4.1) \| \| Subpart F foreign tax credits \| (656) \| (2.0) \| \| All other tax credits \| (475) \| (1.5) \| \| Changes in valuation allowa… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#7 `JNJ_FY2025_2025-12-28:354`** (cited, gold #1)

````text
Item 8. Financial statements and supplementary data > 8. Income taxes (table)
| (Dollars in Millions) | 2025 | 2024 |
|---|---|---|
| Beginning of year | $1,638 | 1,149 |
| Provision | 129 | 451 |
| Utilization | (70) | — |
| Foreign currency translation | 90 | (46) |
| Net acquisitions / (dispositions/liquidations) | 50 | 84 |
| End of year | $1,837 | $1,638 |
````

**#10 `JNJ_FY2025_2025-12-28:213`** (cited, gold #2)

````text
Item 7. Management’s discussion and analysis of results of operations and financial condition > Economic and market factors
The Company is aware that its products are used in an environment where, for more than a decade, policymakers, consumers and businesses have expressed concerns about the rising cost of healthcare. In response to these concerns, the Company has a long-standing policy of pricing products responsibly. For the period 2015 - 2025, in the U.S., the weighted average compound annual growth rate of the Company’s net price increases for healthcare products (prescription and over-the-counter drugs, hospital and professional products) was below the U.S. Consumer Price Index (CPI). The Company operates in certain countries where the economic conditions continue to present significant challenges. The Company continues to monitor these situations and take appropriate actions. Inflation rates continue to have an effect on worldwide economies and, consequently, on the way companies operate. The Company has accounted for operations in Argentina, Venezuela, Turkey and Egypt (beginning in the fiscal fourth quarter of 2024) as highly inflationary, as the prior three-year cumulative inflation rate surpassed 100%. This did not have a material impact to the Company's results in the period. In the face of increasing costs, the Company strives to maintain its profit margins through cost reduction programs, productivity improvements and periodic price increases.
````

**#11 `JNJ_FY2025_2025-12-28:399`** (cited, gold #2)

````text
Item 8. Financial statements and supplementary data > 14. International currency translation
For translation of its subsidiaries operating in non-U.S. Dollar currencies, the Company has determined that the local currencies of its international subsidiaries are the functional currencies except those in highly inflationary economies, which are defined as those which have had compound cumulative rates of inflation of 100% or more during the past three years, or where a substantial portion of its cash flows are not in the local currency. For the majority of the Company's subsidiaries the local currency is the functional currency. In consolidating international subsidiaries, balance sheet currency effects are recorded as a component of accumulated other comprehensive income. The other current and non-current assets line within the Statement of Cash flows includes the impact of foreign currency translation. This equity account includes the results of translating certain balance sheet assets and liabilities at current exchange rates and some accounts at historical rates, except for those located in highly inflationary economies (Argentina, Egypt, Turkey and Venezuela). The translation of balance sheet accounts for highly inflationary economies are reflected in the operating results. A rollforward of the changes during fiscal years 2025, 2024 and 2023 for foreign currency translation adjustments is included in Note 13.
````

**#12 `JNJ_FY2025_2025-12-28:89`** (cited, gold #2)

````text
Item 1A. Risk factors > The Company faces a variety of financial, economic, legal, social and political risks associated with conducting business internationally.
Inflation and currency devaluation risks: The Company faces challenges in maintaining profitability of operations in economies experiencing high inflation rates. Specifically, the Company has accounted for operations in Argentina, Turkey, Venezuela and Egypt as highly inflationary, as the prior three-year cumulative inflation rate surpassed 100%. While the Company strives to maintain profit margins in these areas through cost reduction programs, productivity improvements and periodic price increases, it might experience operating losses as a result of continued inflation. 2025 Annual Report 13 In addition, the impact of currency devaluations in countries experiencing high inflation rates or significant currency exchange fluctuations could negatively impact the Company’s operating results. Illegal importation of pharmaceutical products: The illegal importation of pharmaceutical products from countries where government price controls or other market dynamics result in lower prices may adversely affect the Company’s sales and profitability in the U.S. and other countries in which the Company operates. With the exception of limited quantities of prescription drugs for personal use, foreign imports of pharmaceutical products are illegal under current U.S. law. However, the volume of illegal imports continues to rise as the ability of patients and other customers to obtain the lower-priced imports has grown significantly.
````

</details>

RQ2 citation match (section level): `cited=[('JNJ', 'Item 8'), ('JNJ', 'Item 7'), ('JNJ', 'Item 1A')] gold=[(None, 'Item 8'), (None, 'Item 7')]`

**System C guardrail** (judge `gpt-5.4`): numerical claims 6, verified 6, ungrounded 0, uncited 0, derived 1; sentence verdicts: supported 1, partial 0, unsupported 0, unchecked 0.


<details><summary>Guardrail sentence verdicts</summary>

| sentence | verdict | judge reason |
|---|---|---|
| The valuation allowance for continuing operations increased from $1,638 million at the end of 2024 to $1,837 million at the end of 2025, an increase of approximately 12.1% (($1,837 - $1,638) / $1,638) [JNJ FY2025, Item 8, JNJ_FY2025_2025-12-28:354]. | None |  |
| In 2025, Johnson & Johnson accounted for operations in Argentina, Venezuela, Turkey and Egypt as having highly inflationary economic conditions [JNJ FY2025, Item 7, JNJ_FY2025_2025-12-28:213] [JNJ FY2025, Item 8, JNJ_FY2025_2025-12-28:399] [JNJ FY2025, Item 1A, JNJ_FY2025_2025-12-28:89]. | supported | All cited passages state that Johnson & Johnson accounted for operations in Argentina, Venezuela, Turkey, and Egypt as highly inflationary in 2025. |

</details>

### System C v2 (agentic multi-hop + XBRL)

Model: `gpt-5.4`. Hops: 2. Chunks retrieved: 10, cited: 1.

**Generated answer**

> The valuation allowance for continuing operations increased from $1,638 million at the end of 2024 to $1,837 million at the end of 2025, an increase of approximately 12.1% (($1,837 - $1,638) / $1,638) [JNJ FY2025, Item 8, JNJ_FY2025_2025-12-28:354].  
>
> The filing does not disclose the specific countries the company accounted for as having highly inflationary economic conditions in 2025.

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `JNJ_FY2025_2025-12-28:341` | Item 8 › 8. Income taxes |  |  | The provision for taxes on income on continuing operations consists of: |
| 2 | `JNJ_FY2025_2025-12-28:353` | Item 8 › 8. Income taxes |  |  | The Company has wholly-owned international subsidiaries that have cumulative losses that result in deferred tax assets. The Company believes that it is more likely than not that these subsidiaries will generate future ta… |
| 3 | `JNJ_FY2025_2025-12-28:352` | Item 8 › 8. Income taxes |  |  | \| \| 2025 Deferred Tax \| \| 2024 Deferred Tax \| \| \|---\|---\|---\|---\|---\| \| Total deferred income taxes net of valuation allowances \| $12,630 \| (12,547) \| 15,188 \| (7,175) \| |
| 4 | `JNJ_FY2025_2025-12-28:357` | Item 8 › 8. Income taxes |  |  | (1)Includes TCJA foreign undistributed earnings payments of $2.5 billion, $2.0 billion and $1.5 billion in fiscal years 2025, 2024 and 2023, respectively (2)Included in foreign income taxes paid net of refunds are paymen… |
| 5 | `JNJ_FY2025_2025-12-28:243` | Item 8 › (Dollars in Millions) (Note 1) |  |  | \| \| 2025 \| 2024 \| 2023 \| \|---\|---\|---\|---\| \| Cash and cash equivalents from continuing operations, end of period \| 19,709 \| 24,105 \| 21,859 \| \| Cash and cash equivalents from discontinued operations, end of period \| — \| … |
| 6 | `JNJ_FY2025_2025-12-28:390` | Item 8 › Valuation hierarchy |  |  | \| \| Quoted Prices in Active Markets for Identical Assets \| \| Significant Other Observable Inputs \| \| Significant Unobservable Inputs(1) \| \| Investments Measured at Net Asset Value \| \| \| \| \|---\|---\|---\|---\|---\|---\|---\|---… |
| 7 | `JNJ_FY2025_2025-12-28:354` | Item 8 › 8. Income taxes | ✓ | #1 | \| (Dollars in Millions) \| 2025 \| 2024 \| \|---\|---\|---\| \| Beginning of year \| $1,638 \| 1,149 \| \| Provision \| 129 \| 451 \| \| Utilization \| (70) \| — \| \| Foreign currency translation \| 90 \| (46) \| \| Net acquisitions / (disposi… |
| 8 | `JNJ_FY2025_2025-12-28:342` | Item 8 › 8. Income taxes |  |  | \| (Dollars in Millions) \| 2025 \| 2024 \| 2023 \| \|---\|---\|---\|---\| \| Currently payable: \| \| \| \| \| U.S. taxes \| $1,163 \| 2,200 \| 2,705 \| \| International taxes \| 3,076 \| 2,604 \| 3,090 \| \| Total currently payable \| 4,239 \| 4,… |
| 9 | `JNJ_FY2025_2025-12-28:348` | Item 8 › 8. Income taxes |  |  | \| (Dollars in Millions) \| 2024 \| 2023 \| \|---\|---\|---\| \| U.S. \| $(458) \| (2,033) \| \| International \| 17,145 \| 17,095 \| \| Earnings before taxes on income: \| $16,687 \| 15,062 \| \| Tax rates: \| \| \| \| U.S. statutory rate \| 21.… |
| 10 | `JNJ_FY2025_2025-12-28:358` | Item 8 › 8. Income taxes |  |  | \| (Dollars in Millions) \| 2025 \| 2024 \| 2023 \| \|---\|---\|---\|---\| \| Beginning of year \| $2,020 \| 2,485 \| 3,716 \| \| Increases related to current year tax positions \| 87 \| 176 \| 239 \| \| Increases related to prior period tax… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#7 `JNJ_FY2025_2025-12-28:354`** (cited, gold #1)

````text
Item 8. Financial statements and supplementary data > 8. Income taxes (table)
| (Dollars in Millions) | 2025 | 2024 |
|---|---|---|
| Beginning of year | $1,638 | 1,149 |
| Provision | 129 | 451 |
| Utilization | (70) | — |
| Foreign currency translation | 90 | (46) |
| Net acquisitions / (dispositions/liquidations) | 50 | 84 |
| End of year | $1,837 | $1,638 |
````

</details>

RQ2 citation match (section level): `cited=[('JNJ', 'Item 8')] gold=[(None, 'Item 8'), (None, 'Item 7')]`

**System C guardrail** (judge `gpt-5.4`): numerical claims 6, verified 6, ungrounded 0, uncited 0, derived 1; sentence verdicts: supported 1, partial 0, unsupported 0, unchecked 0.


<details><summary>Guardrail sentence verdicts</summary>

| sentence | verdict | judge reason |
|---|---|---|
| The valuation allowance for continuing operations increased from $1,638 million at the end of 2024 to $1,837 million at the end of 2025, an increase of approximately 12.1% (($1,837 - $1,638) / $1,638) [JNJ FY2025, Item 8, JNJ_FY2025_2025-12-28:354]. | None |  |
| The filing does not disclose the specific countries the company accounted for as having highly inflationary economic conditions in 2025. | supported | The retrieved evidence mentions countries like Ireland and Switzerland for tax payments but does not disclose any countries identified as highly inflationary in 2025. |

</details>
