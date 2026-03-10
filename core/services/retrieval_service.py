from core.rag_system.vectors import VectorStore
from core.rag_system.embedding import embed_text

class RetrievalService:
    def __init__(self, vector_store: VectorStore | None = None):
        self.vector_store = vector_store or VectorStore()

    def retrieve(self, query: str, search_type: str = "similarity", top_k: int = 3, titles: str = "all"):
        # Embed the query text
        query_embedding = embed_text(query)

        # { "id", "content", "metadata", "score" }
        results = self.vector_store.query_documents(
            query_embedding=query_embedding,
            search_type=search_type,
            top_k=top_k,
            titles=titles
        )

        return results

    def retrieve_doc(self, title: str):
        return self.vector_store.retrieve_document(title)

    def list_docs(self):
        return self.vector_store.list_docs()
