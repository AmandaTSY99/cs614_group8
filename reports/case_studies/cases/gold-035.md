# gold-035: Table + text (one filing)

[← all cases](../README.md) · company: Apple Inc. (AAPL) · fiscal year: 2015 · recipe `table_text` · hop `multi` · answer type `mixed` · scope `single_doc` · RQ2 category `cross_section_multihop`

## Gold QA

**Question**

> For Apple Inc. in fiscal year 2015, calculate the percentage increase in segment operating income compared to fiscal year 2014, and identify the primary drivers of the cash generated from operating activities during 2015 as described in the Management's Discussion and Analysis.

**Gold answer**

> 34.79%. Apple's 2015 operating cash flow of $81.3 billion resulted from $53.4 billion of net income, $16.2 billion of non-cash adjustments to net income, and an $11.7 billion increase in the net change in operating assets and liabilities.

**Program**: `subtract(83850, 62209), divide(#0, 62209)` → `0.3478757093025125`

**Gold numbers** (RQ2 numeric_accuracy targets): 34.79%

**Key points** (RQ3 keypoint_recall targets)

1. Segment operating income rose about 34.79% (from $62,209 million to $83,850 million).
2. Net income of $53.4 billion was the main driver of operating cash flow.
3. Non-cash adjustments contributed $16.2 billion.
4. Changes in operating assets and liabilities contributed $11.7 billion.

**Gold evidence**

1. `AAPL_FY2015_2015-09-26` · Item 8. Financial Statements and Supplementary Data › Note 11 – Segment Information and Geographic Data · table

   > | Segment operating income | $83,850 | $62,209 | $56,525 |

2. `AAPL_FY2015_2015-09-26` · Item 7. Management’s Discussion and Analysis of Financial Condition and Results of Operations › Liquidity and Capital Resources · text

   > During 2015, cash generated from operating activities of $81.3 billion was a result of $53.4 billion of net income, non-cash adjustments to net income of $16.2 billion and an increase in the net change in operating assets and liabilities of $11.7 billion.

## Scorecard

| Metric | A (vanilla dense) | B (hybrid + rerank) | C v1 (adaptive multi-hop) | C v2 (agentic multi-hop + XBRL) |
|---|---|---|---|---|
| **Retrieval (RQ1)** | | | | |
| chunks retrieved | 10 | 5 | 17 | 16 |
| recall@5 | 0.00 | 0.50 | 0.50 | 0.50 |
| recall@all | 1.00 | 0.50 | 1.00 | 1.00 |
| complete@all | 1 | 0 | 1 | 1 |
| average precision (lexical) | 0.23 | 0.83 | 0.30 | 0.31 |
| gold evidence first rank | #1: 7, #2: 8 | #1: –, #2: 1 | #1: 2, #2: 12 | #1: 3, #2: 8 |
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
| retrieval hops | 1 | 1 | 3 | 3 |
| tokens | 2021 | 1299 | 14617 | 14252 |
| cost (USD) | 0.0004 | 0.0002 | 0.0529 | 0.0499 |
| latency (s) | 3.3 | 5.7 | 25.5 | 23.4 |

