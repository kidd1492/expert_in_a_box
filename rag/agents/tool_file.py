# agents/tool_file.py
from langchain_ollama import OllamaEmbeddings
import wikipedia as wk
import numpy as np
from utils.log_handler import project_logger, app_logger
from services.ingestion_service import IngestionService
from services.retrieval_service import RetrievalService

ingestion_service = IngestionService()
retrieval_service = RetrievalService()


def wiki_search(term):
    """This function will gather research information from wikipedia and append it it wikiSearch.txt"""
    project_logger.info(f".tool_call : wiki_search search_term: {term} \n")
    try:
        page = wk.page(term)
        response = page.content
        output_file = f"{term}.txt"
        with open(output_file, 'a', encoding='UTF-8') as file:
            file.write(response)
    except wk.exceptions.DisambiguationError:
        response = f"Multiple options found for '{term}'. Please specify."
    except wk.exceptions.PageError:
        response = f"No Wikipedia page found for '{term}'"

    return "response saved to wikiSearch.txt"


def retriever_tool(query: str, search_type: str = "similarity") -> str:
    """Query the vectorstore to retrieve similarity or mmr search_type."""
    project_logger.info(f".tool_call : retriever_tool with search_type={search_type} query: {query}\n")
    results = retrieval_service.retrieve(query, search_type=search_type, top_k=3)
    if not results:
        return "I found no relevant information."
    return "\n\n".join([f"Document {i+1}:\n{content}" for i, (content, _) in enumerate(results)])


def add_file(filepath: str) -> str:
    """Loads a PDF, TXT, or MD file into the SQLite-backed RAG store."""
    project_logger.info(f".tool_call : add_file\n")
    try:
        return ingestion_service.add_file(filepath)
    except Exception as e:
        return f"Error loading file: {e}"
