"""
RQ2 Stage 1 (main `cs614` env): adapter schema in mock mode, stub adapters, resumable generation,
failure logging, and that the generate stage never imports ragas.
"""

import subprocess
import sys

import pytest

from scripts.rq2 import generate as gen
from scripts.rq2.adapters import ADAPTER_KEYS, SystemAAdapter, SystemAdapter, SystemBAdapter, SystemCAdapter
from scripts.rq2.common import GEN_ERRORS_FILE, RECORDS_FILE, REPO_ROOT, read_jsonl

QUESTION = {
    "id": "GOLD-T1", "category": "cross_section_multihop", "ticker": "NVDA", "fiscal_years": [2026],
    "query": "How did NVDA revenue change in 2026 and what footnote debt covenants applied?",
    "ground_truth_answer": "Revenue grew.", "ground_truth_numbers": ["$130.5 billion"], "target_sections": ["Item 7"],
}


@pytest.fixture(autouse=True)
def force_mock_llm(monkeypatch):
    monkeypatch.setenv("LLM_PROVIDER", "mock")


@pytest.mark.parametrize("mode", ["v1_amr", "v2_aamr"])
def test_system_c_adapter_returns_schema(mode):
    out = SystemCAdapter(mode).answer(QUESTION)
    assert set(out) == set(ADAPTER_KEYS)
    assert out["answer"]
    assert out["retrieved_contexts"] and all(isinstance(c, str) for c in out["retrieved_contexts"])
    assert len(out["contexts_meta"]) == len(out["retrieved_contexts"])
    assert {"chunk_id", "ticker", "fiscal_year", "section"} <= set(out["contexts_meta"][0])
    assert set(out["tokens"]) == {"prompt", "completion", "total"} and out["tokens"]["total"] > 0
    assert out["hops"] >= 1
    assert isinstance(out["guardrail_report"], dict)
    for c in out["citations"]:
        assert set(c) == {"tag", "chunk_id", "ticker", "fiscal_year", "section"}


def test_contexts_keep_retrieval_order():
    out = SystemCAdapter("v1_amr").answer(QUESTION)
    hops = [m["chunk_id"] for m in out["contexts_meta"]]
    assert hops == list(dict.fromkeys(hops))  # no reordering / duplicates introduced by the adapter


@pytest.mark.parametrize("cls", [SystemAAdapter, SystemBAdapter])
def test_stub_adapters_raise_with_contract(cls):
    with pytest.raises(NotImplementedError):
        cls().answer(QUESTION)
    assert "ADAPTER_KEYS" in cls.__doc__


class _FakeAdapter(SystemAdapter):
    def __init__(self, fail_ids=()):
        self.calls = []
        self.fail_ids = set(fail_ids)

    def answer(self, q):
        self.calls.append(q["id"])
        if q["id"] in self.fail_ids:
            raise RuntimeError("boom")
        return {
            "answer": f"answer {q['id']}", "retrieved_contexts": ["ctx 1", "ctx 2"],
            "contexts_meta": [{"chunk_id": "a:1", "ticker": "NVDA", "fiscal_year": 2026, "section": "Item 7"}] * 2,
            "citations": [], "guardrail_report": None, "hops": 1,
            "tokens": {"prompt": 10, "completion": 5, "total": 15}, "cost_usd": 0.0, "latency_ms": 1.0,
            "model": "fake", "provider": "fake",
        }


def test_generate_is_resumable_and_logs_failures(tmp_path):
    questions = [dict(QUESTION, id=f"GOLD-T{i}") for i in range(1, 4)]
    adapter = _FakeAdapter(fail_ids={"GOLD-T2"})
    counts = gen.generate({"fake": adapter}, questions, tmp_path, "test-run", commit="abc123")
    assert counts == {"generated": 2, "skipped": 0, "failed": 1}
    records = read_jsonl(tmp_path / RECORDS_FILE)
    assert [r["question_id"] for r in records] == ["GOLD-T1", "GOLD-T3"]
    rec = records[0]
    for key in ("schema_version", "run_id", "system", "question_id", "category", "question", "ground_truth_answer",
                "ground_truth_numbers", "target_sections", "git_commit", "timestamp", *ADAPTER_KEYS):
        assert key in rec
    errors = read_jsonl(tmp_path / GEN_ERRORS_FILE)
    assert [e["question_id"] for e in errors] == ["GOLD-T2"] and "RuntimeError" in errors[0]["error"]

    # Second run: done pairs skipped, only the failed one retried
    adapter.fail_ids.clear()
    adapter.calls.clear()
    counts = gen.generate({"fake": adapter}, questions, tmp_path, "test-run", commit="abc123")
    assert counts == {"generated": 1, "skipped": 2, "failed": 0}
    assert adapter.calls == ["GOLD-T2"]
    assert len(read_jsonl(tmp_path / RECORDS_FILE)) == 3


def test_adapter_missing_keys_is_a_failure(tmp_path):
    class Broken(SystemAdapter):
        def answer(self, q):
            return {"answer": "x"}

    counts = gen.generate({"broken": Broken()}, [QUESTION], tmp_path, "t", commit="x")
    assert counts["failed"] == 1
    assert "missing keys" in read_jsonl(tmp_path / GEN_ERRORS_FILE)[0]["error"]


def test_generate_does_not_import_ragas():
    code = (
        "import sys; import scripts.rq2.generate, scripts.rq2.adapters, scripts.rq2.common; "
        "print('ragas' in sys.modules)"
    )
    out = subprocess.run([sys.executable, "-c", code], cwd=REPO_ROOT, capture_output=True, text=True, timeout=120)
    assert out.returncode == 0, out.stderr
    assert out.stdout.strip().splitlines()[-1] == "False"
