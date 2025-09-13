import json
import numpy as np
from langchain_ollama import OllamaEmbeddings
from langchain.docstore.document import Document
from core.vectors import RAGDatabase  # Your new class-based DB module

# Initialize embedding model and database
EMBED_MODEL = "mxbai-embed-large:335m"
embedding_model = OllamaEmbeddings(model=EMBED_MODEL)
db = RAGDatabase()

def load_or_create_vector_store(chunks: list[Document], model_name: str = EMBED_MODEL) -> str:
    """
    Loads an existing vector store or creates one from provided chunks.
    Accepts List[Document] and stores them using Ollama embeddings.
    """
    if not chunks or not isinstance(chunks[0], Document):
        raise ValueError("Chunks must be a non-empty list of LangChain Document objects.")

    stored_count = 0

    for chunk in chunks:
        content = chunk.page_content.strip()
        metadata = chunk.metadata or {}
        title = metadata.get("title", "")
        metadata_json = json.dumps(metadata)

        # Generate embedding
        embedding = embedding_model.embed_query(content)
        embedding_array = np.array(embedding, dtype=np.float32)

        # Store in database
        db.add_document(content, title, metadata_json, embedding_array)
        stored_count += 1

    print(f"Stored {stored_count} chunks with embeddings.")
    return f"Stored {stored_count} chunks with embeddings."
