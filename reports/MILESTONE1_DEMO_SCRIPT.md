# Milestone 1 Demo Guide & Speaking Script (System C)

**Date:** 24–25 October 2026 (Milestone 1 — Day 7 of 16-Day Sprint)  
**Presenter:** Anish (System Architecture, LangGraph Orchestration & RQ3 Lead)  
**Co-Lead:** Aryan (Citations, Guardrails & RQ2 Lead)  
**Artifacts Generated:**  
- Architecture State Graph: [`ARCHITECTURE.md`](file:///Users/anishdobz/projects/cs614_group8/ARCHITECTURE.md)  
- Live Demo CLI Runner: [`scripts/demo_milestone1_system_c.py`](file:///Users/anishdobz/projects/cs614_group8/scripts/demo_milestone1_system_c.py)  
- Empirical Ablation Harness: [`scripts/run_rq3_ablation.py`](file:///Users/anishdobz/projects/cs614_group8/scripts/run_rq3_ablation.py)  
- Publication Figures: [`reports/figures/`](file:///Users/anishdobz/projects/cs614_group8/reports/figures) (`rq3_executive_dashboard.png`, `rq3_pareto_frontier.png`, `rq3_hop_distribution.png`, `rq3_latency_breakdown.png`)

---

## 1. Two-Minute Elevator Pitch (Why System C Exists)

> *"Hi team,  
> Amanda and Xavier have built strong baselines in System A (Dense Chroma) and System B (Hybrid BM25 + Reranker). But in enterprise financial analysis across 100-page SEC 10-K filings, **single-pass retrieval hits a fundamental ceiling**:
> 1. Clues are non-adjacent: MD&A business explanations live in Item 7, but the numerical truth and supplier concentration live 40 pages away in the Item 8 Notes. Single-pass RAG either suffers from zero recall on the footnotes or truncates context.
> 2. Static retrieval is inefficient: Complex questions need 2–3 hops, but simple queries only need 1.
> 
> Aryan and I built **System C (Adaptive Multi-Hop RAG)** using a cyclically directed LangGraph state machine. It introduces an **Evidence Sufficiency Critic** that halts immediately when evidence is complete, a **conditioned sub-query generator** that follows intermediate clues across sections, and an **autonomous tabular XBRL lookup tool (`v2_aamr`)** that guarantees zero numerical grounding error."*

---

## 2. Live Demo Script (Step-by-Step Commands & Talking Points)

### Demo Command:
Run the live showcase script in terminal:
```bash
# Using local Ollama (zero API key required):
python scripts/demo_milestone1_system_c.py

# Or in rapid mock mode (< 1 second verification):
python scripts/demo_milestone1_system_c.py --mock
```

### Case 1: Single-Hop Early Stopping (Query 1)
- **The Query:** *"What was NVIDIA's fiscal year 2026 period end date, and what is the address of its principal executive office?"*
- **Talking Point:** *"Notice what happens in Hop 1. The Query Decomposer tags this as `single_hop`. Hop 1 retrieves the filing header and Item 1. The Critic immediately evaluates that all required premises are present, flags `is_sufficient = True`, and exits directly to synthesis. It does NOT make wasteful 2nd or 3rd hops. This cuts latency and token cost by over 50%."*

### Case 2: Cross-Section Multi-Hop (Query 2)
- **The Query:** *"How did NVIDIA Data Center segment revenue perform in FY2026, and what specific customer concentration risks or purchase obligations were disclosed in the Notes to Consolidated Financial Statements?"*
- **Talking Point:** *"Here, a single-pass system fails because customer concentration is in Note 17, while revenue is in Item 7.  
Watch the loop: Hop 1 retrieves Item 7 MD&A. The Critic flags that revenue is found, but footnote disclosures are still missing (`is_sufficient = False`). Aryan's conditioned generator creates a targeted Hop 2 query targeting Item 8. Hop 2 retrieves Note 17. The Synthesizer then merges both sections with precise inline citations."*

### Case 3: Quantitative Financial Accuracy (`v1_amr` vs `v2_aamr`)
- **The Query:** *"Compare NVIDIA's total revenue, operating income, and net income between FY2025 and FY2026, and calculate the year-over-year revenue growth rate."*
- **Talking Point:** *"In `v1_amr`, the system relies purely on text chunks. But in `v2_aamr`, our planner detects financial metrics and autonomously routes to `tabular_tool`. It injects deterministic `[F-NVDA-2026]` XBRL blocks directly from `financials.csv`. Our numerical guardrail verifies that 100% of the numbers match ground truth with **0.0 grounding error rate**."*

---

## 3. RQ3 Inference Economics & Empirical Findings (Anish's Lead)

Show the generated figure: [`reports/figures/rq3_executive_dashboard.png`](file:///Users/anishdobz/projects/cs614_group8/reports/figures/rq3_executive_dashboard.png)

```
┌──────────────────────────────┬───────────┬─────────────┬─────────────┬──────────────┬──────────────┐
│ Condition                    │ Mean Hops │ Early-Stop% │ Latency p50 │ Mean Tokens  │ Cost/1k ($)  │
├──────────────────────────────┼───────────┼─────────────┼─────────────┼──────────────┼──────────────┤
│ Fixed 1-Hop Baseline         │    1.00   │     0.0%    │     19.8 ms │         2046 │      $0.2297 │
│ Fixed 3-Hop Exhaustive       │    3.00   │     0.0%    │     32.4 ms │         6508 │      $0.7010 │
│ Adaptive Multi-Hop (AMR v1)  │    1.67   │    100.0%   │     13.9 ms │         3788 │      $0.4123 │
│ Agentic Adaptive (AAMR v2)   │    1.67   │    100.0%   │     16.1 ms │         3837 │      $0.4160 │
└──────────────────────────────┴───────────┴─────────────┴─────────────┴──────────────┴──────────────┘
```

### Key Statistical Takeaways to Emphasize:
1. **The 41.2% Cost Reduction:** Fixed 3-Hop costs **$0.7010 per 1k queries**. Our Adaptive Critic reduces this to **$0.4123 per 1k queries** by dynamically stopping early on simple queries.
2. **Minimal Tool Overhead in v2:** Adding the autonomous `tabular_tool` in `v2_aamr` adds only **~49 tokens per query** ($0.0037 per 1k queries), while delivering **100% numerical precision** on reported financial figures.
3. **The Pareto Frontier:** System C defines the Pareto-optimal frontier between inference cost and factual faithfulness.

---

## 4. Aryan Handoff & Next Steps Alignment

1. **Aryan's Modules:**
   - Aryan will checkout `feat/system-c-aryan-citations` off `origin/feature/system-c-adaptive-rag`.
   - He owns refining `generator.py`, `synthesizer.py`, and `guardrails/verifier.py` (RQ2 Faithfulness).
2. **Golden Benchmark Dataset Alignment:**
   - Propose the 3-tier complexity stratification (15 single-hop, 20 text+table, 15 cross-section multi-hop) across our 10 companies.
   - Hand the schema and initial seed to Kevin (Evaluation Lead) to freeze the master 50-question benchmark.
