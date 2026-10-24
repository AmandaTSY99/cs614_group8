# CS614 Sprint & Gantt Timeline Digest

**Sprint Window:** 18 Oct 2026 – 3 Nov 2026 (Presentation & Submission Day)  
**Team Members:** Anish (Me), Aryan, Amanda, Xavier, Member 5 (Kevin)

---

## 1. Team Allocation & System Ownership

* **Amanda (Lead) & Xavier — Phase 1 Evaluation & System A (Naive Baseline RAG)**:
  * 10-K extraction verification.
  * System A: Single-pass dense Chroma vector retrieval ($k=5$).
  * Baseline recall failure analysis on multi-hop queries.
  * Report ownership: Section 1 (Motivation) & Section 2 (System A Baseline).

* **Xavier & Member 5 (Kevin) — System B (Advanced Single-Pass RAG) & Benchmarking**:
  * Clean `chunks.jsonl` freeze.
  * System B: Sparse BM25 + Dense BGE-m3 hybrid retrieval with Cross-Encoder Reranker (`bge-reranker-large`).
  * Automated RAGAS batch test harness (FinQA/TAT-QA).
  * Report ownership: Section 3 (Ingestion & Preprocessing) & Section 6 (Results, Pareto Curves).

* **Anish (Me) & Aryan — System C (Adaptive Multi-Hop LangGraph System)**:
  * **Anish**: LangGraph execution DAG, Query Decomposer / Planner node, Evidence Sufficiency Critic & Reflection loop ($\le 3$ hops), RQ3 (Inference Economics & Cost).
  * **Aryan**: Conditioned sub-query generator, inline table citation mapping, active hallucination guardrail / self-consistency checks, RQ2 (Factual Faithfulness & Safety).
  * Report ownership: Section 4 (State Machine Arch) & Section 5 (Guardrail Defense).

---

## 2. Key Milestones

* **Checkpoint 0 (Mon, 19 Oct)**: Complete 1-day sanity evaluation of existing 10-K ingested chunks. *(Completed)*
* **Checkpoint 1 (Sun, 25 Oct - Tomorrow!)**: **MILESTONE 1: Team Sync & Go/No-Go**.
  * All 3 RAG systems operational.
  * Demo System C (LangGraph 3-hop loop) + System A & B.
  * Lock slide outline & kick off report drafting.
* **Checkpoint 2 (Thu, 29 Oct)**: Empirical experiments & ablations complete (RQ1, RQ2, RQ3), scorecards generated, report draft 1 ready.
* **Milestone 2 (Tue, 3 Nov)**: **FINAL PRESENTATION & 10-PAGE REPORT SUBMISSION**.

---

## 3. Day-by-Day Sprint Schedule

| Date | Focus | Amanda | Xavier | Anish (Me) | Aryan | Member 5 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **18-19 Oct** | Ingestion & Baseline Setup | Sanity check on parsed 10-Ks | Freeze `chunks.jsonl` | Design LangGraph state & interfaces | Co-design query decomposer prompts | Download FinQA/TAT-QA; RAGAS setup |
| **20-24 Oct** *(Current)* | Core Systems Build Sprint | Build System A (Chroma baseline) | Build System B (BM25 + Reranker) | Build System C (LangGraph, Planner, Critic node) | Build System C (Sub-query gen & citation mapper) | Build System B alpha blender & batch runner |
| **Sun 25 Oct** | **MILESTONE 1: Team Sync** | Demo System A | Demo System B | **Demo System C (State Loop)** | Review traces & lock slide outline | Verify batch harness across systems |
| **26-29 Oct** | Empirical Experiments | Run Sys A suite; draft Sec 1 & 2 | Run Tabular ablation; draft Sec 3 | Run Adaptive vs Fixed 3-Hop ablation; draft Sec 4 | Run Guardrail stress test; draft Sec 5 | Master batch (100 queries); plot Pareto curves; draft Sec 6 |
| **30 Oct - 1 Nov** | Report Assembly & Slides | Edit Sec 1-3; references | Error taxonomy appendix | Integrate 10-pg report draft | Build presentation slides | High-res charts; contribution forms |
| **2-3 Nov** | Rehearsal & Submission | Presentation rehearsal | Repository README & checks | Presentation rehearsal & System C demo | Presentation rehearsal | Final package, submit & present! |
