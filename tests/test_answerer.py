from langchain_core.documents import Document

from answerer import REFUSAL, answer, format_context


def test_refuses_on_empty_context_without_api():
    result = answer("When is the deadline?", [])
    assert result["text"] == REFUSAL
    assert result["citations"] == []


def test_format_context_includes_source_and_page():
    document = Document(
        page_content="Deadline is 2026-06-01",
        metadata={
            "source": "eng.pdf",
            "page": 3,
            "lang": "en",
            "level": "undergraduate",
        },
    )
    context = format_context([document])
    assert "eng.pdf" in context
    assert "3" in context
    assert "Deadline" in context
