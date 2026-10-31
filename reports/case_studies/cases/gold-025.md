# gold-025: Cross-year text

[← all cases](../README.md) · company: Tesla, Inc. (TSLA) · fiscal year: 2022 · recipe `cross_year_text` · hop `multi` · answer type `qualitative` · scope `cross_year` · RQ2 category `multi_company_comparison`

## Gold QA

**Question**

> How did Tesla's explanation for why recognizing its unrecognized tax benefits would not affect its effective tax rate evolve between fiscal year 2016 and fiscal year 2022, and what specific tax examinations are highlighted in the 2022 filing that were not mentioned in 2016?

**Gold answer**

> In both fiscal years 2016 and 2022, Tesla explained that recognizing its unrecognized tax benefits would not affect its effective tax rate because the resulting tax benefits would increase a deferred tax asset that is fully offset by a valuation allowance. However, the 2022 filing specifically notes that the company is currently under examination by the IRS for the years 2015 to 2018, whereas the 2016 filing did not mention any current IRS examinations, only that tax years 2003 to 2015 remained subject to examination.

**Key points** (RQ3 keypoint_recall targets)

1. In both years, the lack of impact on the effective tax rate is due to the deferred tax asset being fully offset by a valuation allowance.
2. The 2022 filing states Tesla is currently under IRS examination for 2015-2018.
3. The 2016 filing states tax years 2003-2015 remain subject to federal examination but does not mention a current IRS examination.

**Gold evidence**

1. `TSLA_FY2022_2022-12-31` · ITEM 8. FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA › Uncertain Tax Positions · text

   > Unrecognized tax benefits of $572 million, if recognized, would not affect our effective tax rate since the tax benefits would increase a deferred tax asset that is currently fully offset by a valuation allowance.

2. `TSLA_FY2022_2022-12-31` · ITEM 8. FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA › Uncertain Tax Positions · text

   > We are currently under examination by the Internal Revenue Service (“IRS”) for the years 2015 to 2018.

3. `TSLA_FY2016_2016-12-31` · ITEM 8. FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA › Uncertain Tax Positions · text

   > As of December 31, 2016, unrecognized tax benefits of $198.3 million, if recognized, would not affect our effective tax rate as the tax benefits would increase a deferred tax asset which is currently fully offset with a full valuation allowance.

4. `TSLA_FY2016_2016-12-31` · ITEM 8. FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA › Uncertain Tax Positions · text

   > Tax years 2003 to 2015 remain subject to examination for federal purposes, and tax years 2003 to 2015 remain subject to examination for California purposes.

## Scorecard

| Metric | A (vanilla dense) | B (hybrid + rerank) | C v1 (adaptive multi-hop) | C v2 (agentic multi-hop + XBRL) |
|---|---|---|---|---|
| **Retrieval (RQ1)** | | | | |
| chunks retrieved | 4 | 5 | 14 | 12 |
| recall@5 | 1.00 | 1.00 | 1.00 | 1.00 |
| recall@all | 1.00 | 1.00 | 1.00 | 1.00 |
| complete@all | 1 | 1 | 1 | 1 |
| average precision (lexical) | 1.00 | 1.00 | 0.87 | 0.87 |
| gold evidence first rank | #1: 1, #2: 1, #3: 1, #4: 1 | #1: 1, #2: 1, #3: 1, #4: 1 | #1: 1, #2: 2, #3: 1, #4: 1 | #1: 1, #2: 2, #3: 1, #4: 1 |
| **Answer (RQ3 string match)** | | | | |
| numeric_correct | ✓ | ✓ | ✓ | ✓ |
| keypoint_recall | 1.00 | 1.00 | 1.00 | 1.00 |
| **Answer & citations (RQ2)** | | | | |
| numeric_accuracy | – | – | – | – |
| citation precision | 1.00 | 1.00 | 1.00 | 1.00 |
| citation recall | 1.00 | 1.00 | 1.00 | 1.00 |
| citation F1 | 1.00 | 1.00 | 1.00 | 1.00 |
| has a citation | 1 | 1 | 1 | 1 |
| grounding error rate | – | – | 0.00 | 0.00 |
| **Cost (RQ3)** | | | | |
| retrieval hops | 1 | 1 | 3 | 3 |
| tokens | 1063 | 1475 | 15012 | 15018 |
| cost (USD) | 0.0003 | 0.0003 | 0.0602 | 0.0608 |
| latency (s) | 4.8 | 8.0 | 30.3 | 33.4 |

