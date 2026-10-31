# gold-041: Single-hop table

[← all cases](../README.md) · company: JPMORGAN CHASE & CO (JPM) · fiscal year: 2023 · recipe `table` · hop `single` · answer type `numeric` · scope `single_doc` · RQ2 category `quantitative_tabular`

## Gold QA

**Question**

> As of December 31, 2023, by how many percentage points was the share of White members on JPMorgan Chase & Co.'s Board of Directors higher than the share of White employees in its total employee population?

**Gold answer**

> 39 percentage points

**Program**: `subtract(82, 43)` → `39.0`

**Gold numbers** (RQ2 numeric_accuracy targets): 39 percentage points

**Gold evidence**

1. `JPM_FY2023_2023-12-31` · Item 1. Business. › Human capital · table

   > | White | 43% | 75% | 88% | 82% |  |

## Scorecard

| Metric | A (vanilla dense) | B (hybrid + rerank) | C v1 (adaptive multi-hop) | C v2 (agentic multi-hop + XBRL) |
|---|---|---|---|---|
| **Retrieval (RQ1)** | | | | |
| chunks retrieved | 10 | 5 | 6 | 6 |
| recall@5 | 1.00 | 1.00 | 1.00 | 1.00 |
| recall@all | 1.00 | 1.00 | 1.00 | 1.00 |
| complete@all | 1 | 1 | 1 | 1 |
| average precision (lexical) | 1.00 | 1.00 | 1.00 | 1.00 |
| gold evidence first rank | #1: 1 | #1: 1 | #1: 1 | #1: 1 |
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
| tokens | 2227 | 1331 | 4294 | 4294 |
| cost (USD) | 0.0003 | 0.0002 | 0.0156 | 0.0156 |
| latency (s) | 1.8 | 6.5 | 7.4 | 7.3 |

