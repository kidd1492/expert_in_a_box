from langchain_community.vectorstores import FAISS
from langchain_ollama import OllamaEmbeddings


embedding_model = OllamaEmbeddings(model="qwen2.5-coder:3b")
vector_store = FAISS.load_local("faiss_index", embedding_model, allow_dangerous_deserialization=True)

query = "The Forward-Forward algorithm "
retrieved_docs = vector_store.similarity_search(query, k=4, )

for i, doc in enumerate(retrieved_docs):
    print(f"\n--- Document {i+1} ---\n")
    print(doc.page_content[:500])
