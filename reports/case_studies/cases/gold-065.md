# gold-065: Table + text (one filing)

[← all cases](../README.md) · company: JOHNSON & JOHNSON (JNJ) · fiscal year: 2015 · recipe `table_text` · hop `multi` · answer type `mixed` · scope `single_doc` · RQ2 category `cross_section_multihop`

## Gold QA

**Question**

> For Johnson & Johnson in fiscal year 2015, by what percentage did the total goodwill balance decrease from the beginning to the end of the year, and on what basis does the company estimate its sales returns reserve?

**Gold answer**

> Total goodwill decreased by 0.93%, from $21,832 million to $21,629 million. The returns reserve is based on historical return trends by product and by market as a percent to gross sales.

**Program**: `subtract(21832, 21629), divide(#0, 21832)` → `0.0092982777574203`

**Gold numbers** (RQ2 numeric_accuracy targets): 0.93%

**Key points** (RQ3 keypoint_recall targets)

1. Total goodwill decreased from 21,832 million dollars to 21,629 million dollars
2. The percentage decrease is approximately 0.93%
3. The sales returns reserve is based on historical return trends by product and by market as a percent to gross sales

**Gold evidence**

1. `JNJ_FY2015_2016-01-03` · Item 8. FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA › Reclassification · table

   > | Goodwill at December 28, 2014 | $7,675 | 2,626 | 11,531 | 21,832 |

2. `JNJ_FY2015_2016-01-03` · Item 8. FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA › Reclassification · table

   > | Goodwill at January 3, 2016 | $7,240 | 2,889 | 11,500 | 21,629 |

3. `JNJ_FY2015_2016-01-03` · Item 7. MANAGEMENT’S DISCUSSION AND ANALYSIS OF RESULTS OF OPERATIONS AND FINANCIAL CONDITION › Critical Accounting Policies and Estimates · text

   > The returns reserve is based on historical return trends by product and by market as a percent to gross sales.

## Scorecard

| Metric | A (vanilla dense) | B (hybrid + rerank) | C v1 (adaptive multi-hop) | C v2 (agentic multi-hop + XBRL) |
|---|---|---|---|---|
| **Retrieval (RQ1)** | | | | |
| chunks retrieved | 10 | 5 | 13 | 15 |
| recall@5 | 0.33 | 0.33 | 0.00 | 0.00 |
| recall@all | 1.00 | 0.33 | 0.67 | 1.00 |
| complete@all | 1 | 0 | 0 | 1 |
| average precision (lexical) | 0.68 | 1.00 | 0.10 | 0.24 |
| gold evidence first rank | #1: 8, #2: 8, #3: 1 | #1: –, #2: –, #3: 1 | #1: 10, #2: 10, #3: – | #1: 13, #2: 13, #3: 7 |
| **Answer (RQ3 string match)** | | | | |
| numeric_correct | ✓ | ✗ | ✗ | ✗ |
| keypoint_recall | 1.00 | 0.67 | 0.33 | 1.00 |
| **Answer & citations (RQ2)** | | | | |
| numeric_accuracy | 1.00 | 0.00 | 0.00 | 0.00 |
| citation precision | 1.00 | 1.00 | 1.00 | 1.00 |
| citation recall | 1.00 | 1.00 | 0.50 | 0.50 |
| citation F1 | 1.00 | 1.00 | 0.67 | 0.67 |
| has a citation | 1 | 1 | 1 | 1 |
| grounding error rate | – | – | 0.00 | 0.00 |
| **Cost (RQ3)** | | | | |
| retrieval hops | 1 | 1 | 3 | 3 |
| tokens | 1998 | 1615 | 17945 | 15660 |
| cost (USD) | 0.0004 | 0.0003 | 0.0607 | 0.0536 |
| latency (s) | 2.4 | 7.4 | 27.2 | 22.4 |

