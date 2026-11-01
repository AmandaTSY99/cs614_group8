# Kevin's revised System B: team handover

Branch: `feature/system-b-accuracy`. Based on `ffc6e00` from `feat/rq2-full-eval`.
This branch is ready for review; it has not been merged into `dev`.

## What is complete

All 97 expected question IDs have one A answer and one revised B answer: 194 answers.
The matched Groq GPT-OSS-120B replay has mean primary accuracy **A 59.536%, B 76.117%**,
a **16.581 percentage-point increase**. B wins 22 questions, ties 71 and loses 4.
The team Wilcoxon signed-rank test gives Holm-adjusted p = 0.0000390 for the overall A/B comparison.

Primary accuracy is numerical matching for numeric questions and key-point recall for qualitative/mixed
questions. It is **not RAGAS faithfulness**. The final subgroup accuracy and citation tables are in
[UPDATED_SLIDE_TABLES.md](UPDATED_SLIDE_TABLES.md). RAGAS cells remain pending; do not reuse old significance labels.

## Code changes

- B still uses dense + BM25 alpha blending and BAAI/bge-reranker-large. It is not an RRF implementation.
- Default output grows from five to ten passages. The first five cross-encoder selections are retained;
  additional slots take unique dense matches, with reranked candidates as fallback.
- The answer prompt asks for supported calculations, units and cited inputs, and permits supported partial
  answers when a multipart question cannot be answered completely. Unsupported inputs must not be invented.
- CLI, unified RQ2 adapter and Streamlit bridge default to ten passages. `app.py` was not changed.
- `tests/test_system_b_dense_supplement.py` checks that the reranked first five survive while dense passages
  are recovered. All 18 System B tests pass.

## Important experimental limits

Both A and B were generated with Groq `openai/gpt-oss-120b`, temperature 0, output cap 1024,
and low reasoning effort. This is a **saved-context replay**, not 97 fresh live retrievals.
A uses archived A contexts. B uses archived B top-five contexts plus archived A dense contexts as a proxy
for B's dense supplement. One separate live adapter smoke check confirmed ten distinct passages.
The benchmark was previously inspected, and both B's prompt and context selection changed, so this is
neither a held-out evaluation nor a prompt-only ablation.

C v1's displayed values come from the historical GPT-5.4 generation / GPT-4o-mini judge experiment.
They are reference values only; no significance comparison with these new Groq outputs is valid.
The lower new A citation coverage is from this new generation run and the team's strict mapped `[n]`
citation parser. Do not mix the old A citation coverage with new B's results.

## Files to use

| File | Purpose |
|---|---|
| `answers.jsonl` | All 194 completed answers, per-question scores, arm, model and token totals |
| `paired_summary.json` | Final paired accuracy, included IDs and win/tie/loss counts |
| `UPDATED_SLIDE_TABLES.md` | Presentation-ready accuracy and citation tables; RAGAS explicitly pending |
| `table_comparisons.json` | Exact paired tests, pair counts and confidence intervals |
| `provenance.json` | Source commit, generation configuration and SHA-256 input/output fingerprints |
| `build_tables.py` | Reconstruct exact replay contexts/citations and compute custom metrics and tables |
| `replay.py` | Original resumable answer-generation runner; completed answers are skipped |
| `summarize.py` | Recompute final accuracy report and summary from saved answers |
| `offline.py` | Reproduce lexical evidence-completeness comparison without API calls |

The shared frozen inputs are already tracked at `reports/rq2/full_v3/records.jsonl` and
`data/benchmark_qa_pool_2015.json`. Reconstructed contexts, model caches, logs and unfinished judge
checkpoints are not duplicated in this commit. Rebuilding the files below does not require credentials
or Supabase queries after the Docker dependencies are available.

## Get the branch and rebuild locally

Commit or stash your own work before switching branches.

```bash
git fetch origin
git switch --track origin/feature/system-b-accuracy
docker compose build runner rq2-eval
docker compose run --rm -T runner python -m unittest discover -s tests -p "test_system_b*.py"
docker compose run --rm -T runner python reports/b-accuracy/summarize.py
docker compose run --rm -T runner python reports/b-accuracy/build_tables.py --publish
```

If the branch already exists locally, use `git switch feature/system-b-accuracy` then
`git pull --ff-only`. `build_tables.py` verifies all 97 unique expected IDs in both arms and writes
`reports/b-accuracy/records.jsonl`, `custom_scores.jsonl`, `ragas_coverage.json`, and the tables.
The `--publish` option excludes partial RAGAS judgments from the published table until scoring is complete.
Omit it to inspect interim results locally, with explicit interim labels.

## Continue RQ2 judging

Kevin's existing local job is running; coordinate before starting another paid/API evaluation to avoid
duplicating work. A fresh clone does not include Kevin's incomplete local judge checkpoint.
If taking over, obtain the latest checkpoint privately and place it at
`reports/b-accuracy/scores_ragas_groq.jsonl`. The scorer skips successful rows and retries errors.

Use your own authorized Groq key in the ignored root `.env` as `GROQ_API_KEY=...`.
Saved-answer evaluation does not need Supabase access. Keep the same judge and settings for A and B:

```bash
docker compose run --rm -T -e EVAL_JUDGE_PROVIDER=groq -e EVAL_JUDGE_MODEL=openai/gpt-oss-120b rq2-eval python -u scripts/rq2/score.py --run reports/b-accuracy --metrics faithfulness,answer_relevancy,context_recall,context_precision,factual_correctness --scores-file scores_ragas_groq.jsonl --concurrency 1 --judge-max-tokens 4096
docker compose run --rm -T runner python reports/b-accuracy/build_tables.py --publish
```

Configuration: RAGAS 0.4.3, temperature 0, answer-relevancy strictness 3, local
`BAAI/bge-small-en-v1.5` embeddings, factual-correctness F1 with answer+keypoints reference and low
atomicity/coverage. The team abstention rules are preserved. There are 970 metric slots (194 x 5),
including legitimate N/A faithfulness judgments for abstentions. Inspect `ragas_coverage.json` rather
than counting raw checkpoint lines, because retries append replacement results.

Rate limits can stop the scorer after repeated failures; respect the provider retry time and rerun
the same command. Do not change the judge midway in the same file. Report missing/failed judgments and
the paired sample size honestly. The overall paired-summary bootstrap uses 5000 resamples/seed 614;
the table comparisons use the team's 2000-resample/seed 0 bootstrap and Wilcoxon/Holm procedure.

For integration into `dev`, review the five implementation files and the new test in this commit.
This branch includes the team's full RQ2 evaluator history; cherry-pick Kevin's handover commit if a
target branch should not also receive those ancestor commits.
