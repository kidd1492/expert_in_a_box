# core/data_ingestion.py
import os, re, fitz
from rag.core.chunking import chunk_text
from rag.logging.log_handler import error_logger


def read_document(filepath: str):
    if not os.path.exists(filepath):
        error_logger.error(f"File not found: {filepath}")
        return {
            "ok": False,
            "chunks": None,
            "ext": None,
            "error": f"File not found: {filepath}"
        }

    ext = filepath.split(".")[-1].lower()

    # --- PDF ---
    if ext == "pdf":
        text = load_pdf(filepath)
        chunks = chunk_text(text, source_name=filepath)

    # --- TXT ---
    elif ext == "txt":
        with open(filepath, 'r', encoding='UTF-8') as file:
            text = file.read()
        chunks = chunk_text(text, source_name=filepath)

    # --- MARKDOWN (normalize to your chunker) ---
    elif ext == "md":
        with open(filepath, 'r', encoding='UTF-8') as file:
            markdown_text = file.read()
        chunks = chunk_text(markdown_text, source_name=filepath)

    # --- Unsupported ---
    else:
        error_logger.error(f"Unsupported file type: {filepath}")
        return {
            "ok": False,
            "chunks": None,
            "ext": None,
            "error": f"Unsupported file type: {ext}"
        }

    return {
        "ok": True,
        "chunks": chunks,
        "ext": ext.upper(),
        "error": None
    }


def load_pdf(filepath: str) -> str:
    """Load and clean text from a single PDF file."""
    try:
        doc = fitz.open(filepath)
        text = "\n".join([page.get_text() for page in doc])
    except Exception as e:
        error_logger.error(f"Error reading PDF {filepath}: {e}")
        raise RuntimeError(f"Failed to load PDF: {e}")

    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{2,}", "\n", text)
    return text
