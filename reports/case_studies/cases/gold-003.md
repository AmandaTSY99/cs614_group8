# gold-003: Single-hop table

[← all cases](../README.md) · company: MICROSOFT CORP (MSFT) · fiscal year: 2016 · recipe `table` · hop `single` · answer type `numeric` · scope `single_doc` · RQ2 category `quantitative_tabular`

## Gold QA

**Question**

> What was the percentage decrease in Microsoft's long-lived assets held in Finland from fiscal year 2014 to fiscal year 2016?

**Gold answer**

> -96.05%

**Program**: `subtract(389, 9840), divide(#0, 9840), multiply(#1, 100)` → `-96.04674796747967`

**Gold numbers** (RQ2 numeric_accuracy targets): -96.05%

**Gold evidence**

1. `MSFT_FY2016_2016-06-30` · Item 8 › PART II · table

   > Finland | 389 | 1,757 | 9,840 |

2. `MSFT_FY2016_2016-06-30` · Item 8 › PART II · table

   > June 30, | 2016 | 2015 | 2014 |

## Scorecard

| Metric | A (vanilla dense) | B (hybrid + rerank) | C v1 (adaptive multi-hop) | C v2 (agentic multi-hop + XBRL) |
|---|---|---|---|---|
| **Retrieval (RQ1)** | | | | |
| chunks retrieved | 10 | 5 | 10 | 7 |
| recall@5 | 0.00 | 0.00 | 0.50 | 0.00 |
| recall@all | 0.00 | 0.00 | 1.00 | 0.50 |
| complete@all | 0 | 0 | 1 | 0 |
| average precision (lexical) | 0.00 | 0.00 | 0.26 | 0.17 |
| gold evidence first rank | #1: –, #2: – | #1: –, #2: – | #1: 8, #2: 5 | #1: –, #2: 6 |
| **Answer (RQ3 string match)** | | | | |
| numeric_correct | ✗ | ✗ | ✓ | ✗ |
| keypoint_recall | – | – | – | – |
| **Answer & citations (RQ2)** | | | | |
| numeric_accuracy | 0.00 | 0.00 | 0.00 | 0.00 |
| citation precision | – | – | 1.00 | – |
| citation recall | – | – | 1.00 | – |
| citation F1 | – | – | 1.00 | – |
| has a citation | 0 | 0 | 1 | 0 |
| grounding error rate | – | – | 0.00 | 0.00 |
| **Cost (RQ3)** | | | | |
| retrieval hops | 1 | 1 | 2 | 1 |
| tokens | 2145 | 1362 | 8385 | 9314 |
| cost (USD) | 0.0003 | 0.0002 | 0.0298 | 0.0302 |
| latency (s) | 1.1 | 6.2 | 13.5 | 10.8 |

