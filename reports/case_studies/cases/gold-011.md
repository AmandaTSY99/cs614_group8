# gold-011: Cross-year table

[← all cases](../README.md) · company: MICROSOFT CORP (MSFT) · fiscal year: 2020 · recipe `cross_year_table` · hop `multi` · answer type `numeric` · scope `cross_year` · RQ2 category `multi_company_comparison`

## Gold QA

**Question**

> What is the percentage decrease in Microsoft's total estimated future amortization expense for intangible assets from June 30, 2017, to June 30, 2020?

**Gold answer**

> -30.36%

**Program**: `subtract(7038, 10106), divide(#0, 10106), multiply(#1, 100)` → `-30.35820304769444`

**Gold numbers** (RQ2 numeric_accuracy targets): -30.36%

**Gold evidence**

1. `MSFT_FY2020_2020-06-30` · Item 8 › PART II · table

   > | Total | $7,038 |

2. `MSFT_FY2017_2017-06-30` · Item 8 › PART II · table

   > | Total | $10,106 |

## Scorecard

| Metric | A (vanilla dense) | B (hybrid + rerank) | C v1 (adaptive multi-hop) | C v2 (agentic multi-hop + XBRL) |
|---|---|---|---|---|
| **Retrieval (RQ1)** | | | | |
| chunks retrieved | 10 | 5 | 13 | 8 |
| recall@5 | 0.50 | 0.50 | 0.00 | 0.00 |
| recall@all | 0.50 | 0.50 | 0.50 | 0.50 |
| complete@all | 0 | 0 | 0 | 0 |
| average precision (lexical) | 0.33 | 0.20 | 0.17 | 0.12 |
| gold evidence first rank | #1: 3, #2: – | #1: 5, #2: – | #1: 6, #2: – | #1: 8, #2: – |
| **Answer (RQ3 string match)** | | | | |
| numeric_correct | ✗ | ✗ | ✗ | ✗ |
| keypoint_recall | – | – | – | – |
| **Answer & citations (RQ2)** | | | | |
| numeric_accuracy | 0.00 | 0.00 | 0.00 | 0.00 |
| citation precision | – | – | 1.00 | – |
| citation recall | – | – | 1.00 | – |
| citation F1 | – | – | 1.00 | – |
| has a citation | 0 | 0 | 1 | 0 |
| grounding error rate | – | – | 0.00 | 0.00 |
| **Cost (RQ3)** | | | | |
| retrieval hops | 1 | 1 | 3 | 1 |
| tokens | 2868 | 1186 | 12460 | 6306 |
| cost (USD) | 0.0004 | 0.0002 | 0.0498 | 0.0230 |
| latency (s) | 1.6 | 5.5 | 23.8 | 9.7 |

