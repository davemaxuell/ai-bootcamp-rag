from extract import split_text, extract_all, Chunk

def test_split_text_respects_size():
    parts = split_text("a" * 4500, size=2000)
    assert len(parts) == 3
    assert all(len(p) <= 2000 for p in parts)

def test_split_text_short_returns_one():
    assert split_text("hello", size=2000) == ["hello"]

def test_extract_all_returns_chunks_with_metadata():
    chunks = extract_all()
    assert len(chunks) > 0
    c = chunks[0]
    assert isinstance(c, Chunk)
    assert c.source and c.page >= 1
    assert c.lang in {"ko", "en", "mixed"}
    assert c.level in {"undergraduate", "graduate", "general"}
    # every chunk has real text
    assert all(ch.text.strip() for ch in chunks)
