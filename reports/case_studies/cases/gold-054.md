# gold-054: Multi-hop text (one filing)

[← all cases](../README.md) · company: JPMORGAN CHASE & CO (JPM) · fiscal year: 2015 · recipe `text` · hop `multi` · answer type `qualitative` · scope `single_doc` · RQ2 category `cross_section_multihop`

## Gold QA

**Question**

> According to JPMorgan Chase & Co.'s 2015 10-K, why would the company's currently outstanding senior long-term debt not qualify as eligible long-term debt (LTD) under the proposed TLAC rules, and what is the potential financial consequence for the firm if the final rules do not grandfather these instruments?

**Gold answer**

> JPMorgan Chase's currently outstanding senior long-term debt would not qualify as eligible LTD under the proposed TLAC rules because it includes structured notes and other debt that permits acceleration for reasons other than insolvency or payment default, which are prohibited features. If the final rules do not allow these outstanding instruments to count as eligible LTD, the firm could be required to issue a substantial amount of new senior long-term debt, which would significantly increase its funding costs.

**Key points** (RQ3 keypoint_recall targets)

1. Current debt includes structured notes and permits acceleration for reasons other than insolvency or payment default.
2. These features disqualify the debt from being eligible LTD under proposed TLAC rules.
3. Compliance may require issuing substantial new senior long-term debt.
4. Issuing new debt would significantly increase funding costs.

**Gold evidence**

1. `JPM_FY2015_2015-12-31` · Item 1A: RISK FACTORS › Part I · text

   > The currently outstanding senior long-term debt of U.S. GSIB BHCs, including JPMorgan Chase & Co., includes structured notes as well as other debt that typically permits acceleration for reasons other than insolvency or payment default and, as a result, none of such outstanding senior long-term debt or any subsequently issued senior long-term debt with similar terms would qualify as eligible LTD under the proposed TLAC rules.

2. `JPM_FY2015_2015-12-31` · Item 1A: RISK FACTORS › Part I · text

   > To the extent that outstanding senior long-term debt of JPMorgan Chase & Co. is not classified as eligible LTD under the TLAC rule as finally adopted by the Federal Reserve, the Firm could be required to issue a substantial amount of new senior long-term debt which could significantly increase the Firm’s funding costs.

## Scorecard

| Metric | A (vanilla dense) | B (hybrid + rerank) | C v1 (adaptive multi-hop) | C v2 (agentic multi-hop + XBRL) |
|---|---|---|---|---|
| **Retrieval (RQ1)** | | | | |
| chunks retrieved | 3 | 5 | 14 | 10 |
| recall@5 | 1.00 | 1.00 | 1.00 | 1.00 |
| recall@all | 1.00 | 1.00 | 1.00 | 1.00 |
| complete@all | 1 | 1 | 1 | 1 |
| average precision (lexical) | 1.00 | 1.00 | 1.00 | 0.58 |
| gold evidence first rank | #1: 1, #2: 2 | #1: 1, #2: 2 | #1: 1, #2: 2 | #1: 2, #2: 3 |
| **Answer (RQ3 string match)** | | | | |
| numeric_correct | – | – | – | – |
| keypoint_recall | 1.00 | 1.00 | 1.00 | 1.00 |
| **Answer & citations (RQ2)** | | | | |
| numeric_accuracy | – | – | – | – |
| citation precision | 1.00 | 1.00 | 0.50 | 0.50 |
| citation recall | 1.00 | 1.00 | 1.00 | 1.00 |
| citation F1 | 1.00 | 1.00 | 0.67 | 0.67 |
| has a citation | 1 | 1 | 1 | 1 |
| grounding error rate | – | – | 0.00 | 0.00 |
| **Cost (RQ3)** | | | | |
| retrieval hops | 1 | 1 | 3 | 2 |
| tokens | 1136 | 1468 | 15652 | 12003 |
| cost (USD) | 0.0002 | 0.0003 | 0.0544 | 0.0435 |
| latency (s) | 3.0 | 7.2 | 25.0 | 20.6 |

