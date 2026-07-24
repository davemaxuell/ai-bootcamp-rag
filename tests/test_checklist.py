from checklist import REFUSAL, build_checklist


def test_empty_retrieval_refuses_without_api():
    result = build_checklist(
        level="undergraduate",
        program="Korean Language",
        applicant_type="new",
        lang="en",
        retriever_fn=lambda *args, **kwargs: [],
    )
    assert result["text"] == REFUSAL
    assert result["citations"] == []
