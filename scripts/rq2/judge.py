"""
RQ2 Stage 2 judge plumbing (`cs614-eval` env): judge LLM + local embeddings for ragas 0.4.3, error
classification, retry with exponential backoff, and per-call usage / rate-limit metering.

The judge talks to an OpenAI-compatible endpoint through `openai` 1.x (Groq: api.groq.com/openai/v1).
"""

import asyncio
import contextvars
import json
import os
import random
from typing import Any, Awaitable, Callable, Dict, Optional, Tuple

JUDGE_ENDPOINTS = {
    "groq": ("https://api.groq.com/openai/v1", "GROQ_API_KEY"),
    "openai": (None, "OPENAI_API_KEY"),
}
DEFAULT_JUDGE_PROVIDER = "groq"
DEFAULT_JUDGE_MODEL = "openai/gpt-oss-120b"
EMBEDDING_MODEL = "BAAI/bge-small-en-v1.5"
JUDGE_TIMEOUT_S = 90.0

MAX_ATTEMPTS = 6
BASE_DELAY_S = 2.0  # 2, 4, 8, 16, 32 s (+ jitter) between the 6 attempts

TOO_LARGE_MARKERS = (
    "context_length_exceeded", "context length", "maximum context", "request too large",
    "reduce the length", "too many tokens", "request_too_large", "prompt is too long",
)
RATELIMIT_HEADER_PREFIXES = ("x-ratelimit-", "retry-after")

# Status values written to scores.jsonl
STATUS_OK, STATUS_NA, STATUS_ERROR, STATUS_TOO_LARGE = "ok", "na", "error", "too_large"
ERROR_TOO_LARGE, ERROR_RETRYABLE, ERROR_FATAL = "too_large", "retryable", "fatal"


def judge_label(provider: str, model: str) -> str:
    return f"{provider}/{model}"


def _exception_chain(exc: BaseException):
    seen = set()
    while exc is not None and id(exc) not in seen:
        seen.add(id(exc))
        yield exc
        # Instructor / ragas wrap provider errors; look through the wrappers.
        nested = getattr(exc, "last_exception", None) or getattr(exc, "__cause__", None) or exc.__context__
        exc = nested


def classify_error(exc: BaseException) -> str:
    """
    `too_large` (request / context too large: never retried), `retryable` (rate limit, timeout, connection,
    5xx) or `fatal` (anything else: not retried).
    """
    import httpx
    import openai

    chain = list(_exception_chain(exc))
    for e in chain:
        status = getattr(e, "status_code", None)
        text = f"{type(e).__name__} {e}".lower()
        if status == 413 or any(m in text for m in TOO_LARGE_MARKERS):
            return ERROR_TOO_LARGE
    for e in chain:
        status = getattr(e, "status_code", None)
        if isinstance(e, (openai.RateLimitError, openai.APITimeoutError, openai.APIConnectionError,
                          openai.InternalServerError, asyncio.TimeoutError, httpx.TimeoutException,
                          httpx.TransportError)):
            return ERROR_RETRYABLE
        if status == 429 or (isinstance(status, int) and status >= 500):
            return ERROR_RETRYABLE
    return ERROR_FATAL


class JudgeCallError(Exception):
    def __init__(self, kind: str, attempts: int, cause: BaseException):
        super().__init__(f"{kind} after {attempts} attempt(s): {type(cause).__name__}: {cause}")
        self.kind = kind
        self.attempts = attempts
        self.cause = cause


async def call_with_retry(
    fn: Callable[[], Awaitable[Any]],
    max_attempts: int = MAX_ATTEMPTS,
    base_delay: float = BASE_DELAY_S,
    sleep: Callable[[float], Awaitable[None]] = asyncio.sleep,
) -> Tuple[Any, int]:
    """Run `fn`, retrying only retryable errors with exponential backoff. Returns `(result, attempts)`."""
    for attempt in range(1, max_attempts + 1):
        try:
            return await fn(), attempt
        except Exception as exc:
            kind = classify_error(exc)
            if kind != ERROR_RETRYABLE or attempt == max_attempts:
                raise JudgeCallError(kind if kind != ERROR_RETRYABLE else "retries_exhausted", attempt, exc) from exc
            await sleep(base_delay * (2 ** (attempt - 1)) + random.uniform(0, 1))
    raise AssertionError("unreachable")


class JudgeMeter:
    """
    Counts judge HTTP calls and tokens per (system, question_id, metric), and keeps the latest rate-limit
    headers, via an httpx response hook on the judge client. The current key lives in a context variable
    set by the scorer around each metric call.
    """

    def __init__(self) -> None:
        self.current: contextvars.ContextVar[Optional[Tuple[str, str, str]]] = contextvars.ContextVar(
            "rq2_judge_key", default=None
        )
        self.usage: Dict[Tuple[str, str, str], Dict[str, Any]] = {}
        self.last_ratelimit: Dict[str, str] = {}

    def start(self, key: Tuple[str, str, str]) -> None:
        self.current.set(key)
        self.usage[key] = {"calls": 0, "prompt_tokens": 0, "completion_tokens": 0, "ratelimit": {}}

    def snapshot(self, key: Tuple[str, str, str]) -> Dict[str, Any]:
        return dict(self.usage.get(key, {"calls": 0, "prompt_tokens": 0, "completion_tokens": 0, "ratelimit": {}}))

    async def on_response(self, response: Any) -> None:
        headers = {k.lower(): v for k, v in response.headers.items()
                   if k.lower().startswith(RATELIMIT_HEADER_PREFIXES)}
        if headers:
            self.last_ratelimit = headers
        key = self.current.get()
        if key is None or key not in self.usage:
            return
        entry = self.usage[key]
        entry["calls"] += 1
        if headers:
            entry["ratelimit"] = headers
        try:
            await response.aread()
            usage = (json.loads(response.content) or {}).get("usage") or {}
        except Exception:
            usage = {}
        entry["prompt_tokens"] += int(usage.get("prompt_tokens") or 0)
        entry["completion_tokens"] += int(usage.get("completion_tokens") or 0)


def build_judge(provider: str, model: str, meter: Optional[JudgeMeter] = None) -> Any:
    """ragas 0.4.3 `InstructorBaseRagasLLM` over an OpenAI-compatible async client (no client-side retries)."""
    import httpx
    from openai import AsyncOpenAI
    from ragas.llms import llm_factory

    if provider not in JUDGE_ENDPOINTS:
        raise ValueError(f"Unsupported judge provider '{provider}'; use one of {sorted(JUDGE_ENDPOINTS)}")
    base_url, key_var = JUDGE_ENDPOINTS[provider]
    api_key = os.environ.get(key_var)
    if not api_key:
        raise RuntimeError(f"{key_var} is not set (load it from .env)")
    hooks = {"response": [meter.on_response]} if meter else {}
    http_client = httpx.AsyncClient(timeout=JUDGE_TIMEOUT_S, event_hooks=hooks)
    client = AsyncOpenAI(api_key=api_key, base_url=base_url, max_retries=0, timeout=JUDGE_TIMEOUT_S,
                         http_client=http_client)
    return llm_factory(model, provider="openai", client=client, temperature=0.0)


def build_embeddings() -> Any:
    """Local sentence-transformers embeddings for Answer Relevancy (downloads the model on first use)."""
    from ragas.embeddings import HuggingFaceEmbeddings

    return HuggingFaceEmbeddings(model=EMBEDDING_MODEL, device="cpu")
