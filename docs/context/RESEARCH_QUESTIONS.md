# CS614 Research Questions & Evaluation Metrics Mapping

This document details the scientific hypotheses, empirical metrics, and evaluation setup for the comparative study across System A, System B, and System C.

---

### RQ1: Retrieval Completeness across Non-Adjacent Sections
* **Question:** Does iterative multi-hop retrieval successfully gather scattered clues across non-adjacent SEC 10-K sections (MD&A, Market Risk disclosures, and Financial Statement Footnotes)?
* **Evaluation Metrics:**
  * Multi-Hop Evidence Recall@$k$
  * Context Precision (RAGAS)
  * Hop-by-Hop Retrieval Attribution (which hops fetched which facts)
* **What It Proves:** Proves whether System C (Adaptive Multi-Hop) successfully discovers distant intermediate clues where single-pass baselines (System A & B) suffer from zero-recall on dependent hops.
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
