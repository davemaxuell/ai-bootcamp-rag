from ingest import _document_id


def test_document_ids_are_stable_and_content_sensitive():
    first = _document_id("source.pdf", 1, "hello")
    assert first == _document_id("source.pdf", 1, "hello")
    assert first != _document_id("source.pdf", 2, "hello")
    assert first != _document_id("source.pdf", 1, "changed")
