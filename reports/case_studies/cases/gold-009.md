# gold-009: Single-hop table

[← all cases](../README.md) · company: Apple Inc. (AAPL) · fiscal year: 2019 · recipe `table` · hop `single` · answer type `numeric` · scope `single_doc` · RQ2 category `quantitative_tabular`

## Gold QA

**Question**

> By what percentage did Apple's total shareholders' equity decrease from the fiscal year 2018 ending balance to the fiscal year 2019 ending balance?

**Gold answer**

> -15.55%

**Program**: `subtract(90488, 107147), divide(#0, 107147), multiply(#1, 100)` → `-15.547798818445688`

**Gold numbers** (RQ2 numeric_accuracy targets): -15.55%

**Gold evidence**

1. `AAPL_FY2019_2019-09-28` · Item 8. Financial Statements and Supplementary Data › CONSOLIDATED STATEMENTS OF SHAREHOLDERS’ EQUITY · table

   > | Total shareholders’ equity, ending balances | $90,488 | $107,147 | $134,047 |

## Scorecard

| Metric | A (vanilla dense) | B (hybrid + rerank) | C v1 (adaptive multi-hop) | C v2 (agentic multi-hop + XBRL) |
|---|---|---|---|---|
| **Retrieval (RQ1)** | | | | |
| chunks retrieved | 10 | 5 | 6 | 7 |
| recall@5 | 1.00 | 1.00 | 1.00 | 1.00 |
| recall@all | 1.00 | 1.00 | 1.00 | 1.00 |
| complete@all | 1 | 1 | 1 | 1 |
| average precision (lexical) | 1.00 | 0.58 | 1.00 | 0.58 |
| gold evidence first rank | #1: 1 | #1: 2 | #1: 1 | #1: 2 |
| **Answer (RQ3 string match)** | | | | |
| numeric_correct | ✓ | ✓ | ✓ | ✓ |
| keypoint_recall | – | – | – | – |
| **Answer & citations (RQ2)** | | | | |
| numeric_accuracy | 0.00 | 0.00 | 0.00 | 0.00 |
| citation precision | 1.00 | 1.00 | 1.00 | 1.00 |
| citation recall | 1.00 | 1.00 | 1.00 | 1.00 |
| citation F1 | 1.00 | 1.00 | 1.00 | 1.00 |
| has a citation | 1 | 1 | 1 | 1 |
| grounding error rate | – | – | 0.00 | 0.00 |
| **Cost (RQ3)** | | | | |
| retrieval hops | 1 | 1 | 1 | 1 |
| tokens | 2259 | 1712 | 5117 | 5374 |
| cost (USD) | 0.0004 | 0.0003 | 0.0174 | 0.0182 |
| latency (s) | 2.3 | 6.8 | 7.1 | 7.6 |

