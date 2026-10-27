#!/usr/bin/env python3
"""
Sync and filter benchmark QA dataset from upstream branch (origin/feature/benchmark_set).

This script isolates Amanda's benchmark dataset and extracts a verified pool
strictly for filings from 2015 onwards, ensuring our production and UI pipelines
remain reproducible and immune to upstream branch mutation.

Usage:
    python scripts/sync_benchmark_pool.py
    python scripts/sync_benchmark_pool.py --min-year 2015 --stats
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List, Set

REPO_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = REPO_ROOT / "data"
UPSTREAM_BRANCH = "origin/feature/benchmark_set"
UPSTREAM_FILE = "benchmark/benchmark_qa_0.jsonl"


def fetch_upstream() -> None:
    """Fetch latest commits from origin without merging or switching branches."""
    print(f"[*] Fetching latest remote branches from origin...")
    try:
        subprocess.run(["git", "fetch", "origin", "feature/benchmark_set"], check=True, capture_output=True)
    except subprocess.CalledProcessError as e:
        print(f"[!] Warning: git fetch origin feature/benchmark_set failed: {e.stderr.decode('utf-8', errors='ignore')}")
        print("[*] Proceeding with cached remote branch if available.")


def load_upstream_benchmark(source_ref: str = f"{UPSTREAM_BRANCH}:{UPSTREAM_FILE}") -> List[Dict[str, Any]]:
    """Load benchmark JSONL directly from git object store."""
    print(f"[*] Reading {source_ref} from git object tree...")
    try:
        raw_output = subprocess.check_output(["git", "show", source_ref]).decode("utf-8")
        records = [json.loads(line) for line in raw_output.strip().splitlines() if line.strip()]
        print(f"[+] Successfully loaded {len(records)} benchmark questions from upstream.")
        return records
    except Exception as e:
        # Fallback to local data/benchmark_qa_0.jsonl if git show fails
        local_fallback = DATA_DIR / "benchmark_qa_0.jsonl"
        if local_fallback.exists():
            print(f"[*] Reading local fallback from {local_fallback}...")
            return [json.loads(line) for line in local_fallback.read_text(encoding="utf-8").splitlines() if line.strip()]
        raise RuntimeError(f"Could not load upstream benchmark from {source_ref} or local fallback: {e}")


def get_all_cited_years(item: Dict[str, Any]) -> List[int]:
    """Collect top-level year and every year cited in gold_evidence."""
    years: Set[int] = set()
    if item.get("year"):
        try:
            years.add(int(item["year"]))
        except (ValueError, TypeError):
            pass
    for ev in item.get("gold_evidence", []):
        if ev.get("year"):
            try:
                years.add(int(ev["year"]))
            except (ValueError, TypeError):
                pass
    return sorted(list(years))


def filter_pool(records: List[Dict[str, Any]], min_year: int = 2015) -> List[Dict[str, Any]]:
    """Filter records so that ALL cited years are >= min_year."""
    pool = []
    for r in records:
        cited_years = get_all_cited_years(r)
        if cited_years and all(y >= min_year for y in cited_years):
            r_copy = dict(r)
            r_copy["applicable_years"] = cited_years
            pool.append(r_copy)
    return pool


def main() -> None:
    parser = argparse.ArgumentParser(description="Sync and filter benchmark QA pool.")
    parser.add_argument("--min-year", type=int, default=2015, help="Minimum fiscal year allowed (default: 2015)")
    parser.add_argument("--skip-fetch", action="store_true", help="Skip running git fetch origin")
    parser.add_argument("--stats", action="store_true", default=True, help="Print category/ticker statistics")
    args = parser.parse_args()

    if not args.skip_fetch:
        fetch_upstream()

    records = load_upstream_benchmark()
    pool = filter_pool(records, min_year=args.min_year)

    DATA_DIR.mkdir(parents=True, exist_ok=True)

    # 1. Save full upstream copy for reference
    upstream_dest = DATA_DIR / "benchmark_qa_0.jsonl"
    with open(upstream_dest, "w", encoding="utf-8") as f:
        for r in records:
            f.write(json.dumps(r) + "\n")

    # 2. Save filtered pool (JSON and JSONL)
    pool_json_dest = DATA_DIR / f"benchmark_qa_pool_{args.min_year}.json"
    pool_jsonl_dest = DATA_DIR / f"benchmark_qa_pool_{args.min_year}.jsonl"

    with open(pool_json_dest, "w", encoding="utf-8") as f:
        json.dump(pool, f, indent=2)

    with open(pool_jsonl_dest, "w", encoding="utf-8") as f:
        for r in pool:
            f.write(json.dumps(r) + "\n")

    print(f"\n[✓] Upstream copy saved: {upstream_dest} ({len(records)} questions)")
    print(f"[✓] {args.min_year}+ Pool saved: {pool_json_dest} ({len(pool)} questions)")
    print(f"[✓] {args.min_year}+ JSONL saved: {pool_jsonl_dest}")

    if args.stats:
        from collections import Counter
        recipes = Counter(q.get("recipe") for q in pool)
        tickers = Counter(q.get("ticker") for q in pool)
        types = Counter(q.get("type") for q in pool)
        print("\n--- Benchmark Pool Summary (FY >= " + str(args.min_year) + ") ---")
        print("Total Questions:", len(pool))
        print("Recipes:", dict(recipes))
        print("Tickers:", dict(sorted(tickers.items())))
        print("Types:", dict(types))


if __name__ == "__main__":
    main()
