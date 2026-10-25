# GROUP PROJECT
```
In this branch, a vanilla RAG pipeline is being built in `build_agent.ipynb`. The project is made reproducible by using docker containerisation to package applications / libraries. 

```

## RAG variants

All variants retrieve once (dense, cosine similarity) and make one LLM call. The vector stores are built in `build_vdb_base_RAG.ipynb` and saved in `chroma_db/`.

| Variant | Chunking | Embedding model | Chroma collection | `financials.csv` in context | LLM | Where |
|---|---|---|---|---|---|---|
| RAG 1 | Fixed word windows (150 words, 30 overlap) | `all-MiniLM-L6-v2` | `rag1_words_minilm` | No | `openai/gpt-oss-120b` (Groq) | notebook only |
| RAG 2 | Fixed word windows (150 words, 30 overlap) | `BAAI/bge-small-en-v1.5` + query prefix | `rag2_words_bge` | No | `openai/gpt-oss-120b` (Groq) | notebook only |
| RAG 3 | Document structure (Items, headings, tables) | `BAAI/bge-small-en-v1.5` + query prefix | `rag3_structure_bge` | No | `openai/gpt-oss-120b` (Groq) | notebook, System A (`rag3`) |
| RAG 4 | Document structure (same index as RAG 3) | `BAAI/bge-small-en-v1.5` + query prefix | `rag3_structure_bge` | Yes | `openai/gpt-oss-120b` (Groq) | notebook, System A (`rag4`) |
| RAG 5 | Document structure, with company and fiscal year embedded in every chunk | `BAAI/bge-small-en-v1.5` + query prefix | `rag5_structure_header_bge` | No | `openai/gpt-oss-120b` (Groq) | notebook, System A (`rag5`, **default**) |
| RAG 6 | Document structure (same index as RAG 5) | `BAAI/bge-small-en-v1.5` + query prefix | `rag5_structure_header_bge` | Yes | `openai/gpt-oss-120b` (Groq) | System A (`rag6`) |

- **`financials.csv`**: reported annual figures from SEC XBRL data (FY2009 onwards: revenue, net income, operating income, total assets and liabilities, equity, cash, operating cash flow, diluted EPS). The rows for the chosen companies and fiscal years are added to the context in code; the LLM does not decide to look them up.
- **Query prefix**: bge expects `Represent this sentence for searching relevant passages: ` in front of queries (not chunks).
- **Defaults in System A**: top-k = 10. Answers cite chunks like `[2]` and may be partial, saying which parts are not in the context.

### Running System A

From the repo root in the container (`/workspace`):

```
python -m src.system_a --query "What was NVIDIA's total revenue?" --tickers NVDA --years 2026   # RAG 5
python -m src.system_a --query "..." --tickers NVDA --years 2026 --variant rag6                # another variant
python -m src.system_a --benchmark --all-variants --limit 10                                   # compare all variants
```

`--tickers` and `--years` filter retrieval (and choose the `financials.csv` rows for RAG 4 and 6). See `python -m src.system_a --help` for all options.
