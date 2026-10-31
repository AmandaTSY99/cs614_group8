# gold-083: Cross-year text

[← all cases](../README.md) · company: Tesla, Inc. (TSLA) · fiscal year: 2025 · recipe `cross_year_text` · hop `multi` · answer type `qualitative` · scope `cross_year` · RQ2 category `multi_company_comparison`

## Gold QA

**Question**

> Contrast the regulatory tax environments impacting Tesla's financial reporting in fiscal year 2025 versus fiscal year 2019, specifically identifying the major federal legislative act enacted in 2025 and the specific state-level agreements discussed in 2019.

**Gold answer**

> In fiscal year 2025, Tesla's financial reporting was impacted by the enactment of the U.S. H.R.1 (OBBBA) on July 4, 2025, which introduced changes to income tax provisions such as domestic R&D expenses and the repeal of certain 2022 Inflation Reduction Act tax credits. In contrast, in fiscal year 2019, Tesla discussed agreements with the State of Nevada and Storey County that provided abatements for various taxes and transferable tax credits for Gigafactory Nevada.

**Key points** (RQ3 keypoint_recall targets)

1. The 2025 filing references the enactment of U.S. H.R.1 (OBBBA) on July 4, 2025.
2. The 2019 filing references agreements with the State of Nevada and Storey County.
3. The 2019 Nevada agreements provided tax abatements and transferable tax credits.

**Gold evidence**

1. `TSLA_FY2025_2025-12-31` · ITEM 8. FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA › Note 2 – Summary of Significant Accounting Policies · text

   > On July 4, 2025, the U.S. H.R.1, an act to provide for reconciliation pursuant to title II of H. Con. Res. 14. (the “OBBBA”) was enacted.

2. `TSLA_FY2019_2019-12-31` · ITEM 8. FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA › Note 2 – Summary of Significant Accounting Policies · text

   > We had entered into agreements with the State of Nevada and Storey County in Nevada that provide abatements for sales, use, real property, personal property and employer excise taxes, discounts to the base tariff energy rates and transferable tax credits.

## Scorecard

| Metric | A (vanilla dense) | B (hybrid + rerank) | C v1 (adaptive multi-hop) | C v2 (agentic multi-hop + XBRL) |
|---|---|---|---|---|
| **Retrieval (RQ1)** | | | | |
| chunks retrieved | 10 | 5 | 14 | 16 |
| recall@5 | 0.00 | 0.50 | 0.00 | 0.50 |
| recall@all | 0.50 | 0.50 | 0.50 | 1.00 |
| complete@all | 0 | 0 | 0 | 1 |
| average precision (lexical) | 0.17 | 0.33 | 0.07 | 0.21 |
| gold evidence first rank | #1: 6, #2: – | #1: 3, #2: – | #1: 14, #2: – | #1: 4, #2: 13 |
| **Answer (RQ3 string match)** | | | | |
| numeric_correct | ✓ | ✓ | ✓ | ✓ |
| keypoint_recall | 0.67 | 0.33 | 1.00 | 1.00 |
| **Answer & citations (RQ2)** | | | | |
| numeric_accuracy | – | – | – | – |
| citation precision | 1.00 | 0.50 | 0.33 | 1.00 |
| citation recall | 1.00 | 1.00 | 1.00 | 1.00 |
| citation F1 | 1.00 | 0.67 | 0.50 | 1.00 |
| has a citation | 1 | 1 | 1 | 1 |
| grounding error rate | – | – | 0.00 | 0.00 |
| **Cost (RQ3)** | | | | |
| retrieval hops | 1 | 1 | 3 | 3 |
| tokens | 1557 | 1668 | 24389 | 17637 |
| cost (USD) | 0.0003 | 0.0003 | 0.0929 | 0.0683 |
| latency (s) | 3.2 | 9.4 | 39.1 | 33.3 |

