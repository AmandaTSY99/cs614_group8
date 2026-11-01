import re
from time import perf_counter
from .retrieval import Scope

SYSTEM_PROMPT = """Answer using only the supplied filing passages. Cite the passage number, such as [2],
immediately after each supported claim. Match the company, fiscal period and line item to the question.
For a calculation, use the reported inputs even when the filing does not state the result directly.
Check the table headings, units and denominator. Show the inputs and calculation, then state the
result with its unit and direction. If a required input is missing, identify it instead of guessing.
For a multipart question, answer each supported part and say which part the passages do not establish.
If no part can be answered from the passages, reply exactly: Not found in the provided context."""


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
