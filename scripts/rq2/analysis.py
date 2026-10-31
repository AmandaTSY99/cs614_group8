"""
RQ2 analysis on top of the scores (`cs614-eval` env, no API calls): primary accuracy, paired system comparisons
with Holm correction, rule-based error types and the citation sensitivity rows.

Rows here have the same shape as the rows in `scores.jsonl`, so `report.aggregate` groups them by system,
category and question attribute like any other metric.
"""

import itertools
import re
from collections import defaultdict
from typing import Any, Dict, Iterable, List, Optional, Tuple

import numpy as np
from scipy import stats

SYSTEM_ORDER = ["system_a", "system_b", "system_c_v1", "system_c_v3"]
DIMENSIONS = ["answer_type", "evidence_format", "hop", "task", "evidence_scope"]
N_BOOT_PAIRED = 2000
SEED = 0
ALPHA = 0.05
MIN_PAIRED_N = 3

# A numeric question is correct when its gold number is in the answer; any other question when at least half of
# its key points are covered. Anything else, or a refusal, is a wrong answer.
NUMERIC_CORRECT_MIN = 1.0
KEYPOINT_CORRECT_MIN = 0.5
CONTEXT_RECALL_MIN = 0.5
FAITHFULNESS_MIN = 0.5
ERROR_TYPES = ["refusal", "retrieval_miss", "wrong_number", "unsupported_claim", "incomplete"]
ERROR_TYPE_RULE = (
    "A wrong answer is a numeric question whose number is not in the answer (numeric_accuracy < 1), or any other "
    "question with keypoint_recall < 0.5, or a refusal. Each gets ONE primary type, first match wins: "
    "1 `refusal` = abstained; 2 `retrieval_miss` = RAGAS context recall < 0.5 (the gold evidence was not "
    "retrieved); 3 `wrong_number` = the question has a gold number and numeric_accuracy < 1 although evidence was "
    "retrieved; 4 `unsupported_claim` = faithfulness < 0.5; 5 `incomplete` = everything else, e.g. key points missed."
)

CITATION_SENSITIVITY = {
    "citation_precision": "citation_precision_incl_uncited",
    "citation_recall": "citation_recall_incl_uncited",
    "citation_f1": "citation_f1_incl_uncited",
}


def order_systems(systems: Iterable[str]) -> List[str]:
    known = [s for s in SYSTEM_ORDER if s in set(systems)]
    return known + sorted(set(systems) - set(known))


def dim_groups(dims: Optional[Dict[str, Any]]) -> List[str]:
    dims = dims or {}
    return [f"{d}={dims[d]}" for d in DIMENSIONS if dims.get(d)]


def _index(scores: List[Dict[str, Any]]) -> Dict[Tuple[str, str, str], Dict[str, Any]]:
    return {(r["system"], r["question_id"], r["metric"]): r for r in scores}


def _value(index: Dict[Tuple[str, str, str], Dict[str, Any]], system: str, qid: str, metric: str) -> Optional[float]:
    row = index.get((system, qid, metric))
    if row and row.get("status") == "ok" and row.get("value") is not None:
        return float(row["value"])
    return None


def _meta(scores: List[Dict[str, Any]]) -> Dict[Tuple[str, str], Dict[str, Any]]:
    meta: Dict[Tuple[str, str], Dict[str, Any]] = {}
    for r in scores:
        meta.setdefault((r["system"], r["question_id"]), {"category": r.get("category"), "dims": r.get("dims") or {}})
    return meta


def _row(system: str, qid: str, meta: Dict[str, Any], metric: str, value: Optional[float], detail: str) -> Dict[str, Any]:
    return {"system": system, "question_id": qid, "category": meta.get("category"), "dims": meta.get("dims") or {},
            "metric": metric, "value": value, "status": "ok" if value is not None else "na", "judge": "none",
            "detail": detail}