Definitions: [README › Metrics](../README.md#metrics). `–` = not applicable (e.g. no gold number, no citations, no guardrail).

## System outputs

### System A (vanilla dense)

Model: `gpt-5.4-2026-03-05`. Hops: 1. Chunks retrieved: 4, cited: 2.

**Generated answer**

> Between FY2016 and FY2022, Tesla’s explanation stayed substantively the same but was updated in wording and detail:
>
> - In FY2016, Tesla said that if its unrecognized tax benefits were recognized, they would not affect the effective tax rate because the tax benefits would increase a deferred tax asset “currently fully offset with a full valuation allowance” [2].
> - In FY2022, Tesla again said recognition would not affect the effective tax rate because the tax benefits would increase a deferred tax asset “currently fully offset by a valuation allowance” [1].
>
> So, the core explanation did not materially change: in both years, the benefits would flow to deferred tax assets that were fully offset by a valuation allowance, preventing an effect on the effective tax rate [1][2].
>
> The specific tax examinations highlighted in the 2022 filing that were not mentioned in 2016 were:
>
> - Tesla stated it was “currently under examination by the Internal Revenue Service (“IRS”) for the years 2015 to 2018” [1].
> - It also said that “additional tax years within the periods 2004 to 2014 and 2019 to 2021 remain subject to examination for federal income tax purposes” [1].
>
> By contrast, the 2016 filing only generally said that tax years 2003 to 2015 remained subject to examination for federal purposes and California purposes, without identifying an active IRS examination for specific years like 2015–2018 [2].

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `TSLA_FY2022_2022-12-31:467` | Item 8 › Uncertain Tax Positions | ✓ | #1, #2, #3, #4 | As of December 31, 2022, accrued interest and penalties related to unrecognized tax benefits are classified as income tax expense and amounted to $31 million. Unrecognized tax benefits of $572 million, if recognized, wou… |
| 2 | `TSLA_FY2016_2016-12-31:553` | Item 8 › Uncertain Tax Positions | ✓ | #1, #3, #4 | Accrued interest and penalties related to unrecognized tax benefits are classified as income tax expense and was immaterial. As of December 31, 2016, unrecognized tax benefits of $198.3 million, if recognized, would not … |
| 3 | `TSLA_FY2022_2022-12-31:465` | Item 8 › Uncertain Tax Positions |  |  | The changes to our gross unrecognized tax benefits were as follows (in millions): |
| 4 | `TSLA_FY2016_2016-12-31:551` | Item 8 › Uncertain Tax Positions |  |  | The aggregate changes in the balance of our gross unrecognized tax benefits during the years ended December 31, 2016, 2015 and 2014 were as follows (in thousands): |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#1 `TSLA_FY2022_2022-12-31:467`** (cited, gold #1, gold #2, gold #3, gold #4)

````text
ITEM 8. FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA > Uncertain Tax Positions
As of December 31, 2022, accrued interest and penalties related to unrecognized tax benefits are classified as income tax expense and amounted to $31 million. Unrecognized tax benefits of $572 million, if recognized, would not affect our effective tax rate since the tax benefits would increase a deferred tax asset that is currently fully offset by a valuation allowance. We file income tax returns in the U.S. and various state and foreign jurisdictions. We are currently under examination by the Internal Revenue Service (“IRS”) for the years 2015 to 2018. Additional tax years within the periods 2004 to 2014 and 2019 to 2021 remain subject to examination for federal income tax purposes. All net operating losses and tax credits generated to date are subject to adjustment for U.S. federal and state income tax purposes. Our returns for 2004 and subsequent tax years remain subject to examination in U.S. state and foreign jurisdictions. Given the uncertainty in timing and outcome of our tax examinations, an estimate of the range of the reasonably possible change in gross unrecognized tax benefits within twelve months cannot be made at this time.
````

**#2 `TSLA_FY2016_2016-12-31:553`** (cited, gold #1, gold #3, gold #4)

````text
ITEM 8. FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA > Uncertain Tax Positions
Accrued interest and penalties related to unrecognized tax benefits are classified as income tax expense and was immaterial. As of December 31, 2016, unrecognized tax benefits of $198.3 million, if recognized, would not affect our effective tax rate as the tax benefits would increase a deferred tax asset which is currently fully offset with a full valuation allowance. We do not anticipate that the amount of existing unrecognized tax benefits will significantly increase or decrease within the next 12 months. We file income tax returns in the United States, California, various states and foreign jurisdictions. Tax years 2003 to 2015 remain subject to examination for federal purposes, and tax years 2003 to 2015 remain subject to examination for California purposes. All net operating losses and tax credits generated to date are subject to adjustment for U.S. federal and California purposes. Tax years 2007 to 2015 remain open for examination in other U.S. state and foreign jurisdictions.
````

</details>

RQ2 citation match (section level): `cited=[('TSLA', 'Item 8')] gold=[(None, 'Item 8')]`

### System B (hybrid + rerank)

Model: `gpt-5.4-2026-03-05`. Hops: 1. Chunks retrieved: 5, cited: 2.

**Generated answer**

> In FY2016, Tesla said that recognizing its unrecognized tax benefits would not affect its effective tax rate because the tax benefits would increase a deferred tax asset “which is currently fully offset with a full valuation allowance” [2].
>
> In FY2022, Tesla gave essentially the same explanation, but with updated wording: the tax benefits “would increase a deferred tax asset that is currently fully offset by a valuation allowance” [1]. So the rationale did not materially change; it remained that the deferred tax asset was fully offset by a valuation allowance [1][2].
>
> The 2022 filing also highlighted specific tax examinations not mentioned in 2016:
> - Tesla was “currently under examination by the Internal Revenue Service (“IRS”) for the years 2015 to 2018” [1].
> - It also said that “additional tax years within the periods 2004 to 2014 and 2019 to 2021 remain subject to examination for federal income tax purposes” [1].
>
> By contrast, the 2016 filing only generally stated that tax years 2003 to 2015 remained subject to examination for federal and California purposes, without mentioning an active IRS examination for 2015–2018 [2].

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `TSLA_FY2022_2022-12-31:467` | Item 8 › Uncertain Tax Positions | ✓ | #1, #2, #3, #4 | As of December 31, 2022, accrued interest and penalties related to unrecognized tax benefits are classified as income tax expense and amounted to $31 million. Unrecognized tax benefits of $572 million, if recognized, wou… |
| 2 | `TSLA_FY2016_2016-12-31:553` | Item 8 › Uncertain Tax Positions | ✓ | #1, #3, #4 | Accrued interest and penalties related to unrecognized tax benefits are classified as income tax expense and was immaterial. As of December 31, 2016, unrecognized tax benefits of $198.3 million, if recognized, would not … |
| 3 | `TSLA_FY2022_2022-12-31:462` | Item 8 › Note 14 – Income Taxes |  |  | \| \| Year Ended December 31, \| \| \| \|---\|---\|---\|---\| \| \| 2022 \| 2021 \| 2020 \| \| Tax at statutory federal rate \| $2,881 \| $1,332 \| $242 \| \| State tax, net of federal benefit \| 51 \| 6 \| 4 \| \| Nondeductible executive compens… |
| 4 | `TSLA_FY2016_2016-12-31:369` | Item 8 › Summary of Significant Accounting Policies |  |  | Marketing, promotional and advertising costs are expensed as incurred and are included as an element of selling, general and administrative expense in our Consolidated Statements of Operations. We incurred marketing, pro… |
| 5 | `TSLA_FY2022_2022-12-31:465` | Item 8 › Uncertain Tax Positions |  |  | The changes to our gross unrecognized tax benefits were as follows (in millions): |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#1 `TSLA_FY2022_2022-12-31:467`** (cited, gold #1, gold #2, gold #3, gold #4)

````text
ITEM 8. FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA > Uncertain Tax Positions
As of December 31, 2022, accrued interest and penalties related to unrecognized tax benefits are classified as income tax expense and amounted to $31 million. Unrecognized tax benefits of $572 million, if recognized, would not affect our effective tax rate since the tax benefits would increase a deferred tax asset that is currently fully offset by a valuation allowance. We file income tax returns in the U.S. and various state and foreign jurisdictions. We are currently under examination by the Internal Revenue Service (“IRS”) for the years 2015 to 2018. Additional tax years within the periods 2004 to 2014 and 2019 to 2021 remain subject to examination for federal income tax purposes. All net operating losses and tax credits generated to date are subject to adjustment for U.S. federal and state income tax purposes. Our returns for 2004 and subsequent tax years remain subject to examination in U.S. state and foreign jurisdictions. Given the uncertainty in timing and outcome of our tax examinations, an estimate of the range of the reasonably possible change in gross unrecognized tax benefits within twelve months cannot be made at this time.
````

**#2 `TSLA_FY2016_2016-12-31:553`** (cited, gold #1, gold #3, gold #4)

````text
ITEM 8. FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA > Uncertain Tax Positions
Accrued interest and penalties related to unrecognized tax benefits are classified as income tax expense and was immaterial. As of December 31, 2016, unrecognized tax benefits of $198.3 million, if recognized, would not affect our effective tax rate as the tax benefits would increase a deferred tax asset which is currently fully offset with a full valuation allowance. We do not anticipate that the amount of existing unrecognized tax benefits will significantly increase or decrease within the next 12 months. We file income tax returns in the United States, California, various states and foreign jurisdictions. Tax years 2003 to 2015 remain subject to examination for federal purposes, and tax years 2003 to 2015 remain subject to examination for California purposes. All net operating losses and tax credits generated to date are subject to adjustment for U.S. federal and California purposes. Tax years 2007 to 2015 remain open for examination in other U.S. state and foreign jurisdictions.
````

</details>

RQ2 citation match (section level): `cited=[('TSLA', 'Item 8')] gold=[(None, 'Item 8')]`

### System C v1 (adaptive multi-hop)

Model: `gpt-5.4`. Hops: 3. Chunks retrieved: 14, cited: 2.

**Generated answer**

> In fiscal year 2016, Tesla stated that unrecognized tax benefits of $198.3 million, if recognized, would not affect its effective tax rate because the tax benefits would increase a deferred tax asset that was currently fully offset with a full valuation allowance. [TSLA FY2016, Item 8, TSLA_FY2016_2016-12-31:553]
>
> In fiscal year 2022, Tesla gave the same core explanation, stating that unrecognized tax benefits of $572 million, if recognized, would not affect its effective tax rate because the tax benefits would increase a deferred tax asset that was currently fully offset by a valuation allowance. [TSLA FY2022, Item 8, TSLA_FY2022_2022-12-31:467]
>
> So, Tesla’s explanation did not materially change between 2016 and 2022; in both years, the reason was that recognition would increase a deferred tax asset that was fully offset by a valuation allowance, although the amount increased from $198.3 million to $572 million and the 2022 wording referred to “a valuation allowance” rather than “a full valuation allowance.” [TSLA FY2016, Item 8, TSLA_FY2016_2016-12-31:553] [TSLA FY2022, Item 8, TSLA_FY2022_2022-12-31:467]
>
> The 2022 filing specifically highlighted that Tesla was currently under examination by the Internal Revenue Service for the years 2015 to 2018. [TSLA FY2022, Item 8, TSLA_FY2022_2022-12-31:467]
>
> The 2022 filing also stated that additional tax years within the periods 2004 to 2014 and 2019 to 2021 remained subject to examination for federal income tax purposes. [TSLA FY2022, Item 8, TSLA_FY2022_2022-12-31:467]
>
> By contrast, the 2016 filing said only that tax years 2003 to 2015 remained subject to examination for federal purposes and California purposes, and that tax years 2007 to 2015 remained open for examination in other U.S. state and foreign jurisdictions, without mentioning an active IRS examination for 2015 to 2018. [TSLA FY2016, Item 8, TSLA_FY2016_2016-12-31:553]

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `TSLA_FY2016_2016-12-31:553` | Item 8 › Uncertain Tax Positions | ✓ | #1, #3, #4 | Accrued interest and penalties related to unrecognized tax benefits are classified as income tax expense and was immaterial. As of December 31, 2016, unrecognized tax benefits of $198.3 million, if recognized, would not … |
| 2 | `TSLA_FY2022_2022-12-31:467` | Item 8 › Uncertain Tax Positions | ✓ | #1, #2, #3, #4 | As of December 31, 2022, accrued interest and penalties related to unrecognized tax benefits are classified as income tax expense and amounted to $31 million. Unrecognized tax benefits of $572 million, if recognized, wou… |
| 3 | `TSLA_FY2016_2016-12-31:307` | Item 7 › Contractual Obligations |  |  | (5) Long-term debt reported above includes SolarCity’s total consolidated indebtedness of $3.58 billion as of December 31, 2016, representing outstanding recourse indebtedness of $1.62 billion and non-recourse indebtedne… |
| 4 | `TSLA_FY2016_2016-12-31:369` | Item 8 › Summary of Significant Accounting Policies |  |  | Marketing, promotional and advertising costs are expensed as incurred and are included as an element of selling, general and administrative expense in our Consolidated Statements of Operations. We incurred marketing, pro… |
| 5 | `TSLA_FY2016_2016-12-31:549` | Item 8 › Note 16 - Income Taxes |  | #3 | As of December 31, 2016, we had approximately $4.34 billion of federal and $3.01 billion of state net operating loss carry-forwards available to offset future taxable income, which will not begin to significantly expire … |
| 6 | `TSLA_FY2016_2016-12-31:551` | Item 8 › Uncertain Tax Positions |  |  | The aggregate changes in the balance of our gross unrecognized tax benefits during the years ended December 31, 2016, 2015 and 2014 were as follows (in thousands): |
| 7 | `TSLA_FY2022_2022-12-31:465` | Item 8 › Uncertain Tax Positions |  |  | The changes to our gross unrecognized tax benefits were as follows (in millions): |
| 8 | `TSLA_FY2022_2022-12-31:462` | Item 8 › Note 14 – Income Taxes |  |  | \| \| Year Ended December 31, \| \| \| \|---\|---\|---\|---\| \| \| 2022 \| 2021 \| 2020 \| \| Tax at statutory federal rate \| $2,881 \| $1,332 \| $242 \| \| State tax, net of federal benefit \| 51 \| 6 \| 4 \| \| Nondeductible executive compens… |
| 9 | `TSLA_FY2022_2022-12-31:454` | Item 8 › Note 14 – Income Taxes |  |  | \| \| Year Ended December 31, \| \| \| \|---\|---\|---\|---\| \| \| 2022 \| 2021 \| 2020 \| \| Domestic \| $5,524 \| $(130) \| $(198) \| \| Noncontrolling interest and redeemable noncontrolling interest \| 31 \| 125 \| 141 \| \| Foreign \| 8,164 \|… |
| 10 | `TSLA_FY2016_2016-12-31:251` | Item 7 › Critical Accounting Policies and Estimates |  |  | We are subject to federal and state taxes in the United States and in many foreign jurisdictions. Significant judgment is required in determining our provision for income taxes, our deferred tax assets and liabilities an… |
| 11 | `TSLA_FY2016_2016-12-31:547` | Item 8 › Note 16 - Income Taxes |  |  | \| \| Year Ended December 31, \| \| \| \|---\|---\|---\|---\| \| \| 2016 \| 2015 \| 2014 \| \| Tax at statutory federal rate \| $(261,222) \| $(306,470) \| $(99,622) \| \| State tax, net of federal benefit \| 568 \| 525 \| 257 \| \| Nondeductible… |
| 12 | `TSLA_FY2016_2016-12-31:540` | Item 8 › Note 16 - Income Taxes |  |  | \| \| Year Ended December 31, \| \| \| \|---\|---\|---\|---\| \| \| 2016 \| 2015 \| 2014 \| \| Domestic \| $130,718 \| $415,694 \| $60,451 \| \| Noncontrolling interest and redeemable noncontrolling interest \| 98,132 \| — \| — \| \| Foreign \| 51… |
| 13 | `TSLA_FY2016_2016-12-31:542` | Item 8 › Note 16 - Income Taxes |  |  | \| \| Year Ended December 31, \| \| \| \|---\|---\|---\|---\| \| \| 2016 \| 2015 \| 2014 \| \| Current: \| \| \| \| \| Federal \| $— \| $— \| $— \| \| State \| 568 \| 525 \| 257 \| \| Foreign \| 53,962 \| 10,342 \| 9,203 \| \| Total current \| 54,530 \| 10,8… |
| 14 | `TSLA_FY2016_2016-12-31:539` | Item 8 › Note 16 - Income Taxes |  |  | A provision for income taxes of $26.7 million, $13.0 million and $9.4 million has been recognized for the years ended December 31, 2016, 2015 and 2014, respectively, related primarily to our subsidiaries located outside … |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#1 `TSLA_FY2016_2016-12-31:553`** (cited, gold #1, gold #3, gold #4)

````text
ITEM 8. FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA > Uncertain Tax Positions
Accrued interest and penalties related to unrecognized tax benefits are classified as income tax expense and was immaterial. As of December 31, 2016, unrecognized tax benefits of $198.3 million, if recognized, would not affect our effective tax rate as the tax benefits would increase a deferred tax asset which is currently fully offset with a full valuation allowance. We do not anticipate that the amount of existing unrecognized tax benefits will significantly increase or decrease within the next 12 months. We file income tax returns in the United States, California, various states and foreign jurisdictions. Tax years 2003 to 2015 remain subject to examination for federal purposes, and tax years 2003 to 2015 remain subject to examination for California purposes. All net operating losses and tax credits generated to date are subject to adjustment for U.S. federal and California purposes. Tax years 2007 to 2015 remain open for examination in other U.S. state and foreign jurisdictions.
````

**#2 `TSLA_FY2022_2022-12-31:467`** (cited, gold #1, gold #2, gold #3, gold #4)

````text
ITEM 8. FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA > Uncertain Tax Positions
As of December 31, 2022, accrued interest and penalties related to unrecognized tax benefits are classified as income tax expense and amounted to $31 million. Unrecognized tax benefits of $572 million, if recognized, would not affect our effective tax rate since the tax benefits would increase a deferred tax asset that is currently fully offset by a valuation allowance. We file income tax returns in the U.S. and various state and foreign jurisdictions. We are currently under examination by the Internal Revenue Service (“IRS”) for the years 2015 to 2018. Additional tax years within the periods 2004 to 2014 and 2019 to 2021 remain subject to examination for federal income tax purposes. All net operating losses and tax credits generated to date are subject to adjustment for U.S. federal and state income tax purposes. Our returns for 2004 and subsequent tax years remain subject to examination in U.S. state and foreign jurisdictions. Given the uncertainty in timing and outcome of our tax examinations, an estimate of the range of the reasonably possible change in gross unrecognized tax benefits within twelve months cannot be made at this time.
````

**#5 `TSLA_FY2016_2016-12-31:549`** (gold #3)

````text
ITEM 8. FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA > Note 16 - Income Taxes
As of December 31, 2016, we had approximately $4.34 billion of federal and $3.01 billion of state net operating loss carry-forwards available to offset future taxable income, which will not begin to significantly expire until 2024 for federal and 2017 for state purposes. A portion of these losses were generated by SolarCity prior to our acquisition and therefore are subject to change of control provisions which limit the amount of acquired tax attributes that can be utilized in a given tax year. We do not expect these change of control limitations to significantly impact our ability to utilize these attributes. The portion of net operating loss carryforwards related to stock options is approximately $2.39 billion and $1.42 billion for federal and state purposes, respectively, of which the tax benefits will be credited to additional paid-in capital when realized. Upon the adoption of ASU No. 2016-09, all tax effects related to share-based payments will be recognized through earnings, subject to normal valuation allowance considerations. We expect that any potential tax benefits, upon adoption of ASU No. 2016-09, would increase our deferred tax asset which would be offset with a full valuation allowance.
````

</details>

RQ2 citation match (section level): `cited=[('TSLA', 'Item 8')] gold=[(None, 'Item 8')]`

**System C guardrail** (judge `gpt-5.4`): numerical claims 4, verified 4, ungrounded 0, uncited 0, derived 0; sentence verdicts: supported 3, partial 0, unsupported 0, unchecked 0.


<details><summary>Guardrail sentence verdicts</summary>

| sentence | verdict | judge reason |
|---|---|---|
| In fiscal year 2016, Tesla stated that unrecognized tax benefits of $198.3 million, if recognized, would not affect its effective tax rate because the tax benefits would increase a deferred tax asset that was currently fully offset with a full valuation allowance. [TSLA FY2016, Item 8, TSLA_FY2016_2016-12-31:553] | None |  |
| In fiscal year 2022, Tesla gave the same core explanation, stating that unrecognized tax benefits of $572 million, if recognized, would not affect its effective tax rate because the tax benefits would increase a deferred tax asset that was currently fully offset by a valuation allowance. [TSLA FY2022, Item 8, TSLA_FY2022_2022-12-31:467] | None |  |
| So, Tesla’s explanation did not materially change between 2016 and 2022; in both years, the reason was that recognition would increase a deferred tax asset that was fully offset by a valuation allowance, although the amount increased from $198.3 million to $572 million and the 2022 wording referred to “a valuation allowance” rather than “a full valuation allowance.” [TSLA FY2016, Item 8, TSLA_FY2016_2016-12-31:553] [TSLA FY2022, Item 8, TSLA_FY2022_2022-12-31:467] | None |  |
| The 2022 filing specifically highlighted that Tesla was currently under examination by the Internal Revenue Service for the years 2015 to 2018. [TSLA FY2022, Item 8, TSLA_FY2022_2022-12-31:467] | supported | The cited text explicitly says Tesla was under IRS examination for the years 2015 to 2018 as of December 31, 2022. |
| The 2022 filing also stated that additional tax years within the periods 2004 to 2014 and 2019 to 2021 remained subject to examination for federal income tax purposes. [TSLA FY2022, Item 8, TSLA_FY2022_2022-12-31:467] | supported | The cited text states that additional tax years 2004 to 2014 and 2019 to 2021 remained subject to examination for federal income tax purposes. |
| By contrast, the 2016 filing said only that tax years 2003 to 2015 remained subject to examination for federal purposes and California purposes, and that tax years 2007 to 2015 remained open for examination in other U.S. state and foreign jurisdictions, without mentioning an active IRS examination for 2015 to 2018. [TSLA FY2016, Item 8, TSLA_FY2016_2016-12-31:553] | supported | The 2016 evidence lists only the open examination years and jurisdictions described and does not mention any active IRS examination for 2015 to 2018. |

</details>

### System C v2 (agentic multi-hop + XBRL)

Model: `gpt-5.4`. Hops: 3. Chunks retrieved: 12, cited: 2.

**Generated answer**

> In fiscal year 2016, Tesla said that unrecognized tax benefits of $198.3 million, if recognized, would not affect its effective tax rate because the tax benefits would increase a deferred tax asset that was currently fully offset with a full valuation allowance. [TSLA FY2016, Item 8, TSLA_FY2016_2016-12-31:553]
>
> In fiscal year 2022, Tesla gave the same basic explanation, stating that unrecognized tax benefits of $572 million, if recognized, would not affect its effective tax rate because the tax benefits would increase a deferred tax asset that was currently fully offset by a valuation allowance. [TSLA FY2022, Item 8, TSLA_FY2022_2022-12-31:467]
>
> So, the explanation did not materially change between 2016 and 2022; it remained that recognition would increase a deferred tax asset that was fully offset by a valuation allowance, although the 2022 filing used the phrasing “fully offset by a valuation allowance” rather than “fully offset with a full valuation allowance.” [TSLA FY2016, Item 8, TSLA_FY2016_2016-12-31:553] [TSLA FY2022, Item 8, TSLA_FY2022_2022-12-31:467]
>
> The 2022 filing specifically highlighted that Tesla was currently under examination by the Internal Revenue Service for the years 2015 to 2018. [TSLA FY2022, Item 8, TSLA_FY2022_2022-12-31:467]
>
> It also stated that additional tax years within the periods 2004 to 2014 and 2019 to 2021 remained subject to examination for federal income tax purposes. [TSLA FY2022, Item 8, TSLA_FY2022_2022-12-31:467]
>
> By contrast, the 2016 filing said only that tax years 2003 to 2015 remained subject to examination for federal purposes, tax years 2003 to 2015 remained subject to examination for California purposes, and tax years 2007 to 2015 remained open for examination in other U.S. state and foreign jurisdictions, without mentioning a current IRS examination for 2015 to 2018. [TSLA FY2016, Item 8, TSLA_FY2016_2016-12-31:553]

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `TSLA_FY2016_2016-12-31:553` | Item 8 › Uncertain Tax Positions | ✓ | #1, #3, #4 | Accrued interest and penalties related to unrecognized tax benefits are classified as income tax expense and was immaterial. As of December 31, 2016, unrecognized tax benefits of $198.3 million, if recognized, would not … |
| 2 | `TSLA_FY2022_2022-12-31:467` | Item 8 › Uncertain Tax Positions | ✓ | #1, #2, #3, #4 | As of December 31, 2022, accrued interest and penalties related to unrecognized tax benefits are classified as income tax expense and amounted to $31 million. Unrecognized tax benefits of $572 million, if recognized, wou… |
| 3 | `TSLA_FY2016_2016-12-31:307` | Item 7 › Contractual Obligations |  |  | (5) Long-term debt reported above includes SolarCity’s total consolidated indebtedness of $3.58 billion as of December 31, 2016, representing outstanding recourse indebtedness of $1.62 billion and non-recourse indebtedne… |
| 4 | `TSLA_FY2016_2016-12-31:369` | Item 8 › Summary of Significant Accounting Policies |  |  | Marketing, promotional and advertising costs are expensed as incurred and are included as an element of selling, general and administrative expense in our Consolidated Statements of Operations. We incurred marketing, pro… |
| 5 | `TSLA_FY2016_2016-12-31:549` | Item 8 › Note 16 - Income Taxes |  | #3 | As of December 31, 2016, we had approximately $4.34 billion of federal and $3.01 billion of state net operating loss carry-forwards available to offset future taxable income, which will not begin to significantly expire … |
| 6 | `TSLA_FY2016_2016-12-31:551` | Item 8 › Uncertain Tax Positions |  |  | The aggregate changes in the balance of our gross unrecognized tax benefits during the years ended December 31, 2016, 2015 and 2014 were as follows (in thousands): |
| 7 | `TSLA_FY2016_2016-12-31:252` | Item 7 › Critical Accounting Policies and Estimates |  |  | Furthermore, significant judgment is required in evaluating our tax positions. In the ordinary course of business, there are many transactions and calculations for which the ultimate tax settlement is uncertain. As a res… |
| 8 | `TSLA_FY2016_2016-12-31:207` | Item 6 |  |  | The following selected consolidated financial data should be read in conjunction with “Management’s Discussion and Analysis of Financial Condition and Results of Operations” and our consolidated financial statements and … |
| 9 | `TSLA_FY2016_2016-12-31:209` | Item 6 |  |  | (1) Diluted net loss per share of common stock is computed excluding common stock subject to repurchase, and, if dilutive, potential shares of common stock outstanding during the period. Potential shares of common stock … |
| 10 | `TSLA_FY2016_2016-12-31:210` | Item 6 |  |  | (2) We acquired SolarCity on November 21, 2016. The results of SolarCity have been included in our results of operation from the date of acquisition. See Note 3, Acquisition of SolarCity, of the Notes to Consolidated Fin… |
| 11 | `TSLA_FY2016_2016-12-31:213` | Item 6 |  |  | amount of 2021 Notes, pursuant to the exercise in full of the overallotment options of the underwriters of our March 2014 public offering. In accordance with accounting guidance on embedded conversion features, we valued… |
| 12 | `TSLA_FY2022_2022-12-31:465` | Item 8 › Uncertain Tax Positions |  |  | The changes to our gross unrecognized tax benefits were as follows (in millions): |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#1 `TSLA_FY2016_2016-12-31:553`** (cited, gold #1, gold #3, gold #4)

````text
ITEM 8. FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA > Uncertain Tax Positions
Accrued interest and penalties related to unrecognized tax benefits are classified as income tax expense and was immaterial. As of December 31, 2016, unrecognized tax benefits of $198.3 million, if recognized, would not affect our effective tax rate as the tax benefits would increase a deferred tax asset which is currently fully offset with a full valuation allowance. We do not anticipate that the amount of existing unrecognized tax benefits will significantly increase or decrease within the next 12 months. We file income tax returns in the United States, California, various states and foreign jurisdictions. Tax years 2003 to 2015 remain subject to examination for federal purposes, and tax years 2003 to 2015 remain subject to examination for California purposes. All net operating losses and tax credits generated to date are subject to adjustment for U.S. federal and California purposes. Tax years 2007 to 2015 remain open for examination in other U.S. state and foreign jurisdictions.
````

**#2 `TSLA_FY2022_2022-12-31:467`** (cited, gold #1, gold #2, gold #3, gold #4)

````text
ITEM 8. FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA > Uncertain Tax Positions
As of December 31, 2022, accrued interest and penalties related to unrecognized tax benefits are classified as income tax expense and amounted to $31 million. Unrecognized tax benefits of $572 million, if recognized, would not affect our effective tax rate since the tax benefits would increase a deferred tax asset that is currently fully offset by a valuation allowance. We file income tax returns in the U.S. and various state and foreign jurisdictions. We are currently under examination by the Internal Revenue Service (“IRS”) for the years 2015 to 2018. Additional tax years within the periods 2004 to 2014 and 2019 to 2021 remain subject to examination for federal income tax purposes. All net operating losses and tax credits generated to date are subject to adjustment for U.S. federal and state income tax purposes. Our returns for 2004 and subsequent tax years remain subject to examination in U.S. state and foreign jurisdictions. Given the uncertainty in timing and outcome of our tax examinations, an estimate of the range of the reasonably possible change in gross unrecognized tax benefits within twelve months cannot be made at this time.
````

**#5 `TSLA_FY2016_2016-12-31:549`** (gold #3)

````text
ITEM 8. FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA > Note 16 - Income Taxes
As of December 31, 2016, we had approximately $4.34 billion of federal and $3.01 billion of state net operating loss carry-forwards available to offset future taxable income, which will not begin to significantly expire until 2024 for federal and 2017 for state purposes. A portion of these losses were generated by SolarCity prior to our acquisition and therefore are subject to change of control provisions which limit the amount of acquired tax attributes that can be utilized in a given tax year. We do not expect these change of control limitations to significantly impact our ability to utilize these attributes. The portion of net operating loss carryforwards related to stock options is approximately $2.39 billion and $1.42 billion for federal and state purposes, respectively, of which the tax benefits will be credited to additional paid-in capital when realized. Upon the adoption of ASU No. 2016-09, all tax effects related to share-based payments will be recognized through earnings, subject to normal valuation allowance considerations. We expect that any potential tax benefits, upon adoption of ASU No. 2016-09, would increase our deferred tax asset which would be offset with a full valuation allowance.
````

</details>

RQ2 citation match (section level): `cited=[('TSLA', 'Item 8')] gold=[(None, 'Item 8')]`

**System C guardrail** (judge `gpt-5.4`): numerical claims 2, verified 2, ungrounded 0, uncited 0, derived 0; sentence verdicts: supported 4, partial 0, unsupported 0, unchecked 0.


<details><summary>Guardrail sentence verdicts</summary>

| sentence | verdict | judge reason |
|---|---|---|
| In fiscal year 2016, Tesla said that unrecognized tax benefits of $198.3 million, if recognized, would not affect its effective tax rate because the tax benefits would increase a deferred tax asset that was currently fully offset with a full valuation allowance. [TSLA FY2016, Item 8, TSLA_FY2016_2016-12-31:553] | None |  |
| In fiscal year 2022, Tesla gave the same basic explanation, stating that unrecognized tax benefits of $572 million, if recognized, would not affect its effective tax rate because the tax benefits would increase a deferred tax asset that was currently fully offset by a valuation allowance. [TSLA FY2022, Item 8, TSLA_FY2022_2022-12-31:467] | None |  |
| So, the explanation did not materially change between 2016 and 2022; it remained that recognition would increase a deferred tax asset that was fully offset by a valuation allowance, although the 2022 filing used the phrasing “fully offset by a valuation allowance” rather than “fully offset with a full valuation allowance.” [TSLA FY2016, Item 8, TSLA_FY2016_2016-12-31:553] [TSLA FY2022, Item 8, TSLA_FY2022_2022-12-31:467] | supported | Both excerpts say recognition would increase a deferred tax asset offset by a valuation allowance, with the quoted wording difference shown. |
| The 2022 filing specifically highlighted that Tesla was currently under examination by the Internal Revenue Service for the years 2015 to 2018. [TSLA FY2022, Item 8, TSLA_FY2022_2022-12-31:467] | supported | The 2022 excerpt explicitly says Tesla was under IRS examination for 2015 to 2018. |
| It also stated that additional tax years within the periods 2004 to 2014 and 2019 to 2021 remained subject to examination for federal income tax purposes. [TSLA FY2022, Item 8, TSLA_FY2022_2022-12-31:467] | supported | The 2022 excerpt explicitly states additional tax years 2004 to 2014 and 2019 to 2021 remained subject to federal examination. |
| By contrast, the 2016 filing said only that tax years 2003 to 2015 remained subject to examination for federal purposes, tax years 2003 to 2015 remained subject to examination for California purposes, and tax years 2007 to 2015 remained open for examination in other U.S. state and foreign jurisdictions, without mentioning a current IRS examination for 2015 to 2018. [TSLA FY2016, Item 8, TSLA_FY2016_2016-12-31:553] | supported | The 2016 excerpt lists those examination periods and does not mention a current IRS examination for 2015 to 2018. |

</details>
