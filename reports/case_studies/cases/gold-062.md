# gold-062: Table + text (one filing)

[← all cases](../README.md) · company: Tesla, Inc. (TSLA) · fiscal year: 2020 · recipe `table_text` · hop `multi` · answer type `mixed` · scope `single_doc` · RQ2 category `cross_section_multihop`

## Gold QA

**Question**

> For Tesla, Inc. in fiscal year 2020, what was the percentage increase in total operating lease liabilities from December 31, 2019 to December 31, 2020, and how does the Management's Discussion and Analysis characterize the company's expected capital expenditure levels for 2021 relative to the cash available from core operations?

**Gold answer**

> Total operating lease liabilities increased by 30.07%. The MD&A states that cash generated from core operations is expected to generally be sufficient to cover future capital expenditures (which are projected to be $4.50 to $6.00 billion in 2021).

**Program**: `subtract(1540, 1184), divide(#0, 1184), multiply(#1, 100)` → `30.067567567567565`

**Gold numbers** (RQ2 numeric_accuracy targets): 30.07%

**Key points** (RQ3 keypoint_recall targets)

1. Total operating lease liabilities increased by 30.07%.
2. The company expects core operations cash to be sufficient to cover capital expenditures.
3. Capital expenditures are expected to be between $4.50 billion and $6.00 billion in 2021.

**Gold evidence**

1. `TSLA_FY2020_2020-12-31` · ITEM 8. FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA › Note 13 – Leases · table

   > | Total operating lease liabilities | $1,540 | $1,184 |

2. `TSLA_FY2020_2020-12-31` · ITEM 7. MANAGEMENT’S DISCUSSION AND ANALYSIS OF FINANCIAL CONDITION AND RESULTS OF OPERATIONS › Liquidity and Capital Resources · text

   > We expect that the cash we generate from our core operations will generally be sufficient to cover our future capital expenditures and to pay down our near-term debt obligations, although we may choose to seek alternative financing sources.

3. `TSLA_FY2020_2020-12-31` · ITEM 7. MANAGEMENT’S DISCUSSION AND ANALYSIS OF FINANCIAL CONDITION AND RESULTS OF OPERATIONS › Liquidity and Capital Resources · text

   > we currently expect our capital expenditures to be $4.50 to $6.00 billion in 2021 and in each of the next two fiscal years.

## Scorecard

| Metric | A (vanilla dense) | B (hybrid + rerank) | C v1 (adaptive multi-hop) | C v2 (agentic multi-hop + XBRL) |
|---|---|---|---|---|
| **Retrieval (RQ1)** | | | | |
| chunks retrieved | 10 | 5 | 6 | 7 |
| recall@5 | 0.33 | 0.67 | 0.33 | 0.33 |
| recall@all | 0.33 | 0.67 | 0.33 | 0.33 |
| complete@all | 0 | 0 | 0 | 0 |
| average precision (lexical) | 0.32 | 0.50 | 0.53 | 0.41 |
| gold evidence first rank | #1: 3, #2: –, #3: – | #1: –, #2: 2, #3: 2 | #1: 2, #2: –, #3: – | #1: 3, #2: –, #3: – |
| **Answer (RQ3 string match)** | | | | |
| numeric_correct | ✓ | ✗ | ✓ | ✓ |
| keypoint_recall | 1.00 | 0.00 | 0.67 | 0.67 |
| **Answer & citations (RQ2)** | | | | |
| numeric_accuracy | 1.00 | 0.00 | 1.00 | 1.00 |
| citation precision | 1.00 | – | 1.00 | 1.00 |
| citation recall | 1.00 | – | 0.50 | 0.50 |
| citation F1 | 1.00 | – | 0.67 | 0.67 |
| has a citation | 1 | 0 | 1 | 1 |
| grounding error rate | – | – | 0.00 | 0.00 |
| **Cost (RQ3)** | | | | |
| retrieval hops | 1 | 1 | 1 | 1 |
| tokens | 2525 | 1436 | 5452 | 5972 |
| cost (USD) | 0.0005 | 0.0002 | 0.0201 | 0.0215 |
| latency (s) | 3.9 | 5.7 | 8.6 | 9.1 |

