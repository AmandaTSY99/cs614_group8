# gold-087: Cross-year text

[← all cases](../README.md) · company: NVIDIA CORP (NVDA) · fiscal year: 2020 · recipe `cross_year_text` · hop `multi` · answer type `qualitative` · scope `cross_year` · RQ2 category `multi_company_comparison`

## Gold QA

**Question**

> How did the range of expiration dates for NVIDIA's currently issued patents change between its fiscal year 2016 and fiscal year 2020 10-K filings?

**Gold answer**

> In the fiscal year 2016 10-K, NVIDIA's currently issued patents had expiration dates from April 2016 to December 2034. In the fiscal year 2020 10-K, the range was March 2020 to October 2039, so both the earliest and the latest expiration dates moved later.

**Key points** (RQ3 keypoint_recall targets)

1. In the fiscal year 2016 10-K, the expiration dates ranged from April 2016 to December 2034.
2. In the fiscal year 2020 10-K, the expiration dates ranged from March 2020 to October 2039.
3. Both the earliest and the latest expiration dates moved later.

**Gold evidence**

1. `NVDA_FY2020_2020-01-26` · ITEM 1. BUSINESS › Patents and Proprietary Rights · text

   > Our currently issued patents have expiration dates from March 2020 to October 2039.

2. `NVDA_FY2016_2016-01-31` · ITEM 1. BUSINESS › Patents and Proprietary Rights · text

   > Our currently issued patents have expiration dates from April 2016 to December 2034.

## Scorecard

| Metric | A (vanilla dense) | B (hybrid + rerank) | C v1 (adaptive multi-hop) | C v2 (agentic multi-hop + XBRL) |
|---|---|---|---|---|
| **Retrieval (RQ1)** | | | | |
| chunks retrieved | 10 | 5 | 6 | 6 |
| recall@5 | 0.00 | 1.00 | 1.00 | 1.00 |
| recall@all | 0.00 | 1.00 | 1.00 | 1.00 |
| complete@all | 0 | 1 | 1 | 1 |
| average precision (lexical) | 0.00 | 1.00 | 1.00 | 1.00 |
| gold evidence first rank | #1: –, #2: – | #1: 1, #2: 1 | #1: 1, #2: 1 | #1: 1, #2: 1 |
| **Answer (RQ3 string match)** | | | | |
| numeric_correct | ✗ | ✓ | ✓ | ✓ |
| keypoint_recall | 0.00 | 1.00 | 1.00 | 1.00 |
| **Answer & citations (RQ2)** | | | | |
| numeric_accuracy | – | – | – | – |
| citation precision | – | 1.00 | 1.00 | 1.00 |
| citation recall | – | 1.00 | 1.00 | 1.00 |
| citation F1 | – | 1.00 | 1.00 | 1.00 |
| has a citation | 0 | 1 | 1 | 1 |
| grounding error rate | – | – | 0.00 | 0.00 |
| **Cost (RQ3)** | | | | |
| retrieval hops | 1 | 1 | 1 | 1 |
| tokens | 2154 | 1434 | 5885 | 5889 |
| cost (USD) | 0.0003 | 0.0003 | 0.0217 | 0.0220 |
| latency (s) | 1.8 | 6.9 | 8.4 | 10.6 |

