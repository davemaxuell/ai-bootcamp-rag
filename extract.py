from dataclasses import dataclass
from pathlib import Path
import pdfplumber
from pypdf import PdfReader
from config import PDF_DIR, meta_for


@dataclass
class Chunk:
    text: str
    source: str
    page: int
    lang: str
    level: str


def split_text(text: str, size: int = 2000) -> list[str]:
    text = text.strip()
    if not text:
        return []
    return [text[i:i + size] for i in range(0, len(text), size)]


def _page_texts(pdf_path) -> list[str]:
    """Per-page text: pdfplumber first (better tables), pypdf fallback."""
    out = []
    with pdfplumber.open(pdf_path) as pdf:
        plumber_pages = [(p.extract_text() or "") for p in pdf.pages]
    reader = PdfReader(str(pdf_path))
    for i, ptext in enumerate(plumber_pages):
        if len(ptext.strip()) < 20 and i < len(reader.pages):
            ptext = reader.pages[i].extract_text() or ptext
        out.append(ptext)
    return out


def extract_chunks(pdf_path) -> list[Chunk]:
    fname = Path(pdf_path).name
    m = meta_for(fname)
    chunks = []
    for page_no, ptext in enumerate(_page_texts(pdf_path), start=1):
        for piece in split_text(ptext):
            chunks.append(Chunk(piece, fname, page_no, m["lang"], m["level"]))
    return chunks


def extract_all() -> list[Chunk]:
    # Note: on case-insensitive filesystems (e.g. Windows), "*.pdf" and
    # "*.PDF" glob patterns both match every file with the same casing,
    # so we dedupe by filename to avoid double-processing (and thus
    # double-embedding) each PDF.
    all_paths = list(PDF_DIR.glob("*.pdf")) + list(PDF_DIR.glob("*.PDF"))
    paths = sorted({p.name: p for p in all_paths}.values(), key=lambda p: p.name)
    chunks = []
    for p in paths:
        chunks.extend(extract_chunks(p))
    return chunks
