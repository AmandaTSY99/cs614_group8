import re
from time import perf_counter
from .retrieval import Scope

SYSTEM_PROMPT = ('Answer the question using ONLY the context below. Cite the chunk ids you used, like [2]. '
                 'Each chunk is labelled with its company and fiscal year. '
                 'If the answer is not in the context, reply exactly: Not found in the provided context.')


def run(retriever, query, scope=Scope(), generator=None):
    start = perf_counter()
    result = retriever.retrieve(query, scope)
    hits = result['hits']
    result.update(query=query, scope=scope.payload(),
                  answer=None, usage=None, status='retrieval_only',
                  citations={str(n): h['id'] for n, h in enumerate(hits, 1)})
    if generator is not None:
        if not hits:
            result.update(answer='Not found in the provided context.', status='no_evidence')
        else:
            context = '\n\n'.join(f"[{n}] ({h['meta']['ticker']} FY{h['meta']['fiscal_year']} 10-K) {h['text']}"
                                    for n, h in enumerate(hits, 1))
            t = perf_counter()
            result.update(generator([{'role': 'system', 'content': SYSTEM_PROMPT},
                {'role': 'user', 'content': f'Context:\n{context}\n\nQuestion: {query}'}]))
            result['timings']['generation_seconds'] = perf_counter() - t
            result['status'] = 'ok'
        cited = re.findall(r'(?:\[|【)(\d+)(?:\]|】)', result['answer'])
        result['invalid_citation_labels'] = sorted(set(cited) - result['citations'].keys())
        result['has_citations'] = bool(cited)
    result['timings']['total_seconds'] = perf_counter() - start
    return result
