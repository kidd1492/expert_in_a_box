from embedding import load_or_create_vector_store
import fitz  # PyMuPDF
import re
from chunking import chunk_text


def read_document(filepath):
    ext = filepath.split(".")[-1]
    if ext == "pdf":
        text = load_pdf(filepath)
        chunks = chunk_text(text, chunk_size=500, chunk_overlap=50)
        load_or_create_vector_store(chunks)
        return "Finished Loading PDF into Store"
    elif ext == "txt":
        with open(filepath, 'r', encoding='UTF-8') as file:
            text = file.read()
            chunks = chunk_text(text, chunk_size=500, chunk_overlap=50)
            load_or_create_vector_store(chunks)
            return "Finished Loading PDF into Store"
    else:
        print("could not read ext")


def load_pdf(filepath: str) -> str:
    """Load and clean text from a single PDF file."""
    try:
        doc = fitz.open(filepath)
        text = "\n".join([page.get_text() for page in doc])
    except Exception as e:
        raise RuntimeError(f"Failed to load PDF: {e}")

    # Clean the text (preserve newlines, normalize spacing)
    text = re.sub(r"[ \t]+", " ", text)       # collapse spaces/tabs
    text = re.sub(r"\n{2,}", "\n", text)      # remove excessive newlines
    return text
