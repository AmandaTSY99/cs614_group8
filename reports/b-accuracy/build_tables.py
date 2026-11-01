"""Reconstruct the completed replay and publish reproducible slide tables (no API calls)."""
import csv
import json
import statistics
import sys
import hashlib
from pathlib import Path

sys.path.insert(0, str(Path.cwd()))
from src.system_b.retrieval import diversify_tail
from scripts.rq2.common import question_dimensions, ragas_reference
from scripts.rq2.metrics_custom import custom_scores
from scripts.rq2.analysis import paired_comparisons

ROOT = Path('reports/b-accuracy')
def read(p):
    return [json.loads(s) for s in Path(p).read_text(encoding='utf8').splitlines() if s.strip()]
def write_rows(p, rows):
    Path(p).write_text(''.join(json.dumps(r, ensure_ascii=False)+'\n' for r in rows), encoding='utf8')

questions = {q['id']: q for q in json.loads(Path('data/benchmark_qa_pool_2015.json').read_text(encoding='utf8'))}
answers = read(ROOT/'answers.jsonl')
indexed = {(r['arm'], r['id']): r for r in answers}
assert len(indexed) == len(answers) == 194
assert set(indexed) == {(arm, qid) for arm in ('A', 'B') for qid in questions}
assert len(questions) == 97
frozen = {(r['system'], r['question_id']): r for r in read('reports/rq2/full_v3/records.jsonl')}
def hits(rec):
    return [dict(id=m['chunk_id'], text=t, meta=m) for t,m in zip(rec['retrieved_contexts'],rec['contexts_meta'],strict=True)]

records, scores = [], []
for qid,q in questions.items():
    for arm in ('A','B'):
        system = 'system_'+arm.lower()
        saved = indexed[arm,qid]
        original = frozen[system,qid]
        selected = hits(original)
        if arm == 'B':
            selected = diversify_tail(selected, hits(frozen['system_a',qid]), 10)
        citations = []
        for n,h in enumerate(selected,1):
            if f'[{n}]' in saved['answer'] or (arm=='B' and f'【{n}】' in saved['answer']):
                citations.append(dict(tag=f'[{n}]',chunk_id=h['id'],**{k:h['meta'].get(k) for k in ('ticker','fiscal_year','section')}))
        rec = {k:original[k] for k in ('question_id','question','type','ground_truth_answer','ground_truth_numbers','target_sections') if k in original}
        rec.update(system=system,answer=saved['answer'],retrieved_contexts=[h['text'] for h in selected],
                   contexts_meta=[h['meta'] for h in selected],citations=citations,guardrail_report=None,
                   dims=question_dimensions(q),ragas_reference=ragas_reference(q),model=saved['model'],
                   keypoint_recall=saved['score'] if q['type']!='numeric' else None,
                   provenance='Exact saved-context replay reconstruction; see replay.py')
        records.append(rec)
        base=dict(system=system,question_id=qid,dims=rec['dims'],category=original.get('category'),judge='none')
        scores.append(dict(base,metric='primary_accuracy',value=saved['score'],status='ok'))
        for metric,(value,status,detail) in custom_scores(rec).items():
            scores.append(dict(base,metric=metric,value=value,status=status,detail=detail))
write_rows(ROOT/'records.jsonl',records)
write_rows(ROOT/'custom_scores.jsonl',scores)

# Preserve separately judged RAGAS outputs and include only successful judgments.
llm_path=ROOT/'scores_ragas_groq.jsonl'
latest={}
if llm_path.exists():
    latest={(r['system'],r['question_id'],r['metric']):r for r in read(llm_path)}
ragas_metrics=('faithfulness','answer_relevancy','context_recall','context_precision','factual_correctness')
coverage={}
for system in ('system_a','system_b'):
    coverage[system]={}
    for metric in ragas_metrics:
        rows=[r for r in latest.values() if r['system']==system and r['metric']==metric]
        counts={status:sum(r['status']==status for r in rows) for status in ('ok','na','error','truncated','too_large')}
        counts['missing']=97-len(rows)
        coverage[system][metric]=counts
