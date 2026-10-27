"""
Active Hallucination & Numerical Grounding Guardrail Node for System C.

Owned by: Aryan (Citations, Guardrails & RQ2 Lead)
Integration Contract:
- Inspects `draft_answer` (or `final_answer`) against `accumulated_evidence`.
- Splits the answer into sentences and resolves each sentence's inline citation tags to chunk_ids.
- Step B (deterministic): every dollar figure / percentage / bps / comma-or-decimal number is checked
  against ONLY the chunks cited in its own sentence -> verified | derived | ungrounded | uncited.
- Step C (LLM, switchable via `GUARDRAIL_SEMANTIC_CHECK`): one batched `call_llm` judging cited,
  number-free factual sentences -> supported | partial | unsupported (| unchecked on parse failure).
- Populates `guardrail_passed` and `guardrail_report` (legacy RQ2 keys plus sentence-level output).
- Output keys are exactly the handoff contract: `final_answer`, `guardrail_passed`, `guardrail_report`,
  `telemetry`. `citations` are rebuilt by `repair_node` when it rewrites the answer.
"""

import json
import os
import re
from typing import Any, Dict, List, Optional, Tuple

from src.system_c.guardrails.citations import (
    BRACKET_RE,
    find_citation_tags,
    resolve_citation_tags,
    split_sentences,
)
from src.system_c.guardrails.scale_normalizer import SCALE_MULTIPLIERS, detect_context_scale_multiplier
from src.system_c.llm import call_llm, get_llm_config
from src.system_c.state import AdaptiveRAGState
from src.system_c.telemetry import track_node_latency

# Numbers with optional `$`, then optional percent / bps / scale suffix.
# Single-letter scales (`$5B`, `12M`) are case-sensitive and must touch the number.
NUMBER_RE = re.compile(
    r"(?<![\w.])(?P<dollar>\$\s?)?"
    # A comma-grouped number may not run on into more digits (`28,391035000000` is not 28,391)
    r"(?P<num>\d{1,3}(?:,\d{3})+(?!\d)(?:\.\d+)?|\d+(?:\.\d+)?)"
    r"(?:(?P<pct>\s?%|\s?percent\b|\s?per\s?cent\b)"
    r"|(?P<bps>\s?bps\b|\s?basis\s+points?\b)"
    r"|(?P<scale>\s?(?:trillion|billion|million|thousand|bn|mn)\b|(?-i:[TBMK])\b))?",
    re.IGNORECASE,
)
YEAR_RE = re.compile(r"199\d|20[0-3]\d")
SCALE_WORDS = {"bn": 1e9, "mn": 1e6, **SCALE_MULTIPLIERS}
SEMANTIC_VERDICTS = ("supported", "partial", "unsupported")
MAX_DERIVATION_CANDIDATES = 150
SEMANTIC_CHUNK_CHARS = 1500

SEMANTIC_SYSTEM_PROMPT = """You are a strict faithfulness judge for answers grounded in SEC 10-K filings.
For each numbered sentence you receive, decide whether its cited evidence supports it
(sentences marked "uncited" are judged against ALL RETRIEVED EVIDENCE instead).
A sentence stating that information is not disclosed or not available is "supported" ONLY if the evidence
really does not contain that information; if the evidence contains it, the sentence is "unsupported".
- "supported": every claim in the sentence is stated in or directly implied by the cited evidence.
- "partial": some claims are supported, others are missing from the cited evidence.
- "unsupported": the cited evidence does not support the sentence, or contradicts it.
Return ONLY JSON: {"results": [{"id": <int>, "verdict": "supported|partial|unsupported", "reason": "<one short sentence>"}]}"""


# ---------------------------------------------------------------------------
# Step A: sentences and citations
# ---------------------------------------------------------------------------


# Moved to `guardrails/citations.py` (shared with the synthesizer); old private names kept for callers/tests.
_split_sentences = split_sentences
_find_citation_tags = find_citation_tags
_resolve_citation_tags = resolve_citation_tags


