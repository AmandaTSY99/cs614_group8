# gold-071: Cross-year table

[← all cases](../README.md) · company: MICROSOFT CORP (MSFT) · fiscal year: 2019 · recipe `cross_year_table` · hop `multi` · answer type `numeric` · scope `cross_year` · RQ2 category `multi_company_comparison`

## Gold QA

**Question**

> By how much did Microsoft's operating income increase in fiscal year 2019 compared to fiscal year 2016 (in millions)?

**Gold answer**

> $22,777 million

**Program**: `subtract(42959, 20182)` → `22777.0`

**Gold numbers** (RQ2 numeric_accuracy targets): $22,777 million

**Gold evidence**

1. `MSFT_FY2019_2019-06-30` · Item 7 › PART II · table

   > | Operating income | 42,959 | 35,058 | 29,025 | 23% | 21% |

2. `MSFT_FY2016_2016-06-30` · ITEM 7. MANAGEMENT’S DISCUSSION AND ANALYSIS OF FINANCIAL CONDITION AND RESULTS OF OPERATIONS › PART II · table

   > | Operating income | $20,182 | $18,161 | $27,759 | 11% | (35)% |

## Scorecard

| Metric | A (vanilla dense) | B (hybrid + rerank) | C v1 (adaptive multi-hop) | C v2 (agentic multi-hop + XBRL) |
|---|---|---|---|---|
| **Retrieval (RQ1)** | | | | |
| chunks retrieved | 10 | 5 | 13 | 8 |
| recall@5 | 0.00 | 0.00 | 0.50 | 0.50 |
| recall@all | 0.00 | 0.00 | 1.00 | 0.50 |
| complete@all | 0 | 0 | 1 | 0 |
| average precision (lexical) | 0.00 | 0.00 | 0.47 | 0.30 |
| gold evidence first rank | #1: –, #2: – | #1: –, #2: – | #1: 2, #2: 7 | #1: 4, #2: – |
| **Answer (RQ3 string match)** | | | | |
| numeric_correct | ✗ | ✗ | ✓ | ✓ |
| keypoint_recall | – | – | – | – |
| **Answer & citations (RQ2)** | | | | |
| numeric_accuracy | 0.00 | 0.00 | 1.00 | 1.00 |
| citation precision | 1.00 | – | 0.00 | 0.00 |
| citation recall | 1.00 | – | 0.00 | 0.00 |
| citation F1 | 1.00 | – | 0.00 | 0.00 |
| has a citation | 1 | 0 | 1 | 1 |
| grounding error rate | – | – | 0.33 | 0.00 |
| **Cost (RQ3)** | | | | |
| retrieval hops | 1 | 1 | 3 | 1 |
| tokens | 1949 | 1428 | 19702 | 8342 |
| cost (USD) | 0.0004 | 0.0002 | 0.0623 | 0.0259 |
| latency (s) | 3.3 | 5.0 | 21.6 | 7.5 |

