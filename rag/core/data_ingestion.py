# core/data_ingestion.py
import os, re, fitz
from langchain_text_splitters import MarkdownTextSplitter
from rag.core.chunking import chunk_text
from rag.logging.log_handler import error_logger


def read_document(filepath: str):
    if not os.path.exists(filepath):
        error_logger.error(f"File not found: {filepath}")
        return None, f"File not found: {filepath}"

    ext = filepath.split(".")[-1].lower()

    if ext == "pdf":
        text = load_pdf(filepath)
        chunks = chunk_text(text, source_name=filepath)

    elif ext == "txt":
        with open(filepath, 'r', encoding='UTF-8') as file:
            text = file.read()
        chunks = chunk_text(text, source_name=filepath)

    elif ext == "md":
        with open(filepath, 'r', encoding='UTF-8') as file:
            markdown_text = file.read()
        splitter = MarkdownTextSplitter(chunk_size=1000, chunk_overlap=100)
        chunks = splitter.create_documents([markdown_text])

    else:
        error_logger.error(f"Unsupported file type: {filepath}")
        return None, f"Unsupported file type: {ext}"

    return chunks, ext.upper()


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
