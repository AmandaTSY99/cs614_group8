# gold-024: Multi-hop text (one filing)

[← all cases](../README.md) · company: NVIDIA CORP (NVDA) · fiscal year: 2015 · recipe `text` · hop `multi` · answer type `qualitative` · scope `single_doc` · RQ2 category `cross_section_multihop`

## Gold QA

**Question**

> For NVIDIA's fiscal year 2015, what were the prior employers of Colette M. Kress and Ajay K. Puri immediately before they joined the company, and what specific roles did they hold at those companies?

**Gold answer**

> Colette M. Kress previously served as Senior Vice President and Chief Financial Officer of the Business Technology and Operations Finance organization at Cisco Systems, Inc., and Ajay K. Puri held positions in sales, marketing, and general management at Sun Microsystems, Inc. before joining NVIDIA.

**Key points** (RQ3 keypoint_recall targets)

1. Colette M. Kress was previously at Cisco Systems, Inc.
2. Kress served as Senior Vice President and CFO of the Business Technology and Operations Finance organization at Cisco
3. Ajay K. Puri was previously at Sun Microsystems, Inc.
4. Puri held positions in sales, marketing, and general management at Sun Microsystems

**Gold evidence**

1. `NVDA_FY2015_2015-01-25` · ITEM 1. BUSINESS › Table of Contents · text

   > Prior to NVIDIA, Ms. Kress most recently served as Senior Vice President and Chief Financial Officer of the Business Technology and Operations Finance organization at Cisco Systems, Inc., a networking equipment company, since 2010.

2. `NVDA_FY2015_2015-01-25` · ITEM 1. BUSINESS › Table of Contents · text

   > Prior to NVIDIA, he held positions in sales, marketing, and general management over a 22-year career at Sun Microsystems, Inc., a computing systems company.

## Scorecard

| Metric | A (vanilla dense) | B (hybrid + rerank) | C v1 (adaptive multi-hop) | C v2 (agentic multi-hop + XBRL) |
|---|---|---|---|---|
| **Retrieval (RQ1)** | | | | |
| chunks retrieved | 10 | 5 | 11 | 13 |
| recall@5 | 1.00 | 1.00 | 0.50 | 0.50 |
| recall@all | 1.00 | 1.00 | 1.00 | 1.00 |
| complete@all | 1 | 1 | 1 | 1 |
| average precision (lexical) | 1.00 | 1.00 | 0.27 | 0.26 |
| gold evidence first rank | #1: 1, #2: 2 | #1: 1, #2: 2 | #1: 3, #2: 10 | #1: 3, #2: 11 |
| **Answer (RQ3 string match)** | | | | |
| numeric_correct | – | – | – | – |
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
| tokens | 2318 | 1222 | 23929 | 25511 |
| cost (USD) | 0.0004 | 0.0002 | 0.0820 | 0.0867 |
| latency (s) | 2.7 | 14.9 | 39.9 | 31.6 |

