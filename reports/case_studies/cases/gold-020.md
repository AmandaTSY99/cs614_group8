# gold-020: Multi-hop text (one filing)

[← all cases](../README.md) · company: MICROSOFT CORP (MSFT) · fiscal year: 2015 · recipe `text` · hop `multi` · answer type `qualitative` · scope `single_doc` · RQ2 category `cross_section_multihop`

## Gold QA

**Question**

> According to Microsoft's fiscal year 2015 10-K, which executive serves as both General Counsel and Chief Compliance Officer, and on which other company's board of directors does that executive serve?

**Gold answer**

> Mr. Smith. He was appointed Executive Vice President, General Counsel, and Secretary in 2011 (after serving as Senior Vice President, General Counsel, and Secretary since November 2001), was named Chief Compliance Officer in 2002, and serves on the Board of Directors of Netflix, Inc.

**Key points** (RQ3 keypoint_recall targets)

1. Mr. Smith is Executive Vice President, General Counsel, and Secretary (since 2011).
2. Mr. Smith was named Chief Compliance Officer in 2002.
3. Mr. Smith serves on the Board of Directors of Netflix, Inc.

**Gold evidence**

1. `MSFT_FY2015_2015-06-30` · Item 1 › PART I · text

   > Mr. Smith was appointed Executive Vice President, General Counsel, and Secretary in 2011.

2. `MSFT_FY2015_2015-06-30` · Item 1 › PART I · text

   > Mr. Smith was also named Chief Compliance Officer in 2002.

3. `MSFT_FY2015_2015-06-30` · Item 1 › PART I · text

   > Mr. Smith also serves on the Board of Directors of Netflix, Inc.

## Scorecard

| Metric | A (vanilla dense) | B (hybrid + rerank) | C v1 (adaptive multi-hop) | C v2 (agentic multi-hop + XBRL) |
|---|---|---|---|---|
| **Retrieval (RQ1)** | | | | |
| chunks retrieved | 10 | 5 | 10 | 14 |
| recall@5 | 1.00 | 1.00 | 1.00 | 1.00 |
| recall@all | 1.00 | 1.00 | 1.00 | 1.00 |
| complete@all | 1 | 1 | 1 | 1 |
| average precision (lexical) | 1.00 | 0.87 | 0.64 | 0.64 |
| gold evidence first rank | #1: 1, #2: 1, #3: 1 | #1: 1, #2: 1, #3: 1 | #1: 1, #2: 1, #3: 1 | #1: 1, #2: 1, #3: 1 |
| **Answer (RQ3 string match)** | | | | |
| numeric_correct | ✗ | ✗ | ✓ | ✓ |
| keypoint_recall | 1.00 | 0.67 | 1.00 | 1.00 |
| **Answer & citations (RQ2)** | | | | |
| numeric_accuracy | – | – | – | – |
| citation precision | 1.00 | 1.00 | 1.00 | 1.00 |
| citation recall | 1.00 | 1.00 | 1.00 | 1.00 |
| citation F1 | 1.00 | 1.00 | 1.00 | 1.00 |
| has a citation | 1 | 1 | 1 | 1 |
| grounding error rate | – | – | 0.00 | 0.00 |
| **Cost (RQ3)** | | | | |
| retrieval hops | 1 | 1 | 3 | 3 |
| tokens | 2140 | 930 | 11898 | 14410 |
| cost (USD) | 0.0003 | 0.0002 | 0.0433 | 0.0493 |
| latency (s) | 1.7 | 5.8 | 21.5 | 26.2 |

