# BUFS Multilingual Admissions RAG — Design Spec

**Date:** 2026-07-24
**Status:** Approved (design)

## Purpose

A multilingual Retrieval-Augmented Generation (RAG) assistant that helps foreign
students understand Busan University of Foreign Studies (BUFS) admissions. Students
ask questions in **any language** and receive grounded, cited answers drawn from the
official admissions PDFs (Korean + English). Beyond Q&A, the app generates a
**personalized required-documents checklist** for a student's program and situation.

Built as a course project satisfying: Claude Code (build tool), LangChain, RAG
(VectorDB + Embedding), a feature beyond simple translation, and Streamlit web deploy.

## Source corpus

Six official PDFs in `C:\Users\user\Desktop\0724` (~50 pages, ~63K extractable chars):

| File | Pages | Notes |
|---|---|---|
| `[ENGLISH] ... 정원외 학부과정 ... 영문.pdf` | 12 | Undergraduate admissions (EN). Good text. |
| `[KOREAN] ... 정원외 학부과정 ... 국문.pdf` | 10 | Undergraduate admissions (KO). Some tables. |
| `[붙임 1] ... 대학원 과정 ... 국문..PDF` | 9 | Graduate admissions (KO). |
| `[붙임 3] ... 대학원 과정 ... 영문..PDF` | 10 | Graduate admissions (EN). Good text. |
| `제출서류 체크리스트 Check List.pdf` | 1 | Document checklist (KO+EN). |
| `BUFS 시스템 온라인 원서접수 안내 ...pdf` | 7 | Online application guide. Screenshot-heavy (~365 chars/pg). |

**Known extraction risks:**
- Application guide + cover pages are image/screenshot-heavy — low text yield. OCR out of
  scope for v1; ingest logs coverage gaps so we know what's missing.
- Admissions tables (quotas, fees, deadlines) hold the highest-value facts and extract
  poorly with naive parsers. Use `pdfplumber` for tables, `pypdf` as fallback.

## Decisions (locked)

- **Answer language:** any — respond in the student's input language, translated from KO/EN source at answer time.
- **Runtime LLM:** OpenAI `gpt-4o-mini` (uses existing OpenAI key).
- **Embeddings:** OpenAI `text-embedding-3-small` (cross-lingual capable).
- **Vector DB:** Chroma, persistent, committed to repo (metadata filtering needed for checklist).
- **Feature scope:** multilingual grounded Q&A **+** personalized checklist generator.
- **Deploy:** Streamlit Community Cloud + GitHub. API key via Streamlit secrets.

## Components

Each unit has one purpose, a clear interface, and is independently testable.

1. **`ingest`** — Extract text per page (`pdfplumber` tables + `pypdf` fallback). Chunk
   per page (or ~800-token windows). Attach metadata `{source, page, lang, level}` where
   `level ∈ {undergraduate, graduate, general}`. Write persistent Chroma store. Log
   per-file char yield to surface coverage gaps.
   - Interface: `python -m ingest` → writes `./chroma_db/`.

2. **`retriever`** — Given a query (+ optional metadata filter), return top-k chunks from
   Chroma. Embeddings are language-agnostic, so a query in any language retrieves KO/EN
   chunks.
   - Interface: `retrieve(query, k=6, filter=None) -> list[chunk]`.

3. **`answerer`** — Given query + retrieved chunks: generate an answer **in the user's
   language**, **cite source doc + page**, and **refuse when context is insufficient**
   (never invent deadlines/requirements). Fallback message directs to the admissions office.
   - Interface: `answer(query, chunks) -> {text, citations}`.

4. **`checklist`** — Input: `level`, program/target, applicant type. Retrieve checklist +
   relevant 모집요강 chunks, produce a structured required-documents list + deadlines in the
   user's language.
   - Interface: `build_checklist(level, program, applicant_type, lang) -> structured list`.

5. **`app.py`** (Streamlit) — Two tabs: **Chat** (grounded multilingual Q&A) and
   **Checklist** (form → personalized list). Detect input language automatically.

## Data flow

```
PDFs ──ingest──▶ Chroma (persisted, committed)
                    │
 user query ──▶ retriever ──▶ answerer ──▶ answer + citation (user's language)
 form input  ──▶ retriever ──▶ checklist ─▶ required-docs list + deadlines
```

## Error handling

- Insufficient retrieval / low relevance → refuse and show fallback ("contact the
  admissions office"), do not guess.
- Every factual answer includes a citation (source file + page).
- Ingest logs low-text files so table/image coverage gaps are visible before demo.
- Missing API key → clear startup error in the Streamlit UI.

## Testing

- Gold eval set: ~15 known-answer questions (deadlines, required documents, eligibility,
  fees) across ≥3 languages. Run after ingest; verify retrieval + answer correctness and
  catch table/image extraction gaps.
- Unit-level: `retriever` returns expected doc for targeted queries; `answerer` refuses on
  empty/irrelevant context.

## Repository / file layout

- Ingestion + retrieval experiments prototyped as **Jupyter notebooks** (user preference).
- Final deployable app is **`app.py`** — Streamlit cannot run `.ipynb`; this is the one
  forced exception to the notebook-only preference.
- Secrets (`.env`, API key) never committed. `.gitignore` covers `.env`, `API_key.txt`,
  `.ipynb_checkpoints/`.

## Out of scope (v1)

- OCR of screenshot-heavy pages.
- Live sync with the university website.
- Authentication / per-user accounts.
