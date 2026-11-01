"""The demo's per-run LLM settings must not leak a visitor's API key to other visitors of the Space."""

import os
import threading

import pytest

from ui import live


@pytest.fixture
def space_env(monkeypatch):
    baseline = {name: None for name in live._ENV_NAMES}
    baseline.update({"GROQ_API_KEY": "space-groq", "GEMINI_API_KEY": "space-gemini"})
    monkeypatch.setattr(live, "_BASELINE", baseline)
    for name in live._ENV_NAMES:
        monkeypatch.delenv(name, raising=False)
    monkeypatch.setenv("GROQ_API_KEY", "space-groq")
    monkeypatch.setenv("GEMINI_API_KEY", "space-gemini")
    return baseline


def test_space_providers_follow_available_secrets(space_env):
    assert live.space_providers() == ["groq", "gemini"]


def test_visitor_key_is_used_only_during_the_run(space_env):
    with live.llm_session("groq", "openai/gpt-oss-120b", api_key="visitor-key"):
        assert os.environ["GROQ_API_KEY"] == "visitor-key"
        assert os.environ["LLM_PROVIDER"] == "groq"
    assert os.environ["GROQ_API_KEY"] == "space-groq"
    assert "LLM_PROVIDER" not in os.environ


def test_space_key_used_when_visitor_brings_none(space_env):
    with live.llm_session("gemini", "gemini-3-flash-preview"):
        assert os.environ["GEMINI_API_KEY"] == "space-gemini"
        assert os.environ["LLM_MODEL"] == "gemini-3-flash-preview"


def test_run_with_other_settings_waits_for_active_run(space_env):
    order = []
    first_in = threading.Event()
    release_first = threading.Event()

    def first():
        with live.llm_session("groq", "openai/gpt-oss-120b"):
            order.append("first-start")
            first_in.set()
            release_first.wait(2)
            order.append("first-end")

    def second():
        first_in.wait(2)
        with live.llm_session("groq", "openai/gpt-oss-120b", api_key="visitor-key"):
            order.append(("second", os.environ["GROQ_API_KEY"]))

    t1, t2 = threading.Thread(target=first), threading.Thread(target=second)
    t1.start(), t2.start()
    first_in.wait(2)
    release_first.set()
    t1.join(3), t2.join(3)
    assert order == ["first-start", "first-end", ("second", "visitor-key")]
    assert os.environ["GROQ_API_KEY"] == "space-groq"


def test_system_a_client_is_not_shared_across_visitor_keys(space_env, monkeypatch):
    from src.system_a import llm as system_a_llm

    monkeypatch.setattr(system_a_llm, "load_dotenv", lambda *a, **k: None)
    with live.llm_session("openai", "gpt-5.4", api_key="visitor-a"):
        first = system_a_llm.get_client()
    with live.llm_session("openai", "gpt-5.4", api_key="visitor-b"):
        second = system_a_llm.get_client()
    with live.llm_session("groq", "openai/gpt-oss-120b"):
        third = system_a_llm.get_client()
    assert first is not second
    assert first.api_key == "visitor-a" and second.api_key == "visitor-b"
    assert third.api_key == "space-groq"