Definitions: [README › Metrics](../README.md#metrics). `–` = not applicable (e.g. no gold number, no citations, no guardrail).

## System outputs

### System A (vanilla dense)

Model: `gpt-5.4-2026-03-05`. Hops: 1. Chunks retrieved: 10, cited: 0.

**Generated answer**

> Not found in the provided context.

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `MSFT_FY2020_2020-06-30:347` | Item 8 › Unrealized Losses on Debt Investments |  |  | \| \| Less than 12 Months \| \| 12 Months or Greater \| \| Total Unrealized Losses \| \| \|---\|---\|---\|---\|---\|---\|---\| \| (In millions) \| Fair Value \| Unrealized Losses \| Fair Value \| Unrealized Losses \| Total Fair Value \| \| \| Ju… |
| 2 | `MSFT_FY2020_2020-06-30:406` | Item 8 › PART II |  |  | \| (In millions) \| \| \| \|---\|---\|---\| \| June 30, \| 2020 \| 2019 \| \| Deferred Income Tax Assets \| \| \| \| Stock-based compensation expense \| $461 \| $406 \| \| Accruals, reserves, and other expenses \| 2,721 \| 2,287 \| \| Loss and c… |
| 3 | `MSFT_FY2020_2020-06-30:274` | Item 8 › BALANCE SHEETS |  | #1 | \| (In millions) \| \| \| \|---\|---\|---\| \| June 30, \| 2020 \| 2019 \| \| Assets \| \| \| \| Current assets: \| \| \| \| Cash and cash equivalents \| $13,576 \| $11,356 \| \| Short-term investments \| 122,951 \| 122,463 \| \| Total cash, cash eq… |
| 4 | `MSFT_FY2020_2020-06-30:194` | Item 7 › PART II |  |  | \| (In millions, except percentages) \| 2020 \| 2019 \| 2018 \| Percentage Change 2020 Versus 2019 \| Percentage Change 2019 Versus 2018 \| \|---\|---\|---\|---\|---\|---\| \| Revenue \| \| \| \| \| \| \| Productivity and Business Processes \|… |
| 5 | `MSFT_FY2020_2020-06-30:188` | Item 7 › PART II |  |  | \| (In millions, except percentages and per share amounts) \| 2020 \| 2019 \| 2018 \| Percentage Change 2020 Versus 2019 \| Percentage Change 2019 Versus 2018 \| \|---\|---\|---\|---\|---\|---\| \| Revenue \| $143,015 \| $125,843 \| $110,… |
| 6 | `MSFT_FY2020_2020-06-30:384` | Item 8 › PART II |  | #1 | \| (In millions) \| Gross Carrying Amount \| Accumulated Amortization \| Net Carrying Amount \| Gross Carrying Amount \| Accumulated Amortization \| Net Carrying Amount \| \| \|---\|---\|---\|---\|---\|---\|---\|---\| \| June 30, \| \| \| 202… |
| 7 | `MSFT_FY2020_2020-06-30:204` | Item 7 › Research and Development |  |  | \| (In millions, except percentages) \| 2020 \| 2019 \| 2018 \| Percentage Change 2020 Versus 2019 \| Percentage Change 2019 Versus 2018 \| \|---\|---\|---\|---\|---\|---\| \| Research and development \| $19,269 \| $16,876 \| $14,726 \| 14… |
| 8 | `MSFT_FY2020_2020-06-30:348` | Item 8 › PART II |  |  | \| \| Less than 12 Months \| \| 12 Months or Greater \| \| Total Unrealized Losses \| \| \|---\|---\|---\|---\|---\|---\|---\| \| (In millions) \| Fair Value \| Unrealized Losses \| Fair Value \| Unrealized Losses \| Total Fair Value \| \| \| Ju… |
| 9 | `MSFT_FY2020_2020-06-30:227` | Item 7 › Uncertain Tax Positions |  |  | \| (In millions, except percentages and per share amounts) \| 2020 \| 2019 \| 2018 \| Percentage Change 2020 Versus 2019 \| Percentage Change 2019 Versus 2018 \| \|---\|---\|---\|---\|---\|---\| \| Net income \| $44,281 \| $39,240 \| $16,… |
| 10 | `MSFT_FY2020_2020-06-30:218` | Item 7 › Fiscal Year 2020 Compared with Fiscal Year 2019 |  |  | Interest and dividends income decreased due to lower yields, offset in part by higher average portfolio balances on fixed-income securities. Interest expense decreased due to capitalization of interest expense and a decr… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#3 `MSFT_FY2020_2020-06-30:274`** (gold #1)

````text
Item 8 > BALANCE SHEETS (table)
| (In millions) |  |  |
|---|---|---|
| June 30, | 2020 | 2019 |
| Assets |  |  |
| Current assets: |  |  |
| Cash and cash equivalents | $13,576 | $11,356 |
| Short-term investments | 122,951 | 122,463 |
| Total cash, cash equivalents, and short-term investments | 136,527 | 133,819 |
| Accounts receivable, net of allowance for doubtful accounts of $788 and $411 | 32,011 | 29,524 |
| Inventories | 1,895 | 2,063 |
| Other current assets | 11,482 | 10,146 |
| Total current assets | 181,915 | 175,552 |
| Property and equipment, net of accumulated depreciation of $43,197 and $35,330 | 44,151 | 36,477 |
| Operating lease right-of-use assets | 8,753 | 7,379 |
| Equity investments | 2,965 | 2,649 |
| Goodwill | 43,351 | 42,026 |
| Intangible assets, net | 7,038 | 7,750 |
| Other long-term assets | 13,138 | 14,723 |
| Total assets | $301,311 | $286,556 |
| Liabilities and stockholders’ equity |  |  |
| Current liabilities: |  |  |
| Accounts payable | $12,530 | $9,382 |
````

**#6 `MSFT_FY2020_2020-06-30:384`** (gold #1)

````text
Item 8 > PART II (table)
| (In millions) | Gross Carrying Amount | Accumulated Amortization | Net Carrying Amount | Gross Carrying Amount | Accumulated Amortization | Net Carrying Amount |  |
|---|---|---|---|---|---|---|---|
| June 30, |  |  | 2020 |  |  | 2019 |  |
| Technology-based | $8,160 | $(6,381) | $1,779 | $7,691 |  | $(5,771) | $1,920 |
| Customer-related | 4,967 | (2,320) | 2,647 | 4,709 |  | (1,785) | 2,924 |
| Marketing-related | 4,158 | (1,588) | 2,570 | 4,165 |  | (1,327) | 2,838 |
| Contract-based | 474 | (432) | 42 | 574 |  | (506) | 68 |
| Total | $17,759 | $(10,721) | $7,038 | $17,139 | (a) | $(9,389) | $7,750 |
````

</details>

RQ2 citation match (section level): `no citations`

### System B (hybrid + rerank)

Model: `gpt-5.4-2026-03-05`. Hops: 1. Chunks retrieved: 5, cited: 0.

**Generated answer**

> Not found in the provided context.

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `MSFT_FY2020_2020-06-30:387` | Item 8 › PART II |  |  | Intangible assets amortization expense was $1.6 billion, $1.9 billion, and $2.2 billion for fiscal years 2020, 2019, and 2018, respectively. The following table outlines the estimated future amortization expense related … |
| 2 | `MSFT_FY2017_2017-06-30:379` | Item 8 › PART II |  |  | Intangible assets amortization expense was $1.7 billion, $978 million, and $1.3 billion for fiscal years 2017, 2016, and 2015, respectively. Amortization of capitalized software was $55 million, $69 million, and $79 mill… |
| 3 | `MSFT_FY2017_2017-06-30:375` | Item 8 › PART II |  |  | (a) Technology-based intangible assets included $59 million and $115 million of net carrying amount of software to be sold, leased, or otherwise marketed as of June 30, 2017 and 2016, respectively. (b) Includes intangibl… |
| 4 | `MSFT_FY2017_2017-06-30:165` | Item 7 › PART II |  |  | • Office Consumer revenue increased $425 million or 14%, driven by higher revenue from Office 365 consumer, mainly due to growth in subscribers. • Dynamics revenue increased 9%, primarily due to higher revenue from Dynam… |
| 5 | `MSFT_FY2020_2020-06-30:274` | Item 8 › BALANCE SHEETS |  | #1 | \| (In millions) \| \| \| \|---\|---\|---\| \| June 30, \| 2020 \| 2019 \| \| Assets \| \| \| \| Current assets: \| \| \| \| Cash and cash equivalents \| $13,576 \| $11,356 \| \| Short-term investments \| 122,951 \| 122,463 \| \| Total cash, cash eq… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#5 `MSFT_FY2020_2020-06-30:274`** (gold #1)

````text
Item 8 > BALANCE SHEETS (table)
| (In millions) |  |  |
|---|---|---|
| June 30, | 2020 | 2019 |
| Assets |  |  |
| Current assets: |  |  |
| Cash and cash equivalents | $13,576 | $11,356 |
| Short-term investments | 122,951 | 122,463 |
| Total cash, cash equivalents, and short-term investments | 136,527 | 133,819 |
| Accounts receivable, net of allowance for doubtful accounts of $788 and $411 | 32,011 | 29,524 |
| Inventories | 1,895 | 2,063 |
| Other current assets | 11,482 | 10,146 |
| Total current assets | 181,915 | 175,552 |
| Property and equipment, net of accumulated depreciation of $43,197 and $35,330 | 44,151 | 36,477 |
| Operating lease right-of-use assets | 8,753 | 7,379 |
| Equity investments | 2,965 | 2,649 |
| Goodwill | 43,351 | 42,026 |
| Intangible assets, net | 7,038 | 7,750 |
| Other long-term assets | 13,138 | 14,723 |
| Total assets | $301,311 | $286,556 |
| Liabilities and stockholders’ equity |  |  |
| Current liabilities: |  |  |
| Accounts payable | $12,530 | $9,382 |
````

</details>

RQ2 citation match (section level): `no citations`

### System C v1 (adaptive multi-hop)

Model: `gpt-5.4`. Hops: 3. Chunks retrieved: 13, cited: 2.

**Generated answer**

> The filing excerpts provided do not disclose the total estimated future amortization expense related to intangible assets as of June 30, 2017, so the percentage decrease from June 30, 2017, to June 30, 2020 cannot be determined from the evidence provided. [MSFT FY2017, Item 8, MSFT_FY2017_2017-06-30:379] [MSFT FY2020, Item 8, MSFT_FY2020_2020-06-30:394]

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `MSFT_FY2020_2020-06-30:387` | Item 8 › PART II |  |  | Intangible assets amortization expense was $1.6 billion, $1.9 billion, and $2.2 billion for fiscal years 2020, 2019, and 2018, respectively. The following table outlines the estimated future amortization expense related … |
| 2 | `MSFT_FY2017_2017-06-30:379` | Item 8 › PART II | ✓ |  | Intangible assets amortization expense was $1.7 billion, $978 million, and $1.3 billion for fiscal years 2017, 2016, and 2015, respectively. Amortization of capitalized software was $55 million, $69 million, and $79 mill… |
| 3 | `MSFT_FY2020_2020-06-30:324` | Item 8 › Intangible Assets |  |  | Our intangible assets are subject to amortization and are amortized using the straight-line method over their estimated period of benefit, ranging from one to 20 years. We evaluate the recoverability of intangible assets… |
| 4 | `MSFT_FY2017_2017-06-30:292` | Item 8 › Intangible Assets |  |  | All of our intangible assets are subject to amortization and are amortized using the straight-line method over their estimated period of benefit, ranging from one to 15 years. We evaluate the recoverability of intangible… |
| 5 | `MSFT_FY2017_2017-06-30:375` | Item 8 › PART II |  |  | (a) Technology-based intangible assets included $59 million and $115 million of net carrying amount of software to be sold, leased, or otherwise marketed as of June 30, 2017 and 2016, respectively. (b) Includes intangibl… |
| 6 | `MSFT_FY2020_2020-06-30:274` | Item 8 › BALANCE SHEETS |  | #1 | \| (In millions) \| \| \| \|---\|---\|---\| \| June 30, \| 2020 \| 2019 \| \| Assets \| \| \| \| Current assets: \| \| \| \| Cash and cash equivalents \| $13,576 \| $11,356 \| \| Short-term investments \| 122,951 \| 122,463 \| \| Total cash, cash eq… |
| 7 | `MSFT_FY2020_2020-06-30:376` | Item 8 › PART II |  |  | Following are the details of the purchase price allocated to the intangible assets acquired: |
| 8 | `MSFT_FY2020_2020-06-30:347` | Item 8 › Unrealized Losses on Debt Investments |  |  | \| \| Less than 12 Months \| \| 12 Months or Greater \| \| Total Unrealized Losses \| \| \|---\|---\|---\|---\|---\|---\|---\| \| (In millions) \| Fair Value \| Unrealized Losses \| Fair Value \| Unrealized Losses \| Total Fair Value \| \| \| Ju… |
| 9 | `MSFT_FY2020_2020-06-30:348` | Item 8 › PART II |  |  | \| \| Less than 12 Months \| \| 12 Months or Greater \| \| Total Unrealized Losses \| \| \|---\|---\|---\|---\|---\|---\|---\| \| (In millions) \| Fair Value \| Unrealized Losses \| Fair Value \| Unrealized Losses \| Total Fair Value \| \| \| Ju… |
| 10 | `MSFT_FY2020_2020-06-30:362` | Item 8 › Fair Values of Derivative Instruments |  |  | \| (In millions) \| Level 1 \| Level 2 \| Level 3 \| Total \| \|---\|---\|---\|---\|---\| \| June 30, 2020 \| \| \| \| \| \| Derivative assets \| $1 \| $398 \| $1 \| $400 \| \| Derivative liabilities \| 0 \| (399) \| 0 \| (399) \| \| June 30, 2019 \| \|… |
| 11 | `MSFT_FY2020_2020-06-30:385` | Item 8 › PART II |  |  | (a) Includes intangible assets of $1.3 billion related to GitHub. See Note 8 – Business Combinations for further information. No material impairments of intangible assets were identified during fiscal years 2020, 2019, o… |
| 12 | `MSFT_FY2020_2020-06-30:383` | Item 8 › PART II |  |  | NOTE 10 — INTANGIBLE ASSETS The components of intangible assets, all of which are finite-lived, were as follows: |
| 13 | `MSFT_FY2020_2020-06-30:394` | Item 8 › PART II | ✓ |  | \| (In millions) \| \| \|---\|---\| \| Year Ending June 30, \| \| \| 2021 \| $3,750 \| \| 2022 \| 7,966 \| \| 2023 \| 2,750 \| \| 2024 \| 5,250 \| \| 2025 \| 2,250 \| \| Thereafter \| 45,441 \| \| Total \| $67,407 \| |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#2 `MSFT_FY2017_2017-06-30:379`** (cited)

````text
Item 8 > PART II
Intangible assets amortization expense was $1.7 billion, $978 million, and $1.3 billion for fiscal years 2017, 2016, and 2015, respectively. Amortization of capitalized software was $55 million, $69 million, and $79 million for fiscal years 2017, 2016, and 2015, respectively. The following table outlines the estimated future amortization expense related to intangible assets held as of June 30, 2017:
````

**#6 `MSFT_FY2020_2020-06-30:274`** (gold #1)

````text
Item 8 > BALANCE SHEETS (table)
| (In millions) |  |  |
|---|---|---|
| June 30, | 2020 | 2019 |
| Assets |  |  |
| Current assets: |  |  |
| Cash and cash equivalents | $13,576 | $11,356 |
| Short-term investments | 122,951 | 122,463 |
| Total cash, cash equivalents, and short-term investments | 136,527 | 133,819 |
| Accounts receivable, net of allowance for doubtful accounts of $788 and $411 | 32,011 | 29,524 |
| Inventories | 1,895 | 2,063 |
| Other current assets | 11,482 | 10,146 |
| Total current assets | 181,915 | 175,552 |
| Property and equipment, net of accumulated depreciation of $43,197 and $35,330 | 44,151 | 36,477 |
| Operating lease right-of-use assets | 8,753 | 7,379 |
| Equity investments | 2,965 | 2,649 |
| Goodwill | 43,351 | 42,026 |
| Intangible assets, net | 7,038 | 7,750 |
| Other long-term assets | 13,138 | 14,723 |
| Total assets | $301,311 | $286,556 |
| Liabilities and stockholders’ equity |  |  |
| Current liabilities: |  |  |
| Accounts payable | $12,530 | $9,382 |
````

**#13 `MSFT_FY2020_2020-06-30:394`** (cited)

````text
Item 8 > PART II (table)
| (In millions) |  |
|---|---|
| Year Ending June 30, |  |
| 2021 | $3,750 |
| 2022 | 7,966 |
| 2023 | 2,750 |
| 2024 | 5,250 |
| 2025 | 2,250 |
| Thereafter | 45,441 |
| Total | $67,407 |
````

</details>

RQ2 citation match (section level): `cited=[('MSFT', 'Item 8')] gold=[(None, 'Item 8')]`

**System C guardrail** (judge `gpt-5.4`): numerical claims 0, verified 0, ungrounded 0, uncited 0, derived 0; sentence verdicts: supported 1, partial 0, unsupported 0, unchecked 0.


<details><summary>Guardrail sentence verdicts</summary>

| sentence | verdict | judge reason |
|---|---|---|
| The filing excerpts provided do not disclose the total estimated future amortization expense related to intangible assets as of June 30, 2017, so the percentage decrease from June 30, 2017, to June 30, 2020 cannot be determined from the evidence provided. [MSFT FY2017, Item 8, MSFT_FY2017_2017-06-30:379] [MSFT FY2020, Item 8, MSFT_FY2020_2020-06-30:394] | supported | The 2017 excerpt only introduces a table without showing totals, while the 2020 excerpt shows a total only for 2020, so the 2017 total and resulting percentage decrease cannot be determined from the provided evidence. |

</details>

### System C v2 (agentic multi-hop + XBRL)

Model: `gpt-5.4`. Hops: 1. Chunks retrieved: 8, cited: 0.

**Generated answer**

> The filing does not disclose the total estimated future amortization expense related to intangible assets as of June 30, 2017 or June 30, 2020 in the provided evidence, so the percentage decrease cannot be determined from these excerpts.

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `F-MSFT-2017` | SEC XBRL Reported Financials (financials.csv) |  |  | fiscal_year,fiscal_year_end,Revenue,NetIncome,OperatingIncome,TotalAssets,TotalLiabilities,StockholdersEquity,CashAndEquivalents,OperatingCashFlow,EPSDiluted 2017,2017-06-30,89950000000,21204000000,22326000000,2410860000… |
| 2 | `F-MSFT-2020` | SEC XBRL Reported Financials (financials.csv) |  |  | fiscal_year,fiscal_year_end,Revenue,NetIncome,OperatingIncome,TotalAssets,TotalLiabilities,StockholdersEquity,CashAndEquivalents,OperatingCashFlow,EPSDiluted 2020,2020-06-30,143015000000,44281000000,52959000000,301311000… |
| 3 | `MSFT_FY2020_2020-06-30:387` | Item 8 › PART II |  |  | Intangible assets amortization expense was $1.6 billion, $1.9 billion, and $2.2 billion for fiscal years 2020, 2019, and 2018, respectively. The following table outlines the estimated future amortization expense related … |
| 4 | `MSFT_FY2017_2017-06-30:379` | Item 8 › PART II |  |  | Intangible assets amortization expense was $1.7 billion, $978 million, and $1.3 billion for fiscal years 2017, 2016, and 2015, respectively. Amortization of capitalized software was $55 million, $69 million, and $79 mill… |
| 5 | `MSFT_FY2020_2020-06-30:324` | Item 8 › Intangible Assets |  |  | Our intangible assets are subject to amortization and are amortized using the straight-line method over their estimated period of benefit, ranging from one to 20 years. We evaluate the recoverability of intangible assets… |
| 6 | `MSFT_FY2017_2017-06-30:292` | Item 8 › Intangible Assets |  |  | All of our intangible assets are subject to amortization and are amortized using the straight-line method over their estimated period of benefit, ranging from one to 15 years. We evaluate the recoverability of intangible… |
| 7 | `MSFT_FY2017_2017-06-30:375` | Item 8 › PART II |  |  | (a) Technology-based intangible assets included $59 million and $115 million of net carrying amount of software to be sold, leased, or otherwise marketed as of June 30, 2017 and 2016, respectively. (b) Includes intangibl… |
| 8 | `MSFT_FY2020_2020-06-30:274` | Item 8 › BALANCE SHEETS |  | #1 | \| (In millions) \| \| \| \|---\|---\|---\| \| June 30, \| 2020 \| 2019 \| \| Assets \| \| \| \| Current assets: \| \| \| \| Cash and cash equivalents \| $13,576 \| $11,356 \| \| Short-term investments \| 122,951 \| 122,463 \| \| Total cash, cash eq… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#8 `MSFT_FY2020_2020-06-30:274`** (gold #1)

````text
Item 8 > BALANCE SHEETS (table)
| (In millions) |  |  |
|---|---|---|
| June 30, | 2020 | 2019 |
| Assets |  |  |
| Current assets: |  |  |
| Cash and cash equivalents | $13,576 | $11,356 |
| Short-term investments | 122,951 | 122,463 |
| Total cash, cash equivalents, and short-term investments | 136,527 | 133,819 |
| Accounts receivable, net of allowance for doubtful accounts of $788 and $411 | 32,011 | 29,524 |
| Inventories | 1,895 | 2,063 |
| Other current assets | 11,482 | 10,146 |
| Total current assets | 181,915 | 175,552 |
| Property and equipment, net of accumulated depreciation of $43,197 and $35,330 | 44,151 | 36,477 |
| Operating lease right-of-use assets | 8,753 | 7,379 |
| Equity investments | 2,965 | 2,649 |
| Goodwill | 43,351 | 42,026 |
| Intangible assets, net | 7,038 | 7,750 |
| Other long-term assets | 13,138 | 14,723 |
| Total assets | $301,311 | $286,556 |
| Liabilities and stockholders’ equity |  |  |
| Current liabilities: |  |  |
| Accounts payable | $12,530 | $9,382 |
````

</details>

RQ2 citation match (section level): `no citations`

**System C guardrail** (judge `gpt-5.4`): numerical claims 0, verified 0, ungrounded 0, uncited 0, derived 0; sentence verdicts: supported 1, partial 0, unsupported 0, unchecked 0.


<details><summary>Guardrail sentence verdicts</summary>

| sentence | verdict | judge reason |
|---|---|---|
| The filing does not disclose the total estimated future amortization expense related to intangible assets as of June 30, 2017 or June 30, 2020 in the provided evidence, so the percentage decrease cannot be determined from these excerpts. | supported | The retrieved excerpts mention future amortization tables for 2017 and 2020 but do not include the totals, so the percentage decrease cannot be determined from these excerpts. |

</details>
