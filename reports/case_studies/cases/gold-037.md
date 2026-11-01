# gold-037: Table + text (one filing)

[← all cases](../README.md) · company: NVIDIA CORP (NVDA) · fiscal year: 2018 · recipe `table_text` · hop `multi` · answer type `mixed` · scope `single_doc` · RQ2 category `cross_section_multihop`

## Gold QA

**Question**

> What was the absolute increase in NVIDIA's Tegra Processor revenue, in millions of dollars, from fiscal year 2016 to fiscal year 2018, and how does the company's business description explain the strategic importance of the Tegra brand within its broader hardware ecosystem?

**Gold answer**

> $975 million. NVIDIA says its Tegra brand integrates an entire computer onto a single chip and incorporates GPUs and multi-core CPUs to drive supercomputing for autonomous robots, drones and cars, as well as for consoles and mobile gaming and entertainment devices.

**Program**: `subtract(1534, 559)` → `975.0`

**Gold numbers** (RQ2 numeric_accuracy targets): $975 million

**Key points** (RQ3 keypoint_recall targets)

1. Tegra Processor revenue rose by $975 million, from $559 million in FY2016 to $1,534 million in FY2018.
2. Tegra integrates an entire computer onto a single chip.
3. Tegra incorporates GPUs and multi-core CPUs.
4. It targets autonomous robots, drones and cars, as well as consoles and mobile gaming devices.

**Gold evidence**

1. `NVDA_FY2018_2018-01-28` · ITEM 7. MANAGEMENT’S DISCUSSION AND ANALYSIS OF FINANCIAL CONDITION AND RESULTS OF OPERATIONS › Revenue by Reportable Segments · table

   > | Tegra Processor | 1,534 | 824 | 710 | 86% | 824 | 559 | 265 | 47% |

2. `NVDA_FY2018_2018-01-28` · ITEM 7. MANAGEMENT’S DISCUSSION AND ANALYSIS OF FINANCIAL CONDITION AND RESULTS OF OPERATIONS › Our Company and Our Businesses · text

   > Our Tegra brand integrates an entire computer onto a single chip, and incorporates GPUs and multi-core CPUs to drive supercomputing for autonomous robots, drones, and cars, as well as for consoles and mobile gaming and entertainment devices.

## Scorecard

| Metric | A (vanilla dense) | B (hybrid + rerank) | C v1 (adaptive multi-hop) | C v2 (agentic multi-hop + XBRL) |
|---|---|---|---|---|
| **Retrieval (RQ1)** | | | | |
| chunks retrieved | 10 | 5 | 8 | 7 |
| recall@5 | 0.00 | 0.00 | 0.00 | 0.00 |
| recall@all | 0.50 | 0.00 | 0.50 | 0.00 |
| complete@all | 0 | 0 | 0 | 0 |
| average precision (lexical) | 0.24 | 0.00 | 0.14 | 0.00 |
| gold evidence first rank | #1: –, #2: 7 | #1: –, #2: – | #1: 7, #2: – | #1: –, #2: – |
| **Answer (RQ3 string match)** | | | | |
| numeric_correct | ✓ | ✗ | ✓ | ✗ |
| keypoint_recall | 1.00 | 0.00 | 0.25 | 0.00 |
| **Answer & citations (RQ2)** | | | | |
| numeric_accuracy | 0.00 | 0.00 | 1.00 | 0.00 |
| citation precision | 0.33 | – | 0.00 | 0.50 |
| citation recall | 1.00 | – | 0.00 | 1.00 |
| citation F1 | 0.50 | – | 0.00 | 0.67 |
| has a citation | 1 | 0 | 1 | 1 |
| grounding error rate | – | – | 0.00 | 0.00 |
| **Cost (RQ3)** | | | | |
| retrieval hops | 1 | 1 | 3 | 1 |
| tokens | 2602 | 1322 | 16750 | 7623 |
| cost (USD) | 0.0006 | 0.0002 | 0.0671 | 0.0320 |
| latency (s) | 5.7 | 5.3 | 37.7 | 15.1 |

