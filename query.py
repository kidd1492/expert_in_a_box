from langchain_community.vectorstores import FAISS
from langchain_ollama import OllamaEmbeddings
from langchain.chains import RetrievalQA
from langchain_community.llms import Ollama

# Load FAISS vector store from disk
def load_vector_store(index_path="faiss_index", embedding_model_name="mxbai-embed-large:335m"):
    embeddings = OllamaEmbeddings(model=embedding_model_name)
    vector_store = FAISS.load_local(index_path, embeddings, allow_dangerous_deserialization=True)
    return vector_store

# Build QA chain and run query
def run_query(query, index_path="faiss_index", llm_model="llama3.2:3b", embedding_model="mxbai-embed-large:335m"):
    vector_store = load_vector_store(index_path, embedding_model)
    llm = Ollama(model=llm_model)

    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=vector_store.as_retriever(),
        chain_type="stuff"
    )

    return qa_chain.run(query)

# Example usage
if __name__ == "__main__":
    syllabus_prompt = "Based on this material, generate a syllabus with topic breakdowns for learning Machine Learning."
    response = run_query(syllabus_prompt)
    print(response)
