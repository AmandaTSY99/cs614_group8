# gold-055: Single-hop text

[← all cases](../README.md) · company: Tesla, Inc. (TSLA) · fiscal year: 2017 · recipe `text` · hop `single` · answer type `qualitative` · scope `single_doc` · RQ2 category `single_hop_factual`

## Gold QA

**Question**

> For Tesla's Powerwall 2 systems sold in fiscal year 2017, what specific energy retention standard is guaranteed under the standard warranty after 10 years of use?

**Gold answer**

> The standard warranty guarantees that the energy capacity of the Powerwall 2 will be 70% or 80% of its nameplate capacity after 10 years of use, with the specific percentage depending on the region of installation.

**Key points** (RQ3 keypoint_recall targets)

1. Guarantees 70% or 80% of nameplate capacity
2. The specific percentage depends on the region of installation
3. The guarantee applies after 10 years of use

**Gold evidence**

1. `TSLA_FY2017_2017-12-31` · ITEM 1. BUSINESS › Energy Storage · text

   > For Powerwall 2, the energy retention warranty involves us guaranteeing that the energy capacity of the product will be 70% or 80% (depending on the region of installation) of its nameplate capacity after 10 years of use.

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
| keypoint_recall | 0.67 | 0.67 | 0.67 | 0.67 |
| **Answer & citations (RQ2)** | | | | |
| numeric_accuracy | – | – | – | – |
| citation precision | 0.50 | 0.50 | 1.00 | 1.00 |
| citation recall | 1.00 | 1.00 | 1.00 | 1.00 |
| citation F1 | 0.67 | 0.67 | 1.00 | 1.00 |
| has a citation | 1 | 1 | 1 | 1 |
| grounding error rate | – | – | 0.00 | 0.00 |
| **Cost (RQ3)** | | | | |
| retrieval hops | 1 | 1 | 1 | 1 |
| tokens | 2059 | 1408 | 4224 | 4218 |
| cost (USD) | 0.0003 | 0.0002 | 0.0145 | 0.0144 |
| latency (s) | 2.3 | 5.9 | 6.1 | 6.5 |

