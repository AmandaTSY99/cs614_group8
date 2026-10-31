# gold-014: Cross-year table

[← all cases](../README.md) · company: JOHNSON & JOHNSON (JNJ) · fiscal year: 2021 · recipe `cross_year_table` · hop `multi` · answer type `numeric` · scope `cross_year` · RQ2 category `multi_company_comparison`

## Gold QA

**Question**

> By how many percentage points did Johnson & Johnson's total research and development expense as a share of total sales increase from fiscal year 2018 to fiscal year 2021?

**Gold answer**

> 2.5 percentage points

**Program**: `subtract(15.7, 13.2)` → `2.5`

**Gold numbers** (RQ2 numeric_accuracy targets): 2.5 percentage points

**Gold evidence**

1. `JNJ_FY2021_2022-01-02` · Item 7.MANAGEMENT’S DISCUSSION AND ANALYSIS OF RESULTS OF OPERATIONS AND FINANCIAL CONDITION › Research and Development Expense: · table

   > Total research and development expense | $14,714 | 15.7% | $12,159 | 14.7%

2. `JNJ_FY2018_2018-12-30` · Item 7. MANAGEMENT’S DISCUSSION AND ANALYSIS OF RESULTS OF OPERATIONS AND FINANCIAL CONDITION › Analysis of Consolidated Earnings Before Provision for Taxes on Income · table

   > Total research and development expense | $10,775 | 13.2% | 10,594 | 13.9 | 9,143 | 12.7

## Scorecard

| Metric | A (vanilla dense) | B (hybrid + rerank) | C v1 (adaptive multi-hop) | C v2 (agentic multi-hop + XBRL) |
|---|---|---|---|---|
| **Retrieval (RQ1)** | | | | |
| chunks retrieved | 10 | 5 | 10 | 8 |
| recall@5 | 0.50 | 1.00 | 0.50 | 0.50 |
| recall@all | 0.50 | 1.00 | 1.00 | 0.50 |
| complete@all | 0 | 1 | 1 | 0 |
| average precision (lexical) | 0.62 | 1.00 | 0.53 | 0.33 |
| gold evidence first rank | #1: 1, #2: – | #1: 1, #2: 2 | #1: 1, #2: 9 | #1: 3, #2: – |
| **Answer (RQ3 string match)** | | | | |
| numeric_correct | ✗ | ✓ | ✓ | ✗ |
| keypoint_recall | – | – | – | – |
| **Answer & citations (RQ2)** | | | | |
| numeric_accuracy | 0.00 | 1.00 | 1.00 | 0.00 |
| citation precision | 1.00 | 1.00 | 1.00 | 1.00 |
| citation recall | 1.00 | 1.00 | 1.00 | 1.00 |
| citation F1 | 1.00 | 1.00 | 1.00 | 1.00 |
| has a citation | 1 | 1 | 1 | 1 |
| grounding error rate | – | – | 0.00 | 0.00 |
| **Cost (RQ3)** | | | | |
| retrieval hops | 1 | 1 | 2 | 1 |
| tokens | 2012 | 1213 | 9084 | 6718 |
| cost (USD) | 0.0004 | 0.0002 | 0.0326 | 0.0254 |
| latency (s) | 2.8 | 5.8 | 14.3 | 10.0 |

