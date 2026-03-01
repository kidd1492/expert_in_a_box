from typing import List
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from rag.logging.log_handler import error_logger

def chunk_text(
    text: str,
    source_name: str = "unknown_source",
    chunk_size: int = 1200,
    chunk_overlap: int = 200
) -> List[Document]:
    """Chunk PDF text and tag each with metadata like topic and section."""
    if not text or not isinstance(text, str):
        error_logger.error("Expected non-empty string input for chunking.")
        raise ValueError("Expected non-empty string input for chunking.")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", ".", " ", ""]
    )

    # Split the raw text first
    document = Document(page_content=text)
    chunks = splitter.split_documents([document])
    print(f"Chunked into {len(chunks)} chunks.")

    tagged_chunks = []
    page_number = 0
    for chunk in chunks:
        content = chunk.page_content.strip()
        #TODO add some metadata to add to the dict
        page_number += 1
        metadata = {"title": source_name, "page_number": page_number}
        tagged_chunks.append(Document(page_content=content, metadata=metadata))

    return tagged_chunks
