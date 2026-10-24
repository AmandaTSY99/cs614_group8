"""python -m src.system_b --help"""
import argparse
from dataclasses import asdict, replace
import json
import os
from pathlib import Path
import sys
from time import perf_counter

from .adapters import BGE_MODEL, ChromaSource, Generator, Reranker
from .pipeline import run
from .retrieval import Config, Retriever, Scope


def main():
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    parser = argparse.ArgumentParser(description='System B: RAG3 + BM25 + cross-encoder, single pass')
    inputs = parser.add_mutually_exclusive_group(required=True)
    inputs.add_argument('--query')
    inputs.add_argument('--benchmark', type=Path, help='JSON list of golden questions')
    parser.add_argument('--chroma-dir', default='chroma_db')
    parser.add_argument('--collection', default='rag3_structure_bge')
    parser.add_argument('--tickers', nargs='+', default=[])
    parser.add_argument('--years', nargs='+', type=int, default=[])
    parser.add_argument('--alpha', type=float, default=0.5)
    parser.add_argument('--candidates', type=int, default=30)
    parser.add_argument('--rerank-candidates', type=int, default=30)
    parser.add_argument('--top-k', type=int, default=5)
    parser.add_argument('--mode', choices=['dense', 'bm25', 'hybrid', 'hybrid_rerank'], default='hybrid_rerank')
    parser.add_argument('--all-modes', action='store_true', help='Benchmark all four retrieval variants')
    parser.add_argument('--reranker', default='BAAI/bge-reranker-large')
    parser.add_argument('--generate', action='store_true', help='Make paid/provider LLM calls; otherwise retrieval only')
    parser.add_argument('--model', default=os.environ.get('SYSTEM_B_MODEL'))
    parser.add_argument('--base-url', default=os.environ.get('SYSTEM_B_BASE_URL'))
    parser.add_argument('--limit', type=int, default=0, help='First N benchmark questions; 0 means all')
    parser.add_argument('--output', type=Path, help='New JSONL output file; existing files are never overwritten')
    parser.add_argument('--resume-from', type=Path, help='Reuse successful matching rows from a previous JSONL run')
    args = parser.parse_args()
    if args.generate and not args.model:
        parser.error('--generate requires --model or SYSTEM_B_MODEL')
    if args.all_modes and not args.benchmark:
        parser.error('--all-modes requires --benchmark')
    if args.limit < 0:
        parser.error('--limit cannot be negative')
    if args.benchmark and not args.output:
        parser.error('--benchmark requires --output')
    if args.output and args.output.exists():
        parser.error('--output already exists; choose a new run filename')
    try:
        config = Config(args.alpha, args.candidates, args.rerank_candidates, args.top_k, args.mode)
        if args.benchmark:
            items = json.loads(args.benchmark.read_text(encoding='utf-8-sig'))
            if not isinstance(items, list) or not items:
                raise ValueError('Benchmark must be a nonempty JSON list')
            if args.limit:
                items = items[:args.limit]
        else:
            items = [{'id': 'interactive', 'query': args.query, 'target_tickers': args.tickers,
                      'fiscal_years': args.years}]
        if any(not isinstance(q.get('query'), str) or not q['query'].strip() for q in items):
            raise ValueError('Each benchmark entry requires a nonempty query')
        previous = {}
        if args.resume_from:
            for line in args.resume_from.read_text(encoding='utf-8').splitlines():
                row = json.loads(line)
                if row.get('status') not in ('ok', 'no_evidence', 'retrieval_only'):
                    continue
                if args.generate and row.get('status') == 'retrieval_only':
                    continue
                expected = asdict(replace(config, mode=row['mode']))
                if row.get('config') != expected or row.get('collection') != args.collection:
                    raise ValueError('Resume configuration differs from this run')
                if bool(row.get('answer') is not None) != args.generate:
                    raise ValueError('Resume generation mode differs')
                if args.generate and row.get('model') and row['model'] != args.model:
                    raise ValueError('Resume generator model differs')
                previous[(row['question_id'], row['mode'])] = row
        setup_start = perf_counter()
        source = ChromaSource(args.chroma_dir, args.collection)
        records = source.records()
        available = {(r['meta']['ticker'], r['meta']['fiscal_year']) for r in records}
        reranker = Reranker(args.reranker)
        retriever = Retriever(records, source, reranker, config)
        generator = Generator(args.model, args.base_url) if args.generate else None
        setup_seconds = perf_counter() - setup_start
    except Exception as exc:
        print(f'Setup failed: {type(exc).__name__}: {exc}', file=sys.stderr)
        return 2
    modes = ['dense', 'bm25', 'hybrid', 'hybrid_rerank'] if args.all_modes else [args.mode]
    failures = 0
    stream = None
    try:
        if args.output:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            stream = args.output.open('x', encoding='utf-8')
        for item in items:
            tickers = item.get('target_tickers') or ([item['ticker']] if item.get('ticker') else [])
            scope = (Scope(filing_pairs=tuple((t.upper(), int(y)) for t, y in item['filing_pairs']))
                     if item.get('filing_pairs') else
                     Scope(tuple(t.upper() for t in tickers), tuple(item.get('fiscal_years', []))))
            for mode in modes:
                retriever.config = replace(config, mode=mode)
                saved = previous.get((item.get('id'), mode))
                if saved:
                    if saved['query'] != item['query'] or saved['scope'] != scope.payload():
                        raise ValueError('Resume question/scope differs')
                    if stream:
                        stream.write(json.dumps(saved, ensure_ascii=False) + '\n')
                        stream.flush()
                    print(f"{saved['question_id']} {mode}: reused")
                    continue
                row = {'question_id': item.get('id'), 'category': item.get('category'),
                       'mode': mode, 'collection': args.collection, 'embedding_model': BGE_MODEL,
                       'reranker_model': args.reranker if mode == 'hybrid_rerank' else None,
                       'corpus_chunks': len(records), 'setup_seconds': setup_seconds,
                       'ground_truth_answer': item.get('ground_truth_answer'),
                       'timing_note': 'First use includes lazy model loading; later calls reuse models.'}
                try:
                    required = scope.filing_pairs or tuple((t, y) for t in scope.tickers for y in scope.years)
                    missing = [pair for pair in required if pair not in available]
                    if missing:
                        raise ValueError(f'Requested filings absent from RAG3: {missing}')
                    row.update(run(retriever, item['query'], scope, generator))
                    gold = item.get('gold_chunk_ids')
                    if gold:
                        row['evidence_recall_at_k'] = len(set(gold) & {h['id'] for h in row['hits']}) / len(set(gold))
                except Exception as exc:
                    failures += 1
                    row.update(status='error', error=f'{type(exc).__name__}: {exc}',
                               config=asdict(retriever.config), query=item['query'])
                line = json.dumps(row, ensure_ascii=False)
                if stream:
                    stream.write(line + '\n')
                    stream.flush()
                print(line if not args.benchmark else f"{row['question_id']} {mode}: {row['status']}")
                if row.get('status') == 'error' and 'tokens per day' in row.get('error', '').lower():
                    print('Daily provider quota exhausted. Saved results can be resumed with --resume-from.', file=sys.stderr)
                    return 3
    finally:
        if stream:
            stream.close()
    return 1 if failures else 0


if __name__ == '__main__':
    raise SystemExit(main())
