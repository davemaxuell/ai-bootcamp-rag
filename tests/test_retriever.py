from unittest.mock import Mock, patch

from retriever import retrieve


def test_empty_query_does_not_load_vectorstore():
    with patch("retriever.get_vectorstore") as get_vectorstore:
        assert retrieve("   ") == []
        get_vectorstore.assert_not_called()


def test_level_filter_includes_general_documents():
    store = Mock()
    store.similarity_search.return_value = []
    with patch("retriever.get_vectorstore", return_value=store):
        retrieve("documents", k=4, level="graduate")
    store.similarity_search.assert_called_once_with(
        "documents",
        k=4,
        filter={"level": {"$in": ["graduate", "general"]}},
    )
