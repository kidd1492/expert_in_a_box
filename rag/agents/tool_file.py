# agents/tool_file.py
import os
import wikipedia as wk
from rag.utils.log_handler import tool_logger


def wiki_search(term):
    """This function will gather research information from wikipedia and save it to a file."""
    tool_logger.info(f".tool_call : wiki_search search_term: {term}")
    os.makedirs("rag/data/wiki", exist_ok=True)
    try:
        page = wk.page(term)
        response = page.content
    except wk.exceptions.DisambiguationError:
        print(f"Multiple options found for '{term}'. Please specify.")
        response = f"Multiple options found for '{term}'. Please specify."
    except wk.exceptions.PageError:
        print(f"No Wikipedia page found for '{term}'")
        response = f"No Wikipedia page found for '{term}'"
    return response