Definitions: [README › Metrics](../README.md#metrics). `–` = not applicable (e.g. no gold number, no citations, no guardrail).

## System outputs

### System A (vanilla dense)

Model: `gpt-5.4-2026-03-05`. Hops: 1. Chunks retrieved: 10, cited: 2.

**Generated answer**

> Apple’s segment operating income increased from **$62,209 million in 2014** to **$83,850 million in 2015** [7].
>
> Percentage increase:
> \[
> \frac{83{,}850 - 62{,}209}{62{,}209} \times 100 \approx 34.8\%
> \]
>
> So, the **segment operating income increased by approximately 34.8%** in fiscal 2015 versus fiscal 2014 [7].
>
> The primary drivers of **cash generated from operating activities in 2015** were:
> - **Net income of $53.4 billion**
> - **Non-cash adjustments to net income of $16.2 billion**
> - **An increase in the net change in operating assets and liabilities of $11.7 billion** [10].

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `AAPL_FY2015_2015-09-26:160` | Item 7 › Segment Operating Performance |  |  | \| \| 2015 \| Change \| 2014 \| Change \| 2013 \| \|---\|---\|---\|---\|---\|---\| \| Net sales \| $15,706 \| 3% \| $15,314 \| 11% \| $13,782 \| \| Percentage of total net sales \| 7% \| \| 8% \| \| 8% \| |
| 2 | `AAPL_FY2015_2015-09-26:162` | Item 7 › Segment Operating Performance |  |  | \| \| 2015 \| Change \| 2014 \| Change \| 2013 \| \|---\|---\|---\|---\|---\|---\| \| Net sales \| $15,093 \| 34% \| $11,248 \| (7)% \| $12,039 \| \| Percentage of total net sales \| 6% \| \| 6% \| \| 7% \| |
| 3 | `AAPL_FY2015_2015-09-26:158` | Item 7 › Segment Operating Performance |  |  | \| \| 2015 \| Change \| 2014 \| Change \| 2013 \| \|---\|---\|---\|---\|---\|---\| \| Net sales \| $58,715 \| 84% \| $31,853 \| 18% \| $27,016 \| \| Percentage of total net sales \| 25% \| \| 17% \| \| 16% \| |
| 4 | `AAPL_FY2015_2015-09-26:156` | Item 7 › Segment Operating Performance |  |  | \| \| 2015 \| Change \| 2014 \| Change \| 2013 \| \|---\|---\|---\|---\|---\|---\| \| Net sales \| $50,337 \| 14% \| $44,285 \| 8% \| $40,980 \| \| Percentage of total net sales \| 22% \| \| 24% \| \| 24% \| |
| 5 | `AAPL_FY2015_2015-09-26:154` | Item 7 › Segment Operating Performance |  |  | \| \| 2015 \| Change \| 2014 \| Change \| 2013 \| \|---\|---\|---\|---\|---\|---\| \| Net sales \| $93,864 \| 17% \| $80,095 \| 4% \| $77,093 \| \| Percentage of total net sales \| 40% \| \| 44% \| \| 45% \| |
| 6 | `AAPL_FY2015_2015-09-26:392` | Item 8 › Note 11 – Segment Information and Geographic Data |  |  | A reconciliation of the Company’s segment operating income to the Consolidated Statements of Operations for 2015, 2014 and 2013 is as follows (in millions): |
| 7 | `AAPL_FY2015_2015-09-26:393` | Item 8 › Note 11 – Segment Information and Geographic Data | ✓ | #1 | \| \| 2015 \| 2014 \| 2013 \| \|---\|---\|---\|---\| \| Segment operating income \| $83,850 \| $62,209 \| $56,525 \| \| Research and development expense \| (8,067) \| (6,041) \| (4,475) \| \| Other corporate expenses, net \| (4,553) \| (3,665)… |
| 8 | `AAPL_FY2015_2015-09-26:185` | Item 7 › Liquidity and Capital Resources |  | #2 | During 2014, cash generated from operating activities of $59.7 billion was a result of $39.5 billion of net income, non-cash adjustments to net income of $13.2 billion and an increase in net change in operating assets an… |
| 9 | `AAPL_FY2015_2015-09-26:140` | Item 7 › Overview and Highlights |  |  | \| \| 2015 \| Change \| 2014 \| Change \| 2013 \| \|---\|---\|---\|---\|---\|---\| \| Net Sales by Operating Segment: \| \| \| \| \| \| \| Americas \| $93,864 \| 17% \| $80,095 \| 4% \| $77,093 \| \| Europe \| 50,337 \| 14% \| 44,285 \| 8% \| 40,980 \| \| … |
| 10 | `AAPL_FY2015_2015-09-26:184` | Item 7 › Liquidity and Capital Resources | ✓ | #2 | During 2015, cash generated from operating activities of $81.3 billion was a result of $53.4 billion of net income, non-cash adjustments to net income of $16.2 billion and an increase in the net change in operating asset… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#7 `AAPL_FY2015_2015-09-26:393`** (cited, gold #1)

````text
Item 8. Financial Statements and Supplementary Data > Note 11 – Segment Information and Geographic Data (table)
|  | 2015 | 2014 | 2013 |
|---|---|---|---|
| Segment operating income | $83,850 | $62,209 | $56,525 |
| Research and development expense | (8,067) | (6,041) | (4,475) |
| Other corporate expenses, net | (4,553) | (3,665) | (3,051) |
| Total operating income | $71,230 | $52,503 | $48,999 |
````

**#8 `AAPL_FY2015_2015-09-26:185`** (gold #2)

````text
Item 7. Management’s Discussion and Analysis of Financial Condition and Results of Operations > Liquidity and Capital Resources
During 2014, cash generated from operating activities of $59.7 billion was a result of $39.5 billion of net income, non-cash adjustments to net income of $13.2 billion and an increase in net change in operating assets and liabilities of $7.0 billion. Cash used in investing activities of $22.6 billion during 2014 consisted primarily of cash used for purchases of marketable securities, net of sales and maturities, of $9.0 billion; cash used to acquire property, plant and equipment of $9.6 billion; and cash paid for business acquisitions, net of cash acquired, of $3.8 billion. Cash used in financing activities of $37.5 billion during 2014 consisted primarily of cash used to repurchase common stock of $45.0 billion and cash used to pay dividends and dividend equivalents of $11.1 billion, partially offset by net proceeds from the issuance of term debt and commercial paper of $12.0 billion and $6.3 billion, respectively. Apple Inc. | 2015 Form 10-K | 30 Capital Assets
````

**#10 `AAPL_FY2015_2015-09-26:184`** (cited, gold #2)

````text
Item 7. Management’s Discussion and Analysis of Financial Condition and Results of Operations > Liquidity and Capital Resources
During 2015, cash generated from operating activities of $81.3 billion was a result of $53.4 billion of net income, non-cash adjustments to net income of $16.2 billion and an increase in the net change in operating assets and liabilities of $11.7 billion. Cash used in investing activities of $56.3 billion during 2015 consisted primarily of cash used for purchases of marketable securities, net of sales and maturities, of $44.4 billion and cash used to acquire property, plant and equipment of $11.2 billion. Cash used in financing activities of $17.7 billion during 2015 consisted primarily of cash used to repurchase common stock of $35.3 billion and cash used to pay dividends and dividend equivalents of $11.6 billion, partially offset by net proceeds from the issuance of term debt of $27.1 billion.
````

</details>

RQ2 citation match (section level): `cited=[('AAPL', 'Item 8'), ('AAPL', 'Item 7')] gold=[(None, 'Item 8'), (None, 'Item 7')]`

### System B (hybrid + rerank)

Model: `gpt-5.4-2026-03-05`. Hops: 1. Chunks retrieved: 5, cited: 0.

**Generated answer**

> Not found in the provided context.

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `AAPL_FY2015_2015-09-26:185` | Item 7 › Liquidity and Capital Resources |  | #2 | During 2014, cash generated from operating activities of $59.7 billion was a result of $39.5 billion of net income, non-cash adjustments to net income of $13.2 billion and an increase in net change in operating assets an… |
| 2 | `AAPL_FY2015_2015-09-26:136` | Item 7 › Overview and Highlights |  |  | Net sales rose 28% or $50.9 billion during 2015 compared to 2014, driven by a 52% year-over-year increase in iPhone® net sales. iPhone net sales and unit sales in 2015 increased in all of the Company’s reportable operati… |
| 3 | `AAPL_FY2015_2015-09-26:184` | Item 7 › Liquidity and Capital Resources |  | #2 | During 2015, cash generated from operating activities of $81.3 billion was a result of $53.4 billion of net income, non-cash adjustments to net income of $16.2 billion and an increase in the net change in operating asset… |
| 4 | `AAPL_FY2015_2015-09-26:152` | Item 7 › Product Performance |  |  | The increase in net sales of Services during 2015 compared to 2014 was primarily due to growth from Internet Services and licensing. The App Store, included within Internet Services, generated strong year-over-year net s… |
| 5 | `AAPL_FY2015_2015-09-26:145` | Item 7 › Product Performance |  |  | The year-over-year growth in iPhone net sales and unit sales during 2015 primarily resulted from strong demand for iPhone 6 and 6 Plus during 2015. Overall average selling prices (“ASPs”) for iPhone increased by 11% duri… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#1 `AAPL_FY2015_2015-09-26:185`** (gold #2)

````text
Item 7. Management’s Discussion and Analysis of Financial Condition and Results of Operations > Liquidity and Capital Resources
During 2014, cash generated from operating activities of $59.7 billion was a result of $39.5 billion of net income, non-cash adjustments to net income of $13.2 billion and an increase in net change in operating assets and liabilities of $7.0 billion. Cash used in investing activities of $22.6 billion during 2014 consisted primarily of cash used for purchases of marketable securities, net of sales and maturities, of $9.0 billion; cash used to acquire property, plant and equipment of $9.6 billion; and cash paid for business acquisitions, net of cash acquired, of $3.8 billion. Cash used in financing activities of $37.5 billion during 2014 consisted primarily of cash used to repurchase common stock of $45.0 billion and cash used to pay dividends and dividend equivalents of $11.1 billion, partially offset by net proceeds from the issuance of term debt and commercial paper of $12.0 billion and $6.3 billion, respectively. Apple Inc. | 2015 Form 10-K | 30 Capital Assets
````

**#3 `AAPL_FY2015_2015-09-26:184`** (gold #2)

````text
Item 7. Management’s Discussion and Analysis of Financial Condition and Results of Operations > Liquidity and Capital Resources
During 2015, cash generated from operating activities of $81.3 billion was a result of $53.4 billion of net income, non-cash adjustments to net income of $16.2 billion and an increase in the net change in operating assets and liabilities of $11.7 billion. Cash used in investing activities of $56.3 billion during 2015 consisted primarily of cash used for purchases of marketable securities, net of sales and maturities, of $44.4 billion and cash used to acquire property, plant and equipment of $11.2 billion. Cash used in financing activities of $17.7 billion during 2015 consisted primarily of cash used to repurchase common stock of $35.3 billion and cash used to pay dividends and dividend equivalents of $11.6 billion, partially offset by net proceeds from the issuance of term debt of $27.1 billion.
````

</details>

RQ2 citation match (section level): `no citations`

### System C v1 (adaptive multi-hop)

Model: `gpt-5.4`. Hops: 3. Chunks retrieved: 17, cited: 2.

**Generated answer**

> Apple’s segment operating income increased from $62,209 million in 2014 to $83,850 million in 2015, an increase of approximately 34.8% (($83,850 - $62,209) / $62,209). [AAPL FY2015, Item 8, AAPL_FY2015_2015-09-26:393]
>
> During 2015, cash generated from operating activities was $81.3 billion, driven by $53.4 billion of net income, non-cash adjustments to net income of $16.2 billion, and an increase in the net change in operating assets and liabilities of $11.7 billion. [AAPL FY2015, Item 7, AAPL_FY2015_2015-09-26:184]

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `AAPL_FY2015_2015-09-26:392` | Item 8 › Note 11 – Segment Information and Geographic Data |  |  | A reconciliation of the Company’s segment operating income to the Consolidated Statements of Operations for 2015, 2014 and 2013 is as follows (in millions): |
| 2 | `AAPL_FY2015_2015-09-26:393` | Item 8 › Note 11 – Segment Information and Geographic Data | ✓ | #1 | \| \| 2015 \| 2014 \| 2013 \| \|---\|---\|---\|---\| \| Segment operating income \| $83,850 \| $62,209 \| $56,525 \| \| Research and development expense \| (8,067) \| (6,041) \| (4,475) \| \| Other corporate expenses, net \| (4,553) \| (3,665)… |
| 3 | `AAPL_FY2015_2015-09-26:390` | Item 8 › Note 11 – Segment Information and Geographic Data |  |  | The Company evaluates the performance of its reportable operating segments based on net sales and operating income. Net sales for geographic segments are generally based on the location of customers and sales through the… |
| 4 | `AAPL_FY2015_2015-09-26:391` | Item 8 › Note 11 – Segment Information and Geographic Data |  |  | \| \| 2015 \| 2014 \| 2013 \| \|---\|---\|---\|---\| \| Americas: \| \| \| \| \| Net sales \| $93,864 \| $80,095 \| $77,093 \| \| Operating income \| $31,186 \| $26,158 \| $24,829 \| \| Europe: \| \| \| \| \| Net sales \| $50,337 \| $44,285 \| $40,980 \| … |
| 5 | `AAPL_FY2015_2015-09-26:160` | Item 7 › Segment Operating Performance |  |  | \| \| 2015 \| Change \| 2014 \| Change \| 2013 \| \|---\|---\|---\|---\|---\|---\| \| Net sales \| $15,706 \| 3% \| $15,314 \| 11% \| $13,782 \| \| Percentage of total net sales \| 7% \| \| 8% \| \| 8% \| |
| 6 | `AAPL_FY2015_2015-09-26:156` | Item 7 › Segment Operating Performance |  |  | \| \| 2015 \| Change \| 2014 \| Change \| 2013 \| \|---\|---\|---\|---\|---\|---\| \| Net sales \| $50,337 \| 14% \| $44,285 \| 8% \| $40,980 \| \| Percentage of total net sales \| 22% \| \| 24% \| \| 24% \| |
| 7 | `AAPL_FY2015_2015-09-26:153` | Item 7 › Segment Operating Performance |  |  | The Company manages its business primarily on a geographic basis. The Company’s reportable operating segments consist of the Americas, Europe, Greater China, Japan and Rest of Asia Pacific. The Americas segment includes … |
| 8 | `AAPL_FY2015_2015-09-26:22` | Item 1 › Business Organization |  |  | The Company manages its business primarily on a geographic basis. In 2015, the Company changed its reportable operating segments as management began reporting business performance and making decisions primarily on a geog… |
| 9 | `AAPL_FY2015_2015-09-26:395` | Item 8 › Note 11 – Segment Information and Geographic Data |  |  | \| \| 2015 \| 2014 \| 2013 \| \|---\|---\|---\|---\| \| Net sales: \| \| \| \| \| U.S. \| $81,732 \| $68,909 \| $66,197 \| \| China (1) \| 56,547 \| 30,638 \| 25,946 \| \| Other countries \| 95,436 \| 83,248 \| 78,767 \| \| Total net sales \| $233,715 … |
| 10 | `AAPL_FY2015_2015-09-26:396` | Item 8 › Note 11 – Segment Information and Geographic Data |  |  | (1) China includes Hong Kong. Long-lived assets located in China consist primarily of product tooling and manufacturing process equipment and assets related to retail stores and related infrastructure. Apple Inc. \| 2015 … |
| 11 | `AAPL_FY2015_2015-09-26:389` | Item 8 › Note 11 – Segment Information and Geographic Data |  |  | The Company reports segment information based on the “management” approach. The management approach designates the internal reporting used by management for making decisions and assessing performance as the source of the… |
| 12 | `AAPL_FY2015_2015-09-26:185` | Item 7 › Liquidity and Capital Resources |  | #2 | During 2014, cash generated from operating activities of $59.7 billion was a result of $39.5 billion of net income, non-cash adjustments to net income of $13.2 billion and an increase in net change in operating assets an… |
| 13 | `AAPL_FY2015_2015-09-26:184` | Item 7 › Liquidity and Capital Resources | ✓ | #2 | During 2015, cash generated from operating activities of $81.3 billion was a result of $53.4 billion of net income, non-cash adjustments to net income of $16.2 billion and an increase in the net change in operating asset… |
| 14 | `AAPL_FY2015_2015-09-26:182` | Item 7 › Liquidity and Capital Resources |  |  | \| \| 2015 \| 2014 \| 2013 \| \|---\|---\|---\|---\| \| Cash, cash equivalents and marketable securities \| $205,666 \| $155,239 \| $146,761 \| \| Property, plant and equipment, net \| $22,471 \| $20,624 \| $16,597 \| \| Commercial paper \| $… |
| 15 | `AAPL_FY2015_2015-09-26:191` | Item 7 › Liquidity and Capital Resources |  |  | \| \| Dividends and Dividend Equivalents Paid \| Accelerated Share Repurchases \| Open Market Share Repurchases \| Taxes Related to Settlement of Equity Awards \| Total \| \|---\|---\|---\|---\|---\|---\| \| 2015 \| $11,561 \| $6,000 \| $… |
| 16 | `AAPL_FY2015_2015-09-26:329` | Item 8 › Note 5 – Income Taxes |  |  | \| \| 2015 \| 2014 \| \|---\|---\|---\| \| Deferred tax assets: \| \| \| \| Accrued liabilities and other reserves \| $4,205 \| $3,326 \| \| Basis of capital assets and investments \| 2,238 \| 898 \| \| Deferred revenue \| 1,941 \| 1,787 \| \| D… |
| 17 | `AAPL_FY2015_2015-09-26:238` | Item 8 › CONSOLIDATED BALANCE SHEETS |  |  | \| \| September 26, 2015 \| September 27, 2014 \| \|---\|---\|---\| \| ASSETS: \| \| \| \| Current assets: \| \| \| \| Cash and cash equivalents \| $21,120 \| $13,844 \| \| Short-term marketable securities \| 20,481 \| 11,233 \| \| Accounts rece… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#2 `AAPL_FY2015_2015-09-26:393`** (cited, gold #1)

````text
Item 8. Financial Statements and Supplementary Data > Note 11 – Segment Information and Geographic Data (table)
|  | 2015 | 2014 | 2013 |
|---|---|---|---|
| Segment operating income | $83,850 | $62,209 | $56,525 |
| Research and development expense | (8,067) | (6,041) | (4,475) |
| Other corporate expenses, net | (4,553) | (3,665) | (3,051) |
| Total operating income | $71,230 | $52,503 | $48,999 |
````

**#12 `AAPL_FY2015_2015-09-26:185`** (gold #2)

````text
Item 7. Management’s Discussion and Analysis of Financial Condition and Results of Operations > Liquidity and Capital Resources
During 2014, cash generated from operating activities of $59.7 billion was a result of $39.5 billion of net income, non-cash adjustments to net income of $13.2 billion and an increase in net change in operating assets and liabilities of $7.0 billion. Cash used in investing activities of $22.6 billion during 2014 consisted primarily of cash used for purchases of marketable securities, net of sales and maturities, of $9.0 billion; cash used to acquire property, plant and equipment of $9.6 billion; and cash paid for business acquisitions, net of cash acquired, of $3.8 billion. Cash used in financing activities of $37.5 billion during 2014 consisted primarily of cash used to repurchase common stock of $45.0 billion and cash used to pay dividends and dividend equivalents of $11.1 billion, partially offset by net proceeds from the issuance of term debt and commercial paper of $12.0 billion and $6.3 billion, respectively. Apple Inc. | 2015 Form 10-K | 30 Capital Assets
````

**#13 `AAPL_FY2015_2015-09-26:184`** (cited, gold #2)

````text
Item 7. Management’s Discussion and Analysis of Financial Condition and Results of Operations > Liquidity and Capital Resources
During 2015, cash generated from operating activities of $81.3 billion was a result of $53.4 billion of net income, non-cash adjustments to net income of $16.2 billion and an increase in the net change in operating assets and liabilities of $11.7 billion. Cash used in investing activities of $56.3 billion during 2015 consisted primarily of cash used for purchases of marketable securities, net of sales and maturities, of $44.4 billion and cash used to acquire property, plant and equipment of $11.2 billion. Cash used in financing activities of $17.7 billion during 2015 consisted primarily of cash used to repurchase common stock of $35.3 billion and cash used to pay dividends and dividend equivalents of $11.6 billion, partially offset by net proceeds from the issuance of term debt of $27.1 billion.
````

</details>

RQ2 citation match (section level): `cited=[('AAPL', 'Item 8'), ('AAPL', 'Item 7')] gold=[(None, 'Item 8'), (None, 'Item 7')]`

**System C guardrail** (judge `gpt-5.4`): numerical claims 10, verified 10, ungrounded 0, uncited 0, derived 1; sentence verdicts: supported 0, partial 0, unsupported 0, unchecked 0.


<details><summary>Guardrail sentence verdicts</summary>

| sentence | verdict | judge reason |
|---|---|---|
| Apple’s segment operating income increased from $62,209 million in 2014 to $83,850 million in 2015, an increase of approximately 34.8% (($83,850 - $62,209) / $62,209). [AAPL FY2015, Item 8, AAPL_FY2015_2015-09-26:393] | None |  |
| During 2015, cash generated from operating activities was $81.3 billion, driven by $53.4 billion of net income, non-cash adjustments to net income of $16.2 billion, and an increase in the net change in operating assets and liabilities of $11.7 billion. [AAPL FY2015, Item 7, AAPL_FY2015_2015-09-26:184] | None |  |

</details>

### System C v2 (agentic multi-hop + XBRL)

Model: `gpt-5.4`. Hops: 3. Chunks retrieved: 16, cited: 2.

**Generated answer**

> Apple’s segment operating income increased from $62,209 million in 2014 to $83,850 million in 2015, an increase of approximately 34.8% (($83,850 - $62,209) / $62,209) [AAPL FY2015, Item 8, AAPL_FY2015_2015-09-26:393].  
>
> During 2015, cash generated from operating activities of $81.3 billion was a result of $53.4 billion of net income, non-cash adjustments to net income of $16.2 billion, and an increase in the net change in operating assets and liabilities of $11.7 billion [AAPL FY2015, Item 7, AAPL_FY2015_2015-09-26:184].

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `F-AAPL-2015` | SEC XBRL Reported Financials (financials.csv) |  |  | fiscal_year,fiscal_year_end,Revenue,NetIncome,OperatingIncome,TotalAssets,TotalLiabilities,StockholdersEquity,CashAndEquivalents,OperatingCashFlow,EPSDiluted 2015,2015-09-26,233715000000,53394000000,71230000000,290479000… |
| 2 | `AAPL_FY2015_2015-09-26:392` | Item 8 › Note 11 – Segment Information and Geographic Data |  |  | A reconciliation of the Company’s segment operating income to the Consolidated Statements of Operations for 2015, 2014 and 2013 is as follows (in millions): |
| 3 | `AAPL_FY2015_2015-09-26:393` | Item 8 › Note 11 – Segment Information and Geographic Data | ✓ | #1 | \| \| 2015 \| 2014 \| 2013 \| \|---\|---\|---\|---\| \| Segment operating income \| $83,850 \| $62,209 \| $56,525 \| \| Research and development expense \| (8,067) \| (6,041) \| (4,475) \| \| Other corporate expenses, net \| (4,553) \| (3,665)… |
| 4 | `AAPL_FY2015_2015-09-26:390` | Item 8 › Note 11 – Segment Information and Geographic Data |  |  | The Company evaluates the performance of its reportable operating segments based on net sales and operating income. Net sales for geographic segments are generally based on the location of customers and sales through the… |
| 5 | `AAPL_FY2015_2015-09-26:160` | Item 7 › Segment Operating Performance |  |  | \| \| 2015 \| Change \| 2014 \| Change \| 2013 \| \|---\|---\|---\|---\|---\|---\| \| Net sales \| $15,706 \| 3% \| $15,314 \| 11% \| $13,782 \| \| Percentage of total net sales \| 7% \| \| 8% \| \| 8% \| |
| 6 | `AAPL_FY2015_2015-09-26:391` | Item 8 › Note 11 – Segment Information and Geographic Data |  |  | \| \| 2015 \| 2014 \| 2013 \| \|---\|---\|---\|---\| \| Americas: \| \| \| \| \| Net sales \| $93,864 \| $80,095 \| $77,093 \| \| Operating income \| $31,186 \| $26,158 \| $24,829 \| \| Europe: \| \| \| \| \| Net sales \| $50,337 \| $44,285 \| $40,980 \| … |
| 7 | `AAPL_FY2015_2015-09-26:156` | Item 7 › Segment Operating Performance |  |  | \| \| 2015 \| Change \| 2014 \| Change \| 2013 \| \|---\|---\|---\|---\|---\|---\| \| Net sales \| $50,337 \| 14% \| $44,285 \| 8% \| $40,980 \| \| Percentage of total net sales \| 22% \| \| 24% \| \| 24% \| |
| 8 | `AAPL_FY2015_2015-09-26:184` | Item 7 › Liquidity and Capital Resources | ✓ | #2 | During 2015, cash generated from operating activities of $81.3 billion was a result of $53.4 billion of net income, non-cash adjustments to net income of $16.2 billion and an increase in the net change in operating asset… |
| 9 | `AAPL_FY2015_2015-09-26:185` | Item 7 › Liquidity and Capital Resources |  | #2 | During 2014, cash generated from operating activities of $59.7 billion was a result of $39.5 billion of net income, non-cash adjustments to net income of $13.2 billion and an increase in net change in operating assets an… |
| 10 | `AAPL_FY2015_2015-09-26:182` | Item 7 › Liquidity and Capital Resources |  |  | \| \| 2015 \| 2014 \| 2013 \| \|---\|---\|---\|---\| \| Cash, cash equivalents and marketable securities \| $205,666 \| $155,239 \| $146,761 \| \| Property, plant and equipment, net \| $22,471 \| $20,624 \| $16,597 \| \| Commercial paper \| $… |
| 11 | `AAPL_FY2015_2015-09-26:247` | Item 8 › CONSOLIDATED STATEMENTS OF CASH FLOWS |  |  | \| \| Years ended \| \| \| \|---\|---\|---\|---\| \| \| September 26, 2015 \| September 27, 2014 \| September 28, 2013 \| \| Cash and cash equivalents, beginning of the year \| $13,844 \| $14,259 \| $10,746 \| \| Operating activities: \| \| \| … |
| 12 | `AAPL_FY2015_2015-09-26:248` | Item 8 › CONSOLIDATED STATEMENTS OF CASH FLOWS |  |  | \| \| Years ended \| \| \| \|---\|---\|---\|---\| \| \| September 26, 2015 \| September 27, 2014 \| September 28, 2013 \| \| Cash generated by operating activities \| 81,266 \| 59,713 \| 53,666 \| \| Investing activities: \| \| \| \| \| Purchases… |
| 13 | `AAPL_FY2015_2015-09-26:186` | Item 7 › Liquidity and Capital Resources |  |  | The Company’s capital expenditures were $11.2 billion during 2015. The Company anticipates utilizing approximately $15.0 billion for capital expenditures during 2016, which includes product tooling and manufacturing proc… |
| 14 | `AAPL_FY2015_2015-09-26:153` | Item 7 › Segment Operating Performance |  |  | The Company manages its business primarily on a geographic basis. The Company’s reportable operating segments consist of the Americas, Europe, Greater China, Japan and Rest of Asia Pacific. The Americas segment includes … |
| 15 | `AAPL_FY2015_2015-09-26:22` | Item 1 › Business Organization |  |  | The Company manages its business primarily on a geographic basis. In 2015, the Company changed its reportable operating segments as management began reporting business performance and making decisions primarily on a geog… |
| 16 | `AAPL_FY2015_2015-09-26:163` | Item 7 › Segment Operating Performance |  |  | The year-over-year increase in Rest of Asia Pacific net sales during 2015 primarily reflects strong growth in net sales and unit sales of iPhone, partially offset by the effect of weakness in foreign currencies relative … |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#3 `AAPL_FY2015_2015-09-26:393`** (cited, gold #1)

````text
Item 8. Financial Statements and Supplementary Data > Note 11 – Segment Information and Geographic Data (table)
|  | 2015 | 2014 | 2013 |
|---|---|---|---|
| Segment operating income | $83,850 | $62,209 | $56,525 |
| Research and development expense | (8,067) | (6,041) | (4,475) |
| Other corporate expenses, net | (4,553) | (3,665) | (3,051) |
| Total operating income | $71,230 | $52,503 | $48,999 |
````

**#8 `AAPL_FY2015_2015-09-26:184`** (cited, gold #2)

````text
Item 7. Management’s Discussion and Analysis of Financial Condition and Results of Operations > Liquidity and Capital Resources
During 2015, cash generated from operating activities of $81.3 billion was a result of $53.4 billion of net income, non-cash adjustments to net income of $16.2 billion and an increase in the net change in operating assets and liabilities of $11.7 billion. Cash used in investing activities of $56.3 billion during 2015 consisted primarily of cash used for purchases of marketable securities, net of sales and maturities, of $44.4 billion and cash used to acquire property, plant and equipment of $11.2 billion. Cash used in financing activities of $17.7 billion during 2015 consisted primarily of cash used to repurchase common stock of $35.3 billion and cash used to pay dividends and dividend equivalents of $11.6 billion, partially offset by net proceeds from the issuance of term debt of $27.1 billion.
````

**#9 `AAPL_FY2015_2015-09-26:185`** (gold #2)

````text
Item 7. Management’s Discussion and Analysis of Financial Condition and Results of Operations > Liquidity and Capital Resources
During 2014, cash generated from operating activities of $59.7 billion was a result of $39.5 billion of net income, non-cash adjustments to net income of $13.2 billion and an increase in net change in operating assets and liabilities of $7.0 billion. Cash used in investing activities of $22.6 billion during 2014 consisted primarily of cash used for purchases of marketable securities, net of sales and maturities, of $9.0 billion; cash used to acquire property, plant and equipment of $9.6 billion; and cash paid for business acquisitions, net of cash acquired, of $3.8 billion. Cash used in financing activities of $37.5 billion during 2014 consisted primarily of cash used to repurchase common stock of $45.0 billion and cash used to pay dividends and dividend equivalents of $11.1 billion, partially offset by net proceeds from the issuance of term debt and commercial paper of $12.0 billion and $6.3 billion, respectively. Apple Inc. | 2015 Form 10-K | 30 Capital Assets
````

</details>

RQ2 citation match (section level): `cited=[('AAPL', 'Item 8'), ('AAPL', 'Item 7')] gold=[(None, 'Item 8'), (None, 'Item 7')]`

**System C guardrail** (judge `gpt-5.4`): numerical claims 10, verified 10, ungrounded 0, uncited 0, derived 1; sentence verdicts: supported 0, partial 0, unsupported 0, unchecked 0.


<details><summary>Guardrail sentence verdicts</summary>

| sentence | verdict | judge reason |
|---|---|---|
| Apple’s segment operating income increased from $62,209 million in 2014 to $83,850 million in 2015, an increase of approximately 34.8% (($83,850 - $62,209) / $62,209) [AAPL FY2015, Item 8, AAPL_FY2015_2015-09-26:393]. | None |  |
| During 2015, cash generated from operating activities of $81.3 billion was a result of $53.4 billion of net income, non-cash adjustments to net income of $16.2 billion, and an increase in the net change in operating assets and liabilities of $11.7 billion [AAPL FY2015, Item 7, AAPL_FY2015_2015-09-26:184]. | None |  |

</details>