# ---------------------------------------------------------------------------
# Step B: numbers
# ---------------------------------------------------------------------------


def _parse_number_match(m: "re.Match[str]") -> Dict[str, Any]:
    num_str = m.group("num")
    pct, bps, scale = m.group("pct"), m.group("bps"), m.group("scale")
    num = float(num_str.replace(",", ""))
    if pct:
        kind, mult = "percent", 1.0
    elif bps:
        kind, mult = "bps", 1.0
    else:
        kind = "currency" if m.group("dollar") else "number"
        mult = SCALE_WORDS.get(scale.strip().lower(), 1.0) if scale else 1.0
    decimals = len(num_str.split(".")[1]) if "." in num_str else 0
    token_end = m.end("pct") if pct else m.end("num")
    return {
        "value": m.group(0).strip(),
        "token": m.string[m.start("num"):token_end].strip(),
        "kind": kind,
        "number": num,
        "magnitude": num * mult,
        "scale": mult,
        "decimals": decimals,
        "explicit_scale": bool(scale),
        "plain": not (m.group("dollar") or pct or bps or scale or "," in num_str or "." in num_str),
    }


def _extract_numbers(text: str) -> List[Dict[str, Any]]:
    """
    Extract quantitative claims: dollar amounts with scale words (`$500 million`, `$5B`), percentages
    (`12%`, `12 percent`), basis points (`50 bps`) and any number with commas or decimals.
    Skips `[...]` tags, 4-digit years (1990-2039) and small plain integers used as counts.
    """
    text_no_cites = BRACKET_RE.sub(" ", text)
    numbers = []
    for m in NUMBER_RE.finditer(text_no_cites):
        info = _parse_number_match(m)
        if info["plain"]:
            raw = m.group("num")
            if YEAR_RE.fullmatch(raw) or len(raw) <= 3:
                continue
        numbers.append(info)
    return numbers


def _extract_candidate_numbers(text: str) -> List[str]:
    """Legacy helper: the extracted numbers as plain tokens (e.g. `'999,999'`, `'75.0%'`)."""
    return [n["token"] for n in _extract_numbers(text)]


def _chunk_values(content: str, chunk_id: str = "") -> List[Dict[str, Any]]:
    """
    All numeric values in a chunk, keyed by kind. Plain/currency numbers without an explicit scale
    also get a copy multiplied by the chunk's "(in millions)"-style header scale.
    XBRL blocks (`F-...` chunk ids) are CSV: each comma-separated field is parsed as its own number.
    Each value carries `bare` (no scale word / percent) and `digits` for the exact-digits fallback.
    """
    if str(chunk_id).startswith("F-"):
        return _xbrl_values(content)
    doc_scale = detect_context_scale_multiplier(content)
    values = []
    for m in NUMBER_RE.finditer(content):
        info = _parse_number_match(m)
        if info["plain"] and YEAR_RE.fullmatch(m.group("num")):
            continue
        family = "percent" if info["kind"] in ("percent", "bps") else "amount"
        pct_value = info["number"] / 100.0 if info["kind"] == "bps" else info["number"]
        base = {"family": family, "raw": info["token"], "scaled": False, "bare": False, "digits": _digits(m.group("num"))}
        if family == "percent":
            values.append({**base, "value": pct_value})
            continue
        values.append({**base, "value": info["magnitude"], "bare": not info["explicit_scale"]})
        if doc_scale != 1.0 and not info["explicit_scale"]:
            values.append({**base, "value": info["number"] * doc_scale, "scaled": True})
    return values


def _xbrl_values(content: str) -> List[Dict[str, Any]]:
    """Numbers in an XBRL CSV block, one per comma-separated field (dates, years and text skipped)."""
    values = []
    for line in content.splitlines():
        for field in line.split(","):
            field = field.strip()
            if not re.fullmatch(r"-?\d+(?:\.\d+)?", field) or YEAR_RE.fullmatch(field):
                continue
            values.append(
                {"value": float(field), "family": "amount", "raw": field, "scaled": False, "bare": True, "digits": _digits(field)}
            )
    return values


