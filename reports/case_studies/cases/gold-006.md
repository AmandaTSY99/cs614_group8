# gold-006: Multi-hop table (one filing)

[← all cases](../README.md) · company: AMAZON COM INC (AMZN) · fiscal year: 2016 · recipe `table` · hop `multi` · answer type `numeric` · scope `single_doc` · RQ2 category `quantitative_tabular`

## Gold QA

**Question**

> What is the percentage of Amazon.com's total future principal payments due after 2021 relative to the total future principal payments due in 2017, based on the data provided in the 10-K for fiscal year 2016?

**Gold answer**

> 497.16%

**Program**: `divide(5250, 1056), multiply(#0, 100)` → `497.15909090909093`

**Gold numbers** (RQ2 numeric_accuracy targets): 497.16%

**Gold evidence**

1. `AMZN_FY2016_2016-12-31` · Item 8. Financial Statements and Supplementary Data › Note 5—LONG-TERM DEBT · table

   > | Thereafter | 5,250 |

2. `AMZN_FY2016_2016-12-31` · Item 8. Financial Statements and Supplementary Data › Note 5—LONG-TERM DEBT · table

   > | 2017 | $1,056 |

## Scorecard

| Metric | A (vanilla dense) | B (hybrid + rerank) | C v1 (adaptive multi-hop) | C v2 (agentic multi-hop + XBRL) |
|---|---|---|---|---|
| **Retrieval (RQ1)** | | | | |
| chunks retrieved | 10 | 5 | 6 | 7 |
| recall@5 | 0.50 | 0.00 | 0.50 | 0.00 |
| recall@all | 1.00 | 0.00 | 1.00 | 0.50 |
| complete@all | 1 | 0 | 1 | 0 |
| average precision (lexical) | 0.42 | 0.00 | 0.29 | 0.17 |
| gold evidence first rank | #1: 6, #2: 2 | #1: –, #2: – | #1: 6, #2: 4 | #1: –, #2: 6 |
| **Answer (RQ3 string match)** | | | | |
| numeric_correct | ✓ | ✗ | ✓ | ✗ |
| keypoint_recall | – | – | – | – |
| **Answer & citations (RQ2)** | | | | |
| numeric_accuracy | 1.00 | 0.00 | 1.00 | 0.00 |
| citation precision | 1.00 | – | 1.00 | 1.00 |
| citation recall | 1.00 | – | 1.00 | 1.00 |
| citation F1 | 1.00 | – | 1.00 | 1.00 |
| has a citation | 1 | 0 | 1 | 1 |
| grounding error rate | – | – | 0.00 | 0.00 |
| **Cost (RQ3)** | | | | |
| retrieval hops | 1 | 1 | 1 | 1 |
| tokens | 2650 | 1355 | 4717 | 5146 |
| cost (USD) | 0.0004 | 0.0002 | 0.0164 | 0.0174 |
| latency (s) | 2.3 | 5.9 | 7.3 | 7.6 |

