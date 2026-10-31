# Project Context: CS614 Gen AI with LLMs

**Project Name:** Adaptive Multi-Hop RAG for SEC 10-K Financial Disclosures  
**Repository Path:** `/Users/anishdobz/projects/cs614_group8` (Isolated from OneDrive / iCloud sync)  
**Git Branch:** `feature/system-c-adaptive-rag`  
**Current Date:** 24 Oct 2026 (Day 7 of 16-Day Sprint)  
**Upcoming Milestone:** Milestone 1 — Team Sync & 3-System Demo (Sun, 25 Oct 2026)

---

## 1. System Triad & Comparative Benchmark

We evaluate three distinct architectural alternatives across FinQA/TAT-QA and 50 curated SEC 10-K questions:
1. **System A (Baseline):** Naive single-pass dense retrieval ($k=5$) using Chroma vector store. *(Lead: Amanda)*
2. **System B (Advanced Single-Pass):** Hybrid sparse BM25 + dense BGE-m3 retrieval with Cross-Encoder reranker (`bge-reranker-large`). *(Leads: Xavier & Kevin)*
3. **System C (Proposed Adaptive Multi-Hop):** LangGraph state machine with query decomposition, iterative evidence sufficiency critic loop (up to 3 hops), follow-up sub-query generation, and strict citation guardrails. *(Leads: Anish & Aryan)*

---

## 2. Research Questions Ownership
* **RQ1 (Retrieval Completeness across distant sections):** Xavier & Amanda
* **RQ2 (Factual Faithfulness & Citation Grounding):** Aryan & Kevin
* **RQ3 (Inference Economics, Cost & Pareto Frontier):** **Anish (Lead)**

---

## 3. Reference Pointers & External Links