def _digits(num_str: str) -> str:
    return re.sub(r"[^\d.]", "", num_str).rstrip(".")


def _significant_digits(digits: str) -> int:
    return len(digits.replace(".", "").lstrip("0"))


def _claim_value(num: Dict[str, Any]) -> Tuple[float, str, float]:
    """`(value, family, tolerance)` where tolerance is half a unit of the precision the answer states."""
    half_unit = 0.5 * (10 ** -num["decimals"])
    if num["kind"] == "percent":
        return num["number"], "percent", half_unit
    if num["kind"] == "bps":
        return num["number"] / 100.0, "percent", half_unit / 100.0
    return num["magnitude"], "amount", half_unit * num["scale"]


def _within(a: float, b: float, tol: float) -> bool:
    return abs(a - b) <= tol + 1e-9 * max(abs(a), abs(b), 1.0)


def _match_number_in_chunks(num: Dict[str, Any], chunks: List[Dict[str, Any]]) -> bool:
    """
    True if `num` appears (to the stated precision, with scale normalisation) in any of `chunks`.
    Fallback for unitless evidence: an answer figure with a scale word (`$350,018 million`) also verifies
    against a bare evidence number (`$350,018`, no scale header) when the full digit string matches exactly
    and has at least 4 significant digits. `chunks` are always the sentence's own cited chunks.
    """
    claim, family, tol = _claim_value(num)
    claim_digits = _digits(num["token"])
    for ch in chunks:
        for cand in _chunk_values(ch.get("content", ""), ch.get("chunk_id", "")):
            if cand["family"] != family:
                continue
            if _within(claim, cand["value"], tol):
                return True
            if (
                num["explicit_scale"]
                and cand["bare"]
                and not cand["scaled"]
                and cand["digits"] == claim_digits
                and _significant_digits(claim_digits) >= 4
            ):
                return True
    return False