Definitions: [README › Metrics](../README.md#metrics). `–` = not applicable (e.g. no gold number, no citations, no guardrail).

## System outputs

### System A (vanilla dense)

Model: `gpt-5.4-2026-03-05`. Hops: 1. Chunks retrieved: 10, cited: 1.

**Generated answer**

> Apple’s total shareholders’ equity decreased from **$107,147 million** in fiscal 2018 to **$90,488 million** in fiscal 2019 [2].
>
> Percentage decrease:
>
> \[
> \frac{107{,}147 - 90{,}488}{107{,}147} \times 100 \approx 15.5\%
> \]
>
> So, Apple’s total shareholders’ equity **decreased by approximately 15.5%** from fiscal 2018 to fiscal 2019 [2].

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `AAPL_FY2019_2019-09-28:173` | Item 8 › CONSOLIDATED STATEMENTS OF SHAREHOLDERS’ EQUITY |  | #1 | \| \| Years ended \| \| \| \|---\|---\|---\|---\| \| \| September 28, 2019 \| September 29, 2018 \| September 30, 2017 \| \| Total shareholders’ equity, beginning balances \| $107,147 \| $134,047 \| $128,249 \| \| Common stock and additional… |
| 2 | `AAPL_FY2019_2019-09-28:174` | Item 8 › CONSOLIDATED STATEMENTS OF SHAREHOLDERS’ EQUITY | ✓ | #1 | \| \| Years ended \| \| \| \|---\|---\|---\|---\| \| \| September 28, 2019 \| September 29, 2018 \| September 30, 2017 \| \| Cumulative effects of changes in accounting principles \| 2,501 \| 278 \| — \| \| Ending balances \| 45,898 \| 70,400 … |
| 3 | `AAPL_FY2019_2019-09-28:106` | Item 7 › Fiscal 2019 Highlights |  |  | Total net sales decreased 2% or $5.4 billion during 2019 compared to 2018, driven by lower net sales of iPhone, partially offset by higher net sales of Wearables, Home and Accessories and Services in all geographic opera… |
| 4 | `AAPL_FY2019_2019-09-28:172` | Item 8 › CONSOLIDATED STATEMENTS OF SHAREHOLDERS’ EQUITY |  |  | (In millions, except per share amounts) |
| 5 | `AAPL_FY2019_2019-09-28:99` | Item 5 › Company Stock Performance |  |  | \| \| September 2014 \| September 2015 \| September 2016 \| September 2017 \| September 2018 \| September 2019 \| \|---\|---\|---\|---\|---\|---\|---\| \| Apple Inc. \| $100 \| $116 \| $116 \| $162 \| $240 \| $237 \| \| S&P 500 Index \| $100 \| $9… |
| 6 | `AAPL_FY2019_2019-09-28:96` | Item 5 › Purchases of Equity Securities by the Issuer and Affiliated Purchasers |  |  | \| Periods \| Total Number of Shares Purchased \| Average Price Paid Per Share \| Total Number of Shares Purchased as Part of Publicly Announced Plans or Programs \| Approximate Dollar Value of Shares That May Yet Be Purchase… |
| 7 | `AAPL_FY2019_2019-09-28:124` | Item 7 › Other Income/(Expense), Net |  |  | The year-over-year decrease in OI&E during 2019 was due primarily to lower interest income and higher interest expense, partially offset by the impact of foreign exchange–related items. The weighted-average interest rate… |
| 8 | `AAPL_FY2019_2019-09-28:115` | Item 7 › Gross Margin |  |  | Products and Services gross margin and gross margin percentage for 2019, 2018 and 2017 were as follows (dollars in millions): |
| 9 | `AAPL_FY2019_2019-09-28:170` | Item 8 › CONSOLIDATED BALANCE SHEETS |  |  | \| \| September 28, 2019 \| September 29, 2018 \| \|---\|---\|---\| \| Non-current liabilities: \| \| \| \| Term debt \| 91,807 \| 93,735 \| \| Other non-current liabilities \| 50,503 \| 48,914 \| \| Total non-current liabilities \| 142,310 \|… |
| 10 | `AAPL_FY2019_2019-09-28:269` | Item 8 › Shares of Common Stock |  |  | \| \| 2019 \| 2018 \| 2017 \| \|---\|---\|---\|---\| \| Common stock outstanding, beginning balances \| 4,754,986 \| 5,126,201 \| 5,336,166 \| \| Common stock repurchased \| (345,205) \| (405,549) \| (246,496) \| \| Common stock issued, net … |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#1 `AAPL_FY2019_2019-09-28:173`** (gold #1)

````text
Item 8. Financial Statements and Supplementary Data > CONSOLIDATED STATEMENTS OF SHAREHOLDERS’ EQUITY (table)
|  | Years ended |  |  |
|---|---|---|---|
|  | September 28, 2019 | September 29, 2018 | September 30, 2017 |
| Total shareholders’ equity, beginning balances | $107,147 | $134,047 | $128,249 |
| Common stock and additional paid-in capital: |  |  |  |
| Beginning balances | 40,201 | 35,867 | 31,251 |
| Common stock issued | 781 | 669 | 555 |
| Common stock withheld related to net share settlement of equity awards | (2,002) | (1,778) | (1,468) |
| Share-based compensation | 6,194 | 5,443 | 4,909 |
| Tax benefit from equity awards, including transfer pricing adjustments | — | — | 620 |
| Ending balances | 45,174 | 40,201 | 35,867 |
| Retained earnings: |  |  |  |
| Beginning balances | 70,400 | 98,330 | 96,364 |
| Net income | 55,256 | 59,531 | 48,351 |
| Dividends and dividend equivalents declared | (14,129) | (13,735) | (12,803) |
| Common stock withheld related to net share settlement of equity awards | (1,029) | (948) | (581) |
| Common stock repurchased | (67,101) | (73,056) | (33,001) |
````

**#2 `AAPL_FY2019_2019-09-28:174`** (cited, gold #1)

````text
Item 8. Financial Statements and Supplementary Data > CONSOLIDATED STATEMENTS OF SHAREHOLDERS’ EQUITY (table)
|  | Years ended |  |  |
|---|---|---|---|
|  | September 28, 2019 | September 29, 2018 | September 30, 2017 |
| Cumulative effects of changes in accounting principles | 2,501 | 278 | — |
| Ending balances | 45,898 | 70,400 | 98,330 |
| Accumulated other comprehensive income/(loss): |  |  |  |
| Beginning balances | (3,454) | (150) | 634 |
| Other comprehensive income/(loss) | 2,781 | (3,026) | (784) |
| Cumulative effects of changes in accounting principles | 89 | (278) | — |
| Ending balances | (584) | (3,454) | (150) |
| Total shareholders’ equity, ending balances | $90,488 | $107,147 | $134,047 |
| Dividends and dividend equivalents declared per share or RSU | $3.00 | $2.72 | $2.40 |
````

</details>

RQ2 citation match (section level): `cited=[('AAPL', 'Item 8')] gold=[(None, 'Item 8')]`

### System B (hybrid + rerank)

Model: `gpt-5.4-2026-03-05`. Hops: 1. Chunks retrieved: 5, cited: 1.

**Generated answer**

> Apple’s total shareholders’ equity decreased from **$107,147 million** in 2018 to **$90,488 million** in 2019 [2].
>
> Percentage decrease:
>
> \[
> \frac{107,147 - 90,488}{107,147} \times 100 \approx 15.5\%
> \]
>
> So, Apple’s total shareholders’ equity decreased by **about 15.5%** [2].

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `AAPL_FY2019_2019-09-28:106` | Item 7 › Fiscal 2019 Highlights |  |  | Total net sales decreased 2% or $5.4 billion during 2019 compared to 2018, driven by lower net sales of iPhone, partially offset by higher net sales of Wearables, Home and Accessories and Services in all geographic opera… |
| 2 | `AAPL_FY2019_2019-09-28:174` | Item 8 › CONSOLIDATED STATEMENTS OF SHAREHOLDERS’ EQUITY | ✓ | #1 | \| \| Years ended \| \| \| \|---\|---\|---\|---\| \| \| September 28, 2019 \| September 29, 2018 \| September 30, 2017 \| \| Cumulative effects of changes in accounting principles \| 2,501 \| 278 \| — \| \| Ending balances \| 45,898 \| 70,400 … |
| 3 | `AAPL_FY2019_2019-09-28:173` | Item 8 › CONSOLIDATED STATEMENTS OF SHAREHOLDERS’ EQUITY |  | #1 | \| \| Years ended \| \| \| \|---\|---\|---\|---\| \| \| September 28, 2019 \| September 29, 2018 \| September 30, 2017 \| \| Total shareholders’ equity, beginning balances \| $107,147 \| $134,047 \| $128,249 \| \| Common stock and additional… |
| 4 | `AAPL_FY2019_2019-09-28:170` | Item 8 › CONSOLIDATED BALANCE SHEETS |  |  | \| \| September 28, 2019 \| September 29, 2018 \| \|---\|---\|---\| \| Non-current liabilities: \| \| \| \| Term debt \| 91,807 \| 93,735 \| \| Other non-current liabilities \| 50,503 \| 48,914 \| \| Total non-current liabilities \| 142,310 \|… |
| 5 | `AAPL_FY2019_2019-09-28:169` | Item 8 › CONSOLIDATED BALANCE SHEETS |  |  | \| \| September 28, 2019 \| September 29, 2018 \| \|---\|---\|---\| \| ASSETS: \| \| \| \| Current assets: \| \| \| \| Cash and cash equivalents \| $48,844 \| $25,913 \| \| Marketable securities \| 51,713 \| 40,388 \| \| Accounts receivable, net… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#2 `AAPL_FY2019_2019-09-28:174`** (cited, gold #1)

````text
Item 8. Financial Statements and Supplementary Data > CONSOLIDATED STATEMENTS OF SHAREHOLDERS’ EQUITY (table)
|  | Years ended |  |  |
|---|---|---|---|
|  | September 28, 2019 | September 29, 2018 | September 30, 2017 |
| Cumulative effects of changes in accounting principles | 2,501 | 278 | — |
| Ending balances | 45,898 | 70,400 | 98,330 |
| Accumulated other comprehensive income/(loss): |  |  |  |
| Beginning balances | (3,454) | (150) | 634 |
| Other comprehensive income/(loss) | 2,781 | (3,026) | (784) |
| Cumulative effects of changes in accounting principles | 89 | (278) | — |
| Ending balances | (584) | (3,454) | (150) |
| Total shareholders’ equity, ending balances | $90,488 | $107,147 | $134,047 |
| Dividends and dividend equivalents declared per share or RSU | $3.00 | $2.72 | $2.40 |
````

**#3 `AAPL_FY2019_2019-09-28:173`** (gold #1)

````text
Item 8. Financial Statements and Supplementary Data > CONSOLIDATED STATEMENTS OF SHAREHOLDERS’ EQUITY (table)
|  | Years ended |  |  |
|---|---|---|---|
|  | September 28, 2019 | September 29, 2018 | September 30, 2017 |
| Total shareholders’ equity, beginning balances | $107,147 | $134,047 | $128,249 |
| Common stock and additional paid-in capital: |  |  |  |
| Beginning balances | 40,201 | 35,867 | 31,251 |
| Common stock issued | 781 | 669 | 555 |
| Common stock withheld related to net share settlement of equity awards | (2,002) | (1,778) | (1,468) |
| Share-based compensation | 6,194 | 5,443 | 4,909 |
| Tax benefit from equity awards, including transfer pricing adjustments | — | — | 620 |
| Ending balances | 45,174 | 40,201 | 35,867 |
| Retained earnings: |  |  |  |
| Beginning balances | 70,400 | 98,330 | 96,364 |
| Net income | 55,256 | 59,531 | 48,351 |
| Dividends and dividend equivalents declared | (14,129) | (13,735) | (12,803) |
| Common stock withheld related to net share settlement of equity awards | (1,029) | (948) | (581) |
| Common stock repurchased | (67,101) | (73,056) | (33,001) |
````

</details>

RQ2 citation match (section level): `cited=[('AAPL', 'Item 8')] gold=[(None, 'Item 8')]`

### System C v1 (adaptive multi-hop)

Model: `gpt-5.4`. Hops: 1. Chunks retrieved: 6, cited: 1.

**Generated answer**

> Apple’s total shareholders’ equity decreased from $107,147 at the end of fiscal 2018 to $90,488 at the end of fiscal 2019, a decline of approximately 15.5% [AAPL FY2019, Item 8, AAPL_FY2019_2019-09-28:174].

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `AAPL_FY2019_2019-09-28:173` | Item 8 › CONSOLIDATED STATEMENTS OF SHAREHOLDERS’ EQUITY |  | #1 | \| \| Years ended \| \| \| \|---\|---\|---\|---\| \| \| September 28, 2019 \| September 29, 2018 \| September 30, 2017 \| \| Total shareholders’ equity, beginning balances \| $107,147 \| $134,047 \| $128,249 \| \| Common stock and additional… |
| 2 | `AAPL_FY2019_2019-09-28:174` | Item 8 › CONSOLIDATED STATEMENTS OF SHAREHOLDERS’ EQUITY | ✓ | #1 | \| \| Years ended \| \| \| \|---\|---\|---\|---\| \| \| September 28, 2019 \| September 29, 2018 \| September 30, 2017 \| \| Cumulative effects of changes in accounting principles \| 2,501 \| 278 \| — \| \| Ending balances \| 45,898 \| 70,400 … |
| 3 | `AAPL_FY2019_2019-09-28:269` | Item 8 › Shares of Common Stock |  |  | \| \| 2019 \| 2018 \| 2017 \| \|---\|---\|---\|---\| \| Common stock outstanding, beginning balances \| 4,754,986 \| 5,126,201 \| 5,336,166 \| \| Common stock repurchased \| (345,205) \| (405,549) \| (246,496) \| \| Common stock issued, net … |
| 4 | `AAPL_FY2019_2019-09-28:170` | Item 8 › CONSOLIDATED BALANCE SHEETS |  |  | \| \| September 28, 2019 \| September 29, 2018 \| \|---\|---\|---\| \| Non-current liabilities: \| \| \| \| Term debt \| 91,807 \| 93,735 \| \| Other non-current liabilities \| 50,503 \| 48,914 \| \| Total non-current liabilities \| 142,310 \|… |
| 5 | `AAPL_FY2019_2019-09-28:179` | Item 8 › CONSOLIDATED STATEMENTS OF CASH FLOWS |  |  | \| \| Years ended \| \| \| \|---\|---\|---\|---\| \| \| September 28, 2019 \| September 29, 2018 \| September 30, 2017 \| \| Payments for taxes related to net share settlement of equity awards \| (2,817) \| (2,527) \| (1,874) \| \| Payments … |
| 6 | `AAPL_FY2019_2019-09-28:169` | Item 8 › CONSOLIDATED BALANCE SHEETS |  |  | \| \| September 28, 2019 \| September 29, 2018 \| \|---\|---\|---\| \| ASSETS: \| \| \| \| Current assets: \| \| \| \| Cash and cash equivalents \| $48,844 \| $25,913 \| \| Marketable securities \| 51,713 \| 40,388 \| \| Accounts receivable, net… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#1 `AAPL_FY2019_2019-09-28:173`** (gold #1)

````text
Item 8. Financial Statements and Supplementary Data > CONSOLIDATED STATEMENTS OF SHAREHOLDERS’ EQUITY (table)
|  | Years ended |  |  |
|---|---|---|---|
|  | September 28, 2019 | September 29, 2018 | September 30, 2017 |
| Total shareholders’ equity, beginning balances | $107,147 | $134,047 | $128,249 |
| Common stock and additional paid-in capital: |  |  |  |
| Beginning balances | 40,201 | 35,867 | 31,251 |
| Common stock issued | 781 | 669 | 555 |
| Common stock withheld related to net share settlement of equity awards | (2,002) | (1,778) | (1,468) |
| Share-based compensation | 6,194 | 5,443 | 4,909 |
| Tax benefit from equity awards, including transfer pricing adjustments | — | — | 620 |
| Ending balances | 45,174 | 40,201 | 35,867 |
| Retained earnings: |  |  |  |
| Beginning balances | 70,400 | 98,330 | 96,364 |
| Net income | 55,256 | 59,531 | 48,351 |
| Dividends and dividend equivalents declared | (14,129) | (13,735) | (12,803) |
| Common stock withheld related to net share settlement of equity awards | (1,029) | (948) | (581) |
| Common stock repurchased | (67,101) | (73,056) | (33,001) |
````

**#2 `AAPL_FY2019_2019-09-28:174`** (cited, gold #1)

````text
Item 8. Financial Statements and Supplementary Data > CONSOLIDATED STATEMENTS OF SHAREHOLDERS’ EQUITY (table)
|  | Years ended |  |  |
|---|---|---|---|
|  | September 28, 2019 | September 29, 2018 | September 30, 2017 |
| Cumulative effects of changes in accounting principles | 2,501 | 278 | — |
| Ending balances | 45,898 | 70,400 | 98,330 |
| Accumulated other comprehensive income/(loss): |  |  |  |
| Beginning balances | (3,454) | (150) | 634 |
| Other comprehensive income/(loss) | 2,781 | (3,026) | (784) |
| Cumulative effects of changes in accounting principles | 89 | (278) | — |
| Ending balances | (584) | (3,454) | (150) |
| Total shareholders’ equity, ending balances | $90,488 | $107,147 | $134,047 |
| Dividends and dividend equivalents declared per share or RSU | $3.00 | $2.72 | $2.40 |
````

</details>

RQ2 citation match (section level): `cited=[('AAPL', 'Item 8')] gold=[(None, 'Item 8')]`

**System C guardrail** (judge `gpt-5.4`): numerical claims 3, verified 3, ungrounded 0, uncited 0, derived 1; sentence verdicts: supported 0, partial 0, unsupported 0, unchecked 0.


<details><summary>Guardrail sentence verdicts</summary>

| sentence | verdict | judge reason |
|---|---|---|
| Apple’s total shareholders’ equity decreased from $107,147 at the end of fiscal 2018 to $90,488 at the end of fiscal 2019, a decline of approximately 15.5% [AAPL FY2019, Item 8, AAPL_FY2019_2019-09-28:174]. | None |  |

</details>

### System C v2 (agentic multi-hop + XBRL)

Model: `gpt-5.4`. Hops: 1. Chunks retrieved: 7, cited: 2.

**Generated answer**

> Apple’s total shareholders’ equity decreased from $107,147 in fiscal 2018 to $90,488 in fiscal 2019, a decline of approximately 15.5% [AAPL FY2019, Item 8, AAPL_FY2019_2019-09-28:174] [AAPL FY2019, Item 8, AAPL_FY2019_2019-09-28:170].

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `F-AAPL-2019` | SEC XBRL Reported Financials (financials.csv) |  |  | fiscal_year,fiscal_year_end,Revenue,NetIncome,OperatingIncome,TotalAssets,TotalLiabilities,StockholdersEquity,CashAndEquivalents,OperatingCashFlow,EPSDiluted 2019,2019-09-28,260174000000,55256000000,63930000000,338516000… |
| 2 | `AAPL_FY2019_2019-09-28:173` | Item 8 › CONSOLIDATED STATEMENTS OF SHAREHOLDERS’ EQUITY |  | #1 | \| \| Years ended \| \| \| \|---\|---\|---\|---\| \| \| September 28, 2019 \| September 29, 2018 \| September 30, 2017 \| \| Total shareholders’ equity, beginning balances \| $107,147 \| $134,047 \| $128,249 \| \| Common stock and additional… |
| 3 | `AAPL_FY2019_2019-09-28:174` | Item 8 › CONSOLIDATED STATEMENTS OF SHAREHOLDERS’ EQUITY | ✓ | #1 | \| \| Years ended \| \| \| \|---\|---\|---\|---\| \| \| September 28, 2019 \| September 29, 2018 \| September 30, 2017 \| \| Cumulative effects of changes in accounting principles \| 2,501 \| 278 \| — \| \| Ending balances \| 45,898 \| 70,400 … |
| 4 | `AAPL_FY2019_2019-09-28:170` | Item 8 › CONSOLIDATED BALANCE SHEETS | ✓ |  | \| \| September 28, 2019 \| September 29, 2018 \| \|---\|---\|---\| \| Non-current liabilities: \| \| \| \| Term debt \| 91,807 \| 93,735 \| \| Other non-current liabilities \| 50,503 \| 48,914 \| \| Total non-current liabilities \| 142,310 \|… |
| 5 | `AAPL_FY2019_2019-09-28:98` | Item 5 › Company Stock Performance |  |  | The following graph shows a comparison of cumulative total shareholder return, calculated on a dividend-reinvested basis, for the Company, the S&P 500 Index, the S&P Information Technology Index and the Dow Jones U.S. Te… |
| 6 | `AAPL_FY2019_2019-09-28:96` | Item 5 › Purchases of Equity Securities by the Issuer and Affiliated Purchasers |  |  | \| Periods \| Total Number of Shares Purchased \| Average Price Paid Per Share \| Total Number of Shares Purchased as Part of Publicly Announced Plans or Programs \| Approximate Dollar Value of Shares That May Yet Be Purchase… |
| 7 | `AAPL_FY2019_2019-09-28:97` | Item 5 › Purchases of Equity Securities by the Issuer and Affiliated Purchasers |  |  | (1) On April 30, 2019, the Company announced the Board of Directors increased the current share repurchase program authorization from $100 billion to $175 billion of the Company’s common stock, of which $96.1 billion had… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#2 `AAPL_FY2019_2019-09-28:173`** (gold #1)

````text
Item 8. Financial Statements and Supplementary Data > CONSOLIDATED STATEMENTS OF SHAREHOLDERS’ EQUITY (table)
|  | Years ended |  |  |
|---|---|---|---|
|  | September 28, 2019 | September 29, 2018 | September 30, 2017 |
| Total shareholders’ equity, beginning balances | $107,147 | $134,047 | $128,249 |
| Common stock and additional paid-in capital: |  |  |  |
| Beginning balances | 40,201 | 35,867 | 31,251 |
| Common stock issued | 781 | 669 | 555 |
| Common stock withheld related to net share settlement of equity awards | (2,002) | (1,778) | (1,468) |
| Share-based compensation | 6,194 | 5,443 | 4,909 |
| Tax benefit from equity awards, including transfer pricing adjustments | — | — | 620 |
| Ending balances | 45,174 | 40,201 | 35,867 |
| Retained earnings: |  |  |  |
| Beginning balances | 70,400 | 98,330 | 96,364 |
| Net income | 55,256 | 59,531 | 48,351 |
| Dividends and dividend equivalents declared | (14,129) | (13,735) | (12,803) |
| Common stock withheld related to net share settlement of equity awards | (1,029) | (948) | (581) |
| Common stock repurchased | (67,101) | (73,056) | (33,001) |
````

**#3 `AAPL_FY2019_2019-09-28:174`** (cited, gold #1)

````text
Item 8. Financial Statements and Supplementary Data > CONSOLIDATED STATEMENTS OF SHAREHOLDERS’ EQUITY (table)
|  | Years ended |  |  |
|---|---|---|---|
|  | September 28, 2019 | September 29, 2018 | September 30, 2017 |
| Cumulative effects of changes in accounting principles | 2,501 | 278 | — |
| Ending balances | 45,898 | 70,400 | 98,330 |
| Accumulated other comprehensive income/(loss): |  |  |  |
| Beginning balances | (3,454) | (150) | 634 |
| Other comprehensive income/(loss) | 2,781 | (3,026) | (784) |
| Cumulative effects of changes in accounting principles | 89 | (278) | — |
| Ending balances | (584) | (3,454) | (150) |
| Total shareholders’ equity, ending balances | $90,488 | $107,147 | $134,047 |
| Dividends and dividend equivalents declared per share or RSU | $3.00 | $2.72 | $2.40 |
````

**#4 `AAPL_FY2019_2019-09-28:170`** (cited)

````text
Item 8. Financial Statements and Supplementary Data > CONSOLIDATED BALANCE SHEETS (table)
|  | September 28, 2019 | September 29, 2018 |
|---|---|---|
| Non-current liabilities: |  |  |
| Term debt | 91,807 | 93,735 |
| Other non-current liabilities | 50,503 | 48,914 |
| Total non-current liabilities | 142,310 | 142,649 |
| Total liabilities | 248,028 | 258,578 |
| Commitments and contingencies |  |  |
| Shareholders’ equity: |  |  |
| Common stock and additional paid-in capital, $0.00001 par value: 12,600,000 shares authorized; 4,443,236 and 4,754,986 shares issued and outstanding, respectively | 45,174 | 40,201 |
| Retained earnings | 45,898 | 70,400 |
| Accumulated other comprehensive income/(loss) | (584) | (3,454) |
| Total shareholders’ equity | 90,488 | 107,147 |
| Total liabilities and shareholders’ equity | $338,516 | $365,725 |
````

</details>

RQ2 citation match (section level): `cited=[('AAPL', 'Item 8')] gold=[(None, 'Item 8')]`

**System C guardrail** (judge `gpt-5.4`): numerical claims 3, verified 3, ungrounded 0, uncited 0, derived 1; sentence verdicts: supported 0, partial 0, unsupported 0, unchecked 0.


<details><summary>Guardrail sentence verdicts</summary>

| sentence | verdict | judge reason |
|---|---|---|
| Apple’s total shareholders’ equity decreased from $107,147 in fiscal 2018 to $90,488 in fiscal 2019, a decline of approximately 15.5% [AAPL FY2019, Item 8, AAPL_FY2019_2019-09-28:174] [AAPL FY2019, Item 8, AAPL_FY2019_2019-09-28:170]. | None |  |

</details>
