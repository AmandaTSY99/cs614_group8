# gold-028: Cross-year text

[← all cases](../README.md) · company: Meta Platforms, Inc. (META) · fiscal year: 2021 · recipe `cross_year_text` · hop `multi` · answer type `qualitative` · scope `cross_year` · RQ2 category `multi_company_comparison`

## Gold QA

**Question**

> How did Meta Platforms, Inc. expand the scope of its risk disclosures regarding privacy, safety, and content review efforts between its 2018 and 2021 fiscal year 10-K filings, specifically reflecting changes in its operational practices and external oversight mechanisms?

**Gold answer**

> In its 2018 10-K, Meta disclosed costs related to its "safety, security, and content review efforts" without specific mention of voluntary practice changes or external oversight bodies. By the 2021 10-K, the company expanded this disclosure to include costs related to "privacy, safety, security, and content review efforts" and explicitly cited "implementing changes to our practices, whether voluntarily, in connection with laws, regulations, regulatory actions, or decisions or recommendations from the independent Oversight Board." This indicates a shift from general operational costs to a more detailed recognition of regulatory and independent governance influences on its cost structure.

**Key points** (RQ3 keypoint_recall targets)

1. The 2018 disclosure referred generally to costs for safety, security, and content review efforts.
2. The 2021 disclosure added privacy to the list of cost drivers.
3. The 2021 disclosure explicitly mentions implementing changes voluntarily or in response to regulations.
4. The 2021 disclosure specifically cites decisions or recommendations from the independent Oversight Board as a factor in costs.

**Gold evidence**

1. `META_FY2021_2021-12-31` · Item 1A.Risk Factors › Our financial results will fluctuate from quarter to quarter and are difficult to predict. · text

   > costs related to our privacy, safety, security, and content review efforts, including as a result of implementing changes to our practices, whether voluntarily, in connection with laws, regulations, regulatory actions, or decisions or recommendations from the independent Oversight Board, or otherwise;

2. `META_FY2018_2018-12-31` · Item 1A. Risk Factors › Our financial results will fluctuate from quarter to quarter and are difficult to predict. · text

   > costs related to our safety, security, and content review efforts;

## Scorecard

| Metric | A (vanilla dense) | B (hybrid + rerank) | C v1 (adaptive multi-hop) | C v2 (agentic multi-hop + XBRL) |
|---|---|---|---|---|
| **Retrieval (RQ1)** | | | | |
| chunks retrieved | 10 | 5 | 13 | 13 |
| recall@5 | 0.00 | 1.00 | 1.00 | 1.00 |
| recall@all | 1.00 | 1.00 | 1.00 | 1.00 |
| complete@all | 1 | 1 | 1 | 1 |
| average precision (lexical) | 0.10 | 0.33 | 0.89 | 0.80 |
| gold evidence first rank | #1: 10, #2: 10 | #1: 4, #2: 4 | #1: 5, #2: 1 | #1: 5, #2: 1 |
| **Answer (RQ3 string match)** | | | | |
| numeric_correct | ✓ | ✗ | ✓ | ✓ |
| keypoint_recall | 0.75 | 0.00 | 0.50 | 0.50 |
| **Answer & citations (RQ2)** | | | | |
| numeric_accuracy | – | – | – | – |
| citation precision | 1.00 | – | 1.00 | 1.00 |
| citation recall | 1.00 | – | 1.00 | 1.00 |
| citation F1 | 1.00 | – | 1.00 | 1.00 |
| has a citation | 1 | 0 | 1 | 1 |
| grounding error rate | – | – | 0.00 | 0.00 |
| **Cost (RQ3)** | | | | |
| retrieval hops | 1 | 1 | 3 | 3 |
| tokens | 1964 | 1299 | 19871 | 19562 |
| cost (USD) | 0.0004 | 0.0002 | 0.0855 | 0.0835 |
| latency (s) | 4.8 | 5.7 | 45.4 | 49.6 |