Definitions: [README › Metrics](../README.md#metrics). `–` = not applicable (e.g. no gold number, no citations, no guardrail).

## System outputs

### System A (vanilla dense)

Model: `gpt-5.4-2026-03-05`. Hops: 1. Chunks retrieved: 10, cited: 2.

**Generated answer**

> Tesla’s **total operating lease liabilities** increased from **$1,184 million** at December 31, 2019 to **$1,540 million** at December 31, 2020 [3].
>
> Percentage increase:
> \[
> \frac{1{,}540 - 1{,}184}{1{,}184} \times 100 \approx 30.1\%
> \]
>
> So, the increase was **about 30.1%** [3].
>
> For the second part, the MD&A says that Tesla’s **“sustained growth has allowed our business to generally fund itself, but we will continue a number of capital-intensive projects in upcoming periods”** [8]. The provided context does **not explicitly mention 2021** or directly compare **expected 2021 capital expenditures** to **cash available from core operations**, so that specific year-based comparison is **not in the provided context** [8].

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `TSLA_FY2020_2020-12-31:277` | Item 7 › Summary of Cash Flows |  |  | Net cash provided by operating activities increased by $3.54 billion to $5.94 billion during the year ended December 31, 2020 from $2.40 billion during the year ended December 31, 2019. This increase was primarily due to… |
| 2 | `TSLA_FY2020_2020-12-31:240` | Item 7 › Revenues |  |  | Automotive leasing revenue increased $183 million, or 21%, in the year ended December 31, 2020 as compared to the year ended December 31, 2019, primarily due to an increase in cumulative vehicles under our direct operati… |
| 3 | `TSLA_FY2020_2020-12-31:514` | Item 8 › Note 13 – Leases | ✓ | #1 | \| \| December 31, 2020 \| December 31, 2019 \| \|---\|---\|---\| \| Operating leases: \| \| \| \| Operating lease right-of-use assets \| $1,558 \| $1,218 \| \| Accrued liabilities and other \| $286 \| $228 \| \| Other long-term liabilities … |
| 4 | `TSLA_FY2020_2020-12-31:521` | Item 8 › Note 13 – Leases |  |  | As of December 31, 2020, the maturities of our operating and finance lease liabilities (excluding short-term leases) are as follows (in millions): |
| 5 | `TSLA_FY2020_2020-12-31:247` | Item 7 › Cost of Revenues and Gross Margin |  |  | freight and duty costs from localized procurement and manufacturing in China and a higher sales mix of lower end trims, as well as a decrease of 8,669 Model S and Model X cash deliveries in the year ended December 31, 20… |
| 6 | `TSLA_FY2020_2020-12-31:278` | Item 7 › Summary of Cash Flows |  |  | a larger increase in operating lease vehicles as Model 3 direct leasing was introduced in the second quarter of 2019 and Model Y direct leasing was introduced in the third quarter of 2020, and a larger increase in accoun… |
| 7 | `TSLA_FY2020_2020-12-31:516` | Item 8 › Note 13 – Leases |  | #1 | \| \| Year Ended \| \| \|---\|---\|---\| \| \| December 31, 2020 \| December 31, 2019 \| \| Operating lease expense: \| \| \| \| Operating lease expense (1) \| $451 \| $426 \| \| Finance lease expense: \| \| \| \| Amortization of leased assets \|… |
| 8 | `TSLA_FY2020_2020-12-31:186` | Item 7 › Overview and 2020 Highlights | ✓ |  | In 2020, our net income attributable to common stockholders was $721 million, representing a favorable change of $1.58 billion compared to the prior year. In 2020, our operating margin was 6.3%, representing a favorable … |
| 9 | `TSLA_FY2020_2020-12-31:455` | Item 8 › Note 10 – Other Long-Term Liabilities |  | #1 | \| \| December 31, \| December 31, \| \|---\|---\|---\| \| \| 2020 \| 2019 \| \| Operating lease liabilities \| $1,254 \| $956 \| \| Accrued warranty reserve \| 989 \| 745 \| \| Sales return reserve \| 500 \| 545 \| \| Deferred tax liability \| 1… |
| 10 | `TSLA_FY2020_2020-12-31:520` | Item 8 › Note 13 – Leases |  |  | \| \| Year Ended \| \| \|---\|---\|---\| \| \| December 31, 2020 \| December 31, 2019 \| \| Cash paid for amounts included in the measurement of lease liabilities: \| \| \| \| Operating cash outflows from operating leases \| $456 \| $396 \|… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#3 `TSLA_FY2020_2020-12-31:514`** (cited, gold #1)

````text
ITEM 8. FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA > Note 13 – Leases (table)
|  | December 31, 2020 | December 31, 2019 |
|---|---|---|
| Operating leases: |  |  |
| Operating lease right-of-use assets | $1,558 | $1,218 |
| Accrued liabilities and other | $286 | $228 |
| Other long-term liabilities | 1,254 | 956 |
| Total operating lease liabilities | $1,540 | $1,184 |
| Finance leases: |  |  |
| Solar energy systems, net | $29 | $30 |
| Property, plant and equipment, net | 1,465 | 1,600 |
| Total finance lease assets | $1,494 | $1,630 |
| Current portion of long-term debt and finance leases | $374 | $386 |
| Long-term debt and finance leases, net of current portion | 1,094 | 1,232 |
| Total finance lease liabilities | $1,468 | $1,618 |
````

**#7 `TSLA_FY2020_2020-12-31:516`** (gold #1)

````text
ITEM 8. FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA > Note 13 – Leases (table)
|  | Year Ended |  |
|---|---|---|
|  | December 31, 2020 | December 31, 2019 |
| Operating lease expense: |  |  |
| Operating lease expense (1) | $451 | $426 |
| Finance lease expense: |  |  |
| Amortization of leased assets | $348 | $299 |
| Interest on lease liabilities | 100 | 104 |
| Total finance lease expense | $448 | $403 |
| Total lease expense | $899 | $829 |
````

**#8 `TSLA_FY2020_2020-12-31:186`** (cited)

````text
ITEM 7. MANAGEMENT’S DISCUSSION AND ANALYSIS OF FINANCIAL CONDITION AND RESULTS OF OPERATIONS > Overview and 2020 Highlights
In 2020, our net income attributable to common stockholders was $721 million, representing a favorable change of $1.58 billion compared to the prior year. In 2020, our operating margin was 6.3%, representing a favorable change of 6.6% compared to the prior year. We continue to focus on operational efficiencies, while we have seen an acceleration of non-cash stock-based compensation expense due to a rapid increase in our market capitalization and updates to our business outlook. We ended 2020 with $19.38 billion in cash and cash equivalents, representing an increase of $13.12 billion from the end of 2019. Our cash flows from operating activities during 2020 was $5.94 billion, compared to $2.41 billion during 2019, and capital expenditures amounted to $3.16 billion during 2020, compared to $1.33 billion during 2019. Sustained growth has allowed our business to generally fund itself, but we will continue a number of capital-intensive projects in upcoming periods.
````

**#9 `TSLA_FY2020_2020-12-31:455`** (gold #1)

````text
ITEM 8. FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA > Note 10 – Other Long-Term Liabilities (table)
|  | December 31, | December 31, |
|---|---|---|
|  | 2020 | 2019 |
| Operating lease liabilities | $1,254 | $956 |
| Accrued warranty reserve | 989 | 745 |
| Sales return reserve | 500 | 545 |
| Deferred tax liability | 151 | 66 |
| Resale value guarantees | 19 | 36 |
| Other non-current liabilities | 417 | 343 |
| Total other long-term liabilities | $3,330 | $2,691 |
````

</details>

RQ2 citation match (section level): `cited=[('TSLA', 'Item 8'), ('TSLA', 'Item 7')] gold=[(None, 'Item 8'), (None, 'Item 7')]`

### System B (hybrid + rerank)

Model: `gpt-5.4-2026-03-05`. Hops: 1. Chunks retrieved: 5, cited: 0.

**Generated answer**

> Not found in the provided context.

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `TSLA_FY2020_2020-12-31:240` | Item 7 › Revenues |  |  | Automotive leasing revenue increased $183 million, or 21%, in the year ended December 31, 2020 as compared to the year ended December 31, 2019, primarily due to an increase in cumulative vehicles under our direct operati… |
| 2 | `TSLA_FY2020_2020-12-31:270` | Item 7 › Liquidity and Capital Resources |  | #2, #3 | As discussed in and subject to the considerations referenced in Part II, Item 7, Management's Discussion and Analysis of Financial Condition and Results of Operations—Management Opportunities, Challenges and Risks and 20… |
| 3 | `TSLA_FY2020_2020-12-31:278` | Item 7 › Summary of Cash Flows |  |  | a larger increase in operating lease vehicles as Model 3 direct leasing was introduced in the second quarter of 2019 and Model Y direct leasing was introduced in the third quarter of 2020, and a larger increase in accoun… |
| 4 | `TSLA_FY2020_2020-12-31:247` | Item 7 › Cost of Revenues and Gross Margin |  |  | freight and duty costs from localized procurement and manufacturing in China and a higher sales mix of lower end trims, as well as a decrease of 8,669 Model S and Model X cash deliveries in the year ended December 31, 20… |
| 5 | `TSLA_FY2020_2020-12-31:195` | Item 7 › Management Opportunities, Challenges and Risks and 2021 Outlook |  |  | Our business has recently been consistently generating cash flow from operations in excess of our level of capital spend, and with better working capital management resulting in shorter days sales outstanding than days p… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#2 `TSLA_FY2020_2020-12-31:270`** (gold #2, gold #3)

````text
ITEM 7. MANAGEMENT’S DISCUSSION AND ANALYSIS OF FINANCIAL CONDITION AND RESULTS OF OPERATIONS > Liquidity and Capital Resources
As discussed in and subject to the considerations referenced in Part II, Item 7, Management's Discussion and Analysis of Financial Condition and Results of Operations—Management Opportunities, Challenges and Risks and 2021 Outlook—Cash Flow and Capital Expenditure Trends in this Annual Report on Form 10-K, we currently expect our capital expenditures to be $4.50 to $6.00 billion in 2021 and in each of the next two fiscal years. We expect that the cash we generate from our core operations will generally be sufficient to cover our future capital expenditures and to pay down our near-term debt obligations, although we may choose to seek alternative financing sources. For example, our local subsidiary has entered into credit facilities to support construction and production at Gigafactory Shanghai. See Note 12, Debt, to the consolidated financial statements included elsewhere in this Annual Report on Form 10-K. As always, we continually evaluate our capital expenditure needs and may decide it is best to raise additional capital to fund the rapid growth of our business.
````

</details>

RQ2 citation match (section level): `no citations`

### System C v1 (adaptive multi-hop)

Model: `gpt-5.4`. Hops: 1. Chunks retrieved: 6, cited: 1.

**Generated answer**

> Tesla’s total operating lease liabilities increased from $1,184 million at December 31, 2019 to $1,540 million at December 31, 2020, an increase of approximately 30.1% [TSLA FY2020, Item 8, TSLA_FY2020_2020-12-31:514].  
>
> The filing does not disclose in the provided evidence how Management’s Discussion and Analysis characterizes expected 2021 capital expenditure levels relative to cash available from core operations.

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `TSLA_FY2020_2020-12-31:521` | Item 8 › Note 13 – Leases |  |  | As of December 31, 2020, the maturities of our operating and finance lease liabilities (excluding short-term leases) are as follows (in millions): |
| 2 | `TSLA_FY2020_2020-12-31:455` | Item 8 › Note 10 – Other Long-Term Liabilities |  | #1 | \| \| December 31, \| December 31, \| \|---\|---\|---\| \| \| 2020 \| 2019 \| \| Operating lease liabilities \| $1,254 \| $956 \| \| Accrued warranty reserve \| 989 \| 745 \| \| Sales return reserve \| 500 \| 545 \| \| Deferred tax liability \| 1… |
| 3 | `TSLA_FY2020_2020-12-31:524` | Item 8 › Operating Lease and Sales-type Lease Receivables |  |  | \| \| Operating \| Sales-type \| \|---\|---\|---\| \| \| Leases \| Leases \| \| 2021 \| $774 \| $21 \| \| 2022 \| 594 \| 21 \| \| 2023 \| 351 \| 21 \| \| 2024 \| 206 \| 30 \| \| 2025 \| 191 \| 5 \| \| Thereafter \| 2,102 \| 4 \| \| Gross lease receivables \|… |
| 4 | `TSLA_FY2020_2020-12-31:516` | Item 8 › Note 13 – Leases |  | #1 | \| \| Year Ended \| \| \|---\|---\|---\| \| \| December 31, 2020 \| December 31, 2019 \| \| Operating lease expense: \| \| \| \| Operating lease expense (1) \| $451 \| $426 \| \| Finance lease expense: \| \| \| \| Amortization of leased assets \|… |
| 5 | `TSLA_FY2020_2020-12-31:514` | Item 8 › Note 13 – Leases | ✓ | #1 | \| \| December 31, 2020 \| December 31, 2019 \| \|---\|---\|---\| \| Operating leases: \| \| \| \| Operating lease right-of-use assets \| $1,558 \| $1,218 \| \| Accrued liabilities and other \| $286 \| $228 \| \| Other long-term liabilities … |
| 6 | `TSLA_FY2020_2020-12-31:359` | Item 8 › Note 2 – Summary of Significant Accounting Policies |  |  | 31, 2020, 2019 and 2018, we recognized $77 million, $186 million and $332 million, respectively, of leasing revenue related to this program. The net carrying amount of operating lease vehicles under this program was $43 … |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#2 `TSLA_FY2020_2020-12-31:455`** (gold #1)

````text
ITEM 8. FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA > Note 10 – Other Long-Term Liabilities (table)
|  | December 31, | December 31, |
|---|---|---|
|  | 2020 | 2019 |
| Operating lease liabilities | $1,254 | $956 |
| Accrued warranty reserve | 989 | 745 |
| Sales return reserve | 500 | 545 |
| Deferred tax liability | 151 | 66 |
| Resale value guarantees | 19 | 36 |
| Other non-current liabilities | 417 | 343 |
| Total other long-term liabilities | $3,330 | $2,691 |
````

**#4 `TSLA_FY2020_2020-12-31:516`** (gold #1)

````text
ITEM 8. FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA > Note 13 – Leases (table)
|  | Year Ended |  |
|---|---|---|
|  | December 31, 2020 | December 31, 2019 |
| Operating lease expense: |  |  |
| Operating lease expense (1) | $451 | $426 |
| Finance lease expense: |  |  |
| Amortization of leased assets | $348 | $299 |
| Interest on lease liabilities | 100 | 104 |
| Total finance lease expense | $448 | $403 |
| Total lease expense | $899 | $829 |
````

**#5 `TSLA_FY2020_2020-12-31:514`** (cited, gold #1)

````text
ITEM 8. FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA > Note 13 – Leases (table)
|  | December 31, 2020 | December 31, 2019 |
|---|---|---|
| Operating leases: |  |  |
| Operating lease right-of-use assets | $1,558 | $1,218 |
| Accrued liabilities and other | $286 | $228 |
| Other long-term liabilities | 1,254 | 956 |
| Total operating lease liabilities | $1,540 | $1,184 |
| Finance leases: |  |  |
| Solar energy systems, net | $29 | $30 |
| Property, plant and equipment, net | 1,465 | 1,600 |
| Total finance lease assets | $1,494 | $1,630 |
| Current portion of long-term debt and finance leases | $374 | $386 |
| Long-term debt and finance leases, net of current portion | 1,094 | 1,232 |
| Total finance lease liabilities | $1,468 | $1,618 |
````

</details>

RQ2 citation match (section level): `cited=[('TSLA', 'Item 8')] gold=[(None, 'Item 8'), (None, 'Item 7')]`

**System C guardrail** (judge `gpt-5.4`): numerical claims 3, verified 3, ungrounded 0, uncited 0, derived 1; sentence verdicts: supported 1, partial 0, unsupported 0, unchecked 0.


<details><summary>Guardrail sentence verdicts</summary>

| sentence | verdict | judge reason |
|---|---|---|
| Tesla’s total operating lease liabilities increased from $1,184 million at December 31, 2019 to $1,540 million at December 31, 2020, an increase of approximately 30.1% [TSLA FY2020, Item 8, TSLA_FY2020_2020-12-31:514]. | None |  |
| The filing does not disclose in the provided evidence how Management’s Discussion and Analysis characterizes expected 2021 capital expenditure levels relative to cash available from core operations. | supported | None of the retrieved evidence discusses MD&A or expected 2021 capital expenditures relative to cash from core operations. |

</details>

### System C v2 (agentic multi-hop + XBRL)

Model: `gpt-5.4`. Hops: 1. Chunks retrieved: 7, cited: 1.

**Generated answer**

> Tesla’s total operating lease liabilities increased from $1,184 million at December 31, 2019 to $1,540 million at December 31, 2020, an increase of about 30.1% (($1,540 - $1,184) / $1,184) [TSLA FY2020, Item 8, TSLA_FY2020_2020-12-31:514].  
>
> The filing does not disclose in the provided evidence how Management’s Discussion and Analysis characterizes expected 2021 capital expenditure levels relative to cash available from core operations.

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `F-TSLA-2020` | SEC XBRL Reported Financials (financials.csv) |  |  | fiscal_year,fiscal_year_end,Revenue,NetIncome,OperatingIncome,TotalAssets,TotalLiabilities,StockholdersEquity,CashAndEquivalents,OperatingCashFlow,EPSDiluted 2020,2020-12-31,31536000000,721000000,1994000000,52148000000,2… |
| 2 | `TSLA_FY2020_2020-12-31:521` | Item 8 › Note 13 – Leases |  |  | As of December 31, 2020, the maturities of our operating and finance lease liabilities (excluding short-term leases) are as follows (in millions): |
| 3 | `TSLA_FY2020_2020-12-31:455` | Item 8 › Note 10 – Other Long-Term Liabilities |  | #1 | \| \| December 31, \| December 31, \| \|---\|---\|---\| \| \| 2020 \| 2019 \| \| Operating lease liabilities \| $1,254 \| $956 \| \| Accrued warranty reserve \| 989 \| 745 \| \| Sales return reserve \| 500 \| 545 \| \| Deferred tax liability \| 1… |
| 4 | `TSLA_FY2020_2020-12-31:524` | Item 8 › Operating Lease and Sales-type Lease Receivables |  |  | \| \| Operating \| Sales-type \| \|---\|---\|---\| \| \| Leases \| Leases \| \| 2021 \| $774 \| $21 \| \| 2022 \| 594 \| 21 \| \| 2023 \| 351 \| 21 \| \| 2024 \| 206 \| 30 \| \| 2025 \| 191 \| 5 \| \| Thereafter \| 2,102 \| 4 \| \| Gross lease receivables \|… |
| 5 | `TSLA_FY2020_2020-12-31:516` | Item 8 › Note 13 – Leases |  | #1 | \| \| Year Ended \| \| \|---\|---\|---\| \| \| December 31, 2020 \| December 31, 2019 \| \| Operating lease expense: \| \| \| \| Operating lease expense (1) \| $451 \| $426 \| \| Finance lease expense: \| \| \| \| Amortization of leased assets \|… |
| 6 | `TSLA_FY2020_2020-12-31:514` | Item 8 › Note 13 – Leases | ✓ | #1 | \| \| December 31, 2020 \| December 31, 2019 \| \|---\|---\|---\| \| Operating leases: \| \| \| \| Operating lease right-of-use assets \| $1,558 \| $1,218 \| \| Accrued liabilities and other \| $286 \| $228 \| \| Other long-term liabilities … |
| 7 | `TSLA_FY2020_2020-12-31:359` | Item 8 › Note 2 – Summary of Significant Accounting Policies |  |  | 31, 2020, 2019 and 2018, we recognized $77 million, $186 million and $332 million, respectively, of leasing revenue related to this program. The net carrying amount of operating lease vehicles under this program was $43 … |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#3 `TSLA_FY2020_2020-12-31:455`** (gold #1)

````text
ITEM 8. FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA > Note 10 – Other Long-Term Liabilities (table)
|  | December 31, | December 31, |
|---|---|---|
|  | 2020 | 2019 |
| Operating lease liabilities | $1,254 | $956 |
| Accrued warranty reserve | 989 | 745 |
| Sales return reserve | 500 | 545 |
| Deferred tax liability | 151 | 66 |
| Resale value guarantees | 19 | 36 |
| Other non-current liabilities | 417 | 343 |
| Total other long-term liabilities | $3,330 | $2,691 |
````

**#5 `TSLA_FY2020_2020-12-31:516`** (gold #1)

````text
ITEM 8. FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA > Note 13 – Leases (table)
|  | Year Ended |  |
|---|---|---|
|  | December 31, 2020 | December 31, 2019 |
| Operating lease expense: |  |  |
| Operating lease expense (1) | $451 | $426 |
| Finance lease expense: |  |  |
| Amortization of leased assets | $348 | $299 |
| Interest on lease liabilities | 100 | 104 |
| Total finance lease expense | $448 | $403 |
| Total lease expense | $899 | $829 |
````

**#6 `TSLA_FY2020_2020-12-31:514`** (cited, gold #1)

````text
ITEM 8. FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA > Note 13 – Leases (table)
|  | December 31, 2020 | December 31, 2019 |
|---|---|---|
| Operating leases: |  |  |
| Operating lease right-of-use assets | $1,558 | $1,218 |
| Accrued liabilities and other | $286 | $228 |
| Other long-term liabilities | 1,254 | 956 |
| Total operating lease liabilities | $1,540 | $1,184 |
| Finance leases: |  |  |
| Solar energy systems, net | $29 | $30 |
| Property, plant and equipment, net | 1,465 | 1,600 |
| Total finance lease assets | $1,494 | $1,630 |
| Current portion of long-term debt and finance leases | $374 | $386 |
| Long-term debt and finance leases, net of current portion | 1,094 | 1,232 |
| Total finance lease liabilities | $1,468 | $1,618 |
````

</details>

RQ2 citation match (section level): `cited=[('TSLA', 'Item 8')] gold=[(None, 'Item 8'), (None, 'Item 7')]`

**System C guardrail** (judge `gpt-5.4`): numerical claims 6, verified 6, ungrounded 0, uncited 0, derived 1; sentence verdicts: supported 1, partial 0, unsupported 0, unchecked 0.


<details><summary>Guardrail sentence verdicts</summary>

| sentence | verdict | judge reason |
|---|---|---|
| Tesla’s total operating lease liabilities increased from $1,184 million at December 31, 2019 to $1,540 million at December 31, 2020, an increase of about 30.1% (($1,540 - $1,184) / $1,184) [TSLA FY2020, Item 8, TSLA_FY2020_2020-12-31:514]. | None |  |
| The filing does not disclose in the provided evidence how Management’s Discussion and Analysis characterizes expected 2021 capital expenditure levels relative to cash available from core operations. | supported | The retrieved evidence contains no MD&A discussion of expected 2021 capital expenditures relative to cash from core operations. |

</details>
