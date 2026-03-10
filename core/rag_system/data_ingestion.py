# core/data_ingestion.py
import os, re, fitz
from utils.helper_functions import read_file
from logging_file.log_handler import error_logger


def read_document(file_path: str) -> str:
    if not os.path.exists(file_path):
        error_logger.error(f"File not found: {file_path}")

    ext = file_path.split(".")[-1].lower()

    # --- PDF ---
    if ext == "pdf":
        text = load_pdf(file_path)

    elif ext in ["txt", "md"]:
        text = read_file(file_path)
    else:
        error_logger.error(f"Unsupported file type: {file_path}")
        return f""

    return text


def load_pdf(file_path: str) -> str:
    """Load and clean text from a single PDF file."""
    try:
        doc = fitz.open(file_path)
        text = "\n".join([page.get_text() for page in doc])
    except Exception as e:
        error_logger.error(f"Error reading PDF {file_path}: {e}")
        raise RuntimeError(f"Failed to load PDF: {e}")

    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{2,}", "\n", text)
    return text
