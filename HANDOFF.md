# BUFS Multilingual Admissions RAG — Handoff

**Date:** 2026-07-24
**Branch:** `feature/bufs-rag`
**Status:** 2 of 9 tasks built. Paused for handoff.

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
| Task 2 | `extract.py` (PDF→metadata-tagged chunks), `tests/test_extract.py` | `7effac5` | ⚠️ **review interrupted — must re-review** |

Tests currently: **6/6 passing** (`py -3 -m pytest`).

**Task 2 note:** the implementer found and fixed a real Windows bug — the plan's
literal `extract_all()` globbed `*.pdf` + `*.PDF`, which double-matches every file
on Windows' case-insensitive filesystem (128→64 chunks). Fix is in `7effac5`;
details in `.superpowers/sdd/task-2-report.md`. The review of this fix did not
finish, so **re-review Task 2 first**.

## Remaining tasks (3–9, all fully specified in the plan)

3. `ingest.py` — embed chunks into persistent Chroma (`chroma_db/`, committed). **First task that spends OpenAI credits.**
4. `retriever.py` — `retrieve(query, k, level)` with metadata filter.
5. `answerer.py` — grounded, cited answer; **refuses without calling the LLM on empty context**.
6. `checklist.py` — `build_checklist(...)` personalized document list.
7. `app.py` — Streamlit UI (Chat + Checklist tabs).
8. `eval/` — multilingual gold-question eval set.
9. `notebooks/01_explore_pdfs.ipynb`, `README.md`, deploy prep.

## How to continue

Two options for your colleague:

**A. Same subagent-driven flow** (what was running): per task — extract brief
(`.superpowers/sdd/scripts` helpers in the superpowers skill), dispatch a fresh
implementer, generate a review package, dispatch a reviewer, fix Critical/Important,
mark complete in the ledger. Re-review Task 2 before starting Task 3.

**B. Manual** — the plan has complete, copy-pasteable code and TDD steps for every
task. Just work top to bottom from Task 3, committing per task.

Either way, after all tasks: run the gold eval (Task 8) and do one whole-branch review.

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
