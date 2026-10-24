# CS614 Case Study Proposal: Adaptive Multi-Hop RAG for Financial Disclosures & SEC 10-K Filings

## 1. Executive Summary & Project Identification
- **Project Title:** *Adaptive Multi-Hop RAG: Iterative Evidence Retrieval and Verification over Complex SEC 10-K Financial Disclosures*
- **Project Archetype:** Dual **System-Type Prototype + Empirical Comparative Study**
- **Domain:** Corporate Financial Reporting & Equity Research (SEC 10-K filings, annual reports, earnings call transcripts)
- **Target Audience:** Financial research analysts, auditors, due diligence teams who need cross-statement, multi-year, and footnoted evidence syntheses.

---

## 2. Problem Statement & Motivation
### Why Naive / Single-Pass RAG Fails in Finance:
1. **Scattered Evidence (Cross-Document / Cross-Section):** Complex financial queries (e.g., *"Did the increase in gross margin in 2024 offset the foreign exchange headwinds discussed in Item 7A, and how did credit facility covenants restrict their response?"*) require synthesizing disconnected sections: Item 8 (Financial Statements), Item 7 (MD&A), Item 7A (Quantitative Market Risk Disclosures), and Debt Footnotes.
2. **Dense Tabular + Textual Heterogeneity:** Financial tables lose row/column context when parsed by standard fixed-size chunkers, leading to misaligned intermediate facts.
3. **Information Gaps & Hallucinations:** Single-pass retrieval fetches top-\(k\) chunks based on surface similarity to the broad query. If Step 1 retrieval misses an entity or prerequisite definition (e.g., specific debt maturity date), the generator hallucinates or outputs an incomplete answer without attempting follow-up retrieval.

---

## 3. Technical Architecture & System Design

```
                     ┌───────────────────────────────┐
                     │          User Query           │
                     └───────────────┬───────────────┘
                                     │
                                     ▼
                     ┌───────────────────────────────┐
                     │   Query Decomposer & Planner  │  ◄── (LLM Sub-goal planning)
                     └───────────────┬───────────────┘
                                     │
                ┌────────────────────┴────────────────────┐
                ▼                                         ▼
   [Hop 1: Entity / Definition Retrieval]    [Hop 2: Target Metric / Statement Retrieval]
                │                                         │
                └────────────────────┬────────────────────┘
                                     │
                                     ▼
                     ┌───────────────────────────────┐
                     │       Hybrid Retriever        │
                     │  (Dense BGE-m3 + Sparse BM25) │
                     └───────────────┬───────────────┘
                                     │
                                     ▼
                     ┌───────────────────────────────┐
                     │    Cross-Encoder Reranker     │  (e.g., bge-reranker-large)
                     │        Top-5 Chunks           │
                     └───────────────┬───────────────┘
                                     │
                                     ▼
                     ┌───────────────────────────────┐
                     │  Evidence Sufficiency Critic  │
                     │     (Self-RAG / Adaptive)     │
                     └───────────────┬───────────────┘
                                     │
                    ┌────────────────┴────────────────┐
          [Gaps Detected & Hop < Max]            [Evidence Sufficient]
                    │                                         │
                    ▼                                         ▼
         ┌─────────────────────┐                   ┌─────────────────────┐
         │ Follow-up Sub-query │                   │ Answer Synthesizer  │
         │     Generator       │                   │ + Precise Citations │
         └──────────┬──────────┘                   └──────────┬──────────┘
                    │                                         │
                    └───────────► (Loop back)                 ▼
                                                   ┌─────────────────────┐
                                                   │ Faithfulness Guard  │
                                                   │ (Hallucination Cut) │
                                                   └─────────────────────┘
```

### Core Components:
1. **Document Processing & Ingestion:**
   - SEC 10-K HTML/PDF parser extracting tables into Markdown/JSON structured format.
   - Semantic chunking with section metadata tags (`fiscal_year`, `item_type`, `table_name`).
2. **Hybrid Retrieval:**
   - Dense: `BAAI/bge-m3` or `text-embedding-3-small`.
   - Sparse: BM25 (critical for ticker symbols, footnote numbers, accounting terms).
