# gold-068: Cross-year table

[← all cases](../README.md) · company: Meta Platforms, Inc. (META) · fiscal year: 2018 · recipe `cross_year_table` · hop `multi` · answer type `numeric` · scope `cross_year` · RQ2 category `multi_company_comparison`

## Gold QA

**Question**

> What was the total increase in Meta Platforms, Inc.'s total revenue between fiscal year 2015 and fiscal year 2018?

**Gold answer**

> $37,910 million

**Program**: `subtract(55838, 17928)` → `37910.0`

**Gold numbers** (RQ2 numeric_accuracy targets): $37,910 million

**Gold evidence**

1. `META_FY2018_2018-12-31` · Item 8. Financial Statements and Supplementary Data › Revenue Recognition · table

   > | Total revenue | $55,838 | $40,653 | $27,638 |

2. `META_FY2015_2015-12-31` · Item 7. Management's Discussion and Analysis of Financial Condition and Results of Operations › Revenue · table

   > | Total revenue | $17,928 | $12,466 | $7,872 | 44% | 58% |

## Scorecard

| Metric | A (vanilla dense) | B (hybrid + rerank) | C v1 (adaptive multi-hop) | C v2 (agentic multi-hop + XBRL) |
|---|---|---|---|---|
| **Retrieval (RQ1)** | | | | |
| chunks retrieved | 10 | 5 | 6 | 8 |
| recall@5 | 0.00 | 0.00 | 1.00 | 0.50 |
| recall@all | 1.00 | 0.00 | 1.00 | 1.00 |
| complete@all | 1 | 0 | 1 | 1 |
| average precision (lexical) | 0.30 | 0.00 | 0.77 | 0.43 |
| gold evidence first rank | #1: 9, #2: 6 | #1: –, #2: – | #1: 4, #2: 1 | #1: 6, #2: 3 |
| **Answer (RQ3 string match)** | | | | |
| numeric_correct | ✓ | ✗ | ✓ | ✓ |
| keypoint_recall | – | – | – | – |
| **Answer & citations (RQ2)** | | | | |
| numeric_accuracy | 1.00 | 0.00 | 1.00 | 1.00 |
| citation precision | 1.00 | 1.00 | 1.00 | 1.00 |
| citation recall | 0.50 | 0.50 | 0.50 | 0.50 |
| citation F1 | 0.67 | 0.67 | 0.67 | 0.67 |
| has a citation | 1 | 1 | 1 | 1 |
| grounding error rate | – | – | 0.00 | 0.00 |
| **Cost (RQ3)** | | | | |
| retrieval hops | 1 | 1 | 1 | 1 |
| tokens | 1657 | 1392 | 4008 | 4744 |
| cost (USD) | 0.0003 | 0.0003 | 0.0143 | 0.0161 |
| latency (s) | 2.1 | 7.2 | 6.3 | 6.7 |

