"""System A command line: RAG 5 (default), RAG 3, RAG 4 or RAG 6, for one query or the benchmark.

Run from the repo root (e.g. in the container, /workspace):
  python -m src.system_a --query "What was NVIDIA's total revenue?" --tickers NVDA --years 2026
  python -m src.system_a --query "..." --tickers NVDA --years 2026 --variant rag4
  python -m src.system_a --benchmark                          # every QA, RAG 5
  python -m src.system_a --benchmark --all-variants --limit 10   # RAG 5, 3, 4 and 6
  python -m src.system_a --benchmark --no-generate            # retrieval metrics only, no LLM calls
"""
import argparse
import sys
from datetime import datetime
from pathlib import Path

import pandas as pd

from .evaluate import DEFAULT_BENCHMARK, ROOT, load_benchmark, run_benchmark, summarize
from .llm import DEFAULT_MODEL
from .pipeline import DEFAULT_VARIANT, TOP_K, VARIANTS, generate, show_hits
from .retrieval import EMBED_MODEL, ChromaIndex, QueryEmbedder, SupabaseIndex


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description="System A: RAG 5 / RAG 3 / RAG 4 / RAG 6 (dense retrieval, one LLM call)")
    inputs = parser.add_mutually_exclusive_group(required=True)
    inputs.add_argument("--query", help="Answer one question")
    inputs.add_argument("--benchmark", type=Path, nargs="*",
                        help="Benchmark .jsonl files; later files override QAs with the same id "
                             f"(default: {' + '.join(str(p.relative_to(ROOT)) for p in DEFAULT_BENCHMARK)})")
    # Variant
    parser.add_argument("--variant", choices=list(VARIANTS), default=DEFAULT_VARIANT)
    parser.add_argument("--all-variants", action="store_true", help=f"Run every variant ({', '.join(VARIANTS)})")
    # Index
    parser.add_argument("--chroma-dir", default="chroma_db")
    parser.add_argument("--collection", help="Override the variant's own collection (see VARIANTS in pipeline.py)")
    parser.add_argument("--embed-model", default=EMBED_MODEL, help="Must match the model that built the collection")
    parser.add_argument("--store", choices=["supabase", "chroma"], default="supabase",
                        help="Vector store backend: 'supabase' (sec_chunks pgvector, default) or local 'chroma'")
    parser.add_argument("--supabase-table", default="sec_chunks")
    # Retrieval
    parser.add_argument("--top-k", type=int, default=TOP_K)
    parser.add_argument("--tickers", nargs="+", default=[], help="--query only: limit to these companies")
    parser.add_argument("--years", nargs="+", type=int, default=[], help="--query only: limit to these fiscal years")
    parser.add_argument("--scope", choices=["gold", "none"], default="gold",
                        help="--benchmark only: filter to each QA's gold companies/years, or search the whole corpus")
    # Generation
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--no-generate", action="store_true", help="Retrieve only, no LLM calls")
    # Benchmark run
    parser.add_argument("--limit", type=int, help="Only the first N QAs")
    parser.add_argument("--ids", nargs="+", help="Only these QA ids")
    parser.add_argument("--num-tol", type=float, default=0.01, help="Relative tolerance for numeric answers")
    parser.add_argument("--sleep", type=float, default=0.0, help="Seconds between LLM calls (stay under rate limits)")
    parser.add_argument("--out", type=Path, help="Results .jsonl (default: results/system_a_<variants>_<time>.jsonl)")
    args = parser.parse_args()

    variants = list(VARIANTS) if args.all_variants else [args.variant]
    embedder = QueryEmbedder(args.embed_model)
    opened = {}                                       # variants that share a collection share one index
    for variant in variants:
        collection = args.collection or VARIANTS[variant]["collection"]
        if collection not in opened:
            if args.store == "supabase":
                opened[collection] = SupabaseIndex(args.supabase_table, embedder)
            else:
                opened[collection] = ChromaIndex(args.chroma_dir, collection, embedder)
    indexes = {v: opened[args.collection or VARIANTS[v]["collection"]] for v in variants}

    if args.query:
        pairs = [(t, y) for t in args.tickers or [None] for y in args.years or [None]] if args.tickers or args.years else []
        if any(VARIANTS[v]["financials"] for v in variants) and not args.tickers:
            print("Note: rag4/rag6 add financials.csv rows only for the companies given with --tickers")
        for variant, index in indexes.items():
            hits = index.retrieve(args.query, args.top_k, pairs)
            print(f"=== {variant} ({index.name}) ===")
            if not args.no_generate:
                out = generate(args.query, hits, variant, pairs, args.model)
                print(out["answer"], "\n")
                if out["financials"]:
                    print("\n".join(out["financials"]), "\n")
            show_hits(hits)
        return

    qas = load_benchmark(args.benchmark)
    if args.ids:
        qas = [qa for qa in qas if qa["id"] in set(args.ids)]
    if args.limit:
        qas = qas[:args.limit]
    out = args.out or ROOT / "results" / f"system_a_{'-'.join(variants)}_{datetime.now():%Y%m%d_%H%M%S}.jsonl"
    print(f"{len(qas)} QAs, variants: {', '.join(variants)}, scope: {args.scope}, top-k: {args.top_k}"
          + (", retrieval only" if args.no_generate else f", model: {args.model}"))
    df = run_benchmark(indexes, qas, args.top_k, args.scope, not args.no_generate,
                       args.model, out, args.num_tol, args.sleep)
    overall, by_recipe = summarize(df)
    with pd.option_context("display.width", 200, "display.max_columns", 20):
        print("\n=== Overall ===\n", overall, "\n\n=== By recipe ===\n", by_recipe, sep="")
    print(f"\nPer-question results: {out}")


if __name__ == "__main__":
    main()
