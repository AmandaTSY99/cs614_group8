# Report review: System C & RQ3 (local) + team Draft_Report update plan

**Prepared:** 1 Nov 2026 · **Scope:** Anish's sections (System C v1/v2/v3, RQ3, overall findings)
**Ground truth used:** `reports/rq3/records.jsonl` (485 runs = 97 questions × 5 systems), `src/`, git history, `scripts/rq2/metrics_custom.py` (strict scorer).
**Status (1 Nov 2026):** Part 1 executed. The local `.md` is rewritten per 1A–1F, `telemetry.py` now prices dated model snapshots correctly, `evaluate_rq3.py` reprices records, includes v2, uses McNemar for accuracy and labels the cascade as an oracle, and the `.docx` is now rendered from the `.md` by `scripts/build_word_report.py`. Part 2 (team `Draft_Report.docx`) is not started; it needs the team decisions in 2A/2C.
Notes from execution: the v3 vs v1 strict-accuracy McNemar (p = 0.039) is not significant after Holm correction across the 15 tests (p_Holm = 0.27); the report shows both. The repriced oracle cascade is $28.93/1k (not $24.83).

---

## Part 1 — Local report audit (`reports/CS614_Group8_System_C_and_RQ3_Final_Report.md`)

> The `.docx` of the same name is **stale**: it predates System C v3 (it covers A, B, v1 and v2 only). Treat the `.md` as the source, fix it, then regenerate the `.docx`.

### 1A. Factual errors (must fix)

| # | Where | Report says | What the code / records show | Fix |
|---|---|---|---|---|
| 1 | §1, §5, §7.2 | "93-question benchmark", "465 runs (93 × 5)" | 97 questions, **485 runs** (97 × 5) | Replace everywhere |
| 2 | §1 | Benchmark spans 7 companies (AAPL…WMT) | Benchmark questions cover **10 tickers** incl. META (18 Qs), JNJ (11), JPM (5) | List all 10 |
| 3 | §3, §6.1 table header | System B = "RRF (k = 60)", "top-3", "Visual ColPali Hybrid" | `src/system_b`: min-max **weighted fusion, α = 0.5**, top-30 candidates reranked → **top 5**. ColPali is Xavier's separate experiment, not System B | Correct description; drop "ColPali" from the B column header |
| 4 | §3 | "four distinct system configurations" then lists five | Five systems | "five" |
| 5 | §6.1 scorecard | A cost $0.383/1k, B $0.236/1k | A/B logged as `gpt-5.4-2026-03-05`, which is missing from `MODEL_PRICING_PER_1M` → silent fallback to $0.15/$0.60 (gpt-4o-mini rates) in `telemetry.py`. Repriced at gpt-5.4 ($2.50/$15): **A $7.00, B $4.34** | Use repriced values (or patch telemetry and re-run `evaluate_rq3.py`) |
| 6 | §6.1 | Risk-adjusted loss A $0.3612 … v3 $0.1521 | `evaluate_rq3.py` counts the 10 unscorable qualitative questions as *wrong* (`incorrect = n_queries − verified`) and uses the wrong A/B costs | Recompute on the 87 scorable Qs (table 1C) |
| 7 | §6.1 | "Numerical accuracy" with no definition | This is the **lenient** scorer (`numeric_correct`: any number within 1% of the *first* gold number). The strict RQ2 scorer gives very different values | Define it; report both (table 1C) |
| 8 | §6.2 | B vs A accuracy "significant, p_adj = 0.0411"; v2 tests from an older JSON | Current `summary_metrics.json`: B vs A p_adj = **0.082 (not significant)**. Wilcoxon on 0/1 accuracy is the wrong test; use McNemar | Replace with table 1D |
| 9 | §6.3 | Cascade A→v2: 76.29% acc, $19.91/1k, 15.45 s | Code (`simulate_routing_cascade`) does **B→v3** and gives 89.69%, $24.83/1k, 15.74 s. It also escalates using the **gold answer** (oracle), which production cannot do | Drop the cascade, or present it explicitly as an oracle upper bound. Replace with the break-even analysis (1E) |
| 10 | §4.3, §7 Case 3 | "10-K lookback barrier: pure textual RAG fails because the 2025 10-K does not carry 2021 figures" | **System A answered gold-066 correctly** in one pass (it retrieved 5 FY2021 + 5 FY2025 chunks). v1 also retrieved FY2021 chunks but missed the balance-sheet row | Reframe: v1's failure was a retrieval miss; XBRL makes multi-year totals a 1-hop lookup. It is not a barrier text RAG cannot cross |
| 11 | §7 Case 4 (gold-073) | "FY2024 → FY2025, 73.8% vs 65.0%", "Chunk 216", v3 "16.2 s" | Question is **FY2016 → FY2022, 56.1% → 64.9% = 8.8 pp**. v3: 2 hops, **11.5 s**. v2: 1 hop, failed ("does not disclose FY2022 gross margin") | Rewrite with record values |
| 12 | §7 Case 2 | v2 cost $0.025 | Record: $0.026 | Minor |
| 13 | §7.2 | "v3 attained 95.18% (79/83); 4 remaining failures" | v3 **first run** (git `a8db615^`): **79/87 = 90.8% lenient, 73.0% strict**, **8** failures (gold-006, 011, 029, 045, 058, 065, 074, 091). All 8 were fixed and the **same** 97 questions re-run → 87/87 | Rewrite §7.2 as "error analysis on the first run", list all 8, and state that the final result is in-sample |
| 14 | §8 limitation 2 | "Granularity-aware sufficiency critic" listed as *future work* | Already implemented in v3 (`critic.py`, `is_xbrl_headline_target`) | Replace with "held-out evaluation of v3" |
| 15 | §3, §4.3 | v3 = schema-aware routing + granularity critic only | Commit `a8db615` also added table-boundary stitching, temporal-role disambiguation, per-ticker search isolation, time-series synthesis rule | Add these four |
| 16 | §3 mermaid | Routing shown as "v1 vs v3" | `graph.py` routes **both v2 and v3** to `tabular_tool` | "v2/v3" |
| 17 | §9 | "162 passed" | Repo has 145 `test_` functions; commit message says 171 (parametrised). Re-run before quoting | Re-run and quote actual output |
| 18 | §2 team table | Four members | Deck lists **Kevin** (RQ2 with Aryan) | Add Kevin |