Definitions: [README › Metrics](../README.md#metrics). `–` = not applicable (e.g. no gold number, no citations, no guardrail).

## System outputs

### System A (vanilla dense)

Model: `gpt-5.4-2026-03-05`. Hops: 1. Chunks retrieved: 10, cited: 2.

**Generated answer**

> For Powerwall 2 systems, Tesla’s standard warranty guarantees that after 10 years of use, the product will retain **70% or 80% of its nameplate/stated energy capacity, depending on the region of installation** [1][2].

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `TSLA_FY2017_2017-12-31:52` | Item 1 › Energy Storage | ✓ | #1 | We generally provide a ten year “no defect” and “energy retention” warranty with every Powerwall 2 and a fifteen year “no defect” and “energy retention” warranty with every Powerpack 2 system. For Powerwall 2, the energy… |
| 2 | `TSLA_FY2017_2017-12-31:157` | Item 1A › We may be compelled to undertake product recalls or take other actions, which could adversely affect our brand image and financial performance. | ✓ | #1 | For energy storage products, we provide limited warranties against defects and to guarantee minimum energy retention levels. For example, we guarantee that each Powerwall 2 product will maintain at least 70-80% of its st… |
| 3 | `TSLA_FY2017_2017-12-31:25` | Item 1 › Energy Storage |  |  | Our energy product portfolio includes systems with a wide range of applications, from residential use to use in large grid-scale projects. Powerwall 2 is a 14 kWh rechargeable lithium-ion battery designed to store energy… |
| 4 | `TSLA_FY2017_2017-12-31:18` | Item 1 › Overview |  |  | We sell our vehicles through our own sales and service network which we are continuing to grow globally. The benefits we receive from distribution ownership enable us to improve the overall customer experience, the speed… |
| 5 | `TSLA_FY2017_2017-12-31:57` | Item 1 › Energy Storage |  |  | We currently offer a loan product to residential customers who purchase Powerwall 2 together with a new solar system, and lease and power purchase agreements to commercial customers who purchase a Powerpack 2 system toge… |
| 6 | `TSLA_FY2017_2017-12-31:398` | Item 8 › Summary of Significant Accounting Policies |  |  | For the years ended December 31, 2017 and 2016, warranty costs incurred for vehicles accounted for as operating leases or collateralized debt arrangements were $35.5 million and $19.0 million, respectively. Solar Energy … |
| 7 | `TSLA_FY2017_2017-12-31:158` | Item 1A › We may be compelled to undertake product recalls or take other actions, which could adversely affect our brand image and financial performance. |  |  | Finally, customers who buy energy from us under solar energy system leases or PPAs are covered by warranties equal to the length of the agreement term, which is typically 20 years. Systems purchased for cash are covered … |
| 8 | `TSLA_FY2017_2017-12-31:53` | Item 1 › Energy Storage |  |  | the warranties for our energy storage systems are subject to customary limitations and exclusions. |
| 9 | `TSLA_FY2017_2017-12-31:37` | Item 1 › Solar Energy Systems |  |  | We are continually innovating and developing new technologies to facilitate the growth of our solar energy systems business. For example, Solar Roof is being designed to work seamlessly with Tesla Powerwall 2 and we have… |
| 10 | `TSLA_FY2017_2017-12-31:395` | Item 8 › Summary of Significant Accounting Policies |  |  | We provide a manufacturer’s warranty on all new and used vehicles, production powertrain components and systems and energy products we sell. In addition, we also provide a warranty on the installation and components of t… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#1 `TSLA_FY2017_2017-12-31:52`** (cited, gold #1)

````text
ITEM 1. BUSINESS > Energy Storage
We generally provide a ten year “no defect” and “energy retention” warranty with every Powerwall 2 and a fifteen year “no defect” and “energy retention” warranty with every Powerpack 2 system. For Powerwall 2, the energy retention warranty involves us guaranteeing that the energy capacity of the product will be 70% or 80% (depending on the region of installation) of its nameplate capacity after 10 years of use. For Powerpack 2, the energy retention warranty involves us guaranteeing a minimum energy capacity in each of its first 15 years of use. For both products, our warranty is subject to specified use restrictions or kWh throughput caps. In addition, we offer certain extended warranties, which customers are able to purchase from us at the time they purchase an energy storage system, including a 20 year extended protection plan for Powerwall 2 and a selection of 10 or 20 year performance guarantees for Powerpack 2. We agree to repair or replace our energy storage products in the event of a valid warranty claim. In circumstances where we install a Powerwall 2 or Powerpack 2 system, we also provide warranties, generally ranging from one to four years, on our installation workmanship. All of
````

**#2 `TSLA_FY2017_2017-12-31:157`** (cited, gold #1)

````text
ITEM 1A. RISK FACTORS > We may be compelled to undertake product recalls or take other actions, which could adversely affect our brand image and financial performance.
For energy storage products, we provide limited warranties against defects and to guarantee minimum energy retention levels. For example, we guarantee that each Powerwall 2 product will maintain at least 70-80% of its stated energy capacity after 10 years, and that each Powerpack 2 product will retain specified minimum energy capacities in each of its first 10 to 15 years of use. For our Solar Roof, we offer a warranty on the glass tiles for the lifetime of a customer’s home and a separate warranty for the energy generation capability of the solar tiles. We also offer extended warranties, availability guarantees and capacity guarantees for periods of up to 20 years at an additional cost at the time of purchase, as well as workmanship warranties to customers who elect to have us install their systems.
````

</details>

RQ2 citation match (section level): `cited=[('TSLA', 'Item 1'), ('TSLA', 'Item 1A')] gold=[(None, 'Item 1')]`

### System B (hybrid + rerank)

Model: `gpt-5.4-2026-03-05`. Hops: 1. Chunks retrieved: 5, cited: 2.

**Generated answer**

> Tesla guaranteed that a Powerwall 2 would retain **70% or 80% of its nameplate/stated energy capacity after 10 years of use, depending on the region of installation** [1][2].

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `TSLA_FY2017_2017-12-31:52` | Item 1 › Energy Storage | ✓ | #1 | We generally provide a ten year “no defect” and “energy retention” warranty with every Powerwall 2 and a fifteen year “no defect” and “energy retention” warranty with every Powerpack 2 system. For Powerwall 2, the energy… |
| 2 | `TSLA_FY2017_2017-12-31:157` | Item 1A › We may be compelled to undertake product recalls or take other actions, which could adversely affect our brand image and financial performance. | ✓ | #1 | For energy storage products, we provide limited warranties against defects and to guarantee minimum energy retention levels. For example, we guarantee that each Powerwall 2 product will maintain at least 70-80% of its st… |
| 3 | `TSLA_FY2017_2017-12-31:25` | Item 1 › Energy Storage |  |  | Our energy product portfolio includes systems with a wide range of applications, from residential use to use in large grid-scale projects. Powerwall 2 is a 14 kWh rechargeable lithium-ion battery designed to store energy… |
| 4 | `TSLA_FY2017_2017-12-31:18` | Item 1 › Overview |  |  | We sell our vehicles through our own sales and service network which we are continuing to grow globally. The benefits we receive from distribution ownership enable us to improve the overall customer experience, the speed… |
| 5 | `TSLA_FY2017_2017-12-31:395` | Item 8 › Summary of Significant Accounting Policies |  |  | We provide a manufacturer’s warranty on all new and used vehicles, production powertrain components and systems and energy products we sell. In addition, we also provide a warranty on the installation and components of t… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#1 `TSLA_FY2017_2017-12-31:52`** (cited, gold #1)

````text
ITEM 1. BUSINESS > Energy Storage
We generally provide a ten year “no defect” and “energy retention” warranty with every Powerwall 2 and a fifteen year “no defect” and “energy retention” warranty with every Powerpack 2 system. For Powerwall 2, the energy retention warranty involves us guaranteeing that the energy capacity of the product will be 70% or 80% (depending on the region of installation) of its nameplate capacity after 10 years of use. For Powerpack 2, the energy retention warranty involves us guaranteeing a minimum energy capacity in each of its first 15 years of use. For both products, our warranty is subject to specified use restrictions or kWh throughput caps. In addition, we offer certain extended warranties, which customers are able to purchase from us at the time they purchase an energy storage system, including a 20 year extended protection plan for Powerwall 2 and a selection of 10 or 20 year performance guarantees for Powerpack 2. We agree to repair or replace our energy storage products in the event of a valid warranty claim. In circumstances where we install a Powerwall 2 or Powerpack 2 system, we also provide warranties, generally ranging from one to four years, on our installation workmanship. All of
````

**#2 `TSLA_FY2017_2017-12-31:157`** (cited, gold #1)

````text
ITEM 1A. RISK FACTORS > We may be compelled to undertake product recalls or take other actions, which could adversely affect our brand image and financial performance.
For energy storage products, we provide limited warranties against defects and to guarantee minimum energy retention levels. For example, we guarantee that each Powerwall 2 product will maintain at least 70-80% of its stated energy capacity after 10 years, and that each Powerpack 2 product will retain specified minimum energy capacities in each of its first 10 to 15 years of use. For our Solar Roof, we offer a warranty on the glass tiles for the lifetime of a customer’s home and a separate warranty for the energy generation capability of the solar tiles. We also offer extended warranties, availability guarantees and capacity guarantees for periods of up to 20 years at an additional cost at the time of purchase, as well as workmanship warranties to customers who elect to have us install their systems.
````

</details>

RQ2 citation match (section level): `cited=[('TSLA', 'Item 1'), ('TSLA', 'Item 1A')] gold=[(None, 'Item 1')]`

### System C v1 (adaptive multi-hop)

Model: `gpt-5.4`. Hops: 1. Chunks retrieved: 6, cited: 1.

**Generated answer**

> For Powerwall 2 systems sold in fiscal year 2017, Tesla’s standard energy retention warranty guarantees that the product’s energy capacity will be 70% or 80%, depending on the region of installation, of its nameplate capacity after 10 years of use [TSLA FY2017, Item 1, TSLA_FY2017_2017-12-31:52].

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `TSLA_FY2017_2017-12-31:52` | Item 1 › Energy Storage | ✓ | #1 | We generally provide a ten year “no defect” and “energy retention” warranty with every Powerwall 2 and a fifteen year “no defect” and “energy retention” warranty with every Powerpack 2 system. For Powerwall 2, the energy… |
| 2 | `TSLA_FY2017_2017-12-31:157` | Item 1A › We may be compelled to undertake product recalls or take other actions, which could adversely affect our brand image and financial performance. |  | #1 | For energy storage products, we provide limited warranties against defects and to guarantee minimum energy retention levels. For example, we guarantee that each Powerwall 2 product will maintain at least 70-80% of its st… |
| 3 | `TSLA_FY2017_2017-12-31:54` | Item 1 › Solar Energy Systems |  |  | For traditional solar systems that are leased or under power purchase agreements (“PPAs”), we provide a full system warranty for 20 years from installation. For other traditional solar systems, we provide a 20 year insta… |
| 4 | `TSLA_FY2017_2017-12-31:156` | Item 1A › We may be compelled to undertake product recalls or take other actions, which could adversely affect our brand image and financial performance. |  |  | our standard range battery and an eight year or 120,000 mile limited warranty for our long range battery, with minimum 70% retention of battery capacity over the warranty period. In addition, customers of new Model S and… |
| 5 | `TSLA_FY2017_2017-12-31:25` | Item 1 › Energy Storage |  |  | Our energy product portfolio includes systems with a wide range of applications, from residential use to use in large grid-scale projects. Powerwall 2 is a 14 kWh rechargeable lithium-ion battery designed to store energy… |
| 6 | `TSLA_FY2017_2017-12-31:395` | Item 8 › Summary of Significant Accounting Policies |  |  | We provide a manufacturer’s warranty on all new and used vehicles, production powertrain components and systems and energy products we sell. In addition, we also provide a warranty on the installation and components of t… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#1 `TSLA_FY2017_2017-12-31:52`** (cited, gold #1)

````text
ITEM 1. BUSINESS > Energy Storage
We generally provide a ten year “no defect” and “energy retention” warranty with every Powerwall 2 and a fifteen year “no defect” and “energy retention” warranty with every Powerpack 2 system. For Powerwall 2, the energy retention warranty involves us guaranteeing that the energy capacity of the product will be 70% or 80% (depending on the region of installation) of its nameplate capacity after 10 years of use. For Powerpack 2, the energy retention warranty involves us guaranteeing a minimum energy capacity in each of its first 15 years of use. For both products, our warranty is subject to specified use restrictions or kWh throughput caps. In addition, we offer certain extended warranties, which customers are able to purchase from us at the time they purchase an energy storage system, including a 20 year extended protection plan for Powerwall 2 and a selection of 10 or 20 year performance guarantees for Powerpack 2. We agree to repair or replace our energy storage products in the event of a valid warranty claim. In circumstances where we install a Powerwall 2 or Powerpack 2 system, we also provide warranties, generally ranging from one to four years, on our installation workmanship. All of
````

**#2 `TSLA_FY2017_2017-12-31:157`** (gold #1)

````text
ITEM 1A. RISK FACTORS > We may be compelled to undertake product recalls or take other actions, which could adversely affect our brand image and financial performance.
For energy storage products, we provide limited warranties against defects and to guarantee minimum energy retention levels. For example, we guarantee that each Powerwall 2 product will maintain at least 70-80% of its stated energy capacity after 10 years, and that each Powerpack 2 product will retain specified minimum energy capacities in each of its first 10 to 15 years of use. For our Solar Roof, we offer a warranty on the glass tiles for the lifetime of a customer’s home and a separate warranty for the energy generation capability of the solar tiles. We also offer extended warranties, availability guarantees and capacity guarantees for periods of up to 20 years at an additional cost at the time of purchase, as well as workmanship warranties to customers who elect to have us install their systems.
````

</details>

RQ2 citation match (section level): `cited=[('TSLA', 'Item 1')] gold=[(None, 'Item 1')]`

**System C guardrail** (judge `gpt-5.4`): numerical claims 2, verified 2, ungrounded 0, uncited 0, derived 0; sentence verdicts: supported 0, partial 0, unsupported 0, unchecked 0.


<details><summary>Guardrail sentence verdicts</summary>

| sentence | verdict | judge reason |
|---|---|---|
| For Powerwall 2 systems sold in fiscal year 2017, Tesla’s standard energy retention warranty guarantees that the product’s energy capacity will be 70% or 80%, depending on the region of installation, of its nameplate capacity after 10 years of use [TSLA FY2017, Item 1, TSLA_FY2017_2017-12-31:52]. | None |  |

</details>

### System C v2 (agentic multi-hop + XBRL)

Model: `gpt-5.4`. Hops: 1. Chunks retrieved: 6, cited: 1.

**Generated answer**

> For Powerwall 2 systems sold in fiscal year 2017, Tesla’s standard energy retention warranty guarantees that the product will retain 70% or 80%, depending on the region of installation, of its nameplate capacity after 10 years of use [TSLA FY2017, Item 1, TSLA_FY2017_2017-12-31:52].

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `TSLA_FY2017_2017-12-31:52` | Item 1 › Energy Storage | ✓ | #1 | We generally provide a ten year “no defect” and “energy retention” warranty with every Powerwall 2 and a fifteen year “no defect” and “energy retention” warranty with every Powerpack 2 system. For Powerwall 2, the energy… |
| 2 | `TSLA_FY2017_2017-12-31:157` | Item 1A › We may be compelled to undertake product recalls or take other actions, which could adversely affect our brand image and financial performance. |  | #1 | For energy storage products, we provide limited warranties against defects and to guarantee minimum energy retention levels. For example, we guarantee that each Powerwall 2 product will maintain at least 70-80% of its st… |
| 3 | `TSLA_FY2017_2017-12-31:54` | Item 1 › Solar Energy Systems |  |  | For traditional solar systems that are leased or under power purchase agreements (“PPAs”), we provide a full system warranty for 20 years from installation. For other traditional solar systems, we provide a 20 year insta… |
| 4 | `TSLA_FY2017_2017-12-31:156` | Item 1A › We may be compelled to undertake product recalls or take other actions, which could adversely affect our brand image and financial performance. |  |  | our standard range battery and an eight year or 120,000 mile limited warranty for our long range battery, with minimum 70% retention of battery capacity over the warranty period. In addition, customers of new Model S and… |
| 5 | `TSLA_FY2017_2017-12-31:25` | Item 1 › Energy Storage |  |  | Our energy product portfolio includes systems with a wide range of applications, from residential use to use in large grid-scale projects. Powerwall 2 is a 14 kWh rechargeable lithium-ion battery designed to store energy… |
| 6 | `TSLA_FY2017_2017-12-31:395` | Item 8 › Summary of Significant Accounting Policies |  |  | We provide a manufacturer’s warranty on all new and used vehicles, production powertrain components and systems and energy products we sell. In addition, we also provide a warranty on the installation and components of t… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#1 `TSLA_FY2017_2017-12-31:52`** (cited, gold #1)

````text
ITEM 1. BUSINESS > Energy Storage
We generally provide a ten year “no defect” and “energy retention” warranty with every Powerwall 2 and a fifteen year “no defect” and “energy retention” warranty with every Powerpack 2 system. For Powerwall 2, the energy retention warranty involves us guaranteeing that the energy capacity of the product will be 70% or 80% (depending on the region of installation) of its nameplate capacity after 10 years of use. For Powerpack 2, the energy retention warranty involves us guaranteeing a minimum energy capacity in each of its first 15 years of use. For both products, our warranty is subject to specified use restrictions or kWh throughput caps. In addition, we offer certain extended warranties, which customers are able to purchase from us at the time they purchase an energy storage system, including a 20 year extended protection plan for Powerwall 2 and a selection of 10 or 20 year performance guarantees for Powerpack 2. We agree to repair or replace our energy storage products in the event of a valid warranty claim. In circumstances where we install a Powerwall 2 or Powerpack 2 system, we also provide warranties, generally ranging from one to four years, on our installation workmanship. All of
````

**#2 `TSLA_FY2017_2017-12-31:157`** (gold #1)

````text
ITEM 1A. RISK FACTORS > We may be compelled to undertake product recalls or take other actions, which could adversely affect our brand image and financial performance.
For energy storage products, we provide limited warranties against defects and to guarantee minimum energy retention levels. For example, we guarantee that each Powerwall 2 product will maintain at least 70-80% of its stated energy capacity after 10 years, and that each Powerpack 2 product will retain specified minimum energy capacities in each of its first 10 to 15 years of use. For our Solar Roof, we offer a warranty on the glass tiles for the lifetime of a customer’s home and a separate warranty for the energy generation capability of the solar tiles. We also offer extended warranties, availability guarantees and capacity guarantees for periods of up to 20 years at an additional cost at the time of purchase, as well as workmanship warranties to customers who elect to have us install their systems.
````

</details>

RQ2 citation match (section level): `cited=[('TSLA', 'Item 1')] gold=[(None, 'Item 1')]`

**System C guardrail** (judge `gpt-5.4`): numerical claims 2, verified 2, ungrounded 0, uncited 0, derived 0; sentence verdicts: supported 0, partial 0, unsupported 0, unchecked 0.


<details><summary>Guardrail sentence verdicts</summary>

| sentence | verdict | judge reason |
|---|---|---|
| For Powerwall 2 systems sold in fiscal year 2017, Tesla’s standard energy retention warranty guarantees that the product will retain 70% or 80%, depending on the region of installation, of its nameplate capacity after 10 years of use [TSLA FY2017, Item 1, TSLA_FY2017_2017-12-31:52]. | None |  |

</details>
