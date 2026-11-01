# gold-034: Table + text (one filing)

[← all cases](../README.md) · company: Meta Platforms, Inc. (META) · fiscal year: 2020 · recipe `table_text` · hop `multi` · answer type `mixed` · scope `single_doc` · RQ2 category `cross_section_multihop`

## Gold QA

**Question**

> What was the year-over-year percentage change in Meta Platforms, Inc.'s domestic income before provision for income taxes from fiscal year 2019 to fiscal year 2020, and how does the company characterize the volatility and drivers of its future income tax rates in its risk factors?

**Gold answer**

> 355.77%. Meta says its future income tax rates could be volatile and difficult to predict due to changes in jurisdictional profit split, changes in the amount and recognition of deferred tax assets and liabilities, or changes in tax laws, regulations, or accounting principles.

**Program**: `subtract(24233, 5317), divide(#0, 5317)` → `3.5576452886966337`

**Gold numbers** (RQ2 numeric_accuracy targets): 355.77%

**Key points** (RQ3 keypoint_recall targets)

1. Domestic income before provision for income taxes rose from $5,317 million to $24,233 million, an increase of 355.77%.
2. Future income tax rates could be volatile and difficult to predict.
3. Drivers include changes in jurisdictional profit split, deferred tax assets and liabilities, and tax laws, regulations or accounting principles.

**Gold evidence**

1. `META_FY2020_2020-12-31` · Item 8.Financial Statements and Supplementary Data › Note 15. Income Taxes · table

   > | Domestic | $24,233 | $5,317 | $8,800 |

2. `META_FY2020_2020-12-31` · Item 1A.Risk Factors › We may have exposure to greater than anticipated tax liabilities. · text

   > Our future income tax rates could be volatile and difficult to predict due to changes in jurisdictional profit split, changes in the amount and recognition of deferred tax assets and liabilities, or by changes in tax laws, regulations, or accounting principles.

## Scorecard

| Metric | A (vanilla dense) | B (hybrid + rerank) | C v1 (adaptive multi-hop) | C v2 (agentic multi-hop + XBRL) |
|---|---|---|---|---|
| **Retrieval (RQ1)** | | | | |
| chunks retrieved | 10 | 5 | 12 | 13 |
| recall@5 | 0.50 | 0.50 | 0.50 | 0.50 |
| recall@all | 0.50 | 0.50 | 1.00 | 0.50 |
| complete@all | 0 | 0 | 1 | 0 |
| average precision (lexical) | 1.00 | 1.00 | 0.60 | 0.50 |
| gold evidence first rank | #1: 1, #2: – | #1: –, #2: 1 | #1: 1, #2: 10 | #1: 2, #2: – |
| **Answer (RQ3 string match)** | | | | |
| numeric_correct | ✓ | ✗ | ✓ | ✓ |
| keypoint_recall | 0.67 | 0.00 | 1.00 | 0.67 |
| **Answer & citations (RQ2)** | | | | |
| numeric_accuracy | 1.00 | 0.00 | 1.00 | 1.00 |
| citation precision | 1.00 | – | 1.00 | 1.00 |
| citation recall | 0.50 | – | 1.00 | 1.00 |
| citation F1 | 0.67 | – | 1.00 | 1.00 |
| has a citation | 1 | 0 | 1 | 1 |
| grounding error rate | – | – | 0.00 | 0.00 |
| **Cost (RQ3)** | | | | |
| retrieval hops | 1 | 1 | 2 | 2 |
| tokens | 2110 | 1360 | 10606 | 10954 |
| cost (USD) | 0.0004 | 0.0002 | 0.0405 | 0.0415 |
| latency (s) | 3.2 | 6.0 | 19.7 | 19.9 |

