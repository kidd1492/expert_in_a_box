# services/ingestion_service.py
from rag.rag_system.data_ingestion import read_document
from rag.rag_system.embedding import embed_documents
from rag.rag_system.vectors import VectorStore
from rag.logging.log_handler import doc_logger
from rag.rag_system.chunking import chunk_text, get_metadata
from utils.helper_functions import delete_ingest_file


class IngestionService:
    def __init__(self, vector_store: VectorStore | None = None):
        self.vector_store = vector_store or VectorStore()

    def add_file(self, file_path: str) -> str:
        text = read_document(file_path) # -> str raw text
        chunks = chunk_text(text) # -> List[Document]
        meta_chunks = get_metadata(chunks, file_path) # -> List[dict]
        embedded = embed_documents(meta_chunks) # -> list[dict]

        # --- Store each embedded chunk ---
        for record in embedded:
            content = record["content"]
            metadata = record["metadata"]
            embedding_array = record["embedding"]
            title = metadata.get("title", file_path)

            # Store in vector DB
            self.vector_store.add_document(
                content=content,
                title=title,
                metadata=metadata,
                embedding=embedding_array
            )

        # --- Logging + return message ---
        doc_logger.info(f"'{file_path}' written to RAG database")
        return f"Finished loading {title} into store)"


    def remove_file(self, titles):
        titles = titles.split(",")
        delete_ingest_file(titles)
        return self.vector_store.remove_file(titles)