Definitions: [README › Metrics](../README.md#metrics). `–` = not applicable (e.g. no gold number, no citations, no guardrail).

## System outputs

### System A (vanilla dense)

Model: `gpt-5.4-2026-03-05`. Hops: 1. Chunks retrieved: 10, cited: 1.

**Generated answer**

> The share of White members on the Board of Directors was 82%, versus 43% for total employees, a difference of 39 percentage points [1].

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `JPM_FY2023_2023-12-31:18` | Item 1 › Human capital | ✓ | #1 | \| December 31, 2023 \| Total employees \| Senior level employees(e) \| Operating Committee \| Board of Directors(f) \| \| \|---\|---\|---\|---\|---\|---\| \| Race/Ethnicity(a): \| \| \| \| \| \| \| White \| 43% \| 75% \| 88% \| 82% \| \| \| Hispani… |
| 2 | `JPM_FY2023_2023-12-31:19` | Item 1 › Human capital |  |  | (a)Based on EEO metrics. Presented as a percentage of the respective populations who self-identified race/ethnicity, which was 96% and 94% of the Firm’s total U.S.-based employees and U.S.-based senior level employees, r… |
| 3 | `JPM_FY2023_2023-12-31:16` | Item 1 › Human capital |  |  | \| Employee Breakdown by Region \| \| Employee Breakdown by LOB and Corporate \| \| \|---\|---\|---\|---\| \| Region \| Employees \| LOB \| Employees \| \| North America \| 186,751 \| CCB \| 141,640 \| \| Asia-Pacific \| 88,406 \| CIB \| 74,404… |
| 4 | `JPM_FY2023_2023-12-31:205` | Item 10 › Executive officers of the registrant |  |  | Unless otherwise noted, during the five fiscal years ended December 31, 2023, all of JPMorgan Chase’s above-named executive officers have continuously held senior-level positions with JPMorgan Chase. There are no family … |
| 5 | `JPM_FY2023_2023-12-31:15` | Item 1 › Human capital |  |  | JPMorgan Chase believes that its long-term growth and success depend on its ability to attract, develop and retain a high-performing and diverse workforce, with inclusion and accessibility as key components of the way th… |
| 6 | `JPM_FY2023_2023-12-31:17` | Item 1 › Human capital |  |  | Diversity, equity and inclusion The following table presents information based on voluntary self-identifications by the Firm’s employees and members of the Board of Directors, as of December 31, 2023. Information on race… |
| 7 | `JPM_FY2023_2023-12-31:203` | Item 10 › Executive officers of the registrant |  |  | \| \| Age \| \| \|---\|---\|---\| \| Name \| (at December 31, 2023) \| Positions and offices \| \| James Dimon \| 67 \| Chairman of the Board since December 2006 and Chief Executive Officer since December 2005. \| \| Ashley Bacon \| 54 \| … |
| 8 | `JPM_FY2023_2023-12-31:247` | Item 15 › Management’s discussion and analysis |  |  | JPMorgan Chase & Co. (NYSE: JPM), a financial holding company incorporated under Delaware law in 1968, is a leading financial services firm based in the United States of America (“U.S.”), with operations worldwide. JPMor… |
| 9 | `JPM_FY2023_2023-12-31:206` | Item 11 |  |  | Refer to Item 10. |
| 10 | `JPM_FY2023_2023-12-31:1493` | Item 15 › Note 22 – Common stock |  |  | As of December 31, 2023, approximately 61.6 million shares of common stock were reserved for issuance under various employee incentive, compensation, option and stock purchase plans, and directors’ compensation plans. 28… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#1 `JPM_FY2023_2023-12-31:18`** (cited, gold #1)

````text
Item 1. Business. > Human capital (table)
| December 31, 2023 | Total employees | Senior level employees(e) | Operating Committee | Board of Directors(f) |  |
|---|---|---|---|---|---|
| Race/Ethnicity(a): |  |  |  |  |  |
| White | 43% | 75% | 88% | 82% |  |
| Hispanic | 21% | 6% | 6% | — |  |
| Asian | 19% | 13% | 6% | — |  |
| Black | 14% | 5% | — | 18% |  |
| Other(b) | 3% | 1% | — | — |  |
| Gender(c): |  |  |  |  |  |
| Men | 51% | 72% | 59% | 55% |  |
| Women | 49% | 28% | 41% | 45% |  |
| LGBTQ+(d) | 4% | 3% | 6% | — |  |
| Military veterans(d) | 3% | 2% | — | 9% |  |
| People with disabilities(d) | 4% | 3% | — | — | (g) |
````

</details>

RQ2 citation match (section level): `cited=[('JPM', 'Item 1')] gold=[(None, 'Item 1')]`

### System B (hybrid + rerank)

Model: `gpt-5.4-2026-03-05`. Hops: 1. Chunks retrieved: 5, cited: 1.

**Generated answer**

> The share was higher by 39 percentage points: 82% on the Board of Directors versus 43% in total employees [1].

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `JPM_FY2023_2023-12-31:18` | Item 1 › Human capital | ✓ | #1 | \| December 31, 2023 \| Total employees \| Senior level employees(e) \| Operating Committee \| Board of Directors(f) \| \| \|---\|---\|---\|---\|---\|---\| \| Race/Ethnicity(a): \| \| \| \| \| \| \| White \| 43% \| 75% \| 88% \| 82% \| \| \| Hispani… |
| 2 | `JPM_FY2023_2023-12-31:15` | Item 1 › Human capital |  |  | JPMorgan Chase believes that its long-term growth and success depend on its ability to attract, develop and retain a high-performing and diverse workforce, with inclusion and accessibility as key components of the way th… |
| 3 | `JPM_FY2023_2023-12-31:247` | Item 15 › Management’s discussion and analysis |  |  | JPMorgan Chase & Co. (NYSE: JPM), a financial holding company incorporated under Delaware law in 1968, is a leading financial services firm based in the United States of America (“U.S.”), with operations worldwide. JPMor… |
| 4 | `JPM_FY2023_2023-12-31:354` | Item 15 › 2023 compared with 2022 |  |  | \| Selected metrics \| \| \| \| \| \| \|---\|---\|---\|---\|---\|---\| \| As of or for the year ended December 31, \| \| \| \| \| \| \| (in billions, except ratios and where otherwise noted) \| 2023 \| \| 2022 \| 2021 \| \| \| Business Metrics \| \| \|… |
| 5 | `JPM_FY2023_2023-12-31:1143` | Item 15 › employee benefit plans |  |  | The weighted-average discount rate used to value the benefit obligations as of December 31, 2023 and 2022, was 5.16% and 5.14%, respectively. |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#1 `JPM_FY2023_2023-12-31:18`** (cited, gold #1)

````text
Item 1. Business. > Human capital (table)
| December 31, 2023 | Total employees | Senior level employees(e) | Operating Committee | Board of Directors(f) |  |
|---|---|---|---|---|---|
| Race/Ethnicity(a): |  |  |  |  |  |
| White | 43% | 75% | 88% | 82% |  |
| Hispanic | 21% | 6% | 6% | — |  |
| Asian | 19% | 13% | 6% | — |  |
| Black | 14% | 5% | — | 18% |  |
| Other(b) | 3% | 1% | — | — |  |
| Gender(c): |  |  |  |  |  |
| Men | 51% | 72% | 59% | 55% |  |
| Women | 49% | 28% | 41% | 45% |  |
| LGBTQ+(d) | 4% | 3% | 6% | — |  |
| Military veterans(d) | 3% | 2% | — | 9% |  |
| People with disabilities(d) | 4% | 3% | — | — | (g) |
````

</details>

RQ2 citation match (section level): `cited=[('JPM', 'Item 1')] gold=[(None, 'Item 1')]`

### System C v1 (adaptive multi-hop)

Model: `gpt-5.4`. Hops: 1. Chunks retrieved: 6, cited: 1.

**Generated answer**

> As of December 31, 2023, White individuals represented 82% of the Board of Directors and 43% of total employees, so the Board’s share was higher by 39 percentage points [JPM FY2023, Item 1, JPM_FY2023_2023-12-31:18].

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `JPM_FY2023_2023-12-31:18` | Item 1 › Human capital | ✓ | #1 | \| December 31, 2023 \| Total employees \| Senior level employees(e) \| Operating Committee \| Board of Directors(f) \| \| \|---\|---\|---\|---\|---\|---\| \| Race/Ethnicity(a): \| \| \| \| \| \| \| White \| 43% \| 75% \| 88% \| 82% \| \| \| Hispani… |
| 2 | `JPM_FY2023_2023-12-31:17` | Item 1 › Human capital |  |  | Diversity, equity and inclusion The following table presents information based on voluntary self-identifications by the Firm’s employees and members of the Board of Directors, as of December 31, 2023. Information on race… |
| 3 | `JPM_FY2023_2023-12-31:203` | Item 10 › Executive officers of the registrant |  |  | \| \| Age \| \| \|---\|---\|---\| \| Name \| (at December 31, 2023) \| Positions and offices \| \| James Dimon \| 67 \| Chairman of the Board since December 2006 and Chief Executive Officer since December 2005. \| \| Ashley Bacon \| 54 \| … |
| 4 | `JPM_FY2023_2023-12-31:19` | Item 1 › Human capital |  |  | (a)Based on EEO metrics. Presented as a percentage of the respective populations who self-identified race/ethnicity, which was 96% and 94% of the Firm’s total U.S.-based employees and U.S.-based senior level employees, r… |
| 5 | `JPM_FY2023_2023-12-31:1493` | Item 15 › Note 22 – Common stock |  |  | As of December 31, 2023, approximately 61.6 million shares of common stock were reserved for issuance under various employee incentive, compensation, option and stock purchase plans, and directors’ compensation plans. 28… |
| 6 | `JPM_FY2023_2023-12-31:265` | Item 15 › Recent events |  |  | •On January 16, 2024, JPMorgan Chase announced that Mark Weinberger, 62, had been elected to its Board of Directors, effective immediately. He will also serve as a member of the Board’s Audit Committee. Mr. Weinberger se… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#1 `JPM_FY2023_2023-12-31:18`** (cited, gold #1)

````text
Item 1. Business. > Human capital (table)
| December 31, 2023 | Total employees | Senior level employees(e) | Operating Committee | Board of Directors(f) |  |
|---|---|---|---|---|---|
| Race/Ethnicity(a): |  |  |  |  |  |
| White | 43% | 75% | 88% | 82% |  |
| Hispanic | 21% | 6% | 6% | — |  |
| Asian | 19% | 13% | 6% | — |  |
| Black | 14% | 5% | — | 18% |  |
| Other(b) | 3% | 1% | — | — |  |
| Gender(c): |  |  |  |  |  |
| Men | 51% | 72% | 59% | 55% |  |
| Women | 49% | 28% | 41% | 45% |  |
| LGBTQ+(d) | 4% | 3% | 6% | — |  |
| Military veterans(d) | 3% | 2% | — | 9% |  |
| People with disabilities(d) | 4% | 3% | — | — | (g) |
````

</details>

RQ2 citation match (section level): `cited=[('JPM', 'Item 1')] gold=[(None, 'Item 1')]`

**System C guardrail** (judge `gpt-5.4`): numerical claims 2, verified 2, ungrounded 0, uncited 0, derived 0; sentence verdicts: supported 0, partial 0, unsupported 0, unchecked 0.


<details><summary>Guardrail sentence verdicts</summary>

| sentence | verdict | judge reason |
|---|---|---|
| As of December 31, 2023, White individuals represented 82% of the Board of Directors and 43% of total employees, so the Board’s share was higher by 39 percentage points [JPM FY2023, Item 1, JPM_FY2023_2023-12-31:18]. | None |  |

</details>

### System C v2 (agentic multi-hop + XBRL)

Model: `gpt-5.4`. Hops: 1. Chunks retrieved: 6, cited: 1.

**Generated answer**

> As of December 31, 2023, White employees were 43% of JPMorgan Chase & Co.'s total employee population, while White members were 82% of its Board of Directors, so the Board’s White share was higher by 39 percentage points [JPM FY2023, Item 1, JPM_FY2023_2023-12-31:18].

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `JPM_FY2023_2023-12-31:18` | Item 1 › Human capital | ✓ | #1 | \| December 31, 2023 \| Total employees \| Senior level employees(e) \| Operating Committee \| Board of Directors(f) \| \| \|---\|---\|---\|---\|---\|---\| \| Race/Ethnicity(a): \| \| \| \| \| \| \| White \| 43% \| 75% \| 88% \| 82% \| \| \| Hispani… |
| 2 | `JPM_FY2023_2023-12-31:17` | Item 1 › Human capital |  |  | Diversity, equity and inclusion The following table presents information based on voluntary self-identifications by the Firm’s employees and members of the Board of Directors, as of December 31, 2023. Information on race… |
| 3 | `JPM_FY2023_2023-12-31:203` | Item 10 › Executive officers of the registrant |  |  | \| \| Age \| \| \|---\|---\|---\| \| Name \| (at December 31, 2023) \| Positions and offices \| \| James Dimon \| 67 \| Chairman of the Board since December 2006 and Chief Executive Officer since December 2005. \| \| Ashley Bacon \| 54 \| … |
| 4 | `JPM_FY2023_2023-12-31:19` | Item 1 › Human capital |  |  | (a)Based on EEO metrics. Presented as a percentage of the respective populations who self-identified race/ethnicity, which was 96% and 94% of the Firm’s total U.S.-based employees and U.S.-based senior level employees, r… |
| 5 | `JPM_FY2023_2023-12-31:1493` | Item 15 › Note 22 – Common stock |  |  | As of December 31, 2023, approximately 61.6 million shares of common stock were reserved for issuance under various employee incentive, compensation, option and stock purchase plans, and directors’ compensation plans. 28… |
| 6 | `JPM_FY2023_2023-12-31:265` | Item 15 › Recent events |  |  | •On January 16, 2024, JPMorgan Chase announced that Mark Weinberger, 62, had been elected to its Board of Directors, effective immediately. He will also serve as a member of the Board’s Audit Committee. Mr. Weinberger se… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#1 `JPM_FY2023_2023-12-31:18`** (cited, gold #1)

````text
Item 1. Business. > Human capital (table)
| December 31, 2023 | Total employees | Senior level employees(e) | Operating Committee | Board of Directors(f) |  |
|---|---|---|---|---|---|
| Race/Ethnicity(a): |  |  |  |  |  |
| White | 43% | 75% | 88% | 82% |  |
| Hispanic | 21% | 6% | 6% | — |  |
| Asian | 19% | 13% | 6% | — |  |
| Black | 14% | 5% | — | 18% |  |
| Other(b) | 3% | 1% | — | — |  |
| Gender(c): |  |  |  |  |  |
| Men | 51% | 72% | 59% | 55% |  |
| Women | 49% | 28% | 41% | 45% |  |
| LGBTQ+(d) | 4% | 3% | 6% | — |  |
| Military veterans(d) | 3% | 2% | — | 9% |  |
| People with disabilities(d) | 4% | 3% | — | — | (g) |
````

</details>

RQ2 citation match (section level): `cited=[('JPM', 'Item 1')] gold=[(None, 'Item 1')]`

**System C guardrail** (judge `gpt-5.4`): numerical claims 2, verified 2, ungrounded 0, uncited 0, derived 0; sentence verdicts: supported 0, partial 0, unsupported 0, unchecked 0.


<details><summary>Guardrail sentence verdicts</summary>

| sentence | verdict | judge reason |
|---|---|---|
| As of December 31, 2023, White employees were 43% of JPMorgan Chase & Co.'s total employee population, while White members were 82% of its Board of Directors, so the Board’s White share was higher by 39 percentage points [JPM FY2023, Item 1, JPM_FY2023_2023-12-31:18]. | None |  |

</details>