3. **Cross-Encoder Reranker:**
   - `BAAI/bge-reranker-large` / `cohere-rerank-v3` to re-score top-25 down to top-5 chunks.
4. **Adaptive Iterative Engine (LangGraph / State Machine):**
   - **Step 1:** Initial query decomposition into 2-3 atomic retrieval goals.
   - **Step 2:** Hop 1 execution + intermediate answer extraction.
   - **Step 3 (Critic / Reflection Node):** Evaluates if retrieved context contains all required premises to answer the core question.
   - **Step 4 (Follow-up Loop):** If info is missing, generates a conditioned follow-up query incorporating Hop 1 findings (bounded by `max_hops = 3`).
   - **Step 5 (Synthesis & Guardrail):** Citations linked to exact page/table; generator constrained by hallucination reflection prompt.

---

## 4. Mandatory Comparative Analysis (The 3 Alternatives)

To exceed the rubric criteria:

| Dimension | Alternative A (Baseline) | Alternative B (Advanced Single-Pass) | Alternative C (Proposed Adaptive Multi-Hop) |
| :--- | :--- | :--- | :--- |
| **Retrieval Strategy** | Naive Single-Pass Dense Embedding (`k=5`) | Hybrid Retrieval (Dense BGE + Sparse BM25) + Cross-Encoder Rerank (`k=5`) | Adaptive Multi-Hop (Decomposition + Hybrid + Reranker + Evidence Sufficiency Loop) |
| **Multi-Hop Handling** | None (Single prompt retrieval) | None (Single prompt retrieval with larger context) | Iterative graph state loop (max 3 hops) |
| **Reasoning Engine** | Llama-3-8B / GPT-4o-mini direct generation | Llama-3-8B / GPT-4o-mini direct generation | Multi-stage prompt routing (Planner -> Retriever -> Critic -> Synthesizer) |
| **Trade-offs Evaluated** | Low latency, low cost, high hallucination / low recall on complex questions | Moderate latency, moderate cost, fails when 2nd hop requires entities discovered in 1st hop | Higher latency & token cost, superior context recall, higher answer faithfulness, zero spurious hops on simple queries |

---

## 5. Evaluation & Benchmarking Methodology

### Golden Test Dataset:
- **Curated Dataset:** 100 Multi-Hop Financial Questions:
  - 50 questions from established benchmarks: **FinQA** / **TAT-QA** (tabular + textual reasoning).
  - 50 curated real-world questions across 5 companies (e.g., Apple, Microsoft, Tesla, Nvidia, Amazon 2023-2024 10-K filings) categorized into:
    - *Single-hop direct* (Sanity check: Does Adaptive know when to stop at Hop 1?).
    - *Cross-section multi-hop* (Item 7 MD&A to Item 8 Financial statements).
    - *Cross-year comparison* (2023 vs 2024 metric shift explaining cause).

### Metrics:
1. **Quantitative Retrieval Metrics:**
   - Evidence Recall @ \(k\)
   - Context Precision
2. **Quantitative Generation Metrics (RAGAS / TruLens Framework):**
   - **Faithfulness:** Are all statements supported by retrieved context?
   - **Answer Relevance:** Does it answer the user's specific prompt?
   - **Citation Precision & F1:** Percentage of cited chunks that actually contain supporting facts.
3. **Operational Trade-Off Metrics:**
   - End-to-End Latency (seconds per query).
   - Token Consumption & API Cost ($/query).
   - Average Hop Count (Convergence rate).
4. **Qualitative Error Taxonomy (Mandatory for A+):**
   - 4-bucket failure analysis:
     1. Retrieval failure at Hop 1.
     2. Retrieval drift / loop termination failure at Hop 2.
     3. Reranker omission of tabular context.
     4. Generation hallucination despite correct context.

---

## 6. Workload Allocation for 5 Team Members

