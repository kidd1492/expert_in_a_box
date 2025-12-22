import os, re, fitz
from core.embedding import load_or_create_vector_store
from core.chunking import chunk_text
from utils.log_handler import app_logger, project_logger
from langchain_text_splitters import MarkdownTextSplitter


def read_document(filepath):
    if not os.path.exists(filepath):
        project_logger.error(f"File not found: {filepath}")
        return f"File not found: {filepath}"

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
        # Skip chunk_text — already chunked

    else:
        project_logger.error(f"Unsupported file type: {filepath}")
        return f"Unsupported file type: {ext}"

    load_or_create_vector_store(chunks)
    app_logger.info(f"{filepath} written to RAG database")
    return f"Finished Loading {ext.upper()} into Store"


def load_pdf(filepath: str) -> str:
    """Load and clean text from a single PDF file."""
    try:
        doc = fitz.open(filepath)
        text = "\n".join([page.get_text() for page in doc])
    except Exception as e:
        project_logger.error(f"Error reading PDF {filepath}: {e}")
        raise RuntimeError(f"Failed to load PDF: {e}")

    # Clean the text (preserve newlines, normalize spacing)
    text = re.sub(r"[ \t]+", " ", text)       # collapse spaces/tabs
    text = re.sub(r"\n{2,}", "\n", text)      # remove excessive newlines
    return text
