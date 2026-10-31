# gold-069: Cross-year table

[← all cases](../README.md) · company: Apple Inc. (AAPL) · fiscal year: 2018 · recipe `cross_year_table` · hop `multi` · answer type `numeric` · scope `cross_year` · RQ2 category `multi_company_comparison`

## Gold QA

**Question**

> By what percentage did Apple Inc.'s ending accrued warranty and related costs decrease from fiscal year 2015 to fiscal year 2018?

**Gold answer**

> 22.76%

**Program**: `subtract(4780, 3692), divide(#0, 4780), multiply(#1, 100)` → `22.761506276150627`

**Gold numbers** (RQ2 numeric_accuracy targets): 22.76%

**Gold evidence**

1. `AAPL_FY2018_2018-09-29` · Item 8. Financial Statements and Supplementary Data › Accrued Warranty and Indemnification · table

   > Ending accrued warranty and related costs | $3,692 | $3,834 | $3,702

2. `AAPL_FY2015_2015-09-26` · Item 8. Financial Statements and Supplementary Data › Accrued Warranty and Indemnification · table

   > Ending accrued warranty and related costs | $4,780 | $4,159 | $2,967

## Scorecard

| Metric | A (vanilla dense) | B (hybrid + rerank) | C v1 (adaptive multi-hop) | C v2 (agentic multi-hop + XBRL) |
|---|---|---|---|---|
| **Retrieval (RQ1)** | | | | |
| chunks retrieved | 10 | 5 | 6 | 6 |
| recall@5 | 1.00 | 1.00 | 1.00 | 1.00 |
| recall@all | 1.00 | 1.00 | 1.00 | 1.00 |
| complete@all | 1 | 1 | 1 | 1 |
| average precision (lexical) | 1.00 | 0.58 | 0.83 | 0.83 |
| gold evidence first rank | #1: 1, #2: 1 | #1: 2, #2: 2 | #1: 1, #2: 1 | #1: 1, #2: 1 |
| **Answer (RQ3 string match)** | | | | |
| numeric_correct | ✓ | ✓ | ✓ | ✓ |
| keypoint_recall | – | – | – | – |
| **Answer & citations (RQ2)** | | | | |
| numeric_accuracy | 1.00 | 1.00 | 1.00 | 1.00 |
| citation precision | 1.00 | 1.00 | 1.00 | 1.00 |
| citation recall | 1.00 | 1.00 | 1.00 | 1.00 |
| citation F1 | 1.00 | 1.00 | 1.00 | 1.00 |
| has a citation | 1 | 1 | 1 | 1 |
| grounding error rate | – | – | 0.00 | 0.00 |
| **Cost (RQ3)** | | | | |
| retrieval hops | 1 | 1 | 1 | 1 |
| tokens | 1682 | 1173 | 3499 | 3508 |
| cost (USD) | 0.0003 | 0.0002 | 0.0134 | 0.0134 |
| latency (s) | 2.2 | 5.8 | 7.0 | 7.3 |