Definitions: [README › Metrics](../README.md#metrics). `–` = not applicable (e.g. no gold number, no citations, no guardrail).

## System outputs

### System A (vanilla dense)

Model: `gpt-5.4-2026-03-05`. Hops: 1. Chunks retrieved: 10, cited: 3.

**Generated answer**

> Johnson & Johnson’s total goodwill balance decreased from **$21,832 million** at **December 28, 2014** to **$21,629 million** at **January 3, 2016**, a decrease of **$203 million**. That is approximately **0.93%** of the beginning balance (($203 / $21,832) × 100) [8].
>
> The company estimates its **sales returns reserve** based on **historical return trends by product and by market as a percent to gross sales** [1][3].

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `JNJ_FY2015_2016-01-03:136` | Item 7 › Critical Accounting Policies and Estimates | ✓ | #3 | Sales returns allowances represent a reserve for products that may be returned due to expiration, destruction in the field, or in specific areas, product recall. The returns reserve is based on historical return trends b… |
| 2 | `JNJ_FY2015_2016-01-03:68` | Item 7 › Analysis of Consolidated Sales |  |  | In 2015, worldwide sales decreased 5.7% to $70.1 billion, compared to increases of 4.2% in 2014 and 6.1% in 2013. These sales changes consisted of the following: |
| 3 | `JNJ_FY2015_2016-01-03:205` | Item 8 › Revenue Recognition | ✓ | #3 | Sales returns allowances represent a reserve for products that may be returned due to expiration, destruction in the field, or in specific areas, product recall. The returns reserve is based on historical return trends b… |
| 4 | `JNJ_FY2015_2016-01-03:235` | Item 8 › Reclassification |  |  | Goodwill as of January 3, 2016 and December 28, 2014, as allocated by segment of business, was as follows: |
| 5 | `JNJ_FY2015_2016-01-03:422` | Item 8 › 22. Restructuring |  |  | \| (Dollars in Millions) \| Severance \| Asset Write-offs \| Other \| Total \| \|---\|---\|---\|---\|---\| \| 2015 restructuring charge \| $484 \| 86 \| 20 \| 590 \| \| Current year activity \| — \| 86 \| 3 \| 89 \| \| Reserve balance, January 3… |
| 6 | `JNJ_FY2015_2016-01-03:141` | Item 7 › Consumer Segment |  |  | (1) Includes reserve for customer rebates of $31 million at January 3, 2016 and $37 million at December 28, 2014, recorded as a contra asset. |
| 7 | `JNJ_FY2015_2016-01-03:139` | Item 7 › Consumer Segment |  |  | \| (Dollars in Millions) \| Balance at Beginning of Period \| Accruals \| Payments/Credits \| Balance at End of Period \| \|---\|---\|---\|---\|---\| \| 2015 \| \| \| \| \| \| Accrued rebates (1) \| $122 \| 581 \| (564) \| 139 \| \| Accrued retu… |
| 8 | `JNJ_FY2015_2016-01-03:236` | Item 8 › Reclassification | ✓ | #1, #2 | \| (Dollars in Millions) \| Consumer \| Pharmaceutical \| Med Devices \| Total \| \|---\|---\|---\|---\|---\| \| Goodwill at December 29, 2013 \| $8,531 \| 2,068 \| 12,199 \| 22,798 \| \| Goodwill, related to acquisitions \| 13 \| 665 \| — \| … |
| 9 | `JNJ_FY2015_2016-01-03:144` | Item 7 › Pharmaceutical Segment |  |  | (1) Includes reserve for customer rebates of $64 million at January 3, 2016 and $70 million* at December 28, 2014, recorded as a contra asset. *Prior year amount has been reclassified to conform to current year presentat… |
| 10 | `JNJ_FY2015_2016-01-03:99` | Item 7 › Analysis of Consolidated Earnings Before Provision for Taxes on Income |  |  | \| % of Sales \| 2015 \| 2014 \| 2013 \| \|---\|---\|---\|---\| \| Cost of products sold \| 30.7% \| 30.6 \| 31.3 \| \| Percent point increase/(decrease) over the prior year \| 0.1 \| (0.7) \| (0.9) \| \| Selling, marketing and administrativ… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#1 `JNJ_FY2015_2016-01-03:136`** (cited, gold #3)

````text
Item 7. MANAGEMENT’S DISCUSSION AND ANALYSIS OF RESULTS OF OPERATIONS AND FINANCIAL CONDITION > Critical Accounting Policies and Estimates
Sales returns allowances represent a reserve for products that may be returned due to expiration, destruction in the field, or in specific areas, product recall. The returns reserve is based on historical return trends by product and by market as a percent to gross sales. In accordance with the Company’s accounting policies, the Company generally issues credit to customers for returned goods. The Company’s sales returns reserves are accounted for in accordance with the U.S. GAAP guidance for revenue recognition when right of return exists. Sales returns reserves are recorded at full sales value. Sales returns in the Consumer and Pharmaceutical segments are almost exclusively not resalable. Sales returns for certain franchises in the Medical Devices segment are typically resalable but are not material. The Company infrequently exchanges products from inventory for returned products. The sales returns reserve for the total Company has been approximately 1.0% of annual net trade sales during the fiscal reporting years 2015, 2014 and 2013.
````

**#3 `JNJ_FY2015_2016-01-03:205`** (cited, gold #3)

````text
Item 8. FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA > Revenue Recognition
Sales returns allowances represent a reserve for products that may be returned due to expiration, destruction in the field, or in specific areas, product recall. The returns reserve is based on historical return trends by product and by market as a percent to gross sales. In accordance with the Company’s accounting policies, the Company generally issues credit to customers for returned goods. The Company’s sales returns reserves are accounted for in accordance with U.S. GAAP guidance for revenue recognition when right of return exists. Sales returns reserves are recorded at full sales value. Sales returns in the Consumer and Pharmaceutical segments are almost exclusively not resalable. Sales returns for certain franchises in the Medical Devices segment are typically resalable but are not material. The Company infrequently exchanges products from inventory for returned products. The sales returns reserve for the total Company has been approximately 1.0% of annual sales to customers during the fiscal reporting years 2015, 2014 and 2013.
````

**#8 `JNJ_FY2015_2016-01-03:236`** (cited, gold #1, gold #2)

````text
Item 8. FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA > Reclassification (table)
| (Dollars in Millions) | Consumer | Pharmaceutical | Med Devices | Total |
|---|---|---|---|---|
| Goodwill at December 29, 2013 | $8,531 | 2,068 | 12,199 | 22,798 |
| Goodwill, related to acquisitions | 13 | 665 | — | 678 |
| Goodwill, related to divestitures | (138) | — | (603) | (741) |
| Currency translation/other | (731) | (107) | (65) | (903) |
| Goodwill at December 28, 2014 | $7,675 | 2,626 | 11,531 | 21,832 |
| Goodwill, related to acquisitions | 110 | 366 | 34 | 510 |
| Goodwill, related to divestitures | (119) | (17) | (57) | (193) |
| Currency translation/other | (426) | (86) | (8) | (520) |
| Goodwill at January 3, 2016 | $7,240 | 2,889 | 11,500 | 21,629 |
````

</details>

RQ2 citation match (section level): `cited=[('JNJ', 'Item 7'), ('JNJ', 'Item 8')] gold=[(None, 'Item 8'), (None, 'Item 7')]`

### System B (hybrid + rerank)

Model: `gpt-5.4-2026-03-05`. Hops: 1. Chunks retrieved: 5, cited: 2.

**Generated answer**

> I don’t see the total goodwill beginning and ending balances in the provided context, so the percentage decrease cannot be determined from these chunks.
>
> Johnson & Johnson estimates its sales returns reserve based on historical return trends by product and by market as a percent to gross sales; the reserve covers products that may be returned due to expiration, destruction in the field, or in specific areas, product recall [1][2].

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `JNJ_FY2015_2016-01-03:136` | Item 7 › Critical Accounting Policies and Estimates | ✓ | #3 | Sales returns allowances represent a reserve for products that may be returned due to expiration, destruction in the field, or in specific areas, product recall. The returns reserve is based on historical return trends b… |
| 2 | `JNJ_FY2015_2016-01-03:205` | Item 8 › Revenue Recognition | ✓ | #3 | Sales returns allowances represent a reserve for products that may be returned due to expiration, destruction in the field, or in specific areas, product recall. The returns reserve is based on historical return trends b… |
| 3 | `JNJ_FY2015_2016-01-03:79` | Item 7 › Pharmaceutical Segment |  |  | Pharmaceutical segment sales in 2015 were $31.4 billion, a decrease of 2.7% from 2014, which included operational growth of 4.2% offset by a negative currency impact of 6.9%. U.S. sales were $18.3 billion, an increase of… |
| 4 | `JNJ_FY2015_2016-01-03:96` | Item 7 › Analysis of Consolidated Earnings Before Provision for Taxes on Income |  |  | Consolidated earnings before provision for taxes on income decreased to $19.2 billion as compared to $20.6 billion in 2014, a decrease of 6.6%. The decrease was primarily attributable to significantly lower sales of OLYS… |
| 5 | `JNJ_FY2015_2016-01-03:142` | Item 7 › Pharmaceutical Segment |  |  | \| (Dollars in Millions) \| Balance at Beginning of Period \| Accruals \| Payments/Credits \| Balance at End of Period \| \|---\|---\|---\|---\|---\| \| 2015 \| \| \| \| \| \| Accrued rebates (1) \| $2,717 \| 10,449 \| (9,715) \| 3,451 \| \| Acc… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#1 `JNJ_FY2015_2016-01-03:136`** (cited, gold #3)

````text
Item 7. MANAGEMENT’S DISCUSSION AND ANALYSIS OF RESULTS OF OPERATIONS AND FINANCIAL CONDITION > Critical Accounting Policies and Estimates
Sales returns allowances represent a reserve for products that may be returned due to expiration, destruction in the field, or in specific areas, product recall. The returns reserve is based on historical return trends by product and by market as a percent to gross sales. In accordance with the Company’s accounting policies, the Company generally issues credit to customers for returned goods. The Company’s sales returns reserves are accounted for in accordance with the U.S. GAAP guidance for revenue recognition when right of return exists. Sales returns reserves are recorded at full sales value. Sales returns in the Consumer and Pharmaceutical segments are almost exclusively not resalable. Sales returns for certain franchises in the Medical Devices segment are typically resalable but are not material. The Company infrequently exchanges products from inventory for returned products. The sales returns reserve for the total Company has been approximately 1.0% of annual net trade sales during the fiscal reporting years 2015, 2014 and 2013.
````

**#2 `JNJ_FY2015_2016-01-03:205`** (cited, gold #3)

````text
Item 8. FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA > Revenue Recognition
Sales returns allowances represent a reserve for products that may be returned due to expiration, destruction in the field, or in specific areas, product recall. The returns reserve is based on historical return trends by product and by market as a percent to gross sales. In accordance with the Company’s accounting policies, the Company generally issues credit to customers for returned goods. The Company’s sales returns reserves are accounted for in accordance with U.S. GAAP guidance for revenue recognition when right of return exists. Sales returns reserves are recorded at full sales value. Sales returns in the Consumer and Pharmaceutical segments are almost exclusively not resalable. Sales returns for certain franchises in the Medical Devices segment are typically resalable but are not material. The Company infrequently exchanges products from inventory for returned products. The sales returns reserve for the total Company has been approximately 1.0% of annual sales to customers during the fiscal reporting years 2015, 2014 and 2013.
````

</details>

RQ2 citation match (section level): `cited=[('JNJ', 'Item 7'), ('JNJ', 'Item 8')] gold=[(None, 'Item 8'), (None, 'Item 7')]`

### System C v1 (adaptive multi-hop)

Model: `gpt-5.4`. Hops: 3. Chunks retrieved: 13, cited: 1.

**Generated answer**

> Johnson & Johnson’s total goodwill balance decreased from $21,832 at December 28, 2014 to $21,629 at January 3, 2016, a decrease of about 0.9% (($21,832 - $21,629) / $21,832) [JNJ FY2015, Item 8, JNJ_FY2015_2016-01-03:236].  
>
> The filing does not disclose in the provided evidence on what basis the company estimates its sales returns reserve.

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `JNJ_FY2015_2016-01-03:139` | Item 7 › Consumer Segment |  |  | \| (Dollars in Millions) \| Balance at Beginning of Period \| Accruals \| Payments/Credits \| Balance at End of Period \| \|---\|---\|---\|---\|---\| \| 2015 \| \| \| \| \| \| Accrued rebates (1) \| $122 \| 581 \| (564) \| 139 \| \| Accrued retu… |
| 2 | `JNJ_FY2015_2016-01-03:142` | Item 7 › Pharmaceutical Segment |  |  | \| (Dollars in Millions) \| Balance at Beginning of Period \| Accruals \| Payments/Credits \| Balance at End of Period \| \|---\|---\|---\|---\|---\| \| 2015 \| \| \| \| \| \| Accrued rebates (1) \| $2,717 \| 10,449 \| (9,715) \| 3,451 \| \| Acc… |
| 3 | `JNJ_FY2015_2016-01-03:145` | Item 7 › Medical Devices Segment |  |  | \| (Dollars in Millions) \| Balance at Beginning of Period \| Accruals \| Payments/Credits \| Balance at End of Period \| \|---\|---\|---\|---\|---\| \| 2015 \| \| \| \| \| \| Accrued rebates(1) \| $844 \| 5,216 \| (4,871) \| 1,189 \| \| Accrued… |
| 4 | `JNJ_FY2015_2016-01-03:140` | Item 7 › Consumer Segment |  |  | \| (Dollars in Millions) \| Balance at Beginning of Period \| Accruals \| Payments/Credits \| Balance at End of Period \| \|---\|---\|---\|---\|---\| \| Total \| $587 \| 2,791 \| (2,898) \| 480 \| |
| 5 | `JNJ_FY2015_2016-01-03:143` | Item 7 › Pharmaceutical Segment |  |  | \| (Dollars in Millions) \| Balance at Beginning of Period \| Accruals \| Payments/Credits \| Balance at End of Period \| \|---\|---\|---\|---\|---\| \| Total \| $2,609 \| 8,349 \| (7,693) \| 3,265 \| |
| 6 | `JNJ_FY2015_2016-01-03:278` | Item 8 › Reclassification |  |  | \| \| One-Percentage- \| One-Percentage- \| \|---\|---\|---\| \| (Dollars in Millions) \| Point Increase \| Point Decrease \| \| Health Care Plans \| \| \| \| Total interest and service cost \| $36 \| (29) \| \| Post-retirement benefit oblig… |
| 7 | `JNJ_FY2015_2016-01-03:168` | Item 8 › (Dollars in Millions Except Share and Per Share Amounts) (Note 1) |  |  | \| \| 2015 \| 2014 \| \|---\|---\|---\| \| Assets \| \| \| \| Current assets \| \| \| \| Cash and cash equivalents (Notes 1 and 2) \| $13,732 \| 14,523 \| \| Marketable securities (Notes 1 and 2) \| 24,644 \| 18,566 \| \| Accounts receivable tra… |
| 8 | `JNJ_FY2015_2016-01-03:209` | Item 8 › Intangible Assets and Goodwill |  |  | The authoritative literature on U.S. GAAP requires that goodwill and intangible assets with indefinite lives be assessed annually for impairment. The Company completed the annual impairment test for 2015 in the fiscal fo… |
| 9 | `JNJ_FY2015_2016-01-03:234` | Item 8 › Reclassification |  |  | \| (Dollars in Millions) \| 2015 \| 2014 \| \|---\|---\|---\| \| Intangible assets with definite lives: \| \| \| \| Patents and trademarks — gross \| $8,299 \| 9,074 \| \| Less accumulated amortization \| 4,745 \| 4,700 \| \| Patents and tra… |
| 10 | `JNJ_FY2015_2016-01-03:236` | Item 8 › Reclassification | ✓ | #1, #2 | \| (Dollars in Millions) \| Consumer \| Pharmaceutical \| Med Devices \| Total \| \|---\|---\|---\|---\|---\| \| Goodwill at December 29, 2013 \| $8,531 \| 2,068 \| 12,199 \| 22,798 \| \| Goodwill, related to acquisitions \| 13 \| 665 \| — \| … |
| 11 | `JNJ_FY2015_2016-01-03:182` | Item 8 › (Dollars in Millions) (Note 1) |  |  | \| \| 2015 \| 2014 \| 2013 \| \|---\|---\|---\|---\| \| Decrease/(Increase) in other current and non-current assets \| 65 \| 442 \| (1,693) \| \| Increase/(Decrease) in other current and non-current liabilities \| 2,159 \| (1,096) \| 298 \|… |
| 12 | `JNJ_FY2015_2016-01-03:187` | Item 8 › NOTES TO CONSOLIDATED FINANCIAL STATEMENTS |  |  | 1. Summary of Significant Accounting Policies |
| 13 | `JNJ_FY2015_2016-01-03:181` | Item 8 › (Dollars in Millions) (Note 1) |  |  | \| \| 2015 \| 2014 \| 2013 \| \|---\|---\|---\|---\| \| Cash flows from operating activities \| \| \| \| \| Net earnings \| $15,409 \| 16,323 \| 13,831 \| \| Adjustments to reconcile net earnings to cash flows from operating activities: \| \| … |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#10 `JNJ_FY2015_2016-01-03:236`** (cited, gold #1, gold #2)

````text
Item 8. FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA > Reclassification (table)
| (Dollars in Millions) | Consumer | Pharmaceutical | Med Devices | Total |
|---|---|---|---|---|
| Goodwill at December 29, 2013 | $8,531 | 2,068 | 12,199 | 22,798 |
| Goodwill, related to acquisitions | 13 | 665 | — | 678 |
| Goodwill, related to divestitures | (138) | — | (603) | (741) |
| Currency translation/other | (731) | (107) | (65) | (903) |
| Goodwill at December 28, 2014 | $7,675 | 2,626 | 11,531 | 21,832 |
| Goodwill, related to acquisitions | 110 | 366 | 34 | 510 |
| Goodwill, related to divestitures | (119) | (17) | (57) | (193) |
| Currency translation/other | (426) | (86) | (8) | (520) |
| Goodwill at January 3, 2016 | $7,240 | 2,889 | 11,500 | 21,629 |
````

</details>

RQ2 citation match (section level): `cited=[('JNJ', 'Item 8')] gold=[(None, 'Item 8'), (None, 'Item 7')]`

**System C guardrail** (judge `gpt-5.4`): numerical claims 6, verified 6, ungrounded 0, uncited 0, derived 1; sentence verdicts: supported 1, partial 0, unsupported 0, unchecked 0.


<details><summary>Guardrail sentence verdicts</summary>

| sentence | verdict | judge reason |
|---|---|---|
| Johnson & Johnson’s total goodwill balance decreased from $21,832 at December 28, 2014 to $21,629 at January 3, 2016, a decrease of about 0.9% (($21,832 - $21,629) / $21,832) [JNJ FY2015, Item 8, JNJ_FY2015_2016-01-03:236]. | None |  |
| The filing does not disclose in the provided evidence on what basis the company estimates its sales returns reserve. | supported | The retrieved evidence shows accrued returns balances but does not disclose the basis used to estimate the sales returns reserve. |

</details>

### System C v2 (agentic multi-hop + XBRL)

Model: `gpt-5.4`. Hops: 3. Chunks retrieved: 15, cited: 3.

**Generated answer**

> Johnson & Johnson’s total goodwill balance decreased from $21,832 at December 28, 2014 to $21,629 at January 3, 2016, a decrease of approximately 0.9% [JNJ FY2015, Item 8, JNJ_FY2015_2016-01-03:236].  
>
> The company estimates its sales returns reserve based on historical return trends by product and by market as a percent to gross sales, and it generally estimates and records sales returns based on historical sales and returns information [JNJ FY2015, Item 8, JNJ_FY2015_2016-01-03:205] [JNJ FY2015, Item 8, JNJ_FY2015_2016-01-03:204].

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `JNJ_FY2015_2016-01-03:139` | Item 7 › Consumer Segment |  |  | \| (Dollars in Millions) \| Balance at Beginning of Period \| Accruals \| Payments/Credits \| Balance at End of Period \| \|---\|---\|---\|---\|---\| \| 2015 \| \| \| \| \| \| Accrued rebates (1) \| $122 \| 581 \| (564) \| 139 \| \| Accrued retu… |
| 2 | `JNJ_FY2015_2016-01-03:142` | Item 7 › Pharmaceutical Segment |  |  | \| (Dollars in Millions) \| Balance at Beginning of Period \| Accruals \| Payments/Credits \| Balance at End of Period \| \|---\|---\|---\|---\|---\| \| 2015 \| \| \| \| \| \| Accrued rebates (1) \| $2,717 \| 10,449 \| (9,715) \| 3,451 \| \| Acc… |
| 3 | `JNJ_FY2015_2016-01-03:145` | Item 7 › Medical Devices Segment |  |  | \| (Dollars in Millions) \| Balance at Beginning of Period \| Accruals \| Payments/Credits \| Balance at End of Period \| \|---\|---\|---\|---\|---\| \| 2015 \| \| \| \| \| \| Accrued rebates(1) \| $844 \| 5,216 \| (4,871) \| 1,189 \| \| Accrued… |
| 4 | `JNJ_FY2015_2016-01-03:140` | Item 7 › Consumer Segment |  |  | \| (Dollars in Millions) \| Balance at Beginning of Period \| Accruals \| Payments/Credits \| Balance at End of Period \| \|---\|---\|---\|---\|---\| \| Total \| $587 \| 2,791 \| (2,898) \| 480 \| |
| 5 | `JNJ_FY2015_2016-01-03:143` | Item 7 › Pharmaceutical Segment |  |  | \| (Dollars in Millions) \| Balance at Beginning of Period \| Accruals \| Payments/Credits \| Balance at End of Period \| \|---\|---\|---\|---\|---\| \| Total \| $2,609 \| 8,349 \| (7,693) \| 3,265 \| |
| 6 | `JNJ_FY2015_2016-01-03:278` | Item 8 › Reclassification |  |  | \| \| One-Percentage- \| One-Percentage- \| \|---\|---\|---\| \| (Dollars in Millions) \| Point Increase \| Point Decrease \| \| Health Care Plans \| \| \| \| Total interest and service cost \| $36 \| (29) \| \| Post-retirement benefit oblig… |
| 7 | `JNJ_FY2015_2016-01-03:205` | Item 8 › Revenue Recognition | ✓ | #3 | Sales returns allowances represent a reserve for products that may be returned due to expiration, destruction in the field, or in specific areas, product recall. The returns reserve is based on historical return trends b… |
| 8 | `JNJ_FY2015_2016-01-03:136` | Item 7 › Critical Accounting Policies and Estimates |  | #3 | Sales returns allowances represent a reserve for products that may be returned due to expiration, destruction in the field, or in specific areas, product recall. The returns reserve is based on historical return trends b… |
| 9 | `JNJ_FY2015_2016-01-03:209` | Item 8 › Intangible Assets and Goodwill |  |  | The authoritative literature on U.S. GAAP requires that goodwill and intangible assets with indefinite lives be assessed annually for impairment. The Company completed the annual impairment test for 2015 in the fiscal fo… |
| 10 | `JNJ_FY2015_2016-01-03:168` | Item 8 › (Dollars in Millions Except Share and Per Share Amounts) (Note 1) |  |  | \| \| 2015 \| 2014 \| \|---\|---\|---\| \| Assets \| \| \| \| Current assets \| \| \| \| Cash and cash equivalents (Notes 1 and 2) \| $13,732 \| 14,523 \| \| Marketable securities (Notes 1 and 2) \| 24,644 \| 18,566 \| \| Accounts receivable tra… |
| 11 | `JNJ_FY2015_2016-01-03:234` | Item 8 › Reclassification |  |  | \| (Dollars in Millions) \| 2015 \| 2014 \| \|---\|---\|---\| \| Intangible assets with definite lives: \| \| \| \| Patents and trademarks — gross \| $8,299 \| 9,074 \| \| Less accumulated amortization \| 4,745 \| 4,700 \| \| Patents and tra… |
| 12 | `JNJ_FY2015_2016-01-03:204` | Item 8 › Revenue Recognition | ✓ | #3 | The Company recognizes revenue from product sales when the goods are shipped or delivered and title and risk of loss pass to the customer. Provisions for certain rebates, sales incentives, trade promotions, coupons, prod… |
| 13 | `JNJ_FY2015_2016-01-03:236` | Item 8 › Reclassification | ✓ | #1, #2 | \| (Dollars in Millions) \| Consumer \| Pharmaceutical \| Med Devices \| Total \| \|---\|---\|---\|---\|---\| \| Goodwill at December 29, 2013 \| $8,531 \| 2,068 \| 12,199 \| 22,798 \| \| Goodwill, related to acquisitions \| 13 \| 665 \| — \| … |
| 14 | `JNJ_FY2015_2016-01-03:179` | Item 8 › (Dollars in Millions) (Note 1) |  |  | \| \| Total \| Retained Earnings \| Accumulated Other Comprehensive Income \| Common Stock Issued Amount \| Treasury Stock Amount \| \|---\|---\|---\|---\|---\|---\| \| Other comprehensive income (loss), net of tax \| (7,862) \| \| (7,862… |
| 15 | `JNJ_FY2015_2016-01-03:178` | Item 8 › (Dollars in Millions) (Note 1) |  |  | \| \| Total \| Retained Earnings \| Accumulated Other Comprehensive Income \| Common Stock Issued Amount \| Treasury Stock Amount \| \|---\|---\|---\|---\|---\|---\| \| Balance, December 30, 2012 \| $64,826 \| 85,992 \| (5,810) \| 3,120 \| … |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#7 `JNJ_FY2015_2016-01-03:205`** (cited, gold #3)

````text
Item 8. FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA > Revenue Recognition
Sales returns allowances represent a reserve for products that may be returned due to expiration, destruction in the field, or in specific areas, product recall. The returns reserve is based on historical return trends by product and by market as a percent to gross sales. In accordance with the Company’s accounting policies, the Company generally issues credit to customers for returned goods. The Company’s sales returns reserves are accounted for in accordance with U.S. GAAP guidance for revenue recognition when right of return exists. Sales returns reserves are recorded at full sales value. Sales returns in the Consumer and Pharmaceutical segments are almost exclusively not resalable. Sales returns for certain franchises in the Medical Devices segment are typically resalable but are not material. The Company infrequently exchanges products from inventory for returned products. The sales returns reserve for the total Company has been approximately 1.0% of annual sales to customers during the fiscal reporting years 2015, 2014 and 2013.
````

**#8 `JNJ_FY2015_2016-01-03:136`** (gold #3)

````text
Item 7. MANAGEMENT’S DISCUSSION AND ANALYSIS OF RESULTS OF OPERATIONS AND FINANCIAL CONDITION > Critical Accounting Policies and Estimates
Sales returns allowances represent a reserve for products that may be returned due to expiration, destruction in the field, or in specific areas, product recall. The returns reserve is based on historical return trends by product and by market as a percent to gross sales. In accordance with the Company’s accounting policies, the Company generally issues credit to customers for returned goods. The Company’s sales returns reserves are accounted for in accordance with the U.S. GAAP guidance for revenue recognition when right of return exists. Sales returns reserves are recorded at full sales value. Sales returns in the Consumer and Pharmaceutical segments are almost exclusively not resalable. Sales returns for certain franchises in the Medical Devices segment are typically resalable but are not material. The Company infrequently exchanges products from inventory for returned products. The sales returns reserve for the total Company has been approximately 1.0% of annual net trade sales during the fiscal reporting years 2015, 2014 and 2013.
````

**#12 `JNJ_FY2015_2016-01-03:204`** (cited, gold #3)

````text
Item 8. FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA > Revenue Recognition
The Company recognizes revenue from product sales when the goods are shipped or delivered and title and risk of loss pass to the customer. Provisions for certain rebates, sales incentives, trade promotions, coupons, product returns and discounts to customers are accounted for as reductions in sales in the same period the related sales are recorded. Product discounts granted are based on the terms of arrangements with direct, indirect and other market participants, as well as market conditions, including prices charged by competitors. Rebates, which include Medicaid, are estimated based on contractual terms, historical experience, patient outcomes, trend analysis and projected market conditions in the various markets served. The Company evaluates market conditions for products or groups of products primarily through the analysis of wholesaler and other third-party sell-through and market research data, as well as internally generated information. Sales returns are generally estimated and recorded based on historical sales and returns information. Products that exhibit unusual sales or return patterns due to dating, competition or other marketing matters are specifically investigated and analyzed as part of the accounting for sales returns accruals.
````

**#13 `JNJ_FY2015_2016-01-03:236`** (cited, gold #1, gold #2)

````text
Item 8. FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA > Reclassification (table)
| (Dollars in Millions) | Consumer | Pharmaceutical | Med Devices | Total |
|---|---|---|---|---|
| Goodwill at December 29, 2013 | $8,531 | 2,068 | 12,199 | 22,798 |
| Goodwill, related to acquisitions | 13 | 665 | — | 678 |
| Goodwill, related to divestitures | (138) | — | (603) | (741) |
| Currency translation/other | (731) | (107) | (65) | (903) |
| Goodwill at December 28, 2014 | $7,675 | 2,626 | 11,531 | 21,832 |
| Goodwill, related to acquisitions | 110 | 366 | 34 | 510 |
| Goodwill, related to divestitures | (119) | (17) | (57) | (193) |
| Currency translation/other | (426) | (86) | (8) | (520) |
| Goodwill at January 3, 2016 | $7,240 | 2,889 | 11,500 | 21,629 |
````

</details>

RQ2 citation match (section level): `cited=[('JNJ', 'Item 8')] gold=[(None, 'Item 8'), (None, 'Item 7')]`

**System C guardrail** (judge `gpt-5.4`): numerical claims 3, verified 3, ungrounded 0, uncited 0, derived 1; sentence verdicts: supported 1, partial 0, unsupported 0, unchecked 0.


<details><summary>Guardrail sentence verdicts</summary>

| sentence | verdict | judge reason |
|---|---|---|
| Johnson & Johnson’s total goodwill balance decreased from $21,832 at December 28, 2014 to $21,629 at January 3, 2016, a decrease of approximately 0.9% [JNJ FY2015, Item 8, JNJ_FY2015_2016-01-03:236]. | None |  |
| The company estimates its sales returns reserve based on historical return trends by product and by market as a percent to gross sales, and it generally estimates and records sales returns based on historical sales and returns information [JNJ FY2015, Item 8, JNJ_FY2015_2016-01-03:205] [JNJ FY2015, Item 8, JNJ_FY2015_2016-01-03:204]. | supported | The cited passages explicitly state both that the returns reserve is based on historical return trends by product and market as a percent of gross sales and that sales returns are generally estimated and recorded based on historical sales and returns information. |

</details>
