# webapp/models.py
from rag.services.ingestion_service import IngestionService
from rag.services.retrieval_service import RetrievalService
from rag.services.chat_service import ChatService
from rag.core.vectors import VectorStore


vector_store = VectorStore()

ingestion_service = IngestionService(vector_store)
retrieval_service = RetrievalService(vector_store)
chat_service = ChatService()

