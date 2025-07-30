from embedding import load_or_create_vector_store
import fitz  # PyMuPDF
import re
from chunking import chunk_pdf_text

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
    return text.strip()



pdf_path = "C:/Users/chris/Desktop/AI_research/machine_learning.pdf"
text = load_pdf(pdf_path)
chunks = chunk_pdf_text(text, chunk_size=300, chunk_overlap=30)

# Optional preview
for i, chunk in enumerate(chunks[:5]):
    print(f"\n--- Chunk {i+1} ---\n{chunk.page_content[:300]}")

load_or_create_vector_store(chunks)