complete=all(c['ok']+c['na']==97 for metrics_ in coverage.values() for c in metrics_.values())
publish='--publish' in sys.argv
if complete or not publish:
    scores += [r for r in latest.values() if r['metric'] in ragas_metrics]
(ROOT/'ragas_coverage.json').write_text(json.dumps(dict(complete=complete,coverage=coverage),indent=2),encoding='utf8')
sources=['data/benchmark_qa_pool_2015.json','reports/rq2/full_v3/records.jsonl',
         'reports/rq2/full_v3/aggregate_scores_gpt4omini.csv',str(ROOT/'answers.jsonl')]
manifest=dict(base_commit='ffc6e002ea83d99c12fba0da5134cae2fb103f9a',expected_questions=97,answer_records=194,
              generation=dict(provider='groq',model='openai/gpt-oss-120b',temperature=0,max_completion_tokens=1024,reasoning_effort='low'),
              context_mode='Archived-context replay; A dense contexts used as proxy for B dense supplement',
              hash_encoding='UTF-8 text normalized to LF newlines (portable across Git checkouts)',
              sha256={p.replace('\\','/'):hashlib.sha256(Path(p).read_text(encoding='utf8').encode('utf8')).hexdigest() for p in sources})
(ROOT/'provenance.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf8')
comparisons=paired_comparisons(scores,systems=['system_a','system_b'])
(ROOT/'table_comparisons.json').write_text(json.dumps(comparisons,indent=2),encoding='utf8')
comp={(r['metric'],r['group']):r for r in comparisons}
historical=list(csv.DictReader(Path('reports/rq2/full_v3/aggregate_scores_gpt4omini.csv').open(encoding='utf8')))
def historical_mean(metric,group):
    rows=[r for r in historical if r['system']=='system_c_v1' and r['metric']==metric and r['category']==group]
    return float(rows[0]['mean']) if rows and rows[0]['mean'] else None
def values(system,metric,ids):
    return [r['value'] for r in scores if r['system']==system and r['metric']==metric and r['question_id'] in ids and r['status']=='ok' and r['value'] is not None]
def sig(metric,group):
    c=comp.get((metric,group))
    if not c:return 'Pending'
    return ('B > A' if c['mean_diff']>0 else 'A > B') if c['significant'] else 'Not significant'

groups=[('All questions','overall',lambda q:True),('Narrative','answer_type=narrative',lambda q:q['type']=='qualitative'),
        ('Numerical / table','answer_type=numerical',lambda q:q['type']=='numeric'),('Mixed text + table','answer_type=mixed',lambda q:q['type']=='mixed'),
        ('Single-hop','hop=single',lambda q:q['hop']=='single'),('Multi-hop','hop=multi',lambda q:q['hop']=='multi'),
        ('Cross-year','evidence_scope=cross_year',lambda q:q['scope']=='cross_year')]
lines=['# Updated System B slide tables','',
       'All 97 distinct expected question IDs have one A and one revised B answer (194 records). Both use Groq openai/gpt-oss-120b, temperature 0. Primary accuracy is final. '+('RAGAS evaluation is complete.' if complete else 'RAGAS evaluation is IN PROGRESS; '+('partial judgments are excluded from this publication snapshot.' if publish else 'available RAGAS means and significance are interim.')),
       '', '## Primary accuracy', '',
       '| Question type | A: Dense (Groq) | Revised B: Hybrid (Groq) | C v1: Historical GPT-5.4 reference | Paired significance A/B |',
       '|---|---:|---:|---:|---|']
for label,group,predicate in groups:
    ids={qid for qid,q in questions.items() if predicate(q)}
    a,b=[statistics.mean(values(s,'primary_accuracy',ids)) for s in ('system_a','system_b')]
    c=historical_mean('primary_accuracy',group)
    lines.append(f'| {label} (n={len(ids)}) | {a:.2f} | {b:.2f} | {c:.2f} | {sig("primary_accuracy",group)} |')
