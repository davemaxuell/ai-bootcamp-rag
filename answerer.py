from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

from config import CHAT_MODEL

load_dotenv()

REFUSAL = (
    "I could not find this in the official BUFS admissions documents. "
    "Please contact the BUFS admissions office to confirm."
)

SYSTEM = (
    "You are a BUFS admissions assistant for foreign students. "
    "Answer ONLY from the provided context. "
    "Reply in the SAME language as the user's question. "
    "If the context does not contain the answer, say you don't know and refer them "
    "to the admissions office; never invent deadlines, fees, or requirements. "
    "Cite supporting facts inline using [source: filename | page: N]."
)


def format_context(docs) -> str:
    blocks = []
    for doc in docs:
        metadata = doc.metadata
        blocks.append(
            f"[source: {metadata['source']} | page: {metadata['page']}]\n"
            f"{doc.page_content}"
        )
    return "\n\n---\n\n".join(blocks)


def _citations(docs) -> list[dict]:
    seen = set()
    citations = []
    for doc in docs:
        citation = (doc.metadata["source"], doc.metadata["page"])
        if citation not in seen:
            seen.add(citation)
            citations.append({"source": citation[0], "page": citation[1]})
    return citations


def answer(query: str, docs: list) -> dict:
    if not docs:
        return {"text": REFUSAL, "citations": []}
    llm = ChatOpenAI(model=CHAT_MODEL, temperature=0)
    context = format_context(docs)
    message = llm.invoke(
        [
            ("system", SYSTEM),
            ("human", f"Context:\n{context}\n\nQuestion: {query}"),
        ]
    )
    return {"text": message.content, "citations": _citations(docs)}