| Member | Designated Role | Core Modules & Deliverables |
| :--- | :--- | :--- |
| **Member 1 (Anish)** | **System Architect & Orchestration Lead** | LangGraph state graph design, multi-hop iteration state machine, query decomposition, and sufficiency reflection critic loop. |
| **Member 2** | **Data Ingestion & Parsing Engineer** | SEC 10-K scraping/HTML parsing, financial table serialization (Markdown/JSON tables), semantic chunking strategy, metadata tagging. |
| **Member 3** | **Retrieval & Reranking Engineer** | Vector DB setup (Chroma/Qdrant), dense embeddings (`bge-m3`), sparse BM25 indexing, cross-encoder reranker integration (`bge-reranker-large`). |
| **Member 4** | **Guardrails & Generation Lead** | Final synthesis prompting, citation mapping to source paragraphs/tables, active hallucination guardrail / self-consistency checks. |
| **Member 5** | **Evaluation Lead & Benchmarking Scientist** | Automated RAGAS / LLM-as-a-judge test harness, FinQA/TAT-QA dataset ingestion, cost/latency/hop-count profiling, error taxonomy analysis. |

---

## 7. Rubric Scoring Simulation: How This Scores

| Criterion | Target Grade | Why It Scores High |
| :--- | :---: | :--- |
| **1. Project Scope & Depth** | **A / A+** | Solves a genuine, notorious failure mode in finance (cross-statement multi-hop). Far exceeds single homework scope. |
| **2. Syllabus Topic Alignment** | **A+** | Hits Sessions 5 (Inference/Cost), 6 (Advanced RAG/Reranking), and 7 (Agentic Orchestration & loops). |
| **3. Technical Correctness** | **A** | Clear LangGraph state machine, avoids infinite loops with explicit bounds (`max_hops=3`), integrates state-of-the-art hybrid search + cross-encoder. |
| **4. Mandatory Comparative Analysis** | **A+** | Compares 3 distinct architectures (Naive vs Advanced Single-Pass vs Adaptive Multi-Hop) across accuracy, latency, and token cost. |
| **5. Evaluation & Reflection** | **A+** | Combines industry-standard RAGAS metrics, benchmark datasets (FinQA/TAT-QA), operational cost tracking, and structured qualitative error analysis. |
| **6. Guardrails & Safety** | **A** | Built-in sufficiency critic prevents generating on partial data; citation hallucination filter rejects ungrounded claims. |
| **7. Reproducibility & Team Cohesion** | **A** | Clear modular split across 5 team members, unified repository, runnable notebook/script harness. |

---

## 8. Strategic Questions to Ask the Professor During Consult (in 4 Days)

Use these questions during the consultation to validate scope and demonstrate depth:

### Question 1: System-Type vs Study-Type Positioning
> *"Professor, our idea blends a working system with an empirical study: we are building an Adaptive Multi-Hop RAG framework for SEC 10-K filings, and comparing it against Naive RAG and Advanced Single-Pass RAG (Hybrid + Reranker). Should we position our report primarily as a **System-Type with rigorous evaluation** or as an **Empirical Study on Multi-Hop Retrieval Trade-offs**?"*
*(Why ask this: Helps lock down the framing and grading rubric emphasis early).*

### Question 2: Scope of the Multi-Hop Adaptation
> *"For our adaptive loop, we are implementing query decomposition and an evidence sufficiency check (Self-RAG style) bounded by 3 hops. Is an LLM-based sufficiency critic sufficient for the course's advanced agentic criteria, or would you recommend adding a graph-based structure (like GraphRAG / LightRAG) or dynamic routing between single-hop and multi-hop paths?"*
*(Why ask this: Signals high technical competence while verifying if LangGraph state loops satisfy the syllabus expectations).*

### Question 3: Evaluation Benchmark & Golden Dataset Expectations
> *"To ensure our evaluation is rigorous and reproducible, we plan to use a combination of established benchmarks (like FinQA / TAT-QA) alongside 50 hand-verified real SEC 10-K multi-hop queries across recent filings. Does this test set balance satisfy your expectations for ground-truth rigor?"*
*(Why ask this: Confirms whether the professor prefers public academic benchmarks or instructor-verified real documents).*

### Question 4: Expected Trade-Off Depth (Cost vs Latency vs Accuracy)
> *"Multi-hop RAG naturally incurs higher latency and token costs due to multiple LLM reasoning and retrieval calls. How much weight do you place on practical deployment trade-offs (e.g., Pareto efficiency curves between RAGAS faithfulness vs latency/cost) in the final reflection section?"*
*(Why ask this: Directly targets the rubric's reflective analysis section, showing the team understands real-world constraints).*
