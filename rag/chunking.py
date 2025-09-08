from typing import List
from langchain.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from log_handler import app_logger

def chunk_text(
    text: str,
    source_name: str = "unknown_source",
    chunk_size: int = 1200,
    chunk_overlap: int = 200
) -> List[Document]:
    """Chunk PDF text and tag each with metadata like topic and section."""
    if not text or not isinstance(text, str):
        raise ValueError("Expected non-empty string input for chunking.")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", ".", " ", ""]
    )

    # Split the raw text first
    document = Document(page_content=text)
    chunks = splitter.split_documents([document])
    app_logger.info(f"Chunked into {len(chunks)} chunks.")
    print(f"Chunked into {len(chunks)} chunks.")

    tagged_chunks = []

    for chunk in chunks:
        content = chunk.page_content.strip()
        metadata = {"source": source_name}
        tagged_chunks.append(Document(page_content=content, metadata=metadata))

    return tagged_chunks
