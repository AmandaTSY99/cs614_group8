"""
RQ2 Stage 2 (`cs614-eval` env, needs ragas): resumable scoring with a fake judge, retry / too_large /
fatal error paths, judge recorded per row and the single-judge guard, usage + rate-limit metering, and the
report (per-category aggregates, bootstrap CIs, generation failures, smoke estimate). No network calls.
"""

import asyncio

import pytest

pytest.importorskip("ragas")

import httpx  # noqa: E402
import openai  # noqa: E402

from scripts.rq2 import judge as J  # noqa: E402
from scripts.rq2 import report as R  # noqa: E402
from scripts.rq2 import score as S  # noqa: E402
from scripts.rq2.common import GEN_ERRORS_FILE, RECORDS_FILE, SCORES_FILE, append_jsonl, read_jsonl  # noqa: E402

JUDGE = J.judge_label(J.DEFAULT_JUDGE_PROVIDER, J.DEFAULT_JUDGE_MODEL)
_REQ = httpx.Request("POST", "https://judge.test/v1/chat/completions")


def _record(qid, system="system_c_v1", category="cross_section_multihop", answer="Revenue was $10 million [X:1]."):
    return {
        "system": system, "question_id": qid, "category": category, "question": f"Question {qid}?",
        "answer": answer, "retrieved_contexts": ["Revenue was $10 million.", "Other text."],
        "citations": [{"tag": "[X:1]", "chunk_id": "X:1", "ticker": "NVDA", "fiscal_year": 2026,
                       "section": "Item 7. MD&A"}],
        "guardrail_report": {"numerical_grounding_error_rate": 0.0},
        "ground_truth_answer": "Revenue was $10 million.", "ground_truth_numbers": ["$10 million"],
        "target_sections": ["Item 7"],
    }


def _rate_limit_error():
    return openai.RateLimitError("rate limited", response=httpx.Response(429, request=_REQ), body=None)


def _too_large_error():
    return openai.APIStatusError("Request too large for model", response=httpx.Response(413, request=_REQ), body=None)


def _context_length_error():
    return openai.BadRequestError("This model's maximum context length is 8192 tokens (context_length_exceeded)",
                                  response=httpx.Response(400, request=_REQ), body=None)


class _Result:
    def __init__(self, value):
        self.value = value


class _FakeMetric:
    """ascore raises the queued errors first, then returns `value`."""

    def __init__(self, value=0.8, errors=()):
        self.value = value
        self.errors = list(errors)
        self.calls = 0
        self.inputs = []

    async def ascore(self, **kwargs):
        self.calls += 1
        self.inputs.append(kwargs)
        if self.errors:
            raise self.errors.pop(0)
        return _Result(self.value)


class _NoSleep:
    def __init__(self):
        self.delays = []

    async def __call__(self, delay):
        self.delays.append(delay)


def _run(run_path, metrics, fakes, sleep=None, meter=None):
    return asyncio.run(S.score_run(
        run_path, metrics, metric_factory=lambda name, llm, emb: fakes[name], llm=object(), embeddings=object(),
        meter=meter or J.JudgeMeter(), sleep=sleep or _NoSleep(),
    ))


def _write_records(run_path, records):
    for r in records:
        append_jsonl(run_path / RECORDS_FILE, r)