Definitions: [README › Metrics](../README.md#metrics). `–` = not applicable (e.g. no gold number, no citations, no guardrail).

## System outputs

### System A (vanilla dense)

Model: `gpt-5.4-2026-03-05`. Hops: 1. Chunks retrieved: 3, cited: 2.

**Generated answer**

> JPMorgan Chase & Co.’s currently outstanding senior long-term debt would not qualify as eligible LTD under the proposed TLAC rules because it includes:
>
> - structured notes, and
> - other debt that permits acceleration for reasons other than insolvency or payment default,
>
> both of which the proposed rules would disqualify from eligible LTD [1].
>
> If the final TLAC rules do not grandfather these instruments and they are not classified as eligible LTD, the firm could be required to issue a substantial amount of new senior long-term debt, which could significantly increase its funding costs [2].

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `JPM_FY2015_2015-12-31:83` | Item 1A › Part I | ✓ | #1 | On October 30, 2015, the Federal Reserve issued proposed rules (the “proposed TLAC rules”) that would require the top-tier holding companies of eight U.S. global systemically important bank holding companies (“U.S. GSIB … |
| 2 | `JPM_FY2015_2015-12-31:84` | Item 1A › Part I | ✓ | #2 | Co., may need to take to come into compliance with the final TLAC rules, including the amount and form of long-term debt that must be refinanced or issued, will depend in substantial part on the ultimate eligibility requ… |
| 3 | `JPM_FY2015_2015-12-31:689` | Item 15 › Other capital requirements |  |  | On October 30, 2015, the Federal Reserve issued proposed rules that would require the top-tier holding companies of eight U.S. global systemically important bank holding companies, including the Firm, among other things,… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#1 `JPM_FY2015_2015-12-31:83`** (cited, gold #1)

````text
Item 1A: RISK FACTORS > Part I
On October 30, 2015, the Federal Reserve issued proposed rules (the “proposed TLAC rules”) that would require the top-tier holding companies of eight U.S. global systemically important bank holding companies (“U.S. GSIB BHCs”), including JPMorgan Chase & Co., among other things, to maintain minimum amounts of eligible LTD, commencing January 1, 2019. The proposed TLAC rules would disqualify from eligible LTD, among other instruments, senior debt securities that permit acceleration for reasons other than insolvency or payment default, as well as debt securities that are not governed by U.S. law and structured notes. The currently outstanding senior long-term debt of U.S. GSIB BHCs, including JPMorgan Chase & Co., includes structured notes as well as other debt that typically permits acceleration for reasons other than insolvency or payment default and, as a result, none of such outstanding senior long-term debt or any subsequently issued senior long-term debt with similar terms would qualify as eligible LTD under the proposed TLAC rules. The Federal Reserve has requested comment on whether certain currently outstanding instruments should be allowed to count as eligible LTD “despite containing features that would be prohibited under the proposal.” The steps that the U.S. GSIB BHCs, including JPMorgan Chase &
````

**#2 `JPM_FY2015_2015-12-31:84`** (cited, gold #2)

````text
Item 1A: RISK FACTORS > Part I
Co., may need to take to come into compliance with the final TLAC rules, including the amount and form of long-term debt that must be refinanced or issued, will depend in substantial part on the ultimate eligibility requirements for senior long-term debt and any grandfathering provisions. To the extent that outstanding senior long-term debt of JPMorgan Chase & Co. is not classified as eligible LTD under the TLAC rule as finally adopted by the Federal Reserve, the Firm could be required to issue a substantial amount of new senior long-term debt which could significantly increase the Firm’s funding costs. Authorities in some non-U.S. jurisdictions in which the Firm has operations have enacted legislation or regulations requiring that certain subsidiaries of the Firm operating in those countries maintain independent capital and liquidity. In addition, some non-U.S. regulators have proposed that large banks which conduct certain businesses in their jurisdictions operate through separate subsidiaries located in those countries. These requirements, and any future laws or regulations that seek to increase capital or liquidity requirements that would be applicable to non-U.S. subsidiaries of the Firm, could hinder the Firm’s ability to efficiently manage its funding and liquidity in a centralized manner.
````

</details>

RQ2 citation match (section level): `cited=[('JPM', 'Item 1A')] gold=[(None, 'Item 1A')]`

### System B (hybrid + rerank)

Model: `gpt-5.4-2026-03-05`. Hops: 1. Chunks retrieved: 5, cited: 2.

**Generated answer**

> JPMorgan Chase’s currently outstanding senior long-term debt would not qualify as eligible LTD under the proposed TLAC rules because it includes structured notes and other debt that permits acceleration for reasons other than insolvency or payment default, and the proposed rules would disqualify those types of instruments from eligible LTD [1].
>
> If the final rules do not grandfather these instruments, the firm could be required to issue a substantial amount of new senior long-term debt, which could significantly increase its funding costs [2].

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `JPM_FY2015_2015-12-31:83` | Item 1A › Part I | ✓ | #1 | On October 30, 2015, the Federal Reserve issued proposed rules (the “proposed TLAC rules”) that would require the top-tier holding companies of eight U.S. global systemically important bank holding companies (“U.S. GSIB … |
| 2 | `JPM_FY2015_2015-12-31:84` | Item 1A › Part I | ✓ | #2 | Co., may need to take to come into compliance with the final TLAC rules, including the amount and form of long-term debt that must be refinanced or issued, will depend in substantial part on the ultimate eligibility requ… |
| 3 | `JPM_FY2015_2015-12-31:81` | Item 1A › If JPMorgan Chase does not effectively manage its liquidity, its business could suffer. |  |  | If the Firm’s access to stable and low cost sources of funding, such as bank deposits, is reduced, the Firm may need to raise alternative funding which may be more expensive or of limited availability. In addition, the F… |
| 4 | `JPM_FY2015_2015-12-31:689` | Item 15 › Other capital requirements |  |  | On October 30, 2015, the Federal Reserve issued proposed rules that would require the top-tier holding companies of eight U.S. global systemically important bank holding companies, including the Firm, among other things,… |
| 5 | `JPM_FY2015_2015-12-31:1427` | Item 15 › Note 21 – Long-term debt |  |  | JPMorgan Chase issues long-term debt denominated in various currencies, although predominantly U.S. dollars, with both fixed and variable interest rates. Included in senior and subordinated debt below are various equity-… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#1 `JPM_FY2015_2015-12-31:83`** (cited, gold #1)

````text
Item 1A: RISK FACTORS > Part I
On October 30, 2015, the Federal Reserve issued proposed rules (the “proposed TLAC rules”) that would require the top-tier holding companies of eight U.S. global systemically important bank holding companies (“U.S. GSIB BHCs”), including JPMorgan Chase & Co., among other things, to maintain minimum amounts of eligible LTD, commencing January 1, 2019. The proposed TLAC rules would disqualify from eligible LTD, among other instruments, senior debt securities that permit acceleration for reasons other than insolvency or payment default, as well as debt securities that are not governed by U.S. law and structured notes. The currently outstanding senior long-term debt of U.S. GSIB BHCs, including JPMorgan Chase & Co., includes structured notes as well as other debt that typically permits acceleration for reasons other than insolvency or payment default and, as a result, none of such outstanding senior long-term debt or any subsequently issued senior long-term debt with similar terms would qualify as eligible LTD under the proposed TLAC rules. The Federal Reserve has requested comment on whether certain currently outstanding instruments should be allowed to count as eligible LTD “despite containing features that would be prohibited under the proposal.” The steps that the U.S. GSIB BHCs, including JPMorgan Chase &
````

**#2 `JPM_FY2015_2015-12-31:84`** (cited, gold #2)

````text
Item 1A: RISK FACTORS > Part I
Co., may need to take to come into compliance with the final TLAC rules, including the amount and form of long-term debt that must be refinanced or issued, will depend in substantial part on the ultimate eligibility requirements for senior long-term debt and any grandfathering provisions. To the extent that outstanding senior long-term debt of JPMorgan Chase & Co. is not classified as eligible LTD under the TLAC rule as finally adopted by the Federal Reserve, the Firm could be required to issue a substantial amount of new senior long-term debt which could significantly increase the Firm’s funding costs. Authorities in some non-U.S. jurisdictions in which the Firm has operations have enacted legislation or regulations requiring that certain subsidiaries of the Firm operating in those countries maintain independent capital and liquidity. In addition, some non-U.S. regulators have proposed that large banks which conduct certain businesses in their jurisdictions operate through separate subsidiaries located in those countries. These requirements, and any future laws or regulations that seek to increase capital or liquidity requirements that would be applicable to non-U.S. subsidiaries of the Firm, could hinder the Firm’s ability to efficiently manage its funding and liquidity in a centralized manner.
````

</details>

RQ2 citation match (section level): `cited=[('JPM', 'Item 1A')] gold=[(None, 'Item 1A')]`

### System C v1 (adaptive multi-hop)

Model: `gpt-5.4`. Hops: 3. Chunks retrieved: 14, cited: 3.

**Generated answer**

> JPMorgan Chase & Co.’s currently outstanding senior long-term debt would not qualify as eligible LTD under the proposed TLAC rules because the proposed rules would disqualify senior debt securities that permit acceleration for reasons other than insolvency or payment default, as well as structured notes and debt securities not governed by U.S. law, and the company stated that its outstanding senior long-term debt includes structured notes and other debt with acceleration terms of that kind. [JPM FY2015, Item 1A, JPM_FY2015_2015-12-31:83] [JPM FY2015, Item 15, JPM_FY2015_2015-12-31:690]
>
> If those outstanding instruments are not classified as eligible LTD under the final TLAC rule, the firm could be required to issue a substantial amount of new senior long-term debt, which could significantly increase the firm’s funding costs. [JPM FY2015, Item 1A, JPM_FY2015_2015-12-31:84]

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `JPM_FY2015_2015-12-31:83` | Item 1A › Part I | ✓ | #1 | On October 30, 2015, the Federal Reserve issued proposed rules (the “proposed TLAC rules”) that would require the top-tier holding companies of eight U.S. global systemically important bank holding companies (“U.S. GSIB … |
| 2 | `JPM_FY2015_2015-12-31:84` | Item 1A › Part I | ✓ | #2 | Co., may need to take to come into compliance with the final TLAC rules, including the amount and form of long-term debt that must be refinanced or issued, will depend in substantial part on the ultimate eligibility requ… |
| 3 | `JPM_FY2015_2015-12-31:689` | Item 15 › Other capital requirements |  |  | On October 30, 2015, the Federal Reserve issued proposed rules that would require the top-tier holding companies of eight U.S. global systemically important bank holding companies, including the Firm, among other things,… |
| 4 | `JPM_FY2015_2015-12-31:688` | Item 15 › Other capital requirements |  |  | Minimum Total Loss Absorbing Capacity In November 2015, the Financial Stability Board (“FSB”) finalized the TLAC standard for GSIBs, which establishes the criteria for TLAC eligible debt and capital instruments and defin… |
| 5 | `JPM_FY2015_2015-12-31:1427` | Item 15 › Note 21 – Long-term debt |  |  | JPMorgan Chase issues long-term debt denominated in various currencies, although predominantly U.S. dollars, with both fixed and variable interest rates. Included in senior and subordinated debt below are various equity-… |
| 6 | `JPM_FY2015_2015-12-31:1428` | Item 15 › Note 21 – Long-term debt |  |  | \| By remaining maturity at December 31, \| \| 2015 \| \| \| \| 2014 \| \| \|---\|---\|---\|---\|---\|---\|---\|---\| \| (in millions, except rates) \| \| Under 1 year \| 1-5 years \| After 5 years \| Total \| Total \| \| \| Parent company \| \| \| \| … |
| 7 | `JPM_FY2015_2015-12-31:1429` | Item 15 › Note 21 – Long-term debt |  |  | \| By remaining maturity at December 31, \| \| 2015 \| \| \| \| 2014 \| \| \|---\|---\|---\|---\|---\|---\|---\|---\| \| \| Variable rate \| 9,700 \| 56,690 \| 5,000 \| 71,390 \| 62,790 \| \| \| \| Interest rates(a) \| 0.37-0.65% \| 0.17-0.72% \| 0.50-… |
| 8 | `JPM_FY2015_2015-12-31:690` | Item 15 › Other capital requirements | ✓ |  | acceleration for reasons other than insolvency or payment default, as well as structured notes and debt securities not governed by U.S. law. The Firm is currently evaluating the impact of the proposal. 156 JPMorgan Chase… |
| 9 | `JPM_FY2015_2015-12-31:938` | Item 15 › Notes to consolidated financial statements |  |  | \| \| December 31, 2015 \| \| \| \| \| December 31, 2014 \| \| \| \| \| \|---\|---\|---\|---\|---\|---\|---\|---\|---\|---\|---\| \| \| \| Estimated fair value hierarchy \| \| \| \| \| Estimated fair value hierarchy \| \| \| \| \| Long-term debt and junior … |
| 10 | `JPM_FY2015_2015-12-31:854` | Item 15 › Notes to consolidated financial statements |  |  | \| Assets and liabilities measured at fair value on a recurring basis \| \| \| \| \| \| \| \| \|---\|---\|---\|---\|---\|---\|---\|---\| \| \| Fair value hierarchy \| \| \| \| \| \| \| \| Non-U.S. government debt securities \| 23,199 \| 13,477 \| — \| … |
| 11 | `JPM_FY2015_2015-12-31:862` | Item 15 › Notes to consolidated financial statements |  |  | \| \| Fair value hierarchy \| \| \| \| \| \| \| \|---\|---\|---\|---\|---\|---\|---\|---\| \| U.S. government agencies(a) \| — \| 65,319 \| \| — \| — \| \| 65,319 \| \| Residential – nonagency \| — \| 50,865 \| \| 30 \| — \| \| 50,895 \| \| Commercial – non… |
| 12 | `JPM_FY2015_2015-12-31:1254` | Item 15 › Financial effects of modifications and redefaults |  |  | \| Year ended December 31, (in millions, except weighted-average data and number of loans) \| Home equity \| \| \| \| \| \| Mortgages \| \| \| \| \| \| Total residential real estate – excluding PCI \| \| \| \|---\|---\|---\|---\|---\|---\|---\|-… |
| 13 | `JPM_FY2015_2015-12-31:903` | Item 15 › Notes to consolidated financial statements |  |  | \| \| Fair value measurements using significant unobservable inputs \| \| \| \| \| \| \| \| \| \| \| \|---\|---\|---\|---\|---\|---\|---\|---\|---\|---\|---\|---\| \| Commercial – nonagency \| 432 \| 17 \| \| 980 \| (914) \| \| (60) \| (149) \| 306 \| (12) … |
| 14 | `JPM_FY2015_2015-12-31:860` | Item 15 › Notes to consolidated financial statements |  |  | \| \| Fair value hierarchy \| \| \| \| \| \| \| \|---\|---\|---\|---\|---\|---\|---\|---\| \| Obligations of U.S. states and municipalities \| — \| 9,298 \| \| 1,273 \| — \| \| 10,571 \| \| Certificates of deposit, bankers’ acceptances and commerci… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#1 `JPM_FY2015_2015-12-31:83`** (cited, gold #1)

````text
Item 1A: RISK FACTORS > Part I
On October 30, 2015, the Federal Reserve issued proposed rules (the “proposed TLAC rules”) that would require the top-tier holding companies of eight U.S. global systemically important bank holding companies (“U.S. GSIB BHCs”), including JPMorgan Chase & Co., among other things, to maintain minimum amounts of eligible LTD, commencing January 1, 2019. The proposed TLAC rules would disqualify from eligible LTD, among other instruments, senior debt securities that permit acceleration for reasons other than insolvency or payment default, as well as debt securities that are not governed by U.S. law and structured notes. The currently outstanding senior long-term debt of U.S. GSIB BHCs, including JPMorgan Chase & Co., includes structured notes as well as other debt that typically permits acceleration for reasons other than insolvency or payment default and, as a result, none of such outstanding senior long-term debt or any subsequently issued senior long-term debt with similar terms would qualify as eligible LTD under the proposed TLAC rules. The Federal Reserve has requested comment on whether certain currently outstanding instruments should be allowed to count as eligible LTD “despite containing features that would be prohibited under the proposal.” The steps that the U.S. GSIB BHCs, including JPMorgan Chase &
````

**#2 `JPM_FY2015_2015-12-31:84`** (cited, gold #2)

````text
Item 1A: RISK FACTORS > Part I
Co., may need to take to come into compliance with the final TLAC rules, including the amount and form of long-term debt that must be refinanced or issued, will depend in substantial part on the ultimate eligibility requirements for senior long-term debt and any grandfathering provisions. To the extent that outstanding senior long-term debt of JPMorgan Chase & Co. is not classified as eligible LTD under the TLAC rule as finally adopted by the Federal Reserve, the Firm could be required to issue a substantial amount of new senior long-term debt which could significantly increase the Firm’s funding costs. Authorities in some non-U.S. jurisdictions in which the Firm has operations have enacted legislation or regulations requiring that certain subsidiaries of the Firm operating in those countries maintain independent capital and liquidity. In addition, some non-U.S. regulators have proposed that large banks which conduct certain businesses in their jurisdictions operate through separate subsidiaries located in those countries. These requirements, and any future laws or regulations that seek to increase capital or liquidity requirements that would be applicable to non-U.S. subsidiaries of the Firm, could hinder the Firm’s ability to efficiently manage its funding and liquidity in a centralized manner.
````

**#8 `JPM_FY2015_2015-12-31:690`** (cited)

````text
ITEM 15: EXHIBITS, FINANCIAL STATEMENT SCHEDULES > Other capital requirements
acceleration for reasons other than insolvency or payment default, as well as structured notes and debt securities not governed by U.S. law. The Firm is currently evaluating the impact of the proposal. 156 JPMorgan Chase & Co./2015 Annual Report
````

</details>

RQ2 citation match (section level): `cited=[('JPM', 'Item 1A'), ('JPM', 'Item 15')] gold=[(None, 'Item 1A')]`

**System C guardrail** (judge `gpt-5.4`): numerical claims 0, verified 0, ungrounded 0, uncited 0, derived 0; sentence verdicts: supported 2, partial 0, unsupported 0, unchecked 0.


<details><summary>Guardrail sentence verdicts</summary>

| sentence | verdict | judge reason |
|---|---|---|
| JPMorgan Chase & Co.’s currently outstanding senior long-term debt would not qualify as eligible LTD under the proposed TLAC rules because the proposed rules would disqualify senior debt securities that permit acceleration for reasons other than insolvency or payment default, as well as structured notes and debt securities not governed by U.S. law, and the company stated that its outstanding senior long-term debt includes structured notes and other debt with acceleration terms of that kind. [JPM FY2015, Item 1A, JPM_FY2015_2015-12-31:83] [JPM FY2015, Item 15, JPM_FY2015_2015-12-31:690] | supported | The cited text states the proposed TLAC rules would disqualify those debt features and that none of JPMorgan's currently outstanding senior long-term debt would qualify because it includes such instruments. |
| If those outstanding instruments are not classified as eligible LTD under the final TLAC rule, the firm could be required to issue a substantial amount of new senior long-term debt, which could significantly increase the firm’s funding costs. [JPM FY2015, Item 1A, JPM_FY2015_2015-12-31:84] | supported | The cited evidence explicitly says the firm could need to issue substantial new senior long-term debt and that this could significantly increase funding costs. |

</details>

### System C v2 (agentic multi-hop + XBRL)

Model: `gpt-5.4`. Hops: 2. Chunks retrieved: 10, cited: 3.

**Generated answer**

> JPMorgan Chase & Co.’s currently outstanding senior long-term debt would not qualify as eligible long-term debt under the proposed TLAC rules because the proposed rules would disqualify senior debt securities that permit acceleration for reasons other than insolvency or payment default, as well as debt securities that are not governed by U.S. law and structured notes, and the company stated that its currently outstanding senior long-term debt includes structured notes as well as other debt that typically permits acceleration for reasons other than insolvency or payment default. [JPM FY2015, Item 1A, JPM_FY2015_2015-12-31:83] [JPM FY2015, Item 15, JPM_FY2015_2015-12-31:689]
>
> If the final TLAC rules do not grandfather these instruments and outstanding senior long-term debt is not classified as eligible LTD, the firm could be required to issue a substantial amount of new senior long-term debt, which could significantly increase the firm’s funding costs. [JPM FY2015, Item 1A, JPM_FY2015_2015-12-31:84]

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `F-JPM-2015` | SEC XBRL Reported Financials (financials.csv) |  |  | fiscal_year,fiscal_year_end,Revenue,NetIncome,OperatingIncome,TotalAssets,TotalLiabilities,StockholdersEquity,CashAndEquivalents,OperatingCashFlow,EPSDiluted 2015,2015-12-31,93543000000,24442000000,,2351698000000,2104125… |
| 2 | `JPM_FY2015_2015-12-31:83` | Item 1A › Part I | ✓ | #1 | On October 30, 2015, the Federal Reserve issued proposed rules (the “proposed TLAC rules”) that would require the top-tier holding companies of eight U.S. global systemically important bank holding companies (“U.S. GSIB … |
| 3 | `JPM_FY2015_2015-12-31:84` | Item 1A › Part I | ✓ | #2 | Co., may need to take to come into compliance with the final TLAC rules, including the amount and form of long-term debt that must be refinanced or issued, will depend in substantial part on the ultimate eligibility requ… |
| 4 | `JPM_FY2015_2015-12-31:689` | Item 15 › Other capital requirements | ✓ |  | On October 30, 2015, the Federal Reserve issued proposed rules that would require the top-tier holding companies of eight U.S. global systemically important bank holding companies, including the Firm, among other things,… |
| 5 | `JPM_FY2015_2015-12-31:688` | Item 15 › Other capital requirements |  |  | Minimum Total Loss Absorbing Capacity In November 2015, the Financial Stability Board (“FSB”) finalized the TLAC standard for GSIBs, which establishes the criteria for TLAC eligible debt and capital instruments and defin… |
| 6 | `JPM_FY2015_2015-12-31:1427` | Item 15 › Note 21 – Long-term debt |  |  | JPMorgan Chase issues long-term debt denominated in various currencies, although predominantly U.S. dollars, with both fixed and variable interest rates. Included in senior and subordinated debt below are various equity-… |
| 7 | `JPM_FY2015_2015-12-31:1428` | Item 15 › Note 21 – Long-term debt |  |  | \| By remaining maturity at December 31, \| \| 2015 \| \| \| \| 2014 \| \| \|---\|---\|---\|---\|---\|---\|---\|---\| \| (in millions, except rates) \| \| Under 1 year \| 1-5 years \| After 5 years \| Total \| Total \| \| \| Parent company \| \| \| \| … |
| 8 | `JPM_FY2015_2015-12-31:1429` | Item 15 › Note 21 – Long-term debt |  |  | \| By remaining maturity at December 31, \| \| 2015 \| \| \| \| 2014 \| \| \|---\|---\|---\|---\|---\|---\|---\|---\| \| \| Variable rate \| 9,700 \| 56,690 \| 5,000 \| 71,390 \| 62,790 \| \| \| \| Interest rates(a) \| 0.37-0.65% \| 0.17-0.72% \| 0.50-… |
| 9 | `JPM_FY2015_2015-12-31:958` | Item 15 › Structured note products by balance sheet classification and risk component |  |  | \| \| December 31, 2015 \| \| \| \| December 31, 2014 \| \| \| \| \|---\|---\|---\|---\|---\|---\|---\|---\|---\| \| (in millions) \| Long-term debt \| Other borrowed funds \| Deposits \| Total \| Long-term debt \| Other borrowed funds \| Deposits … |
| 10 | `JPM_FY2015_2015-12-31:1430` | Item 15 › Note 21 – Long-term debt |  |  | \| By remaining maturity at December 31, \| \| 2015 \| \| \| \| 2014 \| \| \|---\|---\|---\|---\|---\|---\|---\|---\| \| \| Interest rates(a) \| —% \| —% \| 0.83-8.75% \| 0.83-8.75% \| 0.73-8.75% \| \| \| \| Subtotal \| $— \| $— \| $3,969 \| $3,969 \| \| … |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#2 `JPM_FY2015_2015-12-31:83`** (cited, gold #1)

````text
Item 1A: RISK FACTORS > Part I
On October 30, 2015, the Federal Reserve issued proposed rules (the “proposed TLAC rules”) that would require the top-tier holding companies of eight U.S. global systemically important bank holding companies (“U.S. GSIB BHCs”), including JPMorgan Chase & Co., among other things, to maintain minimum amounts of eligible LTD, commencing January 1, 2019. The proposed TLAC rules would disqualify from eligible LTD, among other instruments, senior debt securities that permit acceleration for reasons other than insolvency or payment default, as well as debt securities that are not governed by U.S. law and structured notes. The currently outstanding senior long-term debt of U.S. GSIB BHCs, including JPMorgan Chase & Co., includes structured notes as well as other debt that typically permits acceleration for reasons other than insolvency or payment default and, as a result, none of such outstanding senior long-term debt or any subsequently issued senior long-term debt with similar terms would qualify as eligible LTD under the proposed TLAC rules. The Federal Reserve has requested comment on whether certain currently outstanding instruments should be allowed to count as eligible LTD “despite containing features that would be prohibited under the proposal.” The steps that the U.S. GSIB BHCs, including JPMorgan Chase &
````

**#3 `JPM_FY2015_2015-12-31:84`** (cited, gold #2)

````text
Item 1A: RISK FACTORS > Part I
Co., may need to take to come into compliance with the final TLAC rules, including the amount and form of long-term debt that must be refinanced or issued, will depend in substantial part on the ultimate eligibility requirements for senior long-term debt and any grandfathering provisions. To the extent that outstanding senior long-term debt of JPMorgan Chase & Co. is not classified as eligible LTD under the TLAC rule as finally adopted by the Federal Reserve, the Firm could be required to issue a substantial amount of new senior long-term debt which could significantly increase the Firm’s funding costs. Authorities in some non-U.S. jurisdictions in which the Firm has operations have enacted legislation or regulations requiring that certain subsidiaries of the Firm operating in those countries maintain independent capital and liquidity. In addition, some non-U.S. regulators have proposed that large banks which conduct certain businesses in their jurisdictions operate through separate subsidiaries located in those countries. These requirements, and any future laws or regulations that seek to increase capital or liquidity requirements that would be applicable to non-U.S. subsidiaries of the Firm, could hinder the Firm’s ability to efficiently manage its funding and liquidity in a centralized manner.
````

**#4 `JPM_FY2015_2015-12-31:689`** (cited)

````text
ITEM 15: EXHIBITS, FINANCIAL STATEMENT SCHEDULES > Other capital requirements
On October 30, 2015, the Federal Reserve issued proposed rules that would require the top-tier holding companies of eight U.S. global systemically important bank holding companies, including the Firm, among other things, to maintain minimum levels of eligible TLAC and long-term debt satisfying certain eligibility criteria (“eligible LTD”) commencing January 1, 2019. Under the proposal, these eight U.S GSIBs would be required to maintain minimum TLAC of no less than 18% of the financial institution’s RWA or 9.5% of its leverage exposure (as defined by the rules), plus in the case of the RWA-based measure, a TLAC buffer that is equal to 2.5% of the financial institution’s CET1, any applicable countercyclical buffer and the financial institution’s GSIB surcharge as calculated under method 1. The minimum level of eligible LTD that would be required to be maintained by these eight U.S. GSIBs would be equal to the greater of (A) 6% of the financial institution’s RWA, plus the higher of the method 1 or method 2 GSIB surcharge applicable to the institution and (B) 4.5% of its leverage exposure (as defined by the rules). These proposed TLAC Rules would disqualify from eligible LTD, among other instruments, senior debt securities that permit
````

</details>

RQ2 citation match (section level): `cited=[('JPM', 'Item 1A'), ('JPM', 'Item 15')] gold=[(None, 'Item 1A')]`

**System C guardrail** (judge `gpt-5.4`): numerical claims 0, verified 0, ungrounded 0, uncited 0, derived 0; sentence verdicts: supported 2, partial 0, unsupported 0, unchecked 0.


<details><summary>Guardrail sentence verdicts</summary>

| sentence | verdict | judge reason |
|---|---|---|
| JPMorgan Chase & Co.’s currently outstanding senior long-term debt would not qualify as eligible long-term debt under the proposed TLAC rules because the proposed rules would disqualify senior debt securities that permit acceleration for reasons other than insolvency or payment default, as well as debt securities that are not governed by U.S. law and structured notes, and the company stated that its currently outstanding senior long-term debt includes structured notes as well as other debt that typically permits acceleration for reasons other than insolvency or payment default. [JPM FY2015, Item 1A, JPM_FY2015_2015-12-31:83] [JPM FY2015, Item 15, JPM_FY2015_2015-12-31:689] | supported | The cited text states the proposed TLAC rules would disqualify those debt types and that JPMorgan’s outstanding senior long-term debt includes them, so none would qualify. |
| If the final TLAC rules do not grandfather these instruments and outstanding senior long-term debt is not classified as eligible LTD, the firm could be required to issue a substantial amount of new senior long-term debt, which could significantly increase the firm’s funding costs. [JPM FY2015, Item 1A, JPM_FY2015_2015-12-31:84] | supported | The cited text says if outstanding senior long-term debt is not classified as eligible LTD, the firm could need to issue substantial new senior long-term debt and funding costs could significantly increase. |

</details>
