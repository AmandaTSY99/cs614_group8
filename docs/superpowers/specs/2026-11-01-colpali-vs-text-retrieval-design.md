# Visual retrieval (ColPali, ColQwen) vs text retrieval: evaluation design

Date: 2026-11-01. Status: approved by user in conversation.

## Goal

Re-evaluate page-image retrieval (ColPali v1.3, ColQwen2.5) on the 97-question Benchmark v1 (FY2015+ filings) and
compare it against the text systems A, B, C v1 and C v3. Deliver a written report.

The earlier `colpali_eval` branch tested 20 hand-picked table questions and 5 benchmark questions, with a different
answer model (Qwen on Groq) than the text baselines (gpt-oss). That confounds retriever and generator and is too small.

## Fixed inputs

- Benchmark: `benchmark/benchmark_qa_1.jsonl` (97 questions, 81 distinct gold filings, 78 multi-hop, 33 cross-year, 9 cross-company).
- Text systems: A, B, C v1, C v3. Results are reused as published, not re-run.
  - RQ2 answers and scores: `origin/feat/rq2-full-eval`, `reports/rq2/full_v3/` (answer model gpt-5.4, judge gpt-4o-mini).
  - RQ1 scorer: `origin/feat/rq1` (`scripts/rq1/`). `main` has C v2 but no C v3 retrieval metrics.
- Vision retrievers: `vidore/colpali-v1.3`, `vidore/colqwen2.5-v0.2`.

## Method

1. **Worktree.** Check out the data and code from the other branches in a git worktree. `main` and the untracked `colpali_eval/` files stay untouched.
2. **Index.** Print the 34 missing filings to PDF (headless Edge, as before), render pages at 150 dpi, and embed all 81 filings with both
   retrievers. Cache embeddings on disk and resume from the 4 filings already done.
3. **Retrieval protocol.** Search only the gold filing(s) of each question, top-k pages per filing. This is optimistic for vision because
   Systems A and B search the whole corpus. The report states this and notes C v3's own filing filter.
4. **Retrieval metrics.** Same definitions as RQ1: a page is a hit if it contains the gold evidence quote. Report recall@k, complete@k and MRR at equal k, and
   recall at equal context size in tokens, because pages hold more text than chunks.
5. **Answers.** Top-3 pages per filing go to gpt-5.4 as images. Scoring reuses the RQ2 scorers and the gpt-4o-mini judge: numeric accuracy,
   keypoint recall, refusal rate, faithfulness and the rest. All cells carry bootstrap 95% CIs, split by recipe and hop count.
6. **Costs.** Index size per page, GPU indexing time, query latency, image tokens per answer.

## Deliverable

`reports/colpali/REPORT.md` plus figures: setup, retrieval results, answer accuracy, per-recipe wins and losses, failure cases, cost and storage, limitations.
Publishing as a shareable doc is offered afterwards, not assumed.

## Assumptions

- The OpenAI key can call gpt-5.4 with images and the budget covers about 97 questions with 3+ page images each.
- Several GPU hours on the RTX 3080 Ti are acceptable.
- Only ColPali v1.3 and ColQwen2.5 are in scope. A newer retriever is an optional extra.

## Risks

- C v3 records may not carry retrieved evidence, so C v3 retrieval metrics may need a re-run of its retriever.
- Pages that split a table across a page break can miss complete@k.
- Pre-2001 plain-text filings are out of scope (benchmark is FY2015+).