Definitions: [README › Metrics](../README.md#metrics). `–` = not applicable (e.g. no gold number, no citations, no guardrail).

## System outputs

### System A (vanilla dense)

Model: `gpt-5.4-2026-03-05`. Hops: 1. Chunks retrieved: 10, cited: 2.

**Generated answer**

> Meta’s domestic income before provision for income taxes increased from **$5,317 million in 2019** to **$24,233 million in 2020** [1].
>
> Year-over-year percentage change:
>
> \[
> \frac{24,233 - 5,317}{5,317} \times 100 \approx 355.8\%
> \]
>
> So, the domestic income before provision for income taxes **increased by about 356%** from 2019 to 2020 [1].
>
> As for **how the company characterizes the volatility and drivers of its future income tax rates in its risk factors**, that information is **not provided in the context**. The only related risk-factor-style statement in the context says tax matters “**could have a material impact on our financial condition and operating results**,” but it does not describe the volatility or specific drivers of future income tax rates [8].

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `META_FY2020_2020-12-31:511` | Item 8 › Note 15. Income Taxes | ✓ | #1 | \| \| Year Ended December 31, \| \| \| \|---\|---\|---\|---\| \| \| 2020 \| 2019 \| 2018 \| \| Domestic \| $24,233 \| $5,317 \| $8,800 \| \| Foreign \| 8,947 \| 19,495 \| 16,561 \| \| Income before provision for income taxes \| $33,180 \| $24,812 \|… |
| 2 | `META_FY2020_2020-12-31:312` | Item 7 › Provision for income taxes |  |  | \| \| Year Ended December 31, \| \| \| \| \| \|---\|---\|---\|---\|---\|---\| \| \| 2020 \| 2019 \| 2018 \| 2020 vs 2019 % Change \| 2019 vs 2018 % Change \| \| \| (dollars in millions) \| \| \| \| \| \| Provision for income taxes \| $4,034 \| $6,327 … |
| 3 | `META_FY2020_2020-12-31:313` | Item 7 › Provision for income taxes |  |  | 2020 Compared to 2019. Our provision for income taxes in 2020 decreased $2.29 billion, or 36%, compared to 2019, mostly due to the additional tax expense incurred in 2019 from the Altera Ninth Circuit Opinion and the eff… |
| 4 | `META_FY2020_2020-12-31:515` | Item 8 › Note 15. Income Taxes |  |  | \| \| Year Ended December 31, \| \| \| \|---\|---\|---\|---\| \| \| 2020 \| 2019 \| 2018 \| \| U.S. federal statutory income tax rate \| 21.0% \| 21.0% \| 21.0% \| \| State income taxes, net of federal benefit \| 0.8 \| 1.8 \| 0.7 \| \| Research … |
| 5 | `META_FY2020_2020-12-31:512` | Item 8 › Note 15. Income Taxes |  |  | The provision for income taxes consisted of the following (in millions): |
| 6 | `META_FY2020_2020-12-31:510` | Item 8 › Note 15. Income Taxes |  |  | The components of income before provision for income taxes are as follows (in millions): |
| 7 | `META_FY2020_2020-12-31:513` | Item 8 › Note 15. Income Taxes |  |  | \| \| Year Ended December 31, \| \| \| \|---\|---\|---\|---\| \| \| 2020 \| 2019 \| 2018 \| \| Current: \| \| \| \| \| Federal \| $3,297 \| $4,321 \| $1,747 \| \| State \| 523 \| 565 \| 176 \| \| Foreign \| 1,211 \| 1,481 \| 1,031 \| \| Total current tax e… |
| 8 | `META_FY2020_2020-12-31:413` | Item 8 › Income Taxes | ✓ |  | and could have a material impact on our financial condition and operating results. |
| 9 | `META_FY2020_2020-12-31:517` | Item 8 › Note 15. Income Taxes |  |  | \| \| December 31, \| \| \|---\|---\|---\| \| \| 2020 \| 2019 \| \| Deferred tax assets: \| \| \| \| Net operating loss carryforward \| $2,437 \| $2,051 \| \| Tax credit carryforward \| 1,055 \| 1,333 \| \| Share-based compensation \| 243 \| 135 \|… |
| 10 | `META_FY2020_2020-12-31:310` | Item 7 › Interest and other income, net |  |  | \| \| Year Ended December 31, \| \| \| \| \| \|---\|---\|---\|---\|---\|---\| \| \| 2020 \| 2019 \| 2018 \| 2020 vs 2019 % Change \| 2019 vs 2018 % Change \| \| \| (in millions) \| \| \| \| \| \| Interest income, net \| $672 \| $904 \| $652 \| (26)% \| 3… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#1 `META_FY2020_2020-12-31:511`** (cited, gold #1)

````text
Item 8.Financial Statements and Supplementary Data > Note 15. Income Taxes (table)
|  | Year Ended December 31, |  |  |
|---|---|---|---|
|  | 2020 | 2019 | 2018 |
| Domestic | $24,233 | $5,317 | $8,800 |
| Foreign | 8,947 | 19,495 | 16,561 |
| Income before provision for income taxes | $33,180 | $24,812 | $25,361 |
````

**#8 `META_FY2020_2020-12-31:413`** (cited)

````text
Item 8.Financial Statements and Supplementary Data > Income Taxes
and could have a material impact on our financial condition and operating results.
````

</details>

RQ2 citation match (section level): `cited=[('META', 'Item 8')] gold=[(None, 'Item 8'), (None, 'Item 1A')]`

### System B (hybrid + rerank)

Model: `gpt-5.4-2026-03-05`. Hops: 1. Chunks retrieved: 5, cited: 0.

**Generated answer**

> Not found in the provided context.

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `META_FY2020_2020-12-31:147` | Item 1A › We may have exposure to greater than anticipated tax liabilities. |  | #2 | IRS's position and are litigating this issue, the ultimate resolution is uncertain and, if resolved in a manner unfavorable to us, may adversely affect our financial results. The determination of our worldwide provision … |
| 2 | `META_FY2020_2020-12-31:149` | Item 1A › Changes in tax laws or tax rulings could materially affect our financial position, results of operations, and cash flows. |  |  | The Organization for Economic Cooperation and Development has been working on a Base Erosion and Profit Shifting Project, and issued a report in 2015, an interim report in 2018, and blueprints in 2020 that, if implemente… |
| 3 | `META_FY2020_2020-12-31:312` | Item 7 › Provision for income taxes |  |  | \| \| Year Ended December 31, \| \| \| \| \| \|---\|---\|---\|---\|---\|---\| \| \| 2020 \| 2019 \| 2018 \| 2020 vs 2019 % Change \| 2019 vs 2018 % Change \| \| \| (dollars in millions) \| \| \| \| \| \| Provision for income taxes \| $4,034 \| $6,327 … |
| 4 | `META_FY2020_2020-12-31:377` | Item 8 › CONSOLIDATED STATEMENTS OF INCOME |  |  | \| \| Year Ended December 31, \| \| \| \|---\|---\|---\|---\| \| \| 2020 \| 2019 \| 2018 \| \| Revenue \| $85,965 \| $70,697 \| $55,838 \| \| Costs and expenses: \| \| \| \| \| Cost of revenue \| 16,692 \| 12,770 \| 9,355 \| \| Research and developmen… |
| 5 | `META_FY2020_2020-12-31:313` | Item 7 › Provision for income taxes |  |  | 2020 Compared to 2019. Our provision for income taxes in 2020 decreased $2.29 billion, or 36%, compared to 2019, mostly due to the additional tax expense incurred in 2019 from the Altera Ninth Circuit Opinion and the eff… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#1 `META_FY2020_2020-12-31:147`** (gold #2)

````text
Item 1A.Risk Factors > We may have exposure to greater than anticipated tax liabilities.
IRS's position and are litigating this issue, the ultimate resolution is uncertain and, if resolved in a manner unfavorable to us, may adversely affect our financial results. The determination of our worldwide provision for income taxes and other tax liabilities requires significant judgment by management, and there are many transactions where the ultimate tax determination is uncertain. Our provision for income taxes is determined by the manner in which we operate our business, and any changes to such operations or laws applicable to such operations may affect our effective tax rate. Although we believe that our provision for income taxes and estimates of our non-income tax liabilities are reasonable, the ultimate settlement may differ from the amounts recorded in our financial statements and may materially affect our financial results in the period or periods for which such determination is made. Our future income tax rates could be volatile and difficult to predict due to changes in jurisdictional profit split, changes in the amount and recognition of deferred tax assets and liabilities, or by changes in tax laws, regulations, or accounting principles.
````

</details>

RQ2 citation match (section level): `no citations`

### System C v1 (adaptive multi-hop)

Model: `gpt-5.4`. Hops: 2. Chunks retrieved: 12, cited: 4.

**Generated answer**

> Meta Platforms, Inc.'s domestic income before provision for income taxes increased from $5,317 million in 2019 to $24,233 million in 2020, which was a year-over-year increase of approximately 356% [META FY2020, Item 8, META_FY2020_2020-12-31:511].  
>
> The company characterizes its future income tax rates as potentially volatile and difficult to predict [META FY2020, Item 1A, META_FY2020_2020-12-31:147].  
>
> In its risk factors, the company says its overall tax rate is affected by the mix of income it earns in the U.S. and in jurisdictions with different tax rates, the effects of share-based compensation, the effects of integrating intellectual property from acquisitions, the effects of changes in its business or structure, and the effects of discrete items such as legal and tax settlements and tax elections [META FY2020, Item 1A, META_FY2020_2020-12-31:105].  
>
> The company also says its future income tax rates could be volatile and difficult to predict due to changes in jurisdictional profit split, changes in the amount and recognition of deferred tax assets and liabilities, or changes in tax laws, regulations, or accounting principles [META FY2020, Item 1A, META_FY2020_2020-12-31:147].  
>
> It further warns that changes in tax laws or tax rulings, or changes in interpretations of existing laws, could materially affect its financial position, results of operations, and cash flows, and that new laws in Europe and other countries could significantly increase its tax obligations or require changes in how it operates its business [META FY2020, Item 1A, META_FY2020_2020-12-31:148].

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `META_FY2020_2020-12-31:511` | Item 8 › Note 15. Income Taxes | ✓ | #1 | \| \| Year Ended December 31, \| \| \| \|---\|---\|---\|---\| \| \| 2020 \| 2019 \| 2018 \| \| Domestic \| $24,233 \| $5,317 \| $8,800 \| \| Foreign \| 8,947 \| 19,495 \| 16,561 \| \| Income before provision for income taxes \| $33,180 \| $24,812 \|… |
| 2 | `META_FY2020_2020-12-31:510` | Item 8 › Note 15. Income Taxes |  |  | The components of income before provision for income taxes are as follows (in millions): |
| 3 | `META_FY2020_2020-12-31:313` | Item 7 › Provision for income taxes |  |  | 2020 Compared to 2019. Our provision for income taxes in 2020 decreased $2.29 billion, or 36%, compared to 2019, mostly due to the additional tax expense incurred in 2019 from the Altera Ninth Circuit Opinion and the eff… |
| 4 | `META_FY2020_2020-12-31:320` | Item 7 › Provision for income taxes |  |  | We have previously accrued an estimated unrecognized tax benefit consistent with the guidance in ASC 740, Income Taxes, that is lower than the potential additional federal tax liability from the positions taken by the IR… |
| 5 | `META_FY2020_2020-12-31:512` | Item 8 › Note 15. Income Taxes |  |  | The provision for income taxes consisted of the following (in millions): |
| 6 | `META_FY2020_2020-12-31:312` | Item 7 › Provision for income taxes |  |  | \| \| Year Ended December 31, \| \| \| \| \| \|---\|---\|---\|---\|---\|---\| \| \| 2020 \| 2019 \| 2018 \| 2020 vs 2019 % Change \| 2019 vs 2018 % Change \| \| \| (dollars in millions) \| \| \| \| \| \| Provision for income taxes \| $4,034 \| $6,327 … |
| 7 | `META_FY2020_2020-12-31:151` | Item 1A › Given our levels of share-based compensation, our tax rate may vary significantly depending on our stock price. |  |  | The tax effects of the accounting for share-based compensation may significantly impact our effective tax rate from period to period. In periods in which our stock price is higher than the grant price of the share-based … |
| 8 | `META_FY2020_2020-12-31:105` | Item 1A › Our financial results will fluctuate from quarter to quarter and are difficult to predict. | ✓ |  | •the overall tax rate for our business, which is affected by the mix of income we earn in the U.S. and in jurisdictions with different tax rates, the effects of share-based compensation, the effects of integrating intell… |
| 9 | `META_FY2020_2020-12-31:316` | Item 7 › Provision for income taxes |  |  | Effective Tax Rate Items. Our effective tax rate in the future will depend upon the proportion between the following items and income before provision for income taxes: U.S. tax benefits from foreign derived intangible i… |
| 10 | `META_FY2020_2020-12-31:147` | Item 1A › We may have exposure to greater than anticipated tax liabilities. | ✓ | #2 | IRS's position and are litigating this issue, the ultimate resolution is uncertain and, if resolved in a manner unfavorable to us, may adversely affect our financial results. The determination of our worldwide provision … |
| 11 | `META_FY2020_2020-12-31:148` | Item 1A › Changes in tax laws or tax rulings could materially affect our financial position, results of operations, and cash flows. | ✓ |  | The tax regimes we are subject to or operate under, including income and non-income taxes, are unsettled and may be subject to significant change. Changes in tax laws or tax rulings, or changes in interpretations of exis… |
| 12 | `META_FY2020_2020-12-31:410` | Item 8 › Income Taxes |  |  | We are subject to income taxes in the United States and numerous foreign jurisdictions. Significant judgment is required in determining our provision for income taxes and income tax assets and liabilities, including eval… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#1 `META_FY2020_2020-12-31:511`** (cited, gold #1)

````text
Item 8.Financial Statements and Supplementary Data > Note 15. Income Taxes (table)
|  | Year Ended December 31, |  |  |
|---|---|---|---|
|  | 2020 | 2019 | 2018 |
| Domestic | $24,233 | $5,317 | $8,800 |
| Foreign | 8,947 | 19,495 | 16,561 |
| Income before provision for income taxes | $33,180 | $24,812 | $25,361 |
````

**#8 `META_FY2020_2020-12-31:105`** (cited)

````text
Item 1A.Risk Factors > Our financial results will fluctuate from quarter to quarter and are difficult to predict.
•the overall tax rate for our business, which is affected by the mix of income we earn in the U.S. and in jurisdictions with different tax rates, the effects of share-based compensation, the effects of integrating intellectual property from acquisitions, the effects of changes in our business or structure, and the effects of discrete items such as legal and tax settlements and tax elections; •the impact of changes in tax laws or judicial or regulatory interpretations of tax laws, which are recorded in the period such laws are enacted or interpretations are issued, and may significantly affect the effective tax rate of that period; •tax obligations that may arise from resolutions of tax examinations, including the examination we are currently under by the Internal Revenue Service (IRS), that materially differ from the amounts we have anticipated; •fluctuations in currency exchange rates and changes in the proportion of our revenue and expenses denominated in foreign currencies; •trading activity in our share repurchase program; •fluctuations in the market values of our investments in marketable securities, in the valuation of our equity investments, and in interest rates; •changes in U.S. generally accepted accounting principles; and
````

**#10 `META_FY2020_2020-12-31:147`** (cited, gold #2)

````text
Item 1A.Risk Factors > We may have exposure to greater than anticipated tax liabilities.
IRS's position and are litigating this issue, the ultimate resolution is uncertain and, if resolved in a manner unfavorable to us, may adversely affect our financial results. The determination of our worldwide provision for income taxes and other tax liabilities requires significant judgment by management, and there are many transactions where the ultimate tax determination is uncertain. Our provision for income taxes is determined by the manner in which we operate our business, and any changes to such operations or laws applicable to such operations may affect our effective tax rate. Although we believe that our provision for income taxes and estimates of our non-income tax liabilities are reasonable, the ultimate settlement may differ from the amounts recorded in our financial statements and may materially affect our financial results in the period or periods for which such determination is made. Our future income tax rates could be volatile and difficult to predict due to changes in jurisdictional profit split, changes in the amount and recognition of deferred tax assets and liabilities, or by changes in tax laws, regulations, or accounting principles.
````

**#11 `META_FY2020_2020-12-31:148`** (cited)

````text
Item 1A.Risk Factors > Changes in tax laws or tax rulings could materially affect our financial position, results of operations, and cash flows.
The tax regimes we are subject to or operate under, including income and non-income taxes, are unsettled and may be subject to significant change. Changes in tax laws or tax rulings, or changes in interpretations of existing laws, could materially affect our financial position, results of operations, and cash flows. For example, the 2017 Tax Cuts and Jobs Act (Tax Act) enacted in December 2017 had a significant impact on our tax obligations and effective tax rate for the fourth quarter of 2017. The issuance of additional regulatory or accounting guidance related to the Tax Act, or other executive or Congressional actions in the United States, could materially affect our tax obligations and effective tax rate in the period such guidance is issued or such actions take effect. In addition, many countries in Europe, as well as a number of other countries and organizations, have recently proposed or recommended changes to existing tax laws or have enacted new laws that could significantly increase our tax obligations in many countries where we do business or require us to change the manner in which we operate our business.
````

</details>

RQ2 citation match (section level): `cited=[('META', 'Item 8'), ('META', 'Item 1A')] gold=[(None, 'Item 8'), (None, 'Item 1A')]`

**System C guardrail** (judge `gpt-5.4`): numerical claims 3, verified 3, ungrounded 0, uncited 0, derived 1; sentence verdicts: supported 4, partial 0, unsupported 0, unchecked 0.


<details><summary>Guardrail sentence verdicts</summary>

| sentence | verdict | judge reason |
|---|---|---|
| Meta Platforms, Inc.'s domestic income before provision for income taxes increased from $5,317 million in 2019 to $24,233 million in 2020, which was a year-over-year increase of approximately 356% [META FY2020, Item 8, META_FY2020_2020-12-31:511]. | None |  |
| The company characterizes its future income tax rates as potentially volatile and difficult to predict [META FY2020, Item 1A, META_FY2020_2020-12-31:147]. | supported | The cited text explicitly says future income tax rates could be volatile and difficult to predict. |
| In its risk factors, the company says its overall tax rate is affected by the mix of income it earns in the U.S. and in jurisdictions with different tax rates, the effects of share-based compensation, the effects of integrating intellectual property from acquisitions, the effects of changes in its business or structure, and the effects of discrete items such as legal and tax settlements and tax elections [META FY2020, Item 1A, META_FY2020_2020-12-31:105]. | supported | The cited risk factor lists each stated factor affecting the overall tax rate. |
| The company also says its future income tax rates could be volatile and difficult to predict due to changes in jurisdictional profit split, changes in the amount and recognition of deferred tax assets and liabilities, or changes in tax laws, regulations, or accounting principles [META FY2020, Item 1A, META_FY2020_2020-12-31:147]. | supported | The cited text states those exact reasons future income tax rates could be volatile and difficult to predict. |
| It further warns that changes in tax laws or tax rulings, or changes in interpretations of existing laws, could materially affect its financial position, results of operations, and cash flows, and that new laws in Europe and other countries could significantly increase its tax obligations or require changes in how it operates its business [META FY2020, Item 1A, META_FY2020_2020-12-31:148]. | supported | The cited evidence expressly warns of both material effects from tax law changes and possible increases in obligations or operational changes in Europe and elsewhere. |

</details>

### System C v2 (agentic multi-hop + XBRL)

Model: `gpt-5.4`. Hops: 2. Chunks retrieved: 13, cited: 4.

**Generated answer**

> Meta Platforms, Inc.'s domestic income before provision for income taxes increased from $5,317 million in 2019 to $24,233 million in 2020, which represents a year-over-year increase of approximately 355.8% [META FY2020, Item 8, META_FY2020_2020-12-31:511].  
>
> The company characterizes its financial results and tax rate as subject to fluctuation from quarter to quarter and difficult to predict, noting that the overall tax rate is affected by the mix of income earned in the U.S. and in jurisdictions with different tax rates, the effects of share-based compensation, the effects of integrating intellectual property from acquisitions, the effects of changes in its business or structure, and discrete items such as legal and tax settlements and tax elections [META FY2020, Item 1A, META_FY2020_2020-12-31:105].  
>
> It also states that changes in tax laws or judicial or regulatory interpretations of tax laws may significantly affect the effective tax rate in the period such laws are enacted or interpretations are issued, and that tax obligations arising from resolutions of tax examinations, including the current IRS examination, may materially differ from anticipated amounts [META FY2020, Item 1A, META_FY2020_2020-12-31:105].  
>
> In addition, the company says the tax effects of share-based compensation may significantly impact its effective tax rate from period to period, with higher stock prices at vesting producing excess tax benefits that decrease the effective tax rate, while lower stock prices at vesting may increase the effective tax rate [META FY2020, Item 1A, META_FY2020_2020-12-31:151].  
>
> The company further warns that changes in tax laws or tax rulings, or changes in interpretations of existing laws, could materially affect its financial position, results of operations, and cash flows, and that new or proposed laws in Europe and other countries could significantly increase its tax obligations or require changes in how it operates its business [META FY2020, Item 1A, META_FY2020_2020-12-31:148].

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `F-META-2020` | SEC XBRL Reported Financials (financials.csv) |  |  | fiscal_year,fiscal_year_end,Revenue,NetIncome,OperatingIncome,TotalAssets,TotalLiabilities,StockholdersEquity,CashAndEquivalents,OperatingCashFlow,EPSDiluted 2020,2020-12-31,85965000000,29146000000,32671000000,1593160000… |
| 2 | `META_FY2020_2020-12-31:511` | Item 8 › Note 15. Income Taxes | ✓ | #1 | \| \| Year Ended December 31, \| \| \| \|---\|---\|---\|---\| \| \| 2020 \| 2019 \| 2018 \| \| Domestic \| $24,233 \| $5,317 \| $8,800 \| \| Foreign \| 8,947 \| 19,495 \| 16,561 \| \| Income before provision for income taxes \| $33,180 \| $24,812 \|… |
| 3 | `META_FY2020_2020-12-31:510` | Item 8 › Note 15. Income Taxes |  |  | The components of income before provision for income taxes are as follows (in millions): |
| 4 | `META_FY2020_2020-12-31:313` | Item 7 › Provision for income taxes |  |  | 2020 Compared to 2019. Our provision for income taxes in 2020 decreased $2.29 billion, or 36%, compared to 2019, mostly due to the additional tax expense incurred in 2019 from the Altera Ninth Circuit Opinion and the eff… |
| 5 | `META_FY2020_2020-12-31:320` | Item 7 › Provision for income taxes |  |  | We have previously accrued an estimated unrecognized tax benefit consistent with the guidance in ASC 740, Income Taxes, that is lower than the potential additional federal tax liability from the positions taken by the IR… |
| 6 | `META_FY2020_2020-12-31:512` | Item 8 › Note 15. Income Taxes |  |  | The provision for income taxes consisted of the following (in millions): |
| 7 | `META_FY2020_2020-12-31:312` | Item 7 › Provision for income taxes |  |  | \| \| Year Ended December 31, \| \| \| \| \| \|---\|---\|---\|---\|---\|---\| \| \| 2020 \| 2019 \| 2018 \| 2020 vs 2019 % Change \| 2019 vs 2018 % Change \| \| \| (dollars in millions) \| \| \| \| \| \| Provision for income taxes \| $4,034 \| $6,327 … |
| 8 | `META_FY2020_2020-12-31:105` | Item 1A › Our financial results will fluctuate from quarter to quarter and are difficult to predict. | ✓ |  | •the overall tax rate for our business, which is affected by the mix of income we earn in the U.S. and in jurisdictions with different tax rates, the effects of share-based compensation, the effects of integrating intell… |
| 9 | `META_FY2020_2020-12-31:316` | Item 7 › Provision for income taxes |  |  | Effective Tax Rate Items. Our effective tax rate in the future will depend upon the proportion between the following items and income before provision for income taxes: U.S. tax benefits from foreign derived intangible i… |
| 10 | `META_FY2020_2020-12-31:151` | Item 1A › Given our levels of share-based compensation, our tax rate may vary significantly depending on our stock price. | ✓ |  | The tax effects of the accounting for share-based compensation may significantly impact our effective tax rate from period to period. In periods in which our stock price is higher than the grant price of the share-based … |
| 11 | `META_FY2020_2020-12-31:148` | Item 1A › Changes in tax laws or tax rulings could materially affect our financial position, results of operations, and cash flows. | ✓ |  | The tax regimes we are subject to or operate under, including income and non-income taxes, are unsettled and may be subject to significant change. Changes in tax laws or tax rulings, or changes in interpretations of exis… |
| 12 | `META_FY2020_2020-12-31:364` | Item 8 › Critical Audit Matters |  |  | \| \| Uncertain Tax Positions \| \|---\|---\| \| How We Addressed the Matter in Our Audit \| We obtained an understanding, evaluated the design and tested the operating effectiveness of controls over the Company's process to ass… |
| 13 | `META_FY2020_2020-12-31:363` | Item 8 › Critical Audit Matters |  |  | \| \| Uncertain Tax Positions \| \|---\|---\| \| Description of the Matter \| As discussed in Note 15 to the consolidated financial statements, the Company has received certain notices from the Internal Revenue Service (IRS) rel… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#2 `META_FY2020_2020-12-31:511`** (cited, gold #1)

````text
Item 8.Financial Statements and Supplementary Data > Note 15. Income Taxes (table)
|  | Year Ended December 31, |  |  |
|---|---|---|---|
|  | 2020 | 2019 | 2018 |
| Domestic | $24,233 | $5,317 | $8,800 |
| Foreign | 8,947 | 19,495 | 16,561 |
| Income before provision for income taxes | $33,180 | $24,812 | $25,361 |
````

**#8 `META_FY2020_2020-12-31:105`** (cited)

````text
Item 1A.Risk Factors > Our financial results will fluctuate from quarter to quarter and are difficult to predict.
•the overall tax rate for our business, which is affected by the mix of income we earn in the U.S. and in jurisdictions with different tax rates, the effects of share-based compensation, the effects of integrating intellectual property from acquisitions, the effects of changes in our business or structure, and the effects of discrete items such as legal and tax settlements and tax elections; •the impact of changes in tax laws or judicial or regulatory interpretations of tax laws, which are recorded in the period such laws are enacted or interpretations are issued, and may significantly affect the effective tax rate of that period; •tax obligations that may arise from resolutions of tax examinations, including the examination we are currently under by the Internal Revenue Service (IRS), that materially differ from the amounts we have anticipated; •fluctuations in currency exchange rates and changes in the proportion of our revenue and expenses denominated in foreign currencies; •trading activity in our share repurchase program; •fluctuations in the market values of our investments in marketable securities, in the valuation of our equity investments, and in interest rates; •changes in U.S. generally accepted accounting principles; and
````

**#10 `META_FY2020_2020-12-31:151`** (cited)

````text
Item 1A.Risk Factors > Given our levels of share-based compensation, our tax rate may vary significantly depending on our stock price.
The tax effects of the accounting for share-based compensation may significantly impact our effective tax rate from period to period. In periods in which our stock price is higher than the grant price of the share-based compensation vesting in that period, we will recognize excess tax benefits that will decrease our effective tax rate. For example, in 2020, excess tax benefits recognized from share-based compensation decreased our provision for income taxes by $656 million and our effective tax rate by two percentage points as compared to the tax rate without such benefits. In future periods in which our stock price is lower than the grant price of the share-based compensation vesting in that period, our effective tax rate may increase. The amount and value of share-based compensation issued relative to our earnings in a particular period will also affect the magnitude of the impact of share-based compensation on our effective tax rate. These tax effects are dependent on our stock price, which we do not control, and a decline in our stock price could significantly increase our effective tax rate and adversely affect our financial results.
````

**#11 `META_FY2020_2020-12-31:148`** (cited)

````text
Item 1A.Risk Factors > Changes in tax laws or tax rulings could materially affect our financial position, results of operations, and cash flows.
The tax regimes we are subject to or operate under, including income and non-income taxes, are unsettled and may be subject to significant change. Changes in tax laws or tax rulings, or changes in interpretations of existing laws, could materially affect our financial position, results of operations, and cash flows. For example, the 2017 Tax Cuts and Jobs Act (Tax Act) enacted in December 2017 had a significant impact on our tax obligations and effective tax rate for the fourth quarter of 2017. The issuance of additional regulatory or accounting guidance related to the Tax Act, or other executive or Congressional actions in the United States, could materially affect our tax obligations and effective tax rate in the period such guidance is issued or such actions take effect. In addition, many countries in Europe, as well as a number of other countries and organizations, have recently proposed or recommended changes to existing tax laws or have enacted new laws that could significantly increase our tax obligations in many countries where we do business or require us to change the manner in which we operate our business.
````

</details>

RQ2 citation match (section level): `cited=[('META', 'Item 8'), ('META', 'Item 1A')] gold=[(None, 'Item 8'), (None, 'Item 1A')]`

**System C guardrail** (judge `gpt-5.4`): numerical claims 3, verified 3, ungrounded 0, uncited 0, derived 1; sentence verdicts: supported 4, partial 0, unsupported 0, unchecked 0.


<details><summary>Guardrail sentence verdicts</summary>

| sentence | verdict | judge reason |
|---|---|---|
| Meta Platforms, Inc.'s domestic income before provision for income taxes increased from $5,317 million in 2019 to $24,233 million in 2020, which represents a year-over-year increase of approximately 355.8% [META FY2020, Item 8, META_FY2020_2020-12-31:511]. | None |  |
| The company characterizes its financial results and tax rate as subject to fluctuation from quarter to quarter and difficult to predict, noting that the overall tax rate is affected by the mix of income earned in the U.S. and in jurisdictions with different tax rates, the effects of share-based compensation, the effects of integrating intellectual property from acquisitions, the effects of changes in its business or structure, and discrete items such as legal and tax settlements and tax elections [META FY2020, Item 1A, META_FY2020_2020-12-31:105]. | supported | The cited risk factor states results are difficult to predict and lists each named factor affecting the overall tax rate. |
| It also states that changes in tax laws or judicial or regulatory interpretations of tax laws may significantly affect the effective tax rate in the period such laws are enacted or interpretations are issued, and that tax obligations arising from resolutions of tax examinations, including the current IRS examination, may materially differ from anticipated amounts [META FY2020, Item 1A, META_FY2020_2020-12-31:105]. | supported | The evidence expressly says such tax law changes may significantly affect the effective tax rate and IRS examination resolutions may differ materially from anticipated amounts. |
| In addition, the company says the tax effects of share-based compensation may significantly impact its effective tax rate from period to period, with higher stock prices at vesting producing excess tax benefits that decrease the effective tax rate, while lower stock prices at vesting may increase the effective tax rate [META FY2020, Item 1A, META_FY2020_2020-12-31:151]. | supported | The cited passage directly states share-based compensation tax effects may significantly affect the effective tax rate and explains higher versus lower stock-price vesting effects. |
| The company further warns that changes in tax laws or tax rulings, or changes in interpretations of existing laws, could materially affect its financial position, results of operations, and cash flows, and that new or proposed laws in Europe and other countries could significantly increase its tax obligations or require changes in how it operates its business [META FY2020, Item 1A, META_FY2020_2020-12-31:148]. | supported | The evidence explicitly warns that tax law or interpretation changes could materially affect financials and that European and other countries' new or proposed laws could significantly increase tax obligations or require operational changes. |

</details>
