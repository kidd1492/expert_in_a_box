from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
from typing import List
from langchain_ollama import OllamaEmbeddings
import sqlite3
import json
import numpy as np


def init_db(db_path="rag_store.db"):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS documents (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        content TEXT,
        title TEXT,
        metadata TEXT
    )""")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS embeddings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        document_id INTEGER,
        embedding_vector BLOB,
        FOREIGN KEY(document_id) REFERENCES documents(id)
    )""")

    conn.commit()
    return conn


def chunk_text(
    text: str,
    source_name: str = "unknown_source",
    chunk_size: int = 1500,
    chunk_overlap: int = 300
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
    print(f"Chunked into {len(chunks)} chunks.")

    tagged_chunks = []

    for chunk in chunks:
        content = chunk.page_content.strip()
        metadata = {
            "source": source_name
        }

        tagged_chunks.append(Document(page_content=content, metadata=metadata))

    return tagged_chunks



def add_to_store(chunks, conn):
    embedding_model = OllamaEmbeddings(model="mxbai-embed-large:335m")
    cursor = conn.cursor()

    for chunk in chunks:
        # Insert document
        content = chunk.page_content
        title = chunk.metadata.get("title", "")
        metadata_json = json.dumps(chunk.metadata)

        cursor.execute(
            "INSERT INTO documents (content, title, metadata) VALUES (?, ?, ?)",
            (content, title, metadata_json)
        )
        doc_id = cursor.lastrowid

        # Embed and store vector
        embedding = embedding_model.embed_query(content)
        embedding_blob = np.array(embedding, dtype=np.float32).tobytes()

        cursor.execute(
            "INSERT INTO embeddings (document_id, embedding_vector) VALUES (?, ?)",
            (doc_id, embedding_blob)
        )

    conn.commit()
    print(f"Stored {len(chunks)} chunks with embeddings.")



def retriever_tool(query: str, search_type: str = "similarity") -> str:
    """Tool that queries SQLite-stored documents using cosine similarity or MMR reranking."""

    print(f".tool_call : retriever_tool with search_type={search_type} query: {query}\n")

    EMBED_MODEL = "mxbai-embed-large:335m"
    DB_PATH = "rag_store.db"
    embedding_model = OllamaEmbeddings(model=EMBED_MODEL)
    query_embedding = np.array(embedding_model.embed_query(query), dtype=np.float32)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT document_id, embedding_vector FROM embeddings")
    rows = cursor.fetchall()

    similarities = []
    for doc_id, blob in rows:
        vec = np.frombuffer(blob, dtype=np.float32)
        sim = np.dot(query_embedding, vec) / (np.linalg.norm(query_embedding) * np.linalg.norm(vec))
        similarities.append((doc_id, vec, sim))

    # Sort or rerank
    if search_type == "mmr":
        # Simple MMR-like reranking: pick diverse top-k based on cosine distance
        selected = []
        remaining = sorted(similarities, key=lambda x: x[2], reverse=True)
        while remaining and len(selected) < 3:
            best = remaining.pop(0)
            selected.append(best)
            remaining = [r for r in remaining if np.dot(best[1], r[1]) / (np.linalg.norm(best[1]) * np.linalg.norm(r[1])) < 0.95]
    else:
        selected = sorted(similarities, key=lambda x: x[2], reverse=True)[:3]

    doc_ids = [doc_id for doc_id, _, _ in selected]
    placeholders = ",".join("?" for _ in doc_ids)
    cursor.execute(f"SELECT content, metadata FROM documents WHERE id IN ({placeholders})", doc_ids)
    results = cursor.fetchall()

    if not results:
        return "I found no relevant information."
    
    print("\n\n".join([f"Document {i+1}:\n{content}" for i, (content, _) in enumerate(results)]))
    return "\n\n".join([f"Document {i+1}:\n{content}" for i, (content, _) in enumerate(results)])


if __name__ == "__main__":
    retriever_tool("When was the first cpu used in a computer?", search_type="mmr")
    '''
    filepath = "text.txt"
    with open(filepath, "r", encoding="utf-8") as f:
        text = f.read()

    conn = init_db("rag_store.db")
    chunks = chunk_text(text, source_name=filepath)
    add_to_store(chunks, conn)
    '''
