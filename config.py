from pathlib import Path

BASE = Path(__file__).resolve().parent
PDF_DIR = BASE
CHROMA_DIR = BASE / "chroma_db"
EMBED_MODEL = "text-embedding-3-small"
CHAT_MODEL = "gpt-4o-mini"
COLLECTION = "bufs_admissions"

def meta_for(filename: str) -> dict:
    upper = filename.upper()
    if "영문" in filename or "ENGLISH" in upper:
        lang = "en"
    elif "국문" in filename or "KOREAN" in upper:
        lang = "ko"
    else:
        lang = "mixed"
    if "대학원" in filename:
        level = "graduate"
    elif "학부" in filename:
        level = "undergraduate"
    else:
        level = "general"
    return {"source": filename, "lang": lang, "level": level}