Definitions: [README › Metrics](../README.md#metrics). `–` = not applicable (e.g. no gold number, no citations, no guardrail).

## System outputs

### System A (vanilla dense)

Model: `gpt-5.4-2026-03-05`. Hops: 1. Chunks retrieved: 10, cited: 1.

**Generated answer**

> Amazon.com’s total future **principal payments due after 2021** were **$5,250 million**, and the amount due in **2017** was **$1,056 million** [6].
>
> Percentage relative to 2017:
>
> \[
> \frac{5,250}{1,056} \times 100 \approx 497.2\%
> \]
>
> So, the future principal payments due **after 2021** were approximately **497.2%** of the principal payments due in **2017** [6].

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `AMZN_FY2016_2016-12-31:285` | Item 8 › Commitments |  |  | \| \| Year Ended December 31, \| \| \| \| \| \| \| \|---\|---\|---\|---\|---\|---\|---\|---\| \| \| 2017 \| 2018 \| 2019 \| 2020 \| 2021 \| Thereafter \| Total \| \| Debt principal and interest \| $1,343 \| $312 \| $1,551 \| $463 \| $1,246 \| $7,911 \| $1… |
| 2 | `AMZN_FY2016_2016-12-31:270` | Item 8 › Note 5—LONG-TERM DEBT |  | #2 | \| \| December 31, \| \| \|---\|---\|---\| \| \| 2015 \| 2016 \| \| 1.20% Notes due on November 29, 2017 (1) \| 1,000 \| 1,000 \| \| 2.60% Notes due on December 5, 2019 (2) \| 1,000 \| 1,000 \| \| 3.30% Notes due on December 5, 2021 (2) \| 1,… |
| 3 | `AMZN_FY2016_2016-12-31:171` | Item 7A › Interest Rate Risk |  |  | \| 1.20% Notes due on November 29, 2017 \| $1,000 \| \|---\|---\| \| 2.60% Notes due on December 5, 2019 \| $1,000 \| \| 3.30% Notes due on December 5, 2021 \| $1,000 \| \| 2.50% Notes due on November 29, 2022 \| $1,250 \| \| 3.80% Note… |
| 4 | `AMZN_FY2016_2016-12-31:184` | Item 8 › (in millions, except per share data) |  |  | \| \| Year Ended December 31, \| \| \| \|---\|---\|---\|---\| \| \| 2014 \| 2015 \| 2016 \| \| Net product sales \| $70,080 \| $79,268 \| $94,665 \| \| Net service sales \| 18,908 \| 27,738 \| 41,322 \| \| Total net sales \| 88,988 \| 107,006 \| 135… |
| 5 | `AMZN_FY2016_2016-12-31:189` | Item 8 › (in millions, except per share data) |  |  | \| \| December 31, \| \| \|---\|---\|---\| \| \| 2015 \| 2016 \| \| ASSETS \| \| \| \| Current assets: \| \| \| \| Cash and cash equivalents \| $15,890 \| $19,334 \| \| Marketable securities \| 3,918 \| 6,647 \| \| Inventories \| 10,243 \| 11,461 \| \| … |
| 6 | `AMZN_FY2016_2016-12-31:274` | Item 8 › Note 5—LONG-TERM DEBT | ✓ | #1, #2 | \| Year Ended December 31, \| \| \|---\|---\| \| 2017 \| $1,056 \| \| 2018 \| 37 \| \| 2019 \| 1,278 \| \| 2020 \| 217 \| \| 2021 \| 1,000 \| \| Thereafter \| 5,250 \| \| \| $8,838 \| |
| 7 | `AMZN_FY2016_2016-12-31:181` | Item 8 › (in millions) |  |  | \| \| Year Ended December 31, \| \| \| \|---\|---\|---\|---\| \| \| 2014 \| 2015 \| 2016 \| \| Repayments of long-term debt and other \| (513) \| (1,652) \| (354) \| \| Principal repayments of capital lease obligations \| (1,285) \| (2,462) \| … |
| 8 | `AMZN_FY2016_2016-12-31:81` | Item 1B |  |  | None. |
| 9 | `AMZN_FY2016_2016-12-31:268` | Item 8 › Intangible Assets |  |  | \| Year Ended December 31, \| \| \|---\|---\| \| 2017 \| $264 \| \| 2018 \| 203 \| \| 2019 \| 170 \| \| 2020 \| 103 \| \| 2021 \| 38 \| \| Thereafter \| 76 \| \| \| $854 \| |
| 10 | `AMZN_FY2016_2016-12-31:252` | Item 8 › Note 2—CASH, CASH EQUIVALENTS, AND MARKETABLE SECURITIES |  |  | \| \| Amortized Cost \| Estimated Fair Value \| \|---\|---\|---\| \| Due within one year \| $16,532 \| $16,531 \| \| Due after one year through five years \| 2,766 \| 2,760 \| \| Due after five years through ten years \| 203 \| 202 \| \| Due… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#2 `AMZN_FY2016_2016-12-31:270`** (gold #2)

````text
Item 8. Financial Statements and Supplementary Data > Note 5—LONG-TERM DEBT (table)
|  | December 31, |  |
|---|---|---|
|  | 2015 | 2016 |
| 1.20% Notes due on November 29, 2017 (1) | 1,000 | 1,000 |
| 2.60% Notes due on December 5, 2019 (2) | 1,000 | 1,000 |
| 3.30% Notes due on December 5, 2021 (2) | 1,000 | 1,000 |
| 2.50% Notes due on November 29, 2022 (1) | 1,250 | 1,250 |
| 3.80% Notes due on December 5, 2024 (2) | 1,250 | 1,250 |
| 4.80% Notes due on December 5, 2034 (2) | 1,250 | 1,250 |
| 4.95% Notes due on December 5, 2044 (2) | 1,500 | 1,500 |
| Credit Facility | — | 495 |
| Other long-term debt | 312 | 93 |
| Total debt | 8,562 | 8,838 |
| Less current portion of long-term debt | (238) | (1,056) |
| Face value of long-term debt | $8,324 | $7,782 |
````

**#6 `AMZN_FY2016_2016-12-31:274`** (cited, gold #1, gold #2)

````text
Item 8. Financial Statements and Supplementary Data > Note 5—LONG-TERM DEBT (table)
| Year Ended December 31, |  |
|---|---|
| 2017 | $1,056 |
| 2018 | 37 |
| 2019 | 1,278 |
| 2020 | 217 |
| 2021 | 1,000 |
| Thereafter | 5,250 |
|  | $8,838 |
````

</details>

RQ2 citation match (section level): `cited=[('AMZN', 'Item 8')] gold=[(None, 'Item 8')]`

### System B (hybrid + rerank)

Model: `gpt-5.4-2026-03-05`. Hops: 1. Chunks retrieved: 5, cited: 0.

**Generated answer**

> Not found in the provided context.

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `AMZN_FY2016_2016-12-31:384` | Item 15 › EXHIBIT INDEX |  |  | \| Exhibit Number \| Description \| \|---\|---\| \| 2.1 \| Form of Purchase and Sale Agreement dated as of October 1, 2012, between Acorn Development LLC, a wholly owned subsidiary of the Company, and Lake Union III LLC, Lake Un… |
| 2 | `AMZN_FY2016_2016-12-31:18` | Item 1 |  |  | This Annual Report on Form 10-K and the documents incorporated herein by reference contain forward-looking statements based on expectations, estimates, and projections as of the date of this filing. Actual results may di… |
| 3 | `AMZN_FY2016_2016-12-31:386` | Item 15 › EXHIBIT INDEX |  |  | \| Exhibit Number \| Description \| \|---\|---\| \| 10.5† \| Form of Restricted Stock Unit Agreement for Officers and Employees (incorporated by reference to the Company’s Annual Report on Form 10-K for the Year ended December 3… |
| 4 | `AMZN_FY2016_2016-12-31:273` | Item 8 › Note 5—LONG-TERM DEBT |  |  | The other debt, including the current portion, had a weighted-average interest rate of 3.7% and 3.4% as of December 31, 2015 and 2016. We used the net proceeds from the issuance of this debt primarily to fund certain int… |
| 5 | `AMZN_FY2016_2016-12-31:178` | Item 8 › Report of Independent Registered Public Accounting Firm |  |  | In our opinion, the financial statements referred to above present fairly, in all material respects, the consolidated financial position of Amazon.com, Inc. at December 31, 2016 and 2015, and the consolidated results of … |

RQ2 citation match (section level): `no citations`

### System C v1 (adaptive multi-hop)

Model: `gpt-5.4`. Hops: 1. Chunks retrieved: 6, cited: 1.

**Generated answer**

> Amazon.com’s total future principal payments due after 2021 were $5,250 million, and the total future principal payments due in 2017 were $1,056 million [AMZN FY2016, Item 8, AMZN_FY2016_2016-12-31:274].  
> The percentage of future principal payments due after 2021 relative to those due in 2017 was approximately 497.2% (($5,250 ÷ $1,056) × 100) [AMZN FY2016, Item 8, AMZN_FY2016_2016-12-31:274].

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `AMZN_FY2016_2016-12-31:273` | Item 8 › Note 5—LONG-TERM DEBT |  |  | The other debt, including the current portion, had a weighted-average interest rate of 3.7% and 3.4% as of December 31, 2015 and 2016. We used the net proceeds from the issuance of this debt primarily to fund certain int… |
| 2 | `AMZN_FY2016_2016-12-31:285` | Item 8 › Commitments |  |  | \| \| Year Ended December 31, \| \| \| \| \| \| \| \|---\|---\|---\|---\|---\|---\|---\|---\| \| \| 2017 \| 2018 \| 2019 \| 2020 \| 2021 \| Thereafter \| Total \| \| Debt principal and interest \| $1,343 \| $312 \| $1,551 \| $463 \| $1,246 \| $7,911 \| $1… |
| 3 | `AMZN_FY2016_2016-12-31:269` | Item 8 › Note 5—LONG-TERM DEBT |  |  | In November 2012 and December 2014, we issued $3.0 billion and $6.0 billion of unsecured senior notes, of which $8.3 billion is outstanding, as described in the table below (collectively, the “Notes”). As of December 31,… |
| 4 | `AMZN_FY2016_2016-12-31:270` | Item 8 › Note 5—LONG-TERM DEBT |  | #2 | \| \| December 31, \| \| \|---\|---\|---\| \| \| 2015 \| 2016 \| \| 1.20% Notes due on November 29, 2017 (1) \| 1,000 \| 1,000 \| \| 2.60% Notes due on December 5, 2019 (2) \| 1,000 \| 1,000 \| \| 3.30% Notes due on December 5, 2021 (2) \| 1,… |
| 5 | `AMZN_FY2016_2016-12-31:181` | Item 8 › (in millions) |  |  | \| \| Year Ended December 31, \| \| \| \|---\|---\|---\|---\| \| \| 2014 \| 2015 \| 2016 \| \| Repayments of long-term debt and other \| (513) \| (1,652) \| (354) \| \| Principal repayments of capital lease obligations \| (1,285) \| (2,462) \| … |
| 6 | `AMZN_FY2016_2016-12-31:274` | Item 8 › Note 5—LONG-TERM DEBT | ✓ | #1, #2 | \| Year Ended December 31, \| \| \|---\|---\| \| 2017 \| $1,056 \| \| 2018 \| 37 \| \| 2019 \| 1,278 \| \| 2020 \| 217 \| \| 2021 \| 1,000 \| \| Thereafter \| 5,250 \| \| \| $8,838 \| |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#4 `AMZN_FY2016_2016-12-31:270`** (gold #2)

````text
Item 8. Financial Statements and Supplementary Data > Note 5—LONG-TERM DEBT (table)
|  | December 31, |  |
|---|---|---|
|  | 2015 | 2016 |
| 1.20% Notes due on November 29, 2017 (1) | 1,000 | 1,000 |
| 2.60% Notes due on December 5, 2019 (2) | 1,000 | 1,000 |
| 3.30% Notes due on December 5, 2021 (2) | 1,000 | 1,000 |
| 2.50% Notes due on November 29, 2022 (1) | 1,250 | 1,250 |
| 3.80% Notes due on December 5, 2024 (2) | 1,250 | 1,250 |
| 4.80% Notes due on December 5, 2034 (2) | 1,250 | 1,250 |
| 4.95% Notes due on December 5, 2044 (2) | 1,500 | 1,500 |
| Credit Facility | — | 495 |
| Other long-term debt | 312 | 93 |
| Total debt | 8,562 | 8,838 |
| Less current portion of long-term debt | (238) | (1,056) |
| Face value of long-term debt | $8,324 | $7,782 |
````

**#6 `AMZN_FY2016_2016-12-31:274`** (cited, gold #1, gold #2)

````text
Item 8. Financial Statements and Supplementary Data > Note 5—LONG-TERM DEBT (table)
| Year Ended December 31, |  |
|---|---|
| 2017 | $1,056 |
| 2018 | 37 |
| 2019 | 1,278 |
| 2020 | 217 |
| 2021 | 1,000 |
| Thereafter | 5,250 |
|  | $8,838 |
````

</details>

RQ2 citation match (section level): `cited=[('AMZN', 'Item 8')] gold=[(None, 'Item 8')]`

**System C guardrail** (judge `gpt-5.4`): numerical claims 5, verified 5, ungrounded 0, uncited 0, derived 1; sentence verdicts: supported 0, partial 0, unsupported 0, unchecked 0.


<details><summary>Guardrail sentence verdicts</summary>

| sentence | verdict | judge reason |
|---|---|---|
| Amazon.com’s total future principal payments due after 2021 were $5,250 million, and the total future principal payments due in 2017 were $1,056 million [AMZN FY2016, Item 8, AMZN_FY2016_2016-12-31:274]. | None |  |
| The percentage of future principal payments due after 2021 relative to those due in 2017 was approximately 497.2% (($5,250 ÷ $1,056) × 100) [AMZN FY2016, Item 8, AMZN_FY2016_2016-12-31:274]. | None |  |

</details>

### System C v2 (agentic multi-hop + XBRL)

Model: `gpt-5.4`. Hops: 1. Chunks retrieved: 7, cited: 1.

**Generated answer**

> As of December 31, 2016, Amazon.com’s total debt principal and interest due thereafter was $7,911 million, and the amount due in 2017 was $1,343 million [AMZN FY2016, Item 8, AMZN_FY2016_2016-12-31:285].  
> The percentage of the amount due after 2021 relative to the amount due in 2017 is approximately 589.1% (($7,911 ÷ $1,343) × 100) [AMZN FY2016, Item 8, AMZN_FY2016_2016-12-31:285].

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `F-AMZN-2016` | SEC XBRL Reported Financials (financials.csv) |  |  | fiscal_year,fiscal_year_end,Revenue,NetIncome,OperatingIncome,TotalAssets,TotalLiabilities,StockholdersEquity,CashAndEquivalents,OperatingCashFlow,EPSDiluted 2016,2016-12-31,135987000000,2371000000,4186000000,83402000000… |
| 2 | `AMZN_FY2016_2016-12-31:252` | Item 8 › Note 2—CASH, CASH EQUIVALENTS, AND MARKETABLE SECURITIES |  |  | \| \| Amortized Cost \| Estimated Fair Value \| \|---\|---\|---\| \| Due within one year \| $16,532 \| $16,531 \| \| Due after one year through five years \| 2,766 \| 2,760 \| \| Due after five years through ten years \| 203 \| 202 \| \| Due… |
| 3 | `AMZN_FY2016_2016-12-31:273` | Item 8 › Note 5—LONG-TERM DEBT |  |  | The other debt, including the current portion, had a weighted-average interest rate of 3.7% and 3.4% as of December 31, 2015 and 2016. We used the net proceeds from the issuance of this debt primarily to fund certain int… |
| 4 | `AMZN_FY2016_2016-12-31:269` | Item 8 › Note 5—LONG-TERM DEBT |  |  | In November 2012 and December 2014, we issued $3.0 billion and $6.0 billion of unsecured senior notes, of which $8.3 billion is outstanding, as described in the table below (collectively, the “Notes”). As of December 31,… |
| 5 | `AMZN_FY2016_2016-12-31:285` | Item 8 › Commitments | ✓ |  | \| \| Year Ended December 31, \| \| \| \| \| \| \| \|---\|---\|---\|---\|---\|---\|---\|---\| \| \| 2017 \| 2018 \| 2019 \| 2020 \| 2021 \| Thereafter \| Total \| \| Debt principal and interest \| $1,343 \| $312 \| $1,551 \| $463 \| $1,246 \| $7,911 \| $1… |
| 6 | `AMZN_FY2016_2016-12-31:270` | Item 8 › Note 5—LONG-TERM DEBT |  | #2 | \| \| December 31, \| \| \|---\|---\|---\| \| \| 2015 \| 2016 \| \| 1.20% Notes due on November 29, 2017 (1) \| 1,000 \| 1,000 \| \| 2.60% Notes due on December 5, 2019 (2) \| 1,000 \| 1,000 \| \| 3.30% Notes due on December 5, 2021 (2) \| 1,… |
| 7 | `AMZN_FY2016_2016-12-31:181` | Item 8 › (in millions) |  |  | \| \| Year Ended December 31, \| \| \| \|---\|---\|---\|---\| \| \| 2014 \| 2015 \| 2016 \| \| Repayments of long-term debt and other \| (513) \| (1,652) \| (354) \| \| Principal repayments of capital lease obligations \| (1,285) \| (2,462) \| … |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#5 `AMZN_FY2016_2016-12-31:285`** (cited)

````text
Item 8. Financial Statements and Supplementary Data > Commitments (table)
|  | Year Ended December 31, |  |  |  |  |  |  |
|---|---|---|---|---|---|---|---|
|  | 2017 | 2018 | 2019 | 2020 | 2021 | Thereafter | Total |
| Debt principal and interest | $1,343 | $312 | $1,551 | $463 | $1,246 | $7,911 | $12,826 |
| Capital lease obligations, including interest (1) | 3,910 | 3,008 | 1,662 | 411 | 190 | 225 | 9,406 |
| Finance lease obligations, including interest (2) | 234 | 244 | 247 | 250 | 252 | 2,006 | 3,233 |
| Operating leases | 1,317 | 1,231 | 1,106 | 1,030 | 896 | 3,930 | 9,510 |
| Unconditional purchase obligations (3) | 655 | 590 | 303 | 96 | 43 | 23 | 1,710 |
| Other commitments (4) (5) | 1,025 | 824 | 621 | 493 | 365 | 3,071 | 6,399 |
| Total commitments | $8,484 | $6,209 | $5,490 | $2,743 | $2,992 | $17,166 | $43,084 |
````

**#6 `AMZN_FY2016_2016-12-31:270`** (gold #2)

````text
Item 8. Financial Statements and Supplementary Data > Note 5—LONG-TERM DEBT (table)
|  | December 31, |  |
|---|---|---|
|  | 2015 | 2016 |
| 1.20% Notes due on November 29, 2017 (1) | 1,000 | 1,000 |
| 2.60% Notes due on December 5, 2019 (2) | 1,000 | 1,000 |
| 3.30% Notes due on December 5, 2021 (2) | 1,000 | 1,000 |
| 2.50% Notes due on November 29, 2022 (1) | 1,250 | 1,250 |
| 3.80% Notes due on December 5, 2024 (2) | 1,250 | 1,250 |
| 4.80% Notes due on December 5, 2034 (2) | 1,250 | 1,250 |
| 4.95% Notes due on December 5, 2044 (2) | 1,500 | 1,500 |
| Credit Facility | — | 495 |
| Other long-term debt | 312 | 93 |
| Total debt | 8,562 | 8,838 |
| Less current portion of long-term debt | (238) | (1,056) |
| Face value of long-term debt | $8,324 | $7,782 |
````

</details>

RQ2 citation match (section level): `cited=[('AMZN', 'Item 8')] gold=[(None, 'Item 8')]`

**System C guardrail** (judge `gpt-5.4`): numerical claims 5, verified 5, ungrounded 0, uncited 0, derived 1; sentence verdicts: supported 0, partial 0, unsupported 0, unchecked 0.


<details><summary>Guardrail sentence verdicts</summary>

| sentence | verdict | judge reason |
|---|---|---|
| As of December 31, 2016, Amazon.com’s total debt principal and interest due thereafter was $7,911 million, and the amount due in 2017 was $1,343 million [AMZN FY2016, Item 8, AMZN_FY2016_2016-12-31:285]. | None |  |
| The percentage of the amount due after 2021 relative to the amount due in 2017 is approximately 589.1% (($7,911 ÷ $1,343) × 100) [AMZN FY2016, Item 8, AMZN_FY2016_2016-12-31:285]. | None |  |

</details>
