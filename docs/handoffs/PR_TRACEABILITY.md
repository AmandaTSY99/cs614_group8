# PR Traceability

PR 1 `feat/system-c-aryan-citations` (base `feature/system-c-adaptive-rag` @ `719a8d5`) · PR 2 `feat/rq2-ragas` (stacked on PR 1). Mock tests: all 105 pass on PR 1 (including the Supabase test, which needs `SUPABASE_DB_URL` in `.env`); each commit passes on its own.

| # | Requirement | Where | Key tests | Status |
| --- | --- | --- | --- | --- |
| 1 | Follow-up query uses critic gaps + all evidence; no near-duplicate queries | `nodes/generator.py` | `test_generator.py` | Done |
| 2 | Inline tags `[TICKER FYYEAR, SECTION, CHUNK_ID]` / `[F-TICKER-YEAR]` mapped to exact chunks | `guardrails/citations.py`, `nodes/synthesizer.py` | `test_synthesizer.py` | Done |
| 3 | Every $ / % checked against the sentence's **cited** chunks | `guardrails/verifier.py` | `test_guardrail.py` (numeric) | Done |
| 4 | Unverified sentences flagged (incl. uncited claims, false refusals) | `guardrails/verifier.py` | `test_guardrail.py` (semantic) | Done |
| 5 | Repair flagged output, then re-check | `nodes/repair.py` + existing `repair -> guardrail` edge | `test_guardrail.py`, `test_system_c.py` | Done |
| 6 | All LLM calls via `call_llm` | generator, synthesizer, verifier, repair — one call each, no direct provider calls | `test_output_contract_and_single_llm_call` | Done |
| 7 | Node output contracts unchanged | guardrail returns exactly its 4 keys; repair rebuilds `citations` | `test_guardrail_output_keys_match_handoff_contract` | Done |
| 8 | `guardrail_report` keeps original keys | `verifier.py` | `test_report_keeps_legacy_keys_and_adds_new_ones` | Done |
| 9 | Docker | PR 1: no changes needed · PR 2: `Dockerfile.eval` + `rq2-eval` service | — | Done (eval image untested) |
| 10 | RQ2: RAGAS faithfulness, citation P/R/F1, numerical error rate | PR 2 `scripts/rq2/` | `tests/rq2/` | Done (smoke-tested) |

## External Module Modifications (commit `891f765`)

| File | Change | Why |
| --- | --- | --- |
| `api.py` | `load_dotenv(override=False)` | `.env` was overriding mock mode in tests |
| `llm.py` | optional `provider` / `model` on `call_llm` | lets the guardrail judge use another model; default behaviour unchanged |
| `app.py` | default Groq model → `gpt-oss-120b`; single brackets on citation titles | Llama 8B first drafts had no citations; UI showed `[[…]]` |
| `test_system_c.py` | real chunk ID in repair test | strict resolver rejects fake IDs |
| `test_system_c.py` | `test_arithmetic_derivation_margin_and_growth_grounding` used the fake chunk ID `F-NVDA`; the strict resolver requires `[F-TICKER-YEAR]` and `F-` chunks are parsed as XBRL CSV rows, so it now uses a real-format ID. | Its assertions are unchanged and pass with our derived-number logic. |

## Limitations / pending

- Numeric guardrail checks a figure **exists** in the cited chunk, not that it's the right line item.
- `guardrail_report.faithfulness_score` ≠ RAGAS faithfulness (that's in PR 2).
- Full RQ2 run pending; Systems A/B are stubs; Docker eval image untested.
- Retrieval verified on Supabase (same chunk IDs as local files).