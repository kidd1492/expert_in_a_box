from utils.log_handler import app_logger, project_logger
from langchain_ollama import OllamaEmbeddings
from core.data_ingestion import read_document
import wikipedia as wk
from langchain_core.tools import tool
import numpy as np
from core.vectors import RAGDatabase
from langgraph.graph import MessagesState
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, RemoveMessage


db = RAGDatabase()

EMBED_MODEL = "mxbai-embed-large:335m"
embedding_model = OllamaEmbeddings(model=EMBED_MODEL)

class AgentState(MessagesState):
    summary : str
    thread_id : str

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
    results = db.query_documents(query_embedding, search_type)

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
    

tools = [add_file, wiki_search, retriever_tool]
model = ChatOllama(model='qwen2.5:3b').bind_tools(tools)

def should_continue(state:AgentState):
    if state['messages'][-1].content.lower() in ["exit", "quit", "q"]:
        thread_id = state.get("thread_id")
        summary = state.get("summary", "")
        messages = [m.content for m in state.get("messages", [])]
        db.save_memory(thread_id, summary, messages)
        project_logger.info(f"Session finalized and memory saved. Thread_id: {thread_id}")
        return "end"
    elif len(state["messages"]) > 6:
        return "summarized"
    else:
        return "chat"


def summary_node(state: AgentState):
    summary = state.get("summary", "")
    if summary:
        summary_message =(
            f"This is a summary of the conversation to date: {summary}\n\n"
            "Extend the summary by taking into account the new messages above:"
        )
    else:
        summary_message = "Create a summary of the conversation above: "

    messages =  state["messages"] + [HumanMessage(content=summary_message)]
    response = model.invoke(messages)

    delete_messages = [RemoveMessage(id=m.id) for m in state["messages"][:-2]]
    db.save_memory(
        thread_id=state["thread_id"],
        summary=response.content,
        messages=[m.content for m in state["messages"][-2:]]
    )
    project_logger.info(f"Session summarized and memory saved. Thread_id: {state["thread_id"]}")
    return {"summary": response.content, "messages": delete_messages}


def tools_condition(state: AgentState): 
    messages = state["messages"]
    last_message = messages[-1]
    return "continue" if getattr(last_message, "tool_calls", None) else "human"
