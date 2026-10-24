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
* Detailed Sprint & Gantt: [`docs/context/SPRINT_GANTT.md`](file:///Users/anishdobz/projects/cs614_group8/docs/context/SPRINT_GANTT.md)
* Full Research Hypotheses & Metrics: [`docs/context/RESEARCH_QUESTIONS.md`](file:///Users/anishdobz/projects/cs614_group8/docs/context/RESEARCH_QUESTIONS.md)
* System C Architecture Specification: [`docs/context/SYSTEM_C_SPEC.md`](file:///Users/anishdobz/projects/cs614_group8/docs/context/SYSTEM_C_SPEC.md)
* Course Materials Index: [`docs/context/COURSE_MATERIALS_INDEX.md`](file:///Users/anishdobz/projects/cs614_group8/docs/context/COURSE_MATERIALS_INDEX.md)
* Original Academic Proposal: [`docs/context/CS614_Adaptive_MultiHop_RAG_Proposal.md`](file:///Users/anishdobz/projects/cs614_group8/docs/context/CS614_Adaptive_MultiHop_RAG_Proposal.md)
