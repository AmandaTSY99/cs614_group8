"""
RQ2 retrieval context checks from the saved records and the benchmark's gold evidence (no judge, no API):
whether each gold evidence quote is in the retrieved text, how that relates to refusals, and the retrieval context
each system passes to the answer model (chunks, characters, hops).
"""

import re
from collections import Counter, defaultdict
from typing import Any, Dict, List, Optional

from scripts.rq2.analysis import order_systems
from scripts.rq2.metrics_custom import is_abstention

MIN_WORDS_FOR_OVERLAP = 15
MIN_WORD_OVERLAP = 0.8


def _normalize(text: str) -> str:
    return " ".join(re.sub(r"[*_`]", "", text or "").lower().split())


def _words(text: str) -> set:
    return set(re.findall(r"\w+", (text or "").lower()))


LENIENT_WORD_OVERLAP = 0.6


def quote_in_contexts(evidence: Dict[str, Any], record: Dict[str, Any], lenient: bool = False) -> bool:
    """
    The gold quote is in a retrieved chunk of the gold filing: the normalised quote is a substring of the chunk,
    or (long quotes split over two chunks) at least 80% of its words are in it (the rule of `src/system_a/evaluate.py`).
    `lenient`: also accept any quote, however short, when at least 60% of its words are in a chunk of that filing.
    """
    quote = _normalize(evidence.get("quote", ""))
    quote_words = _words(quote)
    min_words, threshold = (1, LENIENT_WORD_OVERLAP) if lenient else (MIN_WORDS_FOR_OVERLAP, MIN_WORD_OVERLAP)
    for meta, text in zip(record.get("contexts_meta") or [], record.get("retrieved_contexts") or []):
        doc_id = str(meta.get("chunk_id", "")).split(":")[0]
        if doc_id != evidence.get("doc_id"):
            continue
        chunk = _normalize(text)
        if quote and quote in chunk:
            return True
        if len(quote_words) >= min_words and len(quote_words & _words(chunk)) >= threshold * len(quote_words):
            return True
    return False


def evidence_coverage(record: Dict[str, Any], question: Optional[Dict[str, Any]], lenient: bool = False) -> Optional[float]:
    """Share of the question's gold evidence quotes found in the retrieved contexts (None without gold evidence)."""
    evidence = (question or {}).get("gold_evidence") or []
    if not evidence:
        return None
    return sum(quote_in_contexts(e, record, lenient) for e in evidence) / len(evidence)


def refusal_retrieval(records: List[Dict[str, Any]], benchmark: Dict[str, Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Per system: refusals and answers, and how much of the gold evidence was retrieved for each group
    (`full` = every gold quote found, `partial` = some, `none` = none; plus the lenient count of `full`).
    """
    stats: Dict[str, Dict[str, Counter]] = defaultdict(lambda: {"refusal": Counter(), "answered": Counter()})
    for rec in records:
        question = benchmark.get(str(rec["question_id"]))
        cov = evidence_coverage(rec, question)
        if cov is None:
            continue
        bucket = stats[rec["system"]]["refusal" if is_abstention(rec.get("answer", "")) else "answered"]
        bucket["n"] += 1
        bucket["full" if cov == 1.0 else "none" if cov == 0.0 else "partial"] += 1
        bucket["full_lenient"] += evidence_coverage(rec, question, lenient=True) == 1.0
    out = []
    for system in order_systems(stats):
        r, a = stats[system]["refusal"], stats[system]["answered"]
        out.append({"system": system, "answers": r["n"] + a["n"], "refusals": r["n"],
                    "refusals_full_evidence": r["full"], "refusals_partial_evidence": r["partial"],
                    "refusals_no_evidence": r["none"], "refusals_full_evidence_lenient": r["full_lenient"],
                    "answered": a["n"], "answered_full_evidence": a["full"],
                    "answered_partial_evidence": a["partial"], "answered_no_evidence": a["none"],
                    "answered_full_evidence_lenient": a["full_lenient"]})
    return out


def retrieval_context_stats(records: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Per system: average chunks and characters passed to the answer model, hop distribution, mean hops."""
    groups: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
    for rec in records:
        groups[rec["system"]].append(rec)
    out = []
    for system in order_systems(groups):
        recs = groups[system]
        hops = Counter(int(r.get("hops") or 1) for r in recs)
        row = {"system": system, "answers": len(recs),
               "mean_chunks": sum(len(r.get("retrieved_contexts") or []) for r in recs) / len(recs),
               "mean_context_chars": sum(sum(len(c) for c in r.get("retrieved_contexts") or []) for r in recs) / len(recs),
               "mean_hops": sum(int(r.get("hops") or 1) for r in recs) / len(recs)}
        for h in (1, 2, 3):
            row[f"hops_{h}"] = hops.get(h, 0)
        row["hops_other"] = sum(v for k, v in hops.items() if k not in (1, 2, 3))
        out.append(row)
    return out