Definitions: [README › Metrics](../README.md#metrics). `–` = not applicable (e.g. no gold number, no citations, no guardrail).

## System outputs

### System A (vanilla dense)

Model: `gpt-5.4-2026-03-05`. Hops: 1. Chunks retrieved: 10, cited: 1.

**Generated answer**

> The provided context gives Johnson & Johnson’s total research and development expense as **15.7% of sales in 2021** [1].
>
> However, the context does **not provide the 2018 total research and development expense as a percent of total sales**, so the increase from **2018 to 2021** cannot be calculated from the provided context.
>
> What is available:
> - **2021 total R&D expense as % of sales:** **15.7%** [1]
>
> What is missing:
> - **2018 total R&D expense as % of sales** (not in the provided context)

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `JNJ_FY2021_2022-01-02:159` | Item 7 › Research and Development Expense: | ✓ | #1 | \| \| 2021 \| \| 2020 \| \| \|---\|---\|---\|---\|---\| \| (Dollars in Millions) \| Amount \| % of Sales* \| Amount \| % of Sales* \| \| Consumer Health \| $455 \| 3.1% \| $422 \| 3.0% \| \| Pharmaceutical \| 11,882 \| 22.8 \| 9,563 \| 21.0 \| \| Medi… |
| 2 | `JNJ_FY2018_2018-12-30:137` | Item 7 › Analysis of Consolidated Earnings Before Provision for Taxes on Income |  |  | In 2017, cost of products sold as a percent to sales increased to 33.3% from 30.3% as compared to the same period a year ago. The unfavorable increase was primarily driven by $2.3 billion of higher amortization expense a… |
| 3 | `JNJ_FY2021_2022-01-02:163` | Item 7 › Research and Development Expense: |  |  | Other (income) expense, net for the fiscal year 2021 was favorable by $2.4 billion as compared to the prior year primarily due to the following: |
| 4 | `JNJ_FY2021_2022-01-02:158` | Item 7 › Research and Development Expense: |  |  | Research and development expense by segment of business was as follows: |
| 5 | `JNJ_FY2018_2018-12-30:109` | Item 7 › Analysis of Consolidated Sales |  |  | In 2018, worldwide sales increased 6.7% to $81.6 billion, compared to an increases of 6.3% and 2.6% in 2017 and 2016, respectively. These sales changes consisted of the following: |
| 6 | `JNJ_FY2021_2022-01-02:136` | Item 7 › Analysis of Consolidated Sales |  |  | \| Sales increase/(decrease) due to: \| 2021 \| 2020 \| \|---\|---\|---\| \| Volume \| 12.9% \| 3.5% \| \| Price \| (0.7) \| (2.3) \| \| Currency \| 1.4 \| (0.6) \| \| Total \| 13.6% \| 0.6% \| |
| 7 | `JNJ_FY2021_2022-01-02:135` | Item 7 › Analysis of Consolidated Sales |  |  | For discussion on results of operations and financial condition pertaining to the fiscal years 2020 and 2019 see the Company’s Annual Report on Form 10-K for the fiscal year ended January 3, 2021, Item 7. Management's Di… |
| 8 | `JNJ_FY2021_2022-01-02:232` | Item 8 › (Dollars and Shares in Millions Except Per Share Amounts) (Note 1) |  | #1 | \| \| 2021 \| 2020 \| 2019 \| \|---\|---\|---\|---\| \| Sales to customers \| $93,775 \| 82,584 \| 82,059 \| \| Cost of products sold \| 29,855 \| 28,427 \| 27,556 \| \| Gross profit \| 63,920 \| 54,157 \| 54,503 \| \| Selling, marketing and admi… |
| 9 | `JNJ_FY2018_2018-12-30:135` | Item 7 › Analysis of Consolidated Earnings Before Provision for Taxes on Income |  |  | \| % of Sales \| 2018 \| 2017 \| 2016 \| \|---\|---\|---\|---\| \| Cost of products sold* \| 33.2% \| 33.3 \| 30.3 \| \| Percent point increase/(decrease) over the prior year \| (0.1) \| 3.0 \| (0.3) \| \| Selling, marketing and administrati… |
| 10 | `JNJ_FY2021_2022-01-02:164` | Item 7 › Research and Development Expense: |  |  | \| (Dollars in Billions)(Income)/Expense \| 2021 \| 2020 \| Change \| \|---\|---\|---\|---\| \| Litigation expense(1) \| $2.3 \| 5.1 \| (2.8) \| \| Acquisition, Integration and Divestiture related(2) \| (0.5) \| (1.1) \| 0.6 \| \| (Gains)/lo… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#1 `JNJ_FY2021_2022-01-02:159`** (cited, gold #1)

````text
Item 7.MANAGEMENT’S DISCUSSION AND ANALYSIS OF RESULTS OF OPERATIONS AND FINANCIAL CONDITION > Research and Development Expense: (table)
|  | 2021 |  | 2020 |  |
|---|---|---|---|---|
| (Dollars in Millions) | Amount | % of Sales* | Amount | % of Sales* |
| Consumer Health | $455 | 3.1% | $422 | 3.0% |
| Pharmaceutical | 11,882 | 22.8 | 9,563 | 21.0 |
| Medical Devices | 2,377 | 8.8 | 2,174 | 9.5 |
| Total research and development expense | $14,714 | 15.7% | $12,159 | 14.7% |
| Percent increase/(decrease) over the prior year | 21.0% |  | 7.1% |  |
| *As a percent to segment sales |  |  |  |  |
````

**#8 `JNJ_FY2021_2022-01-02:232`** (gold #1)

````text
Item 8. FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA > (Dollars and Shares in Millions Except Per Share Amounts) (Note 1) (table)
|  | 2021 | 2020 | 2019 |
|---|---|---|---|
| Sales to customers | $93,775 | 82,584 | 82,059 |
| Cost of products sold | 29,855 | 28,427 | 27,556 |
| Gross profit | 63,920 | 54,157 | 54,503 |
| Selling, marketing and administrative expenses | 24,659 | 22,084 | 22,178 |
| Research and development expense | 14,714 | 12,159 | 11,355 |
| In-process research and development (Note 5) | 900 | 181 | 890 |
| Interest income | (53) | (111) | (357) |
| Interest expense, net of portion capitalized (Note 4) | 183 | 201 | 318 |
| Other (income) expense, net | 489 | 2,899 | 2,525 |
| Restructuring (Note 20) | 252 | 247 | 266 |
| Earnings before provision for taxes on income | 22,776 | 16,497 | 17,328 |
| Provision for taxes on income (Note 8) | 1,898 | 1,783 | 2,209 |
| Net earnings | $20,878 | 14,714 | 15,119 |
| Net earnings per share (Notes 1 and 15) |  |  |  |
| Basic | $7.93 | 5.59 | 5.72 |
````

</details>

RQ2 citation match (section level): `cited=[('JNJ', 'Item 7')] gold=[(None, 'Item 7')]`

### System B (hybrid + rerank)

Model: `gpt-5.4-2026-03-05`. Hops: 1. Chunks retrieved: 5, cited: 2.

**Generated answer**

> Johnson & Johnson’s total research and development expense as a share of total sales increased from 13.2% in 2018 to 15.7% in 2021, an increase of 2.5 percentage points [1][2].

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `JNJ_FY2021_2022-01-02:159` | Item 7 › Research and Development Expense: | ✓ | #1 | \| \| 2021 \| \| 2020 \| \| \|---\|---\|---\|---\|---\| \| (Dollars in Millions) \| Amount \| % of Sales* \| Amount \| % of Sales* \| \| Consumer Health \| $455 \| 3.1% \| $422 \| 3.0% \| \| Pharmaceutical \| 11,882 \| 22.8 \| 9,563 \| 21.0 \| \| Medi… |
| 2 | `JNJ_FY2018_2018-12-30:138` | Item 7 › Analysis of Consolidated Earnings Before Provision for Taxes on Income | ✓ | #2 | \| \| 2018 \| \| 2017 \| \| 2016 \| \| \|---\|---\|---\|---\|---\|---\|---\| \| (Dollars in Millions) \| Amount \| % of Sales** \| Amount \| % of Sales** \| Amount \| % of Sales** \| \| Consumer \| $565 \| 4.1% \| 586 \| 4.3 \| 585 \| 4.4 \| \| Pharmace… |
| 3 | `JNJ_FY2021_2022-01-02:135` | Item 7 › Analysis of Consolidated Sales |  |  | For discussion on results of operations and financial condition pertaining to the fiscal years 2020 and 2019 see the Company’s Annual Report on Form 10-K for the fiscal year ended January 3, 2021, Item 7. Management's Di… |
| 4 | `JNJ_FY2021_2022-01-02:171` | Item 7 › Pharmaceutical Segment: |  |  | In 2021, the Pharmaceutical segment income before tax as a percent to sales was 34.9% versus 33.9% in 2020. The increase in the income before tax as a percent of sales was primarily driven by the following: •Divestiture … |
| 5 | `JNJ_FY2021_2022-01-02:163` | Item 7 › Research and Development Expense: |  |  | Other (income) expense, net for the fiscal year 2021 was favorable by $2.4 billion as compared to the prior year primarily due to the following: |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#1 `JNJ_FY2021_2022-01-02:159`** (cited, gold #1)

````text
Item 7.MANAGEMENT’S DISCUSSION AND ANALYSIS OF RESULTS OF OPERATIONS AND FINANCIAL CONDITION > Research and Development Expense: (table)
|  | 2021 |  | 2020 |  |
|---|---|---|---|---|
| (Dollars in Millions) | Amount | % of Sales* | Amount | % of Sales* |
| Consumer Health | $455 | 3.1% | $422 | 3.0% |
| Pharmaceutical | 11,882 | 22.8 | 9,563 | 21.0 |
| Medical Devices | 2,377 | 8.8 | 2,174 | 9.5 |
| Total research and development expense | $14,714 | 15.7% | $12,159 | 14.7% |
| Percent increase/(decrease) over the prior year | 21.0% |  | 7.1% |  |
| *As a percent to segment sales |  |  |  |  |
````

**#2 `JNJ_FY2018_2018-12-30:138`** (cited, gold #2)

````text
Item 7. MANAGEMENT’S DISCUSSION AND ANALYSIS OF RESULTS OF OPERATIONS AND FINANCIAL CONDITION > Analysis of Consolidated Earnings Before Provision for Taxes on Income (table)
|  | 2018 |  | 2017 |  | 2016 |  |
|---|---|---|---|---|---|---|
| (Dollars in Millions) | Amount | % of Sales** | Amount | % of Sales** | Amount | % of Sales** |
| Consumer | $565 | 4.1% | 586 | 4.3 | 585 | 4.4 |
| Pharmaceutical | 8,446 | 20.7 | 8,392 | 23.1 | 7,001 | 20.9 |
| Medical Devices | 1,764 | 6.5 | 1,616 | 6.1 | 1,557 | 6.2 |
| Total research and development expense | $10,775 | 13.2% | 10,594 | 13.9 | 9,143 | 12.7 |
| Percent increase/(decrease) over the prior year | 1.7% |  | 15.9 |  | 1.6 |  |
````

</details>

RQ2 citation match (section level): `cited=[('JNJ', 'Item 7')] gold=[(None, 'Item 7')]`

### System C v1 (adaptive multi-hop)

Model: `gpt-5.4`. Hops: 2. Chunks retrieved: 10, cited: 2.

**Generated answer**

> Johnson & Johnson's total research and development expense was 13.2% of sales in fiscal 2018 and 15.7% of sales in fiscal 2021, so it increased by 2.5 percentage points from 2018 to 2021 [JNJ FY2018, Item 7, JNJ_FY2018_2018-12-30:138] [JNJ FY2021, Item 7, JNJ_FY2021_2022-01-02:159].

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `JNJ_FY2021_2022-01-02:159` | Item 7 › Research and Development Expense: | ✓ | #1 | \| \| 2021 \| \| 2020 \| \| \|---\|---\|---\|---\|---\| \| (Dollars in Millions) \| Amount \| % of Sales* \| Amount \| % of Sales* \| \| Consumer Health \| $455 \| 3.1% \| $422 \| 3.0% \| \| Pharmaceutical \| 11,882 \| 22.8 \| 9,563 \| 21.0 \| \| Medi… |
| 2 | `JNJ_FY2018_2018-12-30:234` | Item 8 › Recently Adopted Accounting Standards |  |  | \| (Dollars In millions) \| \| Increase (Decrease) to Net Expense \| \| \|---\|---\|---\|---\| \| \| 2018 \| 2017 \| 2016 \| \| Cost of products sold \| $51 \| 85 \| 104 \| \| Selling, marketing and administrative expenses \| 55 \| 100 \| 122 \|… |
| 3 | `JNJ_FY2021_2022-01-02:160` | Item 7 › Research and Development Expense: |  |  | Research and development activities represent a significant part of the Company's business. These expenditures relate to the processes of discovering, testing and developing new products, upfront payments and development… |
| 4 | `JNJ_FY2021_2022-01-02:158` | Item 7 › Research and Development Expense: |  |  | Research and development expense by segment of business was as follows: |
| 5 | `JNJ_FY2021_2022-01-02:164` | Item 7 › Research and Development Expense: |  |  | \| (Dollars in Billions)(Income)/Expense \| 2021 \| 2020 \| Change \| \|---\|---\|---\|---\| \| Litigation expense(1) \| $2.3 \| 5.1 \| (2.8) \| \| Acquisition, Integration and Divestiture related(2) \| (0.5) \| (1.1) \| 0.6 \| \| (Gains)/lo… |
| 6 | `JNJ_FY2018_2018-12-30:258` | Item 8 › Research and Development |  |  | \| Nature/Type of Collaboration \| Statement of Earnings Presentation \| \|---\|---\| \| Third-party sale of product & profit share payments received \| Sales to customers \| \| Royalties/milestones paid to collaborative partner (… |
| 7 | `JNJ_FY2018_2018-12-30:209` | Item 8 › (Dollars and Shares in Millions Except Per Share Amounts) (Note 1) |  |  | \| \| 2018 \| 2017 \| 2016 \| \|---\|---\|---\|---\| \| Sales to customers \| $81,581 \| 76,450 \| 71,890 \| \| Cost of products sold \| 27,091 \| 25,439 \| 21,789 \| \| Gross profit \| 54,490 \| 51,011 \| 50,101 \| \| Selling, marketing and admi… |
| 8 | `JNJ_FY2021_2022-01-02:232` | Item 8 › (Dollars and Shares in Millions Except Per Share Amounts) (Note 1) |  | #1 | \| \| 2021 \| 2020 \| 2019 \| \|---\|---\|---\|---\| \| Sales to customers \| $93,775 \| 82,584 \| 82,059 \| \| Cost of products sold \| 29,855 \| 28,427 \| 27,556 \| \| Gross profit \| 63,920 \| 54,157 \| 54,503 \| \| Selling, marketing and admi… |
| 9 | `JNJ_FY2018_2018-12-30:138` | Item 7 › Analysis of Consolidated Earnings Before Provision for Taxes on Income | ✓ | #2 | \| \| 2018 \| \| 2017 \| \| 2016 \| \| \|---\|---\|---\|---\|---\|---\|---\| \| (Dollars in Millions) \| Amount \| % of Sales** \| Amount \| % of Sales** \| Amount \| % of Sales** \| \| Consumer \| $565 \| 4.1% \| 586 \| 4.3 \| 585 \| 4.4 \| \| Pharmace… |
| 10 | `JNJ_FY2021_2022-01-02:274` | Item 8 › Research and Development |  |  | \| Nature/Type of Collaboration \| Statement of Earnings Presentation \| \|---\|---\| \| Third-party sale of product & profit share payments received \| Sales to customers \| \| Royalties/milestones paid to collaborative partner (… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#1 `JNJ_FY2021_2022-01-02:159`** (cited, gold #1)

````text
Item 7.MANAGEMENT’S DISCUSSION AND ANALYSIS OF RESULTS OF OPERATIONS AND FINANCIAL CONDITION > Research and Development Expense: (table)
|  | 2021 |  | 2020 |  |
|---|---|---|---|---|
| (Dollars in Millions) | Amount | % of Sales* | Amount | % of Sales* |
| Consumer Health | $455 | 3.1% | $422 | 3.0% |
| Pharmaceutical | 11,882 | 22.8 | 9,563 | 21.0 |
| Medical Devices | 2,377 | 8.8 | 2,174 | 9.5 |
| Total research and development expense | $14,714 | 15.7% | $12,159 | 14.7% |
| Percent increase/(decrease) over the prior year | 21.0% |  | 7.1% |  |
| *As a percent to segment sales |  |  |  |  |
````

**#8 `JNJ_FY2021_2022-01-02:232`** (gold #1)

````text
Item 8. FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA > (Dollars and Shares in Millions Except Per Share Amounts) (Note 1) (table)
|  | 2021 | 2020 | 2019 |
|---|---|---|---|
| Sales to customers | $93,775 | 82,584 | 82,059 |
| Cost of products sold | 29,855 | 28,427 | 27,556 |
| Gross profit | 63,920 | 54,157 | 54,503 |
| Selling, marketing and administrative expenses | 24,659 | 22,084 | 22,178 |
| Research and development expense | 14,714 | 12,159 | 11,355 |
| In-process research and development (Note 5) | 900 | 181 | 890 |
| Interest income | (53) | (111) | (357) |
| Interest expense, net of portion capitalized (Note 4) | 183 | 201 | 318 |
| Other (income) expense, net | 489 | 2,899 | 2,525 |
| Restructuring (Note 20) | 252 | 247 | 266 |
| Earnings before provision for taxes on income | 22,776 | 16,497 | 17,328 |
| Provision for taxes on income (Note 8) | 1,898 | 1,783 | 2,209 |
| Net earnings | $20,878 | 14,714 | 15,119 |
| Net earnings per share (Notes 1 and 15) |  |  |  |
| Basic | $7.93 | 5.59 | 5.72 |
````

**#9 `JNJ_FY2018_2018-12-30:138`** (cited, gold #2)

````text
Item 7. MANAGEMENT’S DISCUSSION AND ANALYSIS OF RESULTS OF OPERATIONS AND FINANCIAL CONDITION > Analysis of Consolidated Earnings Before Provision for Taxes on Income (table)
|  | 2018 |  | 2017 |  | 2016 |  |
|---|---|---|---|---|---|---|
| (Dollars in Millions) | Amount | % of Sales** | Amount | % of Sales** | Amount | % of Sales** |
| Consumer | $565 | 4.1% | 586 | 4.3 | 585 | 4.4 |
| Pharmaceutical | 8,446 | 20.7 | 8,392 | 23.1 | 7,001 | 20.9 |
| Medical Devices | 1,764 | 6.5 | 1,616 | 6.1 | 1,557 | 6.2 |
| Total research and development expense | $10,775 | 13.2% | 10,594 | 13.9 | 9,143 | 12.7 |
| Percent increase/(decrease) over the prior year | 1.7% |  | 15.9 |  | 1.6 |  |
````

</details>

RQ2 citation match (section level): `cited=[('JNJ', 'Item 7')] gold=[(None, 'Item 7')]`

**System C guardrail** (judge `gpt-5.4`): numerical claims 3, verified 3, ungrounded 0, uncited 0, derived 1; sentence verdicts: supported 0, partial 0, unsupported 0, unchecked 0.


<details><summary>Guardrail sentence verdicts</summary>

| sentence | verdict | judge reason |
|---|---|---|
| Johnson & Johnson's total research and development expense was 13.2% of sales in fiscal 2018 and 15.7% of sales in fiscal 2021, so it increased by 2.5 percentage points from 2018 to 2021 [JNJ FY2018, Item 7, JNJ_FY2018_2018-12-30:138] [JNJ FY2021, Item 7, JNJ_FY2021_2022-01-02:159]. | None |  |

</details>

### System C v2 (agentic multi-hop + XBRL)

Model: `gpt-5.4`. Hops: 1. Chunks retrieved: 8, cited: 1.

**Generated answer**

> The filing evidence provided does not disclose Johnson & Johnson's total research and development expense as a percent of total sales for fiscal year 2018.
>
> For fiscal year 2021, total research and development expense was 15.7% of sales. [JNJ FY2021, Item 7, JNJ_FY2021_2022-01-02:159]
>
> Therefore, the increase in percentage points from 2018 to 2021 is not disclosed in the provided filing evidence.

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `F-JNJ-2018` | SEC XBRL Reported Financials (financials.csv) |  |  | fiscal_year,fiscal_year_end,Revenue,NetIncome,OperatingIncome,TotalAssets,TotalLiabilities,StockholdersEquity,CashAndEquivalents,OperatingCashFlow,EPSDiluted 2018,2018-12-30,81581000000,15297000000,,152954000000,93202000… |
| 2 | `F-JNJ-2021` | SEC XBRL Reported Financials (financials.csv) |  |  | fiscal_year,fiscal_year_end,Revenue,NetIncome,OperatingIncome,TotalAssets,TotalLiabilities,StockholdersEquity,CashAndEquivalents,OperatingCashFlow,EPSDiluted 2021,2022-01-02,93775000000,20878000000,,182018000000,10799500… |
| 3 | `JNJ_FY2021_2022-01-02:159` | Item 7 › Research and Development Expense: | ✓ | #1 | \| \| 2021 \| \| 2020 \| \| \|---\|---\|---\|---\|---\| \| (Dollars in Millions) \| Amount \| % of Sales* \| Amount \| % of Sales* \| \| Consumer Health \| $455 \| 3.1% \| $422 \| 3.0% \| \| Pharmaceutical \| 11,882 \| 22.8 \| 9,563 \| 21.0 \| \| Medi… |
| 4 | `JNJ_FY2018_2018-12-30:234` | Item 8 › Recently Adopted Accounting Standards |  |  | \| (Dollars In millions) \| \| Increase (Decrease) to Net Expense \| \| \|---\|---\|---\|---\| \| \| 2018 \| 2017 \| 2016 \| \| Cost of products sold \| $51 \| 85 \| 104 \| \| Selling, marketing and administrative expenses \| 55 \| 100 \| 122 \|… |
| 5 | `JNJ_FY2021_2022-01-02:160` | Item 7 › Research and Development Expense: |  |  | Research and development activities represent a significant part of the Company's business. These expenditures relate to the processes of discovering, testing and developing new products, upfront payments and development… |
| 6 | `JNJ_FY2021_2022-01-02:158` | Item 7 › Research and Development Expense: |  |  | Research and development expense by segment of business was as follows: |
| 7 | `JNJ_FY2021_2022-01-02:164` | Item 7 › Research and Development Expense: |  |  | \| (Dollars in Billions)(Income)/Expense \| 2021 \| 2020 \| Change \| \|---\|---\|---\|---\| \| Litigation expense(1) \| $2.3 \| 5.1 \| (2.8) \| \| Acquisition, Integration and Divestiture related(2) \| (0.5) \| (1.1) \| 0.6 \| \| (Gains)/lo… |
| 8 | `JNJ_FY2018_2018-12-30:258` | Item 8 › Research and Development |  |  | \| Nature/Type of Collaboration \| Statement of Earnings Presentation \| \|---\|---\| \| Third-party sale of product & profit share payments received \| Sales to customers \| \| Royalties/milestones paid to collaborative partner (… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#3 `JNJ_FY2021_2022-01-02:159`** (cited, gold #1)

````text
Item 7.MANAGEMENT’S DISCUSSION AND ANALYSIS OF RESULTS OF OPERATIONS AND FINANCIAL CONDITION > Research and Development Expense: (table)
|  | 2021 |  | 2020 |  |
|---|---|---|---|---|
| (Dollars in Millions) | Amount | % of Sales* | Amount | % of Sales* |
| Consumer Health | $455 | 3.1% | $422 | 3.0% |
| Pharmaceutical | 11,882 | 22.8 | 9,563 | 21.0 |
| Medical Devices | 2,377 | 8.8 | 2,174 | 9.5 |
| Total research and development expense | $14,714 | 15.7% | $12,159 | 14.7% |
| Percent increase/(decrease) over the prior year | 21.0% |  | 7.1% |  |
| *As a percent to segment sales |  |  |  |  |
````

</details>

RQ2 citation match (section level): `cited=[('JNJ', 'Item 7')] gold=[(None, 'Item 7')]`

**System C guardrail** (judge `gpt-5.4`): numerical claims 1, verified 1, ungrounded 0, uncited 0, derived 0; sentence verdicts: supported 2, partial 0, unsupported 0, unchecked 0.


<details><summary>Guardrail sentence verdicts</summary>

| sentence | verdict | judge reason |
|---|---|---|
| The filing evidence provided does not disclose Johnson & Johnson's total research and development expense as a percent of total sales for fiscal year 2018. | supported | The retrieved evidence gives 2021 total R&D as 15.7% of sales but does not disclose Johnson & Johnson's total R&D expense as a percent of total sales for 2018. |
| For fiscal year 2021, total research and development expense was 15.7% of sales. [JNJ FY2021, Item 7, JNJ_FY2021_2022-01-02:159] | None |  |
| Therefore, the increase in percentage points from 2018 to 2021 is not disclosed in the provided filing evidence. | supported | Because the evidence does not disclose the 2018 total R&D percent of sales, the percentage-point increase from 2018 to 2021 cannot be determined from the provided evidence. |

</details>