Definitions: [README › Metrics](../README.md#metrics). `–` = not applicable (e.g. no gold number, no citations, no guardrail).

## System outputs

### System A (vanilla dense)

Model: `gpt-5.4-2026-03-05`. Hops: 1. Chunks retrieved: 10, cited: 0.

**Generated answer**

> Not found in the provided context.

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `NVDA_FY2020_2020-01-26:187` | Item 9 |  |  | None. |
| 2 | `NVDA_FY2020_2020-01-26:388` | Item 15 › EXHIBIT INDEX |  |  | \| \| \| Incorporated by Reference \| \| \| \| \|---\|---\|---\|---\|---\|---\| \| 4.3 \| Indenture, dated as of September 16, 2016, by and between the Company and Wells Fargo Bank, National Association, as Trustee \| 8-K \| 0-23985 \| 4.1… |
| 3 | `NVDA_FY2020_2020-01-26:9` | DOCUMENTS INCORPORATED BY REFERENCE |  |  | Portions of the registrant's Proxy Statement for its 2020 Annual Meeting of Shareholders to be filed with the Securities and Exchange Commission pursuant to Regulation 14A not later than 120 days after the end of the fis… |
| 4 | `NVDA_FY2020_2020-01-26:207` | Item 15 |  |  | \| \| \| \| Page \| \|---\|---\|---\|---\| \| \| \| The exhibits listed in the accompanying index to exhibits are filed or incorporated by reference as a part of this Annual Report on Form 10-K. \| 71 \| |
| 5 | `NVDA_FY2016_2016-01-31:423` | Item 15 › EXHIBIT INDEX |  |  | \| \| \| Incorporated by Reference \| \| \| \| \|---\|---\|---\|---\|---\|---\| \| Exhibit No. \| Exhibit Description \| Schedule/Form \| File Number \| Exhibit \| Filing Date \| \| 3.1 \| Amended and Restated Certificate of Incorporation \| S-… |
| 6 | `NVDA_FY2016_2016-01-31:441` | Item 15 › EXHIBIT INDEX |  |  | \| \| \| Incorporated by Reference \| \| \| \| \|---\|---\|---\|---\|---\|---\| \| Exhibit No. \| Exhibit Description \| Schedule/Form \| File Number \| Exhibit \| Filing Date \| \| 3.1 \| Amended and Restated Certificate of Incorporation \| S-… |
| 7 | `NVDA_FY2020_2020-01-26:387` | Item 15 › EXHIBIT INDEX |  |  | \| \| \| Incorporated by Reference \| \| \| \| \|---\|---\|---\|---\|---\|---\| \| Exhibit No. \| Exhibit Description \| Schedule/Form \| File Number \| Exhibit \| Filing Date \| \| 2.1 \| Agreement and Plan of Merger, dated March 10, 2019, by… |
| 8 | `NVDA_FY2016_2016-01-31:206` | Item 9 |  |  | None. |
| 9 | `NVDA_FY2020_2020-01-26:193` | Item 9B |  |  | None. |
| 10 | `NVDA_FY2020_2020-01-26:67` | Item 1 › Table of Contents |  |  | amended, are available free of charge on or through our web site, http://www.nvidia.com, as soon as reasonably practicable after we electronically file such material with, or furnish it to, the Securities and Exchange Co… |

RQ2 citation match (section level): `no citations`

### System B (hybrid + rerank)

Model: `gpt-5.4-2026-03-05`. Hops: 1. Chunks retrieved: 5, cited: 2.

**Generated answer**

> In NVIDIA’s FY2016 10-K, its currently issued patents had expiration dates ranging from **April 2016 to December 2034** [2]. In its FY2020 10-K, the range was **March 2020 to October 2039** [1].
>
> So, between FY2016 and FY2020:
> - The **earliest expiration date** moved from **April 2016** to **March 2020** [1][2].
> - The **latest expiration date** extended from **December 2034** to **October 2039** [1][2].

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `NVDA_FY2020_2020-01-26:55` | Item 1 › Patents and Proprietary Rights | ✓ | #1, #2 | We rely primarily on a combination of patents, trademarks, trade secrets, employee and third-party nondisclosure agreements, and licensing arrangements to protect our intellectual property in the United States and intern… |
| 2 | `NVDA_FY2016_2016-01-31:43` | Item 1 › Patents and Proprietary Rights | ✓ | #1, #2 | We rely primarily on a combination of patents, trademarks, trade secrets, employee and third-party nondisclosure agreements and licensing arrangements to protect our intellectual property in the United States and interna… |
| 3 | `NVDA_FY2020_2020-01-26:387` | Item 15 › EXHIBIT INDEX |  |  | \| \| \| Incorporated by Reference \| \| \| \| \|---\|---\|---\|---\|---\|---\| \| Exhibit No. \| Exhibit Description \| Schedule/Form \| File Number \| Exhibit \| Filing Date \| \| 2.1 \| Agreement and Plan of Merger, dated March 10, 2019, by… |
| 4 | `NVDA_FY2016_2016-01-31:0` |  |  |  | 10-K 1 nvda-2016x10k.htm FORM 10-K |
| 5 | `NVDA_FY2020_2020-01-26:129` | Item 6 |  |  | (A) In fiscal year 2016, we began the wind down of our Icera modem operations. As a result, our income from operations for fiscal year 2016 included $131 million of restructuring and other charges. (B) In fiscal year 201… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#1 `NVDA_FY2020_2020-01-26:55`** (cited, gold #1, gold #2)

````text
ITEM 1. BUSINESS > Patents and Proprietary Rights
We rely primarily on a combination of patents, trademarks, trade secrets, employee and third-party nondisclosure agreements, and licensing arrangements to protect our intellectual property in the United States and internationally. Our currently issued patents have expiration dates from March 2020 to October 2039. We have numerous patents issued, allowed, and pending in the United States and in foreign jurisdictions. Our patents and pending patent applications primarily relate to our products and the technology used in connection with our products. We also rely on international treaties, organizations, and foreign laws to protect our intellectual property. The laws of certain foreign countries in which our products are or may be manufactured or sold, including various countries in Asia, may not protect our products or intellectual property rights to the same extent as the laws of the United States. This decreased protection makes the possibility of piracy of our technology and products more likely. We continuously assess whether and where to seek formal protection for particular innovations and technologies based on such factors as: • the location in which our products are manufactured; • our strategic technology or product directions in different countries;
````

**#2 `NVDA_FY2016_2016-01-31:43`** (cited, gold #1, gold #2)

````text
ITEM 1. BUSINESS > Patents and Proprietary Rights
We rely primarily on a combination of patents, trademarks, trade secrets, employee and third-party nondisclosure agreements and licensing arrangements to protect our intellectual property in the United States and internationally. Our currently issued patents have expiration dates from April 2016 to December 2034. We have numerous patents issued, allowed and pending in the United States and in foreign jurisdictions. Our patents and pending patent applications primarily relate to our products and the technology used in connection with our products. We also rely on international treaties, organizations and foreign laws to protect our intellectual property. The laws of certain foreign countries in which our products are or may be manufactured or sold, including various countries in Asia, may not protect our products or intellectual property rights to the same extent as the laws of the United States. This decreased protection makes the possibility of piracy of our technology and products more likely. We continuously assess whether and where to seek formal protection for particular innovations and technologies based on such factors as: •the location in which our products are manufactured; •our strategic technology or product directions in different countries;
````

</details>

RQ2 citation match (section level): `cited=[('NVDA', 'Item 1')] gold=[(None, 'Item 1')]`

### System C v1 (adaptive multi-hop)

Model: `gpt-5.4`. Hops: 1. Chunks retrieved: 6, cited: 2.

**Generated answer**

> In NVIDIA’s fiscal year 2016 10-K, its currently issued patents had expiration dates ranging from April 2016 to December 2034 [NVDA FY2016, Item 1, NVDA_FY2016_2016-01-31:43]. In NVIDIA’s fiscal year 2020 10-K, its currently issued patents had expiration dates ranging from March 2020 to October 2039 [NVDA FY2020, Item 1, NVDA_FY2020_2020-01-26:55]. Therefore, the patent expiration range shifted later at both ends, from April 2016–December 2034 in fiscal 2016 to March 2020–October 2039 in fiscal 2020 [NVDA FY2020, Item 1, NVDA_FY2020_2020-01-26:55] [NVDA FY2016, Item 1, NVDA_FY2016_2016-01-31:43].

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `NVDA_FY2020_2020-01-26:55` | Item 1 › Patents and Proprietary Rights | ✓ | #1, #2 | We rely primarily on a combination of patents, trademarks, trade secrets, employee and third-party nondisclosure agreements, and licensing arrangements to protect our intellectual property in the United States and intern… |
| 2 | `NVDA_FY2016_2016-01-31:43` | Item 1 › Patents and Proprietary Rights | ✓ | #1, #2 | We rely primarily on a combination of patents, trademarks, trade secrets, employee and third-party nondisclosure agreements and licensing arrangements to protect our intellectual property in the United States and interna… |
| 3 | `NVDA_FY2016_2016-01-31:372` | Item 15 › (Continued) |  |  | as to that patent. On February 24, 2016, the ITC determined to review in part the ALJ’s ID and asked for further briefing from the parties as to certain issues and patents. As the ITC did not seek to review the findings … |
| 4 | `NVDA_FY2020_2020-01-26:181` | Item 7 › Adoption of New and Recently Issued Accounting Pronouncements |  |  | Refer to Note 1 of the Notes to the Consolidated Financial Statements in Part IV, Item 15 of this Annual Report on Form 10-K for a discussion of adoption of new and recently issued accounting pronouncements. |
| 5 | `NVDA_FY2016_2016-01-31:335` | Item 15 › (Continued) |  |  | (1) Consists primarily of consideration received in advance of our performance obligations under the patent cross licensing agreement that we entered into with Intel Corporation in January 2011. The decrease in deferred … |
| 6 | `NVDA_FY2020_2020-01-26:388` | Item 15 › EXHIBIT INDEX |  |  | \| \| \| Incorporated by Reference \| \| \| \| \|---\|---\|---\|---\|---\|---\| \| 4.3 \| Indenture, dated as of September 16, 2016, by and between the Company and Wells Fargo Bank, National Association, as Trustee \| 8-K \| 0-23985 \| 4.1… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#1 `NVDA_FY2020_2020-01-26:55`** (cited, gold #1, gold #2)

````text
ITEM 1. BUSINESS > Patents and Proprietary Rights
We rely primarily on a combination of patents, trademarks, trade secrets, employee and third-party nondisclosure agreements, and licensing arrangements to protect our intellectual property in the United States and internationally. Our currently issued patents have expiration dates from March 2020 to October 2039. We have numerous patents issued, allowed, and pending in the United States and in foreign jurisdictions. Our patents and pending patent applications primarily relate to our products and the technology used in connection with our products. We also rely on international treaties, organizations, and foreign laws to protect our intellectual property. The laws of certain foreign countries in which our products are or may be manufactured or sold, including various countries in Asia, may not protect our products or intellectual property rights to the same extent as the laws of the United States. This decreased protection makes the possibility of piracy of our technology and products more likely. We continuously assess whether and where to seek formal protection for particular innovations and technologies based on such factors as: • the location in which our products are manufactured; • our strategic technology or product directions in different countries;
````

**#2 `NVDA_FY2016_2016-01-31:43`** (cited, gold #1, gold #2)

````text
ITEM 1. BUSINESS > Patents and Proprietary Rights
We rely primarily on a combination of patents, trademarks, trade secrets, employee and third-party nondisclosure agreements and licensing arrangements to protect our intellectual property in the United States and internationally. Our currently issued patents have expiration dates from April 2016 to December 2034. We have numerous patents issued, allowed and pending in the United States and in foreign jurisdictions. Our patents and pending patent applications primarily relate to our products and the technology used in connection with our products. We also rely on international treaties, organizations and foreign laws to protect our intellectual property. The laws of certain foreign countries in which our products are or may be manufactured or sold, including various countries in Asia, may not protect our products or intellectual property rights to the same extent as the laws of the United States. This decreased protection makes the possibility of piracy of our technology and products more likely. We continuously assess whether and where to seek formal protection for particular innovations and technologies based on such factors as: •the location in which our products are manufactured; •our strategic technology or product directions in different countries;
````

</details>

RQ2 citation match (section level): `cited=[('NVDA', 'Item 1')] gold=[(None, 'Item 1')]`

**System C guardrail** (judge `gpt-5.4`): numerical claims 0, verified 0, ungrounded 0, uncited 0, derived 0; sentence verdicts: supported 3, partial 0, unsupported 0, unchecked 0.


<details><summary>Guardrail sentence verdicts</summary>

| sentence | verdict | judge reason |
|---|---|---|
| In NVIDIA’s fiscal year 2016 10-K, its currently issued patents had expiration dates ranging from April 2016 to December 2034 [NVDA FY2016, Item 1, NVDA_FY2016_2016-01-31:43]. | supported | The cited FY2016 passage states the patents expired from April 2016 to December 2034. |
| In NVIDIA’s fiscal year 2020 10-K, its currently issued patents had expiration dates ranging from March 2020 to October 2039 [NVDA FY2020, Item 1, NVDA_FY2020_2020-01-26:55]. | supported | The cited FY2020 passage states the patents expired from March 2020 to October 2039. |
| Therefore, the patent expiration range shifted later at both ends, from April 2016–December 2034 in fiscal 2016 to March 2020–October 2039 in fiscal 2020 [NVDA FY2020, Item 1, NVDA_FY2020_2020-01-26:55] [NVDA FY2016, Item 1, NVDA_FY2016_2016-01-31:43]. | supported | The two cited passages show both the earliest and latest expiration dates moved later from FY2016 to FY2020. |

</details>

### System C v2 (agentic multi-hop + XBRL)

Model: `gpt-5.4`. Hops: 1. Chunks retrieved: 6, cited: 2.

**Generated answer**

> In NVIDIA’s fiscal year 2016 10-K, its currently issued patents had expiration dates ranging from April 2016 to December 2034 [NVDA FY2016, Item 1, NVDA_FY2016_2016-01-31:43]. In NVIDIA’s fiscal year 2020 10-K, its currently issued patents had expiration dates ranging from March 2020 to October 2039 [NVDA FY2020, Item 1, NVDA_FY2020_2020-01-26:55]. Compared with fiscal year 2016, the start of the range moved later from April 2016 to March 2020, and the end of the range extended from December 2034 to October 2039 [NVDA FY2016, Item 1, NVDA_FY2016_2016-01-31:43] [NVDA FY2020, Item 1, NVDA_FY2020_2020-01-26:55].

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `NVDA_FY2020_2020-01-26:55` | Item 1 › Patents and Proprietary Rights | ✓ | #1, #2 | We rely primarily on a combination of patents, trademarks, trade secrets, employee and third-party nondisclosure agreements, and licensing arrangements to protect our intellectual property in the United States and intern… |
| 2 | `NVDA_FY2016_2016-01-31:43` | Item 1 › Patents and Proprietary Rights | ✓ | #1, #2 | We rely primarily on a combination of patents, trademarks, trade secrets, employee and third-party nondisclosure agreements and licensing arrangements to protect our intellectual property in the United States and interna… |
| 3 | `NVDA_FY2020_2020-01-26:43` | Item 1 › Table of Contents |  |  | Leveraging our intellectual property. We believe our intellectual property is a valuable asset that can be accessed by our customers and partners through licenses and development agreements when they desire to build such… |
| 4 | `NVDA_FY2016_2016-01-31:345` | Item 15 › Note 10 - Guarantees |  |  | In connection with certain agreements that we have executed in the past, we have at times provided indemnities to cover the indemnified party for matters such as tax, product and employee liabilities. We have also on occ… |
| 5 | `NVDA_FY2016_2016-01-31:372` | Item 15 › (Continued) |  |  | as to that patent. On February 24, 2016, the ITC determined to review in part the ALJ’s ID and asked for further briefing from the parties as to certain issues and patents. As the ITC did not seek to review the findings … |
| 6 | `NVDA_FY2020_2020-01-26:388` | Item 15 › EXHIBIT INDEX |  |  | \| \| \| Incorporated by Reference \| \| \| \| \|---\|---\|---\|---\|---\|---\| \| 4.3 \| Indenture, dated as of September 16, 2016, by and between the Company and Wells Fargo Bank, National Association, as Trustee \| 8-K \| 0-23985 \| 4.1… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#1 `NVDA_FY2020_2020-01-26:55`** (cited, gold #1, gold #2)

````text
ITEM 1. BUSINESS > Patents and Proprietary Rights
We rely primarily on a combination of patents, trademarks, trade secrets, employee and third-party nondisclosure agreements, and licensing arrangements to protect our intellectual property in the United States and internationally. Our currently issued patents have expiration dates from March 2020 to October 2039. We have numerous patents issued, allowed, and pending in the United States and in foreign jurisdictions. Our patents and pending patent applications primarily relate to our products and the technology used in connection with our products. We also rely on international treaties, organizations, and foreign laws to protect our intellectual property. The laws of certain foreign countries in which our products are or may be manufactured or sold, including various countries in Asia, may not protect our products or intellectual property rights to the same extent as the laws of the United States. This decreased protection makes the possibility of piracy of our technology and products more likely. We continuously assess whether and where to seek formal protection for particular innovations and technologies based on such factors as: • the location in which our products are manufactured; • our strategic technology or product directions in different countries;
````

**#2 `NVDA_FY2016_2016-01-31:43`** (cited, gold #1, gold #2)

````text
ITEM 1. BUSINESS > Patents and Proprietary Rights
We rely primarily on a combination of patents, trademarks, trade secrets, employee and third-party nondisclosure agreements and licensing arrangements to protect our intellectual property in the United States and internationally. Our currently issued patents have expiration dates from April 2016 to December 2034. We have numerous patents issued, allowed and pending in the United States and in foreign jurisdictions. Our patents and pending patent applications primarily relate to our products and the technology used in connection with our products. We also rely on international treaties, organizations and foreign laws to protect our intellectual property. The laws of certain foreign countries in which our products are or may be manufactured or sold, including various countries in Asia, may not protect our products or intellectual property rights to the same extent as the laws of the United States. This decreased protection makes the possibility of piracy of our technology and products more likely. We continuously assess whether and where to seek formal protection for particular innovations and technologies based on such factors as: •the location in which our products are manufactured; •our strategic technology or product directions in different countries;
````

</details>

RQ2 citation match (section level): `cited=[('NVDA', 'Item 1')] gold=[(None, 'Item 1')]`

**System C guardrail** (judge `gpt-5.4`): numerical claims 0, verified 0, ungrounded 0, uncited 0, derived 0; sentence verdicts: supported 3, partial 0, unsupported 0, unchecked 0.


<details><summary>Guardrail sentence verdicts</summary>

| sentence | verdict | judge reason |
|---|---|---|
| In NVIDIA’s fiscal year 2016 10-K, its currently issued patents had expiration dates ranging from April 2016 to December 2034 [NVDA FY2016, Item 1, NVDA_FY2016_2016-01-31:43]. | supported | The cited FY2016 evidence states the patents had expiration dates from April 2016 to December 2034. |
| In NVIDIA’s fiscal year 2020 10-K, its currently issued patents had expiration dates ranging from March 2020 to October 2039 [NVDA FY2020, Item 1, NVDA_FY2020_2020-01-26:55]. | supported | The cited FY2020 evidence states the patents had expiration dates from March 2020 to October 2039. |
| Compared with fiscal year 2016, the start of the range moved later from April 2016 to March 2020, and the end of the range extended from December 2034 to October 2039 [NVDA FY2016, Item 1, NVDA_FY2016_2016-01-31:43] [NVDA FY2020, Item 1, NVDA_FY2020_2020-01-26:55]. | supported | The two cited passages show the range changed from April 2016–December 2034 to March 2020–October 2039. |

</details>
