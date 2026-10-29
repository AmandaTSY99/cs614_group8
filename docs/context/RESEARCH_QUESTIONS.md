# CS614 Research Questions & Evaluation Metrics Mapping

This document details the scientific hypotheses, empirical metrics, and evaluation setup for the comparative study across System A, System B, and System C.

---

### RQ1: Retrieval Completeness across Question Types
* **Question:** To what extent does adaptive multi-hop retrieval (System C v1/v2) retrieve the complete set of gold evidence compared with single-pass dense (System A) and hybrid-reranked (System B) retrieval, and how does this vary with where the evidence lives: its modality (tabular vs narrative), its spread across 10-K Items, and its spread across fiscal years and companies?
* **Evaluation Metrics:**
  * Evidence Recall@$k$ ($k$ = 5, 10) and Context Recall (all retrieved chunks), using lexical matching of gold quotes
  * Evidence-set completeness (complete@$k$): share of questions where *all* gold evidence was retrieved
  * Zero-recall rate
  * Context Precision (rank-aware average precision; lexical labels, optionally RAGAS LLM-judged)
  * All of the above broken down by recipe, modality, scope (single doc / cross-year / cross-company), evidence count and section spread, plus recall per evidence item for tables vs text
* **What It Proves:** Whether iterative, critic-guided retrieval closes the completeness gap that single-pass systems leave on dispersed, multi-modal evidence, and at what cost to context precision. Hop counts and early stopping are covered in RQ3; citation attribution is covered in RQ2.
* **Leads:** Xavier & Amanda.

---

### RQ2: Factual Faithfulness & Citation Grounding
* **Question:** Does verifying evidence sufficiency before generation prevent hallucinations and enforce strict citation grounding in high-stakes financial disclosures?
* **Evaluation Metrics:**
  * RAGAS Faithfulness Score
  * Citation Precision & Citation F1
  * Numerical Grounding Error Rate (Exact-match on dollar amounts, percentages, fiscal dates)
* **What It Proves:** Proves whether the Evidence Sufficiency Critic and active hallucination guardrails stop the LLM from fabricating numbers or making speculative leaps on partial context.
* **Leads:** Aryan & Kevin.

---

### RQ3: Inference Economics & Operational Trade-offs
* **Question:** What is the operational cost and latency penalty incurred by running multi-stage agentic loops compared to single-pass systems, and what is the optimal Pareto frontier?
* **Evaluation Metrics:**
  * End-to-End Latency ($p50$, $p90$, $p99$ wall-clock seconds per query)
  * Token Consumption per Query (Prompt vs. Completion tokens per hop)
  * Monetary Cost estimate (\$/1,000 queries)
  * Average Hop Count / Early-Stopping Rate (Single-hop sanity vs multi-hop depth)
  * Pareto Frontier Curve (Faithfulness vs. Cost / Latency)
* **What It Proves:** Quantifies the real-world deployment viability: proves whether the accuracy gains of System C justify the latency overhead over single-pass RAG, and identifies when early-stopping prevents wasteful hops.
* **Lead:** **Anish (Me)**.
