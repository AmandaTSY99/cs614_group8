"""
Free, deterministic RQ2 metrics (no LLM): citation precision/recall/F1 at section level, numeric answer
accuracy, numerical grounding error rate and citation coverage. Pure Python; runs in both envs.
"""

import re
from typing import Any, Dict, List, Optional, Tuple

from src.system_c.guardrails.citations import find_citation_tags
from src.system_c.guardrails.scale_normalizer import fuzzy_financial_match

KNOWN_TICKERS = {"AAPL", "AMZN", "GOOGL", "JNJ", "JPM", "META", "MSFT", "NVDA", "TSLA", "WMT"}
ITEM_RE = re.compile(r"\bItem\s+(\d+[A-Z]?)\b", re.IGNORECASE)
XBRL_ID_RE = re.compile(r"^F-([A-Z]{1,6})")
XBRL_SECTION = "XBRL"
CURRENCY_RE = re.compile(r"US\$|[€£¥]")

# Section aliases (a limitation of section-level matching, documented in report.md):
# - Item 15 (Exhibits and Financial Statement Schedules) holds the financial statements and notes in many
#   filings, while the gold labels them Item 8: an Item 15 chunk that is financial statements / notes counts as Item 8.
# - Cover-page chunks have no "Item N" heading; the gold labels cover-page facts Item 1.
FIN_STATEMENT_MARKERS = (
    "financial statements", "notes to consolidated", "notes to the consolidated", "consolidated balance sheet",
    "consolidated statements of", "statements of operations", "statements of cash flows", "balance sheets",
)
COVER_PAGE_MARKERS = (
    "exact name of registrant", "commission file number", "securities registered pursuant to section 12",
    "address of principal executive offices", "i.r.s. employer identification", "indicate by check mark",
)
ALIAS_TEXT_CHARS = 400

Section = Tuple[Optional[str], str]


def normalise_section(text: Any, ticker: Optional[str] = None) -> Optional[Section]:
    """
    `(ticker | None, top-level item)`: "MSFT Item 8 Note 19" -> ("MSFT", "Item 8"),
    "Item 7. Management's Discussion" -> (None, "Item 7"), "financials.csv" -> (None, "XBRL").
    Returns None when no item can be identified.
    """
    s = str(text or "").strip()
    first = s.split(None, 1)[0].upper() if s else ""
    if first in KNOWN_TICKERS:
        ticker = ticker or first
    if "financials.csv" in s.lower():
        return (ticker, XBRL_SECTION)
    m = ITEM_RE.search(s)
    if not m:
        return None
    return (ticker, f"Item {m.group(1).upper()}")


def gold_sections(target_sections: List[Any]) -> List[Section]:
    out: List[Section] = []
    for s in target_sections:
        sec = normalise_section(s)
        if sec and sec not in out:
            out.append(sec)
    return out


def _aliased_section(section: Any, text: str, ticker: Optional[str]) -> Optional[Section]:
    """Apply the Item 15 -> Item 8 and cover page -> Item 1 aliases (see FIN_STATEMENT_MARKERS)."""
    sec = normalise_section(section, ticker)
    section_text = str(section or "").lower()
    head = text[:ALIAS_TEXT_CHARS].lower()
    if sec and sec[1] == "Item 15":
        # The Item 15 heading itself names "Financial Statement Schedules", so look past it.
        sub = section_text.split(">", 1)[1] if ">" in section_text else ""
        if any(m in sub or m in head for m in FIN_STATEMENT_MARKERS):
            return (sec[0], "Item 8")
    if sec is None and any(m in section_text or m in head for m in COVER_PAGE_MARKERS):
        return (ticker, "Item 1")
    return sec


def cited_sections(citations: List[Dict[str, Any]], chunk_text: Optional[Dict[str, str]] = None) -> List[Section]:
    """
    Unique (ticker, item) per answer from each citation's chunk metadata; any `F-…` chunk is XBRL.
    `chunk_text` (chunk_id -> context text) lets the section aliases look at the chunk itself.
    """
    chunk_text = chunk_text or {}
    out: List[Section] = []
    for c in citations:
        cid = str(c.get("chunk_id") or "")
        ticker = (str(c["ticker"]).upper() if c.get("ticker") else None)
        xbrl = XBRL_ID_RE.match(cid)
        if xbrl:
            sec: Optional[Section] = (ticker or xbrl.group(1), XBRL_SECTION)
        else:
            sec = _aliased_section(c.get("section"), chunk_text.get(cid, ""), ticker)
        if sec and sec not in out:
            out.append(sec)
    return out