Definitions: [README › Metrics](../README.md#metrics). `–` = not applicable (e.g. no gold number, no citations, no guardrail).

## System outputs

### System A (vanilla dense)

Model: `gpt-5.4-2026-03-05`. Hops: 1. Chunks retrieved: 10, cited: 2.

**Generated answer**

> Meta’s total revenue increased from **$17.928 billion in 2015** to **$55.838 billion in 2018**, for a total increase of **$37.910 billion** [6][10].

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `META_FY2015_2015-12-31:1` | Washington, D.C. 20549 |  |  | __________________________ |
| 2 | `META_FY2015_2015-12-31:0` |  |  |  | 10-K 1 fb-12312015x10k.htm 10-K |
| 3 | `META_FY2018_2018-12-31:208` | Item 7 › Revenue |  |  | 2018 Compared to 2017. Revenue in 2018 increased $15.19 billion, or 37%, compared to 2017. The increase was mostly due to an increase in advertising revenue. The most important factor driving advertising revenue growth w… |
| 4 | `META_FY2018_2018-12-31:1` | Washington, D.C. 20549 |  |  | __________________________ |
| 5 | `META_FY2015_2015-12-31:215` | Item 7 › Cost of revenue |  |  | 2015 Compared to 2014. Cost of revenue in 2015 increased $714 million, or 33%, compared to 2014. The increase was primarily due to an increase in operational expenses related to our data centers and technical infrastruct… |
| 6 | `META_FY2015_2015-12-31:206` | Item 7 › Revenue | ✓ | #2 | \| \| Year Ended December 31, \| \| \| 2015 vs 2014 % Change \| 2014 vs 2013 % Change \| \|---\|---\|---\|---\|---\|---\| \| \| 2015 \| 2014 \| 2013 \| \| \| \| \| (in millions) \| \| \| \| \| \| Advertising \| $17,079 \| $11,492 \| $6,986 \| 49% \| 65% … |
| 7 | `META_FY2015_2015-12-31:299` | Item 8 › Revenue Recognition |  | #2 | \| \| Year Ended December 31, \| \| \| \|---\|---\|---\|---\| \| \| 2015 \| 2014 \| 2013 \| \| Advertising \| $17,079 \| $11,492 \| $6,986 \| \| Payments and other fees \| 849 \| 974 \| 886 \| \| Total revenue \| $17,928 \| $12,466 \| $7,872 \| |
| 8 | `META_FY2018_2018-12-31:178` | Item 7 › Financial results: |  |  | • Revenue was $55.84 billion, up 37% year-over-year, and ad revenue was $55.01 billion, up 38% year-over-year. • Total costs and expenses were $30.93 billion. • Income from operations was $24.91 billion. • Net income was… |
| 9 | `META_FY2018_2018-12-31:313` | Item 8 › Revenue Recognition |  | #1 | \| \| Year Ended December 31, \| \| \| \|---\|---\|---\|---\| \| \| 2018 \| 2017 (1) \| 2016 (1) \| \| Revenue: \| \| \| \| \| US & Canada(2) \| $25,727 \| $19,065 \| $13,432 \| \| Europe(3) \| 13,631 \| 10,126 \| 6,792 \| \| Asia-Pacific \| 11,733 \| 7… |
| 10 | `META_FY2018_2018-12-31:207` | Item 7 › Revenue | ✓ | #1 | \| \| Year Ended December 31, \| \| \| 2018 vs 2017 % Change \| 2017 vs 2016 % Change \| \|---\|---\|---\|---\|---\|---\| \| \| 2018 \| 2017 \| 2016 \| \| \| \| \| (in millions) \| \| \| \| \| \| Advertising \| $55,013 \| $39,942 \| $26,885 \| 38% \| 49%… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#6 `META_FY2015_2015-12-31:206`** (cited, gold #2)

````text
Item 7. Management's Discussion and Analysis of Financial Condition and Results of Operations > Revenue (table)
|  | Year Ended December 31, |  |  | 2015 vs 2014 % Change | 2014 vs 2013 % Change |
|---|---|---|---|---|---|
|  | 2015 | 2014 | 2013 |  |  |
|  | (in millions) |  |  |  |  |
| Advertising | $17,079 | $11,492 | $6,986 | 49% | 65% |
| Payments and other fees | 849 | 974 | 886 | (13)% | 10% |
| Total revenue | $17,928 | $12,466 | $7,872 | 44% | 58% |
````

**#7 `META_FY2015_2015-12-31:299`** (gold #2)

````text
Item 8. Financial Statements and Supplementary Data > Revenue Recognition (table)
|  | Year Ended December 31, |  |  |
|---|---|---|---|
|  | 2015 | 2014 | 2013 |
| Advertising | $17,079 | $11,492 | $6,986 |
| Payments and other fees | 849 | 974 | 886 |
| Total revenue | $17,928 | $12,466 | $7,872 |
````

**#9 `META_FY2018_2018-12-31:313`** (gold #1)

````text
Item 8. Financial Statements and Supplementary Data > Revenue Recognition (table)
|  | Year Ended December 31, |  |  |
|---|---|---|---|
|  | 2018 | 2017 (1) | 2016 (1) |
| Revenue: |  |  |  |
| US & Canada(2) | $25,727 | $19,065 | $13,432 |
| Europe(3) | 13,631 | 10,126 | 6,792 |
| Asia-Pacific | 11,733 | 7,921 | 5,037 |
| Rest of World(3) | 4,747 | 3,541 | 2,377 |
| Total revenue | $55,838 | $40,653 | $27,638 |
````

**#10 `META_FY2018_2018-12-31:207`** (cited, gold #1)

````text
Item 7. Management's Discussion and Analysis of Financial Condition and Results of Operations > Revenue (table)
|  | Year Ended December 31, |  |  | 2018 vs 2017 % Change | 2017 vs 2016 % Change |
|---|---|---|---|---|---|
|  | 2018 | 2017 | 2016 |  |  |
|  | (in millions) |  |  |  |  |
| Advertising | $55,013 | $39,942 | $26,885 | 38% | 49% |
| Payments and other fees | 825 | 711 | 753 | 16% | (6)% |
| Total revenue | $55,838 | $40,653 | $27,638 | 37% | 47% |
````

</details>

RQ2 citation match (section level): `cited=[('META', 'Item 7')] gold=[(None, 'Item 8'), (None, 'Item 7')]`

### System B (hybrid + rerank)

Model: `gpt-5.4-2026-03-05`. Hops: 1. Chunks retrieved: 5, cited: 2.

**Generated answer**

> Meta’s total revenue was **$55.84 billion** in fiscal year 2018 [4]. In fiscal year 2015, revenue **increased by $5.46 billion compared to 2014** [1], but the **total 2015 revenue amount itself is not provided** in the context. Therefore, the total increase in revenue between fiscal year 2015 and fiscal year 2018 **cannot be determined from the provided context** [1][4].

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `META_FY2015_2015-12-31:207` | Item 7 › Revenue | ✓ |  | 2015 Compared to 2014. Revenue in 2015 increased $5.46 billion, or 44% compared to 2014. The increase was primarily due to an increase in advertising revenue. The most important factor driving advertising revenue growth … |
| 2 | `META_FY2015_2015-12-31:215` | Item 7 › Cost of revenue |  |  | 2015 Compared to 2014. Cost of revenue in 2015 increased $714 million, or 33%, compared to 2014. The increase was primarily due to an increase in operational expenses related to our data centers and technical infrastruct… |
| 3 | `META_FY2018_2018-12-31:215` | Item 7 › Cost of revenue |  |  | 2018 Compared to 2017. Cost of revenue in 2018 increased $3.90 billion, or 72%, compared to 2017. The increase was mostly due to an increase in operational expenses related to our data centers and technical infrastructur… |
| 4 | `META_FY2018_2018-12-31:178` | Item 7 › Financial results: | ✓ |  | • Revenue was $55.84 billion, up 37% year-over-year, and ad revenue was $55.01 billion, up 38% year-over-year. • Total costs and expenses were $30.93 billion. • Income from operations was $24.91 billion. • Net income was… |
| 5 | `META_FY2018_2018-12-31:212` | Item 7 › Revenue |  |  | In 2017 compared to 2016, the average price per ad increased by 29%, as compared with approximately 5% in 2016, and the number of ads delivered increased by 15%, as compared with approximately 50% in 2016. The increase i… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#1 `META_FY2015_2015-12-31:207`** (cited)

````text
Item 7. Management's Discussion and Analysis of Financial Condition and Results of Operations > Revenue
2015 Compared to 2014. Revenue in 2015 increased $5.46 billion, or 44% compared to 2014. The increase was primarily due to an increase in advertising revenue. The most important factor driving advertising revenue growth was an increase in revenue from ads in News Feed on mobile devices. In 2015, we estimate that mobile advertising revenue represented approximately 77% of total advertising revenue, as compared with approximately 65% in 2014. Factors that influenced our mobile advertising revenue growth in 2015 included (i) an increase in demand for our ad inventory, in part driven by an increase in the number of marketers actively advertising on Facebook, (ii) an increase in mobile user growth and engagement, and (iii) an increase in the number and frequency of ads displayed in News Feed, as well as the quality, relevance, and performance of those ads.
````

**#4 `META_FY2018_2018-12-31:178`** (cited)

````text
Item 7. Management's Discussion and Analysis of Financial Condition and Results of Operations > Financial results:
• Revenue was $55.84 billion, up 37% year-over-year, and ad revenue was $55.01 billion, up 38% year-over-year. • Total costs and expenses were $30.93 billion. • Income from operations was $24.91 billion. • Net income was $22.11 billion with diluted earnings per share of $7.57. • Capital expenditures were $13.92 billion. • Effective tax rate was 13%. • Cash and cash equivalents, and marketable securities were $41.11 billion as of December 31, 2018. • Headcount was 35,587 as of December 31, 2018, an increase of 42% year-over-year. In 2018, we continued to focus on our main revenue growth priorities: (i) helping marketers use our products to connect with consumers where they are and (ii) making our ads more relevant and effective.
````

</details>

RQ2 citation match (section level): `cited=[('META', 'Item 7')] gold=[(None, 'Item 8'), (None, 'Item 7')]`

### System C v1 (adaptive multi-hop)

Model: `gpt-5.4`. Hops: 1. Chunks retrieved: 6, cited: 2.

**Generated answer**

> Meta Platforms, Inc.'s total revenue increased from $17,928 million in fiscal year 2015 to $55,838 million in fiscal year 2018, an increase of $37,910 million [META FY2015, Item 8, META_FY2015_2015-12-31:299] [META FY2018, Item 8, META_FY2018_2018-12-31:311].

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `META_FY2015_2015-12-31:299` | Item 8 › Revenue Recognition | ✓ | #2 | \| \| Year Ended December 31, \| \| \| \|---\|---\|---\|---\| \| \| 2015 \| 2014 \| 2013 \| \| Advertising \| $17,079 \| $11,492 \| $6,986 \| \| Payments and other fees \| 849 \| 974 \| 886 \| \| Total revenue \| $17,928 \| $12,466 \| $7,872 \| |
| 2 | `META_FY2015_2015-12-31:213` | Item 7 › Revenue |  |  | The general strengthening of the U.S. dollar relative to certain foreign currencies (primarily the Euro) from the fourth quarter of and full year 2014 to the same periods in 2015 had an unfavorable impact on our revenue.… |
| 3 | `META_FY2015_2015-12-31:206` | Item 7 › Revenue |  | #2 | \| \| Year Ended December 31, \| \| \| 2015 vs 2014 % Change \| 2014 vs 2013 % Change \| \|---\|---\|---\|---\|---\|---\| \| \| 2015 \| 2014 \| 2013 \| \| \| \| \| (in millions) \| \| \| \| \| \| Advertising \| $17,079 \| $11,492 \| $6,986 \| 49% \| 65% … |
| 4 | `META_FY2018_2018-12-31:311` | Item 8 › Revenue Recognition | ✓ | #1 | \| \| Year Ended December 31, \| \| \| \|---\|---\|---\|---\| \| \| 2018 \| 2017 (1) \| 2016 (1) \| \| Advertising \| $55,013 \| $39,942 \| $26,885 \| \| Payments and other fees \| 825 \| 711 \| 753 \| \| Total revenue \| $55,838 \| $40,653 \| $27,6… |
| 5 | `META_FY2018_2018-12-31:213` | Item 7 › Revenue |  |  | The general weakening of the U.S. dollar relative to certain foreign currencies in the full year 2018 compared to the same period in 2017, and in the full year 2017 compared to the same period in 2016, had a favorable im… |
| 6 | `META_FY2015_2015-12-31:398` | Item 8 › Share-based Compensation Plans |  | #2 | \| \| Year Ended December 31, \| \| \| \|---\|---\|---\|---\| \| \| 2015 \| 2014 \| 2013 \| \| Revenue: \| \| \| \| \| United States \| $8,513 \| $5,649 \| $3,613 \| \| Rest of the world(1) \| 9,415 \| 6,817 \| 4,259 \| \| Total revenue \| $17,928 \| $1… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#1 `META_FY2015_2015-12-31:299`** (cited, gold #2)

````text
Item 8. Financial Statements and Supplementary Data > Revenue Recognition (table)
|  | Year Ended December 31, |  |  |
|---|---|---|---|
|  | 2015 | 2014 | 2013 |
| Advertising | $17,079 | $11,492 | $6,986 |
| Payments and other fees | 849 | 974 | 886 |
| Total revenue | $17,928 | $12,466 | $7,872 |
````

**#3 `META_FY2015_2015-12-31:206`** (gold #2)

````text
Item 7. Management's Discussion and Analysis of Financial Condition and Results of Operations > Revenue (table)
|  | Year Ended December 31, |  |  | 2015 vs 2014 % Change | 2014 vs 2013 % Change |
|---|---|---|---|---|---|
|  | 2015 | 2014 | 2013 |  |  |
|  | (in millions) |  |  |  |  |
| Advertising | $17,079 | $11,492 | $6,986 | 49% | 65% |
| Payments and other fees | 849 | 974 | 886 | (13)% | 10% |
| Total revenue | $17,928 | $12,466 | $7,872 | 44% | 58% |
````

**#4 `META_FY2018_2018-12-31:311`** (cited, gold #1)

````text
Item 8. Financial Statements and Supplementary Data > Revenue Recognition (table)
|  | Year Ended December 31, |  |  |
|---|---|---|---|
|  | 2018 | 2017 (1) | 2016 (1) |
| Advertising | $55,013 | $39,942 | $26,885 |
| Payments and other fees | 825 | 711 | 753 |
| Total revenue | $55,838 | $40,653 | $27,638 |
````

**#6 `META_FY2015_2015-12-31:398`** (gold #2)

````text
Item 8. Financial Statements and Supplementary Data > Share-based Compensation Plans (table)
|  | Year Ended December 31, |  |  |
|---|---|---|---|
|  | 2015 | 2014 | 2013 |
| Revenue: |  |  |  |
| United States | $8,513 | $5,649 | $3,613 |
| Rest of the world(1) | 9,415 | 6,817 | 4,259 |
| Total revenue | $17,928 | $12,466 | $7,872 |
````

</details>

RQ2 citation match (section level): `cited=[('META', 'Item 8')] gold=[(None, 'Item 8'), (None, 'Item 7')]`

**System C guardrail** (judge `gpt-5.4`): numerical claims 3, verified 3, ungrounded 0, uncited 0, derived 1; sentence verdicts: supported 0, partial 0, unsupported 0, unchecked 0.


<details><summary>Guardrail sentence verdicts</summary>

| sentence | verdict | judge reason |
|---|---|---|
| Meta Platforms, Inc.'s total revenue increased from $17,928 million in fiscal year 2015 to $55,838 million in fiscal year 2018, an increase of $37,910 million [META FY2015, Item 8, META_FY2015_2015-12-31:299] [META FY2018, Item 8, META_FY2018_2018-12-31:311]. | None |  |

</details>

### System C v2 (agentic multi-hop + XBRL)

Model: `gpt-5.4`. Hops: 1. Chunks retrieved: 8, cited: 2.

**Generated answer**

> Meta Platforms, Inc.'s total revenue increased from $17,928 million in fiscal year 2015 to $55,838 million in fiscal year 2018, an increase of $37,910 million. [META FY2015, Item 8, META_FY2015_2015-12-31:299] [META FY2018, Item 8, META_FY2018_2018-12-31:311]

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `F-META-2015` | SEC XBRL Reported Financials (financials.csv) |  |  | fiscal_year,fiscal_year_end,Revenue,NetIncome,OperatingIncome,TotalAssets,TotalLiabilities,StockholdersEquity,CashAndEquivalents,OperatingCashFlow,EPSDiluted 2015,2015-12-31,17928000000,3688000000,6225000000,49407000000,… |
| 2 | `F-META-2018` | SEC XBRL Reported Financials (financials.csv) |  |  | fiscal_year,fiscal_year_end,Revenue,NetIncome,OperatingIncome,TotalAssets,TotalLiabilities,StockholdersEquity,CashAndEquivalents,OperatingCashFlow,EPSDiluted 2018,2018-12-31,55838000000,22112000000,24913000000,9733400000… |
| 3 | `META_FY2015_2015-12-31:299` | Item 8 › Revenue Recognition | ✓ | #2 | \| \| Year Ended December 31, \| \| \| \|---\|---\|---\|---\| \| \| 2015 \| 2014 \| 2013 \| \| Advertising \| $17,079 \| $11,492 \| $6,986 \| \| Payments and other fees \| 849 \| 974 \| 886 \| \| Total revenue \| $17,928 \| $12,466 \| $7,872 \| |
| 4 | `META_FY2015_2015-12-31:213` | Item 7 › Revenue |  |  | The general strengthening of the U.S. dollar relative to certain foreign currencies (primarily the Euro) from the fourth quarter of and full year 2014 to the same periods in 2015 had an unfavorable impact on our revenue.… |
| 5 | `META_FY2015_2015-12-31:206` | Item 7 › Revenue |  | #2 | \| \| Year Ended December 31, \| \| \| 2015 vs 2014 % Change \| 2014 vs 2013 % Change \| \|---\|---\|---\|---\|---\|---\| \| \| 2015 \| 2014 \| 2013 \| \| \| \| \| (in millions) \| \| \| \| \| \| Advertising \| $17,079 \| $11,492 \| $6,986 \| 49% \| 65% … |
| 6 | `META_FY2018_2018-12-31:311` | Item 8 › Revenue Recognition | ✓ | #1 | \| \| Year Ended December 31, \| \| \| \|---\|---\|---\|---\| \| \| 2018 \| 2017 (1) \| 2016 (1) \| \| Advertising \| $55,013 \| $39,942 \| $26,885 \| \| Payments and other fees \| 825 \| 711 \| 753 \| \| Total revenue \| $55,838 \| $40,653 \| $27,6… |
| 7 | `META_FY2018_2018-12-31:213` | Item 7 › Revenue |  |  | The general weakening of the U.S. dollar relative to certain foreign currencies in the full year 2018 compared to the same period in 2017, and in the full year 2017 compared to the same period in 2016, had a favorable im… |
| 8 | `META_FY2015_2015-12-31:398` | Item 8 › Share-based Compensation Plans |  | #2 | \| \| Year Ended December 31, \| \| \| \|---\|---\|---\|---\| \| \| 2015 \| 2014 \| 2013 \| \| Revenue: \| \| \| \| \| United States \| $8,513 \| $5,649 \| $3,613 \| \| Rest of the world(1) \| 9,415 \| 6,817 \| 4,259 \| \| Total revenue \| $17,928 \| $1… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#3 `META_FY2015_2015-12-31:299`** (cited, gold #2)

````text
Item 8. Financial Statements and Supplementary Data > Revenue Recognition (table)
|  | Year Ended December 31, |  |  |
|---|---|---|---|
|  | 2015 | 2014 | 2013 |
| Advertising | $17,079 | $11,492 | $6,986 |
| Payments and other fees | 849 | 974 | 886 |
| Total revenue | $17,928 | $12,466 | $7,872 |
````

**#5 `META_FY2015_2015-12-31:206`** (gold #2)

````text
Item 7. Management's Discussion and Analysis of Financial Condition and Results of Operations > Revenue (table)
|  | Year Ended December 31, |  |  | 2015 vs 2014 % Change | 2014 vs 2013 % Change |
|---|---|---|---|---|---|
|  | 2015 | 2014 | 2013 |  |  |
|  | (in millions) |  |  |  |  |
| Advertising | $17,079 | $11,492 | $6,986 | 49% | 65% |
| Payments and other fees | 849 | 974 | 886 | (13)% | 10% |
| Total revenue | $17,928 | $12,466 | $7,872 | 44% | 58% |
````

**#6 `META_FY2018_2018-12-31:311`** (cited, gold #1)

````text
Item 8. Financial Statements and Supplementary Data > Revenue Recognition (table)
|  | Year Ended December 31, |  |  |
|---|---|---|---|
|  | 2018 | 2017 (1) | 2016 (1) |
| Advertising | $55,013 | $39,942 | $26,885 |
| Payments and other fees | 825 | 711 | 753 |
| Total revenue | $55,838 | $40,653 | $27,638 |
````

**#8 `META_FY2015_2015-12-31:398`** (gold #2)

````text
Item 8. Financial Statements and Supplementary Data > Share-based Compensation Plans (table)
|  | Year Ended December 31, |  |  |
|---|---|---|---|
|  | 2015 | 2014 | 2013 |
| Revenue: |  |  |  |
| United States | $8,513 | $5,649 | $3,613 |
| Rest of the world(1) | 9,415 | 6,817 | 4,259 |
| Total revenue | $17,928 | $12,466 | $7,872 |
````

</details>

RQ2 citation match (section level): `cited=[('META', 'Item 8')] gold=[(None, 'Item 8'), (None, 'Item 7')]`

**System C guardrail** (judge `gpt-5.4`): numerical claims 3, verified 3, ungrounded 0, uncited 0, derived 1; sentence verdicts: supported 0, partial 0, unsupported 0, unchecked 0.


<details><summary>Guardrail sentence verdicts</summary>

| sentence | verdict | judge reason |
|---|---|---|
| Meta Platforms, Inc.'s total revenue increased from $17,928 million in fiscal year 2015 to $55,838 million in fiscal year 2018, an increase of $37,910 million. [META FY2015, Item 8, META_FY2015_2015-12-31:299] [META FY2018, Item 8, META_FY2018_2018-12-31:311] | None |  |

</details>