def primary_accuracy_rows(records: List[Dict[str, Any]], scores: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Numeric questions: `numeric_accuracy`. Qualitative and mixed questions: the record's saved `keypoint_recall`
    (rule-based). N/A when the question has no gold number / no key points.
    """
    index, meta = _index(scores), _meta(scores)
    rows = []
    for rec in records:
        key = (rec["system"], rec["question_id"])
        if key not in meta:
            continue
        if rec.get("type") == "numeric":
            value, detail = _value(index, *key, "numeric_accuracy"), "numeric_accuracy"
        else:
            value = float(rec["keypoint_recall"]) if rec.get("keypoint_recall") is not None else None
            detail = "keypoint_recall"
        rows.append(_row(*key[:1], key[1], meta[key], "primary_accuracy", value, detail))
    return rows


def classify_error(abstained: bool, numeric_accuracy: Optional[float], primary: Optional[float], is_numeric_type: bool,
                   context_recall: Optional[float], faithfulness: Optional[float]) -> Optional[str]:
    """The ONE primary error type of a wrong answer, or None for a correct answer. See ERROR_TYPE_RULE."""
    if is_numeric_type:
        wrong = primary is not None and primary < NUMERIC_CORRECT_MIN
    else:
        wrong = primary is not None and primary < KEYPOINT_CORRECT_MIN
    if not (abstained or wrong):
        return None
    if abstained:
        return "refusal"
    if context_recall is not None and context_recall < CONTEXT_RECALL_MIN:
        return "retrieval_miss"
    if numeric_accuracy is not None and numeric_accuracy < NUMERIC_CORRECT_MIN:
        return "wrong_number"
    if faithfulness is not None and faithfulness < FAITHFULNESS_MIN:
        return "unsupported_claim"
    return "incomplete"


def error_type_rows(records: List[Dict[str, Any]], scores: List[Dict[str, Any]],
                    primary: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """One row per answer: `error_type` (None when correct), `wrong`, plus category and dims."""
    index, meta = _index(scores), _meta(scores)
    prim = {(r["system"], r["question_id"]): r["value"] for r in primary}
    out = []
    for rec in records:
        key = (rec["system"], rec["question_id"])
        if key not in meta:
            continue
        abstained = (_value(index, *key, "abstained") or 0.0) >= 1.0
        etype = classify_error(
            abstained, _value(index, *key, "numeric_accuracy"), prim.get(key), rec.get("type") == "numeric",
            _value(index, *key, "context_recall"), _value(index, *key, "faithfulness"),
        )
        out.append({"system": key[0], "question_id": key[1], "category": meta[key]["category"],
                    "dims": meta[key]["dims"], "error_type": etype, "wrong": etype is not None})
    return out


def error_type_counts(rows: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Per system x group: answers, wrong answers and a count and share (of wrong answers) per error type."""
    groups: Dict[Tuple[str, str], List[Dict[str, Any]]] = defaultdict(list)
    for r in rows:
        for g in ("overall", *dim_groups(r["dims"])):
            groups[(r["system"], g)].append(r)
    out = []
    for (system, group), rs in sorted(groups.items()):
        wrong = [r for r in rs if r["wrong"]]
        row = {"system": system, "group": group, "answers": len(rs), "wrong": len(wrong)}
        for t in ERROR_TYPES:
            n = sum(r["error_type"] == t for r in wrong)
            row[t] = n
            row[f"{t}_share"] = n / len(wrong) if wrong else None
        out.append(row)
    return out


def citation_sensitivity_rows(scores: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Citation precision / recall / F1 are N/A for an answer with no citations. These rows repeat them with such
    an answer counting as 0 (N/A stays N/A when the question has no gold section).
    """
    rows = []
    for r in scores:
        new = CITATION_SENSITIVITY.get(r["metric"])
        if not new:
            continue
        copy = dict(r, metric=new)
        if r.get("status") == "na" and "no citations" in str(r.get("detail") or ""):
            copy.update(value=0.0, status="ok", detail="no citations counted as 0")
        rows.append(copy)
    return rows


# --- Paired comparisons ------------------------------------------------------------------------

def holm(p_values: List[float]) -> List[float]:
    """Holm-adjusted p-values, in the input order."""
    m = len(p_values)
    order = sorted(range(m), key=lambda i: p_values[i])
    adjusted = [0.0] * m
    running = 0.0
    for rank, i in enumerate(order):
        running = max(running, min(1.0, (m - rank) * p_values[i]))
        adjusted[i] = running
    return adjusted


def paired_bootstrap(diffs: np.ndarray, n_boot: int = N_BOOT_PAIRED, seed: int = SEED) -> Tuple[float, float]:
    """95% CI of the mean paired difference (percentile bootstrap over questions, fixed seed)."""
    rng = np.random.default_rng(seed)
    idx = rng.integers(0, len(diffs), size=(n_boot, len(diffs)))
    means = diffs[idx].mean(axis=1)
    return float(np.percentile(means, 2.5)), float(np.percentile(means, 97.5))


def wilcoxon_p(diffs: np.ndarray) -> float:
    if not np.any(diffs != 0):
        return 1.0
    try:
        return float(stats.wilcoxon(diffs, zero_method="wilcox").pvalue)
    except ValueError:
        return 1.0


def paired_comparisons(scores: List[Dict[str, Any]], systems: Optional[List[str]] = None,
                       n_boot: int = N_BOOT_PAIRED, seed: int = SEED) -> List[Dict[str, Any]]:
    """
    For every metric and group (overall, category, each question attribute value): all system pairs on the same
    questions. `mean_diff` = second system minus first. Bootstrap CI over questions, Wilcoxon signed-rank
    p-value, Holm-corrected across the pairs of that metric and group.
    """
    values: Dict[Tuple[str, str], Dict[str, Dict[str, float]]] = defaultdict(lambda: defaultdict(dict))
    for r in scores:
        if r.get("status") != "ok" or r.get("value") is None:
            continue
        groups = ["overall", f"category={r.get('category')}", *dim_groups(r.get("dims"))]
        for g in groups:
            values[(r["metric"], g)][r["system"]][r["question_id"]] = float(r["value"])
    out = []
    for (metric, group), per_system in sorted(values.items()):
        ordered = order_systems(systems or per_system)
        rows = []
        for a, b in itertools.combinations(ordered, 2):
            common = sorted(set(per_system.get(a, {})) & set(per_system.get(b, {})))
            if len(common) < MIN_PAIRED_N:
                continue
            diffs = np.array([per_system[b][q] - per_system[a][q] for q in common])
            low, high = paired_bootstrap(diffs, n_boot, seed)
            rows.append({"metric": metric, "group": group, "system_a": a, "system_b": b, "n": len(common),
                         "mean_a": float(np.mean([per_system[a][q] for q in common])),
                         "mean_b": float(np.mean([per_system[b][q] for q in common])),
                         "mean_diff": float(diffs.mean()), "ci_low": low, "ci_high": high,
                         "p_wilcoxon": wilcoxon_p(diffs)})
        for row, p_adj in zip(rows, holm([r["p_wilcoxon"] for r in rows])):
            row["p_holm"] = p_adj
            row["significant"] = p_adj < ALPHA
        out.extend(rows)
    return out


def ordering_test(comparisons: List[Dict[str, Any]], metric: str = "primary_accuracy") -> Dict[str, Any]:
    """Overall pairs of `metric` against the expected ordering of SYSTEM_ORDER (later system higher)."""
    rows = []
    for c in comparisons:
        if c["metric"] != metric or c["group"] != "overall":
            continue
        if c["significant"]:
            verdict = "as expected (significant)" if c["mean_diff"] > 0 else "OPPOSITE (significant)"
        else:
            verdict = "not significant"
        rows.append(dict(c, verdict=verdict))
    ordered = order_systems({s for r in rows for s in (r["system_a"], r["system_b"])})
    adjacent = [(a, b) for a, b in zip(ordered, ordered[1:])]
    holds = bool(adjacent) and all(
        any(r["system_a"] == a and r["system_b"] == b and r["verdict"].startswith("as expected") for r in rows)
        for a, b in adjacent
    )
    return {"rows": rows, "ordering_holds": holds, "order": ordered}
