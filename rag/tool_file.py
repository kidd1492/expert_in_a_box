from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain_community.vectorstores import FAISS
from data_ingestion import read_document
import wikipedia as wk
from langchain_core.tools import tool


# ========== FAISS Vector Store Setup ==========
def load_vector_store(index_path="faiss_index", embedding_model_name="mxbai-embed-large:335m"):
    embeddings = OllamaEmbeddings(model=embedding_model_name)
    vector_store = FAISS.load_local(index_path, embeddings, allow_dangerous_deserialization=True)
    print("FAISS store loaded successfully!")
    return vector_store


@tool
def wiki_search(term):
    """This function will gather research information from wikipedia and append it it wikiSearch.txt"""
    print(f".tool_call : wiki_search search_term: {term} \n")
    try:
        page = wk.page(term)
        response = page.content
        with open('wikiSearch.txt', 'a', encoding='UTF-8') as file:
            file.write(response)
    except wk.exceptions.DisambiguationError:
        response = f"Multiple options found for '{term}'. Please specify."
    except wk.exceptions.PageError:
        response = f"No Wikipedia page found for '{term}'"

    return "response saved to wikiSearch.txt"


@tool
def retriever_tool(query: str, search_type: str = "similarity") -> str:
    """Tool that queries FAISS-indexed documents using specified search type.
    Use 'mmr' for diverse results, or 'similarity' for most relevant matches."""

    print(f".tool_call : retriever_tool with search_type={search_type} query: {query}\n")
    
    VECTOR_STORE_PATH = "faiss_index"
    EMBED_MODEL = "mxbai-embed-large:335m"
    vectorstore = load_vector_store(index_path=VECTOR_STORE_PATH, embedding_model_name=EMBED_MODEL)

    # Conditional search_kwargs based on search_type
    search_kwargs = {"k": 3}
    if search_type == "mmr":
        search_kwargs["lambda_mult"] = 0.7  # Controls relevance vs diversity

    retriever = vectorstore.as_retriever(
        search_type=search_type,
        search_kwargs=search_kwargs
    )

    docs = retriever.invoke(query)
    if not docs:
        return "I found no relevant information."
    
    print("\n\n".join([f"Document {i+1}:\n{doc.page_content}" for i, doc in enumerate(docs)]))
    return "\n\n".join([f"Document {i+1}:\n{doc.page_content}" for i, doc in enumerate(docs)])



@tool
def add_file(filepath):
    """This is a function to load a PDF or txt file into the FAISS vectorstore"""
    print(f".tool_call : add file \n")
    read_document(filepath)
    return "loaded file into store"
