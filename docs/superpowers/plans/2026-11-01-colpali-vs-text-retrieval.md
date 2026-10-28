# Visual vs text retrieval (ColPali, ColQwen) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Evaluate ColPali v1.3 and ColQwen2.5 page-image retrieval on the 97-question Benchmark v1 against Systems A, B, C v1 and C v3, and write `reports/colpali/REPORT.md`.

**Architecture:** A new package `scripts/colpali/` adds a *visual system adapter* that emits records in exactly the schema of the existing RQ2 records (`retrieved_contexts` = page text, answer from gpt-5.4 reading page images). The existing RQ1 scorer (`scripts/rq1`, branch `feat/rq1`) and RQ2 scorer (`scripts/rq2`, branch `feat/rq2-full-eval`) then score vision and text systems identically. A small `compare.py` merges everything into tables and figures. Text-system results are reused, never re-run.

**Tech Stack:** Python, `colpali-engine`, PyTorch (CUDA, RTX 3080 Ti 16 GB), `pypdfium2`, headless Edge (HTML to PDF), OpenAI API (gpt-5.4 answers, gpt-4o-mini judge), RAGAS 0.4.3 (via the repo's `scripts/rq2/score.py`), pytest, matplotlib.

## Global Constraints

- Benchmark: `data/benchmark_qa_pool_2015.json` (97 questions, ids `gold-001`..`gold-097`, FY2015+ filings, about 81 gold filings).
- Text systems are reused as published from `reports/rq2/full_v3/records.jsonl` (systems `system_a`, `system_b`, `system_c_v1`, `system_c_v3`); scores from `reports/rq2/full_v3/scores_gpt4omini.jsonl`.
- Vision retrievers: `vidore/colpali-v1.3` and `vidore/colqwen2.5-v0.2`. Pages rendered at 150 dpi from `original.htm` printed to PDF with headless Edge.
- Retrieval protocol: search only the gold filing(s) of each question; top-3 pages per filing go to the answer model (images total capped at 12).
- Answer model gpt-5.4, call parameters mirror the text systems: `temperature=0`, `max_completion_tokens=1500`, `reasoning_effort="low"`. Judge: `openai/gpt-4o-mini`, temperature 0; factual correctness mode `recall`, reference `answer_keypoints`, atomicity `low`. All cells use bootstrap 95% CIs.
- RQ1 metric definitions come from `scripts/rq1/score.py` unchanged (recall@5, recall@10, recall@all, complete@k, MRR-style average precision); additionally recall at an equal context size in words.
- Never read or print `.env`. API keys load via `python-dotenv` from the path in env var `DOTENV_PATH` (default `<repo>/.env`).
- All work happens in the git worktree `C:/Users/UserAdmin/Desktop/cs614_group8_eval` on branch `eval/colpali-v3`; `main` and its untracked `colpali_eval/` files stay untouched.
- Commands run from the worktree root with the main repo's interpreter: `PY=C:/Users/UserAdmin/Desktop/cs614_group8/.venv/Scripts/python` and `python -m scripts.colpali.<module>`.

## File Structure

| File | Responsibility |
|---|---|
| `scripts/colpali/__init__.py` | package marker |
| `scripts/colpali/config.py` | paths, model registry, constants |
| `scripts/colpali/filings.py` | benchmark loading, gold filing manifest, filing HTML paths |
| `scripts/colpali/pages.py` | HTML to PDF, page text, page images |
| `scripts/colpali/retrieve.py` | pure ranking helpers + `VisualRetriever` (model wrapper) |
| `scripts/colpali/index_filings.py` | resumable PDF printing and page embedding, with timing log |
| `scripts/colpali/ceiling.py` | gate: how many gold quotes appear in any page text of their filing |
| `scripts/colpali/generate.py` | record builder, gpt-5.4 vision answers, resumable run |
| `scripts/colpali/score_rq1.py` | RQ1 scoring of vision + text records into one CSV |
| `scripts/colpali/compare.py` | bootstrap tables, per-recipe breakdown, equal-budget recall, cost, figures, case list |
| `tests/colpali/` | unit tests for the pure logic |
| `reports/colpali/REPORT.md` | final report |

---

### Task 0: Worktree, branches and environments

**Files:**
- Create: worktree `../cs614_group8_eval`, `colpali_eval/v3/` (artifact dir, gitignored)

**Interfaces:**
- Produces: a worktree where `scripts/rq1`, `scripts/rq2`, `reports/rq2/full_v3` and `data/benchmark_qa_pool_2015.json` all exist; two working interpreters (`.venv` for GPU/OpenAI, conda `cs614-eval` for RAGAS).

- [ ] **Step 1: Create the worktree from the branch that holds C v3 results**

```bash
cd /c/Users/UserAdmin/Desktop/cs614_group8
git fetch origin
git worktree add ../cs614_group8_eval -b eval/colpali-v3 origin/feat/rq2-full-eval
cd ../cs614_group8_eval
git checkout origin/feat/rq1 -- scripts/rq1
ls scripts/rq1 scripts/rq2 reports/rq2/full_v3 data/benchmark_qa_pool_2015.json
```

Expected: `scripts/rq1/{common,matching,score}.py`, `scripts/rq2/{score,generate,adapters}.py`, `records.jsonl` and `scores_gpt4omini.jsonl` listed.

- [ ] **Step 2: Check the filing HTML is in the worktree**

```bash
ls data/JNJ/10-K/FY2022_2023-01-01/original.htm
```

Expected: the file exists. If `data/` is missing `original.htm` files, stop and ask the user where the HTML lives (the main repo has it); do not copy anything until told.

- [ ] **Step 3: Seed artifacts from the earlier run (same renderer, same ColQwen2.5 model)**

```bash
mkdir -p colpali_eval/v3/pdfs colpali_eval/v3/embs/colqwen2_5
cp /c/Users/UserAdmin/Desktop/cs614_group8/colpali_eval/benchmark/pdfs/*.pdf colpali_eval/v3/pdfs/
cp /c/Users/UserAdmin/Desktop/cs614_group8/colpali_eval/benchmark/embs/*.pt colpali_eval/v3/embs/colqwen2_5/
printf "colpali_eval/v3/\n" >> .git/info/exclude 2>/dev/null || printf "colpali_eval/v3/\n" >> "$(git rev-parse --git-dir)/info/exclude"
ls colpali_eval/v3/pdfs | wc -l
```

Expected: about 99 PDFs copied (only those matching the 97-question filings are used).

- [ ] **Step 4: Install missing packages into the GPU venv and verify CUDA**

```bash
PY=C:/Users/UserAdmin/Desktop/cs614_group8/.venv/Scripts/python
$PY -m pip install openai matplotlib python-dotenv
$PY -c "import torch, colpali_engine, pypdfium2; print('cuda', torch.cuda.is_available(), torch.cuda.get_device_name(0))"
$PY -c "from src.system_a.evaluate import score_answer; print('evaluate import ok')"
```

Expected: `cuda True NVIDIA GeForce RTX 3080 Ti Laptop GPU` and `evaluate import ok`. If the last import fails, `pip install` the missing module it names.

- [ ] **Step 5: Create the RAGAS env documented in `requirements-eval.txt`**

```bash
conda create -n cs614-eval --clone cs614 -y
conda run -n cs614-eval pip install -r requirements-eval.txt
conda run -n cs614-eval python -c "import ragas; print(ragas.__version__)"
```

Expected: `0.4.3`.

- [ ] **Step 6: Ask the user to confirm the OpenAI key is set**

Do not read `.env`. Ask: "Is `OPENAI_API_KEY` set in your `.env`, and does it have gpt-5.4 with image input?" Then set `export DOTENV_PATH=C:/Users/UserAdmin/Desktop/cs614_group8/.env` for later steps. Proceed only after the user confirms.

- [ ] **Step 7: Commit (worktree branch)**

```bash
git add scripts/rq1
git commit -m "chore: bring RQ1 scorer from feat/rq1 into eval branch"
```

---

### Task 1: Config and filing manifest

**Files:**
- Create: `scripts/colpali/__init__.py` (empty), `scripts/colpali/config.py`, `scripts/colpali/filings.py`
- Test: `tests/colpali/__init__.py` (empty), `tests/colpali/test_filings.py`

**Interfaces:**
- Produces (`config.py`): `REPO_ROOT`, `BENCHMARK_PATH`, `DATA_ROOT`, `ARTIFACTS`, `PDF_DIR`, `OUT_ROOT`, `EDGE`, `RENDER_DPI=150`, `BATCH_PAGES=4`, `MAX_IMAGES=12`, `PAGES_PER_FILING=3`, `RANKED_KEPT=10`, `ModelSpec(hf_id, model_cls, processor_cls)`, `MODELS: dict[str, ModelSpec]`, `emb_dir(model_key) -> Path`, `load_env() -> None`.
- Produces (`filings.py`): `load_questions(path=BENCHMARK_PATH) -> list[dict]`, `gold_doc_ids(questions) -> list[str]`, `question_doc_ids(q) -> list[str]`, `doc_html_path(doc_id) -> Path`, `fiscal_year(doc_id) -> int`, `ticker(doc_id) -> str`.

- [ ] **Step 1: Write the failing tests**

```python
# tests/colpali/test_filings.py
from scripts.colpali.filings import (doc_html_path, fiscal_year, gold_doc_ids, load_questions,
                                     question_doc_ids, ticker)


def test_benchmark_has_97_questions_with_gold_evidence():
    questions = load_questions()
    assert len(questions) == 97
    assert all(q["gold_evidence"] for q in questions)


def test_every_gold_doc_resolves_to_filing_html():
    missing = [d for d in gold_doc_ids(load_questions()) if not doc_html_path(d).exists()]
    assert missing == []


def test_doc_id_parsing():
    assert fiscal_year("JNJ_FY2022_2023-01-01") == 2022
    assert ticker("JNJ_FY2022_2023-01-01") == "JNJ"
    assert doc_html_path("JNJ_FY2022_2023-01-01").parts[-4:] == ("JNJ", "10-K", "FY2022_2023-01-01", "original.htm")


def test_question_doc_ids_sorted_unique():
    q = {"gold_evidence": [{"doc_id": "B_FY2020_x"}, {"doc_id": "A_FY2020_x"}, {"doc_id": "B_FY2020_x"}]}
    assert question_doc_ids(q) == ["A_FY2020_x", "B_FY2020_x"]
```

- [ ] **Step 2: Run to verify failure**

Run: `$PY -m pytest tests/colpali/test_filings.py -v`
Expected: FAIL with `ModuleNotFoundError: scripts.colpali`.

- [ ] **Step 3: Implement**

```python
# scripts/colpali/config.py
"""Paths, constants and the retriever registry for the visual vs text retrieval evaluation."""
import os
from dataclasses import dataclass
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
BENCHMARK_PATH = REPO_ROOT / "data" / "benchmark_qa_pool_2015.json"
DATA_ROOT = REPO_ROOT / "data"
ARTIFACTS = REPO_ROOT / "colpali_eval" / "v3"
PDF_DIR = ARTIFACTS / "pdfs"
OUT_ROOT = REPO_ROOT / "reports" / "colpali"
TEXT_RUN = REPO_ROOT / "reports" / "rq2" / "full_v3"
TEXT_SCORES_FILE = "scores_gpt4omini.jsonl"
EDGE = os.environ.get("EDGE_PATH", r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe")

RENDER_DPI = 150
BATCH_PAGES = 4
MAX_IMAGES = 12
PAGES_PER_FILING = 3
RANKED_KEPT = 10

# Derived from the text systems' records: 5,405 prompt + 376 completion tokens cost $0.0191525.
PRICE_IN_PER_TOKEN = 2.5e-6
PRICE_OUT_PER_TOKEN = 15e-6


@dataclass(frozen=True)
class ModelSpec:
    hf_id: str
    model_cls: str
    processor_cls: str


MODELS = {
    "colqwen2_5": ModelSpec("vidore/colqwen2.5-v0.2", "ColQwen2_5", "ColQwen2_5_Processor"),
    "colpali_v1_3": ModelSpec("vidore/colpali-v1.3", "ColPali", "ColPaliProcessor"),
}


def emb_dir(model_key: str) -> Path:
    return ARTIFACTS / "embs" / model_key


def load_env() -> None:
    """Load API keys from DOTENV_PATH (default <repo>/.env). Never prints values."""
    from dotenv import load_dotenv
    load_dotenv(os.environ.get("DOTENV_PATH", str(REPO_ROOT / ".env")))
```

```python
# scripts/colpali/filings.py
"""Benchmark questions and the filings their gold evidence lives in."""
import json
from pathlib import Path
from typing import Any, Dict, List

from scripts.colpali.config import BENCHMARK_PATH, DATA_ROOT


def load_questions(path: Path = BENCHMARK_PATH) -> List[Dict[str, Any]]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def question_doc_ids(q: Dict[str, Any]) -> List[str]:
    return sorted({e["doc_id"] for e in q["gold_evidence"]})


def gold_doc_ids(questions: List[Dict[str, Any]]) -> List[str]:
    return sorted({d for q in questions for d in question_doc_ids(q)})


def ticker(doc_id: str) -> str:
    return doc_id.split("_", 1)[0]


def fiscal_year(doc_id: str) -> int:
    return int(doc_id.split("_")[1].removeprefix("FY"))


def doc_html_path(doc_id: str) -> Path:
    folder = doc_id.split("_", 1)[1]
    return DATA_ROOT / ticker(doc_id) / "10-K" / folder / "original.htm"
```

- [ ] **Step 4: Run to verify pass**

Run: `$PY -m pytest tests/colpali/test_filings.py -v`
Expected: 4 passed. If `test_every_gold_doc_resolves_to_filing_html` fails, list the missing filings for the user (they may be absent from the worktree's `data/`).

- [ ] **Step 5: Print the real manifest size (record it for the report)**

Run: `$PY -c "from scripts.colpali.filings import *; q=load_questions(); print(len(q), len(gold_doc_ids(q)), max(len(question_doc_ids(x)) for x in q))"`
Expected: `97 <about 81> <max filings per question>`.

- [ ] **Step 6: Commit**

```bash
git add scripts/colpali tests/colpali
git commit -m "feat(colpali): config and gold filing manifest"
```

---

### Task 2: Page text and page images

**Files:**
- Create: `scripts/colpali/pages.py`
- Test: `tests/colpali/test_pages.py`

**Interfaces:**
- Consumes: `config.EDGE`, `config.RENDER_DPI`, `config.PDF_DIR`, `filings.doc_html_path`.
- Produces: `pdf_path(doc_id) -> Path`, `print_pdf(doc_id) -> Path` (skips if exists, raises if Edge produced no file), `page_texts(pdf: Path) -> list[str]`, `render_page(pdf: Path, index: int) -> PIL.Image.Image`, `render_pages(pdf: Path) -> list[Image]`, `image_data_url(img) -> str`.

- [ ] **Step 1: Write the failing test (uses the first available PDF)**

```python
# tests/colpali/test_pages.py
import pytest

from scripts.colpali.config import PDF_DIR
from scripts.colpali.pages import image_data_url, page_texts, render_page


def _first_pdf():
    pdfs = sorted(PDF_DIR.glob("*.pdf"))
    if not pdfs:
        pytest.skip("no PDFs printed yet")
    return pdfs[0]


def test_page_texts_returns_one_string_per_page():
    texts = page_texts(_first_pdf())
    assert len(texts) > 10
    assert all(isinstance(t, str) for t in texts)
    assert any(len(t) > 200 for t in texts)


def test_render_page_is_150dpi_letter_sized_and_encodes_to_jpeg_data_url():
    img = render_page(_first_pdf(), 0)
    assert 1100 < img.width < 1400 and 1500 < img.height < 1800
    assert image_data_url(img).startswith("data:image/jpeg;base64,")
```

- [ ] **Step 2: Run to verify failure**

Run: `$PY -m pytest tests/colpali/test_pages.py -v`
Expected: FAIL (`ModuleNotFoundError: scripts.colpali.pages`).

- [ ] **Step 3: Implement**

```python
# scripts/colpali/pages.py
"""Filing HTML -> PDF (headless Edge) -> page text and page images (pypdfium2)."""
import base64
import io
import subprocess
from pathlib import Path
from typing import List

import pypdfium2 as pdfium
from PIL import Image

from scripts.colpali.config import EDGE, PDF_DIR, RENDER_DPI
from scripts.colpali.filings import doc_html_path


def pdf_path(doc_id: str) -> Path:
    return PDF_DIR / f"{doc_id}.pdf"


def print_pdf(doc_id: str) -> Path:
    out = pdf_path(doc_id)
    if out.exists() and out.stat().st_size > 0:
        return out
    PDF_DIR.mkdir(parents=True, exist_ok=True)
    subprocess.run([EDGE, "--headless", "--disable-gpu", "--no-pdf-header-footer",
                    f"--print-to-pdf={out}", doc_html_path(doc_id).as_uri()],
                   capture_output=True, timeout=600)
    if not out.exists() or out.stat().st_size == 0:
        raise RuntimeError(f"Edge produced no PDF for {doc_id}; check EDGE_PATH ({EDGE})")
    return out


def page_texts(pdf: Path) -> List[str]:
    doc = pdfium.PdfDocument(str(pdf))
    try:
        return [doc[i].get_textpage().get_text_range() for i in range(len(doc))]
    finally:
        doc.close()


def render_page(pdf: Path, index: int) -> Image.Image:
    doc = pdfium.PdfDocument(str(pdf))
    try:
        return doc[index].render(scale=RENDER_DPI / 72).to_pil().convert("RGB")
    finally:
        doc.close()


def render_pages(pdf: Path) -> List[Image.Image]:
    doc = pdfium.PdfDocument(str(pdf))
    try:
        return [doc[i].render(scale=RENDER_DPI / 72).to_pil().convert("RGB") for i in range(len(doc))]
    finally:
        doc.close()


def image_data_url(img: Image.Image, quality: int = 85) -> str:
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=quality)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode("ascii")
```

- [ ] **Step 4: Run to verify pass**

Run: `$PY -m pytest tests/colpali/test_pages.py -v`
Expected: 2 passed (letter page at 150 dpi is about 1275 x 1650).

- [ ] **Step 5: Commit**

```bash
git add scripts/colpali/pages.py tests/colpali/test_pages.py
git commit -m "feat(colpali): page text and image helpers"
```

---

### Task 3: Ranking helpers and visual retriever

**Files:**
- Create: `scripts/colpali/retrieve.py`
- Test: `tests/colpali/test_retrieve.py`

**Interfaces:**
- Consumes: `config.MODELS`, `config.BATCH_PAGES`, `config.MAX_IMAGES`, `config.PAGES_PER_FILING`.
- Produces: `PageHit(score: float, doc_id: str, page: int)` (frozen dataclass, `page` 0-based), `rank_pages(scores_by_doc: dict[str, Sequence[float]]) -> list[PageHit]`, `pages_per_filing(n_docs: int) -> int`, `pages_to_send(ranked, per_filing) -> list[PageHit]`, `load_model(model_key) -> (model, processor)`, `VisualRetriever(model_key)` with `.embed_pages(images) -> list[Tensor]`, `.embed_query(text) -> list[Tensor]`, `.score_doc(query_vecs, page_embs) -> list[float]`.

- [ ] **Step 1: Write the failing tests**

```python
# tests/colpali/test_retrieve.py
from scripts.colpali.retrieve import PageHit, pages_per_filing, pages_to_send, rank_pages


def ids(hits):
    return [(h.doc_id, h.page) for h in hits]


def test_rank_pages_merges_filings_by_score_and_breaks_ties_deterministically():
    ranked = rank_pages({"A": [0.1, 0.9], "B": [0.5, 0.5]})
    assert ids(ranked) == [("A", 1), ("B", 0), ("B", 1), ("A", 0)]
    assert isinstance(ranked[0], PageHit)


def test_pages_to_send_takes_top_n_per_filing_in_rank_order():
    ranked = rank_pages({"A": [0.9, 0.8, 0.7], "B": [0.85, 0.6]})
    assert ids(pages_to_send(ranked, 2)) == [("A", 0), ("B", 0), ("A", 1), ("B", 1)]


def test_pages_per_filing_caps_total_images_at_12():
    assert pages_per_filing(1) == 3
    assert pages_per_filing(4) == 3
    assert pages_per_filing(5) == 2
    assert pages_per_filing(13) == 1
```

- [ ] **Step 2: Run to verify failure**

Run: `$PY -m pytest tests/colpali/test_retrieve.py -v`
Expected: FAIL (`ModuleNotFoundError`/`ImportError`).

- [ ] **Step 3: Implement**

```python
# scripts/colpali/retrieve.py
"""Page ranking for multi-vector (late-interaction) visual retrievers."""
from dataclasses import dataclass
from typing import Dict, List, Sequence

from scripts.colpali.config import BATCH_PAGES, MAX_IMAGES, MODELS, PAGES_PER_FILING


@dataclass(frozen=True)
class PageHit:
    score: float
    doc_id: str
    page: int  # 0-based


def rank_pages(scores_by_doc: Dict[str, Sequence[float]]) -> List[PageHit]:
    hits = [PageHit(float(s), d, i) for d, scores in scores_by_doc.items() for i, s in enumerate(scores)]
    return sorted(hits, key=lambda h: (-h.score, h.doc_id, h.page))


def pages_per_filing(n_docs: int) -> int:
    return max(1, min(PAGES_PER_FILING, MAX_IMAGES // n_docs))


def pages_to_send(ranked: List[PageHit], per_filing: int) -> List[PageHit]:
    taken: Dict[str, int] = {}
    sent = []
    for hit in ranked:
        if taken.get(hit.doc_id, 0) < per_filing:
            sent.append(hit)
            taken[hit.doc_id] = taken.get(hit.doc_id, 0) + 1
    return sent


def load_model(model_key: str):
    import torch
    from colpali_engine import models as cm

    spec = MODELS[model_key]
    model = getattr(cm, spec.model_cls).from_pretrained(
        spec.hf_id, torch_dtype=torch.bfloat16, device_map="cuda").eval()
    processor = getattr(cm, spec.processor_cls).from_pretrained(spec.hf_id)
    return model, processor


class VisualRetriever:
    def __init__(self, model_key: str):
        self.model_key = model_key
        self.model, self.processor = load_model(model_key)

    def embed_pages(self, images) -> list:
        import torch
        out = []
        for start in range(0, len(images), BATCH_PAGES):
            batch = self.processor.process_images(images[start:start + BATCH_PAGES]).to(self.model.device)
            with torch.no_grad():
                out.extend(torch.unbind(self.model(**batch).to("cpu")))
        return out

    def embed_query(self, text: str) -> list:
        import torch
        batch = self.processor.process_queries([text]).to(self.model.device)
        with torch.no_grad():
            return list(torch.unbind(self.model(**batch).to("cpu")))

    def score_doc(self, query_vecs: list, page_embs: list) -> List[float]:
        return [float(s) for s in self.processor.score_multi_vector(query_vecs, page_embs)[0]]
```

- [ ] **Step 4: Run to verify pass**

Run: `$PY -m pytest tests/colpali/test_retrieve.py -v`
Expected: 3 passed.

- [ ] **Step 5: Commit**

```bash
git add scripts/colpali/retrieve.py tests/colpali/test_retrieve.py
git commit -m "feat(colpali): page ranking helpers and visual retriever"
```

---

### Task 4: Indexer (PDF printing and page embeddings)

**Files:**
- Create: `scripts/colpali/index_filings.py`

**Interfaces:**
- Consumes: `filings.load_questions/gold_doc_ids`, `pages.print_pdf/render_pages`, `retrieve.VisualRetriever`, `config.emb_dir/ARTIFACTS`.
- Produces: `load_page_embs(model_key, doc_id) -> list[Tensor]`; embedding files `colpali_eval/v3/embs/<model_key>/<doc_id>.pt`; timing log `colpali_eval/v3/embs/<model_key>/index_log.jsonl` with one line `{"doc_id","pages","seconds"}` per newly embedded filing.

- [ ] **Step 1: Implement**

```python
# scripts/colpali/index_filings.py
"""Print gold filings to PDF and cache page embeddings. Resumable: existing PDFs and .pt files are skipped.

Usage: python -m scripts.colpali.index_filings --model colqwen2_5 [--pdfs-only] [--limit-docs N]
"""
import argparse
import json
import time
from typing import List

import torch

from scripts.colpali.config import emb_dir
from scripts.colpali.filings import gold_doc_ids, load_questions
from scripts.colpali.pages import pdf_path, print_pdf, render_pages
from scripts.colpali.retrieve import VisualRetriever


def load_page_embs(model_key: str, doc_id: str) -> List[torch.Tensor]:
    return torch.load(emb_dir(model_key) / f"{doc_id}.pt", weights_only=True)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", required=True, choices=["colqwen2_5", "colpali_v1_3"])
    ap.add_argument("--pdfs-only", action="store_true")
    ap.add_argument("--limit-docs", type=int, default=None)
    args = ap.parse_args()

    doc_ids = gold_doc_ids(load_questions())[: args.limit_docs]
    for n, doc_id in enumerate(doc_ids, 1):
        print_pdf(doc_id)
        print(f"[pdf {n}/{len(doc_ids)}] {doc_id}", flush=True)
    if args.pdfs_only:
        return

    out_dir = emb_dir(args.model)
    out_dir.mkdir(parents=True, exist_ok=True)
    retriever = VisualRetriever(args.model)
    for n, doc_id in enumerate(doc_ids, 1):
        out = out_dir / f"{doc_id}.pt"
        if out.exists():
            continue
        t0 = time.perf_counter()
        embs = retriever.embed_pages(render_pages(pdf_path(doc_id)))
        torch.save(embs, out)
        seconds = round(time.perf_counter() - t0, 1)
        with (out_dir / "index_log.jsonl").open("a", encoding="utf-8") as fh:
            fh.write(json.dumps({"doc_id": doc_id, "pages": len(embs), "seconds": seconds}) + "\n")
        print(f"[emb {n}/{len(doc_ids)}] {doc_id}: {len(embs)} pages in {seconds}s", flush=True)


if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Print any missing PDFs (CPU only, safe to run now)**

Run: `$PY -m scripts.colpali.index_filings --model colqwen2_5 --pdfs-only`
Expected: one `[pdf n/N]` line per filing, no exception. Edge can take a minute per large filing.

- [ ] **Step 3: Smoke-embed two filings with ColQwen2.5**

Run: `$PY -m scripts.colpali.index_filings --model colqwen2_5 --limit-docs 2`
Expected: embeds only those of the first two filings that are not already cached; a `.pt` exists for each. Check `nvidia-smi` shows memory use under 16 GB.

- [ ] **Step 4: Full indexing in the background (hours)**

```bash
$PY -m scripts.colpali.index_filings --model colqwen2_5 > colpali_eval/v3/index_colqwen.log 2>&1
$PY -m scripts.colpali.index_filings --model colpali_v1_3 > colpali_eval/v3/index_colpali.log 2>&1
```

Run both with `run_in_background`, one after the other (one model on the GPU at a time). Expected: every gold filing has a `.pt` per model. Verify: `ls colpali_eval/v3/embs/colqwen2_5/*.pt | wc -l` equals the filing count from Task 1.

- [ ] **Step 5: Commit**

```bash
git add scripts/colpali/index_filings.py
git commit -m "feat(colpali): resumable filing indexer"
```

---

### Task 5: Evidence-ceiling gate

**Files:**
- Create: `scripts/colpali/ceiling.py`
- Test: `tests/colpali/test_ceiling.py`

**Interfaces:**
- Consumes: `scripts.rq1.matching.evidence_in_contexts`, `pages.page_texts/pdf_path`, `filings.*`.
- Produces: `evidence_ceiling(questions, texts_by_doc) -> (found, total, misses)` where `texts_by_doc: dict[str, list[str]]` and `misses` is a list of `(question_id, doc_id, quote_prefix)`; CLI writes `reports/colpali/ceiling.json`.

This checks the PDF text layer is good enough for the RQ1 lexical matcher: if the gold quote cannot be found in any page of its own filing, no retriever could score it.

- [ ] **Step 1: Write the failing test**

```python
# tests/colpali/test_ceiling.py
from scripts.colpali.ceiling import evidence_ceiling


def test_ceiling_counts_gold_quotes_found_in_any_page_of_their_filing():
    questions = [{"id": "q1", "gold_evidence": [
        {"doc_id": "A_FY2020_x", "kind": "text", "quote": "Net cash used in financing activities was 48,474 million dollars"},
        {"doc_id": "A_FY2020_x", "kind": "text", "quote": "A sentence that appears on no page of this filing at all"},
    ]}]
    texts = {"A_FY2020_x": ["cover page", "Net cash used in financing activities was 48,474 million dollars for the year"]}
    found, total, misses = evidence_ceiling(questions, texts)
    assert (found, total) == (1, 2)
    assert misses == [("q1", "A_FY2020_x", "A sentence that appears on no page of this")]
```

- [ ] **Step 2: Run to verify failure**

Run: `$PY -m pytest tests/colpali/test_ceiling.py -v`
Expected: FAIL (`ModuleNotFoundError: scripts.colpali.ceiling`).

- [ ] **Step 3: Implement**

```python
# scripts/colpali/ceiling.py
"""Gate: share of gold evidence quotes found in some page text of their own filing."""
import json
from typing import Any, Dict, List, Tuple

from scripts.colpali.config import OUT_ROOT
from scripts.colpali.filings import gold_doc_ids, load_questions
from scripts.colpali.pages import page_texts, pdf_path
from scripts.rq1.matching import evidence_in_contexts


def evidence_ceiling(questions: List[Dict[str, Any]], texts_by_doc: Dict[str, List[str]]
                     ) -> Tuple[int, int, List[Tuple[str, str, str]]]:
    found, total, misses = 0, 0, []
    for q in questions:
        for ev in q["gold_evidence"]:
            total += 1
            if evidence_in_contexts(ev, texts_by_doc[ev["doc_id"]]):
                found += 1
            else:
                misses.append((q["id"], ev["doc_id"], ev["quote"][:50]))
    return found, total, misses


def main() -> None:
    questions = load_questions()
    texts = {d: page_texts(pdf_path(d)) for d in gold_doc_ids(questions)}
    found, total, misses = evidence_ceiling(questions, texts)
    OUT_ROOT.mkdir(parents=True, exist_ok=True)
    (OUT_ROOT / "ceiling.json").write_text(
        json.dumps({"found": found, "total": total, "share": found / total, "misses": misses}, indent=2),
        encoding="utf-8")
    print(f"gold evidence found in its filing's page text: {found}/{total} = {found / total:.1%}")
    if found / total < 0.90:
        raise SystemExit("Ceiling below 90%: inspect ceiling.json misses before trusting page-level RQ1 scores")


if __name__ == "__main__":
    main()
```

- [ ] **Step 4: Run test, then the real gate**

Run: `$PY -m pytest tests/colpali/test_ceiling.py -v` (expect PASS), then `$PY -m scripts.colpali.ceiling`.
Expected: a share of 90% or more. If lower, open `reports/colpali/ceiling.json`, check whether misses are tables whose PDF text puts cells on separate lines, and report it to the user before continuing (do not loosen the matcher silently).

- [ ] **Step 5: Commit**

```bash
git add scripts/colpali/ceiling.py tests/colpali/test_ceiling.py
git commit -m "feat(colpali): gold-evidence ceiling gate for page text"
```

---

### Task 6: Visual system generation (retrieval + gpt-5.4 vision answers)

**Files:**
- Create: `scripts/colpali/generate.py`
- Test: `tests/colpali/test_generate.py`

**Interfaces:**
- Consumes: `retrieve.*`, `index_filings.load_page_embs`, `pages.*`, `filings.*`, `config.*`, `src.system_a.evaluate.score_answer`.
- Produces: `build_record(system, q, ranked, sent, texts_by_doc, answer, usage, latency_ms, model, run_id) -> dict` (pure); run output `reports/colpali/vision_run/records.jsonl` (one line per system and question; fields below); `gen_errors.jsonl` for failures. Record keys: all keys of the RQ2 records (`system, question_id, query_id, category, recipe, hop, type, question, ground_truth_answer, answer, prediction, retrieved_contexts, contexts_meta, citations, guardrail_report, hops, tokens, cost_usd, latency_ms, model, provider, run_id, status, timestamp, numeric_correct, keypoint_recall`) plus `ranked_contexts`, `ranked_meta` (top 10 pages, for RQ1) and `sent_pages` (labels).

- [ ] **Step 1: Write the failing test**

```python
# tests/colpali/test_generate.py
from scripts.colpali.generate import build_record
from scripts.colpali.retrieve import PageHit


def test_build_record_matches_rq2_schema_and_separates_sent_from_ranked_pages():
    q = {"id": "gold-001", "type": "numeric", "question": "What was the change?", "answer": "-25.64%",
         "key_points": [], "recipe": "table", "hop": "single",
         "gold_evidence": [{"doc_id": "JNJ_FY2022_2023-01-01", "ticker": "JNJ", "year": 2022}]}
    doc = "JNJ_FY2022_2023-01-01"
    texts = {doc: [f"page {i} text" for i in range(20)]}
    ranked = [PageHit(1.0 - i / 100, doc, i) for i in range(20)]
    sent = ranked[:3]
    rec = build_record("colqwen2_5", q, ranked, sent, texts, "It fell 25.64% [1].",
                       {"prompt": 6000, "completion": 100}, 4200.0, "gpt-5.4", "run1")
    assert rec["system"] == "colqwen2_5" and rec["question_id"] == "gold-001" and rec["query_id"] == "gold-001"
    assert rec["retrieved_contexts"] == ["page 0 text", "page 1 text", "page 2 text"]
    assert len(rec["ranked_contexts"]) == 10
    assert rec["contexts_meta"][0] == {"chunk_id": f"{doc}#p1", "ticker": "JNJ", "fiscal_year": 2022, "section": "page 1"}
    assert rec["citations"] == [] and rec["guardrail_report"] is None and rec["hops"] == 1
    assert rec["tokens"] == {"prompt": 6000, "completion": 100, "total": 6100}
    assert abs(rec["cost_usd"] - (6000 * 2.5e-6 + 100 * 15e-6)) < 1e-9
    assert rec["status"] == "ok" and rec["numeric_correct"] is not None and rec["keypoint_recall"] is None
```

- [ ] **Step 2: Run to verify failure**

Run: `$PY -m pytest tests/colpali/test_generate.py -v`
Expected: FAIL (`ModuleNotFoundError: scripts.colpali.generate`).

- [ ] **Step 3: Implement**

```python
# scripts/colpali/generate.py
"""Run a visual retriever over the benchmark and answer with gpt-5.4 reading the retrieved page images.

Resumable per (system, question_id). Usage:
    python -m scripts.colpali.generate --model colqwen2_5 [--limit N] [--run-id vision_run]
"""
import argparse
import json
import os
import time
from datetime import datetime, timezone
from typing import Any, Dict, List

from scripts.colpali.config import (OUT_ROOT, PRICE_IN_PER_TOKEN, PRICE_OUT_PER_TOKEN, RANKED_KEPT,
                                    emb_dir, load_env)
from scripts.colpali.filings import fiscal_year, gold_doc_ids, load_questions, question_doc_ids, ticker
from scripts.colpali.pages import image_data_url, page_texts, pdf_path, render_page
from scripts.colpali.retrieve import PageHit, pages_per_filing, pages_to_send, rank_pages
from src.system_a.evaluate import score_answer

SYSTEM_PROMPT = (
    "Answer the question using ONLY the filing pages shown. Cite the page numbers you used, like [2]. "
    "Read table rows and column headers carefully and give figures with their units and fiscal year. "
    "If the pages do not contain the answer, reply exactly: Not found in the provided context."
)


def _meta(hit: PageHit) -> Dict[str, Any]:
    return {"chunk_id": f"{hit.doc_id}#p{hit.page + 1}", "ticker": ticker(hit.doc_id),
            "fiscal_year": fiscal_year(hit.doc_id), "section": f"page {hit.page + 1}"}


def build_record(system: str, q: Dict[str, Any], ranked: List[PageHit], sent: List[PageHit],
                 texts_by_doc: Dict[str, List[str]], answer: str, usage: Dict[str, int],
                 latency_ms: float, model: str, run_id: str) -> Dict[str, Any]:
    scores = score_answer(q, answer)
    top = ranked[:RANKED_KEPT]
    total = usage["prompt"] + usage["completion"]
    return {
        "status": "ok", "run_id": run_id, "system": system, "question_id": q["id"], "query_id": q["id"],
        "category": q.get("category"), "recipe": q.get("recipe"), "hop": q.get("hop"), "type": q.get("type"),
        "question": q["question"], "ground_truth_answer": q["answer"],
        "answer": answer, "prediction": answer,
        "retrieved_contexts": [texts_by_doc[h.doc_id][h.page] for h in sent],
        "contexts_meta": [_meta(h) for h in sent],
        "ranked_contexts": [texts_by_doc[h.doc_id][h.page] for h in top],
        "ranked_meta": [_meta(h) for h in top],
        "sent_pages": [f"{h.doc_id} p.{h.page + 1}" for h in sent],
        "citations": [], "guardrail_report": None, "hops": 1,
        "tokens": {"prompt": usage["prompt"], "completion": usage["completion"], "total": total},
        "cost_usd": usage["prompt"] * PRICE_IN_PER_TOKEN + usage["completion"] * PRICE_OUT_PER_TOKEN,
        "latency_ms": latency_ms, "model": model, "provider": "openai",
        "numeric_correct": scores["numeric_correct"], "keypoint_recall": scores["keypoint_recall"],
        "timestamp": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    }


def ask_with_images(client, model: str, question: str, sent: List[PageHit]):
    labels = "\n".join(f"[{n}] {h.doc_id} page {h.page + 1}" for n, h in enumerate(sent, 1))
    content = [{"type": "text", "text": f"Pages, in this order:\n{labels}\n\nQuestion: {question}"}]
    content += [{"type": "image_url", "image_url": {"url": image_data_url(render_page(pdf_path(h.doc_id), h.page))}}
                for h in sent]
    resp = client.chat.completions.create(
        model=model, temperature=0, max_completion_tokens=1500, reasoning_effort="low",
        messages=[{"role": "system", "content": SYSTEM_PROMPT}, {"role": "user", "content": content}])
    usage = {"prompt": resp.usage.prompt_tokens, "completion": resp.usage.completion_tokens}
    return (resp.choices[0].message.content or "").strip(), usage


def main() -> None:
    from openai import OpenAI
    import torch
    from scripts.colpali.index_filings import load_page_embs
    from scripts.colpali.retrieve import VisualRetriever

    ap = argparse.ArgumentParser()
    ap.add_argument("--model", required=True, choices=["colqwen2_5", "colpali_v1_3"])
    ap.add_argument("--run-id", default="vision_run")
    ap.add_argument("--limit", type=int, default=None)
    args = ap.parse_args()

    load_env()
    answer_model = os.environ.get("LLM_MODEL", "gpt-5.4")
    run_dir = OUT_ROOT / args.run_id
    run_dir.mkdir(parents=True, exist_ok=True)
    records_path, errors_path = run_dir / "records.jsonl", run_dir / "gen_errors.jsonl"
    done = set()
    if records_path.exists():
        done = {(r["system"], r["question_id"]) for r in map(json.loads, records_path.read_text(encoding="utf-8").splitlines()) if r}

    questions = load_questions()[: args.limit]
    texts = {d: page_texts(pdf_path(d)) for d in gold_doc_ids(questions)}
    embs = {d: load_page_embs(args.model, d) for d in texts}
    retriever, client = VisualRetriever(args.model), OpenAI()

    failed = 0
    for n, q in enumerate(questions, 1):
        if (args.model, q["id"]) in done:
            continue
        try:
            t0 = time.perf_counter()
            docs = question_doc_ids(q)
            qv = retriever.embed_query(q["question"])
            ranked = rank_pages({d: retriever.score_doc(qv, embs[d]) for d in docs})
            sent = pages_to_send(ranked, pages_per_filing(len(docs)))
            answer, usage = ask_with_images(client, answer_model, q["question"], sent)
            rec = build_record(args.model, q, ranked, sent, texts, answer, usage,
                               (time.perf_counter() - t0) * 1000.0, answer_model, args.run_id)
            with records_path.open("a", encoding="utf-8") as fh:
                fh.write(json.dumps(rec) + "\n")
            print(f"[{n}/{len(questions)}] {q['id']} pages={rec['sent_pages']}", flush=True)
        except Exception as exc:  # keep going; failures are retried on the next run
            failed += 1
            with errors_path.open("a", encoding="utf-8") as fh:
                fh.write(json.dumps({"system": args.model, "question_id": q["id"], "error": repr(exc)}) + "\n")
            print(f"[{n}/{len(questions)}] {q['id']} FAILED: {exc!r}", flush=True)
    if failed:
        raise SystemExit(f"{failed} questions failed; see {errors_path}")


if __name__ == "__main__":
    main()
```

- [ ] **Step 4: Run test to verify it passes**

Run: `$PY -m pytest tests/colpali/test_generate.py -v`
Expected: PASS. If `score_answer` rejects the question dict, read `src/system_a/evaluate.py:115-120` and pass the exact keys it needs (`answer`, `type`, `key_points`).

- [ ] **Step 5: Smoke run on 3 questions (spends a few cents, confirm with the user first)**

Run: `$PY -m scripts.colpali.generate --model colqwen2_5 --limit 3 --run-id smoke`
Expected: three `[n/3]` lines with sent pages, `reports/colpali/smoke/records.jsonl` has 3 lines. Inspect one record: `answer` is non-empty, `tokens.prompt` is in the thousands (images counted), `numeric_correct` or `keypoint_recall` is set. If the API rejects `temperature` or `reasoning_effort` for gpt-5.4 with images, print the error to the user, do not guess new parameters.

- [ ] **Step 6: Full runs for both retrievers (background, needs the user's go-ahead for spend)**

```bash
$PY -m scripts.colpali.generate --model colqwen2_5  > reports/colpali/gen_colqwen.log 2>&1
$PY -m scripts.colpali.generate --model colpali_v1_3 > reports/colpali/gen_colpali.log 2>&1
```

Expected: `reports/colpali/vision_run/records.jsonl` has 194 lines (97 per system), `gen_errors.jsonl` absent or empty. Re-run the same command to retry any failures.

- [ ] **Step 7: Commit**

```bash
git add scripts/colpali/generate.py tests/colpali/test_generate.py
git commit -m "feat(colpali): visual system generation with gpt-5.4 vision answers"
```

---

### Task 7: Score retrieval (RQ1) and answers (RQ2) for all six systems

**Files:**
- Create: `scripts/colpali/score_rq1.py`
- Test: `tests/colpali/test_score_rq1.py`

**Interfaces:**
- Consumes: `scripts.rq1.score.evaluate_records(benchmark_path, records_path, k_values)` returning `(question_rows, evidence_rows)`, `config.*`.
- Produces: `rq1_view(records: list[dict]) -> list[dict]` (swaps `retrieved_contexts`/`contexts_meta` for the top-10 `ranked_*`); files `reports/colpali/vision_run/records_rq1.jsonl`, `reports/colpali/rq1/question_scores.csv` (six systems), `evidence_scores.csv`; RQ2 scores in `reports/colpali/vision_run/scores_gpt4omini.jsonl`.

- [ ] **Step 1: Write the failing test**

```python
# tests/colpali/test_score_rq1.py
from scripts.colpali.score_rq1 import rq1_view


def test_rq1_view_scores_the_ranked_top_10_not_only_the_pages_sent_to_the_model():
    rec = {"system": "colqwen2_5", "question_id": "gold-001",
           "retrieved_contexts": ["p1"], "contexts_meta": [{"chunk_id": "a"}],
           "ranked_contexts": ["p1", "p2", "p3"], "ranked_meta": [{"chunk_id": "a"}, {"chunk_id": "b"}, {"chunk_id": "c"}]}
    view = rq1_view([rec])[0]
    assert view["retrieved_contexts"] == ["p1", "p2", "p3"]
    assert view["contexts_meta"] == rec["ranked_meta"]
    assert rec["retrieved_contexts"] == ["p1"]  # input untouched
```

- [ ] **Step 2: Run to verify failure**

Run: `$PY -m pytest tests/colpali/test_score_rq1.py -v`
Expected: FAIL (`ModuleNotFoundError`).

- [ ] **Step 3: Implement**

```python
# scripts/colpali/score_rq1.py
"""RQ1 retrieval scores for the text systems and both visual retrievers, with the unchanged RQ1 scorer.

Text systems are scored on their retrieved_contexts as published; vision systems on their ranked top-10 pages.
Usage: python -m scripts.colpali.score_rq1
"""
import json
from typing import Any, Dict, List

from scripts.colpali.config import BENCHMARK_PATH, OUT_ROOT, TEXT_RUN
from scripts.rq1.score import evaluate_records, write_csv


def rq1_view(records: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    return [{**r, "retrieved_contexts": r["ranked_contexts"], "contexts_meta": r["ranked_meta"]} for r in records]


def main() -> None:
    run = OUT_ROOT / "vision_run"
    vision = [json.loads(l) for l in (run / "records.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
    view_path = run / "records_rq1.jsonl"
    view_path.write_text("\n".join(json.dumps(r) for r in rq1_view(vision)) + "\n", encoding="utf-8")

    text_q, text_e = evaluate_records(BENCHMARK_PATH, TEXT_RUN / "records.jsonl")
    vis_q, vis_e = evaluate_records(BENCHMARK_PATH, view_path)
    out = OUT_ROOT / "rq1"
    out.mkdir(parents=True, exist_ok=True)
    write_csv(out / "question_scores.csv", text_q + vis_q)
    write_csv(out / "evidence_scores.csv", text_e + vis_e)
    print(f"scored {len(text_q)} text + {len(vis_q)} vision records -> {out}")


if __name__ == "__main__":
    main()
```

- [ ] **Step 4: Run test, then RQ1 scoring**

Run: `$PY -m pytest tests/colpali/test_score_rq1.py -v` (PASS), then `$PY -m scripts.colpali.score_rq1`.
Expected: `scored 388 text + 194 vision records`. A `ValueError` about a record missing `retrieved_contexts` names the system and question; report it to the user instead of dropping the record.

- [ ] **Step 5: Reproduce a published number as a sanity check**

Run: `$PY -c "import csv,statistics as s; r=[x for x in csv.DictReader(open('reports/colpali/rq1/question_scores.csv')) if x['system']=='system_c_v3']; print(len(r), round(s.mean(float(x['recall@all']) for x in r),3))"`
Expected: `97` and a recall@all consistent with the C v3 row in `reports/rq3` summaries. Note the value in the report's method section.

- [ ] **Step 6: Run RQ2 scoring on the vision records (conda env, judge gpt-4o-mini)**

First read the flags: `conda run -n cs614-eval python scripts/rq2/score.py --help`. Then run with the same settings as the text scores file (`reports/rq2/full_v3/report_scores_gpt4omini.md` "Configuration"): judge `openai`/`gpt-4o-mini`, factual correctness mode `recall`, reference `answer_keypoints`, atomicity `low`, scores file `scores_gpt4omini.jsonl`:

```bash
export EVAL_JUDGE_PROVIDER=openai EVAL_JUDGE_MODEL=gpt-4o-mini
conda run -n cs614-eval python scripts/rq2/score.py --run reports/colpali/vision_run \
  --scores-file scores_gpt4omini.jsonl --concurrency 4 <fc flags from --help>
```

Expected: `reports/colpali/vision_run/scores_gpt4omini.jsonl` with `status: ok` rows for both systems. For rows with `status: truncated`, re-run with the larger judge output limit flag shown in `--help` (the text run used 8192 for truncated rows). Resumable, so re-running is safe.

- [ ] **Step 7: Commit**

```bash
git add scripts/colpali/score_rq1.py tests/colpali/test_score_rq1.py reports/colpali/rq1 reports/colpali/vision_run/scores_gpt4omini.jsonl reports/colpali/vision_run/records.jsonl
git commit -m "feat(colpali): score vision and text systems with RQ1 and RQ2 scorers"
```

---

### Task 8: Comparison tables, equal-budget recall, cost, figures, case list

**Files:**
- Create: `scripts/colpali/compare.py`
- Test: `tests/colpali/test_compare.py`

**Interfaces:**
- Consumes: `reports/colpali/rq1/question_scores.csv`, records and score JSONL files for the six systems, `scripts.rq1.matching.relevance_matrix`, `scripts.rq1.matching.first_rank`.
- Produces: `bootstrap_ci(values, n=2000, seed=0) -> (mean, lo, hi)`, `primary_accuracy(record, score_rows) -> float | None`, `truncate_to_budget(contexts, words) -> list[str]`, `recall_at_budget(gold_evidence, contexts, words) -> float`, CLI writing into `reports/colpali/tables/`: `retrieval_overall.csv`, `retrieval_by_recipe.csv`, `retrieval_equal_budget.csv`, `answers_overall.csv`, `answers_by_recipe.csv`, `cost.csv`, `cases.csv`, plus `figures/*.png`.

- [ ] **Step 1: Write the failing tests**

```python
# tests/colpali/test_compare.py
from scripts.colpali.compare import bootstrap_ci, primary_accuracy, recall_at_budget, truncate_to_budget


def test_bootstrap_ci_is_deterministic_and_degenerate_for_constant_values():
    assert bootstrap_ci([1.0, 1.0, 1.0]) == (1.0, 1.0, 1.0)
    a, b = bootstrap_ci([0.0, 1.0, 1.0, 0.0]), bootstrap_ci([0.0, 1.0, 1.0, 0.0])
    assert a == b and a[0] == 0.5 and a[1] <= 0.5 <= a[2]


def test_primary_accuracy_uses_numeric_accuracy_for_numeric_and_keypoint_recall_otherwise():
    scores = [{"system": "s", "question_id": "q1", "metric": "numeric_accuracy", "value": 1.0, "status": "ok"}]
    assert primary_accuracy({"system": "s", "question_id": "q1", "type": "numeric"}, scores) == 1.0
    assert primary_accuracy({"system": "s", "question_id": "q2", "type": "qualitative", "keypoint_recall": 0.5}, scores) == 0.5
    assert primary_accuracy({"system": "s", "question_id": "q3", "type": "qualitative", "keypoint_recall": None}, scores) is None


def test_truncate_to_budget_keeps_whole_contexts_and_at_least_one():
    ctx = ["a b c", "d e f", "g h i"]
    assert truncate_to_budget(ctx, 6) == ["a b c", "d e f"]
    assert truncate_to_budget(ctx, 1) == ["a b c"]


def test_recall_at_budget_only_counts_evidence_inside_the_budget():
    ev = [{"quote": "Net cash used in financing activities was 48,474 million", "kind": "text"}]
    ctx = ["unrelated words here and there ok", "Net cash used in financing activities was 48,474 million"]
    assert recall_at_budget(ev, ctx, 6) == 0.0
    assert recall_at_budget(ev, ctx, 100) == 1.0
```

- [ ] **Step 2: Run to verify failure**

Run: `$PY -m pytest tests/colpali/test_compare.py -v`
Expected: FAIL (`ModuleNotFoundError`).

- [ ] **Step 3: Implement the pure functions**

```python
# scripts/colpali/compare.py
"""Merge RQ1 and RQ2 results for the six systems into tables, figures and a case list.

Usage: python -m scripts.colpali.compare
"""
import csv
import json
import random
import statistics
from collections import defaultdict
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Tuple

from scripts.colpali.config import BENCHMARK_PATH, OUT_ROOT, TEXT_RUN, TEXT_SCORES_FILE
from scripts.rq1.matching import first_rank, relevance_matrix

SYSTEMS = ["system_a", "system_b", "system_c_v1", "system_c_v3", "colpali_v1_3", "colqwen2_5"]
BUDGETS = (1500, 3000, 6000)  # words of retrieved context


def bootstrap_ci(values: Sequence[float], n: int = 2000, seed: int = 0) -> Tuple[float, float, float]:
    vals = [float(v) for v in values]
    mean = statistics.fmean(vals)
    rng = random.Random(seed)
    means = sorted(statistics.fmean(rng.choices(vals, k=len(vals))) for _ in range(n))
    return mean, means[int(0.025 * n)], means[int(0.975 * n) - 1]


def primary_accuracy(record: Dict[str, Any], score_rows: List[Dict[str, Any]]) -> Optional[float]:
    """RQ2 primary accuracy: numeric_accuracy for numeric questions, saved keypoint_recall otherwise."""
    if record.get("type") == "numeric":
        for row in score_rows:
            if (row["system"], row["question_id"], row["metric"]) == (
                    record["system"], record["question_id"], "numeric_accuracy") and row["status"] == "ok":
                return float(row["value"])
        return None
    value = record.get("keypoint_recall")
    return float(value) if value is not None else None


def truncate_to_budget(contexts: List[str], words: int) -> List[str]:
    kept, used = [], 0
    for ctx in contexts:
        n = len(ctx.split())
        if kept and used + n > words:
            break
        kept.append(ctx)
        used += n
    return kept


def recall_at_budget(gold_evidence: List[Dict[str, Any]], contexts: List[str], words: int) -> float:
    rel = relevance_matrix(gold_evidence, truncate_to_budget(contexts, words))
    return sum(first_rank(row) is not None for row in rel) / len(gold_evidence)
```

- [ ] **Step 4: Run to verify the pure functions pass**

Run: `$PY -m pytest tests/colpali/test_compare.py -v`
Expected: 4 passed.

- [ ] **Step 5: Validate against published text numbers before trusting new ones**

Append this temporary check to the shell (not to the module):

```bash
$PY - <<'EOF'
import json
from scripts.colpali.compare import primary_accuracy, bootstrap_ci
from scripts.colpali.config import TEXT_RUN, TEXT_SCORES_FILE
recs=[json.loads(l) for l in (TEXT_RUN/"records.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
scores=[json.loads(l) for l in (TEXT_RUN/TEXT_SCORES_FILE).read_text(encoding="utf-8").splitlines() if l.strip()]
for s in ["system_a","system_b","system_c_v1","system_c_v3"]:
    v=[primary_accuracy(r,scores) for r in recs if r["system"]==s]
    v=[x for x in v if x is not None]
    print(s, len(v), round(bootstrap_ci(v)[0],3))
EOF
```

Expected: `0.662`, `0.590`, `0.861`, `0.903` (the published primary_accuracy values, n=97). If they differ, fix `primary_accuracy` to match `scripts/rq2/analysis.py:82-95` before continuing.

- [ ] **Step 6: Implement the table writers and CLI**

Add to `scripts/colpali/compare.py`:

```python
def _read_jsonl(path: Path) -> List[Dict[str, Any]]:
    return [json.loads(l) for l in path.read_text(encoding="utf-8").splitlines() if l.strip()]


def _write(path: Path, rows: List[Dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)


def _cell(values: List[float]) -> Dict[str, float]:
    mean, lo, hi = bootstrap_ci(values)
    return {"mean": round(mean, 3), "ci_lo": round(lo, 3), "ci_hi": round(hi, 3), "n": len(values)}


def main() -> None:
    out = OUT_ROOT / "tables"
    bench = {q["id"]: q for q in json.loads(BENCHMARK_PATH.read_text(encoding="utf-8"))}
    q_rows = list(csv.DictReader((OUT_ROOT / "rq1" / "question_scores.csv").open(encoding="utf-8")))
    records = (_read_jsonl(TEXT_RUN / "records.jsonl") + _read_jsonl(OUT_ROOT / "vision_run" / "records.jsonl"))
    scores = (_read_jsonl(TEXT_RUN / TEXT_SCORES_FILE) + _read_jsonl(OUT_ROOT / "vision_run" / TEXT_SCORES_FILE))

    retrieval_metrics = ["recall@5", "recall@10", "recall@all", "complete@5", "complete@10", "complete@all",
                         "zero_recall", "average_precision"]
    overall, by_recipe = [], []
    for system in SYSTEMS:
        rows = [r for r in q_rows if r["system"] == system]
        overall.append({"system": system, **{f"{m}_{k}": v for m in retrieval_metrics
                                             for k, v in _cell([float(r[m]) for r in rows]).items()}})
        for recipe in sorted({r["recipe"] for r in rows}):
            sub = [r for r in rows if r["recipe"] == recipe]
            by_recipe.append({"system": system, "recipe": recipe,
                              **{f"{m}_{k}": v for m in ("recall@10", "recall@all", "complete@all")
                                 for k, v in _cell([float(r[m]) for r in sub]).items()}})
    _write(out / "retrieval_overall.csv", overall)
    _write(out / "retrieval_by_recipe.csv", by_recipe)

    budget_rows = []
    for system in SYSTEMS:
        recs = [r for r in records if r["system"] == system]
        ctx_key = "ranked_contexts" if system in ("colpali_v1_3", "colqwen2_5") else "retrieved_contexts"
        for words in BUDGETS:
            vals = [recall_at_budget(bench[r["question_id"]]["gold_evidence"], r[ctx_key], words) for r in recs]
            budget_rows.append({"system": system, "budget_words": words, **_cell(vals)})
    _write(out / "retrieval_equal_budget.csv", budget_rows)

    ans_overall, ans_by_recipe, per_q = [], [], {}
    for system in SYSTEMS:
        recs = [r for r in records if r["system"] == system]
        vals = {r["question_id"]: primary_accuracy(r, scores) for r in recs}
        per_q[system] = vals
        ok = [v for v in vals.values() if v is not None]
        refusals = [float(any(s["metric"] == "abstained" and s["system"] == system and s["question_id"] == r["question_id"]
                              and s["value"] == 1.0 for s in scores)) for r in recs]
        ans_overall.append({"system": system, **_cell(ok), "refusal_rate": round(statistics.fmean(refusals), 3)})
        for recipe in sorted({bench[q]["recipe"] for q in vals}):
            sub = [v for q, v in vals.items() if v is not None and bench[q]["recipe"] == recipe]
            ans_by_recipe.append({"system": system, "recipe": recipe, **_cell(sub)})
    _write(out / "answers_overall.csv", ans_overall)
    _write(out / "answers_by_recipe.csv", ans_by_recipe)

    cost = []
    for system in SYSTEMS:
        recs = [r for r in records if r["system"] == system]
        cost.append({"system": system, "mean_prompt_tokens": round(statistics.fmean(r["tokens"]["prompt"] for r in recs)),
                     "mean_cost_usd": round(statistics.fmean(float(r.get("cost_usd") or 0) for r in recs), 4),
                     "mean_latency_s": round(statistics.fmean(float(r["latency_ms"]) for r in recs) / 1000, 1)})
    _write(out / "cost.csv", cost)

    best_text = {q: max((per_q[s].get(q) or 0.0) for s in SYSTEMS[:4]) for q in bench}
    cases = []
    for system in ("colpali_v1_3", "colqwen2_5"):
        for q, v in per_q[system].items():
            if v is not None:
                cases.append({"system": system, "question_id": q, "recipe": bench[q]["recipe"],
                              "vision": round(v, 3), "best_text": round(best_text[q], 3),
                              "delta": round(v - best_text[q], 3)})
    cases.sort(key=lambda c: c["delta"])
    _write(out / "cases.csv", cases)
    print(f"tables -> {out}")


if __name__ == "__main__":
    main()
```

- [ ] **Step 7: Run it and sanity check**

Run: `$PY -m scripts.colpali.compare`
Expected: `tables -> .../reports/colpali/tables` and seven CSVs. Check `answers_overall.csv`: text rows reproduce Step 5's means; vision rows have n close to 97 (a smaller n means missing keypoints or scores, so list which ids and tell the user).

- [ ] **Step 8: Figures (load the `dataviz` skill first)**

Before writing chart code, invoke the `dataviz` skill and follow its palette and layout rules. Add `scripts/colpali/figures.py` with two functions reading the CSVs above: (a) grouped bars with CI whiskers of recall@5, recall@10, recall@all per system; (b) grouped bars of primary accuracy by recipe per system. Save PNGs to `reports/colpali/figures/retrieval_overall.png` and `answers_by_recipe.png`. Run it and open each image to check labels are legible, system names are not truncated, and the six systems are distinguishable in greyscale.

- [ ] **Step 9: Commit**

```bash
git add scripts/colpali/compare.py scripts/colpali/figures.py tests/colpali/test_compare.py reports/colpali/tables reports/colpali/figures
git commit -m "feat(colpali): comparison tables, equal-budget recall, cost and figures"
```

---

### Task 9: Index cost and storage numbers

**Files:**
- Create: `scripts/colpali/index_cost.py`

**Interfaces:**
- Consumes: `colpali_eval/v3/embs/<model>/*.pt`, `index_log.jsonl`.
- Produces: `reports/colpali/tables/index_cost.csv` with columns `model, filings, pages, bytes_per_page, total_gb, gpu_seconds_per_page`. `gpu_seconds_per_page` is only over filings embedded in this run (the 4 reused filings have no timing).

- [ ] **Step 1: Implement and run**

```python
# scripts/colpali/index_cost.py
"""Storage and indexing-time numbers per visual retriever, for the report's cost section."""
import csv
import json

import torch

from scripts.colpali.config import OUT_ROOT, emb_dir


def main() -> None:
    rows = []
    for model_key in ("colqwen2_5", "colpali_v1_3"):
        files = sorted(emb_dir(model_key).glob("*.pt"))
        pages = sum(len(torch.load(f, weights_only=True)) for f in files)
        size = sum(f.stat().st_size for f in files)
        log = emb_dir(model_key) / "index_log.jsonl"
        entries = [json.loads(l) for l in log.read_text(encoding="utf-8").splitlines()] if log.exists() else []
        timed_pages = sum(e["pages"] for e in entries)
        rows.append({"model": model_key, "filings": len(files), "pages": pages,
                     "bytes_per_page": round(size / pages), "total_gb": round(size / 1e9, 2),
                     "gpu_seconds_per_page": round(sum(e["seconds"] for e in entries) / timed_pages, 3) if timed_pages else ""})
    path = OUT_ROOT / "tables" / "index_cost.csv"
    with path.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    print(open(path, encoding="utf-8").read())


if __name__ == "__main__":
    main()
```

Run: `$PY -m scripts.colpali.index_cost`
Expected: two rows. ColQwen2.5 should be near 190 KB per page, ColPali v1.3 near 260 KB per page (earlier estimate: 755 and 1,030 vectors by 128 dims in bf16). Report any large deviation to the user.

- [ ] **Step 2: Commit**

```bash
git add scripts/colpali/index_cost.py reports/colpali/tables/index_cost.csv
git commit -m "feat(colpali): index storage and timing summary"
```

---

### Task 10: Write the report

**Files:**
- Create: `reports/colpali/REPORT.md`

**Interfaces:**
- Consumes: every CSV under `reports/colpali/tables/`, both PNGs, `ceiling.json`, `vision_run/records.jsonl` (for the failure cases), `colpali_eval/FINDINGS.md` on `origin/colpali_eval` (prior results to cite).
- Produces: the final report. Audience (state in the handoff message, not in the file): the CS614 group and the instructors reading the team's final report.

- [ ] **Step 1: Pull the failure cases**

Run: `$PY -c "import csv; r=list(csv.DictReader(open('reports/colpali/tables/cases.csv'))); print(*r[:6], sep='\n'); print('---'); print(*r[-6:], sep='\n')"`
Expected: the six questions where vision is furthest below the best text system and the six where it is furthest above. For each of the 12 (at most 3 per direction per model), open the record in `vision_run/records.jsonl` and the matching text record in `reports/rq2/full_v3/records.jsonl`, and write down what actually happened (retrieval miss, misread number, refusal). Do not infer causes without reading the answers.

- [ ] **Step 2: Write `reports/colpali/REPORT.md` with these sections, numbers copied from the tables (never typed from memory)**

1. **Summary** (5 lines): the answer to "do page-image retrievers beat text retrieval on the 97-question benchmark, and where".
2. **Setup**: benchmark (97 questions, filing count, recipes), the six systems, the retrieval protocol (gold-filing scoped, top-3 pages per filing, image cap 12), answer model and judge settings, and the ceiling result from `ceiling.json`.
3. **Retrieval results**: `retrieval_overall.csv` with CIs, `retrieval_by_recipe.csv`, and `retrieval_equal_budget.csv` with one sentence on why pages and chunks need an equal-context comparison. Include `figures/retrieval_overall.png`.
4. **Answer accuracy**: `answers_overall.csv` (primary accuracy, refusal rate) and `answers_by_recipe.csv`, with `figures/answers_by_recipe.png`. Compare against C v3 (published 0.903) directly.
5. **Where vision wins and loses**: the failure and success cases from Step 1, one short paragraph each, with question id and the retrieved page ranks.
6. **Cost and storage**: `cost.csv` and `index_cost.csv`: tokens and dollars per answer, latency, index size per page and total, GPU time, and the earlier Supabase free-tier estimate from `FINDINGS.md` section 7.
7. **Relation to earlier results**: one paragraph reconciling this run with the earlier 20-question and 5-question results (same direction or not, and why the sample and answer model differ).
8. **Limitations**: gold-filing scoping favours vision (A and B search the whole corpus); lexical matching is a lower bound and uses PDF text for pages versus Markdown chunks; one answer run per system at temperature 0; the vision prompt differs in wording from the text prompts and vision records have no citation metrics; page and chunk units differ; single judge.

- [ ] **Step 3: Check every number and claim**

Run: `grep -nE "[0-9]\.[0-9]{2,3}" reports/colpali/REPORT.md | head -60` and spot-check at least ten values against the CSVs. Confirm each case-study sentence matches the record you read. Run `$PY -m pytest tests/colpali -v` once more.
Expected: tests all pass; no figure in the report absent from a CSV.

- [ ] **Step 4: Commit**

```bash
git add reports/colpali/REPORT.md
git commit -m "docs(colpali): visual vs text retrieval report"
```

---

## Self-Review

**Spec coverage:** Worktree and branch handling (Task 0); indexing of 81 filings with both retrievers incl. PDF printing and resume (Task 4); gold-filing protocol and top-3-per-filing with image cap (Tasks 3, 6); RQ1 definitions unchanged plus equal-context recall (Tasks 7, 8); gpt-5.4 vision answers with the text systems' call parameters, judge gpt-4o-mini, CIs, recipe and hop breakdown (Tasks 6, 7, 8; hop breakdown is covered by recipe since hop is determined by recipe, and `cases.csv` carries recipe); cost and storage (Tasks 8, 9); report with failure cases, cost, limitations (Task 10); C v3 retrieval metrics via the published records' `retrieved_contexts` (Task 7); the C v3 risk and page-break risk are covered by the ceiling gate and the limitations section.

**Placeholder scan:** The only deferred values are the exact RAGAS CLI flags (Task 7 Step 6), resolved by running `--help`, and the figure code (Task 8 Step 8), which is specified by content and gated by the `dataviz` skill; both are deliberate because the first depends on a script not in this branch's history and the second on a skill read at execution time.

**Type consistency:** `PageHit` fields (`score`, `doc_id`, `page`) used identically in retrieve, generate and tests; record keys `ranked_contexts`/`ranked_meta` produced in Task 6 and consumed in Tasks 7 and 8; system names `colqwen2_5` and `colpali_v1_3` match `config.MODELS`, `generate --model`, and `compare.SYSTEMS`; `TEXT_SCORES_FILE` equals the scores filename used in Task 7 Step 6.
