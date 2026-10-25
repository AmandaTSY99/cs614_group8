"""System A answer generation: retrieve once, then one LLM call over the retrieved chunks.

rag5: RAG 3 chunks embedded with the company and fiscal year in front (contextual chunk header). Default.
rag3: structure-based chunks (Items, headings, tables) + bge-small.
rag4: same retrieval as rag3, plus the financials.csv rows for the filtered companies and years.
rag6: same retrieval as rag5, plus the financials.csv rows (RAG 5 + RAG 4's lookup).
"""
from .financials import FINANCIALS_NOTE, lookup_financials
from .llm import DEFAULT_MODEL, chat

# Each variant: the Chroma collection it searches, and whether financials.csv rows are added to the context
VARIANTS = {
    "rag5": {"collection": "rag5_structure_header_bge", "financials": False},
    "rag3": {"collection": "rag3_structure_bge", "financials": False},
    "rag4": {"collection": "rag3_structure_bge", "financials": True},
    "rag6": {"collection": "rag5_structure_header_bge", "financials": True},
}
DEFAULT_VARIANT = "rag5"
TOP_K = 10
RAG_SYSTEM = ("Answer the question using ONLY the context below. Cite the chunk ids you used, like [2]. "
              "Each chunk is labelled with its company and fiscal year. "
              "If the context answers only part of the question, answer that part and say which parts "
              "are not in the context. "
              "If none of the answer is in the context, reply exactly: Not found in the provided context.")


def generate(question, hits, variant=DEFAULT_VARIANT, pairs=None, model=DEFAULT_MODEL):
    """Answer from already-retrieved hits, so variants that share a collection can share one retrieval."""
    if variant not in VARIANTS:
        raise ValueError(f"variant must be one of {list(VARIANTS)}, got '{variant}'")
    use_financials = VARIANTS[variant]["financials"]
    blocks = [f"[{n}] ({h['meta']['ticker']} FY{h['meta']['fiscal_year']} 10-K) {h['text']}"
              for n, h in enumerate(hits, 1)]
    financials = lookup_financials(pairs) if use_financials else []
    system = RAG_SYSTEM + (FINANCIALS_NOTE if use_financials else "")
    context = "\n\n".join(financials + blocks)
    answer = chat([{"role": "system", "content": system},
                   {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {question}"}], model=model)
    return {"answer": answer, "financials": financials}


def answer(index, question, variant=DEFAULT_VARIANT, k=TOP_K, pairs=None, model=DEFAULT_MODEL):
    """Retrieve the top-k chunks (filtered to `pairs` of (ticker, fiscal_year)), then answer from them only.
    `index` must be the variant's collection (VARIANTS[variant]["collection"])."""
    hits = index.retrieve(question, k, pairs)
    return {**generate(question, hits, variant, pairs, model), "hits": hits}


def show_hits(hits, width=150):
    for n, h in enumerate(hits, 1):               # n matches the [n] citations in the answer
        print(f"[{n}] {h['score']:.3f}  {h['id']}\n       {h['text'][:width]}\n")