def _is_derived(num: Dict[str, Any], chunks: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    """
    Check whether `num` is computed from figures in `chunks`, matched to the precision the answer states:
    - percentages: growth `(b - a) / a` or ratio `a / b` of two amounts, or difference of two percentages;
    - amounts: difference of two amounts (same scale basis).
    Returns `{"derived_from": [...], "operation": ...}` or None.
    """
    claim, family, tol = _claim_value(num)
    cands: List[Dict[str, Any]] = []
    seen = set()
    for ch in chunks:
        for c in _chunk_values(ch.get("content", ""), ch.get("chunk_id", "")):
            key = (c["family"], c["scaled"], c["value"])
            if key not in seen and c["value"] != 0.0:
                seen.add(key)
                cands.append(c)
    cands = cands[:MAX_DERIVATION_CANDIDATES]
    amounts = [c for c in cands if c["family"] == "amount"]
    percents = [c for c in cands if c["family"] == "percent"]

    def found(a: Dict[str, Any], b: Dict[str, Any], op: str) -> Dict[str, Any]:
        return {"derived_from": [a["raw"], b["raw"]], "operation": op}

    if family == "percent":
        for a in amounts:
            for b in amounts:
                if a is b or a["scaled"] != b["scaled"]:
                    continue
                if _within(claim, abs((b["value"] - a["value"]) / a["value"]) * 100.0, tol):
                    return found(b, a, "growth")
                if _within(claim, a["value"] / b["value"] * 100.0, tol):
                    return found(a, b, "ratio")
        for a in percents:
            for b in percents:
                if a is not b and _within(claim, abs(a["value"] - b["value"]), tol):
                    return found(a, b, "difference")
        return None

    # Unitless evidence (same rule as verification): `$104,896 million` vs bare `350,018 - 245,122`
    bare_ok = num["explicit_scale"] and _significant_digits(_digits(num["token"])) >= 4
    bare_tol = 0.5 * (10 ** -num["decimals"])
    for a in amounts:
        for b in amounts:
            if a is b:
                continue
            if a["scaled"] == b["scaled"] and _within(claim, abs(a["value"] - b["value"]), tol):
                return found(a, b, "difference")
            if (
                bare_ok
                and a["bare"] and b["bare"] and not a["scaled"] and not b["scaled"]
                and _within(num["number"], abs(a["value"] - b["value"]), bare_tol)
            ):
                return found(a, b, "difference")
    return None


def verify_numerical_grounding(answer: str, evidence_chunks: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Steps A, B and D of the guardrail (no LLM). Each number is checked only against the chunks cited in
    its own sentence. The semantic verdicts are filled in later by `guardrail_node` when enabled.
    """
    chunk_by_id = {str(c["chunk_id"]): c for c in evidence_chunks}
    sentences: List[Dict[str, Any]] = []
    invalid_citations: List[str] = []
    verified: List[str] = []
    ungrounded: List[str] = []
    uncited: List[str] = []
    derived: List[Dict[str, Any]] = []

    for text in _split_sentences(answer):
        tags, chunk_ids, invalid = _resolve_citation_tags(text, evidence_chunks)
        for tag in invalid:
            if tag not in invalid_citations:
                invalid_citations.append(tag)
        cited_chunks = [chunk_by_id[cid] for cid in chunk_ids]

        numbers_out = []
        for num in _extract_numbers(text):
            entry: Dict[str, Any] = {"value": num["value"]}
            if not cited_chunks:
                entry["status"] = "uncited"
                uncited.append(num["token"])
            elif _match_number_in_chunks(num, cited_chunks):
                entry["status"] = "verified"
                verified.append(num["token"])
            else:
                derivation = _is_derived(num, cited_chunks)
                if derivation:
                    entry.update({"status": "derived", **derivation})
                    derived.append({"value": num["value"], **derivation})
                    verified.append(num["token"])  # legacy list counts derived figures as grounded
                else:
                    entry["status"] = "ungrounded"
                    ungrounded.append(num["token"])
            numbers_out.append(entry)

        sentences.append(
            {
                "text": text,
                "citations": tags,
                "chunk_ids": chunk_ids,
                "numbers": numbers_out,
                "semantic_verdict": None,
                "reason": "",
            }
        )

    total = len(verified) + len(ungrounded) + len(uncited)  # `verified` already includes derived figures
    checked = total - len(derived)
    error_rate = round((len(ungrounded) + len(uncited)) / checked, 4) if checked > 0 else 0.0

    report = {
        "total_numerical_claims": total,
        # Legacy list: directly matched plus derived figures (derived ones are also listed in `derived_numbers`)
        "verified_numbers": verified,
        # Legacy list read by app.py / mock repair: every number that failed (ungrounded + uncited).
        "ungrounded_numbers": ungrounded + uncited,
        "uncited_numbers": uncited,
        "derived_numbers": derived,
        "numerical_grounding_error_rate": error_rate,
        "faithfulness_score": round(1.0 - error_rate, 4),
        "has_inline_citations": bool(_find_citation_tags(answer)),
        "invalid_citations": invalid_citations,
        "sentences": sentences,
        "unverified_sentences": [],
        "unchecked_sentences": [],
        # Uncited, number-free factual sentences (judged against all evidence when the semantic check is on)
        "uncited_claim_sentences": [s["text"] for s in sentences if not s["chunk_ids"] and _is_factual_claim(s)],
        "semantic_check_enabled": False,
        "semantic_judge_provider": None,
        "semantic_judge_model": None,
    }
    _finalize_report(report)
    return report


# ---------------------------------------------------------------------------
# Step C: semantic sentence check
# ---------------------------------------------------------------------------


def semantic_check_enabled() -> bool:
    return os.getenv("GUARDRAIL_SEMANTIC_CHECK", "1").strip().lower() not in ("0", "false", "no", "off")


def _judge_override() -> Dict[str, str]:
    """`provider` / `model` overrides for the judge call from `GUARDRAIL_JUDGE_PROVIDER` / `GUARDRAIL_JUDGE_MODEL`."""
    override = {}
    for key, env in (("provider", "GUARDRAIL_JUDGE_PROVIDER"), ("model", "GUARDRAIL_JUDGE_MODEL")):
        value = os.getenv(env, "").strip()
        if value:
            override[key] = value
    return override


def _resolved_judge() -> Tuple[str, str]:
    """The provider/model the judge call will actually use (mirrors `call_llm`'s override rules)."""
    cfg_provider, cfg_model = get_llm_config()
    override = _judge_override()
    if cfg_provider == "mock" or not override:
        return cfg_provider, cfg_model
    provider = override.get("provider", cfg_provider).lower()
    return provider, override.get("model", cfg_model)


def _is_factual_claim(sentence: Dict[str, Any]) -> bool:
    """Number-free sentence with at least 4 words outside citation tags."""
    return not sentence["numbers"] and len(BRACKET_RE.sub(" ", sentence["text"]).split()) >= 4


def _semantic_targets(sentences: List[Dict[str, Any]]) -> List[int]:
    """Number-free factual sentences, cited or not (including "not disclosed" statements)."""
    return [i for i, s in enumerate(sentences) if _is_factual_claim(s)]


def _parse_semantic_response(raw: str) -> Dict[int, Dict[str, str]]:
    text = raw.strip()
    fence = re.search(r"```(?:json)?\s*(.*?)```", text, re.DOTALL)
    if fence:
        text = fence.group(1).strip()
    try:
        data = json.loads(text)
    except (json.JSONDecodeError, TypeError):
        return {}
    items = data.get("results", []) if isinstance(data, dict) else data
    parsed: Dict[int, Dict[str, str]] = {}
    if not isinstance(items, list):
        return parsed
    for item in items:
        if not isinstance(item, dict):
            continue
        verdict = str(item.get("verdict", "")).strip().lower()
        try:
            idx = int(item.get("id"))
        except (TypeError, ValueError):
            continue
        if verdict in SEMANTIC_VERDICTS:
            parsed[idx] = {"verdict": verdict, "reason": str(item.get("reason", "")).strip()}
    return parsed


def _semantic_check(
    state: Dict[str, Any],
    sentences: List[Dict[str, Any]],
    evidence: List[Dict[str, Any]],
) -> Dict[str, Any]:
    """
    ONE batched `call_llm(state, "guardrail_semantic", ...)` for all target sentences.
    Unparseable output: "supported" in mock mode (offline tests), "unchecked" in live mode.
    Returns the updated telemetry.
    """
    telemetry = state.get("telemetry", {})
    targets = _semantic_targets(sentences)
    if not targets:
        return telemetry

    chunk_by_id = {str(c["chunk_id"]): c for c in evidence}
    blocks = []
    needs_all_evidence = False
    for n, i in enumerate(targets, start=1):
        s = sentences[i]
        if s["chunk_ids"]:
            cited = "\n".join(
                f"  [{cid}]: {chunk_by_id[cid].get('content', '')[:SEMANTIC_CHUNK_CHARS]}" for cid in s["chunk_ids"]
            )
            blocks.append(f"Sentence {n}: {s['text']}\nCited evidence:\n{cited}")
        else:
            needs_all_evidence = True
            blocks.append(f"Sentence {n} (uncited): {s['text']}\nCited evidence: none; judge against ALL RETRIEVED EVIDENCE below.")
    user_prompt = "\n\n---\n\n".join(blocks)
    if needs_all_evidence:
        all_evidence = "\n".join(
            f"  [{c['chunk_id']}]: {c.get('content', '')[:SEMANTIC_CHUNK_CHARS]}" for c in evidence
        ) or "  (no evidence retrieved)"
        user_prompt += f"\n\n===\n\nALL RETRIEVED EVIDENCE:\n{all_evidence}"

    raw, telemetry = call_llm(
        state=state,
        node_name="guardrail_semantic",
        messages=[
            {"role": "system", "content": SEMANTIC_SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.0,
        json_mode=True,
        **_judge_override(),
    )

    parsed = _parse_semantic_response(raw)
    provider, _ = get_llm_config()
    for n, i in enumerate(targets, start=1):
        result = parsed.get(n)
        if result:
            sentences[i]["semantic_verdict"] = result["verdict"]
            sentences[i]["reason"] = result["reason"]
        elif provider == "mock":
            sentences[i]["semantic_verdict"] = "supported"
            sentences[i]["reason"] = "mock mode: judge output not parsed"
        else:
            sentences[i]["semantic_verdict"] = "unchecked"
            sentences[i]["reason"] = "judge output could not be parsed"
    return telemetry


# ---------------------------------------------------------------------------
# Step D: pass/fail
# ---------------------------------------------------------------------------


def _finalize_report(report: Dict[str, Any]) -> bool:
    """Recompute `unverified_sentences` / `unchecked_sentences` in place and return whether the guardrail passes."""
    unverified, unchecked = [], []
    for s in report["sentences"]:
        bad_number = any(n["status"] in ("ungrounded", "uncited") for n in s["numbers"])
        bad_citation = any(tag in report["invalid_citations"] for tag in s["citations"])
        if bad_number or bad_citation or s["semantic_verdict"] in ("partial", "unsupported"):
            unverified.append(s["text"])
        elif s["semantic_verdict"] == "unchecked":
            unchecked.append(s["text"])
    report["unverified_sentences"] = unverified
    report["unchecked_sentences"] = unchecked
    verdicts = [s["semantic_verdict"] for s in report["sentences"]]
    report["semantic_verdict_counts"] = {v: verdicts.count(v) for v in (*SEMANTIC_VERDICTS, "unchecked")}
    return not (report["ungrounded_numbers"] or report["invalid_citations"] or unverified)


def guardrail_node(state: AdaptiveRAGState) -> Dict[str, Any]:
    """
    LangGraph Node (Aryan's Module):
    Audits `draft_answer` (numbers, citations, and optionally sentence faithfulness) and produces
    `final_answer` + `guardrail_report`.
    """
    telemetry = dict(state.get("telemetry", {}))
    draft = state.get("draft_answer") or state.get("final_answer") or ""
    evidence = state.get("accumulated_evidence", [])

    with track_node_latency(telemetry, "guardrail"):
        report = verify_numerical_grounding(draft, evidence)

    if semantic_check_enabled():
        report["semantic_check_enabled"] = True
        report["semantic_judge_provider"], report["semantic_judge_model"] = _resolved_judge()
        telemetry = _semantic_check({**state, "telemetry": telemetry}, report["sentences"], evidence)

    passed = _finalize_report(report)
    final_ans = draft
    if not passed:
        problems = []
        if report["ungrounded_numbers"]:
            problems.append(
                "these numerical figures could not be matched in their cited chunks: "
                + ", ".join(report["ungrounded_numbers"])
            )
        if report["invalid_citations"]:
            problems.append("these citation tags do not map to any retrieved chunk: " + ", ".join(report["invalid_citations"]))
        if report["unverified_sentences"]:
            problems.append(f"{len(report['unverified_sentences'])} sentence(s) are not supported by their cited chunks")
        final_ans = (
            f"{draft}\n\n> [Guardrail Audit Warning]: Manual verification required; " + "; ".join(problems) + "."
        )

    return {
        "final_answer": final_ans,
        "guardrail_passed": passed,
        "guardrail_report": report,
        "telemetry": telemetry,
    }