def _matches(cited: Section, gold: Section) -> bool:
    return cited[1] == gold[1] and (gold[0] is None or gold[0] == cited[0])


def citation_prf(
    citations: List[Dict[str, Any]],
    target_sections: List[Any],
    chunk_text: Optional[Dict[str, str]] = None,
) -> Dict[str, Any]:
    """
    Section-level citation precision / recall / F1. An answer with no citations (or a question with no
    usable gold section) gets status "na" — never 0.
    """
    gold = gold_sections(target_sections)
    cited = cited_sections(citations, chunk_text)
    if not citations or not cited:
        return {"status": "na", "precision": None, "recall": None, "f1": None, "detail": "no citations"}
    if not gold:
        return {"status": "na", "precision": None, "recall": None, "f1": None, "detail": "no gold sections"}
    precision = sum(any(_matches(c, g) for g in gold) for c in cited) / len(cited)
    recall = sum(any(_matches(c, g) for c in cited) for g in gold) / len(gold)
    f1 = 0.0 if precision + recall == 0 else 2 * precision * recall / (precision + recall)
    return {
        "status": "ok", "precision": precision, "recall": recall, "f1": f1,
        "detail": f"cited={cited} gold={gold}",
    }


def strip_citation_tags(answer: str) -> str:
    text = answer or ""
    for tag in find_citation_tags(text):
        text = text.replace(tag, " ")
    return re.sub(r"[ \t]+", " ", text).strip()


RATIO_TOLERANCE = 0.005  # same relative tolerance as `fuzzy_financial_match`
MIN_SIGNIFICANT_DIGITS = 3
ACCOUNTING_NEGATIVE_RE = re.compile(r"\$?\(\s*\$?(\d[\d,]*(?:\.\d+)?)\s*\)")
GOLD_MAGNITUDE_RE = re.compile(r"^-?\$?\s*(\d[\d,]*(?:\.\d+)?)\s*(thousand|million|billion|trillion)\b", re.IGNORECASE)
GOLD_PERCENT_RE = re.compile(r"^-?\$?\s*(\d+(?:\.\d+)?)\s*(%|percent)$", re.IGNORECASE)
GOLD_DECIMAL_RE = re.compile(r"^-?(\d*\.\d+)$")
BARE_NUMBER_RE = re.compile(r"(?<![\d.,])(\d{1,3}(?:,\d{3})+(?:\.\d+)?|\d+(?:\.\d+)?)(?![\d])")
PERCENT_RE = re.compile(r"(?<![\d.,])(\d+(?:\.\d+)?)\s*(?:%|percent\b)", re.IGNORECASE)
MAGNITUDE_OR_PERCENT_AFTER_RE = re.compile(r"^\s*(?:(?:thousand|million|billion|trillion|percent)\b|%)", re.IGNORECASE)


def _significant_digits(number: str) -> int:
    digits = number.replace(",", "")
    if "." in digits:
        digits = digits.rstrip("0").rstrip(".")
    return len(digits.replace(".", "").lstrip("0"))


def _unit_bare_match(gold: str, text: str) -> bool:
    """
    A table in thousands / millions gives a bare figure: "$316" matches the gold "$316 million" when the number is
    exactly the gold's and has at least 3 significant digits. A figure that names another magnitude or a percent
    ("$316 billion", "316%") does not count.
    """
    m = GOLD_MAGNITUDE_RE.match(gold)
    if not m or _significant_digits(m.group(1)) < MIN_SIGNIFICANT_DIGITS:
        return False
    value = float(m.group(1).replace(",", ""))
    for hit in BARE_NUMBER_RE.finditer(text):
        if abs(float(hit.group(1).replace(",", "")) - value) < 1e-9 \
                and not MAGNITUDE_OR_PERCENT_AFTER_RE.match(text[hit.end():]):
            return True
    return False


def _within(value: float, target: float, tolerance: float = RATIO_TOLERANCE) -> bool:
    return target != 0 and abs(value - target) <= tolerance * abs(target)