lines+=['','Primary accuracy uses numerical matching for numeric questions and key-point recall for qualitative/mixed questions. The numerical/table and mixed labels follow team answer-type facets; they are not independent evidence-format filters.',
        '', '## Faithfulness, relevance and citations', '',
        '| Metric | What it checks | A: Dense (Groq) | Revised B (Groq) | C v1: Historical reference | Paired significance A/B |',
        '|---|---|---:|---:|---:|---|']
metrics=[('faithfulness','Faithfulness','Claims supported by retrieved text (answered cases)'),
         ('answer_relevancy','Answer relevancy','Answer addresses the question'),
         ('context_recall','Context recall','Gold evidence represented in retrieved text'),
         ('context_precision','Context precision','Retrieved passages are relevant'),
         ('factual_correctness','Factual correctness','Reference claims are correctly stated'),
         ('citation_coverage','Citation coverage','Answers containing at least one mapped citation'),
         ('citation_precision','Citation precision','Citations point to a target section')]
for metric,label,desc in metrics:
    cells=[]
    for s in ('system_a','system_b'):
        vs=values(s,metric,set(questions))
        cells.append((f'{statistics.mean(vs):.0%}' if metric=='citation_coverage' else f'{statistics.mean(vs):.2f}')+f' (n={len(vs)})'+(' [interim]' if metric in ragas_metrics and not complete else '') if vs else 'Pending (0/97 judged)')
    c=historical_mean(metric,'overall')
    ctext=f'{c:.0%}' if metric=='citation_coverage' else f'{c:.2f}'
    lines.append(f'| {label} | {desc} | {cells[0]} | {cells[1]} | {ctext} | {sig(metric,"overall")} |')
lines+=['', '## Interpretation and provenance', '',
        '- C v1 is a historical reference generated with GPT-5.4 and judged with GPT-4o-mini. Comparisons/significance involving C are unavailable for this matched Groq experiment.',
        '- A uses archived dense contexts. B retains five archived reranked passages and supplements from the archived A dense list, up to ten. This is a cached-context replay, not a new live retrieval run across all questions.',
        '- Both B retrieval context and its answer prompt changed. This comparison cannot isolate which change caused the improvement. The benchmark was previously inspected, so it is not a held-out test.',
        '- A/B significance uses the team Wilcoxon signed-rank test and Holm correction across system pairs within each metric/group. There is one comparable pair per group here; no correction across facets is applied, matching the team procedure. Exact p-values and coverage are in table_comparisons.json.',
        '- Citation parsing reproduces the adapters: A uses [n]; B uses [n] or 【n】. Citation precision excludes unscorable answers; n is shown. This section-matching metric does not prove that each cited passage entails the claim.',
        '- RAGAS configuration for A/B: ragas 0.4.3; Groq openai/gpt-oss-120b judge; temperature 0; output cap 4096; answer relevancy strictness 3 with BAAI/bge-small-en-v1.5 local embeddings; factual correctness F1, answer + keypoints reference, low atomicity and coverage. Team abstention handling is preserved. See ragas_coverage.json for successful, N/A, failed and missing judgments by arm/metric.',
        '- Historical C values must not be treated as a common-judge comparison. No primary accuracy score is substituted for RAGAS. RAGAS means use successful judgments only; paired tests use the intersection of successful question IDs. Unequal coverage can make marginal means differ from paired-test means.',
        '- Sources: answers.jsonl, replay.py, reconstructed records.jsonl, custom_scores.jsonl, frozen reports/rq2/full_v3/records.jsonl and aggregate_scores_gpt4omini.csv, and data/benchmark_qa_pool_2015.json.', '']
(ROOT/'UPDATED_SLIDE_TABLES.md').write_text('\n'.join(lines),encoding='utf8')
print('\n'.join(lines[:20]))
