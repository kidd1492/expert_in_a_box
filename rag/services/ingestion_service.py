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
        chunks, ext_or_error = read_document(filepath)
        if chunks is None:
            error_logger.error("No Chuncks to process")
            return ext_or_error  # error message

        embedded = embed_documents(chunks)
        stored_count = 0

        for content, metadata, embedding_array in embedded:
            raw_title = metadata.get("title")
            clean_title = os.path.basename(raw_title)          # Backpropagation.txt
            clean_title = os.path.splitext(clean_title)[0]     # Backpropagation

            metadata["title"] = clean_title
            metadata_json = json.dumps(metadata)

            self.vector_store.add_document(content, clean_title, metadata_json, embedding_array)

        doc_logger.info(f"\'{filepath}\' written to RAG database with {stored_count} chunks")
        return f"Finished Loading {ext_or_error} into Store ({stored_count} chunks)"