Definitions: [README › Metrics](../README.md#metrics). `–` = not applicable (e.g. no gold number, no citations, no guardrail).

## System outputs

### System A (vanilla dense)

Model: `gpt-5.4-2026-03-05`. Hops: 1. Chunks retrieved: 10, cited: 2.

**Generated answer**

> The executive is **Bradford L. Smith**. He served as **Executive Vice President, General Counsel; Secretary** and was also named **Chief Compliance Officer**. He also serves on the **Board of Directors of Netflix, Inc.** [1][3]

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `MSFT_FY2015_2015-06-30:73` | Item 1 › PART I | ✓ | #1, #2, #3 | Mr. Smith was appointed Executive Vice President, General Counsel, and Secretary in 2011. Prior to that he served as Senior Vice President, General Counsel, and Secretary since November 2001. Mr. Smith was also named Chi… |
| 2 | `MSFT_FY2015_2015-06-30:501` | Item 15 › SIGNATURES |  |  | \| Signature \| Title \| \|---\|---\| \| /S/ JOHN W. THOMPSON John W. Thompson \| Chairman \| \| /S/ SATYA NADELLA Satya Nadella \| Director and Chief Executive Officer \| \| /S/ WILLIAM H. GATES III William H. Gates III \| Director \|… |
| 3 | `MSFT_FY2015_2015-06-30:70` | Item 1 › PART I | ✓ |  | \| Name \| Age \| Position with the Company \| \|---\|---\|---\| \| Satya Nadella \| 47 \| Chief Executive Officer \| \| Christopher C. Capossela \| 45 \| Executive Vice President, Chief Marketing Officer \| \| Kathleen T. Hogan \| 49 \| E… |
| 4 | `MSFT_FY2015_2015-06-30:479` | Item 10 |  |  | A list of our executive officers and biographical information appears in Part I, Item 1 of this Form 10-K. Information about our directors may be found under the caption “Our director nominees” in our Proxy Statement for… |
| 5 | `MSFT_FY2015_2015-06-30:500` | Item 15 › SIGNATURES |  |  | Pursuant to the requirements of Section 13 or 15(d) of the Securities Exchange Act of 1934, the Registrant has duly caused this report to be signed on its behalf by the undersigned; thereunto duly authorized, in the City… |
| 6 | `MSFT_FY2015_2015-06-30:13` | INDEX |  |  | \| \| \| Page \| \| \|---\|---\|---\|---\| \| \| Item 9A. \| Controls and Procedures \| 99 \| \| \| \| Report of Management on Internal Control over Financial Reporting \| 99 \| \| \| \| Report of Independent Registered Public Accounting Firm … |
| 7 | `MSFT_FY2015_2015-06-30:12` | INDEX |  |  | \| \| \| Page \| \| \|---\|---\|---\|---\| \| PART I \| \| \| \| \| \| Item 1. \| Business \| 3 \| \| \| \| Executive Officers of the Registrant \| 16 \| \| \| Item 1A. \| Risk Factors \| 18 \| \| \| Item 1B. \| Unresolved Staff Comments \| 26 \| \| \| Item… |
| 8 | `MSFT_FY2015_2015-06-30:0` |  |  |  | 10-K 1 d918813d10k.htm 10-K |
| 9 | `MSFT_FY2015_2015-06-30:497` | Item 15 › PART IV |  |  | \| \| \| \| Incorporated by Reference \| \| \| \| \|---\|---\|---\|---\|---\|---\|---\| \| 12 \| Computation of Ratio of Earnings to Fixed Charges \| X \| \| \| \| \| \| 21 \| Subsidiaries of Registrant \| X \| \| \| \| \| \| 23.1 \| Consent of Independe… |
| 10 | `MSFT_FY2015_2015-06-30:480` | Item 10 |  |  | We have adopted the Microsoft Finance Code of Professional Conduct (the “finance code of ethics”), a code of ethics that applies to our Chief Executive Officer, Chief Financial Officer, Chief Accounting Officer and Corpo… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#1 `MSFT_FY2015_2015-06-30:73`** (cited, gold #1, gold #2, gold #3)

````text
Item 1 > PART I
Mr. Smith was appointed Executive Vice President, General Counsel, and Secretary in 2011. Prior to that he served as Senior Vice President, General Counsel, and Secretary since November 2001. Mr. Smith was also named Chief Compliance Officer in 2002. He had been Deputy General Counsel for Worldwide Sales and previously was responsible for managing the European Law and Corporate Affairs Group, based in Paris. Mr. Smith joined Microsoft in 1993. Mr. Smith also serves on the Board of Directors of Netflix, Inc.
````

**#3 `MSFT_FY2015_2015-06-30:70`** (cited)

````text
Item 1 > PART I (table)
| Name | Age | Position with the Company |
|---|---|---|
| Satya Nadella | 47 | Chief Executive Officer |
| Christopher C. Capossela | 45 | Executive Vice President, Chief Marketing Officer |
| Kathleen T. Hogan | 49 | Executive Vice President, Human Resources |
| Amy E. Hood | 43 | Executive Vice President, Chief Financial Officer |
| Margaret Johnson | 53 | Executive Vice President, Business Development |
| Bradford L. Smith | 56 | Executive Vice President, General Counsel; Secretary |
| B. Kevin Turner | 50 | Chief Operating Officer |
````

</details>

RQ2 citation match (section level): `cited=[('MSFT', 'Item 1')] gold=[(None, 'Item 1')]`

### System B (hybrid + rerank)

Model: `gpt-5.4-2026-03-05`. Hops: 1. Chunks retrieved: 5, cited: 1.

**Generated answer**

> Mr. Smith serves as both General Counsel and Chief Compliance Officer, and he serves on the Board of Directors of Netflix, Inc. [1]

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `MSFT_FY2015_2015-06-30:73` | Item 1 › PART I | ✓ | #1, #2, #3 | Mr. Smith was appointed Executive Vice President, General Counsel, and Secretary in 2011. Prior to that he served as Senior Vice President, General Counsel, and Secretary since November 2001. Mr. Smith was also named Chi… |
| 2 | `MSFT_FY2015_2015-06-30:74` | Item 1 › PART I |  | #1, #2, #3 | Mr. Turner was appointed Chief Operating Officer in September 2005. Before joining Microsoft, he was Executive Vice President of Wal-Mart Stores, Inc. and President and Chief Executive Officer of the Sam’s Club division.… |
| 3 | `MSFT_FY2015_2015-06-30:0` |  |  |  | 10-K 1 d918813d10k.htm 10-K |
| 4 | `MSFT_FY2015_2015-06-30:479` | Item 10 |  |  | A list of our executive officers and biographical information appears in Part I, Item 1 of this Form 10-K. Information about our directors may be found under the caption “Our director nominees” in our Proxy Statement for… |
| 5 | `MSFT_FY2015_2015-06-30:72` | Item 1 › PART I |  | #3 | Ms. Hood was appointed Executive Vice President and Chief Financial Officer in July 2013, subsequent to her appointment as Chief Financial Officer in May 2013. Beginning in 2010, Ms. Hood was Chief Financial Officer of t… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#1 `MSFT_FY2015_2015-06-30:73`** (cited, gold #1, gold #2, gold #3)

````text
Item 1 > PART I
Mr. Smith was appointed Executive Vice President, General Counsel, and Secretary in 2011. Prior to that he served as Senior Vice President, General Counsel, and Secretary since November 2001. Mr. Smith was also named Chief Compliance Officer in 2002. He had been Deputy General Counsel for Worldwide Sales and previously was responsible for managing the European Law and Corporate Affairs Group, based in Paris. Mr. Smith joined Microsoft in 1993. Mr. Smith also serves on the Board of Directors of Netflix, Inc.
````

**#2 `MSFT_FY2015_2015-06-30:74`** (gold #1, gold #2, gold #3)

````text
Item 1 > PART I
Mr. Turner was appointed Chief Operating Officer in September 2005. Before joining Microsoft, he was Executive Vice President of Wal-Mart Stores, Inc. and President and Chief Executive Officer of the Sam’s Club division. From 2001 to 2002, he served as Executive Vice President and Chief Information Officer of Wal-Mart’s Information Systems Division. From 2000 to 2001, he served as its Senior Vice President and Chief Information Officer of the Information Systems Division. Mr. Turner also serves on the Board of Directors of Nordstrom, Inc. EMPLOYEES As of June 30, 2015, we employed approximately 118,000 people on a full-time basis, 60,000 in the U.S. and 58,000 internationally. Of the total employed people, 39,000 were in product research and development, 29,000 in sales and marketing, 32,000 in product support and consulting services, 8,000 in manufacturing and distribution, and 10,000 in general and administration. In June 2015, management approved a restructuring plan that will eliminate up to 7,800 positions in fiscal year 2016, primarily in our Phone Hardware business. As a result of the NDS acquisition, we have certain employees that are subject to collective bargaining agreements. AVAILABLE INFORMATION
````

**#5 `MSFT_FY2015_2015-06-30:72`** (gold #3)

````text
Item 1 > PART I
Ms. Hood was appointed Executive Vice President and Chief Financial Officer in July 2013, subsequent to her appointment as Chief Financial Officer in May 2013. Beginning in 2010, Ms. Hood was Chief Financial Officer of the Microsoft Business Division. From 2006 through 2009, Ms. Hood was General Manager, Microsoft Business Division Strategy. Since joining Microsoft in 2002, Ms. Hood has also held finance-related positions in the Server and Tools Business and the corporate finance organization. Ms. Johnson was appointed Executive Vice President, Business Development in September 2014. Prior to that Ms. Johnson spent 24 years at Qualcomm in various leadership positions across engineering, sales, marketing and business development. She most recently served as Executive Vice President of Qualcomm Technologies, Inc. Ms. Johnson also serves on the Board of Directors of Live Nation Entertainment, Inc.
````

</details>

RQ2 citation match (section level): `cited=[('MSFT', 'Item 1')] gold=[(None, 'Item 1')]`

### System C v1 (adaptive multi-hop)

Model: `gpt-5.4`. Hops: 3. Chunks retrieved: 10, cited: 2.

**Generated answer**

> Bradford L. Smith serves as Executive Vice President, General Counsel, and Secretary, and he was also named Chief Compliance Officer in 2002 [MSFT FY2015, Item 1, MSFT_FY2015_2015-06-30:70] [MSFT FY2015, Item 1, MSFT_FY2015_2015-06-30:73]. He also serves on the Board of Directors of Netflix, Inc. [MSFT FY2015, Item 1, MSFT_FY2015_2015-06-30:73]

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `MSFT_FY2015_2015-06-30:73` | Item 1 › PART I | ✓ | #1, #2, #3 | Mr. Smith was appointed Executive Vice President, General Counsel, and Secretary in 2011. Prior to that he served as Senior Vice President, General Counsel, and Secretary since November 2001. Mr. Smith was also named Chi… |
| 2 | `MSFT_FY2015_2015-06-30:479` | Item 10 |  |  | A list of our executive officers and biographical information appears in Part I, Item 1 of this Form 10-K. Information about our directors may be found under the caption “Our director nominees” in our Proxy Statement for… |
| 3 | `MSFT_FY2015_2015-06-30:70` | Item 1 › PART I | ✓ |  | \| Name \| Age \| Position with the Company \| \|---\|---\|---\| \| Satya Nadella \| 47 \| Chief Executive Officer \| \| Christopher C. Capossela \| 45 \| Executive Vice President, Chief Marketing Officer \| \| Kathleen T. Hogan \| 49 \| E… |
| 4 | `MSFT_FY2015_2015-06-30:480` | Item 10 |  |  | We have adopted the Microsoft Finance Code of Professional Conduct (the “finance code of ethics”), a code of ethics that applies to our Chief Executive Officer, Chief Financial Officer, Chief Accounting Officer and Corpo… |
| 5 | `MSFT_FY2015_2015-06-30:12` | INDEX |  |  | \| \| \| Page \| \| \|---\|---\|---\|---\| \| PART I \| \| \| \| \| \| Item 1. \| Business \| 3 \| \| \| \| Executive Officers of the Registrant \| 16 \| \| \| Item 1A. \| Risk Factors \| 18 \| \| \| Item 1B. \| Unresolved Staff Comments \| 26 \| \| \| Item… |
| 6 | `MSFT_FY2015_2015-06-30:13` | INDEX |  |  | \| \| \| Page \| \| \|---\|---\|---\|---\| \| \| Item 9A. \| Controls and Procedures \| 99 \| \| \| \| Report of Management on Internal Control over Financial Reporting \| 99 \| \| \| \| Report of Independent Registered Public Accounting Firm … |
| 7 | `MSFT_FY2015_2015-06-30:74` | Item 1 › PART I |  | #1, #2, #3 | Mr. Turner was appointed Chief Operating Officer in September 2005. Before joining Microsoft, he was Executive Vice President of Wal-Mart Stores, Inc. and President and Chief Executive Officer of the Sam’s Club division.… |
| 8 | `MSFT_FY2015_2015-06-30:421` | Item 8 › Dividends |  |  | In fiscal year 2015, our Board of Directors declared the following dividends: |
| 9 | `MSFT_FY2015_2015-06-30:494` | Item 15 › PART IV |  |  | \| \| \| \| Incorporated by Reference \| \| \| \| \|---\|---\|---\|---\|---\|---\|---\| \| 10.1* \| Microsoft Corporation 2001 Stock Plan \| \| 10-Q \| 12/31/11 \| 10.1 \| 1/19/12 \| \| 10.3* \| Microsoft Corporation 1999 Stock Plan for Non-Emplo… |
| 10 | `MSFT_FY2015_2015-06-30:69` | Item 1 › PART I |  |  | CUSTOMERS Our customers include individual consumers, small- and medium-sized organizations, large global enterprises, public sector institutions, Internet service providers, application developers, and OEMs. No sales to… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#1 `MSFT_FY2015_2015-06-30:73`** (cited, gold #1, gold #2, gold #3)

````text
Item 1 > PART I
Mr. Smith was appointed Executive Vice President, General Counsel, and Secretary in 2011. Prior to that he served as Senior Vice President, General Counsel, and Secretary since November 2001. Mr. Smith was also named Chief Compliance Officer in 2002. He had been Deputy General Counsel for Worldwide Sales and previously was responsible for managing the European Law and Corporate Affairs Group, based in Paris. Mr. Smith joined Microsoft in 1993. Mr. Smith also serves on the Board of Directors of Netflix, Inc.
````

**#3 `MSFT_FY2015_2015-06-30:70`** (cited)

````text
Item 1 > PART I (table)
| Name | Age | Position with the Company |
|---|---|---|
| Satya Nadella | 47 | Chief Executive Officer |
| Christopher C. Capossela | 45 | Executive Vice President, Chief Marketing Officer |
| Kathleen T. Hogan | 49 | Executive Vice President, Human Resources |
| Amy E. Hood | 43 | Executive Vice President, Chief Financial Officer |
| Margaret Johnson | 53 | Executive Vice President, Business Development |
| Bradford L. Smith | 56 | Executive Vice President, General Counsel; Secretary |
| B. Kevin Turner | 50 | Chief Operating Officer |
````

**#7 `MSFT_FY2015_2015-06-30:74`** (gold #1, gold #2, gold #3)

````text
Item 1 > PART I
Mr. Turner was appointed Chief Operating Officer in September 2005. Before joining Microsoft, he was Executive Vice President of Wal-Mart Stores, Inc. and President and Chief Executive Officer of the Sam’s Club division. From 2001 to 2002, he served as Executive Vice President and Chief Information Officer of Wal-Mart’s Information Systems Division. From 2000 to 2001, he served as its Senior Vice President and Chief Information Officer of the Information Systems Division. Mr. Turner also serves on the Board of Directors of Nordstrom, Inc. EMPLOYEES As of June 30, 2015, we employed approximately 118,000 people on a full-time basis, 60,000 in the U.S. and 58,000 internationally. Of the total employed people, 39,000 were in product research and development, 29,000 in sales and marketing, 32,000 in product support and consulting services, 8,000 in manufacturing and distribution, and 10,000 in general and administration. In June 2015, management approved a restructuring plan that will eliminate up to 7,800 positions in fiscal year 2016, primarily in our Phone Hardware business. As a result of the NDS acquisition, we have certain employees that are subject to collective bargaining agreements. AVAILABLE INFORMATION
````

</details>

RQ2 citation match (section level): `cited=[('MSFT', 'Item 1')] gold=[(None, 'Item 1')]`

**System C guardrail** (judge `gpt-5.4`): numerical claims 0, verified 0, ungrounded 0, uncited 0, derived 0; sentence verdicts: supported 2, partial 0, unsupported 0, unchecked 0.


<details><summary>Guardrail sentence verdicts</summary>

| sentence | verdict | judge reason |
|---|---|---|
| Bradford L. | None |  |
| Smith serves as Executive Vice President, General Counsel, and Secretary, and he was also named Chief Compliance Officer in 2002 [MSFT FY2015, Item 1, MSFT_FY2015_2015-06-30:70] [MSFT FY2015, Item 1, MSFT_FY2015_2015-06-30:73]. | supported | The evidence states Smith is Executive Vice President, General Counsel, and Secretary and that he was named Chief Compliance Officer in 2002. |
| He also serves on the Board of Directors of Netflix, Inc. [MSFT FY2015, Item 1, MSFT_FY2015_2015-06-30:73] | supported | The cited evidence explicitly says Mr. Smith serves on the Board of Directors of Netflix, Inc. |

</details>

### System C v2 (agentic multi-hop + XBRL)

Model: `gpt-5.4`. Hops: 3. Chunks retrieved: 14, cited: 2.

**Generated answer**

> Bradford L. Smith serves as Executive Vice President, General Counsel, and Secretary, and he was also named Chief Compliance Officer in 2002. He also serves on the Board of Directors of Netflix, Inc. [MSFT FY2015, Item 1, MSFT_FY2015_2015-06-30:73] [MSFT FY2015, Item 1, MSFT_FY2015_2015-06-30:70]

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `MSFT_FY2015_2015-06-30:73` | Item 1 › PART I | ✓ | #1, #2, #3 | Mr. Smith was appointed Executive Vice President, General Counsel, and Secretary in 2011. Prior to that he served as Senior Vice President, General Counsel, and Secretary since November 2001. Mr. Smith was also named Chi… |
| 2 | `MSFT_FY2015_2015-06-30:70` | Item 1 › PART I | ✓ |  | \| Name \| Age \| Position with the Company \| \|---\|---\|---\| \| Satya Nadella \| 47 \| Chief Executive Officer \| \| Christopher C. Capossela \| 45 \| Executive Vice President, Chief Marketing Officer \| \| Kathleen T. Hogan \| 49 \| E… |
| 3 | `MSFT_FY2015_2015-06-30:72` | Item 1 › PART I |  | #3 | Ms. Hood was appointed Executive Vice President and Chief Financial Officer in July 2013, subsequent to her appointment as Chief Financial Officer in May 2013. Beginning in 2010, Ms. Hood was Chief Financial Officer of t… |
| 4 | `MSFT_FY2015_2015-06-30:501` | Item 15 › SIGNATURES |  |  | \| Signature \| Title \| \|---\|---\| \| /S/ JOHN W. THOMPSON John W. Thompson \| Chairman \| \| /S/ SATYA NADELLA Satya Nadella \| Director and Chief Executive Officer \| \| /S/ WILLIAM H. GATES III William H. Gates III \| Director \|… |
| 5 | `MSFT_FY2015_2015-06-30:497` | Item 15 › PART IV |  |  | \| \| \| \| Incorporated by Reference \| \| \| \| \|---\|---\|---\|---\|---\|---\|---\| \| 12 \| Computation of Ratio of Earnings to Fixed Charges \| X \| \| \| \| \| \| 21 \| Subsidiaries of Registrant \| X \| \| \| \| \| \| 23.1 \| Consent of Independe… |
| 6 | `MSFT_FY2015_2015-06-30:471` | Item 9A |  |  | Under the supervision and with the participation of our management, including the Chief Executive Officer and Chief Financial Officer, we have evaluated the effectiveness of our disclosure controls and procedures as requ… |
| 7 | `MSFT_FY2015_2015-06-30:479` | Item 10 |  |  | A list of our executive officers and biographical information appears in Part I, Item 1 of this Form 10-K. Information about our directors may be found under the caption “Our director nominees” in our Proxy Statement for… |
| 8 | `MSFT_FY2015_2015-06-30:481` | Item 11 |  |  | The information in the Proxy Statement set forth under the captions “Director compensation,” “Named executive officer compensation,” “Compensation Committee interlocks and insider participation,” and “Compensation Commit… |
| 9 | `MSFT_FY2015_2015-06-30:482` | Item 12 |  |  | The information in the Proxy Statement set forth under the captions “Information regarding beneficial ownership of principal shareholders, directors, and management” and “Equity compensation plan information” is incorpor… |
| 10 | `MSFT_FY2015_2015-06-30:483` | Item 13 |  |  | The information set forth in the Proxy Statement under the captions “Director independence” and “Certain relationships and related transactions” is incorporated herein by reference. |
| 11 | `MSFT_FY2015_2015-06-30:11` | DOCUMENTS INCORPORATED BY REFERENCE |  |  | Portions of the definitive Proxy Statement to be delivered to shareholders in connection with the Annual Meeting of Shareholders to be held on December 2, 2015 are incorporated by reference into Part III. |
| 12 | `MSFT_FY2015_2015-06-30:74` | Item 1 › PART I |  | #1, #2, #3 | Mr. Turner was appointed Chief Operating Officer in September 2005. Before joining Microsoft, he was Executive Vice President of Wal-Mart Stores, Inc. and President and Chief Executive Officer of the Sam’s Club division.… |
| 13 | `MSFT_FY2015_2015-06-30:495` | Item 15 › PART IV |  |  | \| \| \| \| Incorporated by Reference \| \| \| \| \|---\|---\|---\|---\|---\|---\|---\| \| 10.12 \| 2009 Officers’ Indemnification Trust Agreement between Microsoft Corporation and The Bank of New York Mellon Trust Company, as trustee \| \|… |
| 14 | `MSFT_FY2015_2015-06-30:421` | Item 8 › Dividends |  |  | In fiscal year 2015, our Board of Directors declared the following dividends: |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#1 `MSFT_FY2015_2015-06-30:73`** (cited, gold #1, gold #2, gold #3)

````text
Item 1 > PART I
Mr. Smith was appointed Executive Vice President, General Counsel, and Secretary in 2011. Prior to that he served as Senior Vice President, General Counsel, and Secretary since November 2001. Mr. Smith was also named Chief Compliance Officer in 2002. He had been Deputy General Counsel for Worldwide Sales and previously was responsible for managing the European Law and Corporate Affairs Group, based in Paris. Mr. Smith joined Microsoft in 1993. Mr. Smith also serves on the Board of Directors of Netflix, Inc.
````

**#2 `MSFT_FY2015_2015-06-30:70`** (cited)

````text
Item 1 > PART I (table)
| Name | Age | Position with the Company |
|---|---|---|
| Satya Nadella | 47 | Chief Executive Officer |
| Christopher C. Capossela | 45 | Executive Vice President, Chief Marketing Officer |
| Kathleen T. Hogan | 49 | Executive Vice President, Human Resources |
| Amy E. Hood | 43 | Executive Vice President, Chief Financial Officer |
| Margaret Johnson | 53 | Executive Vice President, Business Development |
| Bradford L. Smith | 56 | Executive Vice President, General Counsel; Secretary |
| B. Kevin Turner | 50 | Chief Operating Officer |
````

**#3 `MSFT_FY2015_2015-06-30:72`** (gold #3)

````text
Item 1 > PART I
Ms. Hood was appointed Executive Vice President and Chief Financial Officer in July 2013, subsequent to her appointment as Chief Financial Officer in May 2013. Beginning in 2010, Ms. Hood was Chief Financial Officer of the Microsoft Business Division. From 2006 through 2009, Ms. Hood was General Manager, Microsoft Business Division Strategy. Since joining Microsoft in 2002, Ms. Hood has also held finance-related positions in the Server and Tools Business and the corporate finance organization. Ms. Johnson was appointed Executive Vice President, Business Development in September 2014. Prior to that Ms. Johnson spent 24 years at Qualcomm in various leadership positions across engineering, sales, marketing and business development. She most recently served as Executive Vice President of Qualcomm Technologies, Inc. Ms. Johnson also serves on the Board of Directors of Live Nation Entertainment, Inc.
````

**#12 `MSFT_FY2015_2015-06-30:74`** (gold #1, gold #2, gold #3)

````text
Item 1 > PART I
Mr. Turner was appointed Chief Operating Officer in September 2005. Before joining Microsoft, he was Executive Vice President of Wal-Mart Stores, Inc. and President and Chief Executive Officer of the Sam’s Club division. From 2001 to 2002, he served as Executive Vice President and Chief Information Officer of Wal-Mart’s Information Systems Division. From 2000 to 2001, he served as its Senior Vice President and Chief Information Officer of the Information Systems Division. Mr. Turner also serves on the Board of Directors of Nordstrom, Inc. EMPLOYEES As of June 30, 2015, we employed approximately 118,000 people on a full-time basis, 60,000 in the U.S. and 58,000 internationally. Of the total employed people, 39,000 were in product research and development, 29,000 in sales and marketing, 32,000 in product support and consulting services, 8,000 in manufacturing and distribution, and 10,000 in general and administration. In June 2015, management approved a restructuring plan that will eliminate up to 7,800 positions in fiscal year 2016, primarily in our Phone Hardware business. As a result of the NDS acquisition, we have certain employees that are subject to collective bargaining agreements. AVAILABLE INFORMATION
````

</details>

RQ2 citation match (section level): `cited=[('MSFT', 'Item 1')] gold=[(None, 'Item 1')]`

**System C guardrail** (judge `gpt-5.4`): numerical claims 0, verified 0, ungrounded 0, uncited 0, derived 0; sentence verdicts: supported 2, partial 0, unsupported 0, unchecked 0.


<details><summary>Guardrail sentence verdicts</summary>

| sentence | verdict | judge reason |
|---|---|---|
| Bradford L. | None |  |
| Smith serves as Executive Vice President, General Counsel, and Secretary, and he was also named Chief Compliance Officer in 2002. | supported | The retrieved evidence states Smith is Executive Vice President, General Counsel, and Secretary and was named Chief Compliance Officer in 2002. |
| He also serves on the Board of Directors of Netflix, Inc. [MSFT FY2015, Item 1, MSFT_FY2015_2015-06-30:73] [MSFT FY2015, Item 1, MSFT_FY2015_2015-06-30:70] | supported | The cited evidence explicitly says Mr. Smith serves on the Board of Directors of Netflix, Inc. |

</details>
