# gold-085: Cross-year text

[← all cases](../README.md) · company: MICROSOFT CORP (MSFT) · fiscal year: 2025 · recipe `cross_year_text` · hop `multi` · answer type `qualitative` · scope `cross_year` · RQ2 category `multi_company_comparison`

## Gold QA

**Question**

> How has Microsoft's description of the specific threat vectors and potential consequences of cybersecurity incidents evolved between its fiscal year 2020 10-K and its fiscal year 2025 10-K?

**Gold answer**

> Microsoft's fiscal 2025 10-K states that it has experienced cybersecurity incidents in which threat actors gained unauthorized access to its systems and data, including customer systems and data, and cites a nation-state associated actor that used a password spray attack on a legacy test account to gain access to Microsoft email accounts. It also warns that threat actors may use emerging technologies such as AI and machine learning, and may use the supply chain to introduce malware. The fiscal 2020 10-K described threats in more general terms (malicious software, exploiting vulnerabilities, social engineering and coordinated attacks such as distributed denial of service) without acknowledging actual incidents.

**Key points** (RQ3 keypoint_recall targets)

1. The FY2025 filing explicitly states that Microsoft has experienced cybersecurity incidents involving unauthorized access to systems and customer data.
2. The FY2025 filing identifies the use of AI and machine learning and supply chain attacks as specific evolving threat vectors.
3. The FY2020 filing described threats in more general terms, including malicious software, social engineering, and DDoS attacks, without explicitly acknowledging recent specific breaches in the same way.

**Gold evidence**

1. `MSFT_FY2025_2025-06-30` · Item 1A › Security of our information technology · text

   > we have experienced cybersecurity incidents in which such actors have gained unauthorized access to our systems and data, including customer systems and data.

2. `MSFT_FY2025_2025-06-30` · Item 1A › Security of our information technology · text

   > Threat actors may also utilize emerging technologies, such as AI and machine learning.

3. `MSFT_FY2020_2020-06-30` · Item 1A › Security of our information technology · text

   > These actors may use a wide variety of methods, which may include developing and deploying malicious software or exploiting vulnerabilities in hardware, software, or other infrastructure in order to attack our products and services or gain access to our networks and datacenters

4. `MSFT_FY2025_2025-06-30` · Item 1A › Security of our information technology · text

   > a nation-state associated threat actor used a password spray attack to compromise a legacy test account and, in turn, gain access to Microsoft email accounts.

5. `MSFT_FY2025_2025-06-30` · Item 1A › Security of our information technology · text

   > Malicious actors may employ the supply chain to introduce malware through software updates or compromised supplier accounts or hardware.

## Scorecard

| Metric | A (vanilla dense) | B (hybrid + rerank) | C v1 (adaptive multi-hop) | C v2 (agentic multi-hop + XBRL) |
|---|---|---|---|---|
| **Retrieval (RQ1)** | | | | |
| chunks retrieved | 8 | 5 | 11 | 12 |
| recall@5 | 0.60 | 0.60 | 0.60 | 0.60 |
| recall@all | 0.60 | 0.60 | 0.80 | 0.60 |
| complete@all | 0 | 0 | 0 | 0 |
| average precision (lexical) | 0.23 | 0.45 | 0.35 | 0.50 |
| gold evidence first rank | #1: 5, #2: –, #3: 5, #4: 5, #5: – | #1: 2, #2: –, #3: 5, #4: 2, #5: – | #1: 2, #2: –, #3: 2, #4: 2, #5: 7 | #1: 2, #2: –, #3: 2, #4: 2, #5: – |
| **Answer (RQ3 string match)** | | | | |
| numeric_correct | ✓ | ✗ | ✓ | ✓ |
| keypoint_recall | 0.67 | 0.00 | 1.00 | 0.67 |
| **Answer & citations (RQ2)** | | | | |
| numeric_accuracy | – | – | – | – |
| citation precision | 1.00 | – | 1.00 | 1.00 |
| citation recall | 1.00 | – | 1.00 | 1.00 |
| citation F1 | 1.00 | – | 1.00 | 1.00 |
| has a citation | 1 | 0 | 1 | 1 |
| grounding error rate | – | – | 0.00 | 0.00 |
| **Cost (RQ3)** | | | | |
| retrieval hops | 1 | 1 | 2 | 3 |
| tokens | 2233 | 1255 | 31082 | 41985 |
| cost (USD) | 0.0006 | 0.0002 | 0.1292 | 0.1647 |
| latency (s) | 10.6 | 6.5 | 50.0 | 61.0 |

