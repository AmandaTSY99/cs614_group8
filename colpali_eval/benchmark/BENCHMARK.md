# Benchmark: text RAG 3 vs ColQwen2.5 visual RAG (FY2025+ filings)

**Data:** `benchmark/benchmark_qa_0.jsonl` from `feature/benchmark_set` (100 questions, made by Amanda).
**Scope:** questions whose gold evidence is all in filings from FY2025 onwards, which is **5 questions over
4 filings** (WMT FY2025, AMZN, JNJ and META FY2025). Every system searches only the gold filing(s).

| System | Retrieval | Answer model |
|---|---|---|
| Text RAG 3 | `chunk_by_structure` + `bge-small-en-v1.5`, top 5 chunks | `openai/gpt-oss-120b` |
| Control | same top 5 chunks | `qwen/qwen3.8-27b` |
| Visual RAG | `vidore/colqwen2.5-v0.2` over page images, top 3 pages | `qwen/qwen3.8-27b` (reads the images) |

Grading: `gpt-oss-120b` as judge, against the gold answer and key points (correct / partial / wrong).
Retrieval: rank of the chunk or page that contains each gold evidence quote (a table row's label and all its
numbers, or any 8-word run of a text quote).

## Results

| ID | Type | Recipe | Evidence rank: chunks (top 5 sent) | Evidence rank: pages (top 3 sent) | Text RAG 3 | Control | Visual RAG |
|---|---|---|---|---|---|---|---|
| amanda-013 | numeric | table | 32 | **1** | ✗ | ✗ | ✓ |
| amanda-048 | qualitative | text | 1, 1 | 1, 1 | ✓ | ✗* | ◐ |
| amanda-056 | qualitative | text | 1 | 1 | ✓ | ✓ | ✓ |
| amanda-090 | mixed | table + text | 65, 66 | **3, 1** | ✗ | ✗ | ✓ |
| amanda-094 | mixed | table + text | 6, 4, 4 | **1, 2, 1** | ✗ | ✗ | ✓ |
| **Total** | | | all evidence in context: **2/5** | all evidence in context: **5/5** | **2/5** | **1/5** | **4/5 (+1 partial)** |

✓ correct · ◐ partial · ✗ wrong. *The control's answer was just "[1]": a Qwen output glitch, not a retrieval miss.

## What the answers show

- **amanda-013 (Walmart net property and equipment change, $9,183M).** The balance sheet row ranked 32nd among
  chunks, so both text runs said "Not found". The visual run read both years off the balance sheet page and
  subtracted correctly.
- **amanda-090 (J&J valuation allowance +12.15%, and the highly inflationary countries).** The tax table and
  note ranked 65th and 66th as chunks; the pages ranked 3rd and 1st. Visual RAG got both parts.
- **amanda-094 (Meta tax provision increase $17,171M and the OBBBA charge).** Text retrieval found the OBBBA
  passage but the tax table piece ranked 6th, just outside the top 5. The Qwen control named OBBBA but not the
  figure; visual RAG got both.
- **amanda-048 (Amazon seasonality, qualitative).** Text RAG 3 was fully right. Visual RAG found the right page
  but said accounts payable *declines* at year end (the gold answer says it rises), so a misreading by the
  vision model, not a retrieval miss.
- **amanda-056 (Walmart comparable sales drivers).** Everyone got it.

## Takeaways

1. **The gap is on table questions.** All three questions that need table rows failed under text RAG 3 because
   the rows were not retrieved (ranks 32, 65–66, 6). Visual RAG put every piece of gold evidence in its top 3
   pages and answered all three.
2. **On text-only questions, text RAG 3 is as good or better.** It answered both; visual RAG answered one fully
   and misread one detail.
3. **Same model, different retrieval** (control vs visual): 1/5 vs 4/5, so the gain comes from retrieval, not
   from Qwen.
4. Consistent with the earlier tests in `../FINDINGS.md`: a routed visual tool for statement and table
   questions, text RAG for narrative ones.

## Caveats

- **Only 5 questions.** The FY2025+ filter leaves 5 of the 100; this is an indication, not a significant result.
- Visual RAG sees 3 whole pages, which hold more text than 5 chunks.
- One LLM judge (gpt-oss-120b) and one run per system at temperature 0; answers were spot-checked by hand and
  the grades match.
- Runs on the full 100 questions would need ~13,000 page images indexed (a few GPU hours) and about 1M Groq
  tokens (several days on the free tier).

## Reproduce

```
.venv/Scripts/python colpali_eval/benchmark/run_benchmark.py   # writes results.json
```

PDFs in `pdfs/` and page embeddings in `embs/` (gitignored) are built by `index_filings.py`.
