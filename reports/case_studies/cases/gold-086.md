# gold-086: Cross-year text

[← all cases](../README.md) · company: Tesla, Inc. (TSLA) · fiscal year: 2024 · recipe `cross_year_text` · hop `multi` · answer type `qualitative` · scope `cross_year` · RQ2 category `multi_company_comparison`

## Gold QA

**Question**

> How did the primary drivers of Tesla's capital expenditures differ between fiscal year 2020 and fiscal year 2024, specifically regarding the focus on factory expansion versus technology-related investments?

**Gold answer**

> In fiscal year 2020, Tesla's capital expenditures were primarily driven by physical manufacturing expansion, specifically for Model Y production at the Fremont Factory, the expansion of Gigafactory Shanghai, and the construction of Gigafactory Berlin and Gigafactory Texas. In contrast, by fiscal year 2024, while global factory expansion remained a factor, the capital expenditures were mainly attributed to AI-related capital expenditures and machinery and equipment to enhance the product roadmap.

**Key points** (RQ3 keypoint_recall targets)

1. In 2020, CAPEX was mainly for Model Y production expansion, Gigafactory Shanghai expansion, and construction of Gigafactory Berlin and Texas.
2. In 2024, CAPEX was mainly for AI-related capital expenditures, global factory expansion, and machinery/equipment.
3. The focus shifted from purely physical factory construction in 2020 to include significant AI-related investments in 2024.

**Gold evidence**

1. `TSLA_FY2024_2024-12-31` · ITEM 7. MANAGEMENT’S DISCUSSION AND ANALYSIS OF FINANCIAL CONDITION AND RESULTS OF OPERATIONS › Summary of Cash Flows · text

   > Net cash flows from investing activities and their variability across each period related primarily to capital expenditures, which were $11.34 billion and $8.90 billion for the years ended December 31, 2024 and 2023, respectively, mainly for AI-related capital expenditures, global factory expansion and machinery and equipment as we expand and enhance our product roadmap.

2. `TSLA_FY2020_2020-12-31` · ITEM 7. MANAGEMENT’S DISCUSSION AND ANALYSIS OF FINANCIAL CONDITION AND RESULTS OF OPERATIONS › Summary of Cash Flows · text

   > Cash flows from investing activities and their variability across each period related primarily to capital expenditures, which were $3.16 billion for the year ended December 31, 2020, mainly for Model Y production expansion at the Fremont Factory, expansion of Gigafactory Shanghai and construction of Gigafactory Berlin and Gigafactory Texas, and $1.33 billion for the year ended December 31, 2019, mainly for Gigafactory Shanghai construction, Model 3 production ramp and Model Y preparations.

## Scorecard

| Metric | A (vanilla dense) | B (hybrid + rerank) | C v1 (adaptive multi-hop) | C v2 (agentic multi-hop + XBRL) |
|---|---|---|---|---|
| **Retrieval (RQ1)** | | | | |
| chunks retrieved | 10 | 5 | 10 | 13 |
| recall@5 | 0.00 | 1.00 | 1.00 | 1.00 |
| recall@all | 1.00 | 1.00 | 1.00 | 1.00 |
| complete@all | 1 | 1 | 1 | 1 |
| average precision (lexical) | 0.14 | 1.00 | 0.67 | 0.67 |
| gold evidence first rank | #1: 7, #2: 7 | #1: 1, #2: 1 | #1: 1, #2: 1 | #1: 1, #2: 1 |
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
| tokens | 2650 | 1523 | 13836 | 21715 |
| cost (USD) | 0.0005 | 0.0003 | 0.0552 | 0.0830 |
| latency (s) | 5.2 | 7.3 | 31.7 | 38.9 |