Definitions: [README › Metrics](../README.md#metrics). `–` = not applicable (e.g. no gold number, no citations, no guardrail).

## System outputs

### System A (vanilla dense)

Model: `gpt-5.4-2026-03-05`. Hops: 1. Chunks retrieved: 10, cited: 1.

**Generated answer**

> The provided context gives Microsoft’s operating income change for fiscal year 2019 vs. 2018, but it does not provide Microsoft’s operating income for fiscal year 2016, so the full comparison cannot be calculated from the context.
>
> What is in the context:
> - Fiscal year 2019 operating income increased by **$7.9 billion** vs. fiscal year 2018, which is **$7,900 million** [1].
>
> What is missing:
> - Microsoft’s **operating income for fiscal year 2016** is not provided in the context.
> - Therefore, the increase in operating income in fiscal year 2019 compared to fiscal year 2016 cannot be determined from the provided context. [1]

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `MSFT_FY2019_2019-06-30:170` | Item 7 › Fiscal Year 2019 Compared with Fiscal Year 2018 | ✓ |  | Revenue increased $15.5 billion or 14%, driven by growth across each of our segments. Intelligent Cloud revenue increased, driven by server products and cloud services. Productivity and Business Processes revenue increas… |
| 2 | `MSFT_FY2019_2019-06-30:172` | Item 7 › Fiscal Year 2018 Compared with Fiscal Year 2017 |  |  | Revenue increased $13.8 billion or 14%, driven by growth across each of our segments. Productivity and Business Processes revenue increased, driven by LinkedIn and higher revenue from Office. Intelligent Cloud revenue in… |
| 3 | `MSFT_FY2019_2019-06-30:177` | Item 7 › Fiscal Year 2019 Compared with Fiscal Year 2018 |  |  | Productivity and Business Processes Revenue increased $5.3 billion or 15%. • Office Commercial revenue increased $3.2 billion or 13%, driven by Office 365 Commercial, offset in part by lower revenue from products license… |
| 4 | `MSFT_FY2019_2019-06-30:200` | Item 7 › Fiscal Year 2019 Compared with Fiscal Year 2018 |  |  | General and administrative expenses increased $131 million or 3%. |
| 5 | `MSFT_FY2019_2019-06-30:224` | Item 7 › Fiscal Year 2019 Compared with Fiscal Year 2018 |  |  | Cash from operations increased $8.3 billion to $52.2 billion for fiscal year 2019, mainly due to an increase in cash received from customers, offset in part by an increase in cash paid to suppliers and employees and an i… |
| 6 | `MSFT_FY2019_2019-06-30:182` | Item 7 › Fiscal Year 2018 Compared with Fiscal Year 2017 |  |  | Productivity and Business Processes Revenue increased $6.0 billion or 20%. • LinkedIn revenue increased $3.0 billion to $5.3 billion. Fiscal year 2018 included a full period of results, whereas fiscal year 2017 only incl… |
| 7 | `MSFT_FY2019_2019-06-30:184` | Item 7 › Fiscal Year 2018 Compared with Fiscal Year 2017 |  |  | • Enterprise Services revenue increased $304 million or 5%, driven by higher revenue from Premier Support Services and Microsoft Consulting Services, offset in part by a decline in revenue from custom support agreements.… |
| 8 | `MSFT_FY2019_2019-06-30:192` | Item 7 › Fiscal Year 2019 Compared with Fiscal Year 2018 |  |  | Research and development expenses increased $2.2 billion or 15%, driven by investments in cloud and AI engineering, Gaming, LinkedIn, and GitHub. |
| 9 | `MSFT_FY2016_2016-06-30:162` | Item 7 › PART II |  |  | Fiscal year 2015 compared with fiscal year 2014 Revenue increased $6.7 billion or 8%, primarily due to higher revenue from More Personal Computing and Intelligent Cloud. More Personal Computing revenue increased, primari… |
| 10 | `MSFT_FY2019_2019-06-30:185` | Item 7 › Fiscal Year 2018 Compared with Fiscal Year 2017 |  |  | • Gaming revenue increased $1.3 billion or 14%, driven by Xbox software and services revenue growth of 20%, mainly from third-party title strength. |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#1 `MSFT_FY2019_2019-06-30:170`** (cited)

````text
Item 7 > Fiscal Year 2019 Compared with Fiscal Year 2018
Revenue increased $15.5 billion or 14%, driven by growth across each of our segments. Intelligent Cloud revenue increased, driven by server products and cloud services. Productivity and Business Processes revenue increased, driven by Office and LinkedIn. More Personal Computing revenue increased, driven by Surface, Gaming, and Windows. Gross margin increased $10.9 billion or 15%, driven by growth across each of our segments. Gross margin percentage increased slightly, due to gross margin percentage improvement across each of our segments and favorable segment sales mix. Gross margin included a 5 percentage point improvement in commercial cloud, primarily from Azure. Operating income increased $7.9 billion or 23%, driven by growth across each of our segments. Key changes in expenses were: • Cost of revenue increased $4.6 billion or 12%, driven by growth in commercial cloud, Surface, and Gaming. • Research and development expenses increased $2.2 billion or 15%, driven by investments in cloud and artificial intelligence (“AI”) engineering, Gaming, LinkedIn, and GitHub. • Sales and marketing expenses increased $744 million or 4%, driven by investments in commercial sales capacity, LinkedIn, and GitHub, offset in part by a decrease in marketing. Sales and marketing expenses included a favorable foreign currency impact of 2%.
````

</details>

RQ2 citation match (section level): `cited=[('MSFT', 'Item 7')] gold=[(None, 'Item 7')]`

### System B (hybrid + rerank)

Model: `gpt-5.4-2026-03-05`. Hops: 1. Chunks retrieved: 5, cited: 0.

**Generated answer**

> Not found in the provided context.

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `MSFT_FY2019_2019-06-30:170` | Item 7 › Fiscal Year 2019 Compared with Fiscal Year 2018 |  |  | Revenue increased $15.5 billion or 14%, driven by growth across each of our segments. Intelligent Cloud revenue increased, driven by server products and cloud services. Productivity and Business Processes revenue increas… |
| 2 | `MSFT_FY2019_2019-06-30:159` | Item 7 |  |  | Highlights from fiscal year 2019 compared with fiscal year 2018 included: • Commercial cloud revenue, which includes Microsoft Office 365 Commercial, Microsoft Azure, the commercial portion of LinkedIn, Microsoft Dynamic… |
| 3 | `MSFT_FY2019_2019-06-30:184` | Item 7 › Fiscal Year 2018 Compared with Fiscal Year 2017 |  |  | • Enterprise Services revenue increased $304 million or 5%, driven by higher revenue from Premier Support Services and Microsoft Consulting Services, offset in part by a decline in revenue from custom support agreements.… |
| 4 | `MSFT_FY2019_2019-06-30:224` | Item 7 › Fiscal Year 2019 Compared with Fiscal Year 2018 |  |  | Cash from operations increased $8.3 billion to $52.2 billion for fiscal year 2019, mainly due to an increase in cash received from customers, offset in part by an increase in cash paid to suppliers and employees and an i… |
| 5 | `MSFT_FY2019_2019-06-30:183` | Item 7 › Fiscal Year 2018 Compared with Fiscal Year 2017 |  |  | • Gross margin increased $4.4 billion or 19%, driven by LinkedIn and growth in Office Commercial. Gross margin percentage decreased slightly, due to an increased mix of cloud offerings, offset in part by gross margin per… |

RQ2 citation match (section level): `no citations`

### System C v1 (adaptive multi-hop)

Model: `gpt-5.4`. Hops: 3. Chunks retrieved: 13, cited: 2.

**Generated answer**

> Microsoft's operating income increased by $22,777 million in fiscal year 2019 compared to fiscal year 2016, calculated as $42,959 million minus $20,182 million [MSFT FY2019, Item 8, MSFT_FY2019_2019-06-30:259] [MSFT FY2016, Item 8, MSFT_FY2016_2016-06-30:249].
>
> > [Guardrail Audit Warning]: Manual verification required; these numerical figures could not be matched in their cited chunks: 22,777; 1 sentence(s) are not supported by their cited chunks.

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `MSFT_FY2019_2019-06-30:470` | Item 8 › PART II |  |  | Segment revenue and operating income were as follows during the periods presented: |
| 2 | `MSFT_FY2019_2019-06-30:259` | Item 8 › INCOME STATEMENTS | ✓ | #1 | \| (In millions, except per share amounts) \| \| \| \| \|---\|---\|---\|---\| \| Year Ended June 30, \| 2019 \| 2018 \| 2017 \| \| Revenue: \| \| \| \| \| Product \| $66,069 \| $64,497 \| $63,811 \| \| Service and other \| 59,774 \| 45,863 \| 32,760… |
| 3 | `MSFT_FY2019_2019-06-30:481` | Item 8 › PART II |  |  | \| Fiscal Year 2018 \| \| \| \| \| \| \|---\|---\|---\|---\|---\|---\| \| Revenue \| $24,538 \| $28,918 \| $26,819 \| $30,085 \| $110,360 \| \| Gross margin \| 16,260 \| 17,854 \| 17,550 \| 20,343 \| 72,007 \| \| Operating income \| 7,708 \| 8,679 \| 8… |
| 4 | `MSFT_FY2019_2019-06-30:480` | Item 8 › PART II |  |  | \| (In millions, except per share amounts) \| \| \| \| \| \| \|---\|---\|---\|---\|---\|---\| \| Quarter Ended \| September 30 \| December 31 \| March 31 \| June 30 \| Total \| \| Fiscal Year 2019 \| \| \| \| \| \| \| Revenue \| $29,084 \| $32,471 \| $… |
| 5 | `MSFT_FY2019_2019-06-30:168` | Item 7 › PART II |  | #1 | \| (In millions, except percentages and per share amounts) \| 2019 \| 2018 \| 2017 \| Percentage Change 2019 Versus 2018 \| Percentage Change 2018 Versus 2017 \| \|---\|---\|---\|---\|---\|---\| \| Revenue \| $125,843 \| $110,360 \| $96,5… |
| 6 | `MSFT_FY2019_2019-06-30:471` | Item 8 › PART II |  | #1 | \| (In millions) \| \| \| \| \|---\|---\|---\|---\| \| Year Ended June 30, \| 2019 \| 2018 \| 2017 \| \| Revenue \| \| \| \| \| Productivity and Business Processes \| $41,160 \| $35,865 \| $29,870 \| \| Intelligent Cloud \| 38,985 \| 32,219 \| 27,40… |
| 7 | `MSFT_FY2016_2016-06-30:249` | Item 8 › INCOME STATEMENTS | ✓ | #2 | \| (In millions, except per share amounts) \| \| \| \| \|---\|---\|---\|---\| \| Year Ended June 30, \| 2016 \| 2015 \| 2014 \| \| Revenue: \| \| \| \| \| Product \| $61,502 \| $75,956 \| $72,948 \| \| Service and other \| 23,818 \| 17,624 \| 13,885… |
| 8 | `MSFT_FY2016_2016-06-30:483` | Item 8 › PART II |  |  | \| (In millions, except per share amounts) \| \| \| \| \| \| \| \| \|---\|---\|---\|---\|---\|---\|---\|---\| \| Quarter Ended \| September 30 \| December 31 \| March 31 \| June 30 \| Total \| \| \| \| Fiscal Year 2016 \| \| \| \| \| \| \| \| \| Revenue (a)… |
| 9 | `MSFT_FY2016_2016-06-30:484` | Item 8 › PART II |  |  | \| (In millions, except per share amounts) \| \| \| \| \| \| \| \| \|---\|---\|---\|---\|---\|---\|---\|---\| \| Operating income (loss) \| 5,844 \| 7,776 \| 6,594 \| (2,053) \| \| 18,161 \| \| \| Net income (loss) \| 4,540 \| 5,863 \| 4,985 \| (3,195 … |
| 10 | `MSFT_FY2016_2016-06-30:257` | Item 8 › CASH FLOWS STATEMENTS |  |  | \| (In millions) \| \| \| \| \|---\|---\|---\|---\| \| Year Ended June 30, \| 2016 \| 2015 \| 2014 \| \| Operations \| \| \| \| \| Net income \| $16,798 \| $12,193 \| $22,074 \| \| Adjustments to reconcile net income to net cash from operations: … |
| 11 | `MSFT_FY2016_2016-06-30:250` | Item 8 › INCOME STATEMENTS |  |  | \| (In millions, except per share amounts) \| \| \| \| \|---\|---\|---\|---\| \| Provision for income taxes \| 2,953 \| 6,314 \| 5,746 \| \| Net income \| $16,798 \| $12,193 \| $22,074 \| \| Earnings per share: \| \| \| \| \| Basic \| $2.12 \| $1.4… |
| 12 | `MSFT_FY2019_2019-06-30:260` | Item 8 › INCOME STATEMENTS |  |  | \| (In millions, except per share amounts) \| \| \| \| \|---\|---\|---\|---\| \| Net income \| $39,240 \| $16,571 \| $25,489 \| \| Earnings per share: \| \| \| \| \| Basic \| $5.11 \| $2.15 \| $3.29 \| \| Diluted \| $5.06 \| $2.13 \| $3.25 \| \| Weigh… |
| 13 | `MSFT_FY2016_2016-06-30:164` | Item 7 › PART II |  | #2 | \| (In millions, except percentages) \| 2016 \| 2015 \| 2014 \| Percentage Change 2016 Versus 2015 \| Percentage Change 2015 Versus 2014 \| \|---\|---\|---\|---\|---\|---\| \| Revenue \| \| \| \| \| \| \| Productivity and Business Processes \|… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#2 `MSFT_FY2019_2019-06-30:259`** (cited, gold #1)

````text
Item 8 > INCOME STATEMENTS (table)
| (In millions, except per share amounts) |  |  |  |
|---|---|---|---|
| Year Ended June 30, | 2019 | 2018 | 2017 |
| Revenue: |  |  |  |
| Product | $66,069 | $64,497 | $63,811 |
| Service and other | 59,774 | 45,863 | 32,760 |
| Total revenue | 125,843 | 110,360 | 96,571 |
| Cost of revenue: |  |  |  |
| Product | 16,273 | 15,420 | 15,175 |
| Service and other | 26,637 | 22,933 | 19,086 |
| Total cost of revenue | 42,910 | 38,353 | 34,261 |
| Gross margin | 82,933 | 72,007 | 62,310 |
| Research and development | 16,876 | 14,726 | 13,037 |
| Sales and marketing | 18,213 | 17,469 | 15,461 |
| General and administrative | 4,885 | 4,754 | 4,481 |
| Restructuring | 0 | 0 | 306 |
| Operating income | 42,959 | 35,058 | 29,025 |
| Other income, net | 729 | 1,416 | 876 |
| Income before income taxes | 43,688 | 36,474 | 29,901 |
| Provision for income taxes | 4,448 | 19,903 | 4,412 |
````

**#5 `MSFT_FY2019_2019-06-30:168`** (gold #1)

````text
Item 7 > PART II (table)
| (In millions, except percentages and per share amounts) | 2019 | 2018 | 2017 | Percentage Change 2019 Versus 2018 | Percentage Change 2018 Versus 2017 |
|---|---|---|---|---|---|
| Revenue | $125,843 | $110,360 | $96,571 | 14% | 14% |
| Gross margin | 82,933 | 72,007 | 62,310 | 15% | 16% |
| Operating income | 42,959 | 35,058 | 29,025 | 23% | 21% |
| Net income | 39,240 | 16,571 | 25,489 | 137% | (35)% |
| Diluted earnings per share | 5.06 | 2.13 | 3.25 | 138% | (34)% |
| Non-GAAP operating income | 42,959 | 35,058 | 29,331 | 23% | 20% |
| Non-GAAP net income | 36,830 | 30,267 | 25,732 | 22% | 18% |
| Non-GAAP diluted earnings per share | 4.75 | 3.88 | 3.29 | 22% | 18% |
````

**#6 `MSFT_FY2019_2019-06-30:471`** (gold #1)

````text
Item 8 > PART II (table)
| (In millions) |  |  |  |
|---|---|---|---|
| Year Ended June 30, | 2019 | 2018 | 2017 |
| Revenue |  |  |  |
| Productivity and Business Processes | $41,160 | $35,865 | $29,870 |
| Intelligent Cloud | 38,985 | 32,219 | 27,407 |
| More Personal Computing | 45,698 | 42,276 | 39,294 |
| Total | $125,843 | $110,360 | $96,571 |
| Operating Income (Loss) |  |  |  |
| Productivity and Business Processes | $16,219 | $12,924 | $11,389 |
| Intelligent Cloud | 13,920 | 11,524 | 9,127 |
| More Personal Computing | 12,820 | 10,610 | 8,815 |
| Corporate and Other | 0 | 0 | (306) |
| Total | $42,959 | $35,058 | $29,025 |
````

**#7 `MSFT_FY2016_2016-06-30:249`** (cited, gold #2)

````text
Item 8 > INCOME STATEMENTS (table)
| (In millions, except per share amounts) |  |  |  |
|---|---|---|---|
| Year Ended June 30, | 2016 | 2015 | 2014 |
| Revenue: |  |  |  |
| Product | $61,502 | $75,956 | $72,948 |
| Service and other | 23,818 | 17,624 | 13,885 |
| Total revenue | 85,320 | 93,580 | 86,833 |
| Cost of revenue: |  |  |  |
| Product | 17,880 | 21,410 | 16,681 |
| Service and other | 14,900 | 11,628 | 10,397 |
| Total cost of revenue | 32,780 | 33,038 | 27,078 |
| Gross margin | 52,540 | 60,542 | 59,755 |
| Research and development | 11,988 | 12,046 | 11,381 |
| Sales and marketing | 14,697 | 15,713 | 15,811 |
| General and administrative | 4,563 | 4,611 | 4,677 |
| Impairment, integration, and restructuring | 1,110 | 10,011 | 127 |
| Operating income | 20,182 | 18,161 | 27,759 |
| Other income (expense), net | (431) | 346 | 61 |
| Income before income taxes | 19,751 | 18,507 | 27,820 |
````

**#13 `MSFT_FY2016_2016-06-30:164`** (gold #2)

````text
ITEM 7. MANAGEMENT’S DISCUSSION AND ANALYSIS OF FINANCIAL CONDITION AND RESULTS OF OPERATIONS > PART II (table)
| (In millions, except percentages) | 2016 | 2015 | 2014 | Percentage Change 2016 Versus 2015 | Percentage Change 2015 Versus 2014 |
|---|---|---|---|---|---|
| Revenue |  |  |  |  |  |
| Productivity and Business Processes | $26,487 | $26,430 | $26,976 | 0% | (2)% |
| Intelligent Cloud | 25,042 | 23,715 | 21,735 | 6% | 9% |
| More Personal Computing | 40,460 | 43,160 | 38,460 | (6)% | 12% |
| Corporate and Other | (6,669) | 275 | (338) | * | * |
| Total revenue | $85,320 | $93,580 | $86,833 | (9)% | 8% |
| Operating income (loss) |  |  |  |  |  |
| Productivity and Business Processes | $12,461 | $13,359 | $14,173 | (7)% | (6)% |
| Intelligent Cloud | 9,358 | 9,871 | 8,446 | (5)% | 17% |
| More Personal Computing | 6,142 | 4,667 | 5,605 | 32% | (17)% |
| Corporate and Other | (7,779) | (9,736) | (465) | * | * |
| Total operating income | $20,182 | $18,161 | $27,759 | 11% | (35)% |
````

</details>

RQ2 citation match (section level): `cited=[('MSFT', 'Item 8')] gold=[(None, 'Item 7')]`

**System C guardrail** (judge `gpt-5.4`): numerical claims 3, verified 2, ungrounded 1, uncited 0, derived 0; sentence verdicts: supported 0, partial 0, unsupported 0, unchecked 0.

- ungrounded numbers: 22,777

<details><summary>Guardrail sentence verdicts</summary>

| sentence | verdict | judge reason |
|---|---|---|
| Microsoft's operating income increased by $22,777 million in fiscal year 2019 compared to fiscal year 2016, calculated as $42,959 million minus $20,182 million [MSFT FY2019, Item 8, MSFT_FY2019_2019-06-30:259] [MSFT FY2016, Item 8, MSFT_FY2016_2016-06-30:249]. | None |  |

</details>

### System C v2 (agentic multi-hop + XBRL)

Model: `gpt-5.4`. Hops: 1. Chunks retrieved: 8, cited: 2.

**Generated answer**

> Microsoft's operating income increased by $22,777 million in fiscal year 2019 compared to fiscal year 2016, calculated as $42,959 million minus $20,182 million. [F-MSFT-2019] [F-MSFT-2016]

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `F-MSFT-2016` | SEC XBRL Reported Financials (financials.csv) | ✓ |  | fiscal_year,fiscal_year_end,Revenue,NetIncome,OperatingIncome,TotalAssets,TotalLiabilities,StockholdersEquity,CashAndEquivalents,OperatingCashFlow,EPSDiluted 2016,2016-06-30,85320000000,16798000000,20182000000,1936940000… |
| 2 | `F-MSFT-2019` | SEC XBRL Reported Financials (financials.csv) | ✓ |  | fiscal_year,fiscal_year_end,Revenue,NetIncome,OperatingIncome,TotalAssets,TotalLiabilities,StockholdersEquity,CashAndEquivalents,OperatingCashFlow,EPSDiluted 2019,2019-06-30,125843000000,39240000000,42959000000,286556000… |
| 3 | `MSFT_FY2019_2019-06-30:470` | Item 8 › PART II |  |  | Segment revenue and operating income were as follows during the periods presented: |
| 4 | `MSFT_FY2019_2019-06-30:259` | Item 8 › INCOME STATEMENTS |  | #1 | \| (In millions, except per share amounts) \| \| \| \| \|---\|---\|---\|---\| \| Year Ended June 30, \| 2019 \| 2018 \| 2017 \| \| Revenue: \| \| \| \| \| Product \| $66,069 \| $64,497 \| $63,811 \| \| Service and other \| 59,774 \| 45,863 \| 32,760… |
| 5 | `MSFT_FY2019_2019-06-30:481` | Item 8 › PART II |  |  | \| Fiscal Year 2018 \| \| \| \| \| \| \|---\|---\|---\|---\|---\|---\| \| Revenue \| $24,538 \| $28,918 \| $26,819 \| $30,085 \| $110,360 \| \| Gross margin \| 16,260 \| 17,854 \| 17,550 \| 20,343 \| 72,007 \| \| Operating income \| 7,708 \| 8,679 \| 8… |
| 6 | `MSFT_FY2019_2019-06-30:480` | Item 8 › PART II |  |  | \| (In millions, except per share amounts) \| \| \| \| \| \| \|---\|---\|---\|---\|---\|---\| \| Quarter Ended \| September 30 \| December 31 \| March 31 \| June 30 \| Total \| \| Fiscal Year 2019 \| \| \| \| \| \| \| Revenue \| $29,084 \| $32,471 \| $… |
| 7 | `MSFT_FY2019_2019-06-30:168` | Item 7 › PART II |  | #1 | \| (In millions, except percentages and per share amounts) \| 2019 \| 2018 \| 2017 \| Percentage Change 2019 Versus 2018 \| Percentage Change 2018 Versus 2017 \| \|---\|---\|---\|---\|---\|---\| \| Revenue \| $125,843 \| $110,360 \| $96,5… |
| 8 | `MSFT_FY2019_2019-06-30:471` | Item 8 › PART II |  | #1 | \| (In millions) \| \| \| \| \|---\|---\|---\|---\| \| Year Ended June 30, \| 2019 \| 2018 \| 2017 \| \| Revenue \| \| \| \| \| Productivity and Business Processes \| $41,160 \| $35,865 \| $29,870 \| \| Intelligent Cloud \| 38,985 \| 32,219 \| 27,40… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#1 `F-MSFT-2016`** (cited)

````text
[F-MSFT-2016] (MSFT FY2016 reported financials; amounts in USD, EPSDiluted in USD per share)
fiscal_year,fiscal_year_end,Revenue,NetIncome,OperatingIncome,TotalAssets,TotalLiabilities,StockholdersEquity,CashAndEquivalents,OperatingCashFlow,EPSDiluted
2016,2016-06-30,85320000000,16798000000,20182000000,193694000000,121697000000,71997000000,6510000000,33325000000,2.1
````

**#2 `F-MSFT-2019`** (cited)

````text
[F-MSFT-2019] (MSFT FY2019 reported financials; amounts in USD, EPSDiluted in USD per share)
fiscal_year,fiscal_year_end,Revenue,NetIncome,OperatingIncome,TotalAssets,TotalLiabilities,StockholdersEquity,CashAndEquivalents,OperatingCashFlow,EPSDiluted
2019,2019-06-30,125843000000,39240000000,42959000000,286556000000,184226000000,102330000000,11356000000,52185000000,5.06
````

**#4 `MSFT_FY2019_2019-06-30:259`** (gold #1)

````text
Item 8 > INCOME STATEMENTS (table)
| (In millions, except per share amounts) |  |  |  |
|---|---|---|---|
| Year Ended June 30, | 2019 | 2018 | 2017 |
| Revenue: |  |  |  |
| Product | $66,069 | $64,497 | $63,811 |
| Service and other | 59,774 | 45,863 | 32,760 |
| Total revenue | 125,843 | 110,360 | 96,571 |
| Cost of revenue: |  |  |  |
| Product | 16,273 | 15,420 | 15,175 |
| Service and other | 26,637 | 22,933 | 19,086 |
| Total cost of revenue | 42,910 | 38,353 | 34,261 |
| Gross margin | 82,933 | 72,007 | 62,310 |
| Research and development | 16,876 | 14,726 | 13,037 |
| Sales and marketing | 18,213 | 17,469 | 15,461 |
| General and administrative | 4,885 | 4,754 | 4,481 |
| Restructuring | 0 | 0 | 306 |
| Operating income | 42,959 | 35,058 | 29,025 |
| Other income, net | 729 | 1,416 | 876 |
| Income before income taxes | 43,688 | 36,474 | 29,901 |
| Provision for income taxes | 4,448 | 19,903 | 4,412 |
````

**#7 `MSFT_FY2019_2019-06-30:168`** (gold #1)

````text
Item 7 > PART II (table)
| (In millions, except percentages and per share amounts) | 2019 | 2018 | 2017 | Percentage Change 2019 Versus 2018 | Percentage Change 2018 Versus 2017 |
|---|---|---|---|---|---|
| Revenue | $125,843 | $110,360 | $96,571 | 14% | 14% |
| Gross margin | 82,933 | 72,007 | 62,310 | 15% | 16% |
| Operating income | 42,959 | 35,058 | 29,025 | 23% | 21% |
| Net income | 39,240 | 16,571 | 25,489 | 137% | (35)% |
| Diluted earnings per share | 5.06 | 2.13 | 3.25 | 138% | (34)% |
| Non-GAAP operating income | 42,959 | 35,058 | 29,331 | 23% | 20% |
| Non-GAAP net income | 36,830 | 30,267 | 25,732 | 22% | 18% |
| Non-GAAP diluted earnings per share | 4.75 | 3.88 | 3.29 | 22% | 18% |
````

**#8 `MSFT_FY2019_2019-06-30:471`** (gold #1)

````text
Item 8 > PART II (table)
| (In millions) |  |  |  |
|---|---|---|---|
| Year Ended June 30, | 2019 | 2018 | 2017 |
| Revenue |  |  |  |
| Productivity and Business Processes | $41,160 | $35,865 | $29,870 |
| Intelligent Cloud | 38,985 | 32,219 | 27,407 |
| More Personal Computing | 45,698 | 42,276 | 39,294 |
| Total | $125,843 | $110,360 | $96,571 |
| Operating Income (Loss) |  |  |  |
| Productivity and Business Processes | $16,219 | $12,924 | $11,389 |
| Intelligent Cloud | 13,920 | 11,524 | 9,127 |
| More Personal Computing | 12,820 | 10,610 | 8,815 |
| Corporate and Other | 0 | 0 | (306) |
| Total | $42,959 | $35,058 | $29,025 |
````

</details>

RQ2 citation match (section level): `cited=[('MSFT', 'XBRL')] gold=[(None, 'Item 7')]`

**System C guardrail** (judge `gpt-5.4`): numerical claims 3, verified 3, ungrounded 0, uncited 0, derived 1; sentence verdicts: supported 0, partial 0, unsupported 0, unchecked 0.


<details><summary>Guardrail sentence verdicts</summary>

| sentence | verdict | judge reason |
|---|---|---|
| Microsoft's operating income increased by $22,777 million in fiscal year 2019 compared to fiscal year 2016, calculated as $42,959 million minus $20,182 million. [F-MSFT-2019] [F-MSFT-2016] | None |  |

</details>
