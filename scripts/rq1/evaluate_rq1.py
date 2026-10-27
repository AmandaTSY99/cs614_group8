#!/usr/bin/env python3
"""
RQ1 Evaluation Script: Retrieval Completeness across Non-Adjacent Sections.

Leads: Amanda & Kevin
Course: CS614 Generative AI with LLMs

Evaluates all 4 RAG systems (system_a, system_b, system_c_v1, system_c_v2) on:
1. Evidence Recall@k: Proportion of gold evidence facts retrieved in the candidate context.
2. Multi-Hop Evidence Completeness: % of multi-hop queries where ALL gold evidence items were found.
3. Cross-Section Discovery Rate: % of questions with disparate 10-K sections (e.g. Item 7 + Item 8)
   where evidence was successfully retrieved from both non-adjacent sections.
4. Context Precision: Fraction of retrieved context chunks that contain ground-truth evidence.
5. Hop Saturation: Relationship between iterative hops and evidence discovery.

Can run:
- Offline (instantaneous): reads pre-generated records from `reports/rq3/records.jsonl`.
- Live: queries systems directly across `data/benchmark_qa_pool_2015.json`.
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Set, Tuple

import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

DEFAULT_BENCHMARK = REPO_ROOT / "data" / "benchmark_qa_pool_2015.json"
DEFAULT_RECORDS = REPO_ROOT / "reports" / "rq3" / "records.jsonl"
DEFAULT_OUT_CSV = REPO_ROOT / "reports" / "rq1" / "summary_metrics.csv"
DEFAULT_OUT_JSON = REPO_ROOT / "reports" / "rq1" / "summary_metrics.json"

SYSTEMS = ["system_a", "system_b", "system_c_v1", "system_c_v2"]


def normalize_text(text: str) -> str:
    """Normalize text for fuzzy substring matching."""
    text = re.sub(r"\s+", " ", text.lower().strip())
    # Remove punctuation for robust matching
    text = re.sub(r"[^\w\s]", "", text)
    return text


def evidence_in_contexts(gold_ev: Dict[str, Any], contexts: List[str]) -> bool:
    """Check if a gold evidence piece is covered by the retrieved contexts."""
    quote = gold_ev.get("quote", "").strip()
    if not quote:
        # Fallback to doc_id and section matching if quote is empty
        doc_id = gold_ev.get("doc_id", "")
        item = gold_ev.get("item", "")
        for ctx in contexts:
            if doc_id.lower() in ctx.lower() or item.lower() in ctx.lower():
                return True
        return False

    norm_quote = normalize_text(quote)
    # Check exact normalized substring or key multi-word n-gram overlap
    words = norm_quote.split()
    if len(words) <= 5:
        sub_phrases = [norm_quote]
    else:
        # Check first and last 6 words
        sub_phrases = [" ".join(words[:6]), " ".join(words[-6:]), " ".join(words[len(words)//2 - 3 : len(words)//2 + 3])]

    for ctx in contexts:
        norm_ctx = normalize_text(ctx)
        if any(p in norm_ctx for p in sub_phrases if len(p) > 10):
            return True
        # Also check substantial word overlap
        quote_words = set(words)
        ctx_words = set(norm_ctx.split())
        overlap = len(quote_words.intersection(ctx_words))
        if overlap / max(1, len(quote_words)) >= 0.65:
            return True

    return False


def evaluate_records(benchmark_path: Path, records_path: Path) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """Evaluate retrieval completeness across all systems recorded in records.jsonl."""
    raw_bench = json.loads(benchmark_path.read_text(encoding="utf-8"))
    gold_by_id = {q["id"]: q for q in raw_bench}

    lines = [json.loads(l) for l in records_path.read_text(encoding="utf-8").splitlines() if l.strip()]

    eval_rows = []
    for r in lines:
        sys_name = r.get("system")
        qid = r.get("question_id") or r.get("query_id")
        gold_q = gold_by_id.get(qid)
        if not gold_q:
            continue

        gold_evidence_list = gold_q.get("gold_evidence", [])
        contexts = r.get("retrieved_contexts", [])
        if not contexts and "prediction" in r:
            contexts = [r["prediction"]]

        # Track evidence hits
        hits = 0
        gold_sections: Set[str] = set()
        retrieved_sections: Set[str] = set()

        for ev in gold_evidence_list:
            sec = ev.get("item") or ev.get("section") or "Item 7"
            gold_sections.add(sec.split(".")[0].strip())
            if evidence_in_contexts(ev, contexts):
                hits += 1
                retrieved_sections.add(sec.split(".")[0].strip())

        total_ev = len(gold_evidence_list)
        ev_recall = hits / max(1, total_ev) if total_ev > 0 else 1.0
        all_found = (hits == total_ev) if total_ev > 0 else True

        # Cross-section evaluation
        is_cross_section = len(gold_sections) > 1
        cross_section_hit = (len(retrieved_sections) == len(gold_sections)) if is_cross_section else None

        # Context Precision (heuristic: ratio of contexts containing at least one gold mention)
        relevant_chunks = 0
        for ctx in contexts:
            for ev in gold_evidence_list:
                if evidence_in_contexts(ev, [ctx]):
                    relevant_chunks += 1
                    break
        ctx_precision = relevant_chunks / max(1, len(contexts)) if contexts else 0.0

        eval_rows.append({
            "system": sys_name,
            "question_id": qid,
            "hop_type": gold_q.get("hop", "single"),
            "recipe": gold_q.get("recipe", "table"),
            "total_gold_evidence": total_ev,
            "retrieved_gold_evidence": hits,
            "evidence_recall": ev_recall,
            "all_evidence_found": all_found,
            "is_cross_section": is_cross_section,
            "cross_section_hit": cross_section_hit,
            "retrieved_chunks_count": len(contexts),
            "context_precision": ctx_precision,
            "hops_executed": r.get("hops", 1),
        })

    df = pd.DataFrame(eval_rows)
    summary: Dict[str, Any] = {}

    for s in SYSTEMS:
        sdf = df[df["system"] == s]
        if sdf.empty:
            continue

        n_q = len(sdf)
        mean_recall = float(sdf["evidence_recall"].mean() * 100)
        full_evidence_rate = float(sdf["all_evidence_found"].mean() * 100)
        mean_precision = float(sdf["context_precision"].mean() * 100)

        # Multi-hop slice
        m_df = sdf[sdf["hop_type"] == "multi"]
        m_recall = float(m_df["evidence_recall"].mean() * 100) if not m_df.empty else 0.0
        m_full = float(m_df["all_evidence_found"].mean() * 100) if not m_df.empty else 0.0

        # Cross-section slice
        cs_df = sdf[sdf["is_cross_section"] == True]
        cs_discovery_rate = float(cs_df["cross_section_hit"].mean() * 100) if not cs_df.empty else 100.0

        summary[s] = {
            "n_queries": n_q,
            "overall_evidence_recall_pct": round(mean_recall, 2),
            "full_evidence_discovery_rate_pct": round(full_evidence_rate, 2),
            "context_precision_pct": round(mean_precision, 2),
            "multihop_evidence_recall_pct": round(m_recall, 2),
            "multihop_full_discovery_pct": round(m_full, 2),
            "cross_section_discovery_rate_pct": round(cs_discovery_rate, 2),
            "mean_chunks_retrieved": round(float(sdf["retrieved_chunks_count"].mean()), 1),
            "mean_hops_executed": round(float(sdf["hops_executed"].mean()), 2),
        }

    return df, summary


def main():
    parser = argparse.ArgumentParser(description="RQ1 Retrieval Completeness Evaluation.")
    parser.add_argument("--benchmark", type=Path, default=DEFAULT_BENCHMARK, help="Path to benchmark JSON.")
    parser.add_argument("--records", type=Path, default=DEFAULT_RECORDS, help="Path to evaluation records JSONL.")
    parser.add_argument("--out-csv", type=Path, default=DEFAULT_OUT_CSV, help="Output summary metrics CSV.")
    parser.add_argument("--out-json", type=Path, default=DEFAULT_OUT_JSON, help="Output summary metrics JSON.")
    args = parser.parse_args()

    args.out_csv.parent.mkdir(parents=True, exist_ok=True)
    args.out_json.parent.mkdir(parents=True, exist_ok=True)

    print(f"Loading benchmark: {args.benchmark}")
    print(f"Evaluating records: {args.records}")

    df, summary = evaluate_records(args.benchmark, args.records)

    # Convert summary to DataFrame for CSV export
    rows = []
    for s, data in summary.items():
        rows.append({"system": s, **data})
    summary_df = pd.DataFrame(rows)

    summary_df.to_csv(args.out_csv, index=False)
    args.out_json.write_text(json.dumps(summary, indent=2), encoding="utf-8")

    print("\n" + "=" * 80)
    print("🎯 RQ1 RETRIEVAL COMPLETENESS & EVIDENCE SUFFICIENCY SCORECARD")
    print("=" * 80)
    print(summary_df.to_string(index=False))
    print("=" * 80)
    print(f"Saved CSV scorecard:  {args.out_csv}")
    print(f"Saved JSON scorecard: {args.out_json}\n")


if __name__ == "__main__":
    main()
