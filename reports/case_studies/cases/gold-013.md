# gold-013: Cross-year table

[← all cases](../README.md) · company: NVIDIA CORP (NVDA) · fiscal year: 2021 · recipe `cross_year_table` · hop `multi` · answer type `numeric` · scope `cross_year` · RQ2 category `multi_company_comparison`

## Gold QA

**Question**

> By what percentage did NVIDIA's net income per diluted share increase from the fiscal year ended January 28, 2018, to the fiscal year ended January 31, 2021?

**Gold answer**

> 43.15%

**Program**: `subtract(6.90, 4.82), divide(#0, 4.82)` → `0.43153526970954353`

**Gold numbers** (RQ2 numeric_accuracy targets): 43.15%

**Gold evidence**

1. `NVDA_FY2021_2021-01-31` · ITEM 7. MANAGEMENT’S DISCUSSION AND ANALYSIS OF FINANCIAL CONDITION AND RESULTS OF OPERATIONS › Fiscal Year 2021 Summary · table

   > Net income per diluted share | $6.90 | $4.52 | Up 53%

2. `NVDA_FY2018_2018-01-28` · ITEM 7. MANAGEMENT’S DISCUSSION AND ANALYSIS OF FINANCIAL CONDITION AND RESULTS OF OPERATIONS › Fiscal Year 2018 Summary · table

   > Net income per diluted share | $4.82 | $2.57 | Up 88%

## Scorecard

| Metric | A (vanilla dense) | B (hybrid + rerank) | C v1 (adaptive multi-hop) | C v2 (agentic multi-hop + XBRL) |
|---|---|---|---|---|
| **Retrieval (RQ1)** | | | | |
| chunks retrieved | 10 | 5 | 9 | 8 |
| recall@5 | 1.00 | 1.00 | 0.50 | 0.50 |
| recall@all | 1.00 | 1.00 | 1.00 | 0.50 |
| complete@all | 1 | 1 | 1 | 0 |
| average precision (lexical) | 0.69 | 0.95 | 0.64 | 0.33 |
| gold evidence first rank | #1: 1, #2: 1 | #1: 1, #2: 1 | #1: 1, #2: 7 | #1: 3, #2: – |
| **Answer (RQ3 string match)** | | | | |
| numeric_correct | ✓ | ✓ | ✓ | ✓ |
| keypoint_recall | – | – | – | – |
| **Answer & citations (RQ2)** | | | | |
| numeric_accuracy | 1.00 | 1.00 | 1.00 | 1.00 |
| citation precision | 1.00 | 1.00 | 0.00 | 0.00 |
| citation recall | 1.00 | 1.00 | 0.00 | 0.00 |
| citation F1 | 1.00 | 1.00 | 0.00 | 0.00 |
| has a citation | 1 | 1 | 1 | 1 |
| grounding error rate | – | – | 0.00 | 0.00 |
| **Cost (RQ3)** | | | | |
| retrieval hops | 1 | 1 | 3 | 1 |
| tokens | 1961 | 1480 | 10565 | 4404 |
| cost (USD) | 0.0003 | 0.0003 | 0.0412 | 0.0160 |
| latency (s) | 2.2 | 7.0 | 22.5 | 7.7 |

