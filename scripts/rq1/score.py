"""
RQ1 Stage 1: retrieval scores from existing records (free, deterministic, no LLM). Never re-runs systems.

Relevance labels come from lexical matching of gold evidence quotes (`matching.py`). Ranks follow the order
in which each system produced its `retrieved_contexts` (System C: retrieval order across hops, with v2's
XBRL blocks first), the same order RQ2's RAGAS Context Precision sees.

Per (system, question), written to `question_scores.csv`:
- recall@k            share of gold evidence items found in the first k chunks
- context_recall      share of gold evidence items found anywhere in the retrieved context (recall@all)
- complete@k / complete@all   1 if every gold evidence item was found
- zero_recall         1 if no gold evidence item was found
- context_precision   RAGAS-style average precision over the ranked chunks:
                      sum_k(precision@k * rel_k) / (relevant chunks); 0 if none is relevant

Per (system, question, gold evidence item), written to `evidence_scores.csv`: found, first rank, found@k,
and the item's kind (table / text), for modality-level recall.

Usage:
    python scripts/rq1/score.py [--records reports/rq3/records.jsonl] [--out reports/rq1]
"""

import argparse
import csv
import sys
from pathlib import Path
from typing import Any, Dict, List, Sequence, Tuple

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from scripts.rq1.common import (  # noqa: E402
    BENCHMARK_PATH, EVIDENCE_SCORES_FILE, FACETS, K_VALUES, OUT_DIR, QUESTION_SCORES_FILE, RECORDS_PATH,
    gold_item, load_benchmark, load_records, question_facets,
)
from scripts.rq1.matching import first_rank, relevance_matrix  # noqa: E402


def question_metrics(rel: List[List[bool]], k_values: Sequence[int] = K_VALUES) -> Dict[str, float]:
    """Retrieval metrics for one record from its relevance matrix (gold evidence x ranked chunks)."""
    ranks = [first_rank(row) for row in rel]
    n_ev = len(ranks)
    out: Dict[str, float] = {}
    for k in k_values:
        hits = sum(r is not None and r <= k for r in ranks)
        out[f"recall@{k}"] = hits / n_ev
        out[f"complete@{k}"] = float(hits == n_ev)
    found = sum(r is not None for r in ranks)
    out["context_recall"] = found / n_ev
    out["complete@all"] = float(found == n_ev)
    out["zero_recall"] = float(found == 0)

    relevant = [any(col) for col in zip(*rel)]
    hits_so_far, ap = 0, 0.0
    for k, is_rel in enumerate(relevant, 1):
        if is_rel:
            hits_so_far += 1
            ap += hits_so_far / k
    out["context_precision"] = ap / hits_so_far if hits_so_far else 0.0
    return out


def question_metric_names(k_values: Sequence[int] = K_VALUES) -> List[str]:
    return ([f"recall@{k}" for k in k_values] + ["context_recall"] + [f"complete@{k}" for k in k_values]
            + ["complete@all", "zero_recall", "context_precision"])


def evaluate_records(
    benchmark_path: Path = BENCHMARK_PATH,
    records_path: Path = RECORDS_PATH,
    k_values: Sequence[int] = K_VALUES,
) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    """(question rows, evidence rows) for every record. Raises on records that cannot be scored."""
    records = load_records(records_path)
    bench = load_benchmark(benchmark_path)
    question_rows, evidence_rows = [], []
    for r in records:
        qid = r.get("question_id") or r.get("query_id")
        q = bench.get(qid)
        if q is None:
            raise ValueError(f"Record question_id '{qid}' ({r.get('system')}) is not in {benchmark_path}")
        gold = q["gold_evidence"]
        contexts = r["retrieved_contexts"]
        rel = relevance_matrix(gold, contexts)
        question_rows.append({
            "system": r["system"], "question_id": qid, **question_facets(q),
            "n_gold_evidence": len(gold), "n_contexts": len(contexts),
            **question_metrics(rel, k_values),
        })
        for i, (ev, row) in enumerate(zip(gold, rel)):
            rank = first_rank(row)
            evidence_rows.append({
                "system": r["system"], "question_id": qid, "evidence_index": i, "kind": ev["kind"],
                "ticker": ev.get("ticker"), "year": ev.get("year"), "item": gold_item(ev),
                "found": int(rank is not None), "first_rank": rank,
                **{f"found@{k}": int(rank is not None and rank <= k) for k in k_values},
            })
    return question_rows, evidence_rows


def write_csv(path: Path, rows: List[Dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"Nothing to write to {path}")
    with path.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)


def score(benchmark: Path = BENCHMARK_PATH, records: Path = RECORDS_PATH, out_dir: Path = OUT_DIR,
          k_values: Sequence[int] = K_VALUES) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    question_rows, evidence_rows = evaluate_records(benchmark, records, k_values)
    out_dir.mkdir(parents=True, exist_ok=True)
    write_csv(out_dir / QUESTION_SCORES_FILE, question_rows)
    write_csv(out_dir / EVIDENCE_SCORES_FILE, evidence_rows)
    return question_rows, evidence_rows


def main() -> None:
    p = argparse.ArgumentParser(description="RQ1 Stage 1: deterministic retrieval scores.")
    p.add_argument("--benchmark", type=Path, default=BENCHMARK_PATH)
    p.add_argument("--records", type=Path, default=RECORDS_PATH)
    p.add_argument("--out", type=Path, default=OUT_DIR)
    args = p.parse_args()
    q_rows, e_rows = score(args.benchmark, args.records, args.out)
    print(f"Scored {len(q_rows)} records ({len(e_rows)} gold evidence items) -> {args.out}")
    print(f"Facets: {', '.join(FACETS)}")


if __name__ == "__main__":
    main()