def test_score_is_resumable_and_records_judge(tmp_path):
    _write_records(tmp_path, [_record("Q1"), _record("Q2")])
    fakes = {"faithfulness": _FakeMetric(0.9)}
    counts = _run(tmp_path, ["faithfulness", "numeric_accuracy", "citation_f1"], fakes)
    assert counts == {"scored": 6, "skipped": 0}
    rows = read_jsonl(tmp_path / SCORES_FILE)
    llm_rows = [r for r in rows if r["metric"] == "faithfulness"]
    assert {r["judge"] for r in llm_rows} == {JUDGE}
    assert {r["judge"] for r in rows if r["metric"] != "faithfulness"} == {S.NO_JUDGE}
    assert all(r["value"] == 0.9 and r["status"] == "ok" and r["attempts"] == 1 for r in llm_rows)
    # Citation tags are stripped before RAGAS
    assert "[X:1]" not in fakes["faithfulness"].inputs[0]["response"]

    fakes["faithfulness"].calls = 0
    counts = _run(tmp_path, ["faithfulness", "numeric_accuracy", "citation_f1"], fakes)
    assert counts == {"scored": 0, "skipped": 6}
    assert fakes["faithfulness"].calls == 0
    assert len(read_jsonl(tmp_path / SCORES_FILE)) == 6


def test_retryable_errors_back_off_then_succeed(tmp_path):
    _write_records(tmp_path, [_record("Q1")])
    sleep = _NoSleep()
    fakes = {"context_recall": _FakeMetric(0.7, errors=[_rate_limit_error(), openai.APITimeoutError(_REQ)])}
    _run(tmp_path, ["context_recall"], fakes, sleep=sleep)
    row = read_jsonl(tmp_path / SCORES_FILE)[0]
    assert row["status"] == "ok" and row["value"] == 0.7 and row["attempts"] == 3
    assert len(sleep.delays) == 2 and 2.0 <= sleep.delays[0] < 3.0 and 4.0 <= sleep.delays[1] < 5.0


@pytest.mark.parametrize("make_error", [_too_large_error, _context_length_error])
def test_too_large_is_not_retried(tmp_path, make_error):
    _write_records(tmp_path, [_record("Q1")])
    sleep = _NoSleep()
    fake = _FakeMetric(0.7, errors=[make_error()])
    _run(tmp_path, ["faithfulness"], {"faithfulness": fake}, sleep=sleep)
    row = read_jsonl(tmp_path / SCORES_FILE)[0]
    assert row["status"] == J.STATUS_TOO_LARGE and row["value"] is None and row["attempts"] == 1
    assert fake.calls == 1 and sleep.delays == []
    # too_large is final: a rerun does not retry it
    _run(tmp_path, ["faithfulness"], {"faithfulness": fake}, sleep=sleep)
    assert fake.calls == 1


def test_fatal_error_not_retried_and_retried_next_run(tmp_path):
    _write_records(tmp_path, [_record("Q1")])
    fake = _FakeMetric(0.6, errors=[ValueError("bad schema")])
    _run(tmp_path, ["factual_correctness"], {"factual_correctness": fake})
    row = read_jsonl(tmp_path / SCORES_FILE)[0]
    assert row["status"] == J.STATUS_ERROR and row["attempts"] == 1
    _run(tmp_path, ["factual_correctness"], {"factual_correctness": fake})
    assert read_jsonl(tmp_path / SCORES_FILE)[-1]["status"] == "ok"
    assert R.latest_scores(read_jsonl(tmp_path / SCORES_FILE))[0]["value"] == 0.6


def test_retries_exhausted_is_error(tmp_path):
    _write_records(tmp_path, [_record("Q1")])
    fake = _FakeMetric(0.5, errors=[_rate_limit_error() for _ in range(J.MAX_ATTEMPTS)])
    _run(tmp_path, ["faithfulness"], {"faithfulness": fake})
    row = read_jsonl(tmp_path / SCORES_FILE)[0]
    assert row["status"] == J.STATUS_ERROR and row["attempts"] == J.MAX_ATTEMPTS
    assert "retries_exhausted" in row["detail"]