Definitions: [README › Metrics](../README.md#metrics). `–` = not applicable (e.g. no gold number, no citations, no guardrail).

## System outputs

### System A (vanilla dense)

Model: `gpt-5.4-2026-03-05`. Hops: 1. Chunks retrieved: 10, cited: 2.

**Generated answer**

> NVIDIA's net income per diluted share increased from **$4.82** in fiscal year ended **January 28, 2018** to **$6.90** in fiscal year ended **January 31, 2021** [8][4].
>
> Percentage increase:
>
> \[
> \frac{6.90 - 4.82}{4.82} \times 100 \approx 43.2\%
> \]
>
> So, the net income per diluted share increased by **about 43.2%** [8][4].

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `NVDA_FY2018_2018-01-28:138` | Item 7 › Table of Contents |  | #1, #2 | We recorded a U.S. tax reform provisional net tax benefit of $133 million associated with the one-time transition tax on our historical foreign earnings and the adjustment of deferred tax balances to the lower corporate … |
| 2 | `NVDA_FY2021_2021-01-31:254` | Item 15 › (In millions, except per share data) |  |  | \| \| Year Ended \| \| \| \|---\|---\|---\|---\| \| \| January 31, 2021 \| January 26, 2020 \| January 27, 2019 \| \| Diluted \| $6.90 \| $4.52 \| $6.63 \| \| Weighted average shares used in per share computation: \| \| \| \| \| Basic \| 617 \| 609… |
| 3 | `NVDA_FY2021_2021-01-31:341` | Item 15 › Note 5 - Net Income Per Share |  | #1 | \| \| Year Ended \| \| \| \|---\|---\|---\|---\| \| \| January 31, 2021 \| January 26, 2020 \| January 27, 2019 \| \| \| (In millions, except per share data) \| \| \| \| Numerator: \| \| \| \| \| Net income \| $4,332 \| $2,796 \| $4,141 \| \| Denomina… |
| 4 | `NVDA_FY2021_2021-01-31:165` | Item 7 › Fiscal Year 2021 Summary | ✓ | #1, #2 | \| \| Year Ended \| \| \| \|---\|---\|---\|---\| \| \| January 31, 2021 \| January 26, 2020 \| Change \| \| \| ($ in millions, except per share data) \| \| \| \| Revenue \| $16,675 \| $10,918 \| Up 53% \| \| Gross margin \| 62.3% \| 62.0% \| Up 30 b… |
| 5 | `NVDA_FY2021_2021-01-31:342` | Item 15 › Note 5 - Net Income Per Share |  |  | (1) Calculated as net income divided by basic weighted average shares. (2) Calculated as net income divided by diluted weighted average shares. |
| 6 | `NVDA_FY2018_2018-01-28:277` | Item 15 › Net Income Per Share |  |  | stock method. |
| 7 | `NVDA_FY2021_2021-01-31:340` | Item 15 › Note 5 - Net Income Per Share |  |  | The following is a reconciliation of the denominator of the basic and diluted net income per share computations for the periods presented: |
| 8 | `NVDA_FY2018_2018-01-28:135` | Item 7 › Fiscal Year 2018 Summary | ✓ | #1, #2 | \| \| Year Ended \| \| \| \|---\|---\|---\|---\| \| \| January 28, 2018 \| January 29, 2017 \| Change \| \| \| ($ in millions, except per share data) \| \| \| \| Revenue \| $9,714 \| $6,910 \| Up 41% \| \| Gross margin \| 59.9% \| 58.8% \| Up 110 bp… |
| 9 | `NVDA_FY2018_2018-01-28:127` | Item 6 |  | #2 | \| \| Year Ended \| \| \| \| \| \|---\|---\|---\|---\|---\|---\| \| \| January 28, 2018 \| January 29, 2017 \| January 31, 2016 (A) \| January 25, 2015 \| January 26, 2014 \| \| Consolidated Statements of Income Data: \| (In millions, except p… |
| 10 | `NVDA_FY2021_2021-01-31:166` | Item 7 › Fiscal Year 2021 Summary |  |  | Revenue for fiscal year 2021 was $16.68 billion, up 53% from a year earlier. |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#1 `NVDA_FY2018_2018-01-28:138`** (gold #1, gold #2)

````text
ITEM 7. MANAGEMENT’S DISCUSSION AND ANALYSIS OF FINANCIAL CONDITION AND RESULTS OF OPERATIONS > Table of Contents
We recorded a U.S. tax reform provisional net tax benefit of $133 million associated with the one-time transition tax on our historical foreign earnings and the adjustment of deferred tax balances to the lower corporate tax rate. Net income and net income per diluted share for fiscal year 2018 were $3.05 billion and $4.82, respectively, up 83% and 88%, respectively, from a year earlier, fueled by strong revenue growth and improved gross and operating margins. We returned $1.25 billion to shareholders in fiscal year 2018 through a combination of $909 million in share repurchases and $341 million in quarterly cash dividends. In November 2017, we declared an increase in our quarterly cash dividend to $0.15 per share from $0.14 per share. For fiscal year 2019, we intend to return $1.25 billion to shareholders through ongoing quarterly cash dividends and share repurchases. Cash, cash equivalents and marketable securities were $7.11 billion as of January 28, 2018, compared with $6.80 billion as of January 29, 2017. The increase was primarily related to the increase in operating income.
````

**#3 `NVDA_FY2021_2021-01-31:341`** (gold #1)

````text
ITEM 15. EXHIBITS, FINANCIAL STATEMENT SCHEDULE > Note 5 - Net Income Per Share (table)
|  | Year Ended |  |  |
|---|---|---|---|
|  | January 31, 2021 | January 26, 2020 | January 27, 2019 |
|  | (In millions, except per share data) |  |  |
| Numerator: |  |  |  |
| Net income | $4,332 | $2,796 | $4,141 |
| Denominator: |  |  |  |
| Basic weighted average shares | 617 | 609 | 608 |
| Dilutive impact of outstanding equity awards | 11 | 9 | 17 |
| Diluted weighted average shares | 628 | 618 | 625 |
| Net income per share: |  |  |  |
| Basic (1) | $7.02 | $4.59 | $6.81 |
| Diluted (2) | $6.90 | $4.52 | $6.63 |
| Equity awards excluded from diluted net income per share because their effect would have been anti-dilutive | 3 | 11 | 5 |
````

**#4 `NVDA_FY2021_2021-01-31:165`** (cited, gold #1, gold #2)

````text
ITEM 7. MANAGEMENT’S DISCUSSION AND ANALYSIS OF FINANCIAL CONDITION AND RESULTS OF OPERATIONS > Fiscal Year 2021 Summary (table)
|  | Year Ended |  |  |
|---|---|---|---|
|  | January 31, 2021 | January 26, 2020 | Change |
|  | ($ in millions, except per share data) |  |  |
| Revenue | $16,675 | $10,918 | Up 53% |
| Gross margin | 62.3% | 62.0% | Up 30 bps |
| Operating expenses | $5,864 | $3,922 | Up 50% |
| Income from operations | $4,532 | $2,846 | Up 59% |
| Net income | $4,332 | $2,796 | Up 55% |
| Net income per diluted share | $6.90 | $4.52 | Up 53% |
````

**#8 `NVDA_FY2018_2018-01-28:135`** (cited, gold #1, gold #2)

````text
ITEM 7. MANAGEMENT’S DISCUSSION AND ANALYSIS OF FINANCIAL CONDITION AND RESULTS OF OPERATIONS > Fiscal Year 2018 Summary (table)
|  | Year Ended |  |  |
|---|---|---|---|
|  | January 28, 2018 | January 29, 2017 | Change |
|  | ($ in millions, except per share data) |  |  |
| Revenue | $9,714 | $6,910 | Up 41% |
| Gross margin | 59.9% | 58.8% | Up 110 bps |
| Operating expenses | $2,612 | $2,129 | Up 23% |
| Income from operations | $3,210 | $1,934 | Up 66% |
| Net income | $3,047 | $1,666 | Up 83% |
| Net income per diluted share | $4.82 | $2.57 | Up 88% |
````

**#9 `NVDA_FY2018_2018-01-28:127`** (gold #2)

````text
ITEM 6. SELECTED FINANCIAL DATA (table)
|  | Year Ended |  |  |  |  |
|---|---|---|---|---|---|
|  | January 28, 2018 | January 29, 2017 | January 31, 2016 (A) | January 25, 2015 | January 26, 2014 |
| Consolidated Statements of Income Data: | (In millions, except per share data) |  |  |  |  |
| Revenue | $9,714 | $6,910 | $5,010 | $4,682 | $4,130 |
| Income from operations | $3,210 | $1,934 | $747 | $759 | $496 |
| Net income | $3,047 | $1,666 | $614 | $631 | $440 |
| Net income per share: |  |  |  |  |  |
| Basic | $5.09 | $3.08 | $1.13 | $1.14 | $0.75 |
| Diluted | $4.82 | $2.57 | $1.08 | $1.12 | $0.74 |
| Weighted average shares used in per share computation: |  |  |  |  |  |
| Basic | 599 | 541 | 543 | 552 | 588 |
| Diluted | 632 | 649 | 569 | 563 | 595 |
````

</details>

RQ2 citation match (section level): `cited=[('NVDA', 'Item 7')] gold=[(None, 'Item 7')]`

### System B (hybrid + rerank)

Model: `gpt-5.4-2026-03-05`. Hops: 1. Chunks retrieved: 5, cited: 2.

**Generated answer**

> NVIDIA’s net income per diluted share increased from **$4.82** in fiscal year 2018 to **$6.90** in fiscal year 2021 [2][3].
>
> Percentage increase:
>
> \[
> \frac{6.90 - 4.82}{4.82} \times 100 \approx 43.2\%
> \]
>
> So, the increase was **approximately 43.2%** [2][3].

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `NVDA_FY2018_2018-01-28:138` | Item 7 › Table of Contents |  | #1, #2 | We recorded a U.S. tax reform provisional net tax benefit of $133 million associated with the one-time transition tax on our historical foreign earnings and the adjustment of deferred tax balances to the lower corporate … |
| 2 | `NVDA_FY2018_2018-01-28:135` | Item 7 › Fiscal Year 2018 Summary | ✓ | #1, #2 | \| \| Year Ended \| \| \| \|---\|---\|---\|---\| \| \| January 28, 2018 \| January 29, 2017 \| Change \| \| \| ($ in millions, except per share data) \| \| \| \| Revenue \| $9,714 \| $6,910 \| Up 41% \| \| Gross margin \| 59.9% \| 58.8% \| Up 110 bp… |
| 3 | `NVDA_FY2021_2021-01-31:165` | Item 7 › Fiscal Year 2021 Summary | ✓ | #1, #2 | \| \| Year Ended \| \| \| \|---\|---\|---\|---\| \| \| January 31, 2021 \| January 26, 2020 \| Change \| \| \| ($ in millions, except per share data) \| \| \| \| Revenue \| $16,675 \| $10,918 \| Up 53% \| \| Gross margin \| 62.3% \| 62.0% \| Up 30 b… |
| 4 | `NVDA_FY2018_2018-01-28:419` | Item 15 › Note 17 - Quarterly Summary (Unaudited) |  |  | \| \| Fiscal Year 2018 Quarters Ended \| \| \| \| \|---\|---\|---\|---\|---\| \| \| January 28, 2018 \| October 28, 2017 \| July 29, 2017 \| April 29, 2017 \| \| \| (In millions, except per share data) \| \| \| \| \| Statements of Income Data: \|… |
| 5 | `NVDA_FY2021_2021-01-31:168` | Item 7 › Table of Contents |  | #1, #2 | Gross margin for fiscal year 2021 was up 30 basis points from a year ago, primarily driven by product mix with higher Data Center and lower Automotive revenue, partially offset by Mellanox acquisition-related charges. Op… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#1 `NVDA_FY2018_2018-01-28:138`** (gold #1, gold #2)

````text
ITEM 7. MANAGEMENT’S DISCUSSION AND ANALYSIS OF FINANCIAL CONDITION AND RESULTS OF OPERATIONS > Table of Contents
We recorded a U.S. tax reform provisional net tax benefit of $133 million associated with the one-time transition tax on our historical foreign earnings and the adjustment of deferred tax balances to the lower corporate tax rate. Net income and net income per diluted share for fiscal year 2018 were $3.05 billion and $4.82, respectively, up 83% and 88%, respectively, from a year earlier, fueled by strong revenue growth and improved gross and operating margins. We returned $1.25 billion to shareholders in fiscal year 2018 through a combination of $909 million in share repurchases and $341 million in quarterly cash dividends. In November 2017, we declared an increase in our quarterly cash dividend to $0.15 per share from $0.14 per share. For fiscal year 2019, we intend to return $1.25 billion to shareholders through ongoing quarterly cash dividends and share repurchases. Cash, cash equivalents and marketable securities were $7.11 billion as of January 28, 2018, compared with $6.80 billion as of January 29, 2017. The increase was primarily related to the increase in operating income.
````

**#2 `NVDA_FY2018_2018-01-28:135`** (cited, gold #1, gold #2)

````text
ITEM 7. MANAGEMENT’S DISCUSSION AND ANALYSIS OF FINANCIAL CONDITION AND RESULTS OF OPERATIONS > Fiscal Year 2018 Summary (table)
|  | Year Ended |  |  |
|---|---|---|---|
|  | January 28, 2018 | January 29, 2017 | Change |
|  | ($ in millions, except per share data) |  |  |
| Revenue | $9,714 | $6,910 | Up 41% |
| Gross margin | 59.9% | 58.8% | Up 110 bps |
| Operating expenses | $2,612 | $2,129 | Up 23% |
| Income from operations | $3,210 | $1,934 | Up 66% |
| Net income | $3,047 | $1,666 | Up 83% |
| Net income per diluted share | $4.82 | $2.57 | Up 88% |
````

**#3 `NVDA_FY2021_2021-01-31:165`** (cited, gold #1, gold #2)

````text
ITEM 7. MANAGEMENT’S DISCUSSION AND ANALYSIS OF FINANCIAL CONDITION AND RESULTS OF OPERATIONS > Fiscal Year 2021 Summary (table)
|  | Year Ended |  |  |
|---|---|---|---|
|  | January 31, 2021 | January 26, 2020 | Change |
|  | ($ in millions, except per share data) |  |  |
| Revenue | $16,675 | $10,918 | Up 53% |
| Gross margin | 62.3% | 62.0% | Up 30 bps |
| Operating expenses | $5,864 | $3,922 | Up 50% |
| Income from operations | $4,532 | $2,846 | Up 59% |
| Net income | $4,332 | $2,796 | Up 55% |
| Net income per diluted share | $6.90 | $4.52 | Up 53% |
````

**#5 `NVDA_FY2021_2021-01-31:168`** (gold #1, gold #2)

````text
ITEM 7. MANAGEMENT’S DISCUSSION AND ANALYSIS OF FINANCIAL CONDITION AND RESULTS OF OPERATIONS > Table of Contents
Gross margin for fiscal year 2021 was up 30 basis points from a year ago, primarily driven by product mix with higher Data Center and lower Automotive revenue, partially offset by Mellanox acquisition-related charges. Operating expenses for fiscal year 2021 were $5.86 billion, up 50% from a year ago. The growth was influenced by the inclusion of Mellanox in the second quarter of fiscal year 2021, employee additions and increases in employee compensation and related expenses. Additionally, acquisition-related and other costs of $411 million primarily include $190 million in non-recurring intangible amortization of Mellanox order backlog, $123 million in recurring amortization of Mellanox intangible assets, and $40 million related to the pending acquisition of Arm. Income from operations for fiscal year 2021 was $4.53 billion, up 59% from a year earlier. Net income and net income per diluted share for fiscal year 2021 were $4.33 billion and $6.90, up 55% and 53%, respectively, from a year earlier.
````

</details>

RQ2 citation match (section level): `cited=[('NVDA', 'Item 7')] gold=[(None, 'Item 7')]`

### System C v1 (adaptive multi-hop)

Model: `gpt-5.4`. Hops: 3. Chunks retrieved: 9, cited: 2.

**Generated answer**

> NVIDIA's net income per diluted share increased from $4.82 for the fiscal year ended January 28, 2018 to $6.90 for the fiscal year ended January 31, 2021 [NVDA FY2018, Item 15, NVDA_FY2018_2018-01-28:315] [NVDA FY2021, Item 15, NVDA_FY2021_2021-01-31:341].  
> The increase was approximately 43.2%, calculated as (($6.90 - $4.82) / $4.82) × 100 [NVDA FY2018, Item 15, NVDA_FY2018_2018-01-28:315] [NVDA FY2021, Item 15, NVDA_FY2021_2021-01-31:341].

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `NVDA_FY2021_2021-01-31:341` | Item 15 › Note 5 - Net Income Per Share | ✓ | #1 | \| \| Year Ended \| \| \| \|---\|---\|---\|---\| \| \| January 31, 2021 \| January 26, 2020 \| January 27, 2019 \| \| \| (In millions, except per share data) \| \| \| \| Numerator: \| \| \| \| \| Net income \| $4,332 \| $2,796 \| $4,141 \| \| Denomina… |
| 2 | `NVDA_FY2021_2021-01-31:340` | Item 15 › Note 5 - Net Income Per Share |  |  | The following is a reconciliation of the denominator of the basic and diluted net income per share computations for the periods presented: |
| 3 | `NVDA_FY2018_2018-01-28:314` | Item 15 › Note 3 - Net Income Per Share |  |  | The following is a reconciliation of the denominator of the basic and diluted net income per share computations for the periods presented: |
| 4 | `NVDA_FY2021_2021-01-31:342` | Item 15 › Note 5 - Net Income Per Share |  |  | (1) Calculated as net income divided by basic weighted average shares. (2) Calculated as net income divided by diluted weighted average shares. |
| 5 | `NVDA_FY2021_2021-01-31:287` | Item 15 › Net Income Per Share |  |  | Basic net income per share is computed using the weighted average number of common shares outstanding during the period. Diluted net income per share is computed using the weighted average number of common and potentiall… |
| 6 | `NVDA_FY2018_2018-01-28:316` | Item 15 › Note 3 - Net Income Per Share |  |  | (1) Calculated as net income divided by basic weighted average shares. (2) Calculated as net income divided by diluted weighted average shares. The 1.00% Convertible Senior Notes, or the Convertible Notes, are included i… |
| 7 | `NVDA_FY2018_2018-01-28:315` | Item 15 › Note 3 - Net Income Per Share | ✓ | #2 | \| \| Year Ended \| \| \| \|---\|---\|---\|---\| \| \| January 28, 2018 \| January 29, 2017 \| January 31, 2016 \| \| \| (In millions, except per share data) \| \| \| \| Numerator: \| \| \| \| \| Net income \| $3,047 \| $1,666 \| $614 \| \| Denominato… |
| 8 | `NVDA_FY2021_2021-01-31:359` | Item 15 › Note 10 - Balance Sheet Components |  |  | \| \| January 31, 2021 \| January 26, 2020 \| \|---\|---\|---\| \| \| (In millions) \| \| \| Inventories: \| \| \| \| Raw materials \| $632 \| $249 \| \| Work in-process \| 457 \| 265 \| \| Finished goods \| 737 \| 465 \| \| Total inventories \| $1,8… |
| 9 | `NVDA_FY2021_2021-01-31:254` | Item 15 › (In millions, except per share data) |  |  | \| \| Year Ended \| \| \| \|---\|---\|---\|---\| \| \| January 31, 2021 \| January 26, 2020 \| January 27, 2019 \| \| Diluted \| $6.90 \| $4.52 \| $6.63 \| \| Weighted average shares used in per share computation: \| \| \| \| \| Basic \| 617 \| 609… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#1 `NVDA_FY2021_2021-01-31:341`** (cited, gold #1)

````text
ITEM 15. EXHIBITS, FINANCIAL STATEMENT SCHEDULE > Note 5 - Net Income Per Share (table)
|  | Year Ended |  |  |
|---|---|---|---|
|  | January 31, 2021 | January 26, 2020 | January 27, 2019 |
|  | (In millions, except per share data) |  |  |
| Numerator: |  |  |  |
| Net income | $4,332 | $2,796 | $4,141 |
| Denominator: |  |  |  |
| Basic weighted average shares | 617 | 609 | 608 |
| Dilutive impact of outstanding equity awards | 11 | 9 | 17 |
| Diluted weighted average shares | 628 | 618 | 625 |
| Net income per share: |  |  |  |
| Basic (1) | $7.02 | $4.59 | $6.81 |
| Diluted (2) | $6.90 | $4.52 | $6.63 |
| Equity awards excluded from diluted net income per share because their effect would have been anti-dilutive | 3 | 11 | 5 |
````

**#7 `NVDA_FY2018_2018-01-28:315`** (cited, gold #2)

````text
ITEM 15. EXHIBITS, FINANCIAL STATEMENT SCHEDULE > Note 3 - Net Income Per Share (table)
|  | Year Ended |  |  |
|---|---|---|---|
|  | January 28, 2018 | January 29, 2017 | January 31, 2016 |
|  | (In millions, except per share data) |  |  |
| Numerator: |  |  |  |
| Net income | $3,047 | $1,666 | $614 |
| Denominator: |  |  |  |
| Basic weighted average shares | 599 | 541 | 543 |
| Dilutive impact of outstanding securities: |  |  |  |
| Equity awards | 24 | 26 | 13 |
| 1.00% Convertible Senior Notes | 5 | 44 | 13 |
| Warrants issued with the 1.00% Convertible Senior Notes | 4 | 38 | — |
| Diluted weighted average shares | 632 | 649 | 569 |
| Net income per share: |  |  |  |
| Basic (1) | $5.09 | $3.08 | $1.13 |
| Diluted (2) | $4.82 | $2.57 | $1.08 |
| Equity awards excluded from diluted net income per share because their effect would have been anti-dilutive | 4 | 8 | 10 |
````

</details>

RQ2 citation match (section level): `cited=[('NVDA', 'Item 15')] gold=[(None, 'Item 7')]`

**System C guardrail** (judge `gpt-5.4`): numerical claims 6, verified 6, ungrounded 0, uncited 0, derived 1; sentence verdicts: supported 0, partial 0, unsupported 0, unchecked 0.


<details><summary>Guardrail sentence verdicts</summary>

| sentence | verdict | judge reason |
|---|---|---|
| NVIDIA's net income per diluted share increased from $4.82 for the fiscal year ended January 28, 2018 to $6.90 for the fiscal year ended January 31, 2021 [NVDA FY2018, Item 15, NVDA_FY2018_2018-01-28:315] [NVDA FY2021, Item 15, NVDA_FY2021_2021-01-31:341]. | None |  |
| The increase was approximately 43.2%, calculated as (($6.90 - $4.82) / $4.82) × 100 [NVDA FY2018, Item 15, NVDA_FY2018_2018-01-28:315] [NVDA FY2021, Item 15, NVDA_FY2021_2021-01-31:341]. | None |  |

</details>

### System C v2 (agentic multi-hop + XBRL)

Model: `gpt-5.4`. Hops: 1. Chunks retrieved: 8, cited: 2.

**Generated answer**

> NVIDIA's diluted net income per share increased from $4.82 for the fiscal year ended January 28, 2018 to $6.90 for the fiscal year ended January 31, 2021 [F-NVDA-2018] [F-NVDA-2021].  
> The percentage increase was approximately 43.2%, calculated as (($6.90 - $4.82) / $4.82) × 100 [F-NVDA-2018] [F-NVDA-2021].

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `F-NVDA-2018` | SEC XBRL Reported Financials (financials.csv) | ✓ |  | fiscal_year,fiscal_year_end,Revenue,NetIncome,OperatingIncome,TotalAssets,TotalLiabilities,StockholdersEquity,CashAndEquivalents,OperatingCashFlow,EPSDiluted 2018,2018-01-28,9714000000,3047000000,3210000000,11241000000,3… |
| 2 | `F-NVDA-2021` | SEC XBRL Reported Financials (financials.csv) | ✓ |  | fiscal_year,fiscal_year_end,Revenue,NetIncome,OperatingIncome,TotalAssets,TotalLiabilities,StockholdersEquity,CashAndEquivalents,OperatingCashFlow,EPSDiluted 2021,2021-01-31,16675000000,4332000000,4532000000,28791000000,… |
| 3 | `NVDA_FY2021_2021-01-31:341` | Item 15 › Note 5 - Net Income Per Share |  | #1 | \| \| Year Ended \| \| \| \|---\|---\|---\|---\| \| \| January 31, 2021 \| January 26, 2020 \| January 27, 2019 \| \| \| (In millions, except per share data) \| \| \| \| Numerator: \| \| \| \| \| Net income \| $4,332 \| $2,796 \| $4,141 \| \| Denomina… |
| 4 | `NVDA_FY2021_2021-01-31:340` | Item 15 › Note 5 - Net Income Per Share |  |  | The following is a reconciliation of the denominator of the basic and diluted net income per share computations for the periods presented: |
| 5 | `NVDA_FY2018_2018-01-28:314` | Item 15 › Note 3 - Net Income Per Share |  |  | The following is a reconciliation of the denominator of the basic and diluted net income per share computations for the periods presented: |
| 6 | `NVDA_FY2021_2021-01-31:342` | Item 15 › Note 5 - Net Income Per Share |  |  | (1) Calculated as net income divided by basic weighted average shares. (2) Calculated as net income divided by diluted weighted average shares. |
| 7 | `NVDA_FY2021_2021-01-31:287` | Item 15 › Net Income Per Share |  |  | Basic net income per share is computed using the weighted average number of common shares outstanding during the period. Diluted net income per share is computed using the weighted average number of common and potentiall… |
| 8 | `NVDA_FY2018_2018-01-28:316` | Item 15 › Note 3 - Net Income Per Share |  |  | (1) Calculated as net income divided by basic weighted average shares. (2) Calculated as net income divided by diluted weighted average shares. The 1.00% Convertible Senior Notes, or the Convertible Notes, are included i… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#1 `F-NVDA-2018`** (cited)

````text
[F-NVDA-2018] (NVDA FY2018 reported financials; amounts in USD, EPSDiluted in USD per share)
fiscal_year,fiscal_year_end,Revenue,NetIncome,OperatingIncome,TotalAssets,TotalLiabilities,StockholdersEquity,CashAndEquivalents,OperatingCashFlow,EPSDiluted
2018,2018-01-28,9714000000,3047000000,3210000000,11241000000,3770000000,7471000000,4002000000,3502000000,4.82
````

**#2 `F-NVDA-2021`** (cited)

````text
[F-NVDA-2021] (NVDA FY2021 reported financials; amounts in USD, EPSDiluted in USD per share)
fiscal_year,fiscal_year_end,Revenue,NetIncome,OperatingIncome,TotalAssets,TotalLiabilities,StockholdersEquity,CashAndEquivalents,OperatingCashFlow,EPSDiluted
2021,2021-01-31,16675000000,4332000000,4532000000,28791000000,11898000000,16893000000,847000000,5822000000,6.9
````

**#3 `NVDA_FY2021_2021-01-31:341`** (gold #1)

````text
ITEM 15. EXHIBITS, FINANCIAL STATEMENT SCHEDULE > Note 5 - Net Income Per Share (table)
|  | Year Ended |  |  |
|---|---|---|---|
|  | January 31, 2021 | January 26, 2020 | January 27, 2019 |
|  | (In millions, except per share data) |  |  |
| Numerator: |  |  |  |
| Net income | $4,332 | $2,796 | $4,141 |
| Denominator: |  |  |  |
| Basic weighted average shares | 617 | 609 | 608 |
| Dilutive impact of outstanding equity awards | 11 | 9 | 17 |
| Diluted weighted average shares | 628 | 618 | 625 |
| Net income per share: |  |  |  |
| Basic (1) | $7.02 | $4.59 | $6.81 |
| Diluted (2) | $6.90 | $4.52 | $6.63 |
| Equity awards excluded from diluted net income per share because their effect would have been anti-dilutive | 3 | 11 | 5 |
````

</details>

RQ2 citation match (section level): `cited=[('NVDA', 'XBRL')] gold=[(None, 'Item 7')]`

**System C guardrail** (judge `gpt-5.4`): numerical claims 6, verified 6, ungrounded 0, uncited 0, derived 1; sentence verdicts: supported 0, partial 0, unsupported 0, unchecked 0.


<details><summary>Guardrail sentence verdicts</summary>

| sentence | verdict | judge reason |
|---|---|---|
| NVIDIA's diluted net income per share increased from $4.82 for the fiscal year ended January 28, 2018 to $6.90 for the fiscal year ended January 31, 2021 [F-NVDA-2018] [F-NVDA-2021]. | None |  |
| The percentage increase was approximately 43.2%, calculated as (($6.90 - $4.82) / $4.82) × 100 [F-NVDA-2018] [F-NVDA-2021]. | None |  |

</details>
