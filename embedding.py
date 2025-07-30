import os
from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.docstore.document import Document

VECTOR_STORE_PATH = "faiss_index"

def load_or_create_vector_store(chunks, model_name="mxbai-embed-large:335m"):
    """
    Loads an existing FAISS store or creates one from provided chunks.
    Accepts List[Document] and stores them using Ollama embeddings.
    """
    if not chunks or not isinstance(chunks[0], Document):
        raise ValueError("Chunks must be a non-empty list of LangChain Document objects.")

    embedding_model = OllamaEmbeddings(model=model_name)

    if os.path.exists(VECTOR_STORE_PATH):
        try:
            vector_store = FAISS.load_local(
                VECTOR_STORE_PATH,
                embedding_model,
                allow_dangerous_deserialization=True
            )
            print("✅ Loaded existing FAISS store")
            vector_store.add_documents(chunks)
            print(f"➕ Added {len(chunks)} chunks to FAISS store")
        except Exception as e:
            print(f"⚠️ Failed to load store, creating fresh one: {e}")
            vector_store = FAISS.from_documents(chunks, embedding_model)
    else:
        vector_store = FAISS.from_documents(chunks, embedding_model)
        print(f"🆕 Created new FAISS store with {len(chunks)} chunks")

    vector_store.save_local(VECTOR_STORE_PATH)
    print(f"💾 FAISS store saved to '{VECTOR_STORE_PATH}'")

    return vector_store
