from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

from answerer import REFUSAL, _citations, format_context
from config import CHAT_MODEL
from retriever import retrieve

load_dotenv()

SYSTEM = (
    "You are a BUFS admissions assistant. Using ONLY the context, produce a clear "
    "checklist of required application documents and their deadlines for the given "
    "applicant. Reply in the requested language. Use a numbered list. Clearly mark "
    "requirements that depend on nationality, degree, language score, or applicant "
    "type. If the context lacks information, say so and refer the applicant to the "
    "admissions office. Cite supporting items inline as [source: filename | page: N]."
)


def build_checklist(
    level: str,
    program: str,
    applicant_type: str,
    lang: str,
    retriever_fn=retrieve,
) -> dict:
    query = (
        f"required application documents submission checklist deadlines "
        f"{level} {program} {applicant_type}"
    )
    docs = retriever_fn(query, k=8, level=level)
    if not docs:
        return {"text": REFUSAL, "citations": []}
    llm = ChatOpenAI(model=CHAT_MODEL, temperature=0)
    context = format_context(docs)
    request = (
        f"Applicant: level={level}, program={program}, type={applicant_type}. "
        f"Answer language: {lang}."
    )
    message = llm.invoke(
        [("system", SYSTEM), ("human", f"Context:\n{context}\n\n{request}")]
    )
    return {"text": message.content, "citations": _citations(docs)}
