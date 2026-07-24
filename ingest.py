import hashlib

from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings

from config import CHROMA_DIR, COLLECTION, EMBED_MODEL
from extract import extract_all

load_dotenv()


def _embeddings() -> OpenAIEmbeddings:
    return OpenAIEmbeddings(model=EMBED_MODEL)


def get_vectorstore() -> Chroma:
    return Chroma(
        collection_name=COLLECTION,
        embedding_function=_embeddings(),
        persist_directory=str(CHROMA_DIR),
    )


def _document_id(source: str, page: int, text: str) -> str:
    payload = f"{source}\0{page}\0{text}".encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def build() -> int:
    chunks = extract_all()
    docs = [
        Document(
            page_content=chunk.text,
            metadata={
                "source": chunk.source,
                "page": chunk.page,
                "lang": chunk.lang,
                "level": chunk.level,
            },
        )
        for chunk in chunks
    ]
    ids = [_document_id(chunk.source, chunk.page, chunk.text) for chunk in chunks]

    store = get_vectorstore()
    existing_ids = set(store.get(include=[])["ids"])
    current_ids = set(ids)
    stale_ids = list(existing_ids - current_ids)
    if stale_ids:
        store.delete(ids=stale_ids)
    if docs:
        store.add_documents(docs, ids=ids)
    return len(docs)


if __name__ == "__main__":
    count = build()
    print(f"indexed {count} chunks into {CHROMA_DIR}")
