# agents/tool_file.py
import wikipedia as wk


def wiki_search(term):
    """This function will gather research information from wikipedia and save it to a file."""
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