def _ratio_percent_match(gold: str, text: str) -> bool:
    """A ratio and its percentage are equivalent: the gold "0.72" matches "72.08%", and "72%" matches "0.72"."""
    g = CURRENCY_RE.sub("", gold).strip()
    percent = GOLD_PERCENT_RE.match(g)
    decimal = GOLD_DECIMAL_RE.match(g)
    if decimal and 0 < float(decimal.group(1)) <= 1:
        ratio = float(decimal.group(1))
        return any(_within(float(p.group(1)) / 100.0, ratio) for p in PERCENT_RE.finditer(text))
    if percent:
        ratio = float(percent.group(1)) / 100.0
        return any("." in b.group(1) and _within(float(b.group(1).replace(",", "")), ratio)
                   and not MAGNITUDE_OR_PERCENT_AFTER_RE.match(text[b.end():])
                   for b in BARE_NUMBER_RE.finditer(text))
    return False


def _number_found(gold: str, text: str) -> bool:
    g = CURRENCY_RE.sub("", gold).strip()
    # Accounting negatives: "(6.0)" and "$(316)" are -6.0 and -316.
    text = ACCOUNTING_NEGATIVE_RE.sub(r"-\1", text)
    # The benchmark writes decreases as "-25.64%" while answers say "decreased by 25.6%", so the unsigned
    # value also counts (a sign error is then not caught; documented in report.md).
    candidates = [g] + ([g[1:].strip()] if g.startswith("-") else [])
    return (any(fuzzy_financial_match(c, text) for c in candidates)
            or _unit_bare_match(g, text) or _ratio_percent_match(g, text))


def numeric_accuracy(answer: str, ground_truth_numbers: List[Any]) -> Optional[float]:
    """Share of gold numbers found in the answer (scale-aware: $60.9 billion matches 60,922 million)."""
    gold = [str(n).strip() for n in ground_truth_numbers if str(n).strip()]
    if not gold:
        return None
    text = CURRENCY_RE.sub("", strip_citation_tags(answer))
    hits = sum(_number_found(g, text) for g in gold)
    return hits / len(gold)


ABSTENTION_RE = re.compile(
    r"\b(not found in the provided context|not (?:found|provided|disclosed|available|included) in the "
    r"(?:provided |given )?(?:context|evidence|excerpts|filings?)|cannot be (?:determined|calculated|answered)"
    r"|(?:do|does) not (?:disclose|provide|contain|include)|insufficient (?:information|evidence|context)"
    r"|unable to (?:determine|find|answer))",
    re.IGNORECASE,
)


FIRST_SENTENCE_RE = re.compile(r"^.*?(?:[.!?](?:\s|$)|\n|$)", re.DOTALL)
PARTIAL_ANSWER_RE = re.compile(r"\b(only part|answer only|only answer|partial answer)\b", re.IGNORECASE)


def is_abstention(answer: str) -> bool:
    """
    The system declined to answer: its first sentence says the evidence is missing. A partial answer that
    gives a result and only later notes a missing detail is not an abstention.
    """
    text = strip_citation_tags(answer or "").replace("**", "").strip()
    first = FIRST_SENTENCE_RE.match(text).group(0) if text else ""
    return bool(ABSTENTION_RE.search(first)) and not PARTIAL_ANSWER_RE.search(first)


def grounding_error(guardrail_report: Optional[Dict[str, Any]]) -> Optional[float]:
    if not guardrail_report or guardrail_report.get("numerical_grounding_error_rate") is None:
        return None
    return float(guardrail_report["numerical_grounding_error_rate"])


def has_citation(record: Dict[str, Any]) -> bool:
    return bool(record.get("citations"))


def custom_scores(record: Dict[str, Any]) -> Dict[str, Tuple[Optional[float], str, str]]:
    """metric -> (value, status, detail) for one record."""
    chunk_text = {
        str(meta.get("chunk_id")): text
        for meta, text in zip(record.get("contexts_meta") or [], record.get("retrieved_contexts") or [])
    }
    prf = citation_prf(record.get("citations") or [], record.get("target_sections") or [], chunk_text)
    num = numeric_accuracy(record.get("answer", ""), record.get("ground_truth_numbers") or [])
    ground = grounding_error(record.get("guardrail_report"))
    return {
        "citation_precision": (prf["precision"], prf["status"], prf["detail"]),
        "citation_recall": (prf["recall"], prf["status"], prf["detail"]),
        "citation_f1": (prf["f1"], prf["status"], prf["detail"]),
        "citation_coverage": (1.0 if has_citation(record) else 0.0, "ok", ""),
        "numeric_accuracy": (num, "ok" if num is not None else "na", "" if num is not None else "no gold numbers"),
        "grounding_error_rate": (ground, "ok" if ground is not None else "na",
                                 "" if ground is not None else "no guardrail report"),
        "abstained": (1.0 if is_abstention(record.get("answer", "")) else 0.0, "ok", ""),
    }