### Course Lectures & Labs Directory:
All course lectures, weekly Colab notebooks, and evaluation/inference notes live at:  
👉 [`file:///Users/anishdobz/Library/CloudStorage/OneDrive2-SingaporeManagementUniversity/2_smu_pg/4_2_gen_ai_with_llms_cs614`](file:///Users/anishdobz/Library/CloudStorage/OneDrive2-SingaporeManagementUniversity/2_smu_pg/4_2_gen_ai_with_llms_cs614)  
See detailed breakdown in [`docs/context/COURSE_MATERIALS_INDEX.md`](file:///Users/anishdobz/projects/cs614_group8/docs/context/COURSE_MATERIALS_INDEX.md).

### Team SharePoint Directory (STRICT ACCESS POLICY):
* **Local SharePoint Path:**  
  `file:///Users/anishdobz/Library/CloudStorage/OneDrive2-SingaporeManagementUniversity/CS614%20Group%20Project%20-%20General`
* **Team Proposals & Files:**  
  `file:///Users/anishdobz/Library/CloudStorage/OneDrive2-SingaporeManagementUniversity/CS614%20Group%20Project%20-%20General/Proposal`

> [!CAUTION]
> **STRICT REPOSITORY POLICY:**  
> **NEVER** write, copy, paste, modify, or delete any files in the Team SharePoint directory (`CS614 Group Project - General`) unless **explicitly commanded by the user**. All project development, code, scripts, tests, and active drafts must reside purely inside `/Users/anishdobz/projects/cs614_group8`.

---

## 4. Key Reference Docs in This Repo
* System C Architecture (v1.0 Mermaid State Graph): [`ARCHITECTURE.md`](file:///Users/anishdobz/projects/cs614_group8/ARCHITECTURE.md)
* Milestone 1 Demo Guide & Speaking Script: [`reports/MILESTONE1_DEMO_SCRIPT.md`](file:///Users/anishdobz/projects/cs614_group8/reports/MILESTONE1_DEMO_SCRIPT.md)
* Aryan Integration & Handoff Guide: [`ARYAN_HANDOFF.md`](file:///Users/anishdobz/projects/cs614_group8/ARYAN_HANDOFF.md)
* Active Task Checklist: [`ACTIVE_TASK.md`](file:///Users/anishdobz/projects/cs614_group8/ACTIVE_TASK.md)
* Detailed Sprint & Gantt: [`docs/context/SPRINT_GANTT.md`](file:///Users/anishdobz/projects/cs614_group8/docs/context/SPRINT_GANTT.md)
* Full Research Hypotheses & Metrics: [`docs/context/RESEARCH_QUESTIONS.md`](file:///Users/anishdobz/projects/cs614_group8/docs/context/RESEARCH_QUESTIONS.md)
* Original Academic Proposal: [`docs/context/CS614_Adaptive_MultiHop_RAG_Proposal.md`](file:///Users/anishdobz/projects/cs614_group8/docs/context/CS614_Adaptive_MultiHop_RAG_Proposal.md)
* Course Materials Index: [`docs/context/COURSE_MATERIALS_INDEX.md`](file:///Users/anishdobz/projects/cs614_group8/docs/context/COURSE_MATERIALS_INDEX.md)

---

## 5. Milestone 1 Verified Artifacts & Reports
* **Live Demo Runner:** [`scripts/demo_milestone1_system_c.py`](file:///Users/anishdobz/projects/cs614_group8/scripts/demo_milestone1_system_c.py) (Single-hop early-stopping, MD&A + Footnotes multi-hop, XBRL tabular comparison)
* **RQ3 Ablation Harness:** [`scripts/run_rq3_ablation.py`](file:///Users/anishdobz/projects/cs614_group8/scripts/run_rq3_ablation.py) (Fixed 1-Hop vs. Fixed 3-Hop vs. Adaptive v1 vs. Agentic v2)
* **Pareto Frontier Plotter:** [`scripts/plot_rq3_pareto.py`](file:///Users/anishdobz/projects/cs614_group8/scripts/plot_rq3_pareto.py)
* **Generated Figures:** [`reports/figures/`](file:///Users/anishdobz/projects/cs614_group8/reports/figures) (`rq3_executive_dashboard.png`, `rq3_pareto_frontier.png`, `rq3_latency_breakdown.png`, `rq3_hop_distribution.png`)
* **Unit Tests:** `pytest tests/test_system_c.py -v` (9/9 passing in 0.86s)

---

## 6. Docker & Containerized Deployment Protocol
The project repository is containerized via `Dockerfile` and `docker-compose.yaml`:
* **Jupyter Lab Service:** `docker compose up jupyter` (serves port 8888 with local data volume)
* **System C Demo Execution:** `docker compose run --rm system-c python scripts/demo_milestone1_system_c.py --mock`
* **Unit Tests via Docker:** `docker compose run --rm system-c pytest tests/test_system_c.py -v`
* **Host Ollama Connectivity:** Configured with `host.docker.internal:host-gateway` and `OLLAMA_HOST=http://host.docker.internal:11434` for seamless local LLM inference from inside containers.

---

## 7. Critical Architectural Insights: System C v1 vs. v2 Trade-offs
* Full Analysis Document: [`docs/context/ARCHITECTURAL_INSIGHTS_V1_VS_V2.md`](file:///Users/anishdobz/projects/cs614_group8/docs/context/ARCHITECTURAL_INSIGHTS_V1_VS_V2.md)
* **The 10-K Lookback Barrier:** SEC 10-K balance sheets only report the prior 2 years. Questions spanning >2 years (e.g. FY21 vs FY25 in `gold-066`) cause text RAG (v1) to fail across all 3 hops. System C v2 solves this in 1 hop by querying continuous multi-year XBRL time-series data.
* **The Premature Sufficiency Trade-off:** High-level XBRL tables in v2 occasionally trick the Sufficiency Critic into stopping at Hop 1, missing deep footnote line items (e.g., segment revenues, debt maturity schedules) that v1 retrieved by being forced into Hops 2 and 3. Overall 97-question accuracy: System C v1 = 89.66%, System C v2 = 82.76%, but v2 delivers 36.7% faster median latency ($13.6\text{s}$ vs $21.4\text{s}$) and 13.8% lower cost.
