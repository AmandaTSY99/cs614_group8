"""Chat client: provider from .env (LLM_PROVIDER, default groq), API key from the environment or a hidden prompt."""
import getpass
import os
import threading
from functools import lru_cache
from pathlib import Path

from dotenv import load_dotenv

DEFAULT_MODEL = "openai/gpt-oss-120b"     # on Groq; with LLM_PROVIDER=openai pass --model
KEY_NAMES = {"groq": "GROQ_API_KEY", "openai": "OPENAI_API_KEY", "gemini": "GEMINI_API_KEY", "mock": "MOCK_KEY"}
_EMPTY_TELEMETRY = {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0, "model": DEFAULT_MODEL, "provider": "mock"}
# Per thread, so concurrent answers (e.g. two visitors of the Streamlit demo) never read each other's usage
_TELEMETRY = threading.local()


def get_last_telemetry():
    return dict(getattr(_TELEMETRY, "last", _EMPTY_TELEMETRY))


def get_client():
    """Client for the current LLM_PROVIDER and its key. Cached per (provider, key), never across keys, so the
    demo's per-visitor keys (ui/live.py llm_session) are each used only for their own runs."""
    load_dotenv(Path(__file__).resolve().parents[2] / ".env")   # no keys stored there
    provider = os.getenv("LLM_PROVIDER", "groq").strip().lower()
    if provider in KEY_NAMES and provider != "mock" and not os.environ.get(KEY_NAMES[provider]):
        import sys
        if sys.stdin and sys.stdin.isatty():
            os.environ[KEY_NAMES[provider]] = getpass.getpass(f"Enter your {KEY_NAMES[provider]}: ")
        else:
            raise ValueError(f"Missing environment variable {KEY_NAMES[provider]} for provider '{provider}'")
    return _client_for(provider, os.environ.get(KEY_NAMES.get(provider, ""), ""))


@lru_cache(maxsize=8)
def _client_for(provider, api_key):
    if provider == "mock":
        class _MockChoice:
            message = type("Msg", (), {"content": "Mock System A answer [1]."})()
        class _MockUsage:
            prompt_tokens = 60
            completion_tokens = 25
            total_tokens = 85
        class _MockCompletions:
            def create(self, **kwargs):
                return type("Resp", (), {"choices": [_MockChoice()], "usage": _MockUsage(), "model": kwargs.get("model", "mock")})()
        return type("MockClient", (), {"chat": type("Chat", (), {"completions": _MockCompletions()})()})()

    if provider not in KEY_NAMES:
        raise ValueError(f"LLM_PROVIDER must be 'groq' or 'openai', got '{provider}'")
    if provider == "groq":
        from groq import Groq
        return Groq(api_key=api_key, max_retries=5, timeout=90)       # retries rate-limit (429) errors with backoff
    from openai import OpenAI
    return OpenAI(api_key=api_key, max_retries=5, timeout=90)


def chat(messages, model=None, temperature=0.0, max_tokens=1500):
    """One chat-completion call. Returns the reply text."""
    provider = os.getenv("LLM_PROVIDER", "groq").strip().lower()
    if not model or model == DEFAULT_MODEL:
        model = os.getenv("LLM_MODEL") or ("gpt-4o-mini" if provider == "openai" else DEFAULT_MODEL)
    if provider == "gemini":
        from src.system_c.llm import _call_gemini_native
        m = "gemini-3-flash-preview" if ("flash" in model or model == DEFAULT_MODEL) else model
        content, p_tok, c_tok = _call_gemini_native(m, messages, temperature=temperature)
        _TELEMETRY.last = {
            "prompt_tokens": p_tok,
            "completion_tokens": c_tok,
            "total_tokens": p_tok + c_tok,
            "model": m,
            "provider": "gemini",
        }
        return content

    kwargs = dict(model=model, messages=messages, temperature=temperature)
    if provider == "openai" or "gpt-5" in model or "o1" in model or "o3" in model:
        kwargs["max_completion_tokens"] = max_tokens
    else:
        kwargs["max_tokens"] = max_tokens
    if "gpt-oss" in model:
        kwargs["reasoning_effort"] = "low"
    res = get_client().chat.completions.create(**kwargs)
    usage = getattr(res, "usage", None)
    provider = os.getenv("LLM_PROVIDER", "groq").strip().lower()
    _TELEMETRY.last = {
        "prompt_tokens": getattr(usage, "prompt_tokens", 0) or 0,
        "completion_tokens": getattr(usage, "completion_tokens", 0) or 0,
        "total_tokens": getattr(usage, "total_tokens", 0) or 0,
        "model": getattr(res, "model", model) or model,
        "provider": provider,
    }
    return res.choices[0].message.content