### 1B. Integrity disclosure (must add)

- The final 100% (87/87) is **in-sample**: the 8 first-run failures were diagnosed on the benchmark, fixed, and the same questions re-run.
- Several v3 routing exclusion keywords are lifted from failed benchmark questions (`"tegra"`, `"held in"`, `"scheduled to repay"`, `"goodwill"`, `"stock option"` in `FOOTNOTE_OR_SEGMENT_EXCLUSIONS`).
- Gold answers were **not** changed (verified: 0 field changes in `benchmark_qa_pool_2015.jsonl` in `a8db615`; identical gold across all 5 systems in `records.jsonl`).
- Recommended wording: *"The architectural changes alone (first run) matched v1's accuracy at lower latency; targeted error fixes then reached 87/87 on the development benchmark. A held-out evaluation is required before claiming generalisation."*

### 1C. Verified scorecard with System C v2 (drop-in replacement for §6.1)

All values recomputed from `records.jsonl`; A/B repriced at gpt-5.4 rates.

| Metric | System A | System B | System C v1 | System C v2 | System C v3 |
|---|---:|---:|---:|---:|---:|
| Numeric accuracy, lenient (n = 87) | 71.3% (62) | 58.6% (51) | 89.7% (78) | 82.8% (72) | 100%* (87) |
| Numeric accuracy, strict (n = 63) | 58.7% | 42.9% | 73.0% | 63.5% | 84.1% |
| Strict 95% bootstrap CI | 46–70% | 30–56% | 62–84% | 51–76% | 75–92% |
| Citation coverage | 83.5% | 69.1% | 97.9% | 96.9% | 100% |
| Grounding error rate (guardrail) | n/a | n/a | 8.9% | 6.3% | 6.6% |
| Mean hops | 1.00 | 1.00 | 2.24 | 1.77 | 2.12 |
| Stops after hop 1 | 100% | 100% | 28.9% | 54.6% | 39.2% |
| Latency p50 / p90 (s) | 2.4 / 4.5 | 6.6 / 8.4 | 21.4 / 36.3 | 13.6 / 32.6 | 18.2 / 29.3 |
| Tokens per query | 2,187 | 1,332 | 12,301 | 10,654 | 13,532 |
| Cost per 1,000 queries | $7.00 | $4.34 | $45.39 | $39.10 | $48.96 |
| Cost per correct answer (lenient) | $0.0098 | $0.0074 | $0.0506 | $0.0472 | $0.0490 |
| Expected loss @ $1/error (lenient) | $0.294 | $0.418 | $0.149 | $0.212 | $0.049* |

