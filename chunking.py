# chunking.py

from typing import List
from langchain.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter

def chunk_pdf_text(text: str, chunk_size: int = 300, chunk_overlap: int = 30) -> List[Document]:
    """Chunk PDF text into LangChain Document objects."""
    if not text or not isinstance(text, str):
        raise ValueError("Expected non-empty string input for chunking.")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", ".", " ", ""]
    )

    document = Document(page_content=text)
    chunks = splitter.split_documents([document])

    print(f"✅ Chunked into {len(chunks)} chunks.")
    return chunks
