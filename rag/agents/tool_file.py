# agents/tool_file.py
import wikipedia as wk
from utils.log_handler import tool_logger
from services.ingestion_service import IngestionService
from services.retrieval_service import RetrievalService

ingestion_service = IngestionService()
retrieval_service = RetrievalService()


def wiki_search(term):
    """This function will gather research information from wikipedia and save it to a file."""
    tool_logger.info(f".tool_call : wiki_search search_term: {term}")
    try:
        page = wk.page(term)
        response = page.content
        new_term = term.replace(" ", "_")
        output_file = f"{new_term}.txt"
        with open(output_file, 'a', encoding='UTF-8') as file:
            file.write(response)
    except wk.exceptions.DisambiguationError:
        print(f"Multiple options found for '{term}'. Please specify.")
        response = f"Multiple options found for '{term}'. Please specify."
    except wk.exceptions.PageError:
        print(f"No Wikipedia page found for '{term}'")
        response = f"No Wikipedia page found for '{term}'"

    return f"response saved to {new_term}.txt"


def retriever_tool(query: str, search_type: str = "similarity") -> str:
    """Query the vectorstore to retrieve similarity or mmr search_type."""
    tool_logger.info(f".tool_call : retriever_tool with search_type={search_type} query: {query}")
    results = retrieval_service.retrieve(query, search_type=search_type, top_k=3)
    if not results:
        return "I found no relevant information."
    print("\n\n".join([f"Document {i+1}:\n{content}" for i, (content, _) in enumerate(results)]))
    return "\n\n".join([f"Document {i+1}:\n{content}" for i, (content, _) in enumerate(results)])


def add_file(filepath: str) -> str:
    """Loads a PDF, TXT, or MD file into the SQLite-backed RAG store."""
    tool_logger.info(f".tool_call : add_file file_name : {filepath}")
    try:
        return ingestion_service.add_file(filepath)
    except Exception as e:
        return f"Error loading file: {e}"
