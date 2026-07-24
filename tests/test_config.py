from config import meta_for, EMBED_MODEL, CHAT_MODEL

def test_language_detection():
    assert meta_for("[ENGLISH] ... 영문.pdf")["lang"] == "en"
    assert meta_for("[KOREAN] ... 국문.pdf")["lang"] == "ko"
    assert meta_for("제출서류 체크리스트 Check List.pdf")["lang"] == "mixed"

def test_level_detection():
    assert meta_for("[붙임 1] ... 대학원 과정 ... 국문..PDF")["level"] == "graduate"
    assert meta_for("[KOREAN] ... 학부과정 ... 국문.pdf")["level"] == "undergraduate"
    assert meta_for("BUFS 시스템 온라인 원서접수 안내.pdf")["level"] == "general"

def test_models():
    assert EMBED_MODEL == "text-embedding-3-small"
    assert CHAT_MODEL == "gpt-4o-mini"
