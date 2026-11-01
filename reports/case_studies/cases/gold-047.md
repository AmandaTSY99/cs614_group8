# gold-047: Single-hop table

[← all cases](../README.md) · company: JOHNSON & JOHNSON (JNJ) · fiscal year: 2020 · recipe `table` · hop `single` · answer type `numeric` · scope `single_doc` · RQ2 category `quantitative_tabular`

## Gold QA

**Question**

> In Johnson & Johnson's fiscal year 2020 10-K, by what percentage did the total reserve balance of its global supply chain restructuring program change from December 29, 2019 to January 3, 2021?

**Gold answer**

> -20.00%

**Program**: `subtract(144, 180), divide(#0, 180), multiply(#1, 100)` → `-20.0`

**Gold numbers** (RQ2 numeric_accuracy targets): -20.00%

**Gold evidence**

1. `JNJ_FY2020_2021-01-03` · Item 8. FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA › 20. Restructuring · table

   > | Reserve balance, December 29, 2019 | 164 | — |  | 16 |  | 180 |

2. `JNJ_FY2020_2021-01-03` · Item 8. FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA › 20. Restructuring · table

   > | Reserve balance, January 3, 2021(1) | $135 | — |  | 9 |  | 144 |

## Scorecard

| Metric | A (vanilla dense) | B (hybrid + rerank) | C v1 (adaptive multi-hop) | C v2 (agentic multi-hop + XBRL) |
|---|---|---|---|---|
| **Retrieval (RQ1)** | | | | |
| chunks retrieved | 10 | 5 | 8 | 8 |
| recall@5 | 1.00 | 1.00 | 1.00 | 1.00 |
| recall@all | 1.00 | 1.00 | 1.00 | 1.00 |
| complete@all | 1 | 1 | 1 | 1 |
| average precision (lexical) | 1.00 | 1.00 | 1.00 | 1.00 |
| gold evidence first rank | #1: 1, #2: 1 | #1: 1, #2: 1 | #1: 1, #2: 1 | #1: 1, #2: 1 |
| **Answer (RQ3 string match)** | | | | |
| numeric_correct | ✓ | ✓ | ✓ | ✓ |
| keypoint_recall | – | – | – | – |
| **Answer & citations (RQ2)** | | | | |
| numeric_accuracy | 0.00 | 0.00 | 0.00 | 0.00 |
| citation precision | 1.00 | 1.00 | 1.00 | 1.00 |
| citation recall | 1.00 | 1.00 | 1.00 | 1.00 |
| citation F1 | 1.00 | 1.00 | 1.00 | 1.00 |
| has a citation | 1 | 1 | 1 | 1 |
| grounding error rate | – | – | 0.00 | 0.00 |
| **Cost (RQ3)** | | | | |
| retrieval hops | 1 | 1 | 3 | 3 |
| tokens | 2600 | 981 | 10782 | 11084 |
| cost (USD) | 0.0004 | 0.0002 | 0.0408 | 0.0416 |
| latency (s) | 2.0 | 6.9 | 19.5 | 21.2 |