Definitions: [README › Metrics](../README.md#metrics). `–` = not applicable (e.g. no gold number, no citations, no guardrail).

## System outputs

### System A (vanilla dense)

Model: `gpt-5.4-2026-03-05`. Hops: 1. Chunks retrieved: 10, cited: 2.

**Generated answer**

> In fiscal year 2025, Tesla said a major new federal legislative act was enacted on July 4, 2025: the U.S. H.R.1, referred to as the “OBBBA.” Tesla described it as introducing multiple tax law and other legislative changes, including changes affecting domestic R&D expenses, capital expenditures, U.S. taxation of international earnings, and certain tax credits and regulatory credit programs [6].
>
> For fiscal year 2019, the provided context discusses the federal 2017 Tax Cuts and Jobs Act and its effects on Tesla’s tax accounting, but it does not mention any specific state-level agreements [1].
>
> So, from the provided context:
> - 2025 major federal act: U.S. H.R.1 (“OBBBA”) [6]
> - 2019 specific state-level agreements: not provided in the context [1]

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `TSLA_FY2019_2019-12-31:566` | Item 8 › Note 15 – Income Taxes | ✓ |  | On December 22, 2017, the 2017 Tax Cuts and Jobs Act (“Tax Act”) was enacted into law making significant changes to the Internal Revenue Code. Changes include, but are not limited to, a federal corporate tax rate decreas… |
| 2 | `TSLA_FY2025_2025-12-31:452` | Item 8 › Note 12 – Income Taxes |  |  | Upon adoption of ASU 2023-09, Improvements to Income Tax Disclosures, as described in Note 2, Summary of Significant Accounting Policies, cash paid for income taxes, net of refunds, during the year ended December 31, 202… |
| 3 | `TSLA_FY2025_2025-12-31:295` | Item 8 › Note 2 – Summary of Significant Accounting Policies |  |  | impact our remaining performance obligations and revenue to be recognized under these contracts. In 2025, governmental and regulatory actions, such as OBBBA, have restricted certain regulatory credit programs tied to our… |
| 4 | `TSLA_FY2025_2025-12-31:448` | Item 8 › Note 12 – Income Taxes |  |  | Upon adoption of ASU 2023-09, Improvements to Income Tax Disclosures, as described in Note 2, Summary of Significant Accounting Policies, the reconciliation of taxes at the federal statutory rate to our provision for (be… |
| 5 | `TSLA_FY2025_2025-12-31:450` | Item 8 › Note 12 – Income Taxes |  |  | The reconciliation of taxes at the federal statutory rate to our provision for (benefit from) income taxes for the years ended December 31, 2024 and 2023 in accordance with the guidance prior to the adoption of ASU 2023-… |
| 6 | `TSLA_FY2025_2025-12-31:359` | Item 8 › Note 2 – Summary of Significant Accounting Policies | ✓ | #1 | On July 4, 2025, the U.S. H.R.1, an act to provide for reconciliation pursuant to title II of H. Con. Res. 14. (the “OBBBA”) was enacted. The OBBBA introduces multiple tax law and other legislative changes, including mod… |
| 7 | `TSLA_FY2025_2025-12-31:498` | Item 9 |  |  | None. |
| 8 | `TSLA_FY2025_2025-12-31:444` | Item 8 › Note 12 – Income Taxes |  |  | Our income before provision for (benefit from) income taxes for the years ended December 31, 2025, 2024 and 2023 was as follows (in millions): |
| 9 | `TSLA_FY2025_2025-12-31:358` | Item 8 › Note 2 – Summary of Significant Accounting Policies |  |  | ASU 2023-09 In December 2023, the Financial Accounting Standards Board (“FASB”) issued Accounting Standards Update (“ASU”) No. 2023-09, Improvements to Income Tax Disclosures (Topic 740). The ASU requires disaggregated i… |
| 10 | `TSLA_FY2025_2025-12-31:503` | Item 9A |  |  | There was no change in our internal control over financial reporting that occurred during the quarter ended December 31, 2025, which has materially affected, or is reasonably likely to materially affect, our internal con… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#1 `TSLA_FY2019_2019-12-31:566`** (cited)

````text
ITEM 8. FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA > Note 15 – Income Taxes
On December 22, 2017, the 2017 Tax Cuts and Jobs Act (“Tax Act”) was enacted into law making significant changes to the Internal Revenue Code. Changes include, but are not limited to, a federal corporate tax rate decrease from 35% to 21% for tax years beginning after December 31, 2017, the transition of U.S. international taxation from a worldwide tax system to a territorial system and a one-time transition tax on the mandatory deemed repatriation of foreign earnings. We were required to recognize the effect of the tax law changes in the period of enactment, such as re-measuring our U.S. deferred tax assets and liabilities as well as reassessing the net realizability of our deferred tax assets and liabilities. The Tax Act did not give rise to any material impact on the consolidated balance sheets and consolidated statements of operations due to our historical worldwide loss position and the full valuation allowance on our net U.S. deferred tax assets. Deferred tax assets (liabilities) as of December 31, 2019 and 2018 consisted of the following (in millions):
````

**#6 `TSLA_FY2025_2025-12-31:359`** (cited, gold #1)

````text
ITEM 8. FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA > Note 2 – Summary of Significant Accounting Policies
On July 4, 2025, the U.S. H.R.1, an act to provide for reconciliation pursuant to title II of H. Con. Res. 14. (the “OBBBA”) was enacted. The OBBBA introduces multiple tax law and other legislative changes, including modifications to income tax provisions such as domestic research and development expenses, capital expenditures, and U.S. taxation of international earnings; the repeal or acceleration of the sunset of certain tax credits under the 2022 Inflation Reduction Act and elimination of certain penalties for violations of certain regulatory credit programs. We have recognized the effects of the OBBBA provisions in our financial results to the extent they are applicable to the year ended December 31, 2025. We will continue to evaluate the impact of these provisions on our 2026 and subsequent consolidated financial statements, including loss of certain regulatory credit sales tied to our products and changes to the costs of our products.
````

</details>

RQ2 citation match (section level): `cited=[('TSLA', 'Item 8')] gold=[(None, 'Item 8')]`

### System B (hybrid + rerank)

Model: `gpt-5.4-2026-03-05`. Hops: 1. Chunks retrieved: 5, cited: 2.

**Generated answer**

> In fiscal year 2025, Tesla said a major federal legislative act, the **U.S. H.R.1** (the “**OBBBA**”), was enacted on **July 4, 2025**. Tesla said this law changed tax provisions and repealed or accelerated the sunset of certain tax credits, with effects recognized in its 2025 financial results [3].
>
> In fiscal year 2019, Tesla discussed a different regulatory tax environment centered on incentives being reduced or ending, including the phase-out of the **$7,500 U.S. federal tax credit** and **state-level California regulations** that were **effective March 2016** and were **phasing out a $2,500 incentive** [2].  
>
> So, the 2025 environment was shaped by the federal enactment of **H.R.1 / OBBBA** [3], while the 2019 discussion referenced **California’s state-level incentive phase-out regulations** [2].

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `TSLA_FY2025_2025-12-31:138` | Item 1A › Risks Related to Government Laws and Regulations |  |  | Government and economic incentives that support the development and adoption of electric vehicles in the U.S. and abroad, including certain tax exemptions, tax credits and rebates, may be reduced, eliminated, amended or … |
| 2 | `TSLA_FY2019_2019-12-31:129` | Item 1A › Increases in costs, disruption of supply or shortage of materials, in particular for lithium-ion cells, could harm our business. | ✓ |  | We and our customers currently benefit from certain government and economic incentives supporting the development and adoption of electric vehicles. In the U.S. and abroad, such incentives include tax credits or rebates … |
| 3 | `TSLA_FY2025_2025-12-31:359` | Item 8 › Note 2 – Summary of Significant Accounting Policies | ✓ | #1 | On July 4, 2025, the U.S. H.R.1, an act to provide for reconciliation pursuant to title II of H. Con. Res. 14. (the “OBBBA”) was enacted. The OBBBA introduces multiple tax law and other legislative changes, including mod… |
| 4 | `TSLA_FY2025_2025-12-31:505` | Item 9B |  |  | On January 16, 2026, following review in a manner consistent with the Board’s fiduciary duties and the Company’s related party transactions policy (the “RPT Policy”), Tesla entered into an agreement to invest approximate… |
| 5 | `TSLA_FY2025_2025-12-31:173` | Item 5 › Stock Performance Graph |  |  | This performance graph shall not be deemed “filed” for purposes of Section 18 of the Securities Exchange Act of 1934, as amended (the “Exchange Act”), or incorporated by reference into any filing of Tesla, Inc. under the… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#2 `TSLA_FY2019_2019-12-31:129`** (cited)

````text
ITEM 1A. RISK FACTORS > Increases in costs, disruption of supply or shortage of materials, in particular for lithium-ion cells, could harm our business.
We and our customers currently benefit from certain government and economic incentives supporting the development and adoption of electric vehicles. In the U.S. and abroad, such incentives include tax credits or rebates that encourage the purchase of electric vehicles. Specific policies in place around the world include exempting the purchase of electric vehicles from import taxes, value added taxes, or carbon dioxide and weight-based purchase taxes. Such programs could be reduced, eliminated or exhausted. For example, under current regulations, a $7,500 federal tax credit that was available in the U.S. for the purchase of our vehicles was reduced in phases during 2019 and ended on December 31, 2019. We believe that this sequential phase-out likely pulled forward some vehicle demand into the periods preceding each reduction. Moreover, in July 2018, a previously available incentive for purchases of Model 3 in Ontario, Canada was cancelled and Tesla buyers in Germany lost access to electric vehicle incentives for a short period of time beginning late 2017. In April 2017 and January 2016, respectively, previously available incentives in Hong Kong and Denmark that favored the purchase of electric vehicles expired, negatively impacting sales. Effective March 2016, California implemented regulations phasing out a $2,500
````

**#3 `TSLA_FY2025_2025-12-31:359`** (cited, gold #1)

````text
ITEM 8. FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA > Note 2 – Summary of Significant Accounting Policies
On July 4, 2025, the U.S. H.R.1, an act to provide for reconciliation pursuant to title II of H. Con. Res. 14. (the “OBBBA”) was enacted. The OBBBA introduces multiple tax law and other legislative changes, including modifications to income tax provisions such as domestic research and development expenses, capital expenditures, and U.S. taxation of international earnings; the repeal or acceleration of the sunset of certain tax credits under the 2022 Inflation Reduction Act and elimination of certain penalties for violations of certain regulatory credit programs. We have recognized the effects of the OBBBA provisions in our financial results to the extent they are applicable to the year ended December 31, 2025. We will continue to evaluate the impact of these provisions on our 2026 and subsequent consolidated financial statements, including loss of certain regulatory credit sales tied to our products and changes to the costs of our products.
````

</details>

RQ2 citation match (section level): `cited=[('TSLA', 'Item 1A'), ('TSLA', 'Item 8')] gold=[(None, 'Item 8')]`

### System C v1 (adaptive multi-hop)

Model: `gpt-5.4`. Hops: 3. Chunks retrieved: 14, cited: 5.

**Generated answer**

> In fiscal year 2025, Tesla’s financial reporting was impacted by the One Big Beautiful Bill Act, or OBBBA, enacted on July 4, 2025, which introduced multiple tax law and other legislative changes, including modifications to income tax provisions and the repeal or acceleration of the sunset of certain tax credits under the 2022 Inflation Reduction Act. [TSLA FY2025, Item 8, TSLA_FY2025_2025-12-31:359]
>
> Tesla stated that it recognized the effects of the OBBBA provisions in its financial results to the extent they were applicable to the year ended December 31, 2025. [TSLA FY2025, Item 8, TSLA_FY2025_2025-12-31:359]
>
> Tesla also stated that the OBBBA substantially curtailed IRA incentives by repealing individual consumer tax credits for electric vehicles and residential energy property and imposing more stringent eligibility requirements, accelerated phase-outs, and termination of certain provisions, although some IRA incentives remain available under revised requirements. [TSLA FY2025, Item 1, TSLA_FY2025_2025-12-31:48]
>
> By contrast, in fiscal year 2019, the filing discussed a state-level agreement titled the Agreement for Tax Abatement and Incentives, dated as of May 7, 2015, by and between Tesla Motors, Inc. and the State of Nevada, acting by and through the Nevada Governor’s Office of Economic Development. [TSLA FY2019, Item 15, TSLA_FY2019_2019-12-31:691]
>
> Tesla’s 2025 exhibit index also lists a state-related agreement titled the Grant Contract for State-Owned Construction Land Use Right, dated as of October 17, 2018, by and between Shanghai Planning and Land Resource Administration Bureau, as grantor, and Tesla (Shanghai) Co., Ltd., as grantee. [TSLA FY2025, Item 15, TSLA_FY2025_2025-12-31:522]
>
> Separately, Tesla’s 2019 income tax note identified the federal legislative backdrop as the 2017 Tax Cuts and Jobs Act, enacted on December 22, 2017, which reduced the federal corporate tax rate from 35% to 21% and shifted U.S. international taxation from a worldwide tax system to a territorial system. [TSLA FY2019, Item 8, TSLA_FY2019_2019-12-31:566]

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `TSLA_FY2025_2025-12-31:448` | Item 8 › Note 12 – Income Taxes |  |  | Upon adoption of ASU 2023-09, Improvements to Income Tax Disclosures, as described in Note 2, Summary of Significant Accounting Policies, the reconciliation of taxes at the federal statutory rate to our provision for (be… |
| 2 | `TSLA_FY2025_2025-12-31:358` | Item 8 › Note 2 – Summary of Significant Accounting Policies |  |  | ASU 2023-09 In December 2023, the Financial Accounting Standards Board (“FASB”) issued Accounting Standards Update (“ASU”) No. 2023-09, Improvements to Income Tax Disclosures (Topic 740). The ASU requires disaggregated i… |
| 3 | `TSLA_FY2025_2025-12-31:452` | Item 8 › Note 12 – Income Taxes |  |  | Upon adoption of ASU 2023-09, Improvements to Income Tax Disclosures, as described in Note 2, Summary of Significant Accounting Policies, cash paid for income taxes, net of refunds, during the year ended December 31, 202… |
| 4 | `TSLA_FY2025_2025-12-31:450` | Item 8 › Note 12 – Income Taxes |  |  | The reconciliation of taxes at the federal statutory rate to our provision for (benefit from) income taxes for the years ended December 31, 2024 and 2023 in accordance with the guidance prior to the adoption of ASU 2023-… |
| 5 | `TSLA_FY2019_2019-12-31:566` | Item 8 › Note 15 – Income Taxes | ✓ |  | On December 22, 2017, the 2017 Tax Cuts and Jobs Act (“Tax Act”) was enacted into law making significant changes to the Internal Revenue Code. Changes include, but are not limited to, a federal corporate tax rate decreas… |
| 6 | `TSLA_FY2025_2025-12-31:444` | Item 8 › Note 12 – Income Taxes |  |  | Our income before provision for (benefit from) income taxes for the years ended December 31, 2025, 2024 and 2023 was as follows (in millions): |
| 7 | `TSLA_FY2019_2019-12-31:691` | Item 15 › INDEX TO EXHIBITS | ✓ |  | \| Exhibit \| \| Incorporated by Reference \| \| \| \| Filed \| \|---\|---\|---\|---\|---\|---\|---\| \| Number \| Exhibit Description \| Form \| File No. \| Exhibit \| Filing Date \| Herewith \| \| 10.52† \| Agreement for Tax Abatement and Incen… |
| 8 | `TSLA_FY2025_2025-12-31:522` | Item 15 › INDEX TO EXHIBITS(1) | ✓ |  | \| Exhibit Number \| \| Incorporated by Reference \| \| \| \| Filed Herewith \| \|---\|---\|---\|---\|---\|---\|---\| \| \| Exhibit Description \| Form \| File No. \| Exhibit \| Filing Date \| \| \| 10.16** \| 2025 CEO Interim Restricted Stock Ag… |
| 9 | `TSLA_FY2019_2019-12-31:677` | Item 15 › INDEX TO EXHIBITS |  |  | \| Exhibit \| \| Incorporated by Reference \| \| \| \| Filed \| \|---\|---\|---\|---\|---\|---\|---\| \| Number \| Exhibit Description \| Form \| File No. \| Exhibit \| Filing Date \| Herewith \| \| 10.9** \| Form of Stock Option Agreement under … |
| 10 | `TSLA_FY2019_2019-12-31:675` | Item 15 › INDEX TO EXHIBITS |  |  | \| Exhibit \| \| Incorporated by Reference \| \| \| \| Filed \| \|---\|---\|---\|---\|---\|---\|---\| \| 4.118 \| One Hundred-and-Eighty-First Supplemental Indenture, dated as of June 10, 2016, by and between SolarCity and the Trustee, re… |
| 11 | `TSLA_FY2019_2019-12-31:681` | Item 15 › INDEX TO EXHIBITS |  |  | \| Exhibit \| \| Incorporated by Reference \| \| \| \| Filed \| \|---\|---\|---\|---\|---\|---\|---\| \| 10.30 \| Letter Agreement, dated as of February 24, 2015, regarding addition of co-party to General Terms and Conditions, Production … |
| 12 | `TSLA_FY2019_2019-12-31:676` | Item 15 › INDEX TO EXHIBITS |  |  | \| Exhibit \| \| Incorporated by Reference \| \| \| \| Filed \| \|---\|---\|---\|---\|---\|---\|---\| \| 10.6** \| Form of Restricted Stock Unit Award Agreement under 2010 Equity Incentive Plan. \| 10-K \| 001-34756 \| 10.7 \| March 1, 2017 \|… |
| 13 | `TSLA_FY2025_2025-12-31:48` | Item 1 › Inflation Reduction Act Modified by the OBBBA | ✓ |  | On August 16, 2022, the Inflation Reduction Act of 2022 (“IRA”) was enacted into law and is effective for taxable years beginning after December 31, 2022. The IRA included multiple incentives to promote clean energy, ele… |
| 14 | `TSLA_FY2025_2025-12-31:359` | Item 8 › Note 2 – Summary of Significant Accounting Policies | ✓ | #1 | On July 4, 2025, the U.S. H.R.1, an act to provide for reconciliation pursuant to title II of H. Con. Res. 14. (the “OBBBA”) was enacted. The OBBBA introduces multiple tax law and other legislative changes, including mod… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#5 `TSLA_FY2019_2019-12-31:566`** (cited)

````text
ITEM 8. FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA > Note 15 – Income Taxes
On December 22, 2017, the 2017 Tax Cuts and Jobs Act (“Tax Act”) was enacted into law making significant changes to the Internal Revenue Code. Changes include, but are not limited to, a federal corporate tax rate decrease from 35% to 21% for tax years beginning after December 31, 2017, the transition of U.S. international taxation from a worldwide tax system to a territorial system and a one-time transition tax on the mandatory deemed repatriation of foreign earnings. We were required to recognize the effect of the tax law changes in the period of enactment, such as re-measuring our U.S. deferred tax assets and liabilities as well as reassessing the net realizability of our deferred tax assets and liabilities. The Tax Act did not give rise to any material impact on the consolidated balance sheets and consolidated statements of operations due to our historical worldwide loss position and the full valuation allowance on our net U.S. deferred tax assets. Deferred tax assets (liabilities) as of December 31, 2019 and 2018 consisted of the following (in millions):
````

**#7 `TSLA_FY2019_2019-12-31:691`** (cited)

````text
ITEM 15. EXHIBITS AND FINANCIAL STATEMENT SCHEDULES > INDEX TO EXHIBITS (table)
| Exhibit |  | Incorporated by Reference |  |  |  | Filed |
|---|---|---|---|---|---|---|
| Number | Exhibit Description | Form | File No. | Exhibit | Filing Date | Herewith |
| 10.52† | Agreement for Tax Abatement and Incentives, dated as of May 7, 2015, by and between Tesla Motors, Inc. and the State of Nevada, acting by and through the Nevada Governor’s Office of Economic Development. | 10-Q | 001-34756 | 10.1 | August 7, 2015 |  |
| 10.53† | Amended and Restated Loan and Security Agreement, dated as of August 17, 2017, by and among Tesla 2014 Warehouse SPV LLC, Tesla Finance LLC, the Lenders and Group Agents from time to time party thereto, and Deutsche Bank AG, New York Branch, as Administrative Agent. | 10-Q | 001-34756 | 10.3 | November 3, 2017 |  |
````

**#8 `TSLA_FY2025_2025-12-31:522`** (cited)

````text
ITEM 15. EXHIBITS AND FINANCIAL STATEMENT SCHEDULES > INDEX TO EXHIBITS(1) (table)
| Exhibit Number |  | Incorporated by Reference |  |  |  | Filed Herewith |
|---|---|---|---|---|---|---|
|  | Exhibit Description | Form | File No. | Exhibit | Filing Date |  |
| 10.16** | 2025 CEO Interim Restricted Stock Agreement, dated August 3, 2025 | 8-K | 001-34756 | 10.1 | August 4, 2025 |  |
| 10.17** | Tesla, Inc. 2025 CEO Performance Award Agreement, dated as of September 3, 2025 | S-8 | 333-291402 | 4.4 | November 10, 2025 |  |
| 10.18† | Agreement for Tax Abatement and Incentives, dated as of May 7, 2015, by and between Tesla Motors, Inc. and the State of Nevada, acting by and through the Nevada Governor’s Office of Economic Development. | 10-Q | 001-34756 | 10.1 | August 7, 2015 |  |
| 10.19†† | Grant Contract for State-Owned Construction Land Use Right, dated as of October 17, 2018, by and between Shanghai Planning and Land Resource Administration Bureau, as grantor, and Tesla (Shanghai) Co., Ltd., as grantee (English translation). | 10-Q | 001-34756 | 10.2 | July 29, 2019 |  |
````

**#13 `TSLA_FY2025_2025-12-31:48`** (cited)

````text
ITEM 1. BUSINESS > Inflation Reduction Act Modified by the OBBBA
On August 16, 2022, the Inflation Reduction Act of 2022 (“IRA”) was enacted into law and is effective for taxable years beginning after December 31, 2022. The IRA included multiple incentives to promote clean energy, electric vehicles, battery and energy storage manufacture or purchase, including through providing tax credits to consumers. These IRA incentives were subsequently substantially curtailed by the One Big Beautiful Bill Act (the “OBBBA”) enacted on July 4, 2025, which repeals individual consumer tax credits for electric vehicles and residential energy property, and imposes more stringent eligibility requirements, accelerated phase-outs, and termination of certain provisions, although some of the IRA incentives remain available under the revised requirements.
````

**#14 `TSLA_FY2025_2025-12-31:359`** (cited, gold #1)

````text
ITEM 8. FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA > Note 2 – Summary of Significant Accounting Policies
On July 4, 2025, the U.S. H.R.1, an act to provide for reconciliation pursuant to title II of H. Con. Res. 14. (the “OBBBA”) was enacted. The OBBBA introduces multiple tax law and other legislative changes, including modifications to income tax provisions such as domestic research and development expenses, capital expenditures, and U.S. taxation of international earnings; the repeal or acceleration of the sunset of certain tax credits under the 2022 Inflation Reduction Act and elimination of certain penalties for violations of certain regulatory credit programs. We have recognized the effects of the OBBBA provisions in our financial results to the extent they are applicable to the year ended December 31, 2025. We will continue to evaluate the impact of these provisions on our 2026 and subsequent consolidated financial statements, including loss of certain regulatory credit sales tied to our products and changes to the costs of our products.
````

</details>

RQ2 citation match (section level): `cited=[('TSLA', 'Item 8'), ('TSLA', 'Item 1'), ('TSLA', 'Item 15')] gold=[(None, 'Item 8')]`

**System C guardrail** (judge `gpt-5.4`): numerical claims 2, verified 2, ungrounded 0, uncited 0, derived 0; sentence verdicts: supported 5, partial 0, unsupported 0, unchecked 0.


<details><summary>Guardrail sentence verdicts</summary>

| sentence | verdict | judge reason |
|---|---|---|
| In fiscal year 2025, Tesla’s financial reporting was impacted by the One Big Beautiful Bill Act, or OBBBA, enacted on July 4, 2025, which introduced multiple tax law and other legislative changes, including modifications to income tax provisions and the repeal or acceleration of the sunset of certain tax credits under the 2022 Inflation Reduction Act. [TSLA FY2025, Item 8, TSLA_FY2025_2025-12-31:359] | supported | The evidence states OBBBA was enacted on July 4, 2025, made those listed changes, and its effects were recognized in 2025 financial results. |
| Tesla stated that it recognized the effects of the OBBBA provisions in its financial results to the extent they were applicable to the year ended December 31, 2025. [TSLA FY2025, Item 8, TSLA_FY2025_2025-12-31:359] | supported | The quoted evidence exactly states Tesla recognized OBBBA effects in its financial results to the extent applicable to the year ended December 31, 2025. |
| Tesla also stated that the OBBBA substantially curtailed IRA incentives by repealing individual consumer tax credits for electric vehicles and residential energy property and imposing more stringent eligibility requirements, accelerated phase-outs, and termination of certain provisions, although some IRA incentives remain available under revised requirements. [TSLA FY2025, Item 1, TSLA_FY2025_2025-12-31:48] | supported | The evidence expressly says OBBBA substantially curtailed IRA incentives in the ways described while leaving some incentives available under revised requirements. |
| By contrast, in fiscal year 2019, the filing discussed a state-level agreement titled the Agreement for Tax Abatement and Incentives, dated as of May 7, 2015, by and between Tesla Motors, Inc. and the State of Nevada, acting by and through the Nevada Governor’s Office of Economic Development. [TSLA FY2019, Item 15, TSLA_FY2019_2019-12-31:691] | supported | The 2019 exhibit index lists that exact Nevada Agreement for Tax Abatement and Incentives with the stated date and parties. |
| Tesla’s 2025 exhibit index also lists a state-related agreement titled the Grant Contract for State-Owned Construction Land Use Right, dated as of October 17, 2018, by and between Shanghai Planning and Land Resource Administration Bureau, as grantor, and Tesla (Shanghai) Co., Ltd., as grantee. [TSLA FY2025, Item 15, TSLA_FY2025_2025-12-31:522] | supported | The 2025 exhibit index lists that exact Grant Contract with the stated date, parties, and title. |
| Separately, Tesla’s 2019 income tax note identified the federal legislative backdrop as the 2017 Tax Cuts and Jobs Act, enacted on December 22, 2017, which reduced the federal corporate tax rate from 35% to 21% and shifted U.S. international taxation from a worldwide tax system to a territorial system. [TSLA FY2019, Item 8, TSLA_FY2019_2019-12-31:566] | None |  |

</details>

### System C v2 (agentic multi-hop + XBRL)

Model: `gpt-5.4`. Hops: 3. Chunks retrieved: 16, cited: 3.

**Generated answer**

> In fiscal year 2025, Tesla disclosed that on July 4, 2025, U.S. H.R.1, referred to as the OBBBA, was enacted and introduced multiple tax law and other legislative changes, including modifications to income tax provisions, repeal or acceleration of the sunset of certain tax credits under the 2022 Inflation Reduction Act, and elimination of certain penalties for violations of certain regulatory credit programs. [TSLA FY2025, Item 8, TSLA_FY2025_2025-12-31:359]
>
> Tesla stated that it recognized the effects of the OBBBA provisions in its financial results to the extent applicable to the year ended December 31, 2025, and that it would continue evaluating the impact on 2026 and subsequent consolidated financial statements, including the loss of certain regulatory credit sales tied to its products and changes to product costs. [TSLA FY2025, Item 8, TSLA_FY2025_2025-12-31:359]
>
> Tesla also disclosed for 2025 that the IRA incentives had been modified by the OBBBA to impose more stringent eligibility requirements, accelerated phase-outs, and termination of certain provisions, and that some of these measures are expected to materially affect its consolidated financial statements. [TSLA FY2025, Item 8, TSLA_FY2025_2025-12-31:347]
>
> By contrast, in fiscal year 2019, Tesla discussed state-level agreements with the State of Nevada and Storey County in Nevada related to Gigafactory Nevada. [TSLA FY2019, Item 8, TSLA_FY2019_2019-12-31:427]
>
> Those Nevada agreements provided abatements for sales, use, real property, personal property and employer excise taxes, discounts to base tariff energy rates, and transferable tax credits. [TSLA FY2019, Item 8, TSLA_FY2019_2019-12-31:427]
>
> Tesla disclosed that these incentives were available for applicable periods beginning on October 17, 2014 and ending on either June 30, 2024 or June 30, 2034, depending on the incentive. [TSLA FY2019, Item 8, TSLA_FY2019_2019-12-31:427]
>
> Tesla further stated that under these agreements it was eligible for a maximum of $195 million of transferable tax credits, subject to capital investment and hiring targets for Gigafactory Nevada, and that as of December 31, 2019 and 2018 it had earned the maximum $195 million of transferable tax credits under these agreements. [TSLA FY2019, Item 8, TSLA_FY2019_2019-12-31:427]

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `TSLA_FY2025_2025-12-31:244` | Item 8 › Opinions on the Financial Statements and Internal Control over Financial Reporting |  |  | We have audited the accompanying consolidated balance sheets of Tesla, Inc. and its subsidiaries (the "Company") as of December 31, 2025 and 2024, and the related consolidated statements of operations, of comprehensive i… |
| 2 | `TSLA_FY2025_2025-12-31:503` | Item 9A |  |  | There was no change in our internal control over financial reporting that occurred during the quarter ended December 31, 2025, which has materially affected, or is reasonably likely to materially affect, our internal con… |
| 3 | `TSLA_FY2025_2025-12-31:245` | Item 8 › Opinions on the Financial Statements and Internal Control over Financial Reporting |  |  | In our opinion, the consolidated financial statements referred to above present fairly, in all material respects, the financial position of the Company as of December 31, 2025 and 2024, and the results of its operations … |
| 4 | `TSLA_FY2025_2025-12-31:359` | Item 8 › Note 2 – Summary of Significant Accounting Policies | ✓ | #1 | On July 4, 2025, the U.S. H.R.1, an act to provide for reconciliation pursuant to title II of H. Con. Res. 14. (the “OBBBA”) was enacted. The OBBBA introduces multiple tax law and other legislative changes, including mod… |
| 5 | `TSLA_FY2019_2019-12-31:633` | Item 9A |  |  | There was no change in our internal control over financial reporting that occurred during the fourth fiscal quarter of the year ended December 31, 2019, which has materially affected, or is reasonably likely to materiall… |
| 6 | `TSLA_FY2019_2019-12-31:566` | Item 8 › Note 15 – Income Taxes |  |  | On December 22, 2017, the 2017 Tax Cuts and Jobs Act (“Tax Act”) was enacted into law making significant changes to the Internal Revenue Code. Changes include, but are not limited to, a federal corporate tax rate decreas… |
| 7 | `TSLA_FY2019_2019-12-31:304` | Item 8 › Index to Consolidated Financial Statements |  |  | \| \| Page \| \|---\|---\| \| Report of Independent Registered Public Accounting Firm \| 62 \| \| Consolidated Balance Sheets \| 65 \| \| Consolidated Statements of Operations \| 66 \| \| Consolidated Statements of Comprehensive Loss \| … |
| 8 | `TSLA_FY2019_2019-12-31:565` | Item 8 › Note 15 – Income Taxes |  |  | \| \| Year Ended December 31, \| \| \| \|---\|---\|---\|---\| \| \| 2019 \| 2018 \| 2017 \| \| Current: \| \| \| \| \| Federal \| $— \| $(1) \| $(10) \| \| State \| 5 \| 3 \| 2 \| \| Foreign \| 86 \| 24 \| 43 \| \| Total current \| 91 \| 26 \| 35 \| \| Deferred… |
| 9 | `TSLA_FY2019_2019-12-31:468` | Item 8 › Note 9 – Accrued Liabilities and Other |  |  | \| \| December 31, \| December 31, \| \|---\|---\|---\| \| \| 2019 \| 2018 \| \| Accrued purchases (1) \| $638 \| $394 \| \| Payroll and related costs \| 466 \| 449 \| \| Taxes payable (2) \| 611 \| 348 \| \| Accrued interest \| 86 \| 78 \| \| Finan… |
| 10 | `TSLA_FY2025_2025-12-31:326` | Item 8 › Note 2 – Summary of Significant Accounting Policies |  |  | \| \| December 31, 2025 \| December 31, 2024 \| December 31, 2023 \| \|---\|---\|---\|---\| \| Cash and cash equivalents \| $16,513 \| $16,139 \| $16,398 \| \| Restricted cash included in prepaid expenses and other current assets \| 389 … |
| 11 | `TSLA_FY2019_2019-12-31:475` | Item 8 › Note 12 –Debt |  |  | \| \| Unpaid \| \| \| Unused \| \| \| \|---\|---\|---\|---\|---\|---\|---\| \| \| Principal \| Net Carrying Value \| \| Committed \| Contractual \| Contractual \| \| \| Balance \| Current \| Long-Term \| Amount (1) \| Interest Rates \| Maturity Date \|… |
| 12 | `TSLA_FY2019_2019-12-31:479` | Item 8 › Note 12 –Debt |  |  | \| \| Unpaid \| \| \| Unused \| \| \| \|---\|---\|---\|---\|---\|---\|---\| \| \| Principal \| Net Carrying Value \| \| Committed \| Contractual \| Contractual \| \| \| Balance \| Current \| Long-Term \| Amount (1) \| Interest Rates \| Maturity Date \|… |
| 13 | `TSLA_FY2019_2019-12-31:427` | Item 8 › Note 2 – Summary of Significant Accounting Policies | ✓ | #2 | We had entered into agreements with the State of Nevada and Storey County in Nevada that provide abatements for sales, use, real property, personal property and employer excise taxes, discounts to the base tariff energy … |
| 14 | `TSLA_FY2025_2025-12-31:347` | Item 8 › Note 2 – Summary of Significant Accounting Policies | ✓ | #2 | On August 16, 2022, the IRA was enacted into law and is effective for taxable years beginning after December 31, 2022. The IRA includes multiple incentives to promote clean energy, electric vehicles, battery and energy s… |
| 15 | `TSLA_FY2019_2019-12-31:426` | Item 8 › Note 2 – Summary of Significant Accounting Policies |  |  | Under the new revenue standard, we recognize revenue upon the delivery of ITCs to investors under our lease pass-through fund arrangements as this is the point in time that control of ITCs has transferred. We indemnify t… |
| 16 | `TSLA_FY2019_2019-12-31:403` | Item 8 › Note 2 – Summary of Significant Accounting Policies |  |  | \| \| Year Ended December 31, \| \| \| \|---\|---\|---\|---\| \| \| 2019 \| 2018 \| 2017 \| \| Stock-based awards \| 10 \| 10 \| 10 \| \| Convertible senior notes \| 1 \| 1 \| 2 \| \| Warrants \| — \| — \| 1 \| |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#4 `TSLA_FY2025_2025-12-31:359`** (cited, gold #1)

````text
ITEM 8. FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA > Note 2 – Summary of Significant Accounting Policies
On July 4, 2025, the U.S. H.R.1, an act to provide for reconciliation pursuant to title II of H. Con. Res. 14. (the “OBBBA”) was enacted. The OBBBA introduces multiple tax law and other legislative changes, including modifications to income tax provisions such as domestic research and development expenses, capital expenditures, and U.S. taxation of international earnings; the repeal or acceleration of the sunset of certain tax credits under the 2022 Inflation Reduction Act and elimination of certain penalties for violations of certain regulatory credit programs. We have recognized the effects of the OBBBA provisions in our financial results to the extent they are applicable to the year ended December 31, 2025. We will continue to evaluate the impact of these provisions on our 2026 and subsequent consolidated financial statements, including loss of certain regulatory credit sales tied to our products and changes to the costs of our products.
````

**#13 `TSLA_FY2019_2019-12-31:427`** (cited, gold #2)

````text
ITEM 8. FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA > Note 2 – Summary of Significant Accounting Policies
We had entered into agreements with the State of Nevada and Storey County in Nevada that provide abatements for sales, use, real property, personal property and employer excise taxes, discounts to the base tariff energy rates and transferable tax credits. These incentives are available for the applicable periods beginning on October 17, 2014 and ending on either June 30, 2024 or June 30, 2034 (depending on the incentive). Under these agreements, we were eligible for a maximum of $195 million of transferable tax credits, subject to capital investments by us and our partners for Gigafactory Nevada of at least $3.50 billion, which we exceeded during 2017, and specified hiring targets for Gigafactory Nevada, which we exceeded during 2018. We recorded these credits as earned when we had evidence there was a market for their sale. Credits were applied as a cost offset to either employee expense or to capital assets, depending on the source of the credits. Credits earned from employee hires or capital spending by our partners at Gigafactory Nevada were recorded as a reduction to operating expenses. As of December 31, 2019 and 2018, we had earned the maximum of $195 million of transferable tax credits under these
````

**#14 `TSLA_FY2025_2025-12-31:347`** (cited, gold #2)

````text
ITEM 8. FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA > Note 2 – Summary of Significant Accounting Policies
On August 16, 2022, the IRA was enacted into law and is effective for taxable years beginning after December 31, 2022. The IRA includes multiple incentives to promote clean energy, electric vehicles, battery and energy storage manufacture or purchase. The IRA incentives were subsequently modified by the OBBBA enacted on July 4, 2025, which imposes more stringent eligibility requirements, accelerated phase-outs, and the termination of certain provisions. Some of these measures are expected to materially affect our consolidated financial statements. For the years ended December 31, 2025, 2024 and 2023, the impact from our IRA incentive was primarily a reduction of our costs of revenue in our consolidated statements of operations as discussed above in Cost of Revenues. Nevada Tax Incentives In connection with the construction of Gigafactory Nevada, we entered into agreements in 2014 with the State of Nevada and Storey County in Nevada that provide abatements for specified taxes, discounts to the base tariff energy rates and transferable tax credits of up to $195 million in consideration of capital investment and hiring targets that were met at Gigafactory Nevada. Gigafactory Texas Tax Incentives
````

</details>

RQ2 citation match (section level): `cited=[('TSLA', 'Item 8')] gold=[(None, 'Item 8')]`

**System C guardrail** (judge `gpt-5.4`): numerical claims 2, verified 2, ungrounded 0, uncited 0, derived 0; sentence verdicts: supported 6, partial 0, unsupported 0, unchecked 0.


<details><summary>Guardrail sentence verdicts</summary>

| sentence | verdict | judge reason |
|---|---|---|
| In fiscal year 2025, Tesla disclosed that on July 4, 2025, U.S. H.R.1, referred to as the OBBBA, was enacted and introduced multiple tax law and other legislative changes, including modifications to income tax provisions, repeal or acceleration of the sunset of certain tax credits under the 2022 Inflation Reduction Act, and elimination of certain penalties for violations of certain regulatory credit programs. [TSLA FY2025, Item 8, TSLA_FY2025_2025-12-31:359] | supported | The evidence states the July 4, 2025 enactment of H.R.1/OBBBA and the listed legislative changes. |
| Tesla stated that it recognized the effects of the OBBBA provisions in its financial results to the extent applicable to the year ended December 31, 2025, and that it would continue evaluating the impact on 2026 and subsequent consolidated financial statements, including the loss of certain regulatory credit sales tied to its products and changes to product costs. [TSLA FY2025, Item 8, TSLA_FY2025_2025-12-31:359] | supported | The evidence explicitly says Tesla recognized applicable 2025 effects and would continue evaluating 2026 and later impacts including regulatory credit sales and product costs. |
| Tesla also disclosed for 2025 that the IRA incentives had been modified by the OBBBA to impose more stringent eligibility requirements, accelerated phase-outs, and termination of certain provisions, and that some of these measures are expected to materially affect its consolidated financial statements. [TSLA FY2025, Item 8, TSLA_FY2025_2025-12-31:347] | supported | The evidence states the OBBBA modified IRA incentives with stricter eligibility, accelerated phase-outs, termination of provisions, and expected material effects. |
| By contrast, in fiscal year 2019, Tesla discussed state-level agreements with the State of Nevada and Storey County in Nevada related to Gigafactory Nevada. [TSLA FY2019, Item 8, TSLA_FY2019_2019-12-31:427] | supported | The 2019 evidence discusses agreements with the State of Nevada and Storey County in Nevada for Gigafactory Nevada. |
| Those Nevada agreements provided abatements for sales, use, real property, personal property and employer excise taxes, discounts to base tariff energy rates, and transferable tax credits. [TSLA FY2019, Item 8, TSLA_FY2019_2019-12-31:427] | supported | The evidence lists those exact abatements, discounts, and transferable tax credits. |
| Tesla disclosed that these incentives were available for applicable periods beginning on October 17, 2014 and ending on either June 30, 2024 or June 30, 2034, depending on the incentive. [TSLA FY2019, Item 8, TSLA_FY2019_2019-12-31:427] | supported | The evidence states the incentives were available from October 17, 2014 to either June 30, 2024 or June 30, 2034 depending on the incentive. |
| Tesla further stated that under these agreements it was eligible for a maximum of $195 million of transferable tax credits, subject to capital investment and hiring targets for Gigafactory Nevada, and that as of December 31, 2019 and 2018 it had earned the maximum $195 million of transferable tax credits under these agreements. [TSLA FY2019, Item 8, TSLA_FY2019_2019-12-31:427] | None |  |

</details>