Definitions: [README › Metrics](../README.md#metrics). `–` = not applicable (e.g. no gold number, no citations, no guardrail).

## System outputs

### System A (vanilla dense)

Model: `gpt-5.4-2026-03-05`. Hops: 1. Chunks retrieved: 10, cited: 2.

**Generated answer**

> Apple’s ending accrued warranty and related costs were **$4,780 million** in fiscal 2015 and **$3,692 million** in fiscal 2018 [1][2].
>
> Percentage decrease:
>
> \[
> \frac{4,780 - 3,692}{4,780} \times 100 \approx 22.8\%
> \]
>
> So, the ending accrued warranty and related costs **decreased by about 22.8%** from 2015 to 2018 [1][2].

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `AAPL_FY2015_2015-09-26:377` | Item 8 › Accrued Warranty and Indemnification | ✓ | #1, #2 | \| \| 2015 \| 2014 \| 2013 \| \|---\|---\|---\|---\| \| Beginning accrued warranty and related costs \| $4,159 \| $2,967 \| $1,638 \| \| Cost of warranty claims \| (4,401) \| (3,760) \| (3,703) \| \| Accruals for product warranty \| 5,022 \| 4… |
| 2 | `AAPL_FY2018_2018-09-29:343` | Item 8 › Accrued Warranty and Indemnification | ✓ | #1, #2 | \| \| 2018 \| 2017 \| 2016 \| \|---\|---\|---\|---\| \| Beginning accrued warranty and related costs \| $3,834 \| $3,702 \| $4,780 \| \| Cost of warranty claims \| (4,115) \| (4,322) \| (4,663) \| \| Accruals for product warranty \| 3,973 \| 4… |
| 3 | `AAPL_FY2015_2015-09-26:376` | Item 8 › Accrued Warranty and Indemnification |  |  | The following table shows changes in the Company’s accrued warranties and related costs for 2015, 2014 and 2013 (in millions): |
| 4 | `AAPL_FY2018_2018-09-29:342` | Item 8 › Accrued Warranty and Indemnification |  |  | The following table shows changes in the Company’s accrued warranties and related costs for 2018, 2017 and 2016 (in millions): |
| 5 | `AAPL_FY2018_2018-09-29:137` | Item 7 › Product Performance |  |  | \| \| 2018 \| Change \| 2017 \| Change \| 2016 \| \|---\|---\|---\|---\|---\|---\| \| Net sales \| $37,190 \| 24% \| $29,980 \| 23% \| $24,348 \| \| Percentage of total net sales \| 14% \| \| 13% \| \| 11% \| |
| 6 | `AAPL_FY2018_2018-09-29:128` | Item 7 › Overview and Highlights |  |  | \| \| 2018 \| Change \| 2017 \| Change \| 2016 \| \|---\|---\|---\|---\|---\|---\| \| Total net sales \| $265,595 \| 16% \| $229,234 \| 6% \| $215,639 \| \| Unit Sales by Product: \| \| \| \| \| \| \| iPhone \| 217,722 \| —% \| 216,756 \| 2% \| 211,884 \|… |
| 7 | `AAPL_FY2018_2018-09-29:124` | Item 7 › Overview and Highlights |  |  | The Company’s fiscal year is the 52- or 53-week period that ends on the last Saturday of September. The Company’s fiscal years 2018 and 2016 spanned 52 weeks each, whereas fiscal year 2017 included 53 weeks. A 14th week … |
| 8 | `AAPL_FY2015_2015-09-26:151` | Item 7 › Product Performance |  |  | \| \| 2015 \| Change \| 2014 \| Change \| 2013 \| \|---\|---\|---\|---\|---\|---\| \| Net sales \| $19,909 \| 10% \| $18,063 \| 13% \| $16,051 \| \| Percentage of total net sales \| 9% \| \| 10% \| \| 9% \| |
| 9 | `AAPL_FY2015_2015-09-26:141` | Item 7 › Overview and Highlights |  |  | \| \| 2015 \| Change \| 2014 \| Change \| 2013 \| \|---\|---\|---\|---\|---\|---\| \| Total net sales \| $233,715 \| 28% \| $182,795 \| 7% \| $170,910 \| \| Unit Sales by Product: \| \| \| \| \| \| \| iPhone \| 231,218 \| 37% \| 169,219 \| 13% \| 150,257… |
| 10 | `AAPL_FY2018_2018-09-29:133` | Item 7 › Product Performance |  |  | \| \| 2018 \| Change \| 2017 \| Change \| 2016 \| \|---\|---\|---\|---\|---\|---\| \| Net sales \| $18,805 \| (2)% \| $19,222 \| (7)% \| $20,628 \| \| Percentage of total net sales \| 7% \| \| 8% \| \| 10% \| \| Unit sales \| 43,535 \| —% \| 43,753 \| (… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#1 `AAPL_FY2015_2015-09-26:377`** (cited, gold #1, gold #2)

````text
Item 8. Financial Statements and Supplementary Data > Accrued Warranty and Indemnification (table)
|  | 2015 | 2014 | 2013 |
|---|---|---|---|
| Beginning accrued warranty and related costs | $4,159 | $2,967 | $1,638 |
| Cost of warranty claims | (4,401) | (3,760) | (3,703) |
| Accruals for product warranty | 5,022 | 4,952 | 5,032 |
| Ending accrued warranty and related costs | $4,780 | $4,159 | $2,967 |
````

**#2 `AAPL_FY2018_2018-09-29:343`** (cited, gold #1, gold #2)

````text
Item 8. Financial Statements and Supplementary Data > Accrued Warranty and Indemnification (table)
|  | 2018 | 2017 | 2016 |
|---|---|---|---|
| Beginning accrued warranty and related costs | $3,834 | $3,702 | $4,780 |
| Cost of warranty claims | (4,115) | (4,322) | (4,663) |
| Accruals for product warranty | 3,973 | 4,454 | 3,585 |
| Ending accrued warranty and related costs | $3,692 | $3,834 | $3,702 |
````

</details>

RQ2 citation match (section level): `cited=[('AAPL', 'Item 8')] gold=[(None, 'Item 8')]`

### System B (hybrid + rerank)

Model: `gpt-5.4-2026-03-05`. Hops: 1. Chunks retrieved: 5, cited: 2.

**Generated answer**

> Apple’s ending accrued warranty and related costs were $4,780 in 2015 [2] and $3,692 in 2018 [3].
>
> Percentage decrease = \(\frac{4,780 - 3,692}{4,780} \times 100 \approx 22.8\%\)
>
> So, the ending accrued warranty and related costs decreased by approximately **22.8%** from fiscal 2015 to fiscal 2018. [2][3]

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `AAPL_FY2018_2018-09-29:124` | Item 7 › Overview and Highlights |  |  | The Company’s fiscal year is the 52- or 53-week period that ends on the last Saturday of September. The Company’s fiscal years 2018 and 2016 spanned 52 weeks each, whereas fiscal year 2017 included 53 weeks. A 14th week … |
| 2 | `AAPL_FY2015_2015-09-26:377` | Item 8 › Accrued Warranty and Indemnification | ✓ | #1, #2 | \| \| 2015 \| 2014 \| 2013 \| \|---\|---\|---\|---\| \| Beginning accrued warranty and related costs \| $4,159 \| $2,967 \| $1,638 \| \| Cost of warranty claims \| (4,401) \| (3,760) \| (3,703) \| \| Accruals for product warranty \| 5,022 \| 4… |
| 3 | `AAPL_FY2018_2018-09-29:343` | Item 8 › Accrued Warranty and Indemnification | ✓ | #1, #2 | \| \| 2018 \| 2017 \| 2016 \| \|---\|---\|---\|---\| \| Beginning accrued warranty and related costs \| $3,834 \| $3,702 \| $4,780 \| \| Cost of warranty claims \| (4,115) \| (4,322) \| (4,663) \| \| Accruals for product warranty \| 3,973 \| 4… |
| 4 | `AAPL_FY2018_2018-09-29:152` | Item 7 › Gross Margin |  |  | Gross margin increased in 2018 compared to 2017 due primarily to a favorable shift in mix of iPhones with higher average selling prices and higher Services net sales, partially offset by higher product cost structures. G… |
| 5 | `AAPL_FY2018_2018-09-29:159` | Item 7 › Other Income/(Expense), Net |  |  | The year-over-year decrease in other income/(expense), net during 2018 was due primarily to higher interest expense on debt and the impact of foreign exchange–related items, partially offset by higher interest income. Th… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#2 `AAPL_FY2015_2015-09-26:377`** (cited, gold #1, gold #2)

````text
Item 8. Financial Statements and Supplementary Data > Accrued Warranty and Indemnification (table)
|  | 2015 | 2014 | 2013 |
|---|---|---|---|
| Beginning accrued warranty and related costs | $4,159 | $2,967 | $1,638 |
| Cost of warranty claims | (4,401) | (3,760) | (3,703) |
| Accruals for product warranty | 5,022 | 4,952 | 5,032 |
| Ending accrued warranty and related costs | $4,780 | $4,159 | $2,967 |
````

**#3 `AAPL_FY2018_2018-09-29:343`** (cited, gold #1, gold #2)

````text
Item 8. Financial Statements and Supplementary Data > Accrued Warranty and Indemnification (table)
|  | 2018 | 2017 | 2016 |
|---|---|---|---|
| Beginning accrued warranty and related costs | $3,834 | $3,702 | $4,780 |
| Cost of warranty claims | (4,115) | (4,322) | (4,663) |
| Accruals for product warranty | 3,973 | 4,454 | 3,585 |
| Ending accrued warranty and related costs | $3,692 | $3,834 | $3,702 |
````

</details>

RQ2 citation match (section level): `cited=[('AAPL', 'Item 8')] gold=[(None, 'Item 8')]`

### System C v1 (adaptive multi-hop)

Model: `gpt-5.4`. Hops: 1. Chunks retrieved: 6, cited: 2.

**Generated answer**

> Apple Inc.'s ending accrued warranty and related costs decreased from $4,780 in fiscal year 2015 to $3,692 in fiscal year 2018, a decrease of approximately 22.8% [AAPL FY2015, Item 8, AAPL_FY2015_2015-09-26:377] [AAPL FY2018, Item 8, AAPL_FY2018_2018-09-29:343].

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `AAPL_FY2015_2015-09-26:377` | Item 8 › Accrued Warranty and Indemnification | ✓ | #1, #2 | \| \| 2015 \| 2014 \| 2013 \| \|---\|---\|---\|---\| \| Beginning accrued warranty and related costs \| $4,159 \| $2,967 \| $1,638 \| \| Cost of warranty claims \| (4,401) \| (3,760) \| (3,703) \| \| Accruals for product warranty \| 5,022 \| 4… |
| 2 | `AAPL_FY2015_2015-09-26:376` | Item 8 › Accrued Warranty and Indemnification |  |  | The following table shows changes in the Company’s accrued warranties and related costs for 2015, 2014 and 2013 (in millions): |
| 3 | `AAPL_FY2018_2018-09-29:343` | Item 8 › Accrued Warranty and Indemnification | ✓ | #1, #2 | \| \| 2018 \| 2017 \| 2016 \| \|---\|---\|---\|---\| \| Beginning accrued warranty and related costs \| $3,834 \| $3,702 \| $4,780 \| \| Cost of warranty claims \| (4,115) \| (4,322) \| (4,663) \| \| Accruals for product warranty \| 3,973 \| 4… |
| 4 | `AAPL_FY2015_2015-09-26:263` | Item 8 › Warranty Costs |  |  | The Company generally provides for the estimated cost of hardware and software warranties at the time the related revenue is recognized. The Company assesses the adequacy of its accrued warranty liabilities and adjusts t… |
| 5 | `AAPL_FY2018_2018-09-29:342` | Item 8 › Accrued Warranty and Indemnification |  |  | The following table shows changes in the Company’s accrued warranties and related costs for 2018, 2017 and 2016 (in millions): |
| 6 | `AAPL_FY2015_2015-09-26:380` | Item 8 › Accrued Warranty and Indemnification |  |  | The Company has entered into indemnification agreements with its directors and executive officers. Under these agreements, the Company has agreed to indemnify such individuals to the fullest extent permitted by law again… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#1 `AAPL_FY2015_2015-09-26:377`** (cited, gold #1, gold #2)

````text
Item 8. Financial Statements and Supplementary Data > Accrued Warranty and Indemnification (table)
|  | 2015 | 2014 | 2013 |
|---|---|---|---|
| Beginning accrued warranty and related costs | $4,159 | $2,967 | $1,638 |
| Cost of warranty claims | (4,401) | (3,760) | (3,703) |
| Accruals for product warranty | 5,022 | 4,952 | 5,032 |
| Ending accrued warranty and related costs | $4,780 | $4,159 | $2,967 |
````

**#3 `AAPL_FY2018_2018-09-29:343`** (cited, gold #1, gold #2)

````text
Item 8. Financial Statements and Supplementary Data > Accrued Warranty and Indemnification (table)
|  | 2018 | 2017 | 2016 |
|---|---|---|---|
| Beginning accrued warranty and related costs | $3,834 | $3,702 | $4,780 |
| Cost of warranty claims | (4,115) | (4,322) | (4,663) |
| Accruals for product warranty | 3,973 | 4,454 | 3,585 |
| Ending accrued warranty and related costs | $3,692 | $3,834 | $3,702 |
````

</details>

RQ2 citation match (section level): `cited=[('AAPL', 'Item 8')] gold=[(None, 'Item 8')]`

**System C guardrail** (judge `gpt-5.4`): numerical claims 3, verified 3, ungrounded 0, uncited 0, derived 1; sentence verdicts: supported 0, partial 0, unsupported 0, unchecked 0.


<details><summary>Guardrail sentence verdicts</summary>

| sentence | verdict | judge reason |
|---|---|---|
| Apple Inc.'s ending accrued warranty and related costs decreased from $4,780 in fiscal year 2015 to $3,692 in fiscal year 2018, a decrease of approximately 22.8% [AAPL FY2015, Item 8, AAPL_FY2015_2015-09-26:377] [AAPL FY2018, Item 8, AAPL_FY2018_2018-09-29:343]. | None |  |

</details>

### System C v2 (agentic multi-hop + XBRL)

Model: `gpt-5.4`. Hops: 1. Chunks retrieved: 6, cited: 2.

**Generated answer**

> Apple Inc.'s ending accrued warranty and related costs decreased from $4,780 million in fiscal year 2015 to $3,692 million in fiscal year 2018, a decrease of approximately 22.8% [AAPL FY2015, Item 8, AAPL_FY2015_2015-09-26:377] [AAPL FY2018, Item 8, AAPL_FY2018_2018-09-29:343].

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `AAPL_FY2015_2015-09-26:377` | Item 8 › Accrued Warranty and Indemnification | ✓ | #1, #2 | \| \| 2015 \| 2014 \| 2013 \| \|---\|---\|---\|---\| \| Beginning accrued warranty and related costs \| $4,159 \| $2,967 \| $1,638 \| \| Cost of warranty claims \| (4,401) \| (3,760) \| (3,703) \| \| Accruals for product warranty \| 5,022 \| 4… |
| 2 | `AAPL_FY2015_2015-09-26:376` | Item 8 › Accrued Warranty and Indemnification |  |  | The following table shows changes in the Company’s accrued warranties and related costs for 2015, 2014 and 2013 (in millions): |
| 3 | `AAPL_FY2018_2018-09-29:343` | Item 8 › Accrued Warranty and Indemnification | ✓ | #1, #2 | \| \| 2018 \| 2017 \| 2016 \| \|---\|---\|---\|---\| \| Beginning accrued warranty and related costs \| $3,834 \| $3,702 \| $4,780 \| \| Cost of warranty claims \| (4,115) \| (4,322) \| (4,663) \| \| Accruals for product warranty \| 3,973 \| 4… |
| 4 | `AAPL_FY2018_2018-09-29:342` | Item 8 › Accrued Warranty and Indemnification |  |  | The following table shows changes in the Company’s accrued warranties and related costs for 2018, 2017 and 2016 (in millions): |
| 5 | `AAPL_FY2015_2015-09-26:214` | Item 7 › Critical Accounting Policies and Estimates |  |  | The Company accrues for the estimated cost of warranties at the time the related revenue is recognized based on historical and projected warranty claim rates, historical and projected cost-per-claim and knowledge of spec… |
| 6 | `AAPL_FY2015_2015-09-26:263` | Item 8 › Warranty Costs |  |  | The Company generally provides for the estimated cost of hardware and software warranties at the time the related revenue is recognized. The Company assesses the adequacy of its accrued warranty liabilities and adjusts t… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#1 `AAPL_FY2015_2015-09-26:377`** (cited, gold #1, gold #2)

````text
Item 8. Financial Statements and Supplementary Data > Accrued Warranty and Indemnification (table)
|  | 2015 | 2014 | 2013 |
|---|---|---|---|
| Beginning accrued warranty and related costs | $4,159 | $2,967 | $1,638 |
| Cost of warranty claims | (4,401) | (3,760) | (3,703) |
| Accruals for product warranty | 5,022 | 4,952 | 5,032 |
| Ending accrued warranty and related costs | $4,780 | $4,159 | $2,967 |
````

**#3 `AAPL_FY2018_2018-09-29:343`** (cited, gold #1, gold #2)

````text
Item 8. Financial Statements and Supplementary Data > Accrued Warranty and Indemnification (table)
|  | 2018 | 2017 | 2016 |
|---|---|---|---|
| Beginning accrued warranty and related costs | $3,834 | $3,702 | $4,780 |
| Cost of warranty claims | (4,115) | (4,322) | (4,663) |
| Accruals for product warranty | 3,973 | 4,454 | 3,585 |
| Ending accrued warranty and related costs | $3,692 | $3,834 | $3,702 |
````

</details>

RQ2 citation match (section level): `cited=[('AAPL', 'Item 8')] gold=[(None, 'Item 8')]`

**System C guardrail** (judge `gpt-5.4`): numerical claims 3, verified 3, ungrounded 0, uncited 0, derived 1; sentence verdicts: supported 0, partial 0, unsupported 0, unchecked 0.


<details><summary>Guardrail sentence verdicts</summary>

| sentence | verdict | judge reason |
|---|---|---|
| Apple Inc.'s ending accrued warranty and related costs decreased from $4,780 million in fiscal year 2015 to $3,692 million in fiscal year 2018, a decrease of approximately 22.8% [AAPL FY2015, Item 8, AAPL_FY2015_2015-09-26:377] [AAPL FY2018, Item 8, AAPL_FY2018_2018-09-29:343]. | None |  |

</details>
