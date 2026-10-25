"""Chat client: provider from .env (LLM_PROVIDER, default groq), API key from the environment or a hidden prompt."""
import getpass
import os
from functools import lru_cache
from pathlib import Path

from dotenv import load_dotenv

DEFAULT_MODEL = "openai/gpt-oss-120b"     # on Groq; with LLM_PROVIDER=openai pass --model
KEY_NAMES = {"groq": "GROQ_API_KEY", "openai": "OPENAI_API_KEY"}


@lru_cache(maxsize=1)
def get_client():
    load_dotenv(Path(__file__).resolve().parents[2] / ".env")   # no keys stored there
    provider = os.getenv("LLM_PROVIDER", "groq").strip().lower()
    if provider not in KEY_NAMES:
        raise ValueError(f"LLM_PROVIDER must be 'groq' or 'openai', got '{provider}'")
    if not os.environ.get(KEY_NAMES[provider]):
        os.environ[KEY_NAMES[provider]] = getpass.getpass(f"Enter your {KEY_NAMES[provider]}: ")
    if provider == "groq":
        from groq import Groq
        return Groq(max_retries=5)       # retries rate-limit (429) errors with backoff
    from openai import OpenAI
    return OpenAI(max_retries=5)


def chat(messages, model=DEFAULT_MODEL, temperature=0.0, max_tokens=1500):
    """One chat-completion call. Returns the reply text."""
    kwargs = dict(model=model, messages=messages, temperature=temperature, max_tokens=max_tokens)
    if "gpt-oss" in model:
        kwargs["reasoning_effort"] = "low"
    return get_client().chat.completions.create(**kwargs).choices[0].message.content
