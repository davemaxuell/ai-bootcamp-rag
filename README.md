# BUFS Multilingual Admissions RAG

**작성자:** 맥슈웰 데이브<br>
**학번:** 20232829

A Streamlit assistant for international applicants to Busan University of
Foreign Studies. It retrieves relevant passages from six official Korean and
English admissions PDFs, answers in the question's language, cites filenames
and page numbers, and builds a personalized application-document checklist.

**Live app:** https://ai-bootcamp-rag-7ahkiva6fmc7qzkiifmz6a.streamlit.app/

## Setup

Python 3.11+ is recommended. On Windows, use the Python launcher:

```powershell
py -3 -m pip install -r requirements.txt
```

Create a local `.env` file containing:

```text
OPENAI_API_KEY=your-key
```

The key is used by `text-embedding-3-small` during indexing and by
`gpt-4o-mini` when generating answers. `.env` and `API_key.txt` are ignored by
git and must never be committed.

## Build and run

Build or refresh the persistent Chroma index after adding or changing PDFs:

```powershell
py -3 ingest.py
```

The index uses stable document IDs, so this command is safe to rerun.

Start the app:

```powershell
py -3 -m streamlit run app.py
```

Run the unit tests and the live multilingual evaluation:

```powershell
py -3 -m pytest
py -3 eval/run_eval.py
```

The unit tests do not call OpenAI. Indexing and the live evaluation do.

## Project structure

- `extract.py` extracts page text and attaches source metadata.
- `ingest.py` embeds the extracted chunks into persistent Chroma storage.
- `retriever.py` performs multilingual similarity search with optional program
  level filtering.
- `answerer.py` produces grounded answers and citations.
- `checklist.py` generates a tailored required-document list.
- `app.py` provides the chat and checklist Streamlit interface.
- `eval/` contains multilingual retrieval/answer checks.
- `notebooks/01_explore_pdfs.ipynb` provides an interactive walkthrough.

## Deploy on Streamlit Community Cloud

1. Push the repository, including the built `chroma_db/` directory, to GitHub.
2. Create a Streamlit Community Cloud app with `app.py` as the entry point.
3. In the app settings, add this to **Secrets**:

   ```toml
   OPENAI_API_KEY = "your-key"
   ```

4. Deploy. Do not put the key in source code, the repository, or a committed
   configuration file.

The answers are generated from the supplied official PDFs, but applicants
should confirm consequential deadlines and requirements with the BUFS
admissions office.

## 제출 자료

- 소스 코드 노트북: `submission/BUFS_Admissions_RAG_20232829.ipynb`
- 프로젝트 결과 보고서: `submission/BUFS_Admissions_RAG_결과보고서_20232829.docx`
- 최종 배포 웹 URL: https://ai-bootcamp-rag-7ahkiva6fmc7qzkiifmz6a.streamlit.app/
