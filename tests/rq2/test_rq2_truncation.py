"""
RQ2 judge truncation: a judge answer that hits its output limit is its own `truncated` status (never retried, never
trips the circuit breaker) and is re-scored only when the limit is raised, which is recorded on the row and in
the report.
"""

import asyncio

import pytest

pytest.importorskip("ragas")
from instructor.exceptions import IncompleteOutputException  # noqa: E402

from scripts.rq2 import judge as J  # noqa: E402
from scripts.rq2 import report as R  # noqa: E402
from scripts.rq2 import score as S  # noqa: E402
from scripts.rq2.common import RECORDS_FILE, SCORES_FILE, append_jsonl, read_jsonl  # noqa: E402
from tests.rq2.test_rq2_score_report import _FakeMetric, _NoSleep, _record  # noqa: E402


class _Truncating(_FakeMetric):
    """Raises IncompleteOutputException while the judge limit is below `needs`, then returns `value`."""

    def __init__(self, limit_ref, needs=4096, value=0.8):
        super().__init__(value)
        self.limit_ref, self.needs = limit_ref, needs

    async def ascore(self, **kwargs):
        self.calls += 1
        if self.limit_ref["limit"] < self.needs:
            raise IncompleteOutputException(last_completion=None)
        return type("R", (), {"value": self.value})()


def _write(run_path, n):
    for i in range(n):
        append_jsonl(run_path / RECORDS_FILE, _record(f"Q{i}"))


def _run(run_path, fake, judge_max_tokens=None, metrics=("faithfulness",)):
    return asyncio.run(S.score_run(
        run_path, list(metrics), metric_factory=lambda name, llm, emb: fake, llm=object(), embeddings=object(),
        meter=J.JudgeMeter(), sleep=_NoSleep(), benchmark={}, judge_max_tokens=judge_max_tokens,
    ))


def test_incomplete_output_is_classified_as_truncated_not_retried():
    exc = IncompleteOutputException(last_completion=None)
    assert J.classify_error(exc) == J.ERROR_TRUNCATED
    wrapped = RuntimeError("wrapped")
    wrapped.__cause__ = exc
    assert J.classify_error(wrapped) == J.ERROR_TRUNCATED
    fake = _Truncating({"limit": 1024})
    with pytest.raises(J.JudgeCallError) as info:
        asyncio.run(J.call_with_retry(lambda: fake.ascore(), sleep=_NoSleep()))
    assert info.value.kind == J.ERROR_TRUNCATED and info.value.attempts == 1 and fake.calls == 1


def test_truncation_has_its_own_status_and_never_trips_the_circuit_breaker(tmp_path):
    _write(tmp_path, 8)  # more than the 5 failures that stop the run for ordinary errors
    fake = _Truncating({"limit": 1024})
    counts = _run(tmp_path, fake)
    rows = read_jsonl(tmp_path / SCORES_FILE)
    assert "stopped" not in counts and counts["scored"] == 8
    assert {r["status"] for r in rows} == {J.STATUS_TRUNCATED}
    assert all("IncompleteOutputException" in r["detail"] for r in rows)


def test_truncated_rows_are_rescored_only_with_a_higher_limit_and_record_it(tmp_path):
    _write(tmp_path, 3)
    limit = {"limit": 1024}
    fake = _Truncating(limit, needs=4096)
    _run(tmp_path, fake)                       # default limit: all truncated
    fake.calls = 0
    assert _run(tmp_path, fake)["skipped"] == 3 and fake.calls == 0  # same limit: not retried
    limit["limit"] = 8192
    counts = _run(tmp_path, fake, judge_max_tokens=8192)
    assert counts["scored"] == 3 and fake.calls == 3
    latest = R.latest_scores(read_jsonl(tmp_path / SCORES_FILE))
    assert {r["status"] for r in latest} == {J.STATUS_OK}
    assert all(r["judge_max_tokens"] == 8192 and "judge_max_tokens=8192" in r["detail"] for r in latest)
    fake.calls = 0
    assert _run(tmp_path, fake, judge_max_tokens=8192)["skipped"] == 3 and fake.calls == 0  # completed rows stay