Definitions: [README › Metrics](../README.md#metrics). `–` = not applicable (e.g. no gold number, no citations, no guardrail).

## System outputs

### System A (vanilla dense)

Model: `gpt-5.4-2026-03-05`. Hops: 1. Chunks retrieved: 10, cited: 1.

**Generated answer**

> The total reserve balance decreased from **$180 million** on **December 29, 2019** to **$144 million** on **January 3, 2021** [1].
>
> Percentage change:
>
> \[
> \frac{144 - 180}{180} \times 100 = -20\%
> \]
>
> So, the total reserve balance **decreased by 20%** [1].

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `JNJ_FY2020_2021-01-03:528` | Item 8 › 20. Restructuring | ✓ | #1, #2 | \| (Dollars in Millions) \| Severance \| Asset Write-offs/Sales \| \| Other(2) \| \| Total \| \|---\|---\|---\|---\|---\|---\|---\| \| Reserve balance, December 30, 2018 \| $194 \| — \| \| 48 \| \| 242 \| \| 2019 activity \| (30) \| — \| \| (32) \| \|… |
| 2 | `JNJ_FY2020_2021-01-03:527` | Item 8 › 20. Restructuring |  |  | In total, the Company expects the Global Supply Chain actions to generate approximately $0.6 billion to $0.8 billion in annual pre-tax cost savings that will be substantially delivered by 2022. The Company expects to rec… |
| 3 | `JNJ_FY2020_2021-01-03:526` | Item 8 › 20. Restructuring |  |  | In the fiscal second quarter of 2018, the Company announced plans to implement a series of actions across its Global Supply Chain that are intended to focus resources and increase investments in the critical capabilities… |
| 4 | `JNJ_FY2020_2021-01-03:161` | Item 7 › Pharmaceutical Segment: |  |  | Restructuring: In the fiscal second quarter of 2018, the Company announced plans to implement actions across its global supply chain that are intended to enable the Company to focus resources and increase investments in … |
| 5 | `JNJ_FY2020_2021-01-03:323` | Item 8 › 7.Borrowings |  |  | (1)Weighted average effective rate. (2)Translation rate at January 3, 2021. (3)Translation rate at December 29, 2019. (4)The excess of the fair value over the carrying value of debt was $5.4 billion at the end of fiscal … |
| 6 | `JNJ_FY2020_2021-01-03:178` | Item 7 › Financing and Market Risk |  |  | The Company has access to substantial sources of funds at numerous banks worldwide. In September 2020, the Company secured a new 364-day Credit Facility. Total credit available to the Company approximates $10 billion, wh… |
| 7 | `JNJ_FY2020_2021-01-03:123` | Item 7 › Analysis of Consolidated Sales |  |  | \| Sales increase/(decrease) due to: \| 2020 \| 2019 \| \|---\|---\|---\| \| Volume \| 3.5% \| 3.7% \| \| Price \| (2.3) \| (0.9) \| \| Currency \| (0.6) \| (2.2) \| \| Total \| 0.6% \| 0.6% \| |
| 8 | `JNJ_FY2020_2021-01-03:122` | Item 7 › Analysis of Consolidated Sales |  |  | For discussion on results of operations and financial condition pertaining to the fiscal years 2019 and 2018 see the Company’s Annual Report on Form 10-K for the fiscal year ended December 29, 2019, Item 7. Management's … |
| 9 | `JNJ_FY2020_2021-01-03:436` | Item 8 › Divestitures |  |  | In fiscal year 2018, the Company accepted a binding offer to form a strategic collaboration with Jabil Inc., one of the world’s leading manufacturing services providers for health care products and technology products. T… |
| 10 | `JNJ_FY2020_2021-01-03:171` | Item 7 › Liquidity & Cash Flows |  |  | As of January 3, 2021, the Company's notes payable and long-term debt was in excess of cash, cash equivalents and marketable securities. As of January 3, 2021, the net debt position was $10.1 billion as compared to the p… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#1 `JNJ_FY2020_2021-01-03:528`** (cited, gold #1, gold #2)

````text
Item 8. FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA > 20. Restructuring (table)
| (Dollars in Millions) | Severance | Asset Write-offs/Sales |  | Other(2) |  | Total |
|---|---|---|---|---|---|---|
| Reserve balance, December 30, 2018 | $194 | — |  | 48 |  | 242 |
| 2019 activity | (30) | — |  | (32) |  | (62) |
| Reserve balance, December 29, 2019 | 164 | — |  | 16 |  | 180 |
| Current year activity: |  |  |  |  |  |  |
| Charges | — | 43 |  | 405 |  | 448 |
| Cash settlements | (29) | 24 | (4) | (399) |  | (404) |
| Settled non cash | — | (67) |  | (13) | (3) | (80) |
| Reserve balance, January 3, 2021(1) | $135 | — |  | 9 |  | 144 |
````

</details>

RQ2 citation match (section level): `cited=[('JNJ', 'Item 8')] gold=[(None, 'Item 8')]`

### System B (hybrid + rerank)

Model: `gpt-5.4-2026-03-05`. Hops: 1. Chunks retrieved: 5, cited: 1.

**Generated answer**

> The total reserve balance decreased from $180 million on December 29, 2019 to $144 million on January 3, 2021 [1].
>
> Percentage change = \((144 - 180) / 180 \times 100\) = \(-20\%\)
>
> So, the total reserve balance decreased by 20% [1].

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `JNJ_FY2020_2021-01-03:528` | Item 8 › 20. Restructuring | ✓ | #1, #2 | \| (Dollars in Millions) \| Severance \| Asset Write-offs/Sales \| \| Other(2) \| \| Total \| \|---\|---\|---\|---\|---\|---\|---\| \| Reserve balance, December 30, 2018 \| $194 \| — \| \| 48 \| \| 242 \| \| 2019 activity \| (30) \| — \| \| (32) \| \|… |
| 2 | `JNJ_FY2020_2021-01-03:188` | Item 7 › Consumer Health Segment |  |  | (1)Includes reserve for customer rebates of $66 million at January 3, 2021 and $54 million at December 29, 2019, recorded as a contra asset. |
| 3 | `JNJ_FY2020_2021-01-03:436` | Item 8 › Divestitures |  |  | In fiscal year 2018, the Company accepted a binding offer to form a strategic collaboration with Jabil Inc., one of the world’s leading manufacturing services providers for health care products and technology products. T… |
| 4 | `JNJ_FY2020_2021-01-03:191` | Item 7 › Pharmaceutical Segment |  |  | (1)Includes reserve for customer rebates of $174 million at January 3, 2021 and $93 million at December 29, 2019, recorded as a contra asset. (2)Includes adjustments |
| 5 | `JNJ_FY2020_2021-01-03:122` | Item 7 › Analysis of Consolidated Sales |  |  | For discussion on results of operations and financial condition pertaining to the fiscal years 2019 and 2018 see the Company’s Annual Report on Form 10-K for the fiscal year ended December 29, 2019, Item 7. Management's … |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#1 `JNJ_FY2020_2021-01-03:528`** (cited, gold #1, gold #2)

````text
Item 8. FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA > 20. Restructuring (table)
| (Dollars in Millions) | Severance | Asset Write-offs/Sales |  | Other(2) |  | Total |
|---|---|---|---|---|---|---|
| Reserve balance, December 30, 2018 | $194 | — |  | 48 |  | 242 |
| 2019 activity | (30) | — |  | (32) |  | (62) |
| Reserve balance, December 29, 2019 | 164 | — |  | 16 |  | 180 |
| Current year activity: |  |  |  |  |  |  |
| Charges | — | 43 |  | 405 |  | 448 |
| Cash settlements | (29) | 24 | (4) | (399) |  | (404) |
| Settled non cash | — | (67) |  | (13) | (3) | (80) |
| Reserve balance, January 3, 2021(1) | $135 | — |  | 9 |  | 144 |
````

</details>

RQ2 citation match (section level): `cited=[('JNJ', 'Item 8')] gold=[(None, 'Item 8')]`

### System C v1 (adaptive multi-hop)

Model: `gpt-5.4`. Hops: 3. Chunks retrieved: 8, cited: 1.

**Generated answer**

> The total reserve balance decreased from $180 million on December 29, 2019 to $144 million on January 3, 2021, a decline of 20% [JNJ FY2020, Item 8, JNJ_FY2020_2021-01-03:528].

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `JNJ_FY2020_2021-01-03:528` | Item 8 › 20. Restructuring | ✓ | #1, #2 | \| (Dollars in Millions) \| Severance \| Asset Write-offs/Sales \| \| Other(2) \| \| Total \| \|---\|---\|---\|---\|---\|---\|---\| \| Reserve balance, December 30, 2018 \| $194 \| — \| \| 48 \| \| 242 \| \| 2019 activity \| (30) \| — \| \| (32) \| \|… |
| 2 | `JNJ_FY2020_2021-01-03:527` | Item 8 › 20. Restructuring |  |  | In total, the Company expects the Global Supply Chain actions to generate approximately $0.6 billion to $0.8 billion in annual pre-tax cost savings that will be substantially delivered by 2022. The Company expects to rec… |
| 3 | `JNJ_FY2020_2021-01-03:526` | Item 8 › 20. Restructuring |  |  | In the fiscal second quarter of 2018, the Company announced plans to implement a series of actions across its Global Supply Chain that are intended to focus resources and increase investments in the critical capabilities… |
| 4 | `JNJ_FY2020_2021-01-03:161` | Item 7 › Pharmaceutical Segment: |  |  | Restructuring: In the fiscal second quarter of 2018, the Company announced plans to implement actions across its global supply chain that are intended to enable the Company to focus resources and increase investments in … |
| 5 | `JNJ_FY2020_2021-01-03:436` | Item 8 › Divestitures |  |  | In fiscal year 2018, the Company accepted a binding offer to form a strategic collaboration with Jabil Inc., one of the world’s leading manufacturing services providers for health care products and technology products. T… |
| 6 | `JNJ_FY2020_2021-01-03:162` | Item 7 › Pharmaceutical Segment: |  |  | products sold. Total project costs of approximately $1.3 billion have been recorded since the restructuring was announced. See Note 20 to the Consolidated Financial Statements for additional details related to the restru… |
| 7 | `JNJ_FY2020_2021-01-03:529` | Item 8 › 20. Restructuring |  |  | (1) Cash outlays for severance are expected to be substantially paid out over the next 2 years in accordance with the Company's plans and local laws. (2) Other includes project expense such as salaries for employees supp… |
| 8 | `JNJ_FY2020_2021-01-03:22` | Risks Related to Supply Chain and Operations |  |  | •Difficulties and delays in manufacturing, internally, through third party providers or otherwise within the supply chain, that may lead to voluntary or involuntary business interruptions or shutdowns, product shortages,… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#1 `JNJ_FY2020_2021-01-03:528`** (cited, gold #1, gold #2)

````text
Item 8. FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA > 20. Restructuring (table)
| (Dollars in Millions) | Severance | Asset Write-offs/Sales |  | Other(2) |  | Total |
|---|---|---|---|---|---|---|
| Reserve balance, December 30, 2018 | $194 | — |  | 48 |  | 242 |
| 2019 activity | (30) | — |  | (32) |  | (62) |
| Reserve balance, December 29, 2019 | 164 | — |  | 16 |  | 180 |
| Current year activity: |  |  |  |  |  |  |
| Charges | — | 43 |  | 405 |  | 448 |
| Cash settlements | (29) | 24 | (4) | (399) |  | (404) |
| Settled non cash | — | (67) |  | (13) | (3) | (80) |
| Reserve balance, January 3, 2021(1) | $135 | — |  | 9 |  | 144 |
````

</details>

RQ2 citation match (section level): `cited=[('JNJ', 'Item 8')] gold=[(None, 'Item 8')]`

**System C guardrail** (judge `gpt-5.4`): numerical claims 3, verified 3, ungrounded 0, uncited 0, derived 1; sentence verdicts: supported 0, partial 0, unsupported 0, unchecked 0.


<details><summary>Guardrail sentence verdicts</summary>

| sentence | verdict | judge reason |
|---|---|---|
| The total reserve balance decreased from $180 million on December 29, 2019 to $144 million on January 3, 2021, a decline of 20% [JNJ FY2020, Item 8, JNJ_FY2020_2021-01-03:528]. | None |  |

</details>

### System C v2 (agentic multi-hop + XBRL)

Model: `gpt-5.4`. Hops: 3. Chunks retrieved: 8, cited: 1.

**Generated answer**

> The total reserve balance decreased from 180 on December 29, 2019 to 144 on January 3, 2021, a decline of 20% ((144 - 180) / 180) [JNJ FY2020, Item 8, JNJ_FY2020_2021-01-03:528].

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `JNJ_FY2020_2021-01-03:528` | Item 8 › 20. Restructuring | ✓ | #1, #2 | \| (Dollars in Millions) \| Severance \| Asset Write-offs/Sales \| \| Other(2) \| \| Total \| \|---\|---\|---\|---\|---\|---\|---\| \| Reserve balance, December 30, 2018 \| $194 \| — \| \| 48 \| \| 242 \| \| 2019 activity \| (30) \| — \| \| (32) \| \|… |
| 2 | `JNJ_FY2020_2021-01-03:527` | Item 8 › 20. Restructuring |  |  | In total, the Company expects the Global Supply Chain actions to generate approximately $0.6 billion to $0.8 billion in annual pre-tax cost savings that will be substantially delivered by 2022. The Company expects to rec… |
| 3 | `JNJ_FY2020_2021-01-03:526` | Item 8 › 20. Restructuring |  |  | In the fiscal second quarter of 2018, the Company announced plans to implement a series of actions across its Global Supply Chain that are intended to focus resources and increase investments in the critical capabilities… |
| 4 | `JNJ_FY2020_2021-01-03:161` | Item 7 › Pharmaceutical Segment: |  |  | Restructuring: In the fiscal second quarter of 2018, the Company announced plans to implement actions across its global supply chain that are intended to enable the Company to focus resources and increase investments in … |
| 5 | `JNJ_FY2020_2021-01-03:436` | Item 8 › Divestitures |  |  | In fiscal year 2018, the Company accepted a binding offer to form a strategic collaboration with Jabil Inc., one of the world’s leading manufacturing services providers for health care products and technology products. T… |
| 6 | `JNJ_FY2020_2021-01-03:162` | Item 7 › Pharmaceutical Segment: |  |  | products sold. Total project costs of approximately $1.3 billion have been recorded since the restructuring was announced. See Note 20 to the Consolidated Financial Statements for additional details related to the restru… |
| 7 | `JNJ_FY2020_2021-01-03:226` | Item 8 › (Dollars in Millions) (Note 1) |  |  | \| \| Total \| Retained Earnings \| Accumulated Other Comprehensive Income (Loss) \| Common Stock Issued Amount \| Treasury Stock Amount \| \|---\|---\|---\|---\|---\|---\| \| Repurchase of common stock \| (6,746) \| \| \| \| (6,746) \| \| Ot… |
| 8 | `JNJ_FY2020_2021-01-03:529` | Item 8 › 20. Restructuring |  |  | (1) Cash outlays for severance are expected to be substantially paid out over the next 2 years in accordance with the Company's plans and local laws. (2) Other includes project expense such as salaries for employees supp… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#1 `JNJ_FY2020_2021-01-03:528`** (cited, gold #1, gold #2)

````text
Item 8. FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA > 20. Restructuring (table)
| (Dollars in Millions) | Severance | Asset Write-offs/Sales |  | Other(2) |  | Total |
|---|---|---|---|---|---|---|
| Reserve balance, December 30, 2018 | $194 | — |  | 48 |  | 242 |
| 2019 activity | (30) | — |  | (32) |  | (62) |
| Reserve balance, December 29, 2019 | 164 | — |  | 16 |  | 180 |
| Current year activity: |  |  |  |  |  |  |
| Charges | — | 43 |  | 405 |  | 448 |
| Cash settlements | (29) | 24 | (4) | (399) |  | (404) |
| Settled non cash | — | (67) |  | (13) | (3) | (80) |
| Reserve balance, January 3, 2021(1) | $135 | — |  | 9 |  | 144 |
````

</details>

RQ2 citation match (section level): `cited=[('JNJ', 'Item 8')] gold=[(None, 'Item 8')]`

**System C guardrail** (judge `gpt-5.4`): numerical claims 1, verified 1, ungrounded 0, uncited 0, derived 1; sentence verdicts: supported 0, partial 0, unsupported 0, unchecked 0.


<details><summary>Guardrail sentence verdicts</summary>

| sentence | verdict | judge reason |
|---|---|---|
| The total reserve balance decreased from 180 on December 29, 2019 to 144 on January 3, 2021, a decline of 20% ((144 - 180) / 180) [JNJ FY2020, Item 8, JNJ_FY2020_2021-01-03:528]. | None |  |

</details>