Definitions: [README › Metrics](../README.md#metrics). `–` = not applicable (e.g. no gold number, no citations, no guardrail).

## System outputs

### System A (vanilla dense)

Model: `gpt-5.4-2026-03-05`. Hops: 1. Chunks retrieved: 10, cited: 2.

**Generated answer**

> In its FY2021 10-K, Meta’s risk disclosure explicitly broadened privacy, safety, security, and content review risks to include costs arising from:
>
> - “implementing changes to our practices,”
> - whether done “voluntarily,”
> - or “in connection with laws, regulations, regulatory actions,”
> - or due to “decisions or recommendations from the independent Oversight Board” [10].
>
> This shows an expanded scope that ties these risks not just to internal operations, but also to external oversight and governance mechanisms, including regulators and the independent Oversight Board [10].
>
> However, the provided context does not include the substantive FY2018 risk factor text on privacy, safety, or content review efforts—only the FY2018 table of contents is provided [3]. So I can identify the FY2021 expansion, but I cannot directly compare the exact 2018 disclosure language from the provided context.

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `META_FY2021_2021-12-31:232` | Item 3 |  |  | inquiry may issue as early as the first half of 2022. For additional information, see Part I, Item 1A, "Risk Factors—Our business is subject to complex and evolving U.S. and foreign laws and regulations regarding privacy… |
| 2 | `META_FY2021_2021-12-31:12` | TABLE OF CONTENTS |  |  | \| \| \| Page \| \|---\|---\|---\| \| Note About Forward-Looking Statements \| \| 3 \| \| Limitations of Key Metrics and Other Data \| \| 4 \| \| PART I \| \| \| \| Item 1. \| Business \| 7 \| \| Item 1A. \| Risk Factors \| 12 \| \| Item 1B. \| Unres… |
| 3 | `META_FY2018_2018-12-31:15` | TABLE OF CONTENTS | ✓ |  | \| Note About Forward-Looking Statements \| \| 3 \| \|---\|---\|---\| \| Limitations of Key Metrics and Other Data \| \| 4 \| \| PART I \| \| \| \| Item 1. \| Business \| 5 \| \| Item 1A. \| Risk Factors \| 8 \| \| Item 1B. \| Unresolved Staff Co… |
| 4 | `META_FY2021_2021-12-31:13` | TABLE OF CONTENTS |  |  | \| \| \| Page \| \|---\|---\|---\| \| Item 9B. \| Other Information \| 110 \| \| Item 9C. \| Disclosure Regarding Foreign Jurisdictions that Prevent Inspections \| 110 \| \| PART III \| \| \| \| Item 10. \| Directors, Executive Officers and C… |
| 5 | `META_FY2021_2021-12-31:15` | NOTE ABOUT FORWARD-LOOKING STATEMENTS |  |  | those contained in any forward-looking statements we may make. In light of these risks, uncertainties and assumptions, the future events and trends discussed in this Annual Report on Form 10-K may not occur and actual re… |
| 6 | `META_FY2021_2021-12-31:483` | Item 8 › Legal and Related Matters |  |  | We are also subject to other government inquiries and investigations relating to our business activities and disclosure practices. For example, beginning in September 2021, we became subject to government investigations … |
| 7 | `META_FY2021_2021-12-31:530` | Item 9C |  |  | Not Applicable. |
| 8 | `META_FY2021_2021-12-31:238` | Item 4 |  |  | Not applicable. |
| 9 | `META_FY2021_2021-12-31:49` | Item 1 › Government Regulation |  |  | For additional information about government regulation applicable to our business, see Part I, Item 1A, "Risk Factors" in this Annual Report on Form 10-K. |
| 10 | `META_FY2021_2021-12-31:114` | Item 1A › Our financial results will fluctuate from quarter to quarter and are difficult to predict. | ✓ | #1, #2 | •costs related to our privacy, safety, security, and content review efforts, including as a result of implementing changes to our practices, whether voluntarily, in connection with laws, regulations, regulatory actions, … |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#3 `META_FY2018_2018-12-31:15`** (cited)

````text
TABLE OF CONTENTS (table)
| Note About Forward-Looking Statements |  | 3 |
|---|---|---|
| Limitations of Key Metrics and Other Data |  | 4 |
| PART I |  |  |
| Item 1. | Business | 5 |
| Item 1A. | Risk Factors | 8 |
| Item 1B. | Unresolved Staff Comments | 30 |
| Item 2. | Properties | 30 |
| Item 3. | Legal Proceedings | 30 |
| Item 4. | Mine Safety Disclosures | 30 |
| PART II |  |  |
| Item 5. | Market for Registrant's Common Equity, Related Stockholder Matters and Issuer Purchases of Equity Securities | 31 |
| Item 6. | Selected Financial Data | 33 |
| Item 7. | Management's Discussion and Analysis of Financial Condition and Results of Operations | 35 |
| Item 7A. | Quantitative and Qualitative Disclosures About Market Risk | 54 |
| Item 8. | Financial Statements and Supplementary Data | 55 |
| Item 9. | Changes in and Disagreements with Accountants on Accounting and Financial Disclosure | 84 |
| Item 9A. | Controls and Procedures | 84 |
| Item 9B. | Other Information | 84 |
````

**#10 `META_FY2021_2021-12-31:114`** (cited, gold #1, gold #2)

````text
Item 1A.Risk Factors > Our financial results will fluctuate from quarter to quarter and are difficult to predict.
•costs related to our privacy, safety, security, and content review efforts, including as a result of implementing changes to our practices, whether voluntarily, in connection with laws, regulations, regulatory actions, or decisions or recommendations from the independent Oversight Board, or otherwise; •costs and expenses related to the development, manufacturing, and delivery of our consumer hardware products; •our ability to maintain gross margins and operating margins; •costs related to acquisitions, including costs associated with amortization and additional investments to develop the acquired technologies; •charges associated with impairment of any assets on our balance sheet; •our ability to obtain equipment, components, and labor for our data centers and other technical infrastructure in a timely and cost-effective manner; •system failures or outages or government blocking, which could prevent us from serving ads for any period of time; •breaches of security or privacy, and the costs associated with any such breaches and remediation; •changes in the manner in which we distribute our products or inaccessibility of our products due to third-party actions; •fees paid to third parties for content or the distribution of our products; •refunds or other concessions provided to advertisers; •share-based compensation expense, including acquisition-related expense;
````

</details>

RQ2 citation match (section level): `cited=[('META', 'Item 1A')] gold=[(None, 'Item 1A')]`

### System B (hybrid + rerank)

Model: `gpt-5.4-2026-03-05`. Hops: 1. Chunks retrieved: 5, cited: 0.

**Generated answer**

> Not found in the provided context.

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `META_FY2021_2021-12-31:55` | Item 1 › Corporate Information |  |  | We were incorporated in Delaware in July 2004. We completed our initial public offering in May 2012 and our Class A common stock is currently listed on the Nasdaq Global Select Market under the symbol "FB." In October 20… |
| 2 | `META_FY2021_2021-12-31:392` | Item 8 › Organization and Description of Business |  |  | We were incorporated in Delaware in July 2004. In October 2021, we changed our corporate name from Facebook, Inc. to Meta Platforms, Inc. Our mission is to give people the power to build community and bring the world clo… |
| 3 | `META_FY2021_2021-12-31:16` | NOTE ABOUT FORWARD-LOOKING STATEMENTS |  |  | In October 2021, we changed our corporate name from Facebook, Inc. to Meta Platforms, Inc. We will not distinguish between our prior and current corporate name and will refer to our current corporate name throughout this… |
| 4 | `META_FY2021_2021-12-31:114` | Item 1A › Our financial results will fluctuate from quarter to quarter and are difficult to predict. |  | #1, #2 | •costs related to our privacy, safety, security, and content review efforts, including as a result of implementing changes to our practices, whether voluntarily, in connection with laws, regulations, regulatory actions, … |
| 5 | `META_FY2021_2021-12-31:206` | Item 1A › Risks Related to Data, Security, and Intellectual Property |  | #2 | In addition to our efforts to mitigate cybersecurity risks, we are making significant investments in privacy, safety, security, and content review efforts to combat misuse of our services and user data by third parties, … |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#4 `META_FY2021_2021-12-31:114`** (gold #1, gold #2)

````text
Item 1A.Risk Factors > Our financial results will fluctuate from quarter to quarter and are difficult to predict.
•costs related to our privacy, safety, security, and content review efforts, including as a result of implementing changes to our practices, whether voluntarily, in connection with laws, regulations, regulatory actions, or decisions or recommendations from the independent Oversight Board, or otherwise; •costs and expenses related to the development, manufacturing, and delivery of our consumer hardware products; •our ability to maintain gross margins and operating margins; •costs related to acquisitions, including costs associated with amortization and additional investments to develop the acquired technologies; •charges associated with impairment of any assets on our balance sheet; •our ability to obtain equipment, components, and labor for our data centers and other technical infrastructure in a timely and cost-effective manner; •system failures or outages or government blocking, which could prevent us from serving ads for any period of time; •breaches of security or privacy, and the costs associated with any such breaches and remediation; •changes in the manner in which we distribute our products or inaccessibility of our products due to third-party actions; •fees paid to third parties for content or the distribution of our products; •refunds or other concessions provided to advertisers; •share-based compensation expense, including acquisition-related expense;
````

**#5 `META_FY2021_2021-12-31:206`** (gold #2)

````text
Item 1A.Risk Factors > Risks Related to Data, Security, and Intellectual Property
In addition to our efforts to mitigate cybersecurity risks, we are making significant investments in privacy, safety, security, and content review efforts to combat misuse of our services and user data by third parties, including investigations and audits of platform applications, as well as other enforcement efforts. As a result of these efforts we have discovered and announced, and anticipate that we will continue to discover and announce, additional incidents of misuse of user data or other undesirable activity by third parties. We may not discover all such incidents or activity, whether as a result of our data or technical limitations, including our lack of visibility over our encrypted services, the scale of activity on our platform, challenges related to our personnel working remotely during the COVID-19 pandemic, the allocation of resources to other projects, or other factors, and we may be notified of such incidents or activity by the independent privacy assessor required under our modified consent order with the FTC, the media, or other third parties. Such incidents and activities have in the past, and may in the future, include the use of user data or our systems in a manner inconsistent with our terms, contracts or policies,
````

</details>

RQ2 citation match (section level): `no citations`

### System C v1 (adaptive multi-hop)

Model: `gpt-5.4`. Hops: 3. Chunks retrieved: 13, cited: 4.

**Generated answer**

> In its 2018 filing, Meta disclosed that it was making significant investments in safety, security, and content review efforts to combat misuse of its services and user data by third parties, including investigations and audits of platform applications that previously accessed information of a large number of users of its services. [META FY2018, Item 1A, META_FY2018_2018-12-31:74]
>
> The 2018 disclosure focused on discovering and announcing additional incidents of misuse of user data or other undesirable third-party activity, noted that Meta might not discover all such incidents because of data limitations or the scale of activity on its platform, and said it might instead learn of them via the media or other third parties. [META FY2018, Item 1A, META_FY2018_2018-12-31:74]
>
> The 2018 filing also described the types of harmful activity more specifically as including misuse of user data inconsistent with Meta’s terms, contracts, or policies, false or undesirable user accounts, election interference, improper ad purchases, threats to people’s safety on- or offline, and spamming, scraping, or spreading misinformation. [META FY2018, Item 1A, META_FY2018_2018-12-31:74]
>
> By 2021, Meta expanded this disclosure by stating that it was making significant investments not only in privacy, safety, security, and content review efforts, but also in enforcement efforts, while continuing investigations and audits of platform applications. [META FY2021, Item 1A, META_FY2021_2021-12-31:206]
>
> The 2021 filing broadened the operational limitations it identified by stating that Meta might not discover all incidents because of data or technical limitations, lack of visibility over encrypted services, the scale of activity on its platform, challenges related to personnel working remotely during the COVID-19 pandemic, allocation of resources to other projects, or other factors. [META FY2021, Item 1A, META_FY2021_2021-12-31:206]
>
> Meta also expanded the external oversight mechanisms described in 2021 by stating that it could be notified of incidents or activity by the independent privacy assessor required under its modified consent order with the FTC, in addition to the media or other third parties. [META FY2021, Item 1A, META_FY2021_2021-12-31:206]
>
> The 2021 filing further reflected a more formalized compliance and oversight structure by disclosing ongoing privacy compliance and oversight efforts tied to its modified FTC consent order, GDPR, CCPA, and ePrivacy Directive. [META FY2021, Item 1A, META_FY2021_2021-12-31:187]
>
> Meta stated that its FTC consent order required it to maintain a comprehensive privacy program that included substantial management and board of directors oversight, stringent operational requirements and reporting obligations, prohibitions against misrepresentations relating to user data, regular certifications of compliance to the FTC, and regular assessments by an independent third-party assessor. [META FY2021, Item 1A, META_FY2021_2021-12-31:187]
>
> The 2021 filing also explained that these compliance and oversight efforts were increasing demand on Meta’s systems and resources, required significant new and ongoing investments in compliance processes, personnel, and technical infrastructure, and caused internal resource reallocation that had adversely affected and would continue to adversely affect other business initiatives. [META FY2021, Item 1A, META_FY2021_2021-12-31:187]
>
> Meta additionally disclosed in 2021 that these efforts required substantial modifications to its business practices, made some practices such as product and ads development more difficult, time-consuming, and costly, and adversely affected its ability to develop and launch new features, products, and services in a timely manner. [META FY2021, Item 1A, META_FY2021_2021-12-31:187] [META FY2021, Item 1A, META_FY2021_2021-12-31:188]
>
> The 2021 filing also emphasized that Meta expected significant time and attention from management and the board of directors would be required for these privacy compliance and oversight efforts. [META FY2021, Item 1A, META_FY2021_2021-12-31:188]
>
> Compared with 2018, the 2021 filing therefore expanded the scope of risk disclosure from investments aimed at detecting misuse and harmful activity on the platform to a broader framework that included formal privacy governance, operational restructuring, independent assessment, board-level oversight, and ongoing regulatory supervision under the FTC consent order and other privacy regimes. [META FY2018, Item 1A, META_FY2018_2018-12-31:74] [META FY2021, Item 1A, META_FY2021_2021-12-31:206] [META FY2021, Item 1A, META_FY2021_2021-12-31:187] [META FY2021, Item 1A, META_FY2021_2021-12-31:188]

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `META_FY2021_2021-12-31:206` | Item 1A › Risks Related to Data, Security, and Intellectual Property | ✓ | #2 | In addition to our efforts to mitigate cybersecurity risks, we are making significant investments in privacy, safety, security, and content review efforts to combat misuse of our services and user data by third parties, … |
| 2 | `META_FY2018_2018-12-31:74` | Item 1A › Our new products and changes to existing products could fail to attract or retain users or generate revenue and profits. | ✓ | #2 | In addition to our efforts to mitigate cybersecurity risks, we are making significant investments in safety, security, and content review efforts to combat misuse of our services and user data by third parties, including… |
| 3 | `META_FY2021_2021-12-31:232` | Item 3 |  |  | inquiry may issue as early as the first half of 2022. For additional information, see Part I, Item 1A, "Risk Factors—Our business is subject to complex and evolving U.S. and foreign laws and regulations regarding privacy… |
| 4 | `META_FY2021_2021-12-31:205` | Item 1A › Risks Related to Data, Security, and Intellectual Property |  | #2 | For example, in September 2018, we announced our discovery of a third-party cyber-attack that exploited a vulnerability in Facebook's code to steal user access tokens, which were then used to access certain profile infor… |
| 5 | `META_FY2021_2021-12-31:114` | Item 1A › Our financial results will fluctuate from quarter to quarter and are difficult to predict. |  | #1, #2 | •costs related to our privacy, safety, security, and content review efforts, including as a result of implementing changes to our practices, whether voluntarily, in connection with laws, regulations, regulatory actions, … |
| 6 | `META_FY2021_2021-12-31:41` | Item 1 › Government Regulation |  |  | We are subject to a variety of laws and regulations in the United States and abroad that involve matters central to our business, many of which are still evolving and being tested in courts, and could be interpreted in w… |
| 7 | `META_FY2021_2021-12-31:61` | Item 1A › Risks Related to Government Regulation and Enforcement |  |  | •government restrictions on access to Facebook or our other products, or other actions that impair our ability to sell advertising, in their countries; •complex and evolving U.S. and foreign privacy, data use and data pr… |
| 8 | `META_FY2021_2021-12-31:187` | Item 1A › Risks Related to Government Regulation and Enforcement | ✓ |  | We are engaged in ongoing privacy compliance and oversight efforts, including in connection with our modified consent order with the FTC, requirements of the GDPR, and other regulatory and legislative requirements around… |
| 9 | `META_FY2021_2021-12-31:173` | Item 1A › Risks Related to Government Regulation and Enforcement |  |  | We are subject to a variety of laws and regulations in the United States and abroad that involve matters central to our business, including privacy, data use, data protection and personal information, biometrics, encrypt… |
| 10 | `META_FY2021_2021-12-31:188` | Item 1A › Risks Related to Government Regulation and Enforcement | ✓ |  | difficult, time-consuming, and costly. As a result, we believe our ability to develop and launch new features, products, and services in a timely manner has been and will continue to be adversely affected. We also expect… |
| 11 | `META_FY2021_2021-12-31:186` | Item 1A › Risks Related to Government Regulation and Enforcement |  |  | Compliance with our FTC consent order, the GDPR, the CCPA, the ePrivacy Directive, and other regulatory and legislative privacy requirements require significant operational resources and modifications to our business pra… |
| 12 | `META_FY2021_2021-12-31:48` | Item 1 › Government Regulation |  |  | We are, and expect to continue to be, the subject of investigations, inquiries, data requests, requests for information, actions, and audits by government authorities and regulators in the United States, Europe, and arou… |
| 13 | `META_FY2021_2021-12-31:183` | Item 1A › Risks Related to Government Regulation and Enforcement |  |  | in violation of our terms and policies. In July 2019, we entered into a settlement and modified consent order to resolve the FTC inquiry, which was approved by the federal court and took effect in April 2020. Among other… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#1 `META_FY2021_2021-12-31:206`** (cited, gold #2)

````text
Item 1A.Risk Factors > Risks Related to Data, Security, and Intellectual Property
In addition to our efforts to mitigate cybersecurity risks, we are making significant investments in privacy, safety, security, and content review efforts to combat misuse of our services and user data by third parties, including investigations and audits of platform applications, as well as other enforcement efforts. As a result of these efforts we have discovered and announced, and anticipate that we will continue to discover and announce, additional incidents of misuse of user data or other undesirable activity by third parties. We may not discover all such incidents or activity, whether as a result of our data or technical limitations, including our lack of visibility over our encrypted services, the scale of activity on our platform, challenges related to our personnel working remotely during the COVID-19 pandemic, the allocation of resources to other projects, or other factors, and we may be notified of such incidents or activity by the independent privacy assessor required under our modified consent order with the FTC, the media, or other third parties. Such incidents and activities have in the past, and may in the future, include the use of user data or our systems in a manner inconsistent with our terms, contracts or policies,
````

**#2 `META_FY2018_2018-12-31:74`** (cited, gold #2)

````text
Item 1A. Risk Factors > Our new products and changes to existing products could fail to attract or retain users or generate revenue and profits.
In addition to our efforts to mitigate cybersecurity risks, we are making significant investments in safety, security, and content review efforts to combat misuse of our services and user data by third parties, including investigations and audits of platform applications that previously accessed information of a large number of users of our services. As a result of these efforts we have discovered and announced, and anticipate that we will continue to discover and announce, additional incidents of misuse of user data or other undesirable activity by third parties. We may not discover all such incidents or activity, including as a result of our data limitations or the scale of activity on our platform, and we may be notified of such incidents or activity via the media or other third parties. Such incidents and activities may include the use of user data in a manner inconsistent with our terms, contracts or policies, the existence of false or undesirable user accounts, election interference, improper ad purchases, activities that threaten people’s safety on- or offline, or instances of spamming, scraping, or spreading misinformation. The discovery of the foregoing may negatively affect user trust and engagement, harm our reputation and brands, require us to
````

**#4 `META_FY2021_2021-12-31:205`** (gold #2)

````text
Item 1A.Risk Factors > Risks Related to Data, Security, and Intellectual Property
For example, in September 2018, we announced our discovery of a third-party cyber-attack that exploited a vulnerability in Facebook's code to steal user access tokens, which were then used to access certain profile information from approximately 29 million user accounts on Facebook. The events surrounding this cyber-attack became the subject of Irish Data Protection Commission and other government inquiries. Any such inquiries could subject us to substantial fines and costs, require us to change our business practices, divert resources and the attention of management from our business, or adversely affect our business. We anticipate that our ongoing efforts related to privacy, safety, security, and content review will identify additional instances of misuse of user data or other undesirable activity by third parties on our platform.
````

**#5 `META_FY2021_2021-12-31:114`** (gold #1, gold #2)

````text
Item 1A.Risk Factors > Our financial results will fluctuate from quarter to quarter and are difficult to predict.
•costs related to our privacy, safety, security, and content review efforts, including as a result of implementing changes to our practices, whether voluntarily, in connection with laws, regulations, regulatory actions, or decisions or recommendations from the independent Oversight Board, or otherwise; •costs and expenses related to the development, manufacturing, and delivery of our consumer hardware products; •our ability to maintain gross margins and operating margins; •costs related to acquisitions, including costs associated with amortization and additional investments to develop the acquired technologies; •charges associated with impairment of any assets on our balance sheet; •our ability to obtain equipment, components, and labor for our data centers and other technical infrastructure in a timely and cost-effective manner; •system failures or outages or government blocking, which could prevent us from serving ads for any period of time; •breaches of security or privacy, and the costs associated with any such breaches and remediation; •changes in the manner in which we distribute our products or inaccessibility of our products due to third-party actions; •fees paid to third parties for content or the distribution of our products; •refunds or other concessions provided to advertisers; •share-based compensation expense, including acquisition-related expense;
````

**#8 `META_FY2021_2021-12-31:187`** (cited)

````text
Item 1A.Risk Factors > Risks Related to Government Regulation and Enforcement
We are engaged in ongoing privacy compliance and oversight efforts, including in connection with our modified consent order with the FTC, requirements of the GDPR, and other regulatory and legislative requirements around the world, such as the CCPA and the ePrivacy Directive. In particular, we are maintaining a comprehensive privacy program in connection with the FTC consent order that includes substantial management and board of directors oversight, stringent operational requirements and reporting obligations, prohibitions against making misrepresentations relating to user data, a process to regularly certify our compliance with the privacy program to the FTC, and regular assessments of our privacy program by an independent third-party assessor, which has been and will continue to be challenging and costly to maintain and enhance. These compliance and oversight efforts are increasing demand on our systems and resources, and require significant new and ongoing investments, including investments in compliance processes, personnel, and technical infrastructure. We are reallocating resources internally to assist with these efforts, and this has had, and will continue to have, an adverse impact on our other business initiatives. In addition, these efforts require substantial modifications to our business practices and make some practices such as product and ads development more
````

**#10 `META_FY2021_2021-12-31:188`** (cited)

````text
Item 1A.Risk Factors > Risks Related to Government Regulation and Enforcement
difficult, time-consuming, and costly. As a result, we believe our ability to develop and launch new features, products, and services in a timely manner has been and will continue to be adversely affected. We also expect that our privacy compliance and oversight efforts will require significant time and attention from our management and board of directors. The requirements of the FTC consent order and other privacy-related laws and regulations are complex and apply broadly to our business, and from time to time we notify relevant authorities of instances where we are not in full compliance with these requirements or otherwise discover privacy issues, and we expect to continue to do so as any such issues arise in the future. In addition, regulatory and legislative privacy requirements are constantly evolving and can be subject to significant change and uncertain interpretation. If we are unable to successfully implement and comply with the mandates of the FTC consent order, GDPR, CCPA, ePrivacy Directive, or other regulatory or legislative requirements, or if we are found to be in violation of the consent order or other applicable requirements, we may be subject to regulatory or governmental investigations or lawsuits, which may result in significant monetary
````

</details>

RQ2 citation match (section level): `cited=[('META', 'Item 1A')] gold=[(None, 'Item 1A')]`

**System C guardrail** (judge `gpt-5.4`): numerical claims 0, verified 0, ungrounded 0, uncited 0, derived 0; sentence verdicts: supported 12, partial 0, unsupported 0, unchecked 0.


<details><summary>Guardrail sentence verdicts</summary>

| sentence | verdict | judge reason |
|---|---|---|
| In its 2018 filing, Meta disclosed that it was making significant investments in safety, security, and content review efforts to combat misuse of its services and user data by third parties, including investigations and audits of platform applications that previously accessed information of a large number of users of its services. [META FY2018, Item 1A, META_FY2018_2018-12-31:74] | supported | The cited 2018 text states significant investments in safety, security, and content review, including investigations and audits of platform applications that previously accessed many users' information. |
| The 2018 disclosure focused on discovering and announcing additional incidents of misuse of user data or other undesirable third-party activity, noted that Meta might not discover all such incidents because of data limitations or the scale of activity on its platform, and said it might instead learn of them via the media or other third parties. [META FY2018, Item 1A, META_FY2018_2018-12-31:74] | supported | The evidence expressly says Meta expected to discover and announce additional incidents, might not discover all due to data limitations or scale, and might learn of them via media or other third parties. |
| The 2018 filing also described the types of harmful activity more specifically as including misuse of user data inconsistent with Meta’s terms, contracts, or policies, false or undesirable user accounts, election interference, improper ad purchases, threats to people’s safety on- or offline, and spamming, scraping, or spreading misinformation. [META FY2018, Item 1A, META_FY2018_2018-12-31:74] | supported | The cited passage lists each of those harmful activities as examples. |
| By 2021, Meta expanded this disclosure by stating that it was making significant investments not only in privacy, safety, security, and content review efforts, but also in enforcement efforts, while continuing investigations and audits of platform applications. [META FY2021, Item 1A, META_FY2021_2021-12-31:206] | supported | The 2021 evidence states investments in privacy, safety, security, and content review, including investigations and audits of platform applications, as well as other enforcement efforts. |
| The 2021 filing broadened the operational limitations it identified by stating that Meta might not discover all incidents because of data or technical limitations, lack of visibility over encrypted services, the scale of activity on its platform, challenges related to personnel working remotely during the COVID-19 pandemic, allocation of resources to other projects, or other factors. [META FY2021, Item 1A, META_FY2021_2021-12-31:206] | supported | The cited 2021 text explicitly lists all of those reasons Meta might not discover all incidents. |
| Meta also expanded the external oversight mechanisms described in 2021 by stating that it could be notified of incidents or activity by the independent privacy assessor required under its modified consent order with the FTC, in addition to the media or other third parties. [META FY2021, Item 1A, META_FY2021_2021-12-31:206] | supported | The evidence says Meta may be notified by the independent privacy assessor required under the modified FTC consent order, the media, or other third parties. |
| The 2021 filing further reflected a more formalized compliance and oversight structure by disclosing ongoing privacy compliance and oversight efforts tied to its modified FTC consent order, GDPR, CCPA, and ePrivacy Directive. [META FY2021, Item 1A, META_FY2021_2021-12-31:187] | supported | The 2021 filing states ongoing privacy compliance and oversight efforts in connection with the modified FTC consent order, GDPR, CCPA, and the ePrivacy Directive. |
| Meta stated that its FTC consent order required it to maintain a comprehensive privacy program that included substantial management and board of directors oversight, stringent operational requirements and reporting obligations, prohibitions against misrepresentations relating to user data, regular certifications of compliance to the FTC, and regular assessments by an independent third-party assessor. [META FY2021, Item 1A, META_FY2021_2021-12-31:187] | supported | The cited passage describes the comprehensive privacy program as including each listed oversight, reporting, certification, and independent assessment element. |
| The 2021 filing also explained that these compliance and oversight efforts were increasing demand on Meta’s systems and resources, required significant new and ongoing investments in compliance processes, personnel, and technical infrastructure, and caused internal resource reallocation that had adversely affected and would continue to adversely affect other business initiatives. [META FY2021, Item 1A, META_FY2021_2021-12-31:187] | supported | The evidence states these efforts increase demand on systems and resources, require significant investments, and have had and will continue to have an adverse impact on other business initiatives due to resource reallocation. |
| Meta additionally disclosed in 2021 that these efforts required substantial modifications to its business practices, made some practices such as product and ads development more difficult, time-consuming, and costly, and adversely affected its ability to develop and launch new features, products, and services in a timely manner. [META FY2021, Item 1A, META_FY2021_2021-12-31:187] [META FY2021, Item 1A, META_FY2021_2021-12-31:188] | supported | Across the two cited excerpts, the filing says these efforts require substantial business-practice modifications, make product and ads development more difficult, time-consuming, and costly, and adversely affect timely launches. |
| The 2021 filing also emphasized that Meta expected significant time and attention from management and the board of directors would be required for these privacy compliance and oversight efforts. [META FY2021, Item 1A, META_FY2021_2021-12-31:188] | supported | The cited text explicitly says privacy compliance and oversight efforts will require significant time and attention from management and the board of directors. |
| Compared with 2018, the 2021 filing therefore expanded the scope of risk disclosure from investments aimed at detecting misuse and harmful activity on the platform to a broader framework that included formal privacy governance, operational restructuring, independent assessment, board-level oversight, and ongoing regulatory supervision under the FTC consent order and other privacy regimes. [META FY2018, Item 1A, META_FY2018_2018-12-31:74] [META FY2021, Item 1A, META_FY2021_2021-12-31:206] [META FY2021, Item 1A, META_FY2021_2021-12-31:187] [META FY2021, Item 1A, META_FY2021_2021-12-31:188] | supported | Taken together, the 2018 and 2021 excerpts support that 2021 broadened disclosure from misuse-detection investments to formal privacy governance, operational changes, independent assessment, board oversight, and regulatory compliance obligations. |

</details>

### System C v2 (agentic multi-hop + XBRL)

Model: `gpt-5.4`. Hops: 3. Chunks retrieved: 13, cited: 4.

**Generated answer**

> In its 2018 Form 10-K, Meta disclosed that it was making significant investments in safety, security, and content review efforts to combat misuse of its services and user data by third parties, including investigations and audits of platform applications that previously accessed information of a large number of users of its services. [META FY2018, Item 1A, META_FY2018_2018-12-31:74]
>
> The 2018 disclosure focused on the possibility that these efforts would uncover additional incidents of misuse of user data or other undesirable third-party activity, including false or undesirable user accounts, election interference, improper ad purchases, threats to people’s safety, and spamming, scraping, or spreading misinformation. [META FY2018, Item 1A, META_FY2018_2018-12-31:74]
>
> By 2021, Meta expanded this disclosure by stating that it was making significant investments not only in privacy, safety, security, and content review efforts, but also in enforcement efforts, and that these efforts included investigations and audits of platform applications as well as other enforcement efforts. [META FY2021, Item 1A, META_FY2021_2021-12-31:206]
>
> The 2021 filing also broadened the operational limitations it identified, stating that Meta may not discover all such incidents because of data or technical limitations, lack of visibility over encrypted services, the scale of activity on its platform, challenges related to personnel working remotely during the COVID-19 pandemic, the allocation of resources to other projects, or other factors. [META FY2021, Item 1A, META_FY2021_2021-12-31:206]
>
> Meta further expanded the external oversight dimension in 2021 by disclosing that it may be notified of incidents or activity by the independent privacy assessor required under its modified consent order with the FTC, in addition to the media or other third parties. [META FY2021, Item 1A, META_FY2021_2021-12-31:206]
>
> The 2021 filing also described a much more formalized compliance and oversight structure tied to external regulation, stating that it was engaged in ongoing privacy compliance and oversight efforts in connection with its modified consent order with the FTC, the GDPR, the CCPA, and the ePrivacy Directive. [META FY2021, Item 1A, META_FY2021_2021-12-31:187]
>
> Meta said that, in connection with the FTC consent order, it was maintaining a comprehensive privacy program that included substantial management and board of directors oversight, stringent operational requirements and reporting obligations, prohibitions against making misrepresentations relating to user data, a process to regularly certify compliance to the FTC, and regular assessments of its privacy program by an independent third-party assessor. [META FY2021, Item 1A, META_FY2021_2021-12-31:187]
>
> The company also disclosed in 2021 that these compliance and oversight efforts were increasing demand on its systems and resources, requiring significant new and ongoing investments in compliance processes, personnel, and technical infrastructure, and causing internal resource reallocation that had adversely affected and would continue to adversely affect other business initiatives. [META FY2021, Item 1A, META_FY2021_2021-12-31:187]
>
> In addition, Meta stated that these efforts required substantial modifications to its business practices and made some practices such as product and ads development more difficult, time-consuming, and costly, and that its ability to develop and launch new features, products, and services in a timely manner had been and would continue to be adversely affected. [META FY2021, Item 1A, META_FY2021_2021-12-31:187] [META FY2021, Item 1A, META_FY2021_2021-12-31:188]
>
> The 2021 filing also added that Meta expected its privacy compliance and oversight efforts to require significant time and attention from management and the board of directors, and that failures to comply with the FTC consent order or other privacy requirements could lead to regulatory or governmental investigations or lawsuits and significant monetary penalties. [META FY2021, Item 1A, META_FY2021_2021-12-31:188]
>
> Meta’s 2021 risk disclosures therefore expanded from a 2018 emphasis on internal investments to detect misuse and harmful activity into a broader framework that explicitly incorporated privacy-focused operational changes, formal compliance infrastructure, board-level governance, independent third-party assessment, and ongoing oversight by regulators under the FTC consent order and other privacy regimes. [META FY2018, Item 1A, META_FY2018_2018-12-31:74] [META FY2021, Item 1A, META_FY2021_2021-12-31:206] [META FY2021, Item 1A, META_FY2021_2021-12-31:187] [META FY2021, Item 1A, META_FY2021_2021-12-31:188]

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `META_FY2021_2021-12-31:206` | Item 1A › Risks Related to Data, Security, and Intellectual Property | ✓ | #2 | In addition to our efforts to mitigate cybersecurity risks, we are making significant investments in privacy, safety, security, and content review efforts to combat misuse of our services and user data by third parties, … |
| 2 | `META_FY2018_2018-12-31:74` | Item 1A › Our new products and changes to existing products could fail to attract or retain users or generate revenue and profits. | ✓ | #2 | In addition to our efforts to mitigate cybersecurity risks, we are making significant investments in safety, security, and content review efforts to combat misuse of our services and user data by third parties, including… |
| 3 | `META_FY2021_2021-12-31:232` | Item 3 |  |  | inquiry may issue as early as the first half of 2022. For additional information, see Part I, Item 1A, "Risk Factors—Our business is subject to complex and evolving U.S. and foreign laws and regulations regarding privacy… |
| 4 | `META_FY2021_2021-12-31:205` | Item 1A › Risks Related to Data, Security, and Intellectual Property |  | #2 | For example, in September 2018, we announced our discovery of a third-party cyber-attack that exploited a vulnerability in Facebook's code to steal user access tokens, which were then used to access certain profile infor… |
| 5 | `META_FY2021_2021-12-31:114` | Item 1A › Our financial results will fluctuate from quarter to quarter and are difficult to predict. |  | #1, #2 | •costs related to our privacy, safety, security, and content review efforts, including as a result of implementing changes to our practices, whether voluntarily, in connection with laws, regulations, regulatory actions, … |
| 6 | `META_FY2021_2021-12-31:41` | Item 1 › Government Regulation |  |  | We are subject to a variety of laws and regulations in the United States and abroad that involve matters central to our business, many of which are still evolving and being tested in courts, and could be interpreted in w… |
| 7 | `META_FY2021_2021-12-31:61` | Item 1A › Risks Related to Government Regulation and Enforcement |  |  | •government restrictions on access to Facebook or our other products, or other actions that impair our ability to sell advertising, in their countries; •complex and evolving U.S. and foreign privacy, data use and data pr… |
| 8 | `META_FY2021_2021-12-31:187` | Item 1A › Risks Related to Government Regulation and Enforcement | ✓ |  | We are engaged in ongoing privacy compliance and oversight efforts, including in connection with our modified consent order with the FTC, requirements of the GDPR, and other regulatory and legislative requirements around… |
| 9 | `META_FY2021_2021-12-31:188` | Item 1A › Risks Related to Government Regulation and Enforcement | ✓ |  | difficult, time-consuming, and costly. As a result, we believe our ability to develop and launch new features, products, and services in a timely manner has been and will continue to be adversely affected. We also expect… |
| 10 | `META_FY2021_2021-12-31:173` | Item 1A › Risks Related to Government Regulation and Enforcement |  |  | We are subject to a variety of laws and regulations in the United States and abroad that involve matters central to our business, including privacy, data use, data protection and personal information, biometrics, encrypt… |
| 11 | `META_FY2021_2021-12-31:204` | Item 1A › Risks Related to Data, Security, and Intellectual Property |  | #2 | significant costs in protecting against or remediating such incidents. In addition, we are subject to a variety of laws and regulations in the United States and abroad relating to cybersecurity and data protection, as we… |
| 12 | `META_FY2021_2021-12-31:186` | Item 1A › Risks Related to Government Regulation and Enforcement |  |  | Compliance with our FTC consent order, the GDPR, the CCPA, the ePrivacy Directive, and other regulatory and legislative privacy requirements require significant operational resources and modifications to our business pra… |
| 13 | `META_FY2021_2021-12-31:183` | Item 1A › Risks Related to Government Regulation and Enforcement |  |  | in violation of our terms and policies. In July 2019, we entered into a settlement and modified consent order to resolve the FTC inquiry, which was approved by the federal court and took effect in April 2020. Among other… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#1 `META_FY2021_2021-12-31:206`** (cited, gold #2)

````text
Item 1A.Risk Factors > Risks Related to Data, Security, and Intellectual Property
In addition to our efforts to mitigate cybersecurity risks, we are making significant investments in privacy, safety, security, and content review efforts to combat misuse of our services and user data by third parties, including investigations and audits of platform applications, as well as other enforcement efforts. As a result of these efforts we have discovered and announced, and anticipate that we will continue to discover and announce, additional incidents of misuse of user data or other undesirable activity by third parties. We may not discover all such incidents or activity, whether as a result of our data or technical limitations, including our lack of visibility over our encrypted services, the scale of activity on our platform, challenges related to our personnel working remotely during the COVID-19 pandemic, the allocation of resources to other projects, or other factors, and we may be notified of such incidents or activity by the independent privacy assessor required under our modified consent order with the FTC, the media, or other third parties. Such incidents and activities have in the past, and may in the future, include the use of user data or our systems in a manner inconsistent with our terms, contracts or policies,
````

**#2 `META_FY2018_2018-12-31:74`** (cited, gold #2)

````text
Item 1A. Risk Factors > Our new products and changes to existing products could fail to attract or retain users or generate revenue and profits.
In addition to our efforts to mitigate cybersecurity risks, we are making significant investments in safety, security, and content review efforts to combat misuse of our services and user data by third parties, including investigations and audits of platform applications that previously accessed information of a large number of users of our services. As a result of these efforts we have discovered and announced, and anticipate that we will continue to discover and announce, additional incidents of misuse of user data or other undesirable activity by third parties. We may not discover all such incidents or activity, including as a result of our data limitations or the scale of activity on our platform, and we may be notified of such incidents or activity via the media or other third parties. Such incidents and activities may include the use of user data in a manner inconsistent with our terms, contracts or policies, the existence of false or undesirable user accounts, election interference, improper ad purchases, activities that threaten people’s safety on- or offline, or instances of spamming, scraping, or spreading misinformation. The discovery of the foregoing may negatively affect user trust and engagement, harm our reputation and brands, require us to
````

**#4 `META_FY2021_2021-12-31:205`** (gold #2)

````text
Item 1A.Risk Factors > Risks Related to Data, Security, and Intellectual Property
For example, in September 2018, we announced our discovery of a third-party cyber-attack that exploited a vulnerability in Facebook's code to steal user access tokens, which were then used to access certain profile information from approximately 29 million user accounts on Facebook. The events surrounding this cyber-attack became the subject of Irish Data Protection Commission and other government inquiries. Any such inquiries could subject us to substantial fines and costs, require us to change our business practices, divert resources and the attention of management from our business, or adversely affect our business. We anticipate that our ongoing efforts related to privacy, safety, security, and content review will identify additional instances of misuse of user data or other undesirable activity by third parties on our platform.
````

**#5 `META_FY2021_2021-12-31:114`** (gold #1, gold #2)

````text
Item 1A.Risk Factors > Our financial results will fluctuate from quarter to quarter and are difficult to predict.
•costs related to our privacy, safety, security, and content review efforts, including as a result of implementing changes to our practices, whether voluntarily, in connection with laws, regulations, regulatory actions, or decisions or recommendations from the independent Oversight Board, or otherwise; •costs and expenses related to the development, manufacturing, and delivery of our consumer hardware products; •our ability to maintain gross margins and operating margins; •costs related to acquisitions, including costs associated with amortization and additional investments to develop the acquired technologies; •charges associated with impairment of any assets on our balance sheet; •our ability to obtain equipment, components, and labor for our data centers and other technical infrastructure in a timely and cost-effective manner; •system failures or outages or government blocking, which could prevent us from serving ads for any period of time; •breaches of security or privacy, and the costs associated with any such breaches and remediation; •changes in the manner in which we distribute our products or inaccessibility of our products due to third-party actions; •fees paid to third parties for content or the distribution of our products; •refunds or other concessions provided to advertisers; •share-based compensation expense, including acquisition-related expense;
````

**#8 `META_FY2021_2021-12-31:187`** (cited)

````text
Item 1A.Risk Factors > Risks Related to Government Regulation and Enforcement
We are engaged in ongoing privacy compliance and oversight efforts, including in connection with our modified consent order with the FTC, requirements of the GDPR, and other regulatory and legislative requirements around the world, such as the CCPA and the ePrivacy Directive. In particular, we are maintaining a comprehensive privacy program in connection with the FTC consent order that includes substantial management and board of directors oversight, stringent operational requirements and reporting obligations, prohibitions against making misrepresentations relating to user data, a process to regularly certify our compliance with the privacy program to the FTC, and regular assessments of our privacy program by an independent third-party assessor, which has been and will continue to be challenging and costly to maintain and enhance. These compliance and oversight efforts are increasing demand on our systems and resources, and require significant new and ongoing investments, including investments in compliance processes, personnel, and technical infrastructure. We are reallocating resources internally to assist with these efforts, and this has had, and will continue to have, an adverse impact on our other business initiatives. In addition, these efforts require substantial modifications to our business practices and make some practices such as product and ads development more
````

**#9 `META_FY2021_2021-12-31:188`** (cited)

````text
Item 1A.Risk Factors > Risks Related to Government Regulation and Enforcement
difficult, time-consuming, and costly. As a result, we believe our ability to develop and launch new features, products, and services in a timely manner has been and will continue to be adversely affected. We also expect that our privacy compliance and oversight efforts will require significant time and attention from our management and board of directors. The requirements of the FTC consent order and other privacy-related laws and regulations are complex and apply broadly to our business, and from time to time we notify relevant authorities of instances where we are not in full compliance with these requirements or otherwise discover privacy issues, and we expect to continue to do so as any such issues arise in the future. In addition, regulatory and legislative privacy requirements are constantly evolving and can be subject to significant change and uncertain interpretation. If we are unable to successfully implement and comply with the mandates of the FTC consent order, GDPR, CCPA, ePrivacy Directive, or other regulatory or legislative requirements, or if we are found to be in violation of the consent order or other applicable requirements, we may be subject to regulatory or governmental investigations or lawsuits, which may result in significant monetary
````

**#11 `META_FY2021_2021-12-31:204`** (gold #2)

````text
Item 1A.Risk Factors > Risks Related to Data, Security, and Intellectual Property
significant costs in protecting against or remediating such incidents. In addition, we are subject to a variety of laws and regulations in the United States and abroad relating to cybersecurity and data protection, as well as obligations under our modified consent order with the FTC. As a result, affected users or government authorities could initiate legal or regulatory actions against us in connection with any actual or perceived security breaches or improper access to or disclosure of data, which has occurred in the past and which could cause us to incur significant expense and liability or result in orders or consent decrees forcing us to modify our business practices. Such incidents or our efforts to remediate such incidents may also result in a decline in our active user base or engagement levels. Any of these events could have a material and adverse effect on our business, reputation, or financial results.
````

</details>

RQ2 citation match (section level): `cited=[('META', 'Item 1A')] gold=[(None, 'Item 1A')]`

**System C guardrail** (judge `gpt-5.4`): numerical claims 0, verified 0, ungrounded 0, uncited 0, derived 0; sentence verdicts: supported 11, partial 0, unsupported 0, unchecked 0.


<details><summary>Guardrail sentence verdicts</summary>

| sentence | verdict | judge reason |
|---|---|---|
| In its 2018 Form 10-K, Meta disclosed that it was making significant investments in safety, security, and content review efforts to combat misuse of its services and user data by third parties, including investigations and audits of platform applications that previously accessed information of a large number of users of its services. [META FY2018, Item 1A, META_FY2018_2018-12-31:74] | supported | The cited text states Meta was making significant investments in safety, security, and content review, including investigations and audits of platform applications that accessed many users' information. |
| The 2018 disclosure focused on the possibility that these efforts would uncover additional incidents of misuse of user data or other undesirable third-party activity, including false or undesirable user accounts, election interference, improper ad purchases, threats to people’s safety, and spamming, scraping, or spreading misinformation. [META FY2018, Item 1A, META_FY2018_2018-12-31:74] | supported | The evidence expressly says these efforts could uncover additional misuse incidents and lists the same examples of undesirable activity. |
| By 2021, Meta expanded this disclosure by stating that it was making significant investments not only in privacy, safety, security, and content review efforts, but also in enforcement efforts, and that these efforts included investigations and audits of platform applications as well as other enforcement efforts. [META FY2021, Item 1A, META_FY2021_2021-12-31:206] | supported | The 2021 text adds privacy and other enforcement efforts alongside investigations and audits of platform applications. |
| The 2021 filing also broadened the operational limitations it identified, stating that Meta may not discover all such incidents because of data or technical limitations, lack of visibility over encrypted services, the scale of activity on its platform, challenges related to personnel working remotely during the COVID-19 pandemic, the allocation of resources to other projects, or other factors. [META FY2021, Item 1A, META_FY2021_2021-12-31:206] | supported | The cited passage lists all of those reasons Meta may not discover all incidents. |
| Meta further expanded the external oversight dimension in 2021 by disclosing that it may be notified of incidents or activity by the independent privacy assessor required under its modified consent order with the FTC, in addition to the media or other third parties. [META FY2021, Item 1A, META_FY2021_2021-12-31:206] | supported | The evidence explicitly says Meta may be notified by the independent privacy assessor, the media, or other third parties. |
| The 2021 filing also described a much more formalized compliance and oversight structure tied to external regulation, stating that it was engaged in ongoing privacy compliance and oversight efforts in connection with its modified consent order with the FTC, the GDPR, the CCPA, and the ePrivacy Directive. [META FY2021, Item 1A, META_FY2021_2021-12-31:187] | supported | The cited text states Meta was engaged in ongoing privacy compliance and oversight efforts tied to the FTC order, GDPR, CCPA, and ePrivacy Directive. |
| Meta said that, in connection with the FTC consent order, it was maintaining a comprehensive privacy program that included substantial management and board of directors oversight, stringent operational requirements and reporting obligations, prohibitions against making misrepresentations relating to user data, a process to regularly certify compliance to the FTC, and regular assessments of its privacy program by an independent third-party assessor. [META FY2021, Item 1A, META_FY2021_2021-12-31:187] | supported | The evidence lists each element of the comprehensive privacy program described in the sentence. |
| The company also disclosed in 2021 that these compliance and oversight efforts were increasing demand on its systems and resources, requiring significant new and ongoing investments in compliance processes, personnel, and technical infrastructure, and causing internal resource reallocation that had adversely affected and would continue to adversely affect other business initiatives. [META FY2021, Item 1A, META_FY2021_2021-12-31:187] | supported | The cited passage states these efforts increased demand on systems and resources, required significant investments, and caused adverse internal resource reallocation. |
| In addition, Meta stated that these efforts required substantial modifications to its business practices and made some practices such as product and ads development more difficult, time-consuming, and costly, and that its ability to develop and launch new features, products, and services in a timely manner had been and would continue to be adversely affected. [META FY2021, Item 1A, META_FY2021_2021-12-31:187] [META FY2021, Item 1A, META_FY2021_2021-12-31:188] | supported | The two cited excerpts together state that these efforts made product and ads development more difficult, time-consuming, and costly and adversely affected timely launches. |
| The 2021 filing also added that Meta expected its privacy compliance and oversight efforts to require significant time and attention from management and the board of directors, and that failures to comply with the FTC consent order or other privacy requirements could lead to regulatory or governmental investigations or lawsuits and significant monetary penalties. [META FY2021, Item 1A, META_FY2021_2021-12-31:188] | supported | The evidence says these efforts would require significant management and board attention and that noncompliance could lead to investigations, lawsuits, and significant monetary penalties. |
| Meta’s 2021 risk disclosures therefore expanded from a 2018 emphasis on internal investments to detect misuse and harmful activity into a broader framework that explicitly incorporated privacy-focused operational changes, formal compliance infrastructure, board-level governance, independent third-party assessment, and ongoing oversight by regulators under the FTC consent order and other privacy regimes. [META FY2018, Item 1A, META_FY2018_2018-12-31:74] [META FY2021, Item 1A, META_FY2021_2021-12-31:206] [META FY2021, Item 1A, META_FY2021_2021-12-31:187] [META FY2021, Item 1A, META_FY2021_2021-12-31:188] | supported | Taken together, the 2018 and 2021 excerpts support the described expansion from investment-focused misuse detection to broader privacy compliance, governance, assessment, and regulatory oversight. |

</details>
