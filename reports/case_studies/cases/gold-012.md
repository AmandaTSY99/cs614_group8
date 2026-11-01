# gold-012: Cross-year table

[← all cases](../README.md) · company: AMAZON COM INC (AMZN) · fiscal year: 2024 · recipe `cross_year_table` · hop `multi` · answer type `numeric` · scope `cross_year` · RQ2 category `multi_company_comparison`

## Gold QA

**Question**

> By how many percentage points did the dilutive effect of Amazon's outstanding stock awards, measured as a percentage of the shares used to compute basic earnings per share, change from fiscal year 2018 to fiscal year 2024?

**Gold answer**

> -0.30 percentage points (from about 2.67% in 2018 to about 2.37% in 2024)

**Program**: `divide(248, 10473), divide(13, 487), subtract(#0, #1)` → `-0.0030141062840577035`

**Gold numbers** (RQ2 numeric_accuracy targets): -0.30 percentage points

**Gold evidence**

1. `AMZN_FY2024_2024-12-31` · Item 8. Financial Statements and Supplementary Data › Earnings Per Share · table

   > | Total dilutive effect of outstanding stock awards | — | 188 | 248 |

2. `AMZN_FY2024_2024-12-31` · Item 8. Financial Statements and Supplementary Data › Earnings Per Share · table

   > | Shares used in computation of basic earnings per share | 10,189 | 10,304 | 10,473 |

3. `AMZN_FY2018_2018-12-31` · Item 8. Financial Statements and Supplementary Data › Earnings per Share · table

   > | Total dilutive effect of outstanding stock awards | 10 | 13 | 13 |

4. `AMZN_FY2018_2018-12-31` · Item 8. Financial Statements and Supplementary Data › Earnings per Share · table

   > | Shares used in computation of basic earnings per share | 474 | 480 | 487 |

## Scorecard

| Metric | A (vanilla dense) | B (hybrid + rerank) | C v1 (adaptive multi-hop) | C v2 (agentic multi-hop + XBRL) |
|---|---|---|---|---|
| **Retrieval (RQ1)** | | | | |
| chunks retrieved | 8 | 5 | 6 | 8 |
| recall@5 | 1.00 | 1.00 | 1.00 | 1.00 |
| recall@all | 1.00 | 1.00 | 1.00 | 1.00 |
| complete@all | 1 | 1 | 1 | 1 |
| average precision (lexical) | 0.87 | 1.00 | 0.95 | 0.52 |
| gold evidence first rank | #1: 1, #2: 1, #3: 1, #4: 1 | #1: 1, #2: 1, #3: 1, #4: 1 | #1: 1, #2: 3, #3: 1, #4: 3 | #1: 3, #2: 5, #3: 3, #4: 5 |
| **Answer (RQ3 string match)** | | | | |
| numeric_correct | ✓ | ✓ | ✗ | ✓ |
| keypoint_recall | – | – | – | – |
| **Answer & citations (RQ2)** | | | | |
| numeric_accuracy | 1.00 | 1.00 | 0.00 | 0.00 |
| citation precision | 1.00 | 1.00 | 1.00 | 1.00 |
| citation recall | 1.00 | 1.00 | 1.00 | 1.00 |
| citation F1 | 1.00 | 1.00 | 1.00 | 1.00 |
| has a citation | 1 | 1 | 1 | 1 |
| grounding error rate | – | – | 0.50 | 0.80 |
| **Cost (RQ3)** | | | | |
| retrieval hops | 1 | 1 | 1 | 1 |
| tokens | 1451 | 1394 | 6282 | 7614 |
| cost (USD) | 0.0003 | 0.0003 | 0.0245 | 0.0282 |
| latency (s) | 3.3 | 6.9 | 10.9 | 10.9 |

