# services/ingestion_service.py
import json, os
from rag.core.data_ingestion import read_document
from rag.core.embedding import embed_documents
from rag.core.vectors import VectorStore
from rag.logging.log_handler import doc_logger, error_logger


class IngestionService:
    def __init__(self, vector_store: VectorStore | None = None):
        self.vector_store = vector_store or VectorStore()

    def add_file(self, filepath: str) -> str:
        result = read_document(filepath)
        if not result["ok"]:
            error_logger.error(result["error"])
            return result["error"]

        chunks = result["chunks"]
        ext = result["ext"]

        embedded = embed_documents(chunks)
        stored_count = 0

        for content, metadata, embedding_array in embedded:
            raw_title = metadata.get("title", filepath)
            clean_title = os.path.basename(raw_title)
            clean_title = os.path.splitext(clean_title)[0]

            metadata["title"] = clean_title

            # VectorStore expects metadata as dict, not JSON string
            self.vector_store.add_document(
                content=content,
                title=clean_title,
                metadata=metadata,
                embedding=embedding_array
            )

            stored_count += 1

        doc_logger.info(f"'{filepath}' written to RAG database with {stored_count} chunks")
        return f"Finished loading {ext} into store ({stored_count} chunks)"
