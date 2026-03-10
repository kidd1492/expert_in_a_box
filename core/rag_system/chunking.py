from typing import List
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from core.logging.log_handler import error_logger

def chunk_text(
    text: str,
    chunk_size: int = 1200,
    chunk_overlap: int = 200
) -> List[Document]:
    
    if not text or not isinstance(text, str):
        error_logger.error("Expected non-empty string input for chunking.")
        raise ValueError("Expected non-empty string input for chunking.")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", ".", " ", ""]
    )
    document = Document(page_content=text)
    chunks = splitter.split_documents([document])
    return chunks


def get_metadata(chunks, source_name):
    tagged_chunks = []
    page_number = 0
    for chunk in chunks:
        content = chunk.page_content.strip()
        page_number += 1
        metadata = {
            "title": source_name.split("/")[-1],
            "page_number": page_number,
            "source_path": source_name,
            "source_type": source_name.split(".")[-1].lower()
        }
        tagged_chunks.append(Document(page_content=content, metadata=metadata))

    return tagged_chunks