def test_classify_error():
    assert J.classify_error(_too_large_error()) == J.ERROR_TOO_LARGE
    assert J.classify_error(_context_length_error()) == J.ERROR_TOO_LARGE
    assert J.classify_error(_rate_limit_error()) == J.ERROR_RETRYABLE
    assert J.classify_error(openai.APIConnectionError(request=_REQ)) == J.ERROR_RETRYABLE
    assert J.classify_error(openai.InternalServerError("x", response=httpx.Response(503, request=_REQ),
                                                      body=None)) == J.ERROR_RETRYABLE
    assert J.classify_error(ValueError("parse")) == J.ERROR_FATAL
    # Wrapped by instructor/ragas
    try:
        try:
            raise _rate_limit_error()
        except Exception as inner:
            raise RuntimeError("instructor wrapper") from inner
    except RuntimeError as wrapped:
        assert J.classify_error(wrapped) == J.ERROR_RETRYABLE


def test_missing_inputs_are_na(tmp_path):
    rec = _record("Q1")
    rec["retrieved_contexts"] = []
    _write_records(tmp_path, [rec])
    fake = _FakeMetric()
    _run(tmp_path, ["context_precision"], {"context_precision": fake})
    row = read_jsonl(tmp_path / SCORES_FILE)[0]
    assert row["status"] == "na" and fake.calls == 0


def test_contexts_passed_in_record_order(tmp_path):
    rec = _record("Q1")
    rec["retrieved_contexts"] = ["third-ranked? no: first", "second", "third"]
    _write_records(tmp_path, [rec])
    fake = _FakeMetric()
    _run(tmp_path, ["context_precision"], {"context_precision": fake})
    assert fake.inputs[0]["retrieved_contexts"] == ["third-ranked? no: first", "second", "third"]


def test_single_judge_guard(tmp_path):
    _write_records(tmp_path, [_record("Q1"), _record("Q2")])
    append_jsonl(tmp_path / SCORES_FILE, {"system": "system_c_v1", "question_id": "Q1", "metric": "faithfulness",
                                          "value": 0.5, "status": "ok", "judge": "openai/gpt-4o-mini"})
    with pytest.raises(SystemExit, match="refusing to mix"):
        _run(tmp_path, ["faithfulness"], {"faithfulness": _FakeMetric()})


def test_meter_records_calls_tokens_and_ratelimit_headers():
    meter = J.JudgeMeter()
    key = ("system_c_v1", "Q1", "faithfulness")

    async def go():
        meter.start(key)
        for prompt, completion in ((100, 20), (50, 10)):
            resp = httpx.Response(
                200, request=_REQ,
                headers={"x-ratelimit-limit-requests": "1000", "x-ratelimit-remaining-requests": "990",
                         "x-ratelimit-limit-tokens": "8000", "x-ratelimit-remaining-tokens": "7800",
                         "content-type": "application/json"},
                json={"usage": {"prompt_tokens": prompt, "completion_tokens": completion}},
            )
            await meter.on_response(resp)

    asyncio.run(go())
    snap = meter.snapshot(key)
    assert snap["calls"] == 2 and snap["prompt_tokens"] == 150 and snap["completion_tokens"] == 30
    assert snap["ratelimit"]["x-ratelimit-remaining-requests"] == "990"
    assert meter.last_ratelimit["x-ratelimit-limit-tokens"] == "8000"


def test_usage_written_to_score_rows(tmp_path):
    _write_records(tmp_path, [_record("Q1")])
    meter = J.JudgeMeter()

    class _MeteredMetric(_FakeMetric):
        async def ascore(self, **kwargs):
            await meter.on_response(httpx.Response(
                200, request=_REQ, headers={"x-ratelimit-remaining-tokens": "5000"},
                json={"usage": {"prompt_tokens": 300, "completion_tokens": 40}},
            ))
            return await super().ascore(**kwargs)

    _run(tmp_path, ["faithfulness"], {"faithfulness": _MeteredMetric(0.9)}, meter=meter)
    row = read_jsonl(tmp_path / SCORES_FILE)[0]
    assert (row["judge_calls"], row["judge_prompt_tokens"], row["judge_completion_tokens"]) == (1, 300, 40)
    assert row["ratelimit"] == {"x-ratelimit-remaining-tokens": "5000"}


