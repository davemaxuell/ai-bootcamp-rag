# BUFS Multilingual Admissions RAG — Handoff

**Date:** 2026-07-24
**Branch:** `feature/bufs-rag`
**Status:** Complete — all 9 tasks built and validated.

## What this project is

A multilingual RAG assistant that helps foreign students with BUFS admissions.
Students ask in **any language**; answers are grounded in the official admission
PDFs, cited (file + page), and refuse when the documents don't cover the question.
Second feature: a personalized required-documents checklist. Deploys on Streamlit.

- **Design spec:** `docs/superpowers/specs/2026-07-24-bufs-multilingual-rag-design.md`
- **Implementation plan (9 tasks, full code per task):** `docs/superpowers/plans/2026-07-24-bufs-multilingual-rag.md`
- **Progress ledger:** `.superpowers/sdd/progress.md` (git-ignored scratch)
- **Per-task briefs & reports:** `.superpowers/sdd/task-N-brief.md`, `task-N-report.md`

## Decisions (locked)

- Answer in **any language** (translated from KO/EN source at answer time).
- Runtime LLM: OpenAI **gpt-4o-mini**. Embeddings: OpenAI **text-embedding-3-small**.
- Vector DB: **Chroma**, persistent, committed to the repo.
- Feature scope: grounded multilingual Q&A **+** checklist generator.
- Deploy: **Streamlit** Community Cloud + GitHub.

## Done so far

| Task | What | Commit | Review |
|---|---|---|---|
| Bootstrap | git repo, `feature/bufs-rag` branch, secret-protecting `.gitignore` | `5438980` | n/a |
| Task 1 | `config.py` (paths, model names, `meta_for()` filename→metadata), `requirements.txt`, `tests/test_config.py` | `a2f7e4d` | ✅ clean |
| Task 2 | `extract.py` (PDF→metadata-tagged chunks), `tests/test_extract.py` | `7effac5` | ✅ clean |
| Task 3 | Persistent, idempotent 64-chunk Chroma index | final implementation | ✅ built |
| Task 4 | Multilingual retriever with program-level filtering | final implementation | ✅ smoke-tested |
| Task 5 | Grounded answerer with citations and empty-context refusal | final implementation | ✅ tested |
| Task 6 | Personalized required-documents checklist | final implementation | ✅ tested |
| Task 7 | Streamlit chat + checklist UI | final implementation | ✅ health check |
| Task 8 | Korean/English/Chinese/Vietnamese live eval | final implementation | ✅ 4/4 |
| Task 9 | Demo notebook, README, and deployment instructions | final implementation | ✅ validated |

Tests currently: **12/12 passing** (`py -3 -m pytest`).

**Task 2 note:** the implementer found and fixed a real Windows bug — the plan's
literal `extract_all()` globbed `*.pdf` + `*.PDF`, which double-matches every file
on Windows' case-insensitive filesystem (128→64 chunks). Fix is in `7effac5`;
details are in `.superpowers/sdd/task-2-report.md`. The fix has now been reviewed
and the index contains exactly 64 vectors.

## Final validation

- Persistent index: 64 vectors, matching the 64 extracted chunks.
- Multilingual live eval: 4/4 passed.
- Streamlit health endpoint: HTTP 200.
- Unit tests: 12 passed.
- Notebook JSON and all Python modules compile successfully.

## Environment gotchas (read before running anything)

- **Windows. Use `py -3` for every python/pip/pytest command** (e.g. `py -3 -m pytest`,
  `py -3 ingest.py`, `py -3 -m streamlit run app.py`). The bare `python` on PATH is
  msys2 and has **no pip and none of the packages**.
- Installed console scripts (`streamlit.exe`, `pytest.exe`) are **not on PATH** — always
  invoke via `py -3 -m <module>`.
- **API key:** lives in `.env` as `OPENAI_API_KEY` (and duplicated in `API_key.txt`).
  Both are **git-ignored** — verified. **Never `git add .`**; stage specific files only.
  The key is real and live — rotate it if it ever leaks. For Streamlit Cloud deploy,
  put the key in **Streamlit Secrets**, not in the repo.
- The 6 source PDFs sit in the project root (untracked). `chroma_db/` gets committed
  once Task 3 runs so the deployed app needs no re-ingest.

## Unrelated files already in the folder

`test_gpt.ipynb` (a working OpenAI smoke-test notebook), `Untitled*.ipynb`, `*.txt` —
pre-existing, not part of the RAG app.
