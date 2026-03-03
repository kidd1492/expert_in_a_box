# services/ingestion_service.py
import os
from rag.core.data_ingestion import read_document
from rag.core.embedding import embed_documents
from rag.core.vectors import VectorStore
from rag.logging.log_handler import doc_logger, error_logger


class IngestionService:
    def __init__(self, vector_store: VectorStore | None = None):
        self.vector_store = vector_store or VectorStore()

    def add_file(self, filepath: str) -> str:
        # --- Read and validate document ---
        result = read_document(filepath)
        if not result["ok"]:
            error_logger.error(result["error"])
            return result["error"]

        chunks = result["chunks"]
        ext = result["ext"]

        # --- Embed chunks ---
        embedded = embed_documents(chunks)
        stored_count = 0

        # --- Store each embedded chunk ---
        for record in embedded:
            content = record["content"]
            metadata = record["metadata"]
            embedding_array = record["embedding"]

            # Normalize title
            raw_title = metadata.get("title", filepath)
            clean_title = os.path.basename(raw_title)
            clean_title = os.path.splitext(clean_title)[0]

            metadata["title"] = clean_title

            # Store in vector DB
            self.vector_store.add_document(
                content=content,
                title=clean_title,
                metadata=metadata,
                embedding=embedding_array
            )

            stored_count += 1

        # --- Logging + return message ---
        doc_logger.info(f"'{filepath}' written to RAG database with {stored_count} chunks")
        return f"Finished loading {ext} into store ({stored_count} chunks)"