def test_report_aggregates_per_category_with_ci_and_generation_failures(tmp_path):
    records = [_record("Q1"), _record("Q2"), _record("Q3", category="single_hop_factual"),
               _record("Q1", system="system_c_v2")]
    _write_records(tmp_path, records)
    append_jsonl(tmp_path / GEN_ERRORS_FILE, {"system": "system_c_v2", "question_id": "Q2", "error": "boom"})
    append_jsonl(tmp_path / GEN_ERRORS_FILE, {"system": "system_c_v2", "question_id": "Q1", "error": "later ok"})
    values = {"Q1": 0.2, "Q2": 0.4, "Q3": 0.9}
    for r in records:
        append_jsonl(tmp_path / SCORES_FILE, {
            "system": r["system"], "question_id": r["question_id"], "category": r["category"],
            "metric": "faithfulness", "value": values[r["question_id"]], "status": "ok", "judge": JUDGE,
            "timestamp": "2026-10-25T00:00:00+00:00",
        })
    agg = {(a["system"], a["category"], a["metric"]): a for a in R.aggregate(read_jsonl(tmp_path / SCORES_FILE))}
    overall = agg[("system_c_v1", "overall", "faithfulness")]
    assert overall["n"] == 3 and overall["mean"] == pytest.approx(0.5)
    assert 0.2 <= overall["ci_low"] <= overall["mean"] <= overall["ci_high"] <= 0.9
    cross = agg[("system_c_v1", "cross_section_multihop", "faithfulness")]
    assert cross["n"] == 2 and cross["mean"] == pytest.approx(0.3)
    assert agg[("system_c_v1", "single_hop_factual", "faithfulness")]["n"] == 1

    assert R.generation_failures(read_jsonl(tmp_path / RECORDS_FILE), read_jsonl(tmp_path / GEN_ERRORS_FILE)) == {
        "system_c_v1": 0, "system_c_v2": 1}
    text = R.build_report(tmp_path)
    assert "| system_c_v2 | 1 | 1 |" in text
    assert "Context Precision is order-sensitive" in text
    assert "(n=3)" in text
    assert (tmp_path / "aggregate.csv").exists()


def test_bootstrap_ci_is_deterministic():
    vals = [0.1, 0.5, 0.9, 0.3]
    assert R.bootstrap_ci(vals) == R.bootstrap_ci(vals)
    assert R.bootstrap_ci([0.4]) == (0.4, 0.4)


def test_smoke_estimate_from_usage_and_headers():
    usage = [
        {"system": "s", "question_id": q, "metric": m, "status": "ok", "calls": 2,
         "prompt_tokens": 900, "completion_tokens": 100}
        for q in ("Q1", "Q2", "Q3") for m in R.LLM_METRICS
    ]
    est = R.estimate_free_tier(usage, {"x-ratelimit-limit-requests": "1000", "x-ratelimit-limit-tokens": "8000"},
                               n_samples=120, tokens_per_day=200_000)
    assert est["calls_per_sample"] == 10 and est["tokens_per_sample"] == 5000
    assert est["total_calls"] == 1200 and est["total_tokens"] == 600_000
    assert est["days_by_requests"] == pytest.approx(1.2)
    assert est["days_by_tokens_per_day"] == pytest.approx(3.0)
    assert est["estimated_days"] == pytest.approx(3.0)
    assert est["minutes_by_tokens_per_minute"] == pytest.approx(75.0)


def test_real_judge_and_metrics_construct_offline(monkeypatch):
    """ragas 0.4.3 API check: the judge and four metrics build without any network call."""
    monkeypatch.setenv("GROQ_API_KEY", "test-key-not-used")
    llm = J.build_judge("groq", J.DEFAULT_JUDGE_MODEL, J.JudgeMeter())
    for name in ("faithfulness", "context_recall", "context_precision", "factual_correctness"):
        metric = S.make_metric(name, llm)
        assert hasattr(metric, "ascore")