\*In-sample (see 1B). v3 first run: 90.8% lenient / 73.0% strict, $42.71/1k, p50 18.6 s, 2.03 hops.
RQ1 context recall (from `reports/rq1`): A 0.70, B 0.73, v1 0.91, v2 0.84 (teammate's rq1 report), v3 0.91.

### 1D. Hypothesis tests (drop-in replacement for §6.2)

Accuracy uses an exact McNemar test (paired, binary); hops and latency use paired Wilcoxon.

| Contrast | Metric | Result | p |
|---|---|---|---|
| v3 vs v1 | strict accuracy | 8 fixed / 1 broken | **0.039** |
| v3 vs v1 | lenient accuracy | 9 / 0 | **0.004** |
| v3 vs v2 | strict accuracy | 14 / 1 | **0.001** |
| v1 vs v2 | strict accuracy | 8 / 2 | 0.11 (n.s.) |
| v1 vs A | strict / lenient | 14/5, 21/5 | 0.064 (n.s.) / **0.002** |
| A vs B | strict / lenient | 15/5, 20/9 | 0.041 / 0.061 |
| v2 vs v1 | hops | 1.77 vs 2.24 | **< 0.001** |
| v2 vs v1 | latency | 13.6 vs 21.4 s p50 | **0.002** |
| v3 vs v1 | latency | 18.2 vs 21.4 s p50 | **< 0.001** |
| v3 vs v1 | hops | 2.12 vs 2.24 | 0.13 (n.s.) |
| v3 vs v2 | latency / hops | | 0.44 (n.s.) / **< 0.001** |
| B vs A | latency | 6.6 vs 2.4 s | **< 0.001** |

Note: the v2 vs v1 latency effect is real but the *median paired* difference is only ~0.3 s; the 37% p50 drop overstates the per-question saving.

### 1E. Replace the cascade with a break-even analysis (§6.3)

Expected cost per query = compute cost + P(wrong) × penalty Λ. Using strict accuracy:
- B is cheapest for Λ < $0.02; A for $0.02–$0.17; **v3 for Λ > $0.17** (lenient: ~$0.15).
- v1 and v2 are never the cheapest: v3 dominates both for Λ > ~$0.05.
This is the same analysis as deck slide 22.

### 1F. Where v2 now sits in the narrative

v1 → v2: XBRL pre-retrieval cuts hops and latency significantly, but 8 of the 9 questions v1 solved and v2 missed ended after one hop with XBRL totals already in evidence (premature sufficiency). v2 → v3: schema-aware routing plus line-item sufficiency recovers those answers while keeping the XBRL fast path (gold-066: 1 hop, 7.5 s).

---

## Part 2 — Team `Draft_Report.docx` vs local report: update plan (not executed)

### 2A. Gaps in the team draft

| Section | State | Action (owner) |
|---|---|---|
| Title / intro | Title says "3 RAG systems … BM25 with RRF"; §1 says "three systems" | Retitle around 5 systems (A, B, C v1–v3). Drop "RRF": B uses weighted fusion (Xavier/Aryan) |
| §2 Dataset | Good and consistent (10 cos, 272 filings, 95,044 chunks, 97 Qs; 43/34/20 split) | Keep. Add the 87 lenient-scorable / 63 strict-scorable split |
| §3 Systems | Placeholder: "(Cover how each system works … done by Anish)". Item 4 empty. B described as "BM25 + cross-encoder" only | **Anish:** write §3 from local §3–4 (corrected), incl. v1, v2, v3 and the v1→v2→v3 rationale (1F). Use the deck's slide 7/9/19 diagrams as figures |
| §4.1 RQ1 | Partly done; compares A, B, v1 only | Xavier/Amanda: add v2 and v3 columns (v3 = 0.91 recall, 0.82 complete@all from `reports/rq1`) |
| §4.2 RQ2 | Uses a **third accuracy definition** ("primary accuracy", 0.5% tolerance + key points: 0.66/0.59/0.86/0.90) and 4 systems (no v2). Reports RAGAS faithfulness 0.80/0.72/0.74/0.77 | Team decision: **one primary accuracy metric** across report and deck. Add v2. Confirm source of RAGAS numbers (not in `reports/rq2/full`, which ran with no judge). If valid, update deck slide 15/23 caveat "faithfulness not scored" |
| §4.3 RQ3 | Placeholder (ablation proposal) | **Anish:** replace with 1C scorecard, 1D tests, 1E break-even, Pareto figure regenerated with repriced A/B, and hop distribution |
| §5 ColQwen | Done (Xavier). States "System C v3 … answered all five" FY2025+ Qs | Fine; cite run file |
| §6 Front-end | Empty | Anish: HF Space architecture + screenshot |
| §7 Limitations | Empty | Merge local §8 (corrected) + deck slide 23 caveats + 1B disclosure |
| Appendix | RAGAS tables, 4 systems | Add v2; label which accuracy definition |
| Formatting | "[NFW] apply Calibri 12" note | Final pass |

### 2B. Cross-document consistency rules (apply in both report and deck)
1. **97 questions, 485 runs, 5 systems, 10 companies, 272 filings, 95,044 chunks.**
2. A/B cost always **repriced** ($7.00 / $4.34 per 1k).
3. Always name the accuracy scorer; report lenient and strict side by side (or agree on one primary).
4. v3 100% always paired with "in-sample; first run 91% / 73%".
5. No "lookback barrier that text RAG cannot cross" claim (System A answered gold-066).
6. No routing cascade unless labelled oracle.

### 2C. Suggested order once slides are done
1. Fix local `.md` (Part 1, ~1.5 h) → regenerate `.docx`.
2. Port corrected §3 + §4.3 + §6 into the team draft (~1 h).
3. Team call to settle the primary accuracy metric and the RAGAS source (15 min).
4. Regenerate `rq3_pareto_frontier.png` with repriced A/B and v2 included.