Definitions: [README › Metrics](../README.md#metrics). `–` = not applicable (e.g. no gold number, no citations, no guardrail).

## System outputs

### System A (vanilla dense)

Model: `gpt-5.4-2026-03-05`. Hops: 1. Chunks retrieved: 8, cited: 2.

**Generated answer**

> In 2018, the dilutive effect as a percentage of basic shares was:
>
> - 13 / 487 = about 2.67% [2]
>
> In 2024, the dilutive effect as a percentage of basic shares was:
>
> - 248 / 10,473 = about 2.37% [1]
>
> Change from 2018 to 2024:
>
> - 2.37% − 2.67% = about **-0.30 percentage points**
>
> So, the dilutive effect **decreased by about 0.30 percentage points** from fiscal year 2018 to fiscal year 2024. [1][2]

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `AMZN_FY2024_2024-12-31:209` | Item 8 › Earnings Per Share | ✓ | #1, #2, #3, #4 | \| \| Year Ended December 31, \| \| \| \|---\|---\|---\|---\| \| \| 2022 \| 2023 \| 2024 \| \| Shares used in computation of basic earnings per share \| 10,189 \| 10,304 \| 10,473 \| \| Total dilutive effect of outstanding stock awards \| — \|… |
| 2 | `AMZN_FY2018_2018-12-31:194` | Item 8 › Earnings per Share | ✓ | #1, #2, #3, #4 | \| \| Year Ended December 31, \| \| \| \|---\|---\|---\|---\| \| \| 2016 \| 2017 \| 2018 \| \| Shares used in computation of basic earnings per share \| 474 \| 480 \| 487 \| \| Total dilutive effect of outstanding stock awards \| 10 \| 13 \| 13… |
| 3 | `AMZN_FY2024_2024-12-31:320` | Item 8 › Common Stock |  |  | Common shares outstanding plus shares underlying outstanding stock awards totaled 10.6 billion, 10.8 billion, and 10.9 billion, as of December 31, 2022, 2023, and 2024. These totals include all vested and unvested stock … |
| 4 | `AMZN_FY2024_2024-12-31:325` | Item 8 › Stock Award Activity |  |  | ___________________ (1)The related tax benefits were $4.3 billion, $5.4 billion, and $5.0 billion for 2022, 2023, and 2024. The following table summarizes our restricted stock unit activity (in millions): |
| 5 | `AMZN_FY2024_2024-12-31:189` | Item 8 › (in millions, except per share data) |  | #2, #4 | \| \| Year Ended December 31, \| \| \| \|---\|---\|---\|---\| \| \| 2022 \| 2023 \| 2024 \| \| Income (loss) before income taxes \| (5,936) \| 37,557 \| 68,614 \| \| Benefit (provision) for income taxes \| 3,217 \| (7,120) \| (9,265) \| \| Equity… |
| 6 | `AMZN_FY2024_2024-12-31:118` | Item 7 › Overview |  |  | devices as well as other initiatives including the development of a satellite network for global broadband service and autonomous vehicles for ride-hailing services. We seek to efficiently manage shareholder dilution whi… |
| 7 | `AMZN_FY2024_2024-12-31:324` | Item 8 › Stock Award Activity |  |  | \| \| Year Ended December 31, \| \| \| \|---\|---\|---\|---\| \| \| 2022 \| 2023 \| 2024 \| \| Cost of sales \| $757 \| $836 \| $838 \| \| Fulfillment \| 2,745 \| 3,090 \| 2,973 \| \| Technology and infrastructure \| 10,621 \| 13,434 \| 12,150 \| \| S… |
| 8 | `AMZN_FY2018_2018-12-31:306` | Item 8 › Common Stock |  |  | Common shares outstanding plus shares underlying outstanding stock awards totaled 497 million, 504 million, and 507 million, as of December 31, 2016, 2017, and 2018. These totals include all vested and unvested stock awa… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#1 `AMZN_FY2024_2024-12-31:209`** (cited, gold #1, gold #2, gold #3, gold #4)

````text
Item 8. Financial Statements and Supplementary Data > Earnings Per Share (table)
|  | Year Ended December 31, |  |  |
|---|---|---|---|
|  | 2022 | 2023 | 2024 |
| Shares used in computation of basic earnings per share | 10,189 | 10,304 | 10,473 |
| Total dilutive effect of outstanding stock awards | — | 188 | 248 |
| Shares used in computation of diluted earnings per share | 10,189 | 10,492 | 10,721 |
````

**#2 `AMZN_FY2018_2018-12-31:194`** (cited, gold #1, gold #2, gold #3, gold #4)

````text
Item 8. Financial Statements and Supplementary Data > Earnings per Share (table)
|  | Year Ended December 31, |  |  |
|---|---|---|---|
|  | 2016 | 2017 | 2018 |
| Shares used in computation of basic earnings per share | 474 | 480 | 487 |
| Total dilutive effect of outstanding stock awards | 10 | 13 | 13 |
| Shares used in computation of diluted earnings per share | 484 | 493 | 500 |
````

**#5 `AMZN_FY2024_2024-12-31:189`** (gold #2, gold #4)

````text
Item 8. Financial Statements and Supplementary Data > (in millions, except per share data) (table)
|  | Year Ended December 31, |  |  |
|---|---|---|---|
|  | 2022 | 2023 | 2024 |
| Income (loss) before income taxes | (5,936) | 37,557 | 68,614 |
| Benefit (provision) for income taxes | 3,217 | (7,120) | (9,265) |
| Equity-method investment activity, net of tax | (3) | (12) | (101) |
| Net income (loss) | $(2,722) | $30,425 | $59,248 |
| Basic earnings per share | $(0.27) | $2.95 | $5.66 |
| Diluted earnings per share | $(0.27) | $2.90 | $5.53 |
| Weighted-average shares used in computation of earnings per share: |  |  |  |
| Basic | 10,189 | 10,304 | 10,473 |
| Diluted | 10,189 | 10,492 | 10,721 |
````

</details>

RQ2 citation match (section level): `cited=[('AMZN', 'Item 8')] gold=[(None, 'Item 8')]`

### System B (hybrid + rerank)

Model: `gpt-5.4-2026-03-05`. Hops: 1. Chunks retrieved: 5, cited: 2.

**Generated answer**

> In 2018, the dilutive effect as a percentage of basic shares was:
>
> - 13 / 487 = 2.67% [2]
>
> In 2024, the dilutive effect as a percentage of basic shares was:
>
> - 248 / 10,473 = 2.37% [1]
>
> Change from 2018 to 2024:
>
> - 2.37% - 2.67% = -0.30 percentage points
>
> So, the dilutive effect decreased by about 0.30 percentage points from 2018 to 2024. [1][2]

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `AMZN_FY2024_2024-12-31:209` | Item 8 › Earnings Per Share | ✓ | #1, #2, #3, #4 | \| \| Year Ended December 31, \| \| \| \|---\|---\|---\|---\| \| \| 2022 \| 2023 \| 2024 \| \| Shares used in computation of basic earnings per share \| 10,189 \| 10,304 \| 10,473 \| \| Total dilutive effect of outstanding stock awards \| — \|… |
| 2 | `AMZN_FY2018_2018-12-31:194` | Item 8 › Earnings per Share | ✓ | #1, #2, #3, #4 | \| \| Year Ended December 31, \| \| \| \|---\|---\|---\|---\| \| \| 2016 \| 2017 \| 2018 \| \| Shares used in computation of basic earnings per share \| 474 \| 480 \| 487 \| \| Total dilutive effect of outstanding stock awards \| 10 \| 13 \| 13… |
| 3 | `AMZN_FY2024_2024-12-31:189` | Item 8 › (in millions, except per share data) |  | #2, #4 | \| \| Year Ended December 31, \| \| \| \|---\|---\|---\|---\| \| \| 2022 \| 2023 \| 2024 \| \| Income (loss) before income taxes \| (5,936) \| 37,557 \| 68,614 \| \| Benefit (provision) for income taxes \| 3,217 \| (7,120) \| (9,265) \| \| Equity… |
| 4 | `AMZN_FY2018_2018-12-31:354` | Item 8 › Note 11 — QUARTERLY RESULTS (UNAUDITED) |  | #2, #4 | \| \| Year Ended December 31, 2017 (1) \| \| \| \| \|---\|---\|---\|---\|---\| \| \| First Quarter \| Second Quarter \| Third Quarter (2) \| Fourth Quarter (2) \| \| Net sales \| $35,714 \| $37,955 \| $43,744 \| $60,453 \| \| Operating income \| … |
| 5 | `AMZN_FY2018_2018-12-31:355` | Item 8 › Note 11 — QUARTERLY RESULTS (UNAUDITED) |  | #2, #4 | \| \| Year Ended December 31, 2018 (1) \| \| \| \| \|---\|---\|---\|---\|---\| \| \| First Quarter \| Second Quarter \| Third Quarter \| Fourth Quarter \| \| Net sales \| $51,042 \| $52,886 \| $56,576 \| $72,383 \| \| Operating income \| 1,927 \| … |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#1 `AMZN_FY2024_2024-12-31:209`** (cited, gold #1, gold #2, gold #3, gold #4)

````text
Item 8. Financial Statements and Supplementary Data > Earnings Per Share (table)
|  | Year Ended December 31, |  |  |
|---|---|---|---|
|  | 2022 | 2023 | 2024 |
| Shares used in computation of basic earnings per share | 10,189 | 10,304 | 10,473 |
| Total dilutive effect of outstanding stock awards | — | 188 | 248 |
| Shares used in computation of diluted earnings per share | 10,189 | 10,492 | 10,721 |
````

**#2 `AMZN_FY2018_2018-12-31:194`** (cited, gold #1, gold #2, gold #3, gold #4)

````text
Item 8. Financial Statements and Supplementary Data > Earnings per Share (table)
|  | Year Ended December 31, |  |  |
|---|---|---|---|
|  | 2016 | 2017 | 2018 |
| Shares used in computation of basic earnings per share | 474 | 480 | 487 |
| Total dilutive effect of outstanding stock awards | 10 | 13 | 13 |
| Shares used in computation of diluted earnings per share | 484 | 493 | 500 |
````

**#3 `AMZN_FY2024_2024-12-31:189`** (gold #2, gold #4)

````text
Item 8. Financial Statements and Supplementary Data > (in millions, except per share data) (table)
|  | Year Ended December 31, |  |  |
|---|---|---|---|
|  | 2022 | 2023 | 2024 |
| Income (loss) before income taxes | (5,936) | 37,557 | 68,614 |
| Benefit (provision) for income taxes | 3,217 | (7,120) | (9,265) |
| Equity-method investment activity, net of tax | (3) | (12) | (101) |
| Net income (loss) | $(2,722) | $30,425 | $59,248 |
| Basic earnings per share | $(0.27) | $2.95 | $5.66 |
| Diluted earnings per share | $(0.27) | $2.90 | $5.53 |
| Weighted-average shares used in computation of earnings per share: |  |  |  |
| Basic | 10,189 | 10,304 | 10,473 |
| Diluted | 10,189 | 10,492 | 10,721 |
````

**#4 `AMZN_FY2018_2018-12-31:354`** (gold #2, gold #4)

````text
Item 8. Financial Statements and Supplementary Data > Note 11 — QUARTERLY RESULTS (UNAUDITED) (table)
|  | Year Ended December 31, 2017 (1) |  |  |  |
|---|---|---|---|---|
|  | First Quarter | Second Quarter | Third Quarter (2) | Fourth Quarter (2) |
| Net sales | $35,714 | $37,955 | $43,744 | $60,453 |
| Operating income | 1,005 | 628 | 347 | 2,127 |
| Income before income taxes | 953 | 666 | 316 | 1,872 |
| Provision for income taxes | (229) | (467) | (58) | (16) |
| Net income | 724 | 197 | 256 | 1,856 |
| Basic earnings per share | 1.52 | 0.41 | 0.53 | 3.85 |
| Diluted earnings per share | 1.48 | 0.40 | 0.52 | 3.75 |
| Shares used in computation of earnings per share: |  |  |  |  |
| Basic | 477 | 479 | 481 | 483 |
| Diluted | 490 | 492 | 494 | 496 |
````

**#5 `AMZN_FY2018_2018-12-31:355`** (gold #2, gold #4)

````text
Item 8. Financial Statements and Supplementary Data > Note 11 — QUARTERLY RESULTS (UNAUDITED) (table)
|  | Year Ended December 31, 2018 (1) |  |  |  |
|---|---|---|---|---|
|  | First Quarter | Second Quarter | Third Quarter | Fourth Quarter |
| Net sales | $51,042 | $52,886 | $56,576 | $72,383 |
| Operating income | 1,927 | 2,983 | 3,724 | 3,786 |
| Income before income taxes | 1,916 | 2,605 | 3,390 | 3,350 |
| Provision for income taxes | (287) | (74) | (508) | (327) |
| Net income | 1,629 | 2,534 | 2,883 | 3,027 |
| Basic earnings per share | 3.36 | 5.21 | 5.91 | 6.18 |
| Diluted earnings per share | 3.27 | 5.07 | 5.75 | 6.04 |
| Shares used in computation of earnings per share: |  |  |  |  |
| Basic | 484 | 486 | 488 | 490 |
| Diluted | 498 | 500 | 501 | 501 |
````

</details>

RQ2 citation match (section level): `cited=[('AMZN', 'Item 8')] gold=[(None, 'Item 8')]`

### System C v1 (adaptive multi-hop)

Model: `gpt-5.4`. Hops: 1. Chunks retrieved: 6, cited: 2.

**Generated answer**

> In fiscal year 2018, the dilutive effect of outstanding stock awards was 13 on basic shares of 487, or about 2.67% [AMZN FY2018, Item 8, AMZN_FY2018_2018-12-31:194].  
> In fiscal year 2024, the dilutive effect of outstanding stock awards was 248 on basic shares of 10,473, or about 2.37% [AMZN FY2024, Item 8, AMZN_FY2024_2024-12-31:209].  
> Therefore, the dilutive effect as a percentage of basic shares decreased by about 0.31 percentage points from 2018 to 2024 [AMZN FY2018, Item 8, AMZN_FY2018_2018-12-31:194] [AMZN FY2024, Item 8, AMZN_FY2024_2024-12-31:209].
>
> > [Guardrail Audit Warning]: Manual verification required; these numerical figures could not be matched in their cited chunks: 0.31; 1 sentence(s) are not supported by their cited chunks.

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `AMZN_FY2018_2018-12-31:193` | Item 8 › Earnings per Share |  | #1, #3 | Basic earnings per share is calculated using our weighted-average outstanding common shares. Diluted earnings per share is calculated using our weighted-average outstanding common shares including the dilutive effect of … |
| 2 | `AMZN_FY2024_2024-12-31:208` | Item 8 › Earnings Per Share |  | #1, #3 | Basic earnings per share is calculated using our weighted-average outstanding common shares. Diluted earnings per share is calculated using our weighted-average outstanding common shares including the dilutive effect of … |
| 3 | `AMZN_FY2018_2018-12-31:194` | Item 8 › Earnings per Share | ✓ | #1, #2, #3, #4 | \| \| Year Ended December 31, \| \| \| \|---\|---\|---\|---\| \| \| 2016 \| 2017 \| 2018 \| \| Shares used in computation of basic earnings per share \| 474 \| 480 \| 487 \| \| Total dilutive effect of outstanding stock awards \| 10 \| 13 \| 13… |
| 4 | `AMZN_FY2018_2018-12-31:104` | Item 7 › Overview |  |  | We seek to efficiently manage shareholder dilution while maintaining the flexibility to issue shares for strategic purposes, such as financings, acquisitions, and aligning employee compensation with shareholders’ interes… |
| 5 | `AMZN_FY2024_2024-12-31:209` | Item 8 › Earnings Per Share | ✓ | #1, #2, #3, #4 | \| \| Year Ended December 31, \| \| \| \|---\|---\|---\|---\| \| \| 2022 \| 2023 \| 2024 \| \| Shares used in computation of basic earnings per share \| 10,189 \| 10,304 \| 10,473 \| \| Total dilutive effect of outstanding stock awards \| — \|… |
| 6 | `AMZN_FY2018_2018-12-31:312` | Item 8 › Stock Award Activity |  |  | \| \| Number of Units \| Weighted Average Grant-Date Fair Value \| \|---\|---\|---\| \| Outstanding as of January 1, 2016 \| 18.9 \| $362 \| \| Units granted \| 9.3 \| 660 \| \| Units vested \| (6.1) \| 321 \| \| Units forfeited \| (2.3) \| 44… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#1 `AMZN_FY2018_2018-12-31:193`** (gold #1, gold #3)

````text
Item 8. Financial Statements and Supplementary Data > Earnings per Share
Basic earnings per share is calculated using our weighted-average outstanding common shares. Diluted earnings per share is calculated using our weighted-average outstanding common shares including the dilutive effect of stock awards as determined under the treasury stock method. In periods when we have a net loss, stock awards are excluded from our calculation of earnings per share as their inclusion would have an antidilutive effect. The following table shows the calculation of diluted shares (in millions):
````

**#2 `AMZN_FY2024_2024-12-31:208`** (gold #1, gold #3)

````text
Item 8. Financial Statements and Supplementary Data > Earnings Per Share
Basic earnings per share is calculated using our weighted-average outstanding common shares. Diluted earnings per share is calculated using our weighted-average outstanding common shares including the dilutive effect of stock awards as determined under the treasury stock method. In periods when we have a net loss, stock awards are excluded from our calculation of earnings per share as their inclusion would have an antidilutive effect. The following table shows the calculation of diluted shares (in millions):
````

**#3 `AMZN_FY2018_2018-12-31:194`** (cited, gold #1, gold #2, gold #3, gold #4)

````text
Item 8. Financial Statements and Supplementary Data > Earnings per Share (table)
|  | Year Ended December 31, |  |  |
|---|---|---|---|
|  | 2016 | 2017 | 2018 |
| Shares used in computation of basic earnings per share | 474 | 480 | 487 |
| Total dilutive effect of outstanding stock awards | 10 | 13 | 13 |
| Shares used in computation of diluted earnings per share | 484 | 493 | 500 |
````

**#5 `AMZN_FY2024_2024-12-31:209`** (cited, gold #1, gold #2, gold #3, gold #4)

````text
Item 8. Financial Statements and Supplementary Data > Earnings Per Share (table)
|  | Year Ended December 31, |  |  |
|---|---|---|---|
|  | 2022 | 2023 | 2024 |
| Shares used in computation of basic earnings per share | 10,189 | 10,304 | 10,473 |
| Total dilutive effect of outstanding stock awards | — | 188 | 248 |
| Shares used in computation of diluted earnings per share | 10,189 | 10,492 | 10,721 |
````

</details>

RQ2 citation match (section level): `cited=[('AMZN', 'Item 8')] gold=[(None, 'Item 8')]`

**System C guardrail** (judge `gpt-5.4`): numerical claims 4, verified 3, ungrounded 1, uncited 0, derived 2; sentence verdicts: supported 0, partial 0, unsupported 0, unchecked 0.

- ungrounded numbers: 0.31

<details><summary>Guardrail sentence verdicts</summary>

| sentence | verdict | judge reason |
|---|---|---|
| In fiscal year 2018, the dilutive effect of outstanding stock awards was 13 on basic shares of 487, or about 2.67% [AMZN FY2018, Item 8, AMZN_FY2018_2018-12-31:194]. | None |  |
| In fiscal year 2024, the dilutive effect of outstanding stock awards was 248 on basic shares of 10,473, or about 2.37% [AMZN FY2024, Item 8, AMZN_FY2024_2024-12-31:209]. | None |  |
| Therefore, the dilutive effect as a percentage of basic shares decreased by about 0.31 percentage points from 2018 to 2024 [AMZN FY2018, Item 8, AMZN_FY2018_2018-12-31:194] [AMZN FY2024, Item 8, AMZN_FY2024_2024-12-31:209]. | None |  |

</details>

### System C v2 (agentic multi-hop + XBRL)

Model: `gpt-5.4`. Hops: 1. Chunks retrieved: 8, cited: 2.

**Generated answer**

> In fiscal year 2018, the total dilutive effect of outstanding stock awards was 13 million and the shares used in computation of basic earnings per share were 487 million, so the dilutive effect was approximately 2.67% of basic shares [AMZN FY2018, Item 8, AMZN_FY2018_2018-12-31:194].
>
> In fiscal year 2024, the total dilutive effect of outstanding stock awards was 248 million and the shares used in computation of basic earnings per share were 10,473 million, so the dilutive effect was approximately 2.37% of basic shares [AMZN FY2024, Item 8, AMZN_FY2024_2024-12-31:209].
>
> The dilutive effect therefore decreased by approximately 0.30 percentage points from 2018 to 2024 [AMZN FY2018, Item 8, AMZN_FY2018_2018-12-31:194] [AMZN FY2024, Item 8, AMZN_FY2024_2024-12-31:209].
>
> > [Guardrail Audit Warning]: Manual verification required; these numerical figures could not be matched in their cited chunks: 13, 487, 248, 0.30; 3 sentence(s) are not supported by their cited chunks.

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `F-AMZN-2018` | SEC XBRL Reported Financials (financials.csv) |  |  | fiscal_year,fiscal_year_end,Revenue,NetIncome,OperatingIncome,TotalAssets,TotalLiabilities,StockholdersEquity,CashAndEquivalents,OperatingCashFlow,EPSDiluted 2018,2018-12-31,232887000000,10073000000,12421000000,162648000… |
| 2 | `F-AMZN-2024` | SEC XBRL Reported Financials (financials.csv) |  |  | fiscal_year,fiscal_year_end,Revenue,NetIncome,OperatingIncome,TotalAssets,TotalLiabilities,StockholdersEquity,CashAndEquivalents,OperatingCashFlow,EPSDiluted 2024,2024-12-31,637959000000,59248000000,68593000000,624894000… |
| 3 | `AMZN_FY2018_2018-12-31:193` | Item 8 › Earnings per Share |  | #1, #3 | Basic earnings per share is calculated using our weighted-average outstanding common shares. Diluted earnings per share is calculated using our weighted-average outstanding common shares including the dilutive effect of … |
| 4 | `AMZN_FY2024_2024-12-31:208` | Item 8 › Earnings Per Share |  | #1, #3 | Basic earnings per share is calculated using our weighted-average outstanding common shares. Diluted earnings per share is calculated using our weighted-average outstanding common shares including the dilutive effect of … |
| 5 | `AMZN_FY2018_2018-12-31:194` | Item 8 › Earnings per Share | ✓ | #1, #2, #3, #4 | \| \| Year Ended December 31, \| \| \| \|---\|---\|---\|---\| \| \| 2016 \| 2017 \| 2018 \| \| Shares used in computation of basic earnings per share \| 474 \| 480 \| 487 \| \| Total dilutive effect of outstanding stock awards \| 10 \| 13 \| 13… |
| 6 | `AMZN_FY2024_2024-12-31:209` | Item 8 › Earnings Per Share | ✓ | #1, #2, #3, #4 | \| \| Year Ended December 31, \| \| \| \|---\|---\|---\|---\| \| \| 2022 \| 2023 \| 2024 \| \| Shares used in computation of basic earnings per share \| 10,189 \| 10,304 \| 10,473 \| \| Total dilutive effect of outstanding stock awards \| — \|… |
| 7 | `AMZN_FY2024_2024-12-31:118` | Item 7 › Overview |  |  | devices as well as other initiatives including the development of a satellite network for global broadband service and autonomous vehicles for ride-hailing services. We seek to efficiently manage shareholder dilution whi… |
| 8 | `AMZN_FY2018_2018-12-31:104` | Item 7 › Overview |  |  | We seek to efficiently manage shareholder dilution while maintaining the flexibility to issue shares for strategic purposes, such as financings, acquisitions, and aligning employee compensation with shareholders’ interes… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#3 `AMZN_FY2018_2018-12-31:193`** (gold #1, gold #3)

````text
Item 8. Financial Statements and Supplementary Data > Earnings per Share
Basic earnings per share is calculated using our weighted-average outstanding common shares. Diluted earnings per share is calculated using our weighted-average outstanding common shares including the dilutive effect of stock awards as determined under the treasury stock method. In periods when we have a net loss, stock awards are excluded from our calculation of earnings per share as their inclusion would have an antidilutive effect. The following table shows the calculation of diluted shares (in millions):
````

**#4 `AMZN_FY2024_2024-12-31:208`** (gold #1, gold #3)

````text
Item 8. Financial Statements and Supplementary Data > Earnings Per Share
Basic earnings per share is calculated using our weighted-average outstanding common shares. Diluted earnings per share is calculated using our weighted-average outstanding common shares including the dilutive effect of stock awards as determined under the treasury stock method. In periods when we have a net loss, stock awards are excluded from our calculation of earnings per share as their inclusion would have an antidilutive effect. The following table shows the calculation of diluted shares (in millions):
````

**#5 `AMZN_FY2018_2018-12-31:194`** (cited, gold #1, gold #2, gold #3, gold #4)

````text
Item 8. Financial Statements and Supplementary Data > Earnings per Share (table)
|  | Year Ended December 31, |  |  |
|---|---|---|---|
|  | 2016 | 2017 | 2018 |
| Shares used in computation of basic earnings per share | 474 | 480 | 487 |
| Total dilutive effect of outstanding stock awards | 10 | 13 | 13 |
| Shares used in computation of diluted earnings per share | 484 | 493 | 500 |
````

**#6 `AMZN_FY2024_2024-12-31:209`** (cited, gold #1, gold #2, gold #3, gold #4)

````text
Item 8. Financial Statements and Supplementary Data > Earnings Per Share (table)
|  | Year Ended December 31, |  |  |
|---|---|---|---|
|  | 2022 | 2023 | 2024 |
| Shares used in computation of basic earnings per share | 10,189 | 10,304 | 10,473 |
| Total dilutive effect of outstanding stock awards | — | 188 | 248 |
| Shares used in computation of diluted earnings per share | 10,189 | 10,492 | 10,721 |
````

</details>

RQ2 citation match (section level): `cited=[('AMZN', 'Item 8')] gold=[(None, 'Item 8')]`

**System C guardrail** (judge `gpt-5.4`): numerical claims 7, verified 3, ungrounded 4, uncited 0, derived 2; sentence verdicts: supported 0, partial 0, unsupported 0, unchecked 0.

- ungrounded numbers: 13, 487, 248, 0.30

<details><summary>Guardrail sentence verdicts</summary>

| sentence | verdict | judge reason |
|---|---|---|
| In fiscal year 2018, the total dilutive effect of outstanding stock awards was 13 million and the shares used in computation of basic earnings per share were 487 million, so the dilutive effect was approximately 2.67% of basic shares [AMZN FY2018, Item 8, AMZN_FY2018_2018-12-31:194]. | None |  |
| In fiscal year 2024, the total dilutive effect of outstanding stock awards was 248 million and the shares used in computation of basic earnings per share were 10,473 million, so the dilutive effect was approximately 2.37% of basic shares [AMZN FY2024, Item 8, AMZN_FY2024_2024-12-31:209]. | None |  |
| The dilutive effect therefore decreased by approximately 0.30 percentage points from 2018 to 2024 [AMZN FY2018, Item 8, AMZN_FY2018_2018-12-31:194] [AMZN FY2024, Item 8, AMZN_FY2024_2024-12-31:209]. | None |  |

</details>