Definitions: [README › Metrics](../README.md#metrics). `–` = not applicable (e.g. no gold number, no citations, no guardrail).

## System outputs

### System A (vanilla dense)

Model: `gpt-5.4-2026-03-05`. Hops: 1. Chunks retrieved: 10, cited: 6.

**Generated answer**

> The context only provides Tegra Processor revenue for fiscal year 2018 ($1.53 billion) and growth rates versus fiscal 2017 and fiscal 2016, but not the explicit fiscal 2016 revenue figure. Using the provided growth rates:
>
> - FY2018 Tegra revenue = **$1.53 billion** [2]
> - FY2018 was **up 86% from FY2017** [2]
> - FY2017 was **up 47% from FY2016** [1]
>
> So:
>
> - FY2017 ≈ 1.53 / 1.86 = **$0.823 billion**
> - FY2016 ≈ 0.823 / 1.47 = **$0.560 billion**
>
> Absolute increase from FY2016 to FY2018:
>
> - **$1.53 billion - $0.560 billion ≈ $0.970 billion**, or about **$970 million** [1][2]
>
> On strategic importance, NVIDIA describes Tegra as one of its **two reportable segments** built on the company’s **single underlying architecture** [6][7]. The Tegra brand “integrates an entire computer onto a single chip” and incorporates **GPUs and multi-core CPUs** to power platforms for **autonomous robots, drones, and cars**, as well as **consoles and mobile gaming and entertainment devices** [7][9]. The business table further shows Tegra enabling branded platforms such as **DRIVE**, **SHIELD**, and **Jetson TX 2** [5]. This indicates Tegra’s strategic role is to extend NVIDIA’s hardware ecosystem beyond discrete GPUs into integrated, embedded, automotive, and edge AI platforms [5][7][9].

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `NVDA_FY2018_2018-01-28:165` | Item 7 › Table of Contents | ✓ |  | computing and initial DGX-1 sales. Revenue from Quadro GPUs for professional visualization increased 11% due primarily to higher sales in high end desktop and mobile workstation products. Revenue from GeForce GPU product… |
| 2 | `NVDA_FY2018_2018-01-28:137` | Item 7 › Table of Contents | ✓ |  | Tegra processor business revenue was $1.53 billion, up 86% from a year ago. Tegra processor business revenue includes SOC modules for the Nintendo Switch gaming console and development services. Also included was automot… |
| 3 | `NVDA_FY2018_2018-01-28:169` | Item 7 › Gross Profit and Gross Margin |  |  | GPU Business. The gross margin of our GPU business increased during fiscal year 2018 when compared to fiscal year 2017, primarily due to strong sales of our GeForce gaming GPU products and revenue growth in datacenter, i… |
| 4 | `NVDA_FY2018_2018-01-28:45` | Item 1 › Seasonality |  |  | Our GPU and Tegra processor platforms serve many markets from consumer PC gaming to enterprise workstations to government and cloud service provider datacenters, although a majority of our revenue stems from the consumer… |
| 5 | `NVDA_FY2018_2018-01-28:24` | Item 1 › Our Businesses | ✓ |  | \| GPU \| ∙ \| GeForce for PC gaming and mainstream PCs \| \|---\|---\|---\| \| \| ∙ \| GeForce NOW for cloud-based game-streaming service \| \| \| ∙ \| Quadro for design professionals working in computer-aided design, video editing, s… |
| 6 | `NVDA_FY2018_2018-01-28:23` | Item 1 › Our Businesses | ✓ |  | Our two reportable segments - GPU and Tegra Processor - are based on a single underlying architecture. |
| 7 | `NVDA_FY2018_2018-01-28:133` | Item 7 › Our Company and Our Businesses | ✓ | #2 | Starting with a focus on PC graphics, NVIDIA invented the GPU to solve some of the most complex problems in computer science. We have extended our focus in recent years to the revolutionary field of AI. Fueled by the sus… |
| 8 | `NVDA_FY2018_2018-01-28:21` | Item 1 › Our Company |  | #2 | A rapidly growing number of enterprises and startups use our GPUs to facilitate deep learning that meets, and in several cases surpasses, human perception, in fields ranging from radiology to precision agriculture. For e… |
| 9 | `NVDA_FY2018_2018-01-28:405` | Item 15 › Note 16 - Segment Information | ✓ | #2 | Our Chief Executive Officer, who is considered to be our chief operating decision maker, or CODM, reviews financial information presented on an operating segment basis for purposes of making operating decisions and asses… |
| 10 | `NVDA_FY2018_2018-01-28:163` | Item 7 › Revenue by Reportable Segments |  |  | GPU Business. GPU business revenue increased by 40% in fiscal year 2018 compared to fiscal year 2017 led by growth in gaming, datacenter and professional visualization. Revenue from sales of GeForce GPU products for gami… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#1 `NVDA_FY2018_2018-01-28:165`** (cited)

````text
ITEM 7. MANAGEMENT’S DISCUSSION AND ANALYSIS OF FINANCIAL CONDITION AND RESULTS OF OPERATIONS > Table of Contents
computing and initial DGX-1 sales. Revenue from Quadro GPUs for professional visualization increased 11% due primarily to higher sales in high end desktop and mobile workstation products. Revenue from GeForce GPU products for mainstream PC OEMs declined compared to fiscal year 2016. Tegra Processor Business. Tegra Processor business revenue increased by 86% in fiscal year 2018 compared to fiscal year 2017. This was driven by an increase of over 300% in revenue from SOC modules for gaming platforms and development services, and an increase of 15% in automotive revenue, primarily from infotainment modules, DRIVE PX platforms and development agreements for self-driving cars. Tegra Processor business revenue increased by 47% in fiscal year 2017 compared to fiscal year 2016. This was driven by an increase of over 50% in sales of Tegra products and services serving automotive systems and an increase of almost 50% in gaming development platforms and services compared to fiscal year 2016. All Other. Our patent license agreement with Intel concluded in the first quarter of fiscal year 2018. For fiscal year 2018, we recognized related revenue of $43 million, down from $264 million for fiscal years 2017 and 2016.
````

**#2 `NVDA_FY2018_2018-01-28:137`** (cited)

````text
ITEM 7. MANAGEMENT’S DISCUSSION AND ANALYSIS OF FINANCIAL CONDITION AND RESULTS OF OPERATIONS > Table of Contents
Tegra processor business revenue was $1.53 billion, up 86% from a year ago. Tegra processor business revenue includes SOC modules for the Nintendo Switch gaming console and development services. Also included was automotive revenue of $558 million, which was up 15% from a year earlier, incorporating infotainment modules, production DRIVE PX platforms, and development agreements for self-driving cars. Revenue from our patent license agreement with Intel concluded in the first quarter of fiscal year 2018. Gross margin for fiscal year 2018 was 59.9%, compared with 58.8% a year earlier, reflecting a favorable shift in mix, the growth of our GeForce gaming GPUs, and the growth of our GPU computing platform for cloud, deep learning, AI, and graphics virtualization, partially offset by the conclusion of our patent license agreement with Intel. Operating expenses for fiscal year 2018 were $2.61 billion, up from $2.13 billion in the previous year. This reflects growth in employees and related costs, as well as investments in growth initiatives, including gaming, AI, and autonomous driving.
````

**#5 `NVDA_FY2018_2018-01-28:24`** (cited)

````text
ITEM 1. BUSINESS > Our Businesses (table)
| GPU | ∙ | GeForce for PC gaming and mainstream PCs |
|---|---|---|
|  | ∙ | GeForce NOW for cloud-based game-streaming service |
|  | ∙ | Quadro for design professionals working in computer-aided design, video editing, special effects, and other creative applications |
|  | ∙ | Tesla for AI utilizing deep learning and accelerated computing, leveraging the parallel computing capabilities of GPUs for general purpose computing |
|  | ∙ | GRID to provide the power of NVIDIA graphics through the cloud and datacenters |
|  | ∙ | DGX for AI scientists, researchers and developers |
|  | ∙ | Cryptocurrency-specific GPUs |
| Tegra Processor | ∙ | Tegra processors are primarily designed to enable branded platforms - DRIVE and SHIELD |
|  | ∙ | DRIVE automotive supercomputers and software stacks that provide self-driving capabilities |
|  | ∙ | SHIELD devices and services designed to harness the power of mobile-cloud to revolutionize home entertainment, AI and gaming |
|  | ∙ | Jetson TX 2 is a power-efficient AI computing platform for embedded use |
````

**#6 `NVDA_FY2018_2018-01-28:23`** (cited)

````text
ITEM 1. BUSINESS > Our Businesses
Our two reportable segments - GPU and Tegra Processor - are based on a single underlying architecture.
````

**#7 `NVDA_FY2018_2018-01-28:133`** (cited, gold #2)

````text
ITEM 7. MANAGEMENT’S DISCUSSION AND ANALYSIS OF FINANCIAL CONDITION AND RESULTS OF OPERATIONS > Our Company and Our Businesses
Starting with a focus on PC graphics, NVIDIA invented the GPU to solve some of the most complex problems in computer science. We have extended our focus in recent years to the revolutionary field of AI. Fueled by the sustained demand for better 3D graphics and the scale of the gaming market, NVIDIA has evolved the GPU into a computer brain at the intersection of VR, HPC, and AI. Our two reportable segments - GPU and Tegra Processor - are based on a single underlying architecture. From our proprietary processors, we have created platforms that address four large markets where our expertise is critical: Gaming, Professional Visualization, Datacenter, and Automotive. While our GPU and CUDA architecture is unified, our GPU product brands are aimed at specialized markets including GeForce for gamers; Quadro for designers; Tesla and DGX for AI data scientists and big data researchers; and GRID for cloud-based visual computing users. Our Tegra brand integrates an entire computer onto a single chip, and incorporates GPUs and multi-core CPUs to drive supercomputing for autonomous robots, drones, and cars, as well as for consoles and mobile gaming and entertainment devices.
````

**#8 `NVDA_FY2018_2018-01-28:21`** (gold #2)

````text
ITEM 1. BUSINESS > Our Company
A rapidly growing number of enterprises and startups use our GPUs to facilitate deep learning that meets, and in several cases surpasses, human perception, in fields ranging from radiology to precision agriculture. For example, the transportation industry is turning to our GPUs and AI to enable autonomous vehicles, or AVs, with more than 320 companies and organizations working with NVIDIA’s DRIVE platform. Professional designers use our GPUs to create visual effects in movies and design products ranging from soft drink bottles to commercial aircraft. While our GPU and CUDA architecture is unified, our GPU product brands are aimed at specialized markets including GeForce for gamers; Quadro for designers; Tesla and DGX for AI data scientists and big data researchers; and GRID for cloud-based visual computing users. Our Tegra brand integrates an entire computer onto a single chip, and incorporates GPUs and multi-
````

**#9 `NVDA_FY2018_2018-01-28:405`** (cited, gold #2)

````text
ITEM 15. EXHIBITS, FINANCIAL STATEMENT SCHEDULE > Note 16 - Segment Information
Our Chief Executive Officer, who is considered to be our chief operating decision maker, or CODM, reviews financial information presented on an operating segment basis for purposes of making operating decisions and assessing financial performance. Our operating segments are equivalent to our reportable segments. We report our business in two primary reportable segments - the GPU business and the Tegra Processor business - based on a single underlying graphics architecture. While our GPU and CUDA architecture is unified, our GPU product brands are aimed at specialized markets including GeForce for gamers; Quadro for designers; Tesla and DGX for AI data scientists and big data researchers; and GRID for cloud-based visual computing users. Our Tegra brand integrates an entire computer onto a single chip, and incorporates GPUs and multi-core CPUs to drive supercomputing for autonomous robots, drones, and cars, as well as for consoles and mobile gaming and entertainment devices.
````

</details>

RQ2 citation match (section level): `cited=[('NVDA', 'Item 7'), ('NVDA', 'Item 1'), ('NVDA', 'Item 15')] gold=[(None, 'Item 7')]`

### System B (hybrid + rerank)

Model: `gpt-5.4-2026-03-05`. Hops: 1. Chunks retrieved: 5, cited: 0.

**Generated answer**

> Not found in the provided context.

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `NVDA_FY2018_2018-01-28:165` | Item 7 › Table of Contents |  |  | computing and initial DGX-1 sales. Revenue from Quadro GPUs for professional visualization increased 11% due primarily to higher sales in high end desktop and mobile workstation products. Revenue from GeForce GPU product… |
| 2 | `NVDA_FY2018_2018-01-28:137` | Item 7 › Table of Contents |  |  | Tegra processor business revenue was $1.53 billion, up 86% from a year ago. Tegra processor business revenue includes SOC modules for the Nintendo Switch gaming console and development services. Also included was automot… |
| 3 | `NVDA_FY2018_2018-01-28:169` | Item 7 › Gross Profit and Gross Margin |  |  | GPU Business. The gross margin of our GPU business increased during fiscal year 2018 when compared to fiscal year 2017, primarily due to strong sales of our GeForce gaming GPU products and revenue growth in datacenter, i… |
| 4 | `NVDA_FY2018_2018-01-28:164` | Item 7 › Revenue by Reportable Segments |  |  | GPU business revenue increased by 39% in fiscal year 2017 compared to fiscal year 2016. This increase was primarily due to increased revenue from our GeForce GPU gaming and datacenter platforms. Sales of high-end GeForce… |
| 5 | `NVDA_FY2018_2018-01-28:163` | Item 7 › Revenue by Reportable Segments |  |  | GPU Business. GPU business revenue increased by 40% in fiscal year 2018 compared to fiscal year 2017 led by growth in gaming, datacenter and professional visualization. Revenue from sales of GeForce GPU products for gami… |

RQ2 citation match (section level): `no citations`

### System C v1 (adaptive multi-hop)

Model: `gpt-5.4`. Hops: 3. Chunks retrieved: 8, cited: 3.

**Generated answer**

> NVIDIA's Tegra Processor revenue increased from $559 million in fiscal year 2016 to $1,534 million in fiscal year 2018, an absolute increase of $975 million. [NVDA FY2018, Item 15, NVDA_FY2018_2018-01-28:408]
>
> The company describes Tegra Processor as one of its two reportable segments, alongside GPU, and states that both segments are based on a single underlying architecture. [NVDA FY2018, Item 1, NVDA_FY2018_2018-01-28:23]
>
> Within NVIDIA's business description, Tegra processors are primarily designed to enable branded platforms such as DRIVE and SHIELD, and the Tegra-related offerings listed include DRIVE automotive supercomputers and software stacks that provide self-driving capabilities, SHIELD devices and services for home entertainment, AI and gaming, and Jetson TX 2 as a power-efficient AI computing platform for embedded use. [NVDA FY2018, Item 1, NVDA_FY2018_2018-01-28:24]

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `NVDA_FY2018_2018-01-28:137` | Item 7 › Table of Contents |  |  | Tegra processor business revenue was $1.53 billion, up 86% from a year ago. Tegra processor business revenue includes SOC modules for the Nintendo Switch gaming console and development services. Also included was automot… |
| 2 | `NVDA_FY2018_2018-01-28:165` | Item 7 › Table of Contents |  |  | computing and initial DGX-1 sales. Revenue from Quadro GPUs for professional visualization increased 11% due primarily to higher sales in high end desktop and mobile workstation products. Revenue from GeForce GPU product… |
| 3 | `NVDA_FY2018_2018-01-28:45` | Item 1 › Seasonality |  |  | Our GPU and Tegra processor platforms serve many markets from consumer PC gaming to enterprise workstations to government and cloud service provider datacenters, although a majority of our revenue stems from the consumer… |
| 4 | `NVDA_FY2018_2018-01-28:169` | Item 7 › Gross Profit and Gross Margin |  |  | GPU Business. The gross margin of our GPU business increased during fiscal year 2018 when compared to fiscal year 2017, primarily due to strong sales of our GeForce gaming GPU products and revenue growth in datacenter, i… |
| 5 | `NVDA_FY2018_2018-01-28:24` | Item 1 › Our Businesses | ✓ |  | \| GPU \| ∙ \| GeForce for PC gaming and mainstream PCs \| \|---\|---\|---\| \| \| ∙ \| GeForce NOW for cloud-based game-streaming service \| \| \| ∙ \| Quadro for design professionals working in computer-aided design, video editing, s… |
| 6 | `NVDA_FY2018_2018-01-28:23` | Item 1 › Our Businesses | ✓ |  | Our two reportable segments - GPU and Tegra Processor - are based on a single underlying architecture. |
| 7 | `NVDA_FY2018_2018-01-28:162` | Item 7 › Revenue by Reportable Segments |  | #1 | \| \| Year Ended \| \| \| \| Year Ended \| \| \| \| \|---\|---\|---\|---\|---\|---\|---\|---\|---\| \| \| January 28, 2018 \| January 29, 2017 \| $ Change \| % Change \| January 29, 2017 \| January 31, 2016 \| $ Change \| % Change \| \| \| ($ in millio… |
| 8 | `NVDA_FY2018_2018-01-28:408` | Item 15 › (Continued) | ✓ |  | \| \| GPU \| Tegra Processor \| All Other \| Consolidated \| \|---\|---\|---\|---\|---\| \| \| (In millions) \| \| \| \| \| Year Ended January 28, 2018: \| \| \| \| \| \| Revenue \| $8,137 \| $1,534 \| $43 \| $9,714 \| \| Depreciation and amortization… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#5 `NVDA_FY2018_2018-01-28:24`** (cited)

````text
ITEM 1. BUSINESS > Our Businesses (table)
| GPU | ∙ | GeForce for PC gaming and mainstream PCs |
|---|---|---|
|  | ∙ | GeForce NOW for cloud-based game-streaming service |
|  | ∙ | Quadro for design professionals working in computer-aided design, video editing, special effects, and other creative applications |
|  | ∙ | Tesla for AI utilizing deep learning and accelerated computing, leveraging the parallel computing capabilities of GPUs for general purpose computing |
|  | ∙ | GRID to provide the power of NVIDIA graphics through the cloud and datacenters |
|  | ∙ | DGX for AI scientists, researchers and developers |
|  | ∙ | Cryptocurrency-specific GPUs |
| Tegra Processor | ∙ | Tegra processors are primarily designed to enable branded platforms - DRIVE and SHIELD |
|  | ∙ | DRIVE automotive supercomputers and software stacks that provide self-driving capabilities |
|  | ∙ | SHIELD devices and services designed to harness the power of mobile-cloud to revolutionize home entertainment, AI and gaming |
|  | ∙ | Jetson TX 2 is a power-efficient AI computing platform for embedded use |
````

**#6 `NVDA_FY2018_2018-01-28:23`** (cited)

````text
ITEM 1. BUSINESS > Our Businesses
Our two reportable segments - GPU and Tegra Processor - are based on a single underlying architecture.
````

**#7 `NVDA_FY2018_2018-01-28:162`** (gold #1)

````text
ITEM 7. MANAGEMENT’S DISCUSSION AND ANALYSIS OF FINANCIAL CONDITION AND RESULTS OF OPERATIONS > Revenue by Reportable Segments (table)
|  | Year Ended |  |  |  | Year Ended |  |  |  |
|---|---|---|---|---|---|---|---|---|
|  | January 28, 2018 | January 29, 2017 | $ Change | % Change | January 29, 2017 | January 31, 2016 | $ Change | % Change |
|  | ($ in millions) |  |  |  | ($ in millions) |  |  |  |
| GPU | $8,137 | $5,822 | $2,315 | 40% | $5,822 | $4,187 | $1,635 | 39% |
| Tegra Processor | 1,534 | 824 | 710 | 86% | 824 | 559 | 265 | 47% |
| All Other | 43 | 264 | (221) | (84)% | 264 | 264 | — | —% |
| Total | $9,714 | $6,910 | $2,804 | 41% | $6,910 | $5,010 | $1,900 | 38% |
````

**#8 `NVDA_FY2018_2018-01-28:408`** (cited)

````text
ITEM 15. EXHIBITS, FINANCIAL STATEMENT SCHEDULE > (Continued) (table)
|  | GPU | Tegra Processor | All Other | Consolidated |
|---|---|---|---|---|
|  | (In millions) |  |  |  |
| Year Ended January 28, 2018: |  |  |  |  |
| Revenue | $8,137 | $1,534 | $43 | $9,714 |
| Depreciation and amortization expense | $123 | $37 | $39 | $199 |
| Operating income (loss) | $3,507 | $303 | $(600) | $3,210 |
| Year Ended January 29, 2017: |  |  |  |  |
| Revenue | $5,822 | $824 | $264 | $6,910 |
| Depreciation and amortization expense | $116 | $29 | $42 | $187 |
| Operating income (loss) | $2,180 | $(9) | $(237) | $1,934 |
| Year Ended January 31, 2016: |  |  |  |  |
| Revenue | $4,187 | $559 | $264 | $5,010 |
| Depreciation and amortization expense | $110 | $43 | $44 | $197 |
| Operating income (loss) | $1,344 | $(239) | $(358) | $747 |
````

</details>

RQ2 citation match (section level): `cited=[('NVDA', 'Item 15'), ('NVDA', 'Item 1')] gold=[(None, 'Item 7')]`

**System C guardrail** (judge `gpt-5.4`): numerical claims 3, verified 3, ungrounded 0, uncited 0, derived 1; sentence verdicts: supported 2, partial 0, unsupported 0, unchecked 0.


<details><summary>Guardrail sentence verdicts</summary>

| sentence | verdict | judge reason |
|---|---|---|
| NVIDIA's Tegra Processor revenue increased from $559 million in fiscal year 2016 to $1,534 million in fiscal year 2018, an absolute increase of $975 million. [NVDA FY2018, Item 15, NVDA_FY2018_2018-01-28:408] | None |  |
| The company describes Tegra Processor as one of its two reportable segments, alongside GPU, and states that both segments are based on a single underlying architecture. [NVDA FY2018, Item 1, NVDA_FY2018_2018-01-28:23] | supported | The evidence explicitly states the two reportable segments are GPU and Tegra Processor and that both are based on a single underlying architecture. |
| Within NVIDIA's business description, Tegra processors are primarily designed to enable branded platforms such as DRIVE and SHIELD, and the Tegra-related offerings listed include DRIVE automotive supercomputers and software stacks that provide self-driving capabilities, SHIELD devices and services for home entertainment, AI and gaming, and Jetson TX 2 as a power-efficient AI computing platform for embedded use. [NVDA FY2018, Item 1, NVDA_FY2018_2018-01-28:24] | supported | The evidence directly lists Tegra processors as enabling DRIVE and SHIELD and includes the described DRIVE, SHIELD, and Jetson TX 2 offerings with those functions. |

</details>

### System C v2 (agentic multi-hop + XBRL)

Model: `gpt-5.4`. Hops: 1. Chunks retrieved: 7, cited: 4.

**Generated answer**

> The filing does not disclose NVIDIA’s fiscal year 2016 Tegra Processor revenue amount, so the absolute increase in Tegra Processor revenue from fiscal year 2016 to fiscal year 2018, in millions of dollars, cannot be determined from the provided evidence.
>
> NVIDIA reported Tegra Processor business revenue of $1.53 billion in fiscal year 2018, and said that fiscal year 2018 Tegra Processor revenue increased 47% in fiscal year 2017 compared to fiscal year 2016 and then increased 86% in fiscal year 2018 compared to fiscal year 2017, but it did not provide the fiscal year 2016 base revenue figure in the provided evidence. [NVDA FY2018, Item 7, NVDA_FY2018_2018-01-28:137] [NVDA FY2018, Item 7, NVDA_FY2018_2018-01-28:165]
>
> The company describes Tegra Processor as one of NVIDIA’s two reportable segments, alongside GPU, and says both segments are based on a single underlying architecture. [NVDA FY2018, Item 1, NVDA_FY2018_2018-01-28:23]
>
> Within NVIDIA’s hardware ecosystem, Tegra processors are primarily designed to enable branded platforms such as DRIVE and SHIELD. [NVDA FY2018, Item 1, NVDA_FY2018_2018-01-28:24]
>
> The filing explains this strategic role by linking Tegra to DRIVE automotive supercomputers and software stacks that provide self-driving capabilities, SHIELD devices and services aimed at home entertainment, AI and gaming, and Jetson TX 2 as a power-efficient AI computing platform for embedded use. [NVDA FY2018, Item 1, NVDA_FY2018_2018-01-28:24]

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `F-NVDA-2018` | SEC XBRL Reported Financials (financials.csv) |  |  | fiscal_year,fiscal_year_end,Revenue,NetIncome,OperatingIncome,TotalAssets,TotalLiabilities,StockholdersEquity,CashAndEquivalents,OperatingCashFlow,EPSDiluted 2018,2018-01-28,9714000000,3047000000,3210000000,11241000000,3… |
| 2 | `NVDA_FY2018_2018-01-28:137` | Item 7 › Table of Contents | ✓ |  | Tegra processor business revenue was $1.53 billion, up 86% from a year ago. Tegra processor business revenue includes SOC modules for the Nintendo Switch gaming console and development services. Also included was automot… |
| 3 | `NVDA_FY2018_2018-01-28:165` | Item 7 › Table of Contents | ✓ |  | computing and initial DGX-1 sales. Revenue from Quadro GPUs for professional visualization increased 11% due primarily to higher sales in high end desktop and mobile workstation products. Revenue from GeForce GPU product… |
| 4 | `NVDA_FY2018_2018-01-28:45` | Item 1 › Seasonality |  |  | Our GPU and Tegra processor platforms serve many markets from consumer PC gaming to enterprise workstations to government and cloud service provider datacenters, although a majority of our revenue stems from the consumer… |
| 5 | `NVDA_FY2018_2018-01-28:169` | Item 7 › Gross Profit and Gross Margin |  |  | GPU Business. The gross margin of our GPU business increased during fiscal year 2018 when compared to fiscal year 2017, primarily due to strong sales of our GeForce gaming GPU products and revenue growth in datacenter, i… |
| 6 | `NVDA_FY2018_2018-01-28:24` | Item 1 › Our Businesses | ✓ |  | \| GPU \| ∙ \| GeForce for PC gaming and mainstream PCs \| \|---\|---\|---\| \| \| ∙ \| GeForce NOW for cloud-based game-streaming service \| \| \| ∙ \| Quadro for design professionals working in computer-aided design, video editing, s… |
| 7 | `NVDA_FY2018_2018-01-28:23` | Item 1 › Our Businesses | ✓ |  | Our two reportable segments - GPU and Tegra Processor - are based on a single underlying architecture. |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#2 `NVDA_FY2018_2018-01-28:137`** (cited)

````text
ITEM 7. MANAGEMENT’S DISCUSSION AND ANALYSIS OF FINANCIAL CONDITION AND RESULTS OF OPERATIONS > Table of Contents
Tegra processor business revenue was $1.53 billion, up 86% from a year ago. Tegra processor business revenue includes SOC modules for the Nintendo Switch gaming console and development services. Also included was automotive revenue of $558 million, which was up 15% from a year earlier, incorporating infotainment modules, production DRIVE PX platforms, and development agreements for self-driving cars. Revenue from our patent license agreement with Intel concluded in the first quarter of fiscal year 2018. Gross margin for fiscal year 2018 was 59.9%, compared with 58.8% a year earlier, reflecting a favorable shift in mix, the growth of our GeForce gaming GPUs, and the growth of our GPU computing platform for cloud, deep learning, AI, and graphics virtualization, partially offset by the conclusion of our patent license agreement with Intel. Operating expenses for fiscal year 2018 were $2.61 billion, up from $2.13 billion in the previous year. This reflects growth in employees and related costs, as well as investments in growth initiatives, including gaming, AI, and autonomous driving.
````

**#3 `NVDA_FY2018_2018-01-28:165`** (cited)

````text
ITEM 7. MANAGEMENT’S DISCUSSION AND ANALYSIS OF FINANCIAL CONDITION AND RESULTS OF OPERATIONS > Table of Contents
computing and initial DGX-1 sales. Revenue from Quadro GPUs for professional visualization increased 11% due primarily to higher sales in high end desktop and mobile workstation products. Revenue from GeForce GPU products for mainstream PC OEMs declined compared to fiscal year 2016. Tegra Processor Business. Tegra Processor business revenue increased by 86% in fiscal year 2018 compared to fiscal year 2017. This was driven by an increase of over 300% in revenue from SOC modules for gaming platforms and development services, and an increase of 15% in automotive revenue, primarily from infotainment modules, DRIVE PX platforms and development agreements for self-driving cars. Tegra Processor business revenue increased by 47% in fiscal year 2017 compared to fiscal year 2016. This was driven by an increase of over 50% in sales of Tegra products and services serving automotive systems and an increase of almost 50% in gaming development platforms and services compared to fiscal year 2016. All Other. Our patent license agreement with Intel concluded in the first quarter of fiscal year 2018. For fiscal year 2018, we recognized related revenue of $43 million, down from $264 million for fiscal years 2017 and 2016.
````

**#6 `NVDA_FY2018_2018-01-28:24`** (cited)

````text
ITEM 1. BUSINESS > Our Businesses (table)
| GPU | ∙ | GeForce for PC gaming and mainstream PCs |
|---|---|---|
|  | ∙ | GeForce NOW for cloud-based game-streaming service |
|  | ∙ | Quadro for design professionals working in computer-aided design, video editing, special effects, and other creative applications |
|  | ∙ | Tesla for AI utilizing deep learning and accelerated computing, leveraging the parallel computing capabilities of GPUs for general purpose computing |
|  | ∙ | GRID to provide the power of NVIDIA graphics through the cloud and datacenters |
|  | ∙ | DGX for AI scientists, researchers and developers |
|  | ∙ | Cryptocurrency-specific GPUs |
| Tegra Processor | ∙ | Tegra processors are primarily designed to enable branded platforms - DRIVE and SHIELD |
|  | ∙ | DRIVE automotive supercomputers and software stacks that provide self-driving capabilities |
|  | ∙ | SHIELD devices and services designed to harness the power of mobile-cloud to revolutionize home entertainment, AI and gaming |
|  | ∙ | Jetson TX 2 is a power-efficient AI computing platform for embedded use |
````

**#7 `NVDA_FY2018_2018-01-28:23`** (cited)

````text
ITEM 1. BUSINESS > Our Businesses
Our two reportable segments - GPU and Tegra Processor - are based on a single underlying architecture.
````

</details>

RQ2 citation match (section level): `cited=[('NVDA', 'Item 7'), ('NVDA', 'Item 1')] gold=[(None, 'Item 7')]`

**System C guardrail** (judge `gpt-5.4`): numerical claims 3, verified 3, ungrounded 0, uncited 0, derived 0; sentence verdicts: supported 4, partial 0, unsupported 0, unchecked 0.


<details><summary>Guardrail sentence verdicts</summary>

| sentence | verdict | judge reason |
|---|---|---|
| The filing does not disclose NVIDIA’s fiscal year 2016 Tegra Processor revenue amount, so the absolute increase in Tegra Processor revenue from fiscal year 2016 to fiscal year 2018, in millions of dollars, cannot be determined from the provided evidence. | supported | The evidence gives FY2018 Tegra revenue and growth rates for FY2018 and FY2017, but no explicit FY2016 Tegra revenue amount, so the absolute FY2016-to-FY2018 increase cannot be determined from the provided evidence alone. |
| NVIDIA reported Tegra Processor business revenue of $1.53 billion in fiscal year 2018, and said that fiscal year 2018 Tegra Processor revenue increased 47% in fiscal year 2017 compared to fiscal year 2016 and then increased 86% in fiscal year 2018 compared to fiscal year 2017, but it did not provide the fiscal year 2016 base revenue figure in the provided evidence. [NVDA FY2018, Item 7, NVDA_FY2018_2018-01-28:137] [NVDA FY2018, Item 7, NVDA_FY2018_2018-01-28:165] | None |  |
| The company describes Tegra Processor as one of NVIDIA’s two reportable segments, alongside GPU, and says both segments are based on a single underlying architecture. [NVDA FY2018, Item 1, NVDA_FY2018_2018-01-28:23] | supported | The cited text explicitly states NVIDIA has two reportable segments, GPU and Tegra Processor, based on a single underlying architecture. |
| Within NVIDIA’s hardware ecosystem, Tegra processors are primarily designed to enable branded platforms such as DRIVE and SHIELD. [NVDA FY2018, Item 1, NVDA_FY2018_2018-01-28:24] | supported | The cited table explicitly says Tegra processors are primarily designed to enable the branded platforms DRIVE and SHIELD. |
| The filing explains this strategic role by linking Tegra to DRIVE automotive supercomputers and software stacks that provide self-driving capabilities, SHIELD devices and services aimed at home entertainment, AI and gaming, and Jetson TX 2 as a power-efficient AI computing platform for embedded use. [NVDA FY2018, Item 1, NVDA_FY2018_2018-01-28:24] | supported | The cited table explicitly links Tegra to DRIVE, SHIELD, and Jetson TX 2 with the described functions. |

</details>