Definitions: [README › Metrics](../README.md#metrics). `–` = not applicable (e.g. no gold number, no citations, no guardrail).

## System outputs

### System A (vanilla dense)

Model: `gpt-5.4-2026-03-05`. Hops: 1. Chunks retrieved: 10, cited: 4.

**Generated answer**

> In fiscal 2020, Tesla’s capital expenditures were described primarily in terms of factory and production expansion: Model Y production expansion at Fremont, expansion of Gigafactory Shanghai, and construction of Gigafactory Berlin and Gigafactory Texas [7]. The 2020 outlook also emphasized ramping new products, constructing or ramping manufacturing facilities on three continents, and piloting new battery cell manufacturing [3].
>
> By fiscal 2024, Tesla still emphasized manufacturing growth and factory ramping, but the stated drivers had broadened more clearly toward technology-related investments as well. Tesla said it was developing and ramping new products, building or ramping manufacturing facilities, piloting new battery cell technologies, expanding the Supercharger network, and investing in autonomy and other artificial intelligence-enabled training and products [1]. It also said it would continue using cash flows to invest in autonomy, vertical integration, and product roadmap expansion [10].
>
> So, the difference is that in 2020 the primary capex focus described in the context was mainly factory construction/expansion and production ramp-up [7][3], whereas in 2024 the focus included those manufacturing investments but also more explicitly highlighted technology-related investments, especially autonomy, AI-enabled products, and battery cell technology development [1][10].

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `TSLA_FY2024_2024-12-31:194` | Item 7 › Management Opportunities, Challenges and Uncertainties and 2025 Outlook | ✓ |  | Our capital expenditures are typically difficult to project beyond the short-term given the number and breadth of our core projects at any given time, and may further be impacted by uncertainties in future global market … |
| 2 | `TSLA_FY2024_2024-12-31:184` | Item 7 › Overview and 2024 Highlights |  |  | We ended 2024 with $36.56 billion in cash and cash equivalents and investments, representing an increase of $7.47 billion from the end of 2023. Our cash flows provided by operating activities were $14.92 billion in 2024 … |
| 3 | `TSLA_FY2020_2020-12-31:194` | Item 7 › Management Opportunities, Challenges and Risks and 2021 Outlook | ✓ |  | Our capital expenditures are typically difficult to project beyond the short term given the number and breadth of our core projects at any given time, and uncertainties in future global market conditions resulting from t… |
| 4 | `TSLA_FY2024_2024-12-31:183` | Item 7 › Overview and 2024 Highlights |  |  | In 2024, we recognized total revenues of $97.69 billion, representing an increase of $917 million compared to the prior year. In 2024, our net income attributable to common stockholders was $7.09 billion, representing a … |
| 5 | `TSLA_FY2024_2024-12-31:189` | Item 7 › Management Opportunities, Challenges and Uncertainties and 2025 Outlook |  |  | Our cost reduction efforts, cost innovation strategies, and additional localized procurement and manufacturing are key to our vehicles’ affordability and have allowed us to competitively price our vehicles. We will also … |
| 6 | `TSLA_FY2024_2024-12-31:187` | Item 7 › Management Opportunities, Challenges and Uncertainties and 2025 Outlook |  |  | We are focused on growing our manufacturing capacity, which includes capacity for manufacturing newer vehicle models such as our Cybertruck, Tesla Semi and future vehicles utilizing aspects of our next generation platfor… |
| 7 | `TSLA_FY2020_2020-12-31:278` | Item 7 › Summary of Cash Flows | ✓ | #1, #2 | a larger increase in operating lease vehicles as Model 3 direct leasing was introduced in the second quarter of 2019 and Model Y direct leasing was introduced in the third quarter of 2020, and a larger increase in accoun… |
| 8 | `TSLA_FY2020_2020-12-31:270` | Item 7 › Liquidity and Capital Resources |  |  | As discussed in and subject to the considerations referenced in Part II, Item 7, Management's Discussion and Analysis of Financial Condition and Results of Operations—Management Opportunities, Challenges and Risks and 20… |
| 9 | `TSLA_FY2020_2020-12-31:273` | Item 7 › Liquidity and Capital Resources |  |  | We expect that our current sources of liquidity together with our projection of cash flows from operating activities will provide us with adequate liquidity over at least the next 12 months, even considering the expected… |
| 10 | `TSLA_FY2024_2024-12-31:195` | Item 7 › Management Opportunities, Challenges and Uncertainties and 2025 Outlook | ✓ |  | Our business has generally been consistently generating cash flow from operations in excess of our level of capital spend, and with better working capital management resulting in shorter days sales outstanding than days … |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#1 `TSLA_FY2024_2024-12-31:194`** (cited)

````text
ITEM 7. MANAGEMENT’S DISCUSSION AND ANALYSIS OF FINANCIAL CONDITION AND RESULTS OF OPERATIONS > Management Opportunities, Challenges and Uncertainties and 2025 Outlook
Our capital expenditures are typically difficult to project beyond the short-term given the number and breadth of our core projects at any given time, and may further be impacted by uncertainties in future global market conditions. We are simultaneously developing and ramping new products, building or ramping manufacturing facilities on three continents, piloting the development and manufacture of new battery cell technologies, expanding our Supercharger network and investing in autonomy and other artificial intelligence enabled training and products, and the pace of our capital spend may vary depending on overall priority among projects, the pace at which we meet milestones, production adjustments to and among our various products, increased capital efficiencies and the addition of new projects. Owing and subject to the foregoing as well as the pipeline of announced projects under development, all other continuing infrastructure growth and varying levels of inflation, we currently expect our capital expenditures to exceed $11.00 billion in 2025 and in each of the following two fiscal years.
````

**#3 `TSLA_FY2020_2020-12-31:194`** (cited)

````text
ITEM 7. MANAGEMENT’S DISCUSSION AND ANALYSIS OF FINANCIAL CONDITION AND RESULTS OF OPERATIONS > Management Opportunities, Challenges and Risks and 2021 Outlook
Our capital expenditures are typically difficult to project beyond the short term given the number and breadth of our core projects at any given time, and uncertainties in future global market conditions resulting from the COVID-19 pandemic currently makes projections more challenging. We are simultaneously ramping new products in the new Model S and Model X, Model Y and Solar Roof, constructing or ramping manufacturing facilities on three continents and piloting the development and manufacture of new battery cell technologies, and the pace of our capital spend may vary depending on overall priority among projects, the pace at which we meet milestones, production adjustments to and among our various products, increased capital efficiencies and the addition of new projects. Owing and subject to the foregoing as well as the pipeline of announced projects under development and all other continuing infrastructure growth, we currently expect our capital expenditures to be $4.50 to $6.00 billion in 2021 and each of the next two fiscal years.
````

**#7 `TSLA_FY2020_2020-12-31:278`** (cited, gold #1, gold #2)

````text
ITEM 7. MANAGEMENT’S DISCUSSION AND ANALYSIS OF FINANCIAL CONDITION AND RESULTS OF OPERATIONS > Summary of Cash Flows
a larger increase in operating lease vehicles as Model 3 direct leasing was introduced in the second quarter of 2019 and Model Y direct leasing was introduced in the third quarter of 2020, and a larger increase in accounts receivables of government rebates already passed through to customers. Cash Flows from Investing Activities Cash flows from investing activities and their variability across each period related primarily to capital expenditures, which were $3.16 billion for the year ended December 31, 2020, mainly for Model Y production expansion at the Fremont Factory, expansion of Gigafactory Shanghai and construction of Gigafactory Berlin and Gigafactory Texas, and $1.33 billion for the year ended December 31, 2019, mainly for Gigafactory Shanghai construction, Model 3 production ramp and Model Y preparations. The increase in capital expenditures was partially offset by decreases of $32 million in business combinations, net of cash acquired, and $30 million of design, acquisition and installation of solar energy systems when compared to the prior year. Additionally, we received $123 million and $46 million, respectively, of government grants in connection with us making certain manufacturing equipment investments at Gigafactory Shanghai for the years ended December 31, 2020 and 2019, respectively.
````

**#10 `TSLA_FY2024_2024-12-31:195`** (cited)

````text
ITEM 7. MANAGEMENT’S DISCUSSION AND ANALYSIS OF FINANCIAL CONDITION AND RESULTS OF OPERATIONS > Management Opportunities, Challenges and Uncertainties and 2025 Outlook
Our business has generally been consistently generating cash flow from operations in excess of our level of capital spend, and with better working capital management resulting in shorter days sales outstanding than days payable outstanding, our sales growth is also generally facilitating positive cash generation. We have and will continue to utilize such cash flows, among other things, to invest in autonomy, do more vertical integration, expand our product roadmap and provide financing options to our customers. At the same time, we are likely to see heightened levels of capital expenditures during certain periods depending on the specific pace of our capital-intensive projects and other potential variables such as rising material prices and increases in supply chain and labor expenses resulting from changes in global trade conditions and labor availability. Overall, we expect our ability to be self-funding to continue as long as macroeconomic factors support current trends in our sales.
````

</details>

RQ2 citation match (section level): `cited=[('TSLA', 'Item 7')] gold=[(None, 'Item 7')]`

### System B (hybrid + rerank)

Model: `gpt-5.4-2026-03-05`. Hops: 1. Chunks retrieved: 5, cited: 2.

**Generated answer**

> In fiscal year 2020, Tesla’s capital expenditures were driven mainly by factory expansion and vehicle production buildout: Model Y production expansion at Fremont, expansion of Gigafactory Shanghai, and construction of Gigafactory Berlin and Gigafactory Texas [2].
>
> In fiscal year 2024, Tesla’s capital expenditures were still partly tied to global factory expansion and machinery/equipment, but the company specifically highlighted AI-related capital expenditures as a major driver as well [1].
>
> So, compared with 2020’s stronger emphasis on expanding manufacturing facilities, 2024 shifted toward a mix of factory expansion and more explicit technology-related investment, especially AI [1][2].

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `TSLA_FY2024_2024-12-31:240` | Item 7 › Summary of Cash Flows | ✓ | #1, #2 | Net cash flows from investing activities and their variability across each period related primarily to capital expenditures, which were $11.34 billion and $8.90 billion for the years ended December 31, 2024 and 2023, res… |
| 2 | `TSLA_FY2020_2020-12-31:278` | Item 7 › Summary of Cash Flows | ✓ | #1, #2 | a larger increase in operating lease vehicles as Model 3 direct leasing was introduced in the second quarter of 2019 and Model Y direct leasing was introduced in the third quarter of 2020, and a larger increase in accoun… |
| 3 | `TSLA_FY2024_2024-12-31:187` | Item 7 › Management Opportunities, Challenges and Uncertainties and 2025 Outlook |  |  | We are focused on growing our manufacturing capacity, which includes capacity for manufacturing newer vehicle models such as our Cybertruck, Tesla Semi and future vehicles utilizing aspects of our next generation platfor… |
| 4 | `TSLA_FY2024_2024-12-31:194` | Item 7 › Management Opportunities, Challenges and Uncertainties and 2025 Outlook |  |  | Our capital expenditures are typically difficult to project beyond the short-term given the number and breadth of our core projects at any given time, and may further be impacted by uncertainties in future global market … |
| 5 | `TSLA_FY2020_2020-12-31:194` | Item 7 › Management Opportunities, Challenges and Risks and 2021 Outlook |  |  | Our capital expenditures are typically difficult to project beyond the short term given the number and breadth of our core projects at any given time, and uncertainties in future global market conditions resulting from t… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#1 `TSLA_FY2024_2024-12-31:240`** (cited, gold #1, gold #2)

````text
ITEM 7. MANAGEMENT’S DISCUSSION AND ANALYSIS OF FINANCIAL CONDITION AND RESULTS OF OPERATIONS > Summary of Cash Flows
Net cash flows from investing activities and their variability across each period related primarily to capital expenditures, which were $11.34 billion and $8.90 billion for the years ended December 31, 2024 and 2023, respectively, mainly for AI-related capital expenditures, global factory expansion and machinery and equipment as we expand and enhance our product roadmap. We also purchased $7.45 billion and $6.62 billion of investments, net of proceeds from maturities and sales, for the years ended December 31, 2024 and 2023, respectively. Cash Flows from Financing Activities Net cash flows from financing activities increased by $1.26 billion to $3.85 billion during the year ended December 31, 2024 from $2.59 billion during the year ended December 31, 2023. The increase was primarily due to a $1.81 billion increase in proceeds from issuances of debt, partially offset by a $1.15 billion increase in repayments of debt. See Note 10, Debt, to the consolidated financial statements included elsewhere in this Annual Report on Form 10-K for further details regarding our debt obligations. Additionally, there was an increase of $541 million in proceeds from exercises of stock options and other stock issuances compared to the prior year.
````

**#2 `TSLA_FY2020_2020-12-31:278`** (cited, gold #1, gold #2)

````text
ITEM 7. MANAGEMENT’S DISCUSSION AND ANALYSIS OF FINANCIAL CONDITION AND RESULTS OF OPERATIONS > Summary of Cash Flows
a larger increase in operating lease vehicles as Model 3 direct leasing was introduced in the second quarter of 2019 and Model Y direct leasing was introduced in the third quarter of 2020, and a larger increase in accounts receivables of government rebates already passed through to customers. Cash Flows from Investing Activities Cash flows from investing activities and their variability across each period related primarily to capital expenditures, which were $3.16 billion for the year ended December 31, 2020, mainly for Model Y production expansion at the Fremont Factory, expansion of Gigafactory Shanghai and construction of Gigafactory Berlin and Gigafactory Texas, and $1.33 billion for the year ended December 31, 2019, mainly for Gigafactory Shanghai construction, Model 3 production ramp and Model Y preparations. The increase in capital expenditures was partially offset by decreases of $32 million in business combinations, net of cash acquired, and $30 million of design, acquisition and installation of solar energy systems when compared to the prior year. Additionally, we received $123 million and $46 million, respectively, of government grants in connection with us making certain manufacturing equipment investments at Gigafactory Shanghai for the years ended December 31, 2020 and 2019, respectively.
````

</details>

RQ2 citation match (section level): `cited=[('TSLA', 'Item 7')] gold=[(None, 'Item 7')]`

### System C v1 (adaptive multi-hop)

Model: `gpt-5.4`. Hops: 3. Chunks retrieved: 10, cited: 2.

**Generated answer**

> In fiscal year 2020, Tesla’s capital expenditures were $3.16 billion and were mainly driven by factory and production expansion, specifically Model Y production expansion at the Fremont Factory, expansion of Gigafactory Shanghai, and construction of Gigafactory Berlin and Gigafactory Texas [TSLA FY2020, Item 7, TSLA_FY2020_2020-12-31:278].  
>
> In fiscal year 2024, Tesla’s capital expenditures were $11.34 billion and were mainly driven by technology-related and broader infrastructure investments, specifically AI-related capital expenditures, global factory expansion, and machinery and equipment as Tesla expanded and enhanced its product roadmap [TSLA FY2024, Item 7, TSLA_FY2024_2024-12-31:240].  
>
> So, the primary emphasis shifted from a 2020 focus centered on manufacturing footprint buildout and vehicle production capacity expansion at specific factories to a 2024 focus that still included factory expansion but placed notable weight on AI-related capital expenditures and machinery and equipment tied to product roadmap enhancement [TSLA FY2020, Item 7, TSLA_FY2020_2020-12-31:278] [TSLA FY2024, Item 7, TSLA_FY2024_2024-12-31:240].

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `TSLA_FY2020_2020-12-31:278` | Item 7 › Summary of Cash Flows | ✓ | #1, #2 | a larger increase in operating lease vehicles as Model 3 direct leasing was introduced in the second quarter of 2019 and Model Y direct leasing was introduced in the third quarter of 2020, and a larger increase in accoun… |
| 2 | `TSLA_FY2020_2020-12-31:270` | Item 7 › Liquidity and Capital Resources |  |  | As discussed in and subject to the considerations referenced in Part II, Item 7, Management's Discussion and Analysis of Financial Condition and Results of Operations—Management Opportunities, Challenges and Risks and 20… |
| 3 | `TSLA_FY2020_2020-12-31:194` | Item 7 › Management Opportunities, Challenges and Risks and 2021 Outlook |  |  | Our capital expenditures are typically difficult to project beyond the short term given the number and breadth of our core projects at any given time, and uncertainties in future global market conditions resulting from t… |
| 4 | `TSLA_FY2024_2024-12-31:194` | Item 7 › Management Opportunities, Challenges and Uncertainties and 2025 Outlook |  |  | Our capital expenditures are typically difficult to project beyond the short-term given the number and breadth of our core projects at any given time, and may further be impacted by uncertainties in future global market … |
| 5 | `TSLA_FY2024_2024-12-31:195` | Item 7 › Management Opportunities, Challenges and Uncertainties and 2025 Outlook |  |  | Our business has generally been consistently generating cash flow from operations in excess of our level of capital spend, and with better working capital management resulting in shorter days sales outstanding than days … |
| 6 | `TSLA_FY2024_2024-12-31:240` | Item 7 › Summary of Cash Flows | ✓ | #1, #2 | Net cash flows from investing activities and their variability across each period related primarily to capital expenditures, which were $11.34 billion and $8.90 billion for the years ended December 31, 2024 and 2023, res… |
| 7 | `TSLA_FY2020_2020-12-31:273` | Item 7 › Liquidity and Capital Resources |  |  | We expect that our current sources of liquidity together with our projection of cash flows from operating activities will provide us with adequate liquidity over at least the next 12 months, even considering the expected… |
| 8 | `TSLA_FY2024_2024-12-31:234` | Item 7 › Liquidity and Capital Resources |  |  | In addition, because a large portion of our future expenditures will be to fund our growth, we expect that if needed we will be able to adjust our capital and operating expenditures by operating segment. For example, if … |
| 9 | `TSLA_FY2024_2024-12-31:235` | Item 7 › Liquidity and Capital Resources |  |  | From time to time in the ordinary course of business, we enter into agreements with vendors for the purchase of components and raw materials to be used in the manufacture of our products. However, due to contractual term… |
| 10 | `TSLA_FY2020_2020-12-31:269` | Item 7 › Liquidity and Capital Resources |  |  | As of December 31, 2020, we had $19.38 billion of cash and cash equivalents. Balances held in foreign currencies had a U.S. dollar equivalent of $6.76 billion and consisted primarily of euros, Chinese yuan and Canadian d… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#1 `TSLA_FY2020_2020-12-31:278`** (cited, gold #1, gold #2)

````text
ITEM 7. MANAGEMENT’S DISCUSSION AND ANALYSIS OF FINANCIAL CONDITION AND RESULTS OF OPERATIONS > Summary of Cash Flows
a larger increase in operating lease vehicles as Model 3 direct leasing was introduced in the second quarter of 2019 and Model Y direct leasing was introduced in the third quarter of 2020, and a larger increase in accounts receivables of government rebates already passed through to customers. Cash Flows from Investing Activities Cash flows from investing activities and their variability across each period related primarily to capital expenditures, which were $3.16 billion for the year ended December 31, 2020, mainly for Model Y production expansion at the Fremont Factory, expansion of Gigafactory Shanghai and construction of Gigafactory Berlin and Gigafactory Texas, and $1.33 billion for the year ended December 31, 2019, mainly for Gigafactory Shanghai construction, Model 3 production ramp and Model Y preparations. The increase in capital expenditures was partially offset by decreases of $32 million in business combinations, net of cash acquired, and $30 million of design, acquisition and installation of solar energy systems when compared to the prior year. Additionally, we received $123 million and $46 million, respectively, of government grants in connection with us making certain manufacturing equipment investments at Gigafactory Shanghai for the years ended December 31, 2020 and 2019, respectively.
````

**#6 `TSLA_FY2024_2024-12-31:240`** (cited, gold #1, gold #2)

````text
ITEM 7. MANAGEMENT’S DISCUSSION AND ANALYSIS OF FINANCIAL CONDITION AND RESULTS OF OPERATIONS > Summary of Cash Flows
Net cash flows from investing activities and their variability across each period related primarily to capital expenditures, which were $11.34 billion and $8.90 billion for the years ended December 31, 2024 and 2023, respectively, mainly for AI-related capital expenditures, global factory expansion and machinery and equipment as we expand and enhance our product roadmap. We also purchased $7.45 billion and $6.62 billion of investments, net of proceeds from maturities and sales, for the years ended December 31, 2024 and 2023, respectively. Cash Flows from Financing Activities Net cash flows from financing activities increased by $1.26 billion to $3.85 billion during the year ended December 31, 2024 from $2.59 billion during the year ended December 31, 2023. The increase was primarily due to a $1.81 billion increase in proceeds from issuances of debt, partially offset by a $1.15 billion increase in repayments of debt. See Note 10, Debt, to the consolidated financial statements included elsewhere in this Annual Report on Form 10-K for further details regarding our debt obligations. Additionally, there was an increase of $541 million in proceeds from exercises of stock options and other stock issuances compared to the prior year.
````

</details>

RQ2 citation match (section level): `cited=[('TSLA', 'Item 7')] gold=[(None, 'Item 7')]`

**System C guardrail** (judge `gpt-5.4`): numerical claims 2, verified 2, ungrounded 0, uncited 0, derived 0; sentence verdicts: supported 1, partial 0, unsupported 0, unchecked 0.


<details><summary>Guardrail sentence verdicts</summary>

| sentence | verdict | judge reason |
|---|---|---|
| In fiscal year 2020, Tesla’s capital expenditures were $3.16 billion and were mainly driven by factory and production expansion, specifically Model Y production expansion at the Fremont Factory, expansion of Gigafactory Shanghai, and construction of Gigafactory Berlin and Gigafactory Texas [TSLA FY2020, Item 7, TSLA_FY2020_2020-12-31:278]. | None |  |
| In fiscal year 2024, Tesla’s capital expenditures were $11.34 billion and were mainly driven by technology-related and broader infrastructure investments, specifically AI-related capital expenditures, global factory expansion, and machinery and equipment as Tesla expanded and enhanced its product roadmap [TSLA FY2024, Item 7, TSLA_FY2024_2024-12-31:240]. | None |  |
| So, the primary emphasis shifted from a 2020 focus centered on manufacturing footprint buildout and vehicle production capacity expansion at specific factories to a 2024 focus that still included factory expansion but placed notable weight on AI-related capital expenditures and machinery and equipment tied to product roadmap enhancement [TSLA FY2020, Item 7, TSLA_FY2020_2020-12-31:278] [TSLA FY2024, Item 7, TSLA_FY2024_2024-12-31:240]. | supported | The 2020 evidence emphasizes factory-specific production expansion, while the 2024 evidence emphasizes AI-related capex, global factory expansion, and machinery/equipment for product roadmap enhancement. |

</details>

### System C v2 (agentic multi-hop + XBRL)

Model: `gpt-5.4`. Hops: 3. Chunks retrieved: 13, cited: 3.

**Generated answer**

> In fiscal year 2020, Tesla’s capital expenditures were $3.16 billion and were mainly for Model Y production expansion at the Fremont Factory, expansion of Gigafactory Shanghai, and construction of Gigafactory Berlin and Gigafactory Texas. [TSLA FY2020, Item 7, TSLA_FY2020_2020-12-31:278]
>
> In fiscal year 2024, Tesla’s capital expenditures were $11.34 billion and were mainly for AI-related capital expenditures, global factory expansion and machinery and equipment as Tesla expanded and enhanced its product roadmap. [TSLA FY2024, Item 7, TSLA_FY2024_2024-12-31:240]
>
> Compared with 2020, when the disclosed capex drivers were factory and production expansion projects, Tesla’s 2024 capex explicitly included technology-related investments such as AI-related capital expenditures, while still including factory expansion. [TSLA FY2020, Item 7, TSLA_FY2020_2020-12-31:278] [TSLA FY2024, Item 7, TSLA_FY2024_2024-12-31:240]
>
> Tesla also stated in its 2025 outlook that it was building or ramping manufacturing facilities on three continents, piloting the development and manufacture of new battery cell technologies, expanding its Supercharger network and investing in autonomy and other artificial intelligence enabled training and products. [TSLA FY2024, Item 7, TSLA_FY2024_2024-12-31:194]

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `TSLA_FY2020_2020-12-31:278` | Item 7 › Summary of Cash Flows | ✓ | #1, #2 | a larger increase in operating lease vehicles as Model 3 direct leasing was introduced in the second quarter of 2019 and Model Y direct leasing was introduced in the third quarter of 2020, and a larger increase in accoun… |
| 2 | `TSLA_FY2020_2020-12-31:270` | Item 7 › Liquidity and Capital Resources |  |  | As discussed in and subject to the considerations referenced in Part II, Item 7, Management's Discussion and Analysis of Financial Condition and Results of Operations—Management Opportunities, Challenges and Risks and 20… |
| 3 | `TSLA_FY2020_2020-12-31:194` | Item 7 › Management Opportunities, Challenges and Risks and 2021 Outlook |  |  | Our capital expenditures are typically difficult to project beyond the short term given the number and breadth of our core projects at any given time, and uncertainties in future global market conditions resulting from t… |
| 4 | `TSLA_FY2024_2024-12-31:194` | Item 7 › Management Opportunities, Challenges and Uncertainties and 2025 Outlook | ✓ |  | Our capital expenditures are typically difficult to project beyond the short-term given the number and breadth of our core projects at any given time, and may further be impacted by uncertainties in future global market … |
| 5 | `TSLA_FY2024_2024-12-31:195` | Item 7 › Management Opportunities, Challenges and Uncertainties and 2025 Outlook |  |  | Our business has generally been consistently generating cash flow from operations in excess of our level of capital spend, and with better working capital management resulting in shorter days sales outstanding than days … |
| 6 | `TSLA_FY2024_2024-12-31:240` | Item 7 › Summary of Cash Flows | ✓ | #1, #2 | Net cash flows from investing activities and their variability across each period related primarily to capital expenditures, which were $11.34 billion and $8.90 billion for the years ended December 31, 2024 and 2023, res… |
| 7 | `TSLA_FY2020_2020-12-31:48` | Item 1 › Gigafactory Shanghai in China |  |  | We established Gigafactory Shanghai to increase the affordability of our vehicles for customers in local markets by reducing transportation and manufacturing costs and eliminating the impact of unfavorable tariffs. We co… |
| 8 | `TSLA_FY2020_2020-12-31:450` | Item 8 › Note 8 – Property, Plant and Equipment, Net |  |  | In 2019, the Shanghai government agreed to provide $85 million of certain incentives in connection with us making certain manufacturing equipment investments at Gigafactory Shanghai, of which $46 million was received in … |
| 9 | `TSLA_FY2020_2020-12-31:97` | Item 1A › We may be impacted by macroeconomic conditions resulting from the global COVID-19 pandemic. |  |  | Our ability to increase production of our vehicles on a sustained basis, make them affordable globally by accessing local supply chains and workforces and streamline delivery logistics is dependent on the construction an… |
| 10 | `TSLA_FY2024_2024-12-31:235` | Item 7 › Liquidity and Capital Resources |  |  | From time to time in the ordinary course of business, we enter into agreements with vendors for the purchase of components and raw materials to be used in the manufacture of our products. However, due to contractual term… |
| 11 | `TSLA_FY2020_2020-12-31:269` | Item 7 › Liquidity and Capital Resources |  |  | As of December 31, 2020, we had $19.38 billion of cash and cash equivalents. Balances held in foreign currencies had a U.S. dollar equivalent of $6.76 billion and consisted primarily of euros, Chinese yuan and Canadian d… |
| 12 | `TSLA_FY2024_2024-12-31:234` | Item 7 › Liquidity and Capital Resources |  |  | In addition, because a large portion of our future expenditures will be to fund our growth, we expect that if needed we will be able to adjust our capital and operating expenditures by operating segment. For example, if … |
| 13 | `TSLA_FY2020_2020-12-31:104` | Item 1A › Risks Related to Our Operations |  |  | Our plan to grow the volume and profitability of our vehicles and energy storage products depends on significant lithium-ion battery cell production by our partner Panasonic at Gigafactory Nevada. Although Panasonic has … |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#1 `TSLA_FY2020_2020-12-31:278`** (cited, gold #1, gold #2)

````text
ITEM 7. MANAGEMENT’S DISCUSSION AND ANALYSIS OF FINANCIAL CONDITION AND RESULTS OF OPERATIONS > Summary of Cash Flows
a larger increase in operating lease vehicles as Model 3 direct leasing was introduced in the second quarter of 2019 and Model Y direct leasing was introduced in the third quarter of 2020, and a larger increase in accounts receivables of government rebates already passed through to customers. Cash Flows from Investing Activities Cash flows from investing activities and their variability across each period related primarily to capital expenditures, which were $3.16 billion for the year ended December 31, 2020, mainly for Model Y production expansion at the Fremont Factory, expansion of Gigafactory Shanghai and construction of Gigafactory Berlin and Gigafactory Texas, and $1.33 billion for the year ended December 31, 2019, mainly for Gigafactory Shanghai construction, Model 3 production ramp and Model Y preparations. The increase in capital expenditures was partially offset by decreases of $32 million in business combinations, net of cash acquired, and $30 million of design, acquisition and installation of solar energy systems when compared to the prior year. Additionally, we received $123 million and $46 million, respectively, of government grants in connection with us making certain manufacturing equipment investments at Gigafactory Shanghai for the years ended December 31, 2020 and 2019, respectively.
````

**#4 `TSLA_FY2024_2024-12-31:194`** (cited)

````text
ITEM 7. MANAGEMENT’S DISCUSSION AND ANALYSIS OF FINANCIAL CONDITION AND RESULTS OF OPERATIONS > Management Opportunities, Challenges and Uncertainties and 2025 Outlook
Our capital expenditures are typically difficult to project beyond the short-term given the number and breadth of our core projects at any given time, and may further be impacted by uncertainties in future global market conditions. We are simultaneously developing and ramping new products, building or ramping manufacturing facilities on three continents, piloting the development and manufacture of new battery cell technologies, expanding our Supercharger network and investing in autonomy and other artificial intelligence enabled training and products, and the pace of our capital spend may vary depending on overall priority among projects, the pace at which we meet milestones, production adjustments to and among our various products, increased capital efficiencies and the addition of new projects. Owing and subject to the foregoing as well as the pipeline of announced projects under development, all other continuing infrastructure growth and varying levels of inflation, we currently expect our capital expenditures to exceed $11.00 billion in 2025 and in each of the following two fiscal years.
````

**#6 `TSLA_FY2024_2024-12-31:240`** (cited, gold #1, gold #2)

````text
ITEM 7. MANAGEMENT’S DISCUSSION AND ANALYSIS OF FINANCIAL CONDITION AND RESULTS OF OPERATIONS > Summary of Cash Flows
Net cash flows from investing activities and their variability across each period related primarily to capital expenditures, which were $11.34 billion and $8.90 billion for the years ended December 31, 2024 and 2023, respectively, mainly for AI-related capital expenditures, global factory expansion and machinery and equipment as we expand and enhance our product roadmap. We also purchased $7.45 billion and $6.62 billion of investments, net of proceeds from maturities and sales, for the years ended December 31, 2024 and 2023, respectively. Cash Flows from Financing Activities Net cash flows from financing activities increased by $1.26 billion to $3.85 billion during the year ended December 31, 2024 from $2.59 billion during the year ended December 31, 2023. The increase was primarily due to a $1.81 billion increase in proceeds from issuances of debt, partially offset by a $1.15 billion increase in repayments of debt. See Note 10, Debt, to the consolidated financial statements included elsewhere in this Annual Report on Form 10-K for further details regarding our debt obligations. Additionally, there was an increase of $541 million in proceeds from exercises of stock options and other stock issuances compared to the prior year.
````

</details>

RQ2 citation match (section level): `cited=[('TSLA', 'Item 7')] gold=[(None, 'Item 7')]`

**System C guardrail** (judge `gpt-5.4`): numerical claims 2, verified 2, ungrounded 0, uncited 0, derived 0; sentence verdicts: supported 2, partial 0, unsupported 0, unchecked 0.


<details><summary>Guardrail sentence verdicts</summary>

| sentence | verdict | judge reason |
|---|---|---|
| In fiscal year 2020, Tesla’s capital expenditures were $3.16 billion and were mainly for Model Y production expansion at the Fremont Factory, expansion of Gigafactory Shanghai, and construction of Gigafactory Berlin and Gigafactory Texas. [TSLA FY2020, Item 7, TSLA_FY2020_2020-12-31:278] | None |  |
| In fiscal year 2024, Tesla’s capital expenditures were $11.34 billion and were mainly for AI-related capital expenditures, global factory expansion and machinery and equipment as Tesla expanded and enhanced its product roadmap. [TSLA FY2024, Item 7, TSLA_FY2024_2024-12-31:240] | None |  |
| Compared with 2020, when the disclosed capex drivers were factory and production expansion projects, Tesla’s 2024 capex explicitly included technology-related investments such as AI-related capital expenditures, while still including factory expansion. [TSLA FY2020, Item 7, TSLA_FY2020_2020-12-31:278] [TSLA FY2024, Item 7, TSLA_FY2024_2024-12-31:240] | supported | 2020 cites factory/production expansion projects, while 2024 explicitly adds AI-related capital expenditures alongside global factory expansion. |
| Tesla also stated in its 2025 outlook that it was building or ramping manufacturing facilities on three continents, piloting the development and manufacture of new battery cell technologies, expanding its Supercharger network and investing in autonomy and other artificial intelligence enabled training and products. [TSLA FY2024, Item 7, TSLA_FY2024_2024-12-31:194] | supported | The cited 2025 outlook states all listed activities, including facilities on three continents, battery cell technology pilots, Supercharger expansion, and AI/autonomy investments. |

</details>