Definitions: [README › Metrics](../README.md#metrics). `–` = not applicable (e.g. no gold number, no citations, no guardrail).

## System outputs

### System A (vanilla dense)

Model: `gpt-5.4-2026-03-05`. Hops: 1. Chunks retrieved: 8, cited: 5.

**Generated answer**

> Between FY2020 and FY2025, Microsoft’s disclosure became much more specific about both the kinds of cyber threats it faces and the consequences those incidents can have.
>
> **In FY2020**, Microsoft described cyber risk in broader, more general terms:
> - Cyberthreats were said to be “constantly evolving,” harder to detect, and potentially able to persist undetected for long periods [6].
> - It warned that breaches of facilities, networks, or data security could:
>   - disrupt systems and business applications,
>   - impair service delivery and privacy protection,
>   - delay product development,
>   - compromise confidential or technical business information,
>   - harm reputation or competitive position,
>   - lead to theft or misuse of intellectual property or other assets,
>   - require more resources to improve technologies, and
>   - otherwise adversely affect the business [6].
> - It also summarized the risk at a high level as cyberattacks and security vulnerabilities potentially causing reduced revenue, increased costs, liability claims, or reputational/competitive harm [3].
>
> **In FY2025**, Microsoft provided a much more detailed and concrete description of threat vectors:
> - It identified specific threat actors, including individual hackers, organized groups, nation-states, state-sponsored organizations, and cybercriminal groups [5].
> - It listed specific attack methods, including:
>   - malicious software,
>   - exploitation of known and potential vulnerabilities,
>   - exploitation of intentionally designed processes in Microsoft or third-party hardware/software/infrastructure,
>   - attacks on products, services, networks, and datacenters,
>   - social engineering to obtain passwords or induce harmful actions, and
>   - coordinated attacks [5].
> - It also disclosed a specific example: a nation-state actor used a **password spray attack** beginning in late November 2023 to compromise a legacy test account, access Microsoft email accounts, and then gain unauthorized access to some source code repositories and internal systems [5][8].
> - FY2025 further noted operational weaknesses such as failures in applying security patches to all connected hardware and devices, including end-of-life and end-of-support equipment, as a continuing source of unauthorized access risk [8].
>
> **The consequences described in FY2025** also became more explicit and tied to real incidents:
> - Microsoft said it had experienced incidents involving unauthorized access to its systems and data, including customer systems and data [5].
> - It stated that the disclosed incident “has and may continue to result in harm to our reputation and customer relationships” [8].
> - It warned that threat actors could continue using obtained information to try to access systems or otherwise adversely affect business and results of operations [8].
> - It said cyber incidents and attacks, individually or in the aggregate, could adversely affect financial condition, results of operations, competitive position, and reputation [8].
> - It also noted that cybersecurity-related legislation and regulation may increase costs and create compliance and enforcement risks [7].
>
> **Overall**, the evolution is from a **generic, principle-level risk description in FY2020** to a **more granular, incident-informed, and actor/method-specific disclosure in FY2025**, with clearer examples of how attacks occur and more concrete articulation of business, operational, financial, reputational, and customer-relationship consequences [3][6][5][8][7].

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `MSFT_FY2025_2025-06-30:83` | Item 1A › PART I |  |  | CYBERSECURITY, DATA PRIVACY, AND PLATFORM ABUSE RISKS Cyberattacks and security vulnerabilities could lead to reduced revenue, increased costs, liability claims, or harm to our reputation or competitive position. |
| 2 | `MSFT_FY2025_2025-06-30:145` | Item 1C › PART I |  |  | We describe the risks from cybersecurity threats, including previous cybersecurity incidents, in section “Risk Factors” (Part I, Item 1A of this Form 10-K). As of the date of this Form 10-K, we do not believe any risks f… |
| 3 | `MSFT_FY2020_2020-06-30:100` | Item 1A › PART I | ✓ |  | Cyberattacks and security vulnerabilities could lead to reduced revenue, increased costs, liability claims, or harm to our reputation or competitive position. |
| 4 | `MSFT_FY2025_2025-06-30:139` | Item 1C |  |  | RISK MANAGEMENT AND STRATEGY Microsoft plays a central role in the world’s digital ecosystem. We have made it the top corporate priority to protect the computing environment used by our customers and employees and to sup… |
| 5 | `MSFT_FY2025_2025-06-30:84` | Item 1A › Security of our information technology | ✓ | #1, #3, #4 | Threats to security can take a variety of forms. Threat actors, including individual and groups of hackers and sophisticated organizations, including nation-states, state-sponsored organizations, or cybercriminal groups,… |
| 6 | `MSFT_FY2020_2020-06-30:102` | Item 1A › Security of our information technology | ✓ |  | Cyberthreats are constantly evolving, increasing the difficulty of detecting and successfully defending against them. We may have no current capability to detect certain vulnerabilities, which may allow them to persist i… |
| 7 | `MSFT_FY2025_2025-06-30:116` | Item 1A › PART I | ✓ |  | could impact cloud and devices supply chain cost competitiveness. The potential replacement of the recently rescinded AI Diffusion Rule and other potential AI-related rulemakings could adversely affect Microsoft’s busine… |
| 8 | `MSFT_FY2025_2025-06-30:85` | Item 1A › Security of our information technology | ✓ | #1, #4 | legacy test account and, in turn, gain access to Microsoft email accounts. The threat actor used information it obtained to gain unauthorized access to some of our source code repositories and internal systems, and the t… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#3 `MSFT_FY2020_2020-06-30:100`** (cited)

````text
Item 1A > PART I
Cyberattacks and security vulnerabilities could lead to reduced revenue, increased costs, liability claims, or harm to our reputation or competitive position.
````

**#5 `MSFT_FY2025_2025-06-30:84`** (cited, gold #1, gold #3, gold #4)

````text
Item 1A > Security of our information technology
Threats to security can take a variety of forms. Threat actors, including individual and groups of hackers and sophisticated organizations, including nation-states, state-sponsored organizations, or cybercriminal groups, continuously undertake attacks that pose threats to our customers and our internal infrastructure, and we have experienced cybersecurity incidents in which such actors have gained unauthorized access to our systems and data, including customer systems and data. These actors use a wide variety of methods, which include developing and deploying malicious software; exploiting known and potential vulnerabilities or intentionally designed processes in our or third-party hardware, software, or other infrastructure to attack our products and services or gain access to our networks and datacenters; using social engineering techniques to induce our employees, users, partners, or customers to disclose sensitive information, such as passwords, or take other actions to gain access to our data or our users’ or customers’ data; or acting in a coordinated manner or conducting coordinated attacks. For example, as previously disclosed in our Form 8-K filed with the Securities and Exchange Commission on January 19, 2024 and amended on March 8, 2024, beginning in late November 2023, a nation-state associated threat actor used a password spray attack to compromise a
````

**#6 `MSFT_FY2020_2020-06-30:102`** (cited)

````text
Item 1A > Security of our information technology
Cyberthreats are constantly evolving, increasing the difficulty of detecting and successfully defending against them. We may have no current capability to detect certain vulnerabilities, which may allow them to persist in the environment over long periods of time. Cyberthreats can have cascading impacts that unfold with increasing speed across our internal networks and systems and those of our partners and customers. Breaches of our facilities, network, or data security could disrupt the security of our systems and business applications, impair our ability to provide services to our customers and protect the privacy of their data, result in product development delays, compromise confidential or technical business information harming our reputation or competitive position, result in theft or misuse of our intellectual property or other assets, require us to allocate more resources to improve technologies, or otherwise adversely affect our business.
````

**#7 `MSFT_FY2025_2025-06-30:116`** (cited)

````text
Item 1A > PART I
could impact cloud and devices supply chain cost competitiveness. The potential replacement of the recently rescinded AI Diffusion Rule and other potential AI-related rulemakings could adversely affect Microsoft’s business, strategy, and operations. Periods of intense diplomatic or armed conflict like the ongoing conflict in Ukraine and the Israel-Hamas conflict could result in (1) new and rapidly evolving sanctions and trade restrictions, which may impair trade with sanctioned individuals and countries, and (2) negative impacts to regional trade ecosystems among our customers, partners, and us. • Cybersecurity: Legislative and regulatory actions related to cybersecurity may increase the costs associated with developing, implementing, or securing our products and services. The legal and regulatory environment in this area is complex and continues to evolve across multiple jurisdictions. As a result, there is considerable uncertainty regarding both current and future compliance obligations. This uncertainty increases the risk that we may incur additional operational costs, face regulatory enforcement actions, or encounter challenges in the development and deployment of our products. •
````

**#8 `MSFT_FY2025_2025-06-30:85`** (cited, gold #1, gold #4)

````text
Item 1A > Security of our information technology
legacy test account and, in turn, gain access to Microsoft email accounts. The threat actor used information it obtained to gain unauthorized access to some of our source code repositories and internal systems, and the threat actor could continue to utilize this and other information to attempt to gain access to our systems or otherwise adversely affect our business and results of operations. This incident has and may continue to result in harm to our reputation and customer relationships. Nation-state and state-sponsored actors can sustain malicious activities for extended periods and deploy significant resources to plan and carry out attacks. Nation-state attacks against us, our customers, or our partners have and may continue to intensify due to our transparency to our customers, other stakeholders, and the public about cyberattacks, and during elections or periods of intense diplomatic or armed conflict. Challenges or failures in applying security patches to all hardware and devices connected to our systems, including end-of-life and end-of-support equipment, have and may continue to result in unauthorized access to our systems and data in the future. Cyber incidents and attacks, individually or in the aggregate, could adversely affect our financial condition, results of operations, competitive position, and reputation,
````

</details>

RQ2 citation match (section level): `cited=[('MSFT', 'Item 1A')] gold=[(None, 'Item 1A')]`

### System B (hybrid + rerank)

Model: `gpt-5.4-2026-03-05`. Hops: 1. Chunks retrieved: 5, cited: 0.

**Generated answer**

> Not found in the provided context.

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `MSFT_FY2025_2025-06-30:145` | Item 1C › PART I |  |  | We describe the risks from cybersecurity threats, including previous cybersecurity incidents, in section “Risk Factors” (Part I, Item 1A of this Form 10-K). As of the date of this Form 10-K, we do not believe any risks f… |
| 2 | `MSFT_FY2025_2025-06-30:85` | Item 1A › Security of our information technology |  | #1, #4 | legacy test account and, in turn, gain access to Microsoft email accounts. The threat actor used information it obtained to gain unauthorized access to some of our source code repositories and internal systems, and the t… |
| 3 | `MSFT_FY2025_2025-06-30:139` | Item 1C |  |  | RISK MANAGEMENT AND STRATEGY Microsoft plays a central role in the world’s digital ecosystem. We have made it the top corporate priority to protect the computing environment used by our customers and employees and to sup… |
| 4 | `MSFT_FY2025_2025-06-30:166` | Item 7 › Reportable Segments |  |  | We report our financial performance based on the following segments: Productivity and Business Processes, Intelligent Cloud, and More Personal Computing. The segment amounts included in MD&A are presented on a basis cons… |
| 5 | `MSFT_FY2025_2025-06-30:84` | Item 1A › Security of our information technology |  | #1, #3, #4 | Threats to security can take a variety of forms. Threat actors, including individual and groups of hackers and sophisticated organizations, including nation-states, state-sponsored organizations, or cybercriminal groups,… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#2 `MSFT_FY2025_2025-06-30:85`** (gold #1, gold #4)

````text
Item 1A > Security of our information technology
legacy test account and, in turn, gain access to Microsoft email accounts. The threat actor used information it obtained to gain unauthorized access to some of our source code repositories and internal systems, and the threat actor could continue to utilize this and other information to attempt to gain access to our systems or otherwise adversely affect our business and results of operations. This incident has and may continue to result in harm to our reputation and customer relationships. Nation-state and state-sponsored actors can sustain malicious activities for extended periods and deploy significant resources to plan and carry out attacks. Nation-state attacks against us, our customers, or our partners have and may continue to intensify due to our transparency to our customers, other stakeholders, and the public about cyberattacks, and during elections or periods of intense diplomatic or armed conflict. Challenges or failures in applying security patches to all hardware and devices connected to our systems, including end-of-life and end-of-support equipment, have and may continue to result in unauthorized access to our systems and data in the future. Cyber incidents and attacks, individually or in the aggregate, could adversely affect our financial condition, results of operations, competitive position, and reputation,
````

**#5 `MSFT_FY2025_2025-06-30:84`** (gold #1, gold #3, gold #4)

````text
Item 1A > Security of our information technology
Threats to security can take a variety of forms. Threat actors, including individual and groups of hackers and sophisticated organizations, including nation-states, state-sponsored organizations, or cybercriminal groups, continuously undertake attacks that pose threats to our customers and our internal infrastructure, and we have experienced cybersecurity incidents in which such actors have gained unauthorized access to our systems and data, including customer systems and data. These actors use a wide variety of methods, which include developing and deploying malicious software; exploiting known and potential vulnerabilities or intentionally designed processes in our or third-party hardware, software, or other infrastructure to attack our products and services or gain access to our networks and datacenters; using social engineering techniques to induce our employees, users, partners, or customers to disclose sensitive information, such as passwords, or take other actions to gain access to our data or our users’ or customers’ data; or acting in a coordinated manner or conducting coordinated attacks. For example, as previously disclosed in our Form 8-K filed with the Securities and Exchange Commission on January 19, 2024 and amended on March 8, 2024, beginning in late November 2023, a nation-state associated threat actor used a password spray attack to compromise a
````

</details>

RQ2 citation match (section level): `no citations`

### System C v1 (adaptive multi-hop)

Model: `gpt-5.4`. Hops: 2. Chunks retrieved: 11, cited: 5.

**Generated answer**

> Between fiscal 2020 and fiscal 2025, Microsoft’s description of threat actors remained broadly similar in identifying individual hackers, groups, sophisticated organizations, state-sponsored organizations, and nation-states as persistent attackers, but the 2025 filing uses more expansive language by referring to “threat actors,” including “cybercriminal groups,” and states that Microsoft has experienced cybersecurity incidents in which such actors gained unauthorized access to its systems and data, including customer systems and data [MSFT FY2020, Item 1A, MSFT_FY2020_2020-06-30:101] [MSFT FY2025, Item 1A, MSFT_FY2025_2025-06-30:84].
>
> In fiscal 2020, Microsoft described threat methods as developing and deploying malicious software, exploiting vulnerabilities in hardware, software, or other infrastructure, using social engineering to induce disclosure of passwords or other sensitive information, and launching distributed denial of service or other coordinated attacks [MSFT FY2020, Item 1A, MSFT_FY2020_2020-06-30:101]. In fiscal 2025, Microsoft expanded this description to include exploiting “known and potential vulnerabilities or intentionally designed processes” in Microsoft or third-party hardware, software, or other infrastructure, attacking products and services or gaining access to networks and datacenters, using social engineering against employees, users, partners, or customers, and acting in a coordinated manner or conducting coordinated attacks [MSFT FY2025, Item 1A, MSFT_FY2025_2025-06-30:84].
>
> The 2025 filing also adds a specific disclosed example of a nation-state associated threat actor using a password spray attack beginning in late November 2023, which is a concrete attack vector not described in the 2020 filing [MSFT FY2025, Item 1A, MSFT_FY2025_2025-06-30:84] [MSFT FY2020, Item 1A, MSFT_FY2020_2020-06-30:101].
>
> For internal information technology risks, the 2020 filing said inadequate account security practices could result in unauthorized access to confidential data and gave the example that system administrators may fail to timely remove employee account access when no longer appropriate [MSFT FY2020, Item 1A, MSFT_FY2020_2020-06-30:101]. In 2025, Microsoft broadened this discussion by stating that inadequate account security or organizational security practices, including those of acquired companies or third parties it uses, have resulted and may result in unauthorized access to its systems and data, including customer systems and data, and it added examples such as passwords not being rotated and employee access not being updated or removed on a timely basis [MSFT FY2025, Item 1A, MSFT_FY2025_2025-06-30:86].
>
> The 2025 filing further expands the threat-vector discussion by adding supply-chain risk, stating that malicious actors may employ the supply chain to introduce malware through software updates or compromised supplier accounts or hardware, which was not described in the 2020 filing [MSFT FY2025, Item 1A, MSFT_FY2025_2025-06-30:86] [MSFT FY2020, Item 1A, MSFT_FY2020_2020-06-30:101].
>
> For product and customer security, the 2020 filing emphasized that customers using cloud-based services rely on the security of Microsoft’s infrastructure, including hardware and other elements provided by third parties, and that adversaries who acquire user account information at other companies can compromise Microsoft users’ accounts where accounts share the same attributes as passwords [MSFT FY2020, Item 1A, MSFT_FY2020_2020-06-30:104]. In 2025, Microsoft broadened this to cover both cloud and on-premises environments, stated that threats to or attacks on its own infrastructure, such as the nation-state attack described in the prior risk factor, have also affected customers and may do so in the future, and added that adversaries can attack customers’ on-premises or cloud environments, sometimes exploiting previously unknown “zero-day” vulnerabilities [MSFT FY2025, Item 1A, MSFT_FY2025_2025-06-30:90].
>
> The 2025 filing also adds more detail on persistence and post-patch risk by stating that product vulnerabilities can persist even after security patches have been issued if customers have not installed the most recent updates, or if attackers exploited the vulnerabilities before patching to install additional malware to further compromise customers’ systems, which is not described in the 2020 filing [MSFT FY2025, Item 1A, MSFT_FY2025_2025-06-30:90] [MSFT FY2020, Item 1A, MSFT_FY
>
> > [Guardrail Audit Warning]: Manual verification required; 1 sentence(s) are not supported by their cited chunks.

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `MSFT_FY2025_2025-06-30:145` | Item 1C › PART I |  |  | We describe the risks from cybersecurity threats, including previous cybersecurity incidents, in section “Risk Factors” (Part I, Item 1A of this Form 10-K). As of the date of this Form 10-K, we do not believe any risks f… |
| 2 | `MSFT_FY2025_2025-06-30:84` | Item 1A › Security of our information technology | ✓ | #1, #3, #4 | Threats to security can take a variety of forms. Threat actors, including individual and groups of hackers and sophisticated organizations, including nation-states, state-sponsored organizations, or cybercriminal groups,… |
| 3 | `MSFT_FY2025_2025-06-30:147` | Item 1C › PART I |  |  | Our CISO leads the strategy, engineering, and operations of cybersecurity across the company, and reports to the EVP of Cloud + AI. Our CISO has extensive experience assessing and managing cybersecurity programs and cybe… |
| 4 | `MSFT_FY2025_2025-06-30:143` | Item 1C › PART I |  |  | When appropriate, we utilize external service providers to assess, test, or otherwise assist our program. We also leverage third parties by working with external researchers, operating bug bounty programs, and managing c… |
| 5 | `MSFT_FY2025_2025-06-30:146` | Item 1C › PART I |  |  | Our Board of Directors oversees cybersecurity risk. Cybersecurity reviews by the Board are scheduled to occur at least quarterly, or more frequently as determined to be necessary or advisable. Presentations to the Board … |
| 6 | `MSFT_FY2025_2025-06-30:141` | Item 1C |  |  | Our computing environments, products, and services are reviewed by our internal audit teams as well as independent third-party assessors. We are committed to managing the most significant risks to our strategies and ambi… |
| 7 | `MSFT_FY2025_2025-06-30:86` | Item 1A › Security of our information technology | ✓ | #1, #5 | or expose us to legal or regulatory risk. Inadequate account security or organizational security practices, including those of companies we have acquired or those of the third parties we utilize, have resulted and may re… |
| 8 | `MSFT_FY2025_2025-06-30:91` | Item 1A › Security of our products, services, devices, and customers’ data |  |  | our cloud services as customers embrace digital transformation. Adversaries that acquire user account information can use that information to compromise our users’ accounts, including where accounts share the same attrib… |
| 9 | `MSFT_FY2020_2020-06-30:104` | Item 1A › Security of our products, services, devices, and customers’ data | ✓ |  | The security of our products and services is important in our customers’ decisions to purchase or use our products or services. Security threats are a significant challenge to companies like us whose business is providin… |
| 10 | `MSFT_FY2025_2025-06-30:90` | Item 1A › Security of our products, services, devices, and customers’ data | ✓ |  | The security of our products and services is important in our customers’ decisions to purchase or use our products or services across cloud and on-premises environments. Security threats are a significant challenge to co… |
| 11 | `MSFT_FY2020_2020-06-30:101` | Item 1A › Security of our information technology | ✓ | #3 | Threats to IT security can take a variety of forms. Individual and groups of hackers and sophisticated organizations, including state-sponsored organizations or nation-states, continuously undertake attacks that pose thr… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#2 `MSFT_FY2025_2025-06-30:84`** (cited, gold #1, gold #3, gold #4)

````text
Item 1A > Security of our information technology
Threats to security can take a variety of forms. Threat actors, including individual and groups of hackers and sophisticated organizations, including nation-states, state-sponsored organizations, or cybercriminal groups, continuously undertake attacks that pose threats to our customers and our internal infrastructure, and we have experienced cybersecurity incidents in which such actors have gained unauthorized access to our systems and data, including customer systems and data. These actors use a wide variety of methods, which include developing and deploying malicious software; exploiting known and potential vulnerabilities or intentionally designed processes in our or third-party hardware, software, or other infrastructure to attack our products and services or gain access to our networks and datacenters; using social engineering techniques to induce our employees, users, partners, or customers to disclose sensitive information, such as passwords, or take other actions to gain access to our data or our users’ or customers’ data; or acting in a coordinated manner or conducting coordinated attacks. For example, as previously disclosed in our Form 8-K filed with the Securities and Exchange Commission on January 19, 2024 and amended on March 8, 2024, beginning in late November 2023, a nation-state associated threat actor used a password spray attack to compromise a
````

**#7 `MSFT_FY2025_2025-06-30:86`** (cited, gold #1, gold #5)

````text
Item 1A > Security of our information technology
or expose us to legal or regulatory risk. Inadequate account security or organizational security practices, including those of companies we have acquired or those of the third parties we utilize, have resulted and may result in unauthorized access to our systems and data, including customer systems and data. For example, passwords may not be rotated and employee access may not be updated or removed on a timely basis. Employees or third parties may intentionally compromise our or our users’ security or systems or reveal confidential information, and laws in foreign jurisdictions may compel actions by such parties against our interests and could limit our recourse. Malicious actors may employ the supply chain to introduce malware through software updates or compromised supplier accounts or hardware.
````

**#9 `MSFT_FY2020_2020-06-30:104`** (cited)

````text
Item 1A > Security of our products, services, devices, and customers’ data
The security of our products and services is important in our customers’ decisions to purchase or use our products or services. Security threats are a significant challenge to companies like us whose business is providing technology products and services to others. Threats to our own IT infrastructure can also affect our customers. Customers using our cloud-based services rely on the security of our infrastructure, including hardware and other elements provided by third parties, to ensure the reliability of our services and the protection of their data. Adversaries tend to focus their efforts on the most popular operating systems, programs, and services, including many of ours, and we expect that to continue. Adversaries that acquire user account information at other companies can use that information to compromise our users’ accounts where accounts share the same attributes as passwords. Inadequate account security practices may also result in unauthorized access. User activity may also result in ransomware or other malicious software impacting a customer’s use of our products or services. We are also increasingly incorporating open source software into our products. There may be vulnerabilities in open source software that may make our products susceptible to cyberattacks.
````

**#10 `MSFT_FY2025_2025-06-30:90`** (cited)

````text
Item 1A > Security of our products, services, devices, and customers’ data
The security of our products and services is important in our customers’ decisions to purchase or use our products or services across cloud and on-premises environments. Security threats are a significant challenge to companies like us, whose business is providing technology products and services to others. Threats to or attacks on our own infrastructure, such as the nation-state attack described in the prior risk factor, have also affected our customers and may do so in the future. The reliability of our cloud-based services and the protection of customer data depend on the security of our infrastructure, which includes hardware and other elements provided by third parties. Adversaries tend to focus their efforts on the most popular operating systems, programs, and services, including many of ours, as well as customers with sensitive data, and we expect that to continue. In addition, adversaries can attack our customers’ on-premises or cloud environments, sometimes exploiting previously unknown (“zero-day”) vulnerabilities. Product vulnerabilities can persist even after we have issued security patches if customers have not installed the most recent updates, or if the attackers exploited the vulnerabilities before patching to install additional malware to further compromise customers’ systems. Adversaries will continue to attack customers using
````

**#11 `MSFT_FY2020_2020-06-30:101`** (cited, gold #3)

````text
Item 1A > Security of our information technology
Threats to IT security can take a variety of forms. Individual and groups of hackers and sophisticated organizations, including state-sponsored organizations or nation-states, continuously undertake attacks that pose threats to our customers and our IT. These actors may use a wide variety of methods, which may include developing and deploying malicious software or exploiting vulnerabilities in hardware, software, or other infrastructure in order to attack our products and services or gain access to our networks and datacenters, using social engineering techniques to induce our employees, users, partners, or customers to disclose passwords or other sensitive information or take other actions to gain access to our data or our users’ or customers’ data, or acting in a coordinated manner to launch distributed denial of service or other coordinated attacks. Inadequate account security practices may also result in unauthorized access to confidential data. For example, system administrators may fail to timely remove employee account access when no longer appropriate. Employees or third parties may intentionally compromise our or our users’ security or systems, or reveal confidential information.
````

</details>

RQ2 citation match (section level): `cited=[('MSFT', 'Item 1A')] gold=[(None, 'Item 1A')]`

**System C guardrail** (judge `gpt-5.4`): numerical claims 0, verified 0, ungrounded 0, uncited 0, derived 0; sentence verdicts: supported 9, partial 1, unsupported 0, unchecked 0.


<details><summary>Guardrail sentence verdicts</summary>

| sentence | verdict | judge reason |
|---|---|---|
| Between fiscal 2020 and fiscal 2025, Microsoft’s description of threat actors remained broadly similar in identifying individual hackers, groups, sophisticated organizations, state-sponsored organizations, and nation-states as persistent attackers, but the 2025 filing uses more expansive language by referring to “threat actors,” including “cybercriminal groups,” and states that Microsoft has experienced cybersecurity incidents in which such actors gained unauthorized access to its systems and data, including customer systems and data [MSFT FY2020, Item 1A, MSFT_FY2020_2020-06-30:101] [MSFT FY2025, Item 1A, MSFT_FY2025_2025-06-30:84]. | supported | The 2020 and 2025 excerpts show similar actor categories, and 2025 adds 'threat actors,' 'cybercriminal groups,' and disclosed unauthorized access to Microsoft and customer systems/data. |
| In fiscal 2020, Microsoft described threat methods as developing and deploying malicious software, exploiting vulnerabilities in hardware, software, or other infrastructure, using social engineering to induce disclosure of passwords or other sensitive information, and launching distributed denial of service or other coordinated attacks [MSFT FY2020, Item 1A, MSFT_FY2020_2020-06-30:101]. | supported | The 2020 excerpt explicitly lists malicious software, exploiting vulnerabilities, social engineering for passwords or sensitive information, and DDoS or other coordinated attacks. |
| In fiscal 2025, Microsoft expanded this description to include exploiting “known and potential vulnerabilities or intentionally designed processes” in Microsoft or third-party hardware, software, or other infrastructure, attacking products and services or gaining access to networks and datacenters, using social engineering against employees, users, partners, or customers, and acting in a coordinated manner or conducting coordinated attacks [MSFT FY2025, Item 1A, MSFT_FY2025_2025-06-30:84]. | supported | The 2025 excerpt expressly includes exploiting known and potential vulnerabilities or intentionally designed processes, attacks on products/services or networks/datacenters, social engineering, and coordinated attacks. |
| The 2025 filing also adds a specific disclosed example of a nation-state associated threat actor using a password spray attack beginning in late November 2023, which is a concrete attack vector not described in the 2020 filing [MSFT FY2025, Item 1A, MSFT_FY2025_2025-06-30:84] [MSFT FY2020, Item 1A, MSFT_FY2020_2020-06-30:101]. | supported | The 2025 excerpt gives the late-November 2023 password spray example, and the 2020 excerpt does not mention that concrete attack vector. |
| For internal information technology risks, the 2020 filing said inadequate account security practices could result in unauthorized access to confidential data and gave the example that system administrators may fail to timely remove employee account access when no longer appropriate [MSFT FY2020, Item 1A, MSFT_FY2020_2020-06-30:101]. | supported | The 2020 excerpt states inadequate account security practices may cause unauthorized access and gives the example of failing to timely remove employee access. |
| In 2025, Microsoft broadened this discussion by stating that inadequate account security or organizational security practices, including those of acquired companies or third parties it uses, have resulted and may result in unauthorized access to its systems and data, including customer systems and data, and it added examples such as passwords not being rotated and employee access not being updated or removed on a timely basis [MSFT FY2025, Item 1A, MSFT_FY2025_2025-06-30:86]. | supported | The 2025 excerpt states inadequate account or organizational security practices, including at acquired companies or third parties, have resulted and may result in unauthorized access, with examples of password rotation and delayed access updates/removals. |
| The 2025 filing further expands the threat-vector discussion by adding supply-chain risk, stating that malicious actors may employ the supply chain to introduce malware through software updates or compromised supplier accounts or hardware, which was not described in the 2020 filing [MSFT FY2025, Item 1A, MSFT_FY2025_2025-06-30:86] [MSFT FY2020, Item 1A, MSFT_FY2020_2020-06-30:101]. | supported | The 2025 excerpt adds supply-chain malware via software updates or compromised supplier accounts or hardware, and the 2020 excerpt does not describe that risk. |
| For product and customer security, the 2020 filing emphasized that customers using cloud-based services rely on the security of Microsoft’s infrastructure, including hardware and other elements provided by third parties, and that adversaries who acquire user account information at other companies can compromise Microsoft users’ accounts where accounts share the same attributes as passwords [MSFT FY2020, Item 1A, MSFT_FY2020_2020-06-30:104]. | supported | The 2020 excerpt says cloud customers rely on Microsoft infrastructure including third-party hardware/elements and that stolen account information from other companies can compromise Microsoft users' accounts where attributes such as passwords are shared. |
| In 2025, Microsoft broadened this to cover both cloud and on-premises environments, stated that threats to or attacks on its own infrastructure, such as the nation-state attack described in the prior risk factor, have also affected customers and may do so in the future, and added that adversaries can attack customers’ on-premises or cloud environments, sometimes exploiting previously unknown “zero-day” vulnerabilities [MSFT FY2025, Item 1A, MSFT_FY2025_2025-06-30:90]. | supported | The 2025 excerpt explicitly covers cloud and on-premises environments, says attacks on Microsoft infrastructure have affected customers, and mentions attacks exploiting zero-day vulnerabilities. |
| The 2025 filing also adds more detail on persistence and post-patch risk by stating that product vulnerabilities can persist even after security patches have been issued if customers have not installed the most recent updates, or if attackers exploited the vulnerabilities before patching to install additional malware to further compromise customers’ systems, which is not described in the 2020 filing [MSFT FY2025, Item 1A, MSFT_FY2025_2025-06-30:90] [MSFT FY2020, Item 1A, MSFT_FY | partial | The 2025 excerpt supports the post-patch persistence detail, but no 2020 evidence is provided here to support the claim that this was not described in the 2020 filing. |

</details>

### System C v2 (agentic multi-hop + XBRL)

Model: `gpt-5.4`. Hops: 3. Chunks retrieved: 12, cited: 6.

**Generated answer**

> Between fiscal year 2020 and fiscal year 2025, Microsoft’s risk disclosure evolved from a more general description of cybersecurity threats to a more detailed discussion of specific attack methods, affected environments, customer-environment constraints, and the consequences of limited visibility into customer systems. [MSFT FY2020, Item 1A, MSFT_FY2020_2020-06-30:104] [MSFT FY2025, Item 1A, MSFT_FY2025_2025-06-30:90] [MSFT FY2025, Item 1A, MSFT_FY2025_2025-06-30:91] [MSFT FY2025, Item 1A, MSFT_FY2025_2025-06-30:92] [MSFT FY2025, Item 1A, MSFT_FY2025_2025-06-30:93]
>
> In fiscal year 2020, Microsoft described security threats as a significant challenge for a technology provider and said threats to its own IT infrastructure could affect customers. [MSFT FY2020, Item 1A, MSFT_FY2020_2020-06-30:104] It emphasized that customers using cloud-based services relied on the security of Microsoft’s infrastructure, including third-party hardware and other elements, to ensure service reliability and data protection. [MSFT FY2020, Item 1A, MSFT_FY2020_2020-06-30:104] It also identified several specific threat vectors: adversaries targeting popular operating systems, programs, and services; attackers using account information obtained at other companies to compromise Microsoft users’ accounts where passwords or other attributes were shared; inadequate account security practices leading to unauthorized access; user activity causing ransomware or other malicious software impacts; and vulnerabilities in open source software incorporated into Microsoft products. [MSFT FY2020, Item 1A, MSFT_FY2020_2020-06-30:104] In a related 2020 disclosure, Microsoft said it needed to continuously engineer more secure products and services, improve software update deployment, develop mitigation technologies for situations where updates were not deployed, maintain digital security infrastructure, and provide security tools and information to customers. [MSFT FY2020, Item 1A, MSFT_FY2020_2020-06-30:105]
>
> In fiscal year 2025, Microsoft retained many of those themes but expanded them materially. [MSFT FY2025, Item 1A, MSFT_FY2025_2025-06-30:90] [MSFT FY2025, Item 1A, MSFT_FY2025_2025-06-30:91] It stated that security is important to customer purchasing and usage decisions across both cloud and on-premises environments, rather than focusing only on cloud-based services. [MSFT FY2025, Item 1A, MSFT_FY2025_2025-06-30:90] It also expressly said that threats to or attacks on Microsoft’s own infrastructure, such as the nation-state attack described in the prior risk factor, have affected customers and may do so in the future. [MSFT FY2025, Item 1A, MSFT_FY2025_2025-06-30:90] Microsoft further disclosed that adversaries target not only popular operating systems, programs, and services, but also customers with sensitive data. [MSFT FY2025, Item 1A, MSFT_FY2025_2025-06-30:90]
>
> The 2025 filing added several more specific threat vectors. [MSFT FY2025, Item 1A, MSFT_FY2025_2025-06-30:90] [MSFT FY2025, Item 1A, MSFT_FY2025_2025-06-30:91] These included attacks on customers’ on-premises or cloud environments, exploitation of previously unknown “zero-day” vulnerabilities, persistence of product vulnerabilities even after security patches are issued when customers have not installed updates, and attackers exploiting vulnerabilities before patching to install additional malware and further compromise customer systems. [MSFT FY2025, Item 1A, MSFT_FY2025_2025-06-30:90] Microsoft also said weaknesses in its development processes can result in vulnerabilities in its products, and that features relying on generative AI can be susceptible to security threats. [MSFT FY2025, Item 1A, MSFT_FY2025_2025-06-30:91] In addition, it highlighted customer-environment complexity as a risk factor, noting that customers operate complex systems with third-party hardware and software from multiple vendors, may continue using systems and products that no longer incorporate the strongest current security advances or standards, and may have limited capabilities and resources to adopt state-of-the-art cybersecurity practices.

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `MSFT_FY2025_2025-06-30:145` | Item 1C › PART I |  |  | We describe the risks from cybersecurity threats, including previous cybersecurity incidents, in section “Risk Factors” (Part I, Item 1A of this Form 10-K). As of the date of this Form 10-K, we do not believe any risks f… |
| 2 | `MSFT_FY2025_2025-06-30:84` | Item 1A › Security of our information technology |  | #1, #3, #4 | Threats to security can take a variety of forms. Threat actors, including individual and groups of hackers and sophisticated organizations, including nation-states, state-sponsored organizations, or cybercriminal groups,… |
| 3 | `MSFT_FY2025_2025-06-30:147` | Item 1C › PART I |  |  | Our CISO leads the strategy, engineering, and operations of cybersecurity across the company, and reports to the EVP of Cloud + AI. Our CISO has extensive experience assessing and managing cybersecurity programs and cybe… |
| 4 | `MSFT_FY2025_2025-06-30:143` | Item 1C › PART I |  |  | When appropriate, we utilize external service providers to assess, test, or otherwise assist our program. We also leverage third parties by working with external researchers, operating bug bounty programs, and managing c… |
| 5 | `MSFT_FY2025_2025-06-30:146` | Item 1C › PART I |  |  | Our Board of Directors oversees cybersecurity risk. Cybersecurity reviews by the Board are scheduled to occur at least quarterly, or more frequently as determined to be necessary or advisable. Presentations to the Board … |
| 6 | `MSFT_FY2025_2025-06-30:141` | Item 1C |  |  | Our computing environments, products, and services are reviewed by our internal audit teams as well as independent third-party assessors. We are committed to managing the most significant risks to our strategies and ambi… |
| 7 | `MSFT_FY2020_2020-06-30:104` | Item 1A › Security of our products, services, devices, and customers’ data | ✓ |  | The security of our products and services is important in our customers’ decisions to purchase or use our products or services. Security threats are a significant challenge to companies like us whose business is providin… |
| 8 | `MSFT_FY2025_2025-06-30:90` | Item 1A › Security of our products, services, devices, and customers’ data | ✓ |  | The security of our products and services is important in our customers’ decisions to purchase or use our products or services across cloud and on-premises environments. Security threats are a significant challenge to co… |
| 9 | `MSFT_FY2025_2025-06-30:93` | Item 1A › Security of our products, services, devices, and customers’ data | ✓ |  | Cyberattacks could adversely impact our customers even if our production services are not directly compromised. We are committed to notifying our customers whose systems have been impacted as we become aware and have act… |
| 10 | `MSFT_FY2025_2025-06-30:92` | Item 1A › Security of our products, services, devices, and customers’ data | ✓ |  | Our customers operate complex systems with third-party hardware and software from multiple vendors that may include systems acquired over many years. They expect our products and services to support all these systems and… |
| 11 | `MSFT_FY2025_2025-06-30:91` | Item 1A › Security of our products, services, devices, and customers’ data | ✓ |  | our cloud services as customers embrace digital transformation. Adversaries that acquire user account information can use that information to compromise our users’ accounts, including where accounts share the same attrib… |
| 12 | `MSFT_FY2020_2020-06-30:105` | Item 1A › Security of our products, services, devices, and customers’ data | ✓ |  | To defend against security threats to our internal IT systems, our cloud-based services, and our customers’ systems, we must continuously engineer more secure products and services, enhance security and reliability featu… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#2 `MSFT_FY2025_2025-06-30:84`** (gold #1, gold #3, gold #4)

````text
Item 1A > Security of our information technology
Threats to security can take a variety of forms. Threat actors, including individual and groups of hackers and sophisticated organizations, including nation-states, state-sponsored organizations, or cybercriminal groups, continuously undertake attacks that pose threats to our customers and our internal infrastructure, and we have experienced cybersecurity incidents in which such actors have gained unauthorized access to our systems and data, including customer systems and data. These actors use a wide variety of methods, which include developing and deploying malicious software; exploiting known and potential vulnerabilities or intentionally designed processes in our or third-party hardware, software, or other infrastructure to attack our products and services or gain access to our networks and datacenters; using social engineering techniques to induce our employees, users, partners, or customers to disclose sensitive information, such as passwords, or take other actions to gain access to our data or our users’ or customers’ data; or acting in a coordinated manner or conducting coordinated attacks. For example, as previously disclosed in our Form 8-K filed with the Securities and Exchange Commission on January 19, 2024 and amended on March 8, 2024, beginning in late November 2023, a nation-state associated threat actor used a password spray attack to compromise a
````

**#7 `MSFT_FY2020_2020-06-30:104`** (cited)

````text
Item 1A > Security of our products, services, devices, and customers’ data
The security of our products and services is important in our customers’ decisions to purchase or use our products or services. Security threats are a significant challenge to companies like us whose business is providing technology products and services to others. Threats to our own IT infrastructure can also affect our customers. Customers using our cloud-based services rely on the security of our infrastructure, including hardware and other elements provided by third parties, to ensure the reliability of our services and the protection of their data. Adversaries tend to focus their efforts on the most popular operating systems, programs, and services, including many of ours, and we expect that to continue. Adversaries that acquire user account information at other companies can use that information to compromise our users’ accounts where accounts share the same attributes as passwords. Inadequate account security practices may also result in unauthorized access. User activity may also result in ransomware or other malicious software impacting a customer’s use of our products or services. We are also increasingly incorporating open source software into our products. There may be vulnerabilities in open source software that may make our products susceptible to cyberattacks.
````

**#8 `MSFT_FY2025_2025-06-30:90`** (cited)

````text
Item 1A > Security of our products, services, devices, and customers’ data
The security of our products and services is important in our customers’ decisions to purchase or use our products or services across cloud and on-premises environments. Security threats are a significant challenge to companies like us, whose business is providing technology products and services to others. Threats to or attacks on our own infrastructure, such as the nation-state attack described in the prior risk factor, have also affected our customers and may do so in the future. The reliability of our cloud-based services and the protection of customer data depend on the security of our infrastructure, which includes hardware and other elements provided by third parties. Adversaries tend to focus their efforts on the most popular operating systems, programs, and services, including many of ours, as well as customers with sensitive data, and we expect that to continue. In addition, adversaries can attack our customers’ on-premises or cloud environments, sometimes exploiting previously unknown (“zero-day”) vulnerabilities. Product vulnerabilities can persist even after we have issued security patches if customers have not installed the most recent updates, or if the attackers exploited the vulnerabilities before patching to install additional malware to further compromise customers’ systems. Adversaries will continue to attack customers using
````

**#9 `MSFT_FY2025_2025-06-30:93`** (cited)

````text
Item 1A > Security of our products, services, devices, and customers’ data
Cyberattacks could adversely impact our customers even if our production services are not directly compromised. We are committed to notifying our customers whose systems have been impacted as we become aware and have actionable information for customers to help protect themselves. We are also committed to providing guidance and support on detection, tracking, and remediation. We may not be able to detect the existence or extent of these attacks for all of our customers or have information on how to detect or track an attack, especially where an attack involves on-premises software such as Exchange Server where we may have no or limited visibility into our customers’ computing environments. Any of the foregoing events could result in reputational harm, loss of revenue, increased costs, or otherwise adversely affect our business, financial condition, and results of operations.
````

**#10 `MSFT_FY2025_2025-06-30:92`** (cited)

````text
Item 1A > Security of our products, services, devices, and customers’ data
Our customers operate complex systems with third-party hardware and software from multiple vendors that may include systems acquired over many years. They expect our products and services to support all these systems and products, including those that no longer incorporate the strongest current security advances or standards. As a result, we may not be able to discontinue support in our services for a product, service, standard, or feature solely because a more secure alternative is available. Failure to utilize the most current security advances and standards can increase our customers’ vulnerability to attack. Further, customers of widely varied sizes and technical sophistication use our technology, and consequently may still have limited capabilities and resources to help them adopt and implement state-of-the-art cybersecurity practices and technologies. In addition, we must account for this wide variation of technical sophistication when defining default settings for our products and services, including security default settings, as these settings may limit or otherwise impact other aspects of operations and some customers may have limited capability to review and reset these defaults.
````

**#11 `MSFT_FY2025_2025-06-30:91`** (cited)

````text
Item 1A > Security of our products, services, devices, and customers’ data
our cloud services as customers embrace digital transformation. Adversaries that acquire user account information can use that information to compromise our users’ accounts, including where accounts share the same attributes such as passwords. Inadequate account security practices may also result in unauthorized access, and user activity may result in ransomware or other malicious software impacting a customer’s use of our products or services. Weaknesses in our development processes can result in vulnerabilities in our products. Open source software can also contain vulnerabilities that may make our products susceptible to cyberattacks as we increasingly incorporate open source software into our products. Additionally, features that rely on generative AI can be susceptible to security threats.
````

**#12 `MSFT_FY2020_2020-06-30:105`** (cited)

````text
Item 1A > Security of our products, services, devices, and customers’ data
To defend against security threats to our internal IT systems, our cloud-based services, and our customers’ systems, we must continuously engineer more secure products and services, enhance security and reliability features, improve the deployment of software updates to address security vulnerabilities in our own products as well as those provided by others, develop mitigation technologies that help to secure customers from attacks even when software updates are not deployed, maintain the digital security infrastructure that protects the integrity of our network, products, and services, and provide security tools such as firewalls and anti-virus software and information about the need to deploy security measures and the impact of doing so. Customers in certain industries such as financial services, health care, and government may have enhanced or specialized requirements to which we must engineer our product and services.
````

</details>

RQ2 citation match (section level): `cited=[('MSFT', 'Item 1A')] gold=[(None, 'Item 1A')]`

**System C guardrail** (judge `gpt-5.4`): numerical claims 0, verified 0, ungrounded 0, uncited 0, derived 0; sentence verdicts: supported 13, partial 0, unsupported 0, unchecked 0.


<details><summary>Guardrail sentence verdicts</summary>

| sentence | verdict | judge reason |
|---|---|---|
| Between fiscal year 2020 and fiscal year 2025, Microsoft’s risk disclosure evolved from a more general description of cybersecurity threats to a more detailed discussion of specific attack methods, affected environments, customer-environment constraints, and the consequences of limited visibility into customer systems. [MSFT FY2020, Item 1A, MSFT_FY2020_2020-06-30:104] [MSFT FY2025, Item 1A, MSFT_FY2025_2025-06-30:90] [MSFT FY2025, Item 1A, MSFT_FY2025_2025-06-30:91] [MSFT FY2025, Item 1A, MSFT_FY2025_2025-06-30:92] [MSFT FY2025, Item 1A, MSFT_FY2025_2025-06-30:93] | supported | The 2020 text is more general, while the 2025 text adds specific attack methods, environments, customer constraints, and limited-visibility consequences. |
| In fiscal year 2020, Microsoft described security threats as a significant challenge for a technology provider and said threats to its own IT infrastructure could affect customers. [MSFT FY2020, Item 1A, MSFT_FY2020_2020-06-30:104] | supported | The cited 2020 passage states both that security threats are a significant challenge and that threats to Microsoft's IT infrastructure can affect customers. |
| It emphasized that customers using cloud-based services relied on the security of Microsoft’s infrastructure, including third-party hardware and other elements, to ensure service reliability and data protection. [MSFT FY2020, Item 1A, MSFT_FY2020_2020-06-30:104] | supported | The 2020 evidence expressly says cloud customers rely on Microsoft's infrastructure, including third-party elements, for reliability and data protection. |
| It also identified several specific threat vectors: adversaries targeting popular operating systems, programs, and services; attackers using account information obtained at other companies to compromise Microsoft users’ accounts where passwords or other attributes were shared; inadequate account security practices leading to unauthorized access; user activity causing ransomware or other malicious software impacts; and vulnerabilities in open source software incorporated into Microsoft products. [MSFT FY2020, Item 1A, MSFT_FY2020_2020-06-30:104] | supported | Each listed threat vector appears in the 2020 cited passage. |
| In a related 2020 disclosure, Microsoft said it needed to continuously engineer more secure products and services, improve software update deployment, develop mitigation technologies for situations where updates were not deployed, maintain digital security infrastructure, and provide security tools and information to customers. [MSFT FY2020, Item 1A, MSFT_FY2020_2020-06-30:105] | supported | The 2020 cited passage explicitly lists all of those required security actions and customer support measures. |
| In fiscal year 2025, Microsoft retained many of those themes but expanded them materially. [MSFT FY2025, Item 1A, MSFT_FY2025_2025-06-30:90] [MSFT FY2025, Item 1A, MSFT_FY2025_2025-06-30:91] | supported | The 2025 text repeats prior themes and adds materially more detail on environments, zero-days, patching, development weaknesses, and generative AI. |
| It stated that security is important to customer purchasing and usage decisions across both cloud and on-premises environments, rather than focusing only on cloud-based services. [MSFT FY2025, Item 1A, MSFT_FY2025_2025-06-30:90] | supported | The 2025 passage explicitly says security matters across cloud and on-premises environments. |
| It also expressly said that threats to or attacks on Microsoft’s own infrastructure, such as the nation-state attack described in the prior risk factor, have affected customers and may do so in the future. [MSFT FY2025, Item 1A, MSFT_FY2025_2025-06-30:90] | supported | The cited 2025 text expressly states that threats to or attacks on Microsoft's infrastructure, including the nation-state attack, have affected customers and may do so again. |
| Microsoft further disclosed that adversaries target not only popular operating systems, programs, and services, but also customers with sensitive data. [MSFT FY2025, Item 1A, MSFT_FY2025_2025-06-30:90] | supported | The 2025 evidence says adversaries focus on popular systems and services as well as customers with sensitive data. |
| The 2025 filing added several more specific threat vectors. [MSFT FY2025, Item 1A, MSFT_FY2025_2025-06-30:90] [MSFT FY2025, Item 1A, MSFT_FY2025_2025-06-30:91] | supported | The 2025 cited passages add several specific threat vectors beyond the more general earlier discussion. |
| These included attacks on customers’ on-premises or cloud environments, exploitation of previously unknown “zero-day” vulnerabilities, persistence of product vulnerabilities even after security patches are issued when customers have not installed updates, and attackers exploiting vulnerabilities before patching to install additional malware and further compromise customer systems. [MSFT FY2025, Item 1A, MSFT_FY2025_2025-06-30:90] | supported | The cited 2025 passage explicitly describes all four listed attack and patching scenarios. |
| Microsoft also said weaknesses in its development processes can result in vulnerabilities in its products, and that features relying on generative AI can be susceptible to security threats. [MSFT FY2025, Item 1A, MSFT_FY2025_2025-06-30:91] | supported | The 2025 evidence expressly states both development-process weaknesses can create vulnerabilities and generative-AI features can face security threats. |
| In addition, it highlighted customer-environment complexity as a risk factor, noting that customers operate complex systems with third-party hardware and software from multiple vendors, may continue using systems and products that no longer incorporate the strongest current security advances or standards, and may have limited capabilities and resources to adopt state-of-the-art cybersecurity practices. | supported | The retrieved 2025 evidence explicitly describes complex customer environments, older systems lacking current security standards, and limited customer capabilities and resources. |

</details>
