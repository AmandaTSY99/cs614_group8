"""Architectural contract tests enforcing dataset purity, anti-leakage firewall, embedding parity, and plug-and-play adapters."""
import json
from pathlib import Path
from typing import Any, Dict
from unittest.mock import patch
import pytest

from scripts.rq2.adapters import ADAPTER_KEYS, get_adapters

REPO_ROOT = Path(__file__).resolve().parents[1]
BENCHMARK_2015_PATH = REPO_ROOT / "data" / "benchmark_qa_pool_2015.json"


@pytest.fixture(autouse=True)
def force_mock_env(monkeypatch):
    """Enforce mock environment for ultra-fast, deterministic architectural testing."""
    monkeypatch.setenv("LLM_PROVIDER", "mock")


def test_no_legacy_golden_dataset_anywhere():
    """Invariant 1: Assert legacy golden dataset and builder scripts are completely purged."""
    assert not (REPO_ROOT / "data" / "golden_eval_set.json").exists(), "data/golden_eval_set.json must not exist!"
    assert not (REPO_ROOT / "scripts" / "build_golden_eval_set.py").exists(), "scripts/build_golden_eval_set.py must not exist!"
    assert not (REPO_ROOT / "tests" / "test_golden_eval_set.py").exists(), "tests/test_golden_eval_set.py must not exist!"

    # Verify no active codebase file references golden_eval_set.json
    active_dirs = [REPO_ROOT / "src", REPO_ROOT / "scripts", REPO_ROOT / ".github"]
    violations = []
    for d in active_dirs:
        for p in d.rglob("*"):
            if p.is_file() and p.suffix in (".py", ".yml", ".yaml"):
                content = p.read_text(encoding="utf-8", errors="ignore")
                if "golden_eval_set.json" in content:
                    violations.append(str(p.relative_to(REPO_ROOT)))
    assert not violations, f"Forbidden references to golden_eval_set.json found in: {violations}"


def test_benchmark_strictly_2015_onwards():
    """Invariant 2: Assert canonical benchmark is strictly 2015+."""
    assert BENCHMARK_2015_PATH.is_file(), f"{BENCHMARK_2015_PATH} must exist!"
    records = json.loads(BENCHMARK_2015_PATH.read_text(encoding="utf-8"))
    assert len(records) >= 40, f"Expected at least 40 benchmark questions, found {len(records)}"

    for r in records:
        years = set()
        if r.get("year"):
            years.add(int(r["year"]))
        for ev in r.get("gold_evidence", []):
            if ev.get("year"):
                years.add(int(ev["year"]))
        assert years, f"Question {r['id']} has no year metadata!"
        assert all(y >= 2015 for y in years), f"Question {r['id']} contains pre-2015 filing year: {years}"


def test_anti_leakage_firewall_all_systems():
    """Invariant 3: Ground-truth answers, programs, quotes, and sections must NEVER enter retrieval or prompts."""
    canary_qa = {
        "id": "CANARY-999",
        "question": "What was NVIDIA data center revenue in FY2026?",
        "query": "What was NVIDIA data center revenue in FY2026?",
        "ticker": "NVDA",
        "target_tickers": ["NVDA"],
        "year": 2026,
        "fiscal_years": [2026],
        "answer": "CANARY_SECRET_ANSWER_999",
        "program": "CANARY_SECRET_PROGRAM_999",
        "key_points": ["CANARY_SECRET_KEYPOINT_999"],
        "gold_evidence": [
            {
                "doc_id": "NVDA_FY2026",
                "ticker": "NVDA",
                "year": 2026,
                "quote": "CANARY_SECRET_QUOTE_999",
                "item": "CANARY_SECRET_ITEM_999",
                "heading": "CANARY_SECRET_HEADING_999",
            }
        ]
    }
    canary_tokens = [
        "CANARY_SECRET_ANSWER_999",
        "CANARY_SECRET_PROGRAM_999",
        "CANARY_SECRET_KEYPOINT_999",
        "CANARY_SECRET_QUOTE_999",
        "CANARY_SECRET_ITEM_999",
        "CANARY_SECRET_HEADING_999",
    ]

    adapters = get_adapters(["system_a", "system_b", "system_c_v1", "system_c_v2"])
    for name, adapter in adapters.items():
        out = adapter.answer(canary_qa)
        # Inspect all retrieved contexts
        contexts_str = " ".join(out.get("retrieved_contexts", []))
        for token in canary_tokens:
            assert token not in contexts_str, f"Leakage detected! Ground-truth token '{token}' leaked into {name} retrieved contexts!"
            assert token not in str(out.get("contexts_meta", [])), f"Leakage detected! Ground-truth token '{token}' leaked into {name} contexts_meta!"


def test_embedding_model_and_prefix_parity():
    """Invariant 4: Assert System A, System B, and System C share the exact same embedding model & prefix."""
    from src.system_a.retrieval import EMBED_MODEL as SYS_A_MODEL, BGE_QUERY_PREFIX as SYS_A_PREFIX
    from src.system_b.adapters import BGE_MODEL as SYS_B_MODEL, BGE_PREFIX as SYS_B_PREFIX
    from src.system_c.nodes.retriever import EMBED_MODEL as SYS_C_MODEL, BGE_QUERY_PREFIX as SYS_C_PREFIX

    assert SYS_A_MODEL == "BAAI/bge-small-en-v1.5"
    assert SYS_B_MODEL == "BAAI/bge-small-en-v1.5"
    assert SYS_C_MODEL == "BAAI/bge-small-en-v1.5"

    assert SYS_A_PREFIX == "Represent this sentence for searching relevant passages: "
    assert SYS_B_PREFIX == "Represent this sentence for searching relevant passages: "
    assert SYS_C_PREFIX == "Represent this sentence for searching relevant passages: "


def test_plug_and_play_adapter_schema_all_systems():
    """Invariant 5: All 4+1 systems must run on real 2015+ benchmark items and return complete telemetry."""
    records = json.loads(BENCHMARK_2015_PATH.read_text(encoding="utf-8"))
    sample_q = records[0]  # amanda-001 or amanda-002

    systems = ["system_a", "system_b", "system_c_v1", "system_c_v2", "system_c_fixed_3hop"]
    adapters = get_adapters(systems)

    for sys_name, adapter in adapters.items():
        out = adapter.answer(sample_q)
        assert set(out) == set(ADAPTER_KEYS), f"{sys_name} missing keys from ADAPTER_KEYS: {set(ADAPTER_KEYS) - set(out)}"
        assert out["answer"], f"{sys_name} returned empty answer"
        assert len(out["retrieved_contexts"]) > 0, f"{sys_name} returned 0 retrieved contexts"
        assert len(out["contexts_meta"]) == len(out["retrieved_contexts"])
        assert out["hops"] >= 1
        assert out["tokens"]["total"] > 0
        assert out["latency_ms"] >= 0.0
        assert "stage_timings_ms" in out
        assert out["model"]
        assert out["provider"]
