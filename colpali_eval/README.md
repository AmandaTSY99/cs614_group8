# Visual RAG (ColQwen2.5) vs text RAG 3 on split tables

Tests whether page-image retrieval fixes questions whose answer sits in a cash flow table that
`chunk_by_structure` cut into pieces (200-word limit in `split_table`).

## Setup

| | Text RAG 3 (before) | Control | Visual RAG (after) |
|---|---|---|---|
| Input | `10-K.md` | `10-K.md` | `original.htm` printed to PDF (headless Edge), pages at 150 dpi |
| Unit retrieved | top 5 chunks (`chunk_by_structure`) | same | top 3 pages |
| Retriever | `BAAI/bge-small-en-v1.5` | same | `vidore/colqwen2.5-v0.2` (multi-vector, late interaction) |
| Answer model | `openai/gpt-oss-120b` (Groq) | `qwen/qwen3.8-27b` (Groq) | `qwen/qwen3.8-27b` (Groq, reads the page images) |
| Scope | one filing (ticker + fiscal year) | same | same |

The control isolates retrieval: it and Visual RAG share the answer model, so their difference comes from page retrieval.

## Results

| Question | Expected ($M) | Text RAG 3 (gpt-oss-120b) | Control (Qwen, text chunks) | ColQwen2.5 + Qwen |
|---|---|---|---|---|
| MSFT FY2025 net change in cash | 11,927 | wrong | wrong | correct |
| MSFT FY2025 net cash used in investing | 72,599 | wrong | wrong | correct |
| NVDA FY2026 net cash used in financing | 48,474 | wrong | wrong | correct |
| NVDA FY2026 cash at end of period | 10,605 | wrong | wrong | correct |
| **Total** | | **0/4** | **0/4** | **4/4** |

Rank of the page that holds the answer (out of 137 MSFT / 113 NVDA pages):

| Question | ColPali v1.3 | ColQwen2.5 |
|---|---|---|
| MSFT net change in cash | 48 | 1 |
| MSFT investing | 22 | 1 |
| NVDA financing | 1 | 1 |
| NVDA end-of-period cash | 18 | 1 |

## Why text RAG failed

None of the 5 retrieved chunks contained the answer for any question; every text run replied
"Not found in the provided context." The MD&A narrative ("Cash from operations increased $17.6 billion...")
outranks the split table pieces, and the piece with the bottom rows repeats only the `(In millions)` header,
not the `2025 | 2024 | 2023` row, so it has neither the words nor the year the query asks for.
A whole page keeps the title, year headers and every row together.

## Caveats

- 4 hand-picked questions on 2 filings: a demonstration of the failure mode, not a benchmark.
- The retriever matters: the original ColPali v1.3 got 1/4 end to end on the same pages.
- Cost: hundreds of vectors per page (vs one per text chunk), a GPU to index (RTX 3080 Ti), and a vision model to answer.
  Indexing all ~880 filings (~100k pages) was not attempted.
- Pre-2001 filings are plain text, so their pages carry little visual structure.

## Reproduce

```
.venv/Scripts/python colpali_eval/run_eval.py      # writes results.md, results.json, pages/
.venv/Scripts/python colpali_eval/diagnose.py vidore/colqwen2.5-v0.2   # answer-page ranks
```
Needs `GROQ_API_KEY` in `.env`, CUDA PyTorch, `colpali-engine`, `pypdfium2`.
PDFs: `msedge --headless --print-to-pdf=colpali_eval/pdfs/<name>.pdf data/<ticker>/10-K/<folder>/original.htm`.