Definitions: [README › Metrics](../README.md#metrics). `–` = not applicable (e.g. no gold number, no citations, no guardrail).

## System outputs

### System A (vanilla dense)

Model: `gpt-5.4-2026-03-05`. Hops: 1. Chunks retrieved: 10, cited: 2.

**Generated answer**

> Immediately before joining NVIDIA:
>
> - **Colette M. Kress** was at **Cisco Systems, Inc.**, where she served as **Senior Vice President and Chief Financial Officer of the Business Technology and Operations Finance organization** [1].
> - **Ajay K. Puri** was at **Sun Microsystems, Inc.**, where he **held positions in sales, marketing, and general management** over a 22-year career [2].
>
> The context gives a specific title for Kress, but for Puri it does **not** provide a single immediate pre-NVIDIA title beyond those functional roles at Sun Microsystems [1][2].

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `NVDA_FY2015_2015-01-25:49` | Item 1 › Table of Contents | ✓ | #1 | Colette M. Kress joined NVIDIA in September 2013 as Executive Vice President and Chief Financial Officer. Prior to NVIDIA, Ms. Kress most recently served as Senior Vice President and Chief Financial Officer of the Busine… |
| 2 | `NVDA_FY2015_2015-01-25:50` | Item 1 › Table of Contents | ✓ | #2 | Ajay K. Puri joined NVIDIA in December 2005 as Senior Vice President, Worldwide Sales and became Executive Vice President, Worldwide Sales (subsequently renamed to Worldwide Field Operations) in January 2009. Prior to NV… |
| 3 | `NVDA_FY2015_2015-01-25:48` | Item 1 › Executive Officers of the Registrant |  |  | Jen-Hsun Huang co-founded NVIDIA in April 1993 and has served as its President, Chief Executive Officer and a member of the Board of Directors since its inception. From 1985 to 1993, Mr. Huang was employed at LSI Logic C… |
| 4 | `NVDA_FY2015_2015-01-25:234` | Item 15 › Note 1 - Organization and Summary of Significant Accounting Policies |  |  | Our Company NVIDIA is dedicated to advancing visual computing. We enable individuals to interact with digital ideas, data and entertainment with an ease and efficiency unmatched by any other communication medium. Our two… |
| 5 | `NVDA_FY2015_2015-01-25:47` | Item 1 › Executive Officers of the Registrant |  |  | \| Name \| Age \| Position \| \|---\|---\|---\| \| Jen-Hsun Huang \| 52 \| President, Chief Executive Officer and Director \| \| Colette M. Kress \| 47 \| Executive Vice President and Chief Financial Officer \| \| Ajay K. Puri \| 60 \| Exe… |
| 6 | `NVDA_FY2015_2015-01-25:115` | Item 7 › Our Company and Our Businesses |  |  | We also integrate our GPUs into tiny mobile chips called system-on-a-chip (SOC) processors, which power tablets, and automotive infotainment and safety systems. Our Tegra brand integrates an entire computer onto a single… |
| 7 | `NVDA_FY2015_2015-01-25:5` | Santa Clara, California 95050 |  |  | (408) 486-2000 |
| 8 | `NVDA_FY2015_2015-01-25:52` | Item 1 › Table of Contents |  |  | Debora Shoquist joined NVIDIA in September 2007 as Senior Vice President of Operations and became Executive Vice President of Operations in January 2009. From 2004 to 2007, Ms. Shoquist served as Executive Vice President… |
| 9 | `NVDA_FY2015_2015-01-25:18` | Item 1 › Our Company |  |  | NVIDIA GPUs are chosen by gamers to enjoy immersive, beautiful fantasy worlds. They are used by professional designers to create visual effects in movies and design products ranging from soft drink bottles to commercial … |
| 10 | `NVDA_FY2015_2015-01-25:410` | Item 15 › Table of Contents |  |  | \| Signature \| Title \| Date \| \|---\|---\|---\| \| /s/ JEN-HSUN HUANG \| President, Chief Executive Officer and Director (Principal Executive Officer) \| March 11, 2015 \| \| Jen-Hsun Huang \| \| \| \| /s/ COLETTE M. KRESS \| Executive… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#1 `NVDA_FY2015_2015-01-25:49`** (cited, gold #1)

````text
ITEM 1. BUSINESS > Table of Contents
Colette M. Kress joined NVIDIA in September 2013 as Executive Vice President and Chief Financial Officer. Prior to NVIDIA, Ms. Kress most recently served as Senior Vice President and Chief Financial Officer of the Business Technology and Operations Finance organization at Cisco Systems, Inc., a networking equipment company, since 2010. At Cisco, Ms. Kress was responsible for financial strategy, planning, reporting and business development for all business segments, engineering and operations. From 1997 to 2010 Ms. Kress held a variety of positions at Microsoft Corporation, a software company, including, beginning in 2006, Chief Financial Officer of the Server and Tools division, where Ms. Kress was responsible for financial strategy, planning, reporting and business development for the division. Prior to joining Microsoft, Ms. Kress spent eight years at Texas Instruments Incorporated, a semiconductor company, where she held a variety of finance positions. Ms. Kress holds a B.S. degree in Finance from University of Arizona and an M.B.A. degree from Southern Methodist University.
````

**#2 `NVDA_FY2015_2015-01-25:50`** (cited, gold #2)

````text
ITEM 1. BUSINESS > Table of Contents
Ajay K. Puri joined NVIDIA in December 2005 as Senior Vice President, Worldwide Sales and became Executive Vice President, Worldwide Sales (subsequently renamed to Worldwide Field Operations) in January 2009. Prior to NVIDIA, he held positions in sales, marketing, and general management over a 22-year career at Sun Microsystems, Inc., a computing systems company. Mr. Puri previously held marketing, management consulting, and product development positions at Hewlett-Packard Company, an information technology company, Booz Allen Hamilton Inc., a management and technology consulting company, and Texas Instruments. Mr. Puri holds a B.S.E.E. degree from the University of Minnesota, an M.S.E.E. degree from the California Institute of Technology and an M.B.A. degree from Harvard Business School.
````

</details>

RQ2 citation match (section level): `cited=[('NVDA', 'Item 1')] gold=[(None, 'Item 1')]`

### System B (hybrid + rerank)

Model: `gpt-5.4-2026-03-05`. Hops: 1. Chunks retrieved: 5, cited: 2.

**Generated answer**

> Before joining NVIDIA:
>
> - **Colette M. Kress** most recently worked at **Cisco Systems, Inc.** as **Senior Vice President and Chief Financial Officer of the Business Technology and Operations Finance organization** [1].
> - **Ajay K. Puri** worked at **Sun Microsystems, Inc.**, where he held **positions in sales, marketing, and general management** over a 22-year career [2].

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `NVDA_FY2015_2015-01-25:49` | Item 1 › Table of Contents | ✓ | #1 | Colette M. Kress joined NVIDIA in September 2013 as Executive Vice President and Chief Financial Officer. Prior to NVIDIA, Ms. Kress most recently served as Senior Vice President and Chief Financial Officer of the Busine… |
| 2 | `NVDA_FY2015_2015-01-25:50` | Item 1 › Table of Contents | ✓ | #2 | Ajay K. Puri joined NVIDIA in December 2005 as Senior Vice President, Worldwide Sales and became Executive Vice President, Worldwide Sales (subsequently renamed to Worldwide Field Operations) in January 2009. Prior to NV… |
| 3 | `NVDA_FY2015_2015-01-25:47` | Item 1 › Executive Officers of the Registrant |  |  | \| Name \| Age \| Position \| \|---\|---\|---\| \| Jen-Hsun Huang \| 52 \| President, Chief Executive Officer and Director \| \| Colette M. Kress \| 47 \| Executive Vice President and Chief Financial Officer \| \| Ajay K. Puri \| 60 \| Exe… |
| 4 | `NVDA_FY2015_2015-01-25:51` | Item 1 › Table of Contents |  |  | David M. Shannon serves as Executive Vice President, Chief Administrative Officer and Secretary of NVIDIA. In this role, he is responsible for NVIDIA’s legal and human resources functions, as well as intellectual propert… |
| 5 | `NVDA_FY2015_2015-01-25:118` | Item 7 › Table of Contents |  |  | We announced that NVIDIA GRID technology will be available on the VMware Horizon DaaS Platform to deliver 3D graphics on virtualized desktops and applications delivered through the cloud, partnered with VMware on a custo… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#1 `NVDA_FY2015_2015-01-25:49`** (cited, gold #1)

````text
ITEM 1. BUSINESS > Table of Contents
Colette M. Kress joined NVIDIA in September 2013 as Executive Vice President and Chief Financial Officer. Prior to NVIDIA, Ms. Kress most recently served as Senior Vice President and Chief Financial Officer of the Business Technology and Operations Finance organization at Cisco Systems, Inc., a networking equipment company, since 2010. At Cisco, Ms. Kress was responsible for financial strategy, planning, reporting and business development for all business segments, engineering and operations. From 1997 to 2010 Ms. Kress held a variety of positions at Microsoft Corporation, a software company, including, beginning in 2006, Chief Financial Officer of the Server and Tools division, where Ms. Kress was responsible for financial strategy, planning, reporting and business development for the division. Prior to joining Microsoft, Ms. Kress spent eight years at Texas Instruments Incorporated, a semiconductor company, where she held a variety of finance positions. Ms. Kress holds a B.S. degree in Finance from University of Arizona and an M.B.A. degree from Southern Methodist University.
````

**#2 `NVDA_FY2015_2015-01-25:50`** (cited, gold #2)

````text
ITEM 1. BUSINESS > Table of Contents
Ajay K. Puri joined NVIDIA in December 2005 as Senior Vice President, Worldwide Sales and became Executive Vice President, Worldwide Sales (subsequently renamed to Worldwide Field Operations) in January 2009. Prior to NVIDIA, he held positions in sales, marketing, and general management over a 22-year career at Sun Microsystems, Inc., a computing systems company. Mr. Puri previously held marketing, management consulting, and product development positions at Hewlett-Packard Company, an information technology company, Booz Allen Hamilton Inc., a management and technology consulting company, and Texas Instruments. Mr. Puri holds a B.S.E.E. degree from the University of Minnesota, an M.S.E.E. degree from the California Institute of Technology and an M.B.A. degree from Harvard Business School.
````

</details>

RQ2 citation match (section level): `cited=[('NVDA', 'Item 1')] gold=[(None, 'Item 1')]`

### System C v1 (adaptive multi-hop)

Model: `gpt-5.4`. Hops: 3. Chunks retrieved: 11, cited: 2.

**Generated answer**

> Immediately before joining NVIDIA, Colette M. Kress most recently served at Cisco Systems, Inc. as Senior Vice President and Chief Financial Officer of the Business Technology and Operations Finance organization. [NVDA FY2015, Item 1, NVDA_FY2015_2015-01-25:49]
>
> Immediately before joining NVIDIA, Ajay K. Puri was at Sun Microsystems, Inc., where he held positions in sales, marketing, and general management over a 22-year career. [NVDA FY2015, Item 1, NVDA_FY2015_2015-01-25:50]
>
> > [Guardrail Audit Warning]: Manual verification required; 2 sentence(s) are not supported by their cited chunks.

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `NVDA_FY2015_2015-01-25:399` | Item 15 › Table of Contents |  |  | \| 10.17+ \| 2007 Equity Incentive Plan - Incentive Stock Option \| 8-K \| 0-23985 \| 10.21 \| 9/13/2010 \| \|---\|---\|---\|---\|---\|---\| \| 10.31+ \| Offer Letter between NVIDIA Corporation and Colette Kress, dated September 13, 201… |
| 2 | `NVDA_FY2015_2015-01-25:417` | Item 15 › Table of Contents |  |  | \| 10.16+ \| 2007 Equity Incentive Plan - Non Statutory Stock Option \| 8-K \| 0-23985 \| 10.2 \| 9/13/2010 \| \|---\|---\|---\|---\|---\|---\| \| 10.29+ \| Fiscal Year 2015 Variable Compensation Plan \| 8-K \| 0-23985 \| 10.1 \| 4/15/2014 … |
| 3 | `NVDA_FY2015_2015-01-25:49` | Item 1 › Table of Contents | ✓ | #1 | Colette M. Kress joined NVIDIA in September 2013 as Executive Vice President and Chief Financial Officer. Prior to NVIDIA, Ms. Kress most recently served as Senior Vice President and Chief Financial Officer of the Busine… |
| 4 | `NVDA_FY2015_2015-01-25:410` | Item 15 › Table of Contents |  |  | \| Signature \| Title \| Date \| \|---\|---\|---\| \| /s/ JEN-HSUN HUANG \| President, Chief Executive Officer and Director (Principal Executive Officer) \| March 11, 2015 \| \| Jen-Hsun Huang \| \| \| \| /s/ COLETTE M. KRESS \| Executive… |
| 5 | `NVDA_FY2015_2015-01-25:47` | Item 1 › Executive Officers of the Registrant |  |  | \| Name \| Age \| Position \| \|---\|---\|---\| \| Jen-Hsun Huang \| 52 \| President, Chief Executive Officer and Director \| \| Colette M. Kress \| 47 \| Executive Vice President and Chief Financial Officer \| \| Ajay K. Puri \| 60 \| Exe… |
| 6 | `NVDA_FY2015_2015-01-25:408` | Item 15 › POWER OF ATTORNEY |  |  | KNOW ALL PERSONS BY THESE PRESENTS, that each person whose signature appears below constitutes and appoints Jen-Hsun Huang and Colette M. Kress, and each or any one of them, his true and lawful attorney-in-fact and agent… |
| 7 | `NVDA_FY2015_2015-01-25:48` | Item 1 › Executive Officers of the Registrant |  |  | Jen-Hsun Huang co-founded NVIDIA in April 1993 and has served as its President, Chief Executive Officer and a member of the Board of Directors since its inception. From 1985 to 1993, Mr. Huang was employed at LSI Logic C… |
| 8 | `NVDA_FY2015_2015-01-25:13` | TABLE OF CONTENTS |  |  | \| \| \| Page \| \|---\|---\|---\| \| \| PART I \| \| \| Item 10. \| Directors, Executive Officers and Corporate Governance \| 43 \| \| Item 11. \| Executive Compensation \| 43 \| \| Item 12. \| Security Ownership of Certain Beneficial Owners… |
| 9 | `NVDA_FY2015_2015-01-25:46` | Item 1 › Executive Officers of the Registrant |  |  | The following sets forth certain information regarding our executive officers, their ages and positions as of March 6, 2015: |
| 10 | `NVDA_FY2015_2015-01-25:50` | Item 1 › Table of Contents | ✓ | #2 | Ajay K. Puri joined NVIDIA in December 2005 as Senior Vice President, Worldwide Sales and became Executive Vice President, Worldwide Sales (subsequently renamed to Worldwide Field Operations) in January 2009. Prior to NV… |
| 11 | `NVDA_FY2015_2015-01-25:51` | Item 1 › Table of Contents |  |  | David M. Shannon serves as Executive Vice President, Chief Administrative Officer and Secretary of NVIDIA. In this role, he is responsible for NVIDIA’s legal and human resources functions, as well as intellectual propert… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#3 `NVDA_FY2015_2015-01-25:49`** (cited, gold #1)

````text
ITEM 1. BUSINESS > Table of Contents
Colette M. Kress joined NVIDIA in September 2013 as Executive Vice President and Chief Financial Officer. Prior to NVIDIA, Ms. Kress most recently served as Senior Vice President and Chief Financial Officer of the Business Technology and Operations Finance organization at Cisco Systems, Inc., a networking equipment company, since 2010. At Cisco, Ms. Kress was responsible for financial strategy, planning, reporting and business development for all business segments, engineering and operations. From 1997 to 2010 Ms. Kress held a variety of positions at Microsoft Corporation, a software company, including, beginning in 2006, Chief Financial Officer of the Server and Tools division, where Ms. Kress was responsible for financial strategy, planning, reporting and business development for the division. Prior to joining Microsoft, Ms. Kress spent eight years at Texas Instruments Incorporated, a semiconductor company, where she held a variety of finance positions. Ms. Kress holds a B.S. degree in Finance from University of Arizona and an M.B.A. degree from Southern Methodist University.
````

**#10 `NVDA_FY2015_2015-01-25:50`** (cited, gold #2)

````text
ITEM 1. BUSINESS > Table of Contents
Ajay K. Puri joined NVIDIA in December 2005 as Senior Vice President, Worldwide Sales and became Executive Vice President, Worldwide Sales (subsequently renamed to Worldwide Field Operations) in January 2009. Prior to NVIDIA, he held positions in sales, marketing, and general management over a 22-year career at Sun Microsystems, Inc., a computing systems company. Mr. Puri previously held marketing, management consulting, and product development positions at Hewlett-Packard Company, an information technology company, Booz Allen Hamilton Inc., a management and technology consulting company, and Texas Instruments. Mr. Puri holds a B.S.E.E. degree from the University of Minnesota, an M.S.E.E. degree from the California Institute of Technology and an M.B.A. degree from Harvard Business School.
````

</details>

RQ2 citation match (section level): `cited=[('NVDA', 'Item 1')] gold=[(None, 'Item 1')]`

**System C guardrail** (judge `gpt-5.4`): numerical claims 0, verified 0, ungrounded 0, uncited 0, derived 0; sentence verdicts: supported 2, partial 2, unsupported 0, unchecked 0.


<details><summary>Guardrail sentence verdicts</summary>

| sentence | verdict | judge reason |
|---|---|---|
| Immediately before joining NVIDIA, Colette M. | partial | The evidence shows she most recently served at Cisco before NVIDIA, but the sentence is incomplete and does not state the role. |
| Kress most recently served at Cisco Systems, Inc. as Senior Vice President and Chief Financial Officer of the Business Technology and Operations Finance organization. [NVDA FY2015, Item 1, NVDA_FY2015_2015-01-25:49] | supported | The cited evidence states exactly that Kress most recently served at Cisco as Senior Vice President and CFO of the Business Technology and Operations Finance organization. |
| Immediately before joining NVIDIA, Ajay K. | partial | The evidence shows that prior to NVIDIA Puri had a 22-year career at Sun Microsystems, but the sentence is incomplete. |
| Puri was at Sun Microsystems, Inc., where he held positions in sales, marketing, and general management over a 22-year career. [NVDA FY2015, Item 1, NVDA_FY2015_2015-01-25:50] | supported | The cited evidence explicitly says Puri held sales, marketing, and general management positions over a 22-year career at Sun Microsystems. |

</details>

### System C v2 (agentic multi-hop + XBRL)

Model: `gpt-5.4`. Hops: 3. Chunks retrieved: 13, cited: 2.

**Generated answer**

> Immediately before joining NVIDIA, Colette M. Kress most recently served as Senior Vice President and Chief Financial Officer of the Business Technology and Operations Finance organization at Cisco Systems, Inc. [NVDA FY2015, Item 1, NVDA_FY2015_2015-01-25:49]
>
> Immediately before joining NVIDIA, Ajay K. Puri was at Sun Microsystems, Inc., where he held positions in sales, marketing, and general management over a 22-year career. [NVDA FY2015, Item 1, NVDA_FY2015_2015-01-25:50]
>
> The filing does not disclose a more specific final title for Mr. Puri at Sun Microsystems immediately before he joined NVIDIA. [NVDA FY2015, Item 1, NVDA_FY2015_2015-01-25:50]
>
> > [Guardrail Audit Warning]: Manual verification required; 2 sentence(s) are not supported by their cited chunks.

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `NVDA_FY2015_2015-01-25:399` | Item 15 › Table of Contents |  |  | \| 10.17+ \| 2007 Equity Incentive Plan - Incentive Stock Option \| 8-K \| 0-23985 \| 10.21 \| 9/13/2010 \| \|---\|---\|---\|---\|---\|---\| \| 10.31+ \| Offer Letter between NVIDIA Corporation and Colette Kress, dated September 13, 201… |
| 2 | `NVDA_FY2015_2015-01-25:417` | Item 15 › Table of Contents |  |  | \| 10.16+ \| 2007 Equity Incentive Plan - Non Statutory Stock Option \| 8-K \| 0-23985 \| 10.2 \| 9/13/2010 \| \|---\|---\|---\|---\|---\|---\| \| 10.29+ \| Fiscal Year 2015 Variable Compensation Plan \| 8-K \| 0-23985 \| 10.1 \| 4/15/2014 … |
| 3 | `NVDA_FY2015_2015-01-25:49` | Item 1 › Table of Contents | ✓ | #1 | Colette M. Kress joined NVIDIA in September 2013 as Executive Vice President and Chief Financial Officer. Prior to NVIDIA, Ms. Kress most recently served as Senior Vice President and Chief Financial Officer of the Busine… |
| 4 | `NVDA_FY2015_2015-01-25:410` | Item 15 › Table of Contents |  |  | \| Signature \| Title \| Date \| \|---\|---\|---\| \| /s/ JEN-HSUN HUANG \| President, Chief Executive Officer and Director (Principal Executive Officer) \| March 11, 2015 \| \| Jen-Hsun Huang \| \| \| \| /s/ COLETTE M. KRESS \| Executive… |
| 5 | `NVDA_FY2015_2015-01-25:47` | Item 1 › Executive Officers of the Registrant |  |  | \| Name \| Age \| Position \| \|---\|---\|---\| \| Jen-Hsun Huang \| 52 \| President, Chief Executive Officer and Director \| \| Colette M. Kress \| 47 \| Executive Vice President and Chief Financial Officer \| \| Ajay K. Puri \| 60 \| Exe… |
| 6 | `NVDA_FY2015_2015-01-25:408` | Item 15 › POWER OF ATTORNEY |  |  | KNOW ALL PERSONS BY THESE PRESENTS, that each person whose signature appears below constitutes and appoints Jen-Hsun Huang and Colette M. Kress, and each or any one of them, his true and lawful attorney-in-fact and agent… |
| 7 | `NVDA_FY2015_2015-01-25:48` | Item 1 › Executive Officers of the Registrant |  |  | Jen-Hsun Huang co-founded NVIDIA in April 1993 and has served as its President, Chief Executive Officer and a member of the Board of Directors since its inception. From 1985 to 1993, Mr. Huang was employed at LSI Logic C… |
| 8 | `NVDA_FY2015_2015-01-25:46` | Item 1 › Executive Officers of the Registrant |  |  | The following sets forth certain information regarding our executive officers, their ages and positions as of March 6, 2015: |
| 9 | `NVDA_FY2015_2015-01-25:13` | TABLE OF CONTENTS |  |  | \| \| \| Page \| \|---\|---\|---\| \| \| PART I \| \| \| Item 10. \| Directors, Executive Officers and Corporate Governance \| 43 \| \| Item 11. \| Executive Compensation \| 43 \| \| Item 12. \| Security Ownership of Certain Beneficial Owners… |
| 10 | `NVDA_FY2015_2015-01-25:197` | Item 10 › Identification of Executive Officers |  |  | Reference is made to the information regarding executive officers appearing under the heading “Executive Officers of the Registrant” in Part I of this Annual Report on Form 10-K, which information is hereby incorporated … |
| 11 | `NVDA_FY2015_2015-01-25:50` | Item 1 › Table of Contents | ✓ | #2 | Ajay K. Puri joined NVIDIA in December 2005 as Senior Vice President, Worldwide Sales and became Executive Vice President, Worldwide Sales (subsequently renamed to Worldwide Field Operations) in January 2009. Prior to NV… |
| 12 | `NVDA_FY2015_2015-01-25:52` | Item 1 › Table of Contents |  |  | Debora Shoquist joined NVIDIA in September 2007 as Senior Vice President of Operations and became Executive Vice President of Operations in January 2009. From 2004 to 2007, Ms. Shoquist served as Executive Vice President… |
| 13 | `NVDA_FY2015_2015-01-25:51` | Item 1 › Table of Contents |  |  | David M. Shannon serves as Executive Vice President, Chief Administrative Officer and Secretary of NVIDIA. In this role, he is responsible for NVIDIA’s legal and human resources functions, as well as intellectual propert… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#3 `NVDA_FY2015_2015-01-25:49`** (cited, gold #1)

````text
ITEM 1. BUSINESS > Table of Contents
Colette M. Kress joined NVIDIA in September 2013 as Executive Vice President and Chief Financial Officer. Prior to NVIDIA, Ms. Kress most recently served as Senior Vice President and Chief Financial Officer of the Business Technology and Operations Finance organization at Cisco Systems, Inc., a networking equipment company, since 2010. At Cisco, Ms. Kress was responsible for financial strategy, planning, reporting and business development for all business segments, engineering and operations. From 1997 to 2010 Ms. Kress held a variety of positions at Microsoft Corporation, a software company, including, beginning in 2006, Chief Financial Officer of the Server and Tools division, where Ms. Kress was responsible for financial strategy, planning, reporting and business development for the division. Prior to joining Microsoft, Ms. Kress spent eight years at Texas Instruments Incorporated, a semiconductor company, where she held a variety of finance positions. Ms. Kress holds a B.S. degree in Finance from University of Arizona and an M.B.A. degree from Southern Methodist University.
````

**#11 `NVDA_FY2015_2015-01-25:50`** (cited, gold #2)

````text
ITEM 1. BUSINESS > Table of Contents
Ajay K. Puri joined NVIDIA in December 2005 as Senior Vice President, Worldwide Sales and became Executive Vice President, Worldwide Sales (subsequently renamed to Worldwide Field Operations) in January 2009. Prior to NVIDIA, he held positions in sales, marketing, and general management over a 22-year career at Sun Microsystems, Inc., a computing systems company. Mr. Puri previously held marketing, management consulting, and product development positions at Hewlett-Packard Company, an information technology company, Booz Allen Hamilton Inc., a management and technology consulting company, and Texas Instruments. Mr. Puri holds a B.S.E.E. degree from the University of Minnesota, an M.S.E.E. degree from the California Institute of Technology and an M.B.A. degree from Harvard Business School.
````

</details>

RQ2 citation match (section level): `cited=[('NVDA', 'Item 1')] gold=[(None, 'Item 1')]`

**System C guardrail** (judge `gpt-5.4`): numerical claims 0, verified 0, ungrounded 0, uncited 0, derived 0; sentence verdicts: supported 4, partial 2, unsupported 0, unchecked 0.


<details><summary>Guardrail sentence verdicts</summary>

| sentence | verdict | judge reason |
|---|---|---|
| Immediately before joining NVIDIA, Colette M. | partial | The evidence identifies Colette Kress's role immediately before NVIDIA but the sentence is incomplete and makes no full claim. |
| Kress most recently served as Senior Vice President and Chief Financial Officer of the Business Technology and Operations Finance organization at Cisco Systems, Inc. [NVDA FY2015, Item 1, NVDA_FY2015_2015-01-25:49] | supported | The cited passage states exactly that Ms. Kress most recently served in that Cisco SVP/CFO role. |
| Immediately before joining NVIDIA, Ajay K. | partial | The evidence identifies Ajay Puri's employer before NVIDIA, but the sentence is incomplete and makes no full claim. |
| Puri was at Sun Microsystems, Inc., where he held positions in sales, marketing, and general management over a 22-year career. [NVDA FY2015, Item 1, NVDA_FY2015_2015-01-25:50] | supported | The cited passage states he held sales, marketing, and general management positions over a 22-year career at Sun Microsystems. |
| The filing does not disclose a more specific final title for Mr. | supported | The retrieved evidence does not disclose a more specific final title for Mr. Puri at Sun Microsystems before joining NVIDIA. |
| Puri at Sun Microsystems immediately before he joined NVIDIA. [NVDA FY2015, Item 1, NVDA_FY2015_2015-01-25:50] | supported | The cited passage gives only that he held various positions at Sun and does not provide a more specific immediately prior title. |

</details>