def test_still_truncated_at_the_higher_limit_stays_truncated(tmp_path):
    _write(tmp_path, 1)
    fake = _Truncating({"limit": 0}, needs=10 ** 9)
    _run(tmp_path, fake)
    _run(tmp_path, fake, judge_max_tokens=8192)
    (row,) = R.latest_scores(read_jsonl(tmp_path / SCORES_FILE))
    assert row["status"] == J.STATUS_TRUNCATED and row["judge_max_tokens"] == 8192
    fake.calls = 0
    assert _run(tmp_path, fake, judge_max_tokens=8192)["skipped"] == 1 and fake.calls == 0
    assert S.is_done({"status": "truncated", "judge_max_tokens": 8192}, 8192)
    assert not S.is_done({"status": "truncated", "judge_max_tokens": 8192}, 16384)
    assert not S.is_done({"status": "error"}, None) and S.is_done({"status": "ok"}, 8192)


def test_older_error_rows_are_retried_under_the_new_limit(tmp_path):
    _write(tmp_path, 1)
    append_jsonl(tmp_path / SCORES_FILE, {"system": "system_c_v1", "question_id": "Q0", "metric": "faithfulness",
                                          "status": "error", "value": None, "judge": S.J.judge_label(
                                              J.DEFAULT_JUDGE_PROVIDER, J.DEFAULT_JUDGE_MODEL),
                                          "detail": "fatal after 1 attempt(s): IncompleteOutputException: "})
    assert _run(tmp_path, _FakeMetric(0.9), judge_max_tokens=8192)["scored"] == 1


def test_judge_max_tokens_setting_reaches_the_judge_and_is_validated(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "test-key-not-used")
    assert J.build_judge("openai", "gpt-4o-mini", J.JudgeMeter()).model_args["max_tokens"] == J.RAGAS_DEFAULT_MAX_TOKENS
    raised = J.build_judge("openai", "gpt-4o-mini", J.JudgeMeter(), max_tokens=8192)
    assert raised.model_args["max_tokens"] == 8192 and raised.model_args["temperature"] == 0.0
    with pytest.raises(ValueError):
        J.build_judge("openai", "gpt-4o-mini", J.JudgeMeter(), max_tokens=J.MAX_JUDGE_MAX_TOKENS + 1)


def test_report_lists_failed_rows_and_the_output_limit(tmp_path):
    scores = [
        {"system": "system_a", "question_id": "gold-001", "metric": "faithfulness", "status": "truncated",
         "value": None, "judge": "x", "category": "c", "detail": "", "judge_max_tokens": 8192},
        {"system": "system_a", "question_id": "gold-002", "metric": "faithfulness", "status": "ok",
         "value": 0.5, "judge": "x", "category": "c", "detail": "judge_max_tokens=8192", "judge_max_tokens": 8192},
        {"system": "system_a", "question_id": "gold-003", "metric": "factual_correctness", "status": "error",
         "value": None, "judge": "x", "category": "c", "detail": "boom"},
    ]
    failed = R.failed_to_score(scores)
    assert [(f["system"], f["metric"], f["status"], f["count"]) for f in failed] == [
        ("system_a", "factual_correctness", "error", 1), ("system_a", "faithfulness", "truncated", 1)]
    assert failed[1]["questions"] == ["gold-001"]
    text = R.render_report([{"system": "system_a", "question_id": "gold-001", "provider": "p", "model": "m"}],
                           scores, [], R.aggregate(scores))
    assert "## Failed to score" in text and "| system_a | faithfulness | truncated | 1 | gold-001 |" in text
    assert "8192 tokens for the 2 rows" in text and "does not affect rows that completed" in text
    assert "No judge rows failed" in R.render_report([], [], [], [])
