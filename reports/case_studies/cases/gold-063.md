# gold-063: Table + text (one filing)

[← all cases](../README.md) · company: JOHNSON & JOHNSON (JNJ) · fiscal year: 2016 · recipe `table_text` · hop `multi` · answer type `mixed` · scope `single_doc` · RQ2 category `cross_section_multihop`

## Gold QA

**Question**

> For Johnson & Johnson's fiscal year 2016, what was the increase in total Goodwill (in millions) compared to the balance at the beginning of the fiscal year (January 3, 2016), and what were the primary drivers for the increase in the Pharmaceutical segment's income before tax as a percent of sales compared to 2015?

**Gold answer**

> Goodwill increased by $1,176 million, from $21,629 million at January 3, 2016 to $22,805 million at January 1, 2017. The Pharmaceutical segment's income before tax as a percent of sales rose to 38.3% from 37.3%, primarily due to strong sales volume growth and favorable selling, marketing and administrative expenses due to cost management.

**Program**: `subtract(22805, 21629)` → `1176.0`

**Gold numbers** (RQ2 numeric_accuracy targets): $1,176 million

**Key points** (RQ3 keypoint_recall targets)

1. The increase in total Goodwill was $1,176 million.
2. The Pharmaceutical segment's income before tax as a percent of sales increased to 38.3% in 2016 from 37.3% in 2015.
3. The increase was driven by strong sales volume growth.
4. The increase was driven by favorable selling, marketing and administrative expenses due to cost management.

**Gold evidence**

1. `JNJ_FY2016_2017-01-01` · Item 8. FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA › Reclassification · table

   > Goodwill at January 3, 2016 | $7,240 | 2,889 | 11,500 | 21,629

2. `JNJ_FY2016_2017-01-01` · Item 8. FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA › Reclassification · table

   > Goodwill at January 1, 2017 | $8,263 | 2,840 | 11,702 | 22,805

3. `JNJ_FY2016_2017-01-01` · Item 7. MANAGEMENT’S DISCUSSION AND ANALYSIS OF RESULTS OF OPERATIONS AND FINANCIAL CONDITION › Income Before Tax by Segment · text

   > The increase in income before tax was primarily due to strong sales volume growth and favorable selling, marketing and administrative expenses due to cost management.

4. `JNJ_FY2016_2017-01-01` · Item 7. MANAGEMENT’S DISCUSSION AND ANALYSIS OF RESULTS OF OPERATIONS AND FINANCIAL CONDITION › Income Before Tax by Segment · text

   > In 2016, the Pharmaceutical segment income before tax as a percent to sales was 38.3% versus 37.3% in 2015.

## Scorecard

| Metric | A (vanilla dense) | B (hybrid + rerank) | C v1 (adaptive multi-hop) | C v2 (agentic multi-hop + XBRL) |
|---|---|---|---|---|
| **Retrieval (RQ1)** | | | | |
| chunks retrieved | 10 | 5 | 12 | 13 |
| recall@5 | 0.50 | 0.50 | 0.50 | 0.50 |
| recall@all | 1.00 | 0.50 | 1.00 | 1.00 |
| complete@all | 1 | 0 | 1 | 1 |
| average precision (lexical) | 0.75 | 0.95 | 0.37 | 0.31 |
| gold evidence first rank | #1: 6, #2: 6, #3: 1, #4: 1 | #1: –, #2: –, #3: 1, #4: 1 | #1: 3, #2: 3, #3: 8, #4: 7 | #1: 3, #2: 3, #3: 10, #4: 8 |
| **Answer (RQ3 string match)** | | | | |
| numeric_correct | ✓ | ✗ | ✓ | ✓ |
| keypoint_recall | 1.00 | 0.00 | 1.00 | 1.00 |
| **Answer & citations (RQ2)** | | | | |
| numeric_accuracy | 1.00 | 0.00 | 1.00 | 1.00 |
| citation precision | 1.00 | – | 1.00 | 1.00 |
| citation recall | 1.00 | – | 1.00 | 1.00 |
| citation F1 | 1.00 | – | 1.00 | 1.00 |
| has a citation | 1 | 0 | 1 | 1 |
| grounding error rate | – | – | 0.00 | 0.00 |
| **Cost (RQ3)** | | | | |
| retrieval hops | 1 | 1 | 2 | 2 |
| tokens | 2696 | 1429 | 10749 | 11753 |
| cost (USD) | 0.0005 | 0.0002 | 0.0390 | 0.0430 |
| latency (s) | 3.1 | 5.8 | 16.6 | 18.4 |

