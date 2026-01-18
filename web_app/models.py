# webapp/models.py
from rag.services.ingestion_service import IngestionService
from rag.services.retrieval_service import RetrievalService
from rag.services.memory_service import MemoryService
from rag.core.vectors import VectorStore
from rag.core.memory import MemoryStore

vector_store = VectorStore()
memory_store = MemoryStore()

ingestion_service = IngestionService(vector_store)
retrieval_service = RetrievalService(vector_store)
memory_service = MemoryService(memory_store)
