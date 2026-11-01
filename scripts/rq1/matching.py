"""
Lexical matching of one gold evidence quote against retrieved chunks (no LLM).

A quote counts as retrieved in a chunk if one of three 6-word sub-phrases (start, middle, end) appears in
the normalised chunk, or >= 65% of the quote's words do. This is a lower bound: a figure the gold quotes
from one table can also be stated elsewhere in the filing, and a quote split across two chunks may match
neither.
"""

import re
from typing import Any, Dict, List, Optional

MIN_PHRASE_CHARS = 10
WORD_OVERLAP = 0.65


def normalize_text(text: str) -> str:
    """Lowercase, collapse whitespace, drop punctuation."""
    text = re.sub(r"\s+", " ", text.lower().strip())
    return re.sub(r"[^\w\s]", "", text)


def _sub_phrases(words: List[str]) -> List[str]:
    if len(words) <= 5:
        return [" ".join(words)]
    mid = len(words) // 2
    return [" ".join(words[:6]), " ".join(words[-6:]), " ".join(words[mid - 3: mid + 3])]


def evidence_in_contexts(gold_ev: Dict[str, Any], contexts: List[str]) -> bool:
    """True if the gold evidence quote is found in any of `contexts`."""
    words = normalize_text(gold_ev.get("quote", "")).split()
    if not words:
        raise ValueError(f"Gold evidence has an empty quote: {gold_ev}")
    phrases = [p for p in _sub_phrases(words) if len(p) > MIN_PHRASE_CHARS]
    quote_words = set(words)
    for ctx in contexts:
        norm_ctx = normalize_text(ctx)
        if any(p in norm_ctx for p in phrases):
            return True
        if len(quote_words & set(norm_ctx.split())) / len(quote_words) >= WORD_OVERLAP:
            return True
    return False


def relevance_matrix(gold_evidence: List[Dict[str, Any]], contexts: List[str]) -> List[List[bool]]:
    """`m[i][j]`: gold evidence i is found in retrieved chunk j (chunks in the order the system produced them)."""
    return [[evidence_in_contexts(ev, [ctx]) for ctx in contexts] for ev in gold_evidence]


def first_rank(row: List[bool]) -> Optional[int]:
    """1-based rank of the first chunk containing the evidence, or None."""
    return next((j + 1 for j, hit in enumerate(row) if hit), None)
