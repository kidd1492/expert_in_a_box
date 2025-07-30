from typing import List
from langchain.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
import re
import os

def chunk_pdf_text(
    text: str,
    source_name: str = "unknown_source",
    chunk_size: int = 300,
    chunk_overlap: int = 30
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
    print(f"✅ Chunked into {len(chunks)} chunks.")

    tagged_chunks = []
    current_section = "Introduction"
    current_topic = "General Concepts"

    for chunk in chunks:
        content = chunk.page_content.strip()

        # Try to detect a heading — very basic
        header_match = re.search(r"(Chapter\s+\d+:.*|^\d+\.\s+.*|#+\s*.*)", content)
        if header_match:
            heading = header_match.group(0)
            # Simplify the header to extract topic name
            current_topic = re.sub(r"(Chapter\s+\d+:|\d+\.\s+|#+)", "", heading).strip()
            current_section = heading.strip()

        metadata = {
            "topic": current_topic,
            "section": current_section,
            "source": source_name
        }

        tagged_chunks.append(Document(page_content=content, metadata=metadata))

    return tagged_chunks
