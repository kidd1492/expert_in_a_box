# services/retrieval_service.py
from rag.core.vectors import VectorStore
from rag.core.embedding import embed_text


class RetrievalService:
    def __init__(self, vector_store: VectorStore | None = None):
        self.vector_store = vector_store or VectorStore()

    def retrieve(self, query: str, search_type: str = "similarity", top_k: int = 3, titles: str = "all"):
        query_embedding = embed_text(query)
        results = self.vector_store.query_documents(query_embedding, search_type=search_type, top_k=top_k, titles=titles)
        return results
