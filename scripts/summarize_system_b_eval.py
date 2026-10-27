"""Summarize saved runs without making additional model calls.

Reference word overlap is a diagnostic proxy, NOT answer correctness or faithfulness.
Citation checks validate label existence, NOT support for claims.
"""
import argparse
from collections import Counter, defaultdict
import csv
import hashlib
import json
from pathlib import Path
import re
import statistics
import unicodedata


def words(text):
    text = re.sub(r'(?:\[|【)\d+(?:\]|】)', '', text or '')
    return re.findall(r'\w+', unicodedata.normalize('NFKC', text).lower())


def reference_f1(answer, reference):
    a, b = Counter(words(answer)), Counter(words(reference))
    overlap = sum((a & b).values())
    return 2 * overlap / (sum(a.values()) + sum(b.values())) if a and b else 0.0


def percentile(values, p):
    if not values:
        return None
    ordered = sorted(values)
    pos = (len(ordered) - 1) * p
    lo = int(pos)
    hi = min(lo + 1, len(ordered) - 1)
    return ordered[lo] + (ordered[hi] - ordered[lo]) * (pos - lo)


def summarize(rows):
    groups = defaultdict(list)
    per_query = []
    for row in rows:
        success = row.get('status') in ('ok', 'no_evidence')
        answer = row.get('answer') or ''
        labels = re.findall(r'(?:\[|【)(\d+)(?:\]|】)', answer)
        invalid = set(labels) - set(row.get('citations', {}))
        usage = row.get('usage') or {}
        item = {
            'question_id': row.get('question_id'), 'mode': row.get('mode'),
            'category': row.get('category'), 'status': row.get('status'),
            'error': row.get('error'), 'answer': '\n'.join(line.rstrip() for line in answer.splitlines()),
            'reference_token_f1_proxy': reference_f1(answer, row.get('ground_truth_answer')) if success else None,
            'has_recognized_citation': bool(labels) if success else None,
            'invalid_citation_label_count': len(invalid) if success else None,
            'explicit_abstention': 'not found in the provided context' in answer.lower() if success else None,
            'pure_abstention': words(answer) == words('Not found in the provided context') if success else None,
            'total_seconds': row.get('timings', {}).get('total_seconds'),
            'retrieval_seconds': row.get('timings', {}).get('retrieval_seconds'),
            'generation_seconds': row.get('timings', {}).get('generation_seconds'),
            'prompt_tokens': usage.get('prompt_tokens'),
            'completion_tokens': usage.get('completion_tokens'),
            'total_tokens': usage.get('total_tokens'),
            'finish_reason': row.get('finish_reason'),
            'rate_limit_retries': row.get('rate_limit_retries'),
        }
        per_query.append(item)
        groups[row.get('mode')].append(item)
    summary = {}
    for mode, group in groups.items():
        good = [r for r in group if r['status'] in ('ok', 'no_evidence')]
        times = [r['total_seconds'] for r in good if r['total_seconds'] is not None]
        summary[mode] = {
            'attempts': len(group), 'completed': len(good),
            'failures': sum(r['status'] == 'error' for r in group),
            'retrieval_only': sum(r['status'] == 'retrieval_only' for r in group),
            'mean_reference_token_f1_proxy': statistics.mean(r['reference_token_f1_proxy'] for r in good) if good else None,
            'answers_with_recognized_citations': sum(r['has_recognized_citation'] for r in good),
            'answers_with_invalid_citation_labels': sum(r['invalid_citation_label_count'] > 0 for r in good),
            'explicit_abstentions': sum(r['explicit_abstention'] for r in good),
            'pure_abstentions': sum(r['pure_abstention'] for r in good),
            'latency_p50_seconds': percentile(times, .5),
            'latency_p90_seconds': percentile(times, .9),
            'total_reported_tokens': sum(r['total_tokens'] or 0 for r in good),
            'missing_usage_count': sum(r['total_tokens'] is None for r in good),
            'truncated_outputs': sum(r['finish_reason'] == 'length' for r in good),
            'finish_reason_not_recorded': sum(r['finish_reason'] is None for r in good),
            'recorded_rate_limit_retries': sum(r['rate_limit_retries'] or 0 for r in good),
        }
    return summary, per_query


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input', type=Path)
    parser.add_argument('--output-dir', type=Path, required=True)
    parser.add_argument('--judgments', type=Path, help='Optional output from judge_system_b_eval.py')
    args = parser.parse_args()
    raw = args.input.read_bytes()
    rows = [json.loads(line) for line in raw.decode('utf-8').splitlines() if line.strip()]
    keys = [(r.get('question_id'), r.get('mode')) for r in rows]
    if len(keys) != len(set(keys)):
        raise ValueError('Duplicate question/mode results; resolve retries before summarizing')
    summary, per_query = summarize(rows)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    report = {
        'source': str(args.input), 'source_sha256': hashlib.sha256(raw).hexdigest(),
        'rows': len(rows), 'unique_questions': len({k[0] for k in keys}),
        'limitations': [
            'Reference token F1 is word overlap, not semantic correctness or faithfulness.',
            'Citation checks recognize single numeric labels and validate existence only.',
            'Ground-truth answers have not all been independently reviewed.',
            'Failed requests may incur tokens absent from provider usage totals.',
            'Latency includes cold model initialization on first use and excludes corpus setup.',
            'No RAGAS, numerical-verification, evidence-recall, alpha sweep, or context-size sweep is claimed.',
        ],
        'modes': summary,
    }
    if args.judgments:
        judgments = [json.loads(line) for line in args.judgments.read_text(encoding='utf-8').splitlines() if line.strip()]
        if any(j.get('input_sha256') != report['source_sha256'] for j in judgments):
            raise ValueError('Judgments do not match this result file')
        judge_keys = [(j['question_id'], j['mode']) for j in judgments]
        if len(judge_keys) != len(set(judge_keys)) or set(judge_keys) != set(keys):
            raise ValueError('Judgments must cover every question/mode exactly once')
        judged_modes = {}
        for mode in summary:
            entries = [j for j in judgments if j['mode'] == mode]
            good = [j for j in entries if j['status'] == 'ok']
            stats = {'judged': len(good), 'errors': sum(j['status'] == 'error' for j in entries),
                     'skipped': sum(j['status'] == 'skipped' for j in entries)}
            for metric in ('correctness', 'faithfulness', 'citation_support', 'numerical_accuracy'):
                scores = [j['judgment'][metric] for j in good if j['judgment'][metric] is not None]
                stats[metric + '_mean'] = statistics.mean(scores) if scores else None
                stats[metric + '_n'] = len(scores)
            judged_modes[mode] = stats
        report['provisional_model_judgments'] = judged_modes
        report['limitations'].append('Custom same-model judgments are not RAGAS or human-validated scores; self-evaluation bias is possible.')
    (args.output_dir / 'summary.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
    with (args.output_dir / 'per_query.csv').open('w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=list(per_query[0]))
        writer.writeheader()
        writer.writerows(per_query)
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
