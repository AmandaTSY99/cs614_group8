"""Chat client: provider from .env (LLM_PROVIDER, default groq), API key from the environment or a hidden prompt."""
import getpass
import os
from functools import lru_cache
from pathlib import Path

from dotenv import load_dotenv

DEFAULT_MODEL = "openai/gpt-oss-120b"     # on Groq; with LLM_PROVIDER=openai pass --model
KEY_NAMES = {"groq": "GROQ_API_KEY", "openai": "OPENAI_API_KEY", "mock": "MOCK_KEY"}
LAST_TELEMETRY = {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0, "model": DEFAULT_MODEL, "provider": "mock"}


def get_last_telemetry():
    return dict(LAST_TELEMETRY)


@lru_cache(maxsize=1)
def get_client():
    load_dotenv(Path(__file__).resolve().parents[2] / ".env")   # no keys stored there
    provider = os.getenv("LLM_PROVIDER", "groq").strip().lower()
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
    if not os.environ.get(KEY_NAMES[provider]):
        import sys
        if sys.stdin and sys.stdin.isatty():
            os.environ[KEY_NAMES[provider]] = getpass.getpass(f"Enter your {KEY_NAMES[provider]}: ")
        else:
            raise ValueError(f"Missing environment variable {KEY_NAMES[provider]} for provider '{provider}'")
    if provider == "groq":
        from groq import Groq
        return Groq(max_retries=5)       # retries rate-limit (429) errors with backoff
    from openai import OpenAI
    return OpenAI(max_retries=5)


def chat(messages, model=DEFAULT_MODEL, temperature=0.0, max_tokens=1500):
    """One chat-completion call. Returns the reply text."""
    global LAST_TELEMETRY
    kwargs = dict(model=model, messages=messages, temperature=temperature, max_tokens=max_tokens)
    if "gpt-oss" in model:
        kwargs["reasoning_effort"] = "low"
    res = get_client().chat.completions.create(**kwargs)
    usage = getattr(res, "usage", None)
    provider = os.getenv("LLM_PROVIDER", "groq").strip().lower()
    LAST_TELEMETRY = {
        "prompt_tokens": getattr(usage, "prompt_tokens", 0) or 0,
        "completion_tokens": getattr(usage, "completion_tokens", 0) or 0,
        "total_tokens": getattr(usage, "total_tokens", 0) or 0,
        "model": getattr(res, "model", model) or model,
        "provider": provider,
    }
    return res.choices[0].message.content
