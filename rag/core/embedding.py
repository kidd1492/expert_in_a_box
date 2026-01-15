# core/embedding.py
import numpy as np
from langchain_ollama import OllamaEmbeddings
from langchain_core.documents import Document

EMBED_MODEL = "mxbai-embed-large:335m"
embedding_model = OllamaEmbeddings(model=EMBED_MODEL)


def embed_text(text: str) -> np.ndarray:
    embedding = embedding_model.embed_query(text)
    return np.array(embedding, dtype=np.float32)


def embed_documents(chunks: list[Document]) -> list[tuple[str, dict, np.ndarray]]:
    """
    Returns a list of (content, metadata, embedding_array)
    without touching the database.
    """
    results = []
    for chunk in chunks:
        content = chunk.page_content.strip()
        metadata = chunk.metadata or {}
        emb = embed_text(content)
        results.append((content, metadata, emb))
    return results