Definitions: [README › Metrics](../README.md#metrics). `–` = not applicable (e.g. no gold number, no citations, no guardrail).

## System outputs

### System A (vanilla dense)

Model: `gpt-5.4-2026-03-05`. Hops: 1. Chunks retrieved: 10, cited: 2.

**Generated answer**

> Total goodwill increased by **$1,176 million** in fiscal 2016, from **$21,629 million** at January 3, 2016 to **$22,805 million** at January 1, 2017 [6].
>
> The Pharmaceutical segment’s income before tax as a percent of sales increased to **38.3% in 2016 from 37.3% in 2015**. The primary drivers were:
> - **Strong sales volume growth**
> - **Favorable selling, marketing and administrative expenses due to cost management** [1]
>
> The context also notes that **2015 had higher divestiture gains ($0.7 billion)**, partially offset by a **higher IPR&D charge ($0.2 billion)** compared with 2016 [1].

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `JNJ_FY2016_2017-01-01:150` | Item 7 › Income Before Tax by Segment | ✓ | #3, #4 | Pharmaceutical Segment: In 2016, the Pharmaceutical segment income before tax as a percent to sales was 38.3% versus 37.3% in 2015. The increase in income before tax was primarily due to strong sales volume growth and fa… |
| 2 | `JNJ_FY2016_2017-01-01:134` | Item 7 › Analysis of Consolidated Earnings Before Provision for Taxes on Income |  | #3, #4 | Consolidated earnings before provision for taxes on income increased to $19.8 billion in 2016, as compared to $19.2 billion in 2015, an increase of 3.2%. The increase was primarily attributable to higher sales volume, fa… |
| 3 | `JNJ_FY2016_2017-01-01:283` | Item 8 › Reclassification |  |  | Goodwill as of January 1, 2017 and January 3, 2016, as allocated by segment of business, was as follows: |
| 4 | `JNJ_FY2016_2017-01-01:145` | Item 7 › Analysis of Consolidated Earnings Before Provision for Taxes on Income |  |  | Interest expense in 2016 was higher as compared to 2015. The average debt balance was $23.5 billion in 2016 versus $19.3 billion in 2015. The total debt balance at the end of 2016 was $27.1 billion as compared to $19.9 b… |
| 5 | `JNJ_FY2016_2017-01-01:140` | Item 7 › Analysis of Consolidated Earnings Before Provision for Taxes on Income |  |  | \| \| 2016 \| \| 2015 \| \| 2014 \| \| \|---\|---\|---\|---\|---\|---\|---\| \| (Dollars in Millions) \| Amount \| % of Sales* \| Amount \| % of Sales* \| Amount \| % of Sales* \| \| Consumer \| $580 \| 4.4% \| 625 \| 4.6 \| 629 \| 4.3 \| \| Pharmaceuti… |
| 6 | `JNJ_FY2016_2017-01-01:284` | Item 8 › Reclassification | ✓ | #1, #2 | \| (Dollars in Millions) \| Consumer \| Pharmaceutical \| Med Devices \| Total \| \|---\|---\|---\|---\|---\| \| Goodwill at December 28, 2014 \| $7,675 \| 2,626 \| 11,531 \| 21,832 \| \| Goodwill, related to acquisitions \| 110 \| 366 \| 34 … |
| 7 | `JNJ_FY2016_2017-01-01:144` | Item 7 › Analysis of Consolidated Earnings Before Provision for Taxes on Income |  |  | The change in other (income) expense, net for the fiscal year 2015 was a favorable change of $2.0 billion as compared to the prior year primarily due to lower litigation expense of $1.1 billion, lower Synthes integration… |
| 8 | `JNJ_FY2016_2017-01-01:148` | Item 7 › Income Before Tax by Segment |  | #4 | \| \| Income Before Tax \| \| Segment Sales \| \| Percent of Segment Sales \| \| \|---\|---\|---\|---\|---\|---\|---\| \| (Dollars in Millions) \| 2016 \| 2015 \| 2016 \| 2015 \| 2016 \| 2015 \| \| Consumer \| $2,441 \| 1,787 \| $13,307 \| 13,507 \| … |
| 9 | `JNJ_FY2016_2017-01-01:137` | Item 7 › Analysis of Consolidated Earnings Before Provision for Taxes on Income |  |  | \| % of Sales \| 2016 \| 2015 \| 2014 \| \|---\|---\|---\|---\| \| Cost of products sold \| 30.2% \| 30.7 \| 30.6 \| \| Percent point increase/(decrease) over the prior year \| (0.5) \| 0.1 \| (0.7) \| \| Selling, marketing and administrativ… |
| 10 | `JNJ_FY2016_2017-01-01:146` | Item 7 › Analysis of Consolidated Earnings Before Provision for Taxes on Income |  |  | Interest expense in 2015 increased slightly as compared to 2014. The average debt balance was $19.3 billion in 2015 versus $18.5 billion in 2014. The total debt balance at the end of 2015 was $19.9 billion as compared to… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#1 `JNJ_FY2016_2017-01-01:150`** (cited, gold #3, gold #4)

````text
Item 7. MANAGEMENT’S DISCUSSION AND ANALYSIS OF RESULTS OF OPERATIONS AND FINANCIAL CONDITION > Income Before Tax by Segment
Pharmaceutical Segment: In 2016, the Pharmaceutical segment income before tax as a percent to sales was 38.3% versus 37.3% in 2015. The increase in income before tax was primarily due to strong sales volume growth and favorable selling, marketing and administrative expenses due to cost management. Additionally, the fiscal year 2015, had higher gains of $0.7 billion related to divestitures partially offset by a higher IPR&D charge of $0.2 billion as compared to 2016. The fiscal year of 2016 included the gains from the divestitures of the controlled substance raw material and API business and certain anesthetic products in Europe versus the gains recorded in 2015 from the U.S. divestiture of NUCYNTA®.
````

**#2 `JNJ_FY2016_2017-01-01:134`** (gold #3, gold #4)

````text
Item 7. MANAGEMENT’S DISCUSSION AND ANALYSIS OF RESULTS OF OPERATIONS AND FINANCIAL CONDITION > Analysis of Consolidated Earnings Before Provision for Taxes on Income
Consolidated earnings before provision for taxes on income increased to $19.8 billion in 2016, as compared to $19.2 billion in 2015, an increase of 3.2%. The increase was primarily attributable to higher sales volume, favorable mix in the business and lower selling, marketing and administrative costs. This was partially offset by higher net litigation expense of $0.7 billion and a higher restructuring charge of $0.1 billion as compared to 2015. Additionally, the fiscal year 2015 included higher gains on the sale of assets/businesses as compared to 2016. The fiscal year of 2016 included gains of $0.6 billion from the divestitures of the controlled substance raw material and API business, certain anesthetic products in Europe and certain non-strategic Consumer brands versus gains of $2.6 billion recorded in 2015 primarily from the divestiture of the Cordis business, the U.S. divestiture of NUCYNTA® and the SPLENDA® brand. This was partially offset by a $0.3 billion intangible asset write-down related to Acclarent included in 2015.
````

**#6 `JNJ_FY2016_2017-01-01:284`** (cited, gold #1, gold #2)

````text
Item 8. FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA > Reclassification (table)
| (Dollars in Millions) | Consumer | Pharmaceutical | Med Devices | Total |
|---|---|---|---|---|
| Goodwill at December 28, 2014 | $7,675 | 2,626 | 11,531 | 21,832 |
| Goodwill, related to acquisitions | 110 | 366 | 34 | 510 |
| Goodwill, related to divestitures | (119) | (17) | (57) | (193) |
| Currency translation/other | (426) | (86) | (8) | (520) |
| Goodwill at January 3, 2016 | $7,240 | 2,889 | 11,500 | 21,629 |
| Goodwill, related to acquisitions | 1,362 | — | 210 | 1,572 |
| Goodwill, related to divestitures | (63) | (12) | — | (75) |
| Currency translation/other | (276) | (37) | (8) | (321) |
| Goodwill at January 1, 2017 | $8,263 | 2,840 | 11,702 | 22,805 |
````

**#8 `JNJ_FY2016_2017-01-01:148`** (gold #4)

````text
Item 7. MANAGEMENT’S DISCUSSION AND ANALYSIS OF RESULTS OF OPERATIONS AND FINANCIAL CONDITION > Income Before Tax by Segment (table)
|  | Income Before Tax |  | Segment Sales |  | Percent of Segment Sales |  |
|---|---|---|---|---|---|---|
| (Dollars in Millions) | 2016 | 2015 | 2016 | 2015 | 2016 | 2015 |
| Consumer | $2,441 | 1,787 | $13,307 | 13,507 | 18.3% | 13.2 |
| Pharmaceutical | 12,827 | 11,734 | 33,464 | 31,430 | 38.3 | 37.3 |
| Medical Devices | 5,578 | 6,826 | 25,119 | 25,137 | 22.2 | 27.2 |
| Total (1) | 20,846 | 20,347 | 71,890 | 70,074 | 29.0 | 29.0 |
| Less: Expenses not allocated to segments (2) | 1,043 | 1,151 |  |  |  |  |
| Earnings before provision for taxes on income | $19,803 | 19,196 | $71,890 | 70,074 | 27.5% | 27.4 |
````

</details>

RQ2 citation match (section level): `cited=[('JNJ', 'Item 7'), ('JNJ', 'Item 8')] gold=[(None, 'Item 8'), (None, 'Item 7')]`

### System B (hybrid + rerank)

Model: `gpt-5.4-2026-03-05`. Hops: 1. Chunks retrieved: 5, cited: 0.

**Generated answer**

> Not found in the provided context.

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `JNJ_FY2016_2017-01-01:150` | Item 7 › Income Before Tax by Segment |  | #3, #4 | Pharmaceutical Segment: In 2016, the Pharmaceutical segment income before tax as a percent to sales was 38.3% versus 37.3% in 2015. The increase in income before tax was primarily due to strong sales volume growth and fa… |
| 2 | `JNJ_FY2016_2017-01-01:151` | Item 7 › Income Before Tax by Segment |  | #4 | In 2015, the Pharmaceutical segment income before tax as a percent to sales was 37.3% versus 36.2% in 2014. The favorable income before tax was primarily due to higher gains recognized in 2015 partially offset by a sales… |
| 3 | `JNJ_FY2016_2017-01-01:141` | Item 7 › Analysis of Consolidated Earnings Before Provision for Taxes on Income |  | #4 | As a percent to segment sales Research and development activities represent a significant part of the Company's business. These expenditures relate to the processes of discovering, testing and developing new products, up… |
| 4 | `JNJ_FY2016_2017-01-01:115` | Item 7 › Pharmaceutical Segment |  |  | Pharmaceutical segment sales in 2016 were $33.5 billion, an increase of 6.5% from 2015, which included operational growth of 7.4% partially offset by a negative currency impact of 0.9%. U.S. sales were $20.1 billion, an … |
| 5 | `JNJ_FY2016_2017-01-01:149` | Item 7 › Income Before Tax by Segment |  | #3, #4 | (1) See Note 18 to the Consolidated Financial Statements for more details. (2) Amounts not allocated to segments include interest (income) expense and general corporate (income) expense. Consumer Segment: In 2016, the Co… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#1 `JNJ_FY2016_2017-01-01:150`** (gold #3, gold #4)

````text
Item 7. MANAGEMENT’S DISCUSSION AND ANALYSIS OF RESULTS OF OPERATIONS AND FINANCIAL CONDITION > Income Before Tax by Segment
Pharmaceutical Segment: In 2016, the Pharmaceutical segment income before tax as a percent to sales was 38.3% versus 37.3% in 2015. The increase in income before tax was primarily due to strong sales volume growth and favorable selling, marketing and administrative expenses due to cost management. Additionally, the fiscal year 2015, had higher gains of $0.7 billion related to divestitures partially offset by a higher IPR&D charge of $0.2 billion as compared to 2016. The fiscal year of 2016 included the gains from the divestitures of the controlled substance raw material and API business and certain anesthetic products in Europe versus the gains recorded in 2015 from the U.S. divestiture of NUCYNTA®.
````

**#2 `JNJ_FY2016_2017-01-01:151`** (gold #4)

````text
Item 7. MANAGEMENT’S DISCUSSION AND ANALYSIS OF RESULTS OF OPERATIONS AND FINANCIAL CONDITION > Income Before Tax by Segment
In 2015, the Pharmaceutical segment income before tax as a percent to sales was 37.3% versus 36.2% in 2014. The favorable income before tax was primarily due to higher gains recognized in 2015 partially offset by a sales decline of OLYSIO®/SOVRIAD®(simeprevir), increased investment spending and negative currency impacts as compared to 2014. Included in 2015 was a gain of $1.0 billion on the U.S. divestiture of NUCYNTA®, as well as receipt of a contingent payment and a positive adjustment to previous reserve estimates, including Managed Medicaid rebates. Additionally, the Pharmaceutical segment income before tax in 2014 was negatively impacted by $0.2 billion for an additional year of the Branded Prescription Drug Fee and higher intangible asset amortization expense of $0.3 billion primarily related to the write-down of INCIVO® (telaprevir).
````

**#3 `JNJ_FY2016_2017-01-01:141`** (gold #4)

````text
Item 7. MANAGEMENT’S DISCUSSION AND ANALYSIS OF RESULTS OF OPERATIONS AND FINANCIAL CONDITION > Analysis of Consolidated Earnings Before Provision for Taxes on Income
As a percent to segment sales Research and development activities represent a significant part of the Company's business. These expenditures relate to the processes of discovering, testing and developing new products, upfront payments and milestones, improving existing products, as well as ensuring product efficacy and regulatory compliance prior to launch. The Company remains committed to investing in research and development with the aim of delivering high quality and innovative products. In 2016, worldwide costs of research and development activities increased by 0.5% compared to 2015 but decreased as a percent of sales. The decrease as a percent of sales was attributable to higher overall sales in the Pharmaceutical segment. The increased dollar spend in the Pharmaceutical segment was for investment spending to advance the pipeline. In 2015, worldwide costs of research and development activities increased by 6.5% compared to 2014. The increase as a percent to sales was attributable to increased investment spending primarily in the Pharmaceutical segment, lower overall sales and business mix.
````

**#5 `JNJ_FY2016_2017-01-01:149`** (gold #3, gold #4)

````text
Item 7. MANAGEMENT’S DISCUSSION AND ANALYSIS OF RESULTS OF OPERATIONS AND FINANCIAL CONDITION > Income Before Tax by Segment
(1) See Note 18 to the Consolidated Financial Statements for more details. (2) Amounts not allocated to segments include interest (income) expense and general corporate (income) expense. Consumer Segment: In 2016, the Consumer segment income before tax as a percent to sales was 18.3%, versus 13.2% in 2015, primarily driven by favorable selling, marketing and administrative expenses due to cost management and higher gross profit margins from cost improvement projects and favorable mix. This was partially offset by higher gains in 2015 related to divestitures, primarily the divestiture of the SPLENDA® brand. Additionally, operations in Venezuela negatively impacted the Consumer segment income before tax in 2016 as compared to 2015. In 2015, the Consumer segment income before tax as a percent to sales was 13.2%, versus 13.4% in 2014, primarily due to lower divestiture gains in 2015 versus 2014. In 2015, the Consumer segment tax included a gain of $0.3 billion from divestitures, primarily the divestiture of the SPLENDA® brand. In 2014, the Consumer segment included a gain $0.5 billion from divestitures, primarily the divestiture of the K-Y® brand.
````

</details>

RQ2 citation match (section level): `no citations`

### System C v1 (adaptive multi-hop)

Model: `gpt-5.4`. Hops: 2. Chunks retrieved: 12, cited: 2.

**Generated answer**

> Total goodwill increased by $1,176 million in fiscal 2016, rising from $21,629 million at January 3, 2016 to $22,805 million at January 1, 2017 [JNJ FY2016, Item 8, JNJ_FY2016_2017-01-01:284].  
>
> The Pharmaceutical segment’s income before tax as a percent of sales increased to 38.3% in 2016 from 37.3% in 2015, primarily due to strong sales volume growth and favorable selling, marketing and administrative expenses due to cost management [JNJ FY2016, Item 7, JNJ_FY2016_2017-01-01:150].  
>
> The filing also states that fiscal 2015 had higher gains of $0.7 billion related to divestitures, partially offset by a higher IPR&D charge of $0.2 billion as compared to 2016 [JNJ FY2016, Item 7, JNJ_FY2016_2017-01-01:150].

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `JNJ_FY2016_2017-01-01:283` | Item 8 › Reclassification |  |  | Goodwill as of January 1, 2017 and January 3, 2016, as allocated by segment of business, was as follows: |
| 2 | `JNJ_FY2016_2017-01-01:235` | Item 8 › Not Adopted as of January 1, 2017 |  |  | During the fiscal first quarter of 2017, the FASB issued Accounting Standard Update 2017-04: Simplifying the Test for Goodwill Impairment. This update simplifies how an entity is required to test goodwill for impairment.… |
| 3 | `JNJ_FY2016_2017-01-01:284` | Item 8 › Reclassification | ✓ | #1, #2 | \| (Dollars in Millions) \| Consumer \| Pharmaceutical \| Med Devices \| Total \| \|---\|---\|---\|---\|---\| \| Goodwill at December 28, 2014 \| $7,675 \| 2,626 \| 11,531 \| 21,832 \| \| Goodwill, related to acquisitions \| 110 \| 366 \| 34 … |
| 4 | `JNJ_FY2016_2017-01-01:145` | Item 7 › Analysis of Consolidated Earnings Before Provision for Taxes on Income |  |  | Interest expense in 2016 was higher as compared to 2015. The average debt balance was $23.5 billion in 2016 versus $19.3 billion in 2015. The total debt balance at the end of 2016 was $27.1 billion as compared to $19.9 b… |
| 5 | `JNJ_FY2016_2017-01-01:465` | Item 8 › 22. Restructuring |  |  | \| (Dollars in Millions) \| Severance \| Asset Write-offs \| Other** \| Total \| \|---\|---\|---\|---\|---\| \| 2015 restructuring charge \| $484 \| 86 \| 20 \| 590 \| \| 2015 activity \| \| (86) \| (3) \| (89) \| \| Reserve balance, January 3, … |
| 6 | `JNJ_FY2016_2017-01-01:317` | Item 8 › Reclassification |  |  | \| (Dollars in Millions) \| 2016 \| 2015 \| 2014 \| \|---\|---\|---\|---\| \| Beginning of year \| $3,080 \| 2,465 \| 2,729 \| \| Increases related to current year tax positions \| 348 \| 570 \| 281 \| \| Increases related to prior period ta… |
| 7 | `JNJ_FY2016_2017-01-01:148` | Item 7 › Income Before Tax by Segment |  | #4 | \| \| Income Before Tax \| \| Segment Sales \| \| Percent of Segment Sales \| \| \|---\|---\|---\|---\|---\|---\|---\| \| (Dollars in Millions) \| 2016 \| 2015 \| 2016 \| 2015 \| 2016 \| 2015 \| \| Consumer \| $2,441 \| 1,787 \| $13,307 \| 13,507 \| … |
| 8 | `JNJ_FY2016_2017-01-01:152` | Item 7 › Income Before Tax by Segment |  | #3, #4 | Medical Devices Segment: In 2016, the Medical Devices segment income before tax as a percent to sales was 22.2% versus 27.2% in 2015. The decrease in the income before tax as a percent to sales was primarily due to lower… |
| 9 | `JNJ_FY2016_2017-01-01:150` | Item 7 › Income Before Tax by Segment | ✓ | #3, #4 | Pharmaceutical Segment: In 2016, the Pharmaceutical segment income before tax as a percent to sales was 38.3% versus 37.3% in 2015. The increase in income before tax was primarily due to strong sales volume growth and fa… |
| 10 | `JNJ_FY2016_2017-01-01:182` | Item 7 › Pharmaceutical Segment |  |  | \| (Dollars in Millions) \| Balance at Beginning of Period \| Accruals \| Payments/Credits(2) \| Balance at End of Period \| \|---\|---\|---\|---\|---\| \| 2016 \| \| \| \| \| \| Accrued rebates (1) \| $3,451 \| 12,306 \| (12,337) \| 3,420 \| \|… |
| 11 | `JNJ_FY2016_2017-01-01:379` | Item 8 › Restricted Share Units and Performance Share Units |  |  | \| \| Income Before Tax \| \| \| Identifiable Assets \| \| \|---\|---\|---\|---\|---\|---\| \| (Dollars in Millions) \| 2016 (3) \| 2015 (4) \| 2014 (5) \| 2016 \| 2015 \| \| Consumer \| $2,441 \| 1,787 \| 1,941 \| $23,971 \| 20,772 \| \| Pharmaceut… |
| 12 | `JNJ_FY2016_2017-01-01:138` | Item 7 › Analysis of Consolidated Earnings Before Provision for Taxes on Income |  | #3, #4 | In 2016, cost of products sold as a percent to sales decreased to 30.2% from 30.7% as compared to the same period a year ago. Favorable mix in the business and cost improvement programs was partially offset by the unfavo… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#3 `JNJ_FY2016_2017-01-01:284`** (cited, gold #1, gold #2)

````text
Item 8. FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA > Reclassification (table)
| (Dollars in Millions) | Consumer | Pharmaceutical | Med Devices | Total |
|---|---|---|---|---|
| Goodwill at December 28, 2014 | $7,675 | 2,626 | 11,531 | 21,832 |
| Goodwill, related to acquisitions | 110 | 366 | 34 | 510 |
| Goodwill, related to divestitures | (119) | (17) | (57) | (193) |
| Currency translation/other | (426) | (86) | (8) | (520) |
| Goodwill at January 3, 2016 | $7,240 | 2,889 | 11,500 | 21,629 |
| Goodwill, related to acquisitions | 1,362 | — | 210 | 1,572 |
| Goodwill, related to divestitures | (63) | (12) | — | (75) |
| Currency translation/other | (276) | (37) | (8) | (321) |
| Goodwill at January 1, 2017 | $8,263 | 2,840 | 11,702 | 22,805 |
````

**#7 `JNJ_FY2016_2017-01-01:148`** (gold #4)

````text
Item 7. MANAGEMENT’S DISCUSSION AND ANALYSIS OF RESULTS OF OPERATIONS AND FINANCIAL CONDITION > Income Before Tax by Segment (table)
|  | Income Before Tax |  | Segment Sales |  | Percent of Segment Sales |  |
|---|---|---|---|---|---|---|
| (Dollars in Millions) | 2016 | 2015 | 2016 | 2015 | 2016 | 2015 |
| Consumer | $2,441 | 1,787 | $13,307 | 13,507 | 18.3% | 13.2 |
| Pharmaceutical | 12,827 | 11,734 | 33,464 | 31,430 | 38.3 | 37.3 |
| Medical Devices | 5,578 | 6,826 | 25,119 | 25,137 | 22.2 | 27.2 |
| Total (1) | 20,846 | 20,347 | 71,890 | 70,074 | 29.0 | 29.0 |
| Less: Expenses not allocated to segments (2) | 1,043 | 1,151 |  |  |  |  |
| Earnings before provision for taxes on income | $19,803 | 19,196 | $71,890 | 70,074 | 27.5% | 27.4 |
````

**#8 `JNJ_FY2016_2017-01-01:152`** (gold #3, gold #4)

````text
Item 7. MANAGEMENT’S DISCUSSION AND ANALYSIS OF RESULTS OF OPERATIONS AND FINANCIAL CONDITION > Income Before Tax by Segment
Medical Devices Segment: In 2016, the Medical Devices segment income before tax as a percent to sales was 22.2% versus 27.2% in 2015. The decrease in the income before tax as a percent to sales was primarily due to lower gains of $1.4 billion related to divestitures, higher litigation expense of $0.8 billion and a higher restructuring charge of $0.1 billion as compared to 2015. This was partially offset by an intangible asset write-down of $0.3 billion related to Acclarent in 2015 and favorable selling, marketing and administrative expenses in 2016. In 2015, the Medical Devices segment income before tax as a percent to sales was 27.2% versus 28.9% in 2014 primarily due to a restructuring charge of $0.6 billion, an intangible asset write-down of $0.3 billion related to Acclarent, and lower gains of $0.5 billion on divestitures as compared to 2014. In 2015, the Medical Devices segment included gains of $1.4 billion, primarily for the divestiture of the Cordis business versus a gain of $1.9 billion recorded in 2014 for the divestiture of the Ortho-Clinical Diagnostics business. The 2015 income before tax was favorably impacted by lower net litigation expense of
````

**#9 `JNJ_FY2016_2017-01-01:150`** (cited, gold #3, gold #4)

````text
Item 7. MANAGEMENT’S DISCUSSION AND ANALYSIS OF RESULTS OF OPERATIONS AND FINANCIAL CONDITION > Income Before Tax by Segment
Pharmaceutical Segment: In 2016, the Pharmaceutical segment income before tax as a percent to sales was 38.3% versus 37.3% in 2015. The increase in income before tax was primarily due to strong sales volume growth and favorable selling, marketing and administrative expenses due to cost management. Additionally, the fiscal year 2015, had higher gains of $0.7 billion related to divestitures partially offset by a higher IPR&D charge of $0.2 billion as compared to 2016. The fiscal year of 2016 included the gains from the divestitures of the controlled substance raw material and API business and certain anesthetic products in Europe versus the gains recorded in 2015 from the U.S. divestiture of NUCYNTA®.
````

**#12 `JNJ_FY2016_2017-01-01:138`** (gold #3, gold #4)

````text
Item 7. MANAGEMENT’S DISCUSSION AND ANALYSIS OF RESULTS OF OPERATIONS AND FINANCIAL CONDITION > Analysis of Consolidated Earnings Before Provision for Taxes on Income
In 2016, cost of products sold as a percent to sales decreased to 30.2% from 30.7% as compared to the same period a year ago. Favorable mix in the business and cost improvement programs was partially offset by the unfavorable impact of transactional currency. Intangible asset amortization expense of $1.2 billion was included in cost of products sold for 2016 and 2015. There was a decrease in the percent to sales of selling, marketing and administrative expenses in 2016 compared to the prior year, primarily due to cost management in all the segments and favorable mix.
````

</details>

RQ2 citation match (section level): `cited=[('JNJ', 'Item 8'), ('JNJ', 'Item 7')] gold=[(None, 'Item 8'), (None, 'Item 7')]`

**System C guardrail** (judge `gpt-5.4`): numerical claims 7, verified 7, ungrounded 0, uncited 0, derived 1; sentence verdicts: supported 0, partial 0, unsupported 0, unchecked 0.


<details><summary>Guardrail sentence verdicts</summary>

| sentence | verdict | judge reason |
|---|---|---|
| Total goodwill increased by $1,176 million in fiscal 2016, rising from $21,629 million at January 3, 2016 to $22,805 million at January 1, 2017 [JNJ FY2016, Item 8, JNJ_FY2016_2017-01-01:284]. | None |  |
| The Pharmaceutical segment’s income before tax as a percent of sales increased to 38.3% in 2016 from 37.3% in 2015, primarily due to strong sales volume growth and favorable selling, marketing and administrative expenses due to cost management [JNJ FY2016, Item 7, JNJ_FY2016_2017-01-01:150]. | None |  |
| The filing also states that fiscal 2015 had higher gains of $0.7 billion related to divestitures, partially offset by a higher IPR&D charge of $0.2 billion as compared to 2016 [JNJ FY2016, Item 7, JNJ_FY2016_2017-01-01:150]. | None |  |

</details>

### System C v2 (agentic multi-hop + XBRL)

Model: `gpt-5.4`. Hops: 2. Chunks retrieved: 13, cited: 3.

**Generated answer**

> Johnson & Johnson’s total goodwill increased by $1,176 million in fiscal 2016, rising from $21,629 million at January 3, 2016 to $22,805 million at January 1, 2017 [JNJ FY2016, Item 8, JNJ_FY2016_2017-01-01:284].  
>
> The Pharmaceutical segment’s income before tax as a percent of sales increased to 38.3% in 2016 from 37.3% in 2015 [JNJ FY2016, Item 7, JNJ_FY2016_2017-01-01:148] [JNJ FY2016, Item 7, JNJ_FY2016_2017-01-01:150].  
>
> The filing states that the increase was primarily due to strong sales volume growth and favorable selling, marketing and administrative expenses due to cost management [JNJ FY2016, Item 7, JNJ_FY2016_2017-01-01:150].  
>
> The filing also notes that fiscal 2015 had higher gains of $0.7 billion related to divestitures, partially offset by a higher IPR&D charge of $0.2 billion as compared to 2016 [JNJ FY2016, Item 7, JNJ_FY2016_2017-01-01:150].

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `F-JNJ-2016` | SEC XBRL Reported Financials (financials.csv) |  |  | fiscal_year,fiscal_year_end,Revenue,NetIncome,OperatingIncome,TotalAssets,TotalLiabilities,StockholdersEquity,CashAndEquivalents,OperatingCashFlow,EPSDiluted 2016,2017-01-01,,16540000000,,141208000000,70790000000,,189720… |
| 2 | `JNJ_FY2016_2017-01-01:465` | Item 8 › 22. Restructuring |  |  | \| (Dollars in Millions) \| Severance \| Asset Write-offs \| Other** \| Total \| \|---\|---\|---\|---\|---\| \| 2015 restructuring charge \| $484 \| 86 \| 20 \| 590 \| \| 2015 activity \| \| (86) \| (3) \| (89) \| \| Reserve balance, January 3, … |
| 3 | `JNJ_FY2016_2017-01-01:284` | Item 8 › Reclassification | ✓ | #1, #2 | \| (Dollars in Millions) \| Consumer \| Pharmaceutical \| Med Devices \| Total \| \|---\|---\|---\|---\|---\| \| Goodwill at December 28, 2014 \| $7,675 \| 2,626 \| 11,531 \| 21,832 \| \| Goodwill, related to acquisitions \| 110 \| 366 \| 34 … |
| 4 | `JNJ_FY2016_2017-01-01:145` | Item 7 › Analysis of Consolidated Earnings Before Provision for Taxes on Income |  |  | Interest expense in 2016 was higher as compared to 2015. The average debt balance was $23.5 billion in 2016 versus $19.3 billion in 2015. The total debt balance at the end of 2016 was $27.1 billion as compared to $19.9 b… |
| 5 | `JNJ_FY2016_2017-01-01:179` | Item 7 › Consumer Segment |  |  | \| (Dollars in Millions) \| Balance at Beginning of Period \| Accruals \| Payments/Credits \| Balance at End of Period \| \|---\|---\|---\|---\|---\| \| 2016 \| \| \| \| \| \| Accrued rebates (1) \| $139 \| 615 \| (618) \| 136 \| \| Accrued retu… |
| 6 | `JNJ_FY2016_2017-01-01:180` | Item 7 › Consumer Segment |  |  | \| (Dollars in Millions) \| Balance at Beginning of Period \| Accruals \| Payments/Credits \| Balance at End of Period \| \|---\|---\|---\|---\|---\| \| Total \| $480 \| 2,722 \| (2,562) \| 640 \| |
| 7 | `JNJ_FY2016_2017-01-01:317` | Item 8 › Reclassification |  |  | \| (Dollars in Millions) \| 2016 \| 2015 \| 2014 \| \|---\|---\|---\|---\| \| Beginning of year \| $3,080 \| 2,465 \| 2,729 \| \| Increases related to current year tax positions \| 348 \| 570 \| 281 \| \| Increases related to prior period ta… |
| 8 | `JNJ_FY2016_2017-01-01:148` | Item 7 › Income Before Tax by Segment | ✓ | #4 | \| \| Income Before Tax \| \| Segment Sales \| \| Percent of Segment Sales \| \| \|---\|---\|---\|---\|---\|---\|---\| \| (Dollars in Millions) \| 2016 \| 2015 \| 2016 \| 2015 \| 2016 \| 2015 \| \| Consumer \| $2,441 \| 1,787 \| $13,307 \| 13,507 \| … |
| 9 | `JNJ_FY2016_2017-01-01:208` | Item 8 › (Dollars in Millions Except Share and Per Share Amounts) (Note 1) |  |  | \| \| 2016 \| 2015 \| \|---\|---\|---\| \| Assets \| \| \| \| Current assets \| \| \| \| Cash and cash equivalents (Notes 1 and 2) \| $18,972 \| 13,732 \| \| Marketable securities (Notes 1 and 2) \| 22,935 \| 24,644 \| \| Accounts receivable tra… |
| 10 | `JNJ_FY2016_2017-01-01:150` | Item 7 › Income Before Tax by Segment | ✓ | #3, #4 | Pharmaceutical Segment: In 2016, the Pharmaceutical segment income before tax as a percent to sales was 38.3% versus 37.3% in 2015. The increase in income before tax was primarily due to strong sales volume growth and fa… |
| 11 | `JNJ_FY2016_2017-01-01:152` | Item 7 › Income Before Tax by Segment |  | #3, #4 | Medical Devices Segment: In 2016, the Medical Devices segment income before tax as a percent to sales was 22.2% versus 27.2% in 2015. The decrease in the income before tax as a percent to sales was primarily due to lower… |
| 12 | `JNJ_FY2016_2017-01-01:182` | Item 7 › Pharmaceutical Segment |  |  | \| (Dollars in Millions) \| Balance at Beginning of Period \| Accruals \| Payments/Credits(2) \| Balance at End of Period \| \|---\|---\|---\|---\|---\| \| 2016 \| \| \| \| \| \| Accrued rebates (1) \| $3,451 \| 12,306 \| (12,337) \| 3,420 \| \|… |
| 13 | `JNJ_FY2016_2017-01-01:379` | Item 8 › Restricted Share Units and Performance Share Units |  |  | \| \| Income Before Tax \| \| \| Identifiable Assets \| \| \|---\|---\|---\|---\|---\|---\| \| (Dollars in Millions) \| 2016 (3) \| 2015 (4) \| 2014 (5) \| 2016 \| 2015 \| \| Consumer \| $2,441 \| 1,787 \| 1,941 \| $23,971 \| 20,772 \| \| Pharmaceut… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#3 `JNJ_FY2016_2017-01-01:284`** (cited, gold #1, gold #2)

````text
Item 8. FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA > Reclassification (table)
| (Dollars in Millions) | Consumer | Pharmaceutical | Med Devices | Total |
|---|---|---|---|---|
| Goodwill at December 28, 2014 | $7,675 | 2,626 | 11,531 | 21,832 |
| Goodwill, related to acquisitions | 110 | 366 | 34 | 510 |
| Goodwill, related to divestitures | (119) | (17) | (57) | (193) |
| Currency translation/other | (426) | (86) | (8) | (520) |
| Goodwill at January 3, 2016 | $7,240 | 2,889 | 11,500 | 21,629 |
| Goodwill, related to acquisitions | 1,362 | — | 210 | 1,572 |
| Goodwill, related to divestitures | (63) | (12) | — | (75) |
| Currency translation/other | (276) | (37) | (8) | (321) |
| Goodwill at January 1, 2017 | $8,263 | 2,840 | 11,702 | 22,805 |
````

**#8 `JNJ_FY2016_2017-01-01:148`** (cited, gold #4)

````text
Item 7. MANAGEMENT’S DISCUSSION AND ANALYSIS OF RESULTS OF OPERATIONS AND FINANCIAL CONDITION > Income Before Tax by Segment (table)
|  | Income Before Tax |  | Segment Sales |  | Percent of Segment Sales |  |
|---|---|---|---|---|---|---|
| (Dollars in Millions) | 2016 | 2015 | 2016 | 2015 | 2016 | 2015 |
| Consumer | $2,441 | 1,787 | $13,307 | 13,507 | 18.3% | 13.2 |
| Pharmaceutical | 12,827 | 11,734 | 33,464 | 31,430 | 38.3 | 37.3 |
| Medical Devices | 5,578 | 6,826 | 25,119 | 25,137 | 22.2 | 27.2 |
| Total (1) | 20,846 | 20,347 | 71,890 | 70,074 | 29.0 | 29.0 |
| Less: Expenses not allocated to segments (2) | 1,043 | 1,151 |  |  |  |  |
| Earnings before provision for taxes on income | $19,803 | 19,196 | $71,890 | 70,074 | 27.5% | 27.4 |
````

**#10 `JNJ_FY2016_2017-01-01:150`** (cited, gold #3, gold #4)

````text
Item 7. MANAGEMENT’S DISCUSSION AND ANALYSIS OF RESULTS OF OPERATIONS AND FINANCIAL CONDITION > Income Before Tax by Segment
Pharmaceutical Segment: In 2016, the Pharmaceutical segment income before tax as a percent to sales was 38.3% versus 37.3% in 2015. The increase in income before tax was primarily due to strong sales volume growth and favorable selling, marketing and administrative expenses due to cost management. Additionally, the fiscal year 2015, had higher gains of $0.7 billion related to divestitures partially offset by a higher IPR&D charge of $0.2 billion as compared to 2016. The fiscal year of 2016 included the gains from the divestitures of the controlled substance raw material and API business and certain anesthetic products in Europe versus the gains recorded in 2015 from the U.S. divestiture of NUCYNTA®.
````

**#11 `JNJ_FY2016_2017-01-01:152`** (gold #3, gold #4)

````text
Item 7. MANAGEMENT’S DISCUSSION AND ANALYSIS OF RESULTS OF OPERATIONS AND FINANCIAL CONDITION > Income Before Tax by Segment
Medical Devices Segment: In 2016, the Medical Devices segment income before tax as a percent to sales was 22.2% versus 27.2% in 2015. The decrease in the income before tax as a percent to sales was primarily due to lower gains of $1.4 billion related to divestitures, higher litigation expense of $0.8 billion and a higher restructuring charge of $0.1 billion as compared to 2015. This was partially offset by an intangible asset write-down of $0.3 billion related to Acclarent in 2015 and favorable selling, marketing and administrative expenses in 2016. In 2015, the Medical Devices segment income before tax as a percent to sales was 27.2% versus 28.9% in 2014 primarily due to a restructuring charge of $0.6 billion, an intangible asset write-down of $0.3 billion related to Acclarent, and lower gains of $0.5 billion on divestitures as compared to 2014. In 2015, the Medical Devices segment included gains of $1.4 billion, primarily for the divestiture of the Cordis business versus a gain of $1.9 billion recorded in 2014 for the divestiture of the Ortho-Clinical Diagnostics business. The 2015 income before tax was favorably impacted by lower net litigation expense of
````

</details>

RQ2 citation match (section level): `cited=[('JNJ', 'Item 8'), ('JNJ', 'Item 7')] gold=[(None, 'Item 8'), (None, 'Item 7')]`

**System C guardrail** (judge `gpt-5.4`): numerical claims 7, verified 7, ungrounded 0, uncited 0, derived 1; sentence verdicts: supported 1, partial 0, unsupported 0, unchecked 0.


<details><summary>Guardrail sentence verdicts</summary>

| sentence | verdict | judge reason |
|---|---|---|
| Johnson & Johnson’s total goodwill increased by $1,176 million in fiscal 2016, rising from $21,629 million at January 3, 2016 to $22,805 million at January 1, 2017 [JNJ FY2016, Item 8, JNJ_FY2016_2017-01-01:284]. | None |  |
| The Pharmaceutical segment’s income before tax as a percent of sales increased to 38.3% in 2016 from 37.3% in 2015 [JNJ FY2016, Item 7, JNJ_FY2016_2017-01-01:148] [JNJ FY2016, Item 7, JNJ_FY2016_2017-01-01:150]. | None |  |
| The filing states that the increase was primarily due to strong sales volume growth and favorable selling, marketing and administrative expenses due to cost management [JNJ FY2016, Item 7, JNJ_FY2016_2017-01-01:150]. | supported | The cited passage states the increase was primarily due to strong sales volume growth and favorable selling, marketing and administrative expenses from cost management. |
| The filing also notes that fiscal 2015 had higher gains of $0.7 billion related to divestitures, partially offset by a higher IPR&D charge of $0.2 billion as compared to 2016 [JNJ FY2016, Item 7, JNJ_FY2016_2017-01-01:150]. | None |  |

</details>
