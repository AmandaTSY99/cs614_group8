"""
Domain-Specific Financial Scale & Unit Normalization Engine for System C Guardrails.

Owned by: Anish (System Architect) - Provided as a modular utility for Aryan's Verifier.

Solves the classic SEC 10-K RAG false-positive issue:
- Filings report tables in millions (e.g. "$115,185" with header "(in millions)").
- LLMs synthesize this as "$115.18 billion" or "$115.2B".
- Standard string equality regex fails, falsely flagging valid scale conversions as hallucinations.

Features:
1. Multiplier parsing: thousand/K, million/M/mn, billion/B/bn, trillion/T/tn, basis points (bps).
2. Canonical float representation and relative tolerance comparison (default: 0.5% tolerance).
3. Contextual scale detection: scans table headers or surrounding context for "(in millions)" or "in thousands".
"""

import re
from typing import List, Optional, Tuple

SCALE_MULTIPLIERS = {
    "thousand": 1e3,
    "k": 1e3,
    "million": 1e6,
    "m": 1e6,
    "mn": 1e6,
    "billion": 1e9,
    "b": 1e9,
    "bn": 1e9,
    "trillion": 1e12,
    "t": 1e12,
    "tn": 1e12,
}

# Regex to capture numbers with optional currency prefix and optional magnitude suffix
# e.g., "$115.18 billion", "115.2B", "$115,185 million", "75.0%", "142%"
NUM_WITH_SCALE_RE = re.compile(
    r"\$?\s*(\d{1,3}(?:,\d{3})+(?:\.\d+)?|\d+(?:\.\d+)?)\s*(trillion|billion|million|thousand|bps|%|[ktmb])\b",
    re.IGNORECASE,
)

RAW_NUMBER_RE = re.compile(
    r"\$?\s*(\d{1,3}(?:,\d{3})+(?:\.\d+)?|\d+\.\d+|\b\d{2,}\b)",
    re.IGNORECASE,
)


def parse_financial_value(text: str) -> Optional[float]:
    """
    Parse a string financial figure into its canonical absolute float value.
    Examples:
        "$115.18 billion" -> 115180000000.0
        "115.2B"          -> 115200000000.0
        "$115,185"        -> 115185.0
        "75.0%"           -> 75.0
    """
    clean = text.strip().replace("$", "").replace(",", "")
    match = re.match(
        r"^(\d+(?:\.\d+)?)\s*(trillion|billion|million|thousand|bps|%|[ktmb])?$",
        clean,
        re.IGNORECASE,
    )
    if not match:
        try:
            return float(clean)
        except ValueError:
            return None

    num_str, unit = match.groups()
    try:
        val = float(num_str)
    except ValueError:
        return None

    if not unit:
        return val

    unit_lower = unit.lower()
    if unit_lower in SCALE_MULTIPLIERS:
        return val * SCALE_MULTIPLIERS[unit_lower]
    elif unit_lower == "%":
        return val
    elif unit_lower == "bps":
        return val * 0.0001
    return val


def detect_context_scale_multiplier(text: str) -> float:
    """
    Detect whether a table or document chunk specifies an overall scale in its headers.
    e.g. "(in millions, except per share data)" -> 1e6
         "(in thousands)"                      -> 1e3
    """
    text_lower = text[:500].lower()
    if "in millions" in text_lower or "(millions)" in text_lower:
        return 1e6
    if "in billions" in text_lower or "(billions)" in text_lower:
        return 1e9
    if "in thousands" in text_lower or "(thousands)" in text_lower:
        return 1e3
    return 1.0


def extract_all_financial_values(text: str) -> List[Tuple[float, str]]:
    """
    Extract all candidate float values and their raw representations from a text block,
    taking into account both inline multipliers and document-level scale headers.
    """
    values: List[Tuple[float, str]] = []
    doc_scale = detect_context_scale_multiplier(text)

    # 1. Matches with explicit inline scale (e.g. "$115.18 billion" or "75.0%")
    for match in NUM_WITH_SCALE_RE.finditer(text):
        raw = match.group(0)
        parsed = parse_financial_value(raw)
        if parsed is not None:
            values.append((parsed, raw))

    # 2. Raw numbers (with doc_scale applied, and 1.0 scale as fallback)
    for match in RAW_NUMBER_RE.finditer(text):
        raw = match.group(0).replace("$", "").replace(",", "")
        # Skip likely fiscal years
        if re.fullmatch(r"199\d|20[0-2]\d", raw):
            continue
        try:
            val = float(raw)
            values.append((val, match.group(0)))
            if doc_scale != 1.0:
                values.append((val * doc_scale, f"{match.group(0)} (scaled x{int(doc_scale)})"))
        except ValueError:
            pass

    return values


def fuzzy_financial_match(
    claim_token: str,
    evidence_text: str,
    tolerance: float = 0.005,
) -> bool:
    """
    Verify whether `claim_token` (e.g. "$115.2B" or "115.18 billion" or "75.0%")
    is numerically grounded in `evidence_text` within relative `tolerance` (default 0.5%).

    Returns True if an exact string match OR a scaled float match is found.
    """
    clean_claim = claim_token.strip().replace(",", "")

    # Direct substring / un-punctuated match
    if claim_token in evidence_text or clean_claim in evidence_text.replace(",", ""):
        return True

    claim_val = parse_financial_value(claim_token)
    if claim_val is None or claim_val == 0.0:
        return False

    candidate_values = extract_all_financial_values(evidence_text)
    for cand_val, _ in candidate_values:
        if cand_val == 0.0:
            continue
        # Relative error comparison: |claim - candidate| / |candidate|
        rel_err = abs(claim_val - cand_val) / abs(cand_val)
        if rel_err <= tolerance:
            return True

    return False