Definitions: [README › Metrics](../README.md#metrics). `–` = not applicable (e.g. no gold number, no citations, no guardrail).

## System outputs

### System A (vanilla dense)

Model: `gpt-5.4-2026-03-05`. Hops: 1. Chunks retrieved: 10, cited: 0.

**Generated answer**

> Not found in the provided context.

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `MSFT_FY2016_2016-06-30:480` | Item 8 › PART II |  |  | Our total commercial cloud revenue, which primarily comprises Office 365 commercial, Azure, Dynamics Online, and other cloud properties, was $9.5 billion, $5.8 billion, and $2.8 billion in fiscal years 2016, 2015, and 20… |
| 2 | `MSFT_FY2016_2016-06-30:196` | Item 7 › PART II |  |  | Dividends and interest income increased due to higher portfolio balances and slightly higher yields on fixed-income securities. Interest expense increased due to higher outstanding long-term debt. Net recognized gains on… |
| 3 | `MSFT_FY2016_2016-06-30:197` | Item 7 › PART II |  |  | Dividends and interest income decreased due to lower yields on fixed-income securities, offset in part by higher portfolio balances. Interest expense increased due to higher outstanding long-term debt. Net recognized gai… |
| 4 | `MSFT_FY2016_2016-06-30:411` | Item 8 › PART II |  |  | \| (In millions) \| \| \| \|---\|---\|---\| \| Other long-term assets (a) \| $219 \| $228 \| \| Long-term deferred income tax liabilities (a) \| (1,476) \| (1,295) \| \| Net deferred income tax assets (liabilities) (a) \| $(1,257) \| $(1,0… |
| 5 | `MSFT_FY2016_2016-06-30:198` | Item 7 › PART II |  |  | The decrease in our effective tax rate for fiscal year 2016 compared to fiscal year 2015 was primarily due to changes in the mix of our income before income taxes between the U.S. and foreign countries including the impa… |
| 6 | `MSFT_FY2016_2016-06-30:167` | Item 7 › Reportable Segments |  |  | Productivity and Business Processes operating income decreased $898 million or 7%, driven by lower gross margin. Gross margin decreased $970 million or 4%, primarily due to higher cost of revenue. Gross margin included a… |
| 7 | `MSFT_FY2016_2016-06-30:175` | Item 7 › PART II |  |  | Productivity and Business Processes operating income decreased $814 million or 6%, driven by lower gross margin, offset in part by a reduction in operating expenses. Gross margin decreased $1.0 billion or 4%, primarily d… |
| 8 | `MSFT_FY2016_2016-06-30:364` | Item 8 › Financial Assets and Liabilities Measured at Fair Value on a Nonrecurring Basis |  |  | During fiscal years 2016, 2015, and 2014, depreciation expense was $4.9 billion, $4.1 billion, and $3.4 billion, respectively. |
| 9 | `MSFT_FY2016_2016-06-30:305` | Item 8 › PART II |  |  | \| (In millions) \| June 30, 2015 \| \| \|---\|---\|---\| \| \| As adjusted \| As reported \| \| Balance sheets: \| \| \| \| Current deferred income tax assets \| $0 \| $1,915 \| \| Other long-term assets \| $3,117 \| $2,953 \| \| Other current … |
| 10 | `MSFT_FY2016_2016-06-30:164` | Item 7 › PART II |  |  | \| (In millions, except percentages) \| 2016 \| 2015 \| 2014 \| Percentage Change 2016 Versus 2015 \| Percentage Change 2015 Versus 2014 \| \|---\|---\|---\|---\|---\|---\| \| Revenue \| \| \| \| \| \| \| Productivity and Business Processes \|… |

RQ2 citation match (section level): `no citations`

### System B (hybrid + rerank)

Model: `gpt-5.4-2026-03-05`. Hops: 1. Chunks retrieved: 5, cited: 0.

**Generated answer**

> Not found in the provided context.

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `MSFT_FY2016_2016-06-30:480` | Item 8 › PART II |  |  | Our total commercial cloud revenue, which primarily comprises Office 365 commercial, Azure, Dynamics Online, and other cloud properties, was $9.5 billion, $5.8 billion, and $2.8 billion in fiscal years 2016, 2015, and 20… |
| 2 | `MSFT_FY2016_2016-06-30:178` | Item 7 › PART II |  |  | • Gaming revenue increased $463 million or 5%, mainly due to growth in Xbox Live and video games revenue, offset in part by a decrease in Xbox hardware revenue and third-party video game royalties. We sold 12.1 million X… |
| 3 | `MSFT_FY2016_2016-06-30:211` | Item 7 › Cash Flows |  |  | Fiscal year 2016 compared with fiscal year 2015 Cash flows from operations increased $3.7 billion to $33.3 billion during the fiscal year, mainly due to lower operating expenditures and a reduction in materials and produ… |
| 4 | `MSFT_FY2016_2016-06-30:197` | Item 7 › PART II |  |  | Dividends and interest income decreased due to lower yields on fixed-income securities, offset in part by higher portfolio balances. Interest expense increased due to higher outstanding long-term debt. Net recognized gai… |
| 5 | `MSFT_FY2016_2016-06-30:203` | Item 7 › PART II |  |  | We are subject to income tax in many jurisdictions outside the U.S. Our operations in certain jurisdictions remain subject to examination for tax years 1996 to 2016, some of which are currently under audit by local tax a… |

RQ2 citation match (section level): `no citations`

### System C v1 (adaptive multi-hop)

Model: `gpt-5.4`. Hops: 2. Chunks retrieved: 10, cited: 1.

**Generated answer**

> Microsoft’s long-lived assets held in Finland were $9,840 million in fiscal year 2014 and $389 million in fiscal year 2016 [MSFT FY2016, Item 8, MSFT_FY2016_2016-06-30:481].  
> The decrease was 96.0%, calculated as (($9,840 - $389) / $9,840) × 100 [MSFT FY2016, Item 8, MSFT_FY2016_2016-06-30:481].

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `MSFT_FY2016_2016-06-30:480` | Item 8 › PART II |  |  | Our total commercial cloud revenue, which primarily comprises Office 365 commercial, Azure, Dynamics Online, and other cloud properties, was $9.5 billion, $5.8 billion, and $2.8 billion in fiscal years 2016, 2015, and 20… |
| 2 | `MSFT_FY2016_2016-06-30:411` | Item 8 › PART II |  |  | \| (In millions) \| \| \| \|---\|---\|---\| \| Other long-term assets (a) \| $219 \| $228 \| \| Long-term deferred income tax liabilities (a) \| (1,476) \| (1,295) \| \| Net deferred income tax assets (liabilities) (a) \| $(1,257) \| $(1,0… |
| 3 | `MSFT_FY2016_2016-06-30:305` | Item 8 › PART II |  |  | \| (In millions) \| June 30, 2015 \| \| \|---\|---\|---\| \| \| As adjusted \| As reported \| \| Balance sheets: \| \| \| \| Current deferred income tax assets \| $0 \| $1,915 \| \| Other long-term assets \| $3,117 \| $2,953 \| \| Other current … |
| 4 | `MSFT_FY2016_2016-06-30:368` | Item 8 › Nokia’s Devices and Services Business |  |  | \| (In millions) \| \| \|---\|---\| \| Cash \| $1,506 \| \| Accounts receivable (a) \| 754 \| \| Inventories \| 544 \| \| Other current assets \| 936 \| \| Property and equipment \| 981 \| \| Intangible assets \| 4,509 \| \| Goodwill (b) \| 5,456… |
| 5 | `MSFT_FY2016_2016-06-30:254` | Item 8 › BALANCE SHEETS |  | #2 | \| (In millions) \| \| \| \|---\|---\|---\| \| June 30, \| 2016 \| 2015 \| \| Assets \| \| \| \| Current assets: \| \| \| \| Cash and cash equivalents \| $6,510 \| $5,595 \| \| Short-term investments (including securities loaned of $204 and $75)… |
| 6 | `MSFT_FY2016_2016-06-30:207` | Item 7 › Cash, Cash Equivalents, and Investments |  |  | Of the cash, cash equivalents, and short-term investments as of June 30, 2016, $108.9 billion was held by our foreign subsidiaries and would be subject to material repatriation tax effects. The amount of cash, cash equiv… |
| 7 | `MSFT_FY2016_2016-06-30:267` | Item 8 › Segment Information |  |  | In June 2015, we announced a change in organizational structure to align to our strategic direction as a productivity and platform company. During the first quarter of fiscal year 2016, our chief operating decision maker… |
| 8 | `MSFT_FY2016_2016-06-30:481` | Item 8 › PART II | ✓ | #1, #2 | \| (In millions) \| \| \| \| \|---\|---\|---\|---\| \| June 30, \| 2016 \| 2015 \| 2014 \| \| United States \| $22,819 \| $19,562 \| $17,653 \| \| Luxembourg \| 6,854 \| 6,879 \| 6,913 \| \| Finland \| 389 \| 1,757 \| 9,840 \| \| Other countries \| 9,8… |
| 9 | `MSFT_FY2016_2016-06-30:340` | Item 8 › Fair Values of Derivative Instruments |  | #2 | \| \| June 30, 2016 \| \| \| \| June 30, 2015 \| \| \| \| \|---\|---\|---\|---\|---\|---\|---\|---\|---\| \| \| Assets \| \| \| Liabilities \| Assets \| \| \| Liabilities \| \| (In millions) \| Short-term Investments \| Other Current Assets \| Equity and… |
| 10 | `MSFT_FY2016_2016-06-30:353` | Item 8 › Assets and Liabilities Measured at Fair Value on a Recurring Basis |  |  | \| (In millions) \| Level 1 \| Level 2 \| Level 3 \| Gross Fair Value \| Netting (a) \| Net Fair Value \| \| \|---\|---\|---\|---\|---\|---\|---\|---\| \| June 30, 2016 \| \| \| \| \| \| \| \| \| Assets \| \| \| \| \| \| \| \| \| Mutual funds \| $1,012 \| $0 … |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#5 `MSFT_FY2016_2016-06-30:254`** (gold #2)

````text
Item 8 > BALANCE SHEETS (table)
| (In millions) |  |  |
|---|---|---|
| June 30, | 2016 | 2015 |
| Assets |  |  |
| Current assets: |  |  |
| Cash and cash equivalents | $6,510 | $5,595 |
| Short-term investments (including securities loaned of $204 and $75) | 106,730 | 90,931 |
| Total cash, cash equivalents, and short-term investments | 113,240 | 96,526 |
| Accounts receivable, net of allowance for doubtful accounts of $426 and $335 | 18,277 | 17,908 |
| Inventories | 2,251 | 2,902 |
| Other | 5,892 | 5,461 |
| Total current assets | 139,660 | 122,797 |
| Property and equipment, net of accumulated depreciation of $19,800 and $17,606 | 18,356 | 14,731 |
| Equity and other investments | 10,431 | 12,053 |
| Goodwill | 17,872 | 16,939 |
| Intangible assets, net | 3,733 | 4,835 |
| Other long-term assets | 3,642 | 3,117 |
| Total assets | $193,694 | $174,472 |
| Liabilities and stockholders’ equity |  |  |
| Current liabilities: |  |  |
| Accounts payable | $6,898 | $6,591 |
| Short-term debt | 12,904 | 4,985 |
````

**#8 `MSFT_FY2016_2016-06-30:481`** (cited, gold #1, gold #2)

````text
Item 8 > PART II (table)
| (In millions) |  |  |  |
|---|---|---|---|
| June 30, | 2016 | 2015 | 2014 |
| United States | $22,819 | $19,562 | $17,653 |
| Luxembourg | 6,854 | 6,879 | 6,913 |
| Finland | 389 | 1,757 | 9,840 |
| Other countries | 9,899 | 8,307 | 5,713 |
| Total | $39,961 | $36,505 | $40,119 |
````

**#9 `MSFT_FY2016_2016-06-30:340`** (gold #2)

````text
Item 8 > Fair Values of Derivative Instruments (table)
|  | June 30, 2016 |  |  |  | June 30, 2015 |  |  |  |
|---|---|---|---|---|---|---|---|---|
|  | Assets |  |  | Liabilities | Assets |  |  | Liabilities |
| (In millions) | Short-term Investments | Other Current Assets | Equity and Other Investments | Other Current Liabilities | Short-term Investments | Other Current Assets | Equity and Other Investments | Other Current Liabilities |
| Non-designated Hedge Derivatives |  |  |  |  |  |  |  |  |
| Foreign exchange contracts | $33 | $156 | $0 | $(296) | $17 | $167 | $0 | $(79) |
| Equity contracts | 23 | 0 | 0 | (16) | 148 | 0 | 0 | (18) |
| Interest rate contracts | 10 | 0 | 0 | (25) | 7 | 0 | 0 | (12) |
| Credit contracts | 6 | 0 | 0 | (5) | 16 | 0 | 0 | (9) |
| Commodity contracts | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
````

</details>

RQ2 citation match (section level): `cited=[('MSFT', 'Item 8')] gold=[(None, 'Item 8')]`

**System C guardrail** (judge `gpt-5.4`): numerical claims 6, verified 6, ungrounded 0, uncited 0, derived 1; sentence verdicts: supported 0, partial 0, unsupported 0, unchecked 0.


<details><summary>Guardrail sentence verdicts</summary>

| sentence | verdict | judge reason |
|---|---|---|
| Microsoft’s long-lived assets held in Finland were $9,840 million in fiscal year 2014 and $389 million in fiscal year 2016 [MSFT FY2016, Item 8, MSFT_FY2016_2016-06-30:481]. | None |  |
| The decrease was 96.0%, calculated as (($9,840 - $389) / $9,840) × 100 [MSFT FY2016, Item 8, MSFT_FY2016_2016-06-30:481]. | None |  |

</details>

### System C v2 (agentic multi-hop + XBRL)

Model: `gpt-5.4`. Hops: 1. Chunks retrieved: 7, cited: 0.

**Generated answer**

> Microsoft’s long-lived assets held in Finland in fiscal years 2016 and 2014 are not disclosed in the provided evidence blocks, so the percentage decrease cannot be verified from this evidence.

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `F-MSFT-2016` | SEC XBRL Reported Financials (financials.csv) |  |  | fiscal_year,fiscal_year_end,Revenue,NetIncome,OperatingIncome,TotalAssets,TotalLiabilities,StockholdersEquity,CashAndEquivalents,OperatingCashFlow,EPSDiluted 2016,2016-06-30,85320000000,16798000000,20182000000,1936940000… |
| 2 | `MSFT_FY2016_2016-06-30:480` | Item 8 › PART II |  |  | Our total commercial cloud revenue, which primarily comprises Office 365 commercial, Azure, Dynamics Online, and other cloud properties, was $9.5 billion, $5.8 billion, and $2.8 billion in fiscal years 2016, 2015, and 20… |
| 3 | `MSFT_FY2016_2016-06-30:411` | Item 8 › PART II |  |  | \| (In millions) \| \| \| \|---\|---\|---\| \| Other long-term assets (a) \| $219 \| $228 \| \| Long-term deferred income tax liabilities (a) \| (1,476) \| (1,295) \| \| Net deferred income tax assets (liabilities) (a) \| $(1,257) \| $(1,0… |
| 4 | `MSFT_FY2016_2016-06-30:305` | Item 8 › PART II |  |  | \| (In millions) \| June 30, 2015 \| \| \|---\|---\|---\| \| \| As adjusted \| As reported \| \| Balance sheets: \| \| \| \| Current deferred income tax assets \| $0 \| $1,915 \| \| Other long-term assets \| $3,117 \| $2,953 \| \| Other current … |
| 5 | `MSFT_FY2016_2016-06-30:368` | Item 8 › Nokia’s Devices and Services Business |  |  | \| (In millions) \| \| \|---\|---\| \| Cash \| $1,506 \| \| Accounts receivable (a) \| 754 \| \| Inventories \| 544 \| \| Other current assets \| 936 \| \| Property and equipment \| 981 \| \| Intangible assets \| 4,509 \| \| Goodwill (b) \| 5,456… |
| 6 | `MSFT_FY2016_2016-06-30:254` | Item 8 › BALANCE SHEETS |  | #2 | \| (In millions) \| \| \| \|---\|---\|---\| \| June 30, \| 2016 \| 2015 \| \| Assets \| \| \| \| Current assets: \| \| \| \| Cash and cash equivalents \| $6,510 \| $5,595 \| \| Short-term investments (including securities loaned of $204 and $75)… |
| 7 | `MSFT_FY2016_2016-06-30:207` | Item 7 › Cash, Cash Equivalents, and Investments |  |  | Of the cash, cash equivalents, and short-term investments as of June 30, 2016, $108.9 billion was held by our foreign subsidiaries and would be subject to material repatriation tax effects. The amount of cash, cash equiv… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#6 `MSFT_FY2016_2016-06-30:254`** (gold #2)

````text
Item 8 > BALANCE SHEETS (table)
| (In millions) |  |  |
|---|---|---|
| June 30, | 2016 | 2015 |
| Assets |  |  |
| Current assets: |  |  |
| Cash and cash equivalents | $6,510 | $5,595 |
| Short-term investments (including securities loaned of $204 and $75) | 106,730 | 90,931 |
| Total cash, cash equivalents, and short-term investments | 113,240 | 96,526 |
| Accounts receivable, net of allowance for doubtful accounts of $426 and $335 | 18,277 | 17,908 |
| Inventories | 2,251 | 2,902 |
| Other | 5,892 | 5,461 |
| Total current assets | 139,660 | 122,797 |
| Property and equipment, net of accumulated depreciation of $19,800 and $17,606 | 18,356 | 14,731 |
| Equity and other investments | 10,431 | 12,053 |
| Goodwill | 17,872 | 16,939 |
| Intangible assets, net | 3,733 | 4,835 |
| Other long-term assets | 3,642 | 3,117 |
| Total assets | $193,694 | $174,472 |
| Liabilities and stockholders’ equity |  |  |
| Current liabilities: |  |  |
| Accounts payable | $6,898 | $6,591 |
| Short-term debt | 12,904 | 4,985 |
````

</details>

RQ2 citation match (section level): `no citations`

**System C guardrail** (judge `gpt-5.4`): numerical claims 0, verified 0, ungrounded 0, uncited 0, derived 0; sentence verdicts: supported 1, partial 0, unsupported 0, unchecked 0.


<details><summary>Guardrail sentence verdicts</summary>

| sentence | verdict | judge reason |
|---|---|---|
| Microsoft’s long-lived assets held in Finland in fiscal years 2016 and 2014 are not disclosed in the provided evidence blocks, so the percentage decrease cannot be verified from this evidence. | supported | The retrieved evidence does not disclose Microsoft long-lived assets held in Finland for fiscal 2016 or 2014, so the decrease cannot be verified from this evidence. |

</details>
