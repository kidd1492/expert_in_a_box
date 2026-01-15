from utils.log_handler import app_logger, project_logger
from langchain_ollama import OllamaEmbeddings
from core.data_ingestion import read_document
import wikipedia as wk
from langchain_core.tools import tool
import numpy as np
from agents.vectors import VectorStore


vectors = VectorStore()

EMBED_MODEL = "mxbai-embed-large:335m"
embedding_model = OllamaEmbeddings(model=EMBED_MODEL)


@tool
def wiki_search(term):
    """This function will gather research information from wikipedia and append it it wikiSearch.txt"""
    project_logger.info(f".tool_call : wiki_search search_term: {term} \n")
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
    '''This function is used to query the vectorstore to retreive similarity or mmr search_type'''
    project_logger.info(f".tool_call : retriever_tool with search_type={search_type} query: {query}\n")
    query_embedding = np.array(embedding_model.embed_query(query), dtype=np.float32)
    results = vectors.query_documents(query_embedding, search_type)

    if not results:
        return "I found no relevant information."
    print("\n\n".join([f"Document {i+1}:\n{content}" for i, (content, _) in enumerate(results)]))
    return "\n\n".join([f"Document {i+1}:\n{content}" for i, (content, _) in enumerate(results)])


@tool
def add_file(filepath: str) -> str:
    """Loads a PDF, TXT, or MD file into the SQLite-backed RAG store."""
    project_logger.info(f".tool_call : add_file\n")
    result = read_document(filepath)
    print(result)
    return f"Successfully loaded '{filepath}' into RAG store."
    