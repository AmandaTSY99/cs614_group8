"""System A answer generation: retrieve once, then one LLM call over the retrieved chunks.

rag3: top-k chunks only.
rag4: same retrieval, plus the financials.csv rows for the filtered companies and years.
"""
from .financials import FINANCIALS_NOTE, lookup_financials
from .llm import DEFAULT_MODEL, chat

VARIANTS = ("rag3", "rag4")
RAG_SYSTEM = ("Answer the question using ONLY the context below. Cite the chunk ids you used, like [2]. "
              "Each chunk is labelled with its company and fiscal year. "
              "If the answer is not in the context, reply exactly: Not found in the provided context.")


def generate(question, hits, variant="rag3", pairs=None, model=DEFAULT_MODEL):
    """Answer from already-retrieved hits, so several variants can share one retrieval."""
    if variant not in VARIANTS:
        raise ValueError(f"variant must be one of {VARIANTS}, got '{variant}'")
    blocks = [f"[{n}] ({h['meta']['ticker']} FY{h['meta']['fiscal_year']} 10-K) {h['text']}"
              for n, h in enumerate(hits, 1)]
    financials = lookup_financials(pairs) if variant == "rag4" else []
    system = RAG_SYSTEM + (FINANCIALS_NOTE if variant == "rag4" else "")
    context = "\n\n".join(financials + blocks)
    answer = chat([{"role": "system", "content": system},
                   {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {question}"}], model=model)
    return {"answer": answer, "financials": financials}


def answer(index, question, variant="rag3", k=5, pairs=None, model=DEFAULT_MODEL):
    """Retrieve the top-k chunks (filtered to `pairs` of (ticker, fiscal_year)), then answer from them only."""
    hits = index.retrieve(question, k, pairs)
    return {**generate(question, hits, variant, pairs, model), "hits": hits}


def show_hits(hits, width=150):
    for n, h in enumerate(hits, 1):               # n matches the [n] citations in the answer
        print(f"[{n}] {h['score']:.3f}  {h['id']}\n       {h['text'][:width]}\n")
