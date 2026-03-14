# webapp/models.py
from core.services.ingestion_service import IngestionService
from core.services.retrieval_service import RetrievalService
from core.services.chat_service import ChatService
from core.rag_system.vectors import VectorStore
from core.services.memory_service import MemoryService

from core.services.research_service import ResearchService

vector_store = VectorStore()

ingestion_service = IngestionService(vector_store)
retrieval_service = RetrievalService(vector_store)
chat_service = ChatService()
memory_service = MemoryService()
research_service = ResearchService()
