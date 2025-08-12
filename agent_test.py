from typing import Annotated, Sequence, TypedDict
from langchain_core.messages import BaseMessage, SystemMessage, HumanMessage
from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain_core.tools import tool
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from langchain_community.vectorstores import FAISS
import wikipedia as wk

# ========== Agent State ==========
class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]


# ========== FAISS Vector Store Setup ==========
def load_vector_store(index_path="testing/faiss_index", embedding_model_name="mxbai-embed-large:335m"):
    embeddings = OllamaEmbeddings(model=embedding_model_name)
    vector_store = FAISS.load_local(index_path, embeddings, allow_dangerous_deserialization=True)
    print("✅ FAISS store loaded successfully!")
    return vector_store

# ========== Tools ==========
@tool
def wiki_search(term):
    """Search Wikipedia and save content to wikiSearch.txt"""
    print(f"wiki_search tool called with {term}")
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
def retriever_tool(query: str) -> str:
    """Query FAISS-indexed documents."""
    print(f"retriever tool called with {query}")
    vectorstore = load_vector_store()
    retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 5})
    docs = retriever.invoke(query)
    if not docs:
        return "I found no relevant information."
    return "\n\n".join([f"Document {i+1}:\n{doc.page_content}" for i, doc in enumerate(docs)])

tools = [wiki_search, retriever_tool]

# ========== Models ==========
model = ChatOllama(model='llama3.2:3b').bind_tools(tools)
manager_model = ChatOllama(model='llama3.2:3b')


# ========== LangGraph ==========
graph = StateGraph(AgentState)

app = graph.compile()

# Optional: Save graph visualization
with open("graph.png", "wb") as f:
    f.write(app.get_graph().draw_mermaid_png())



# ========== Run Agent ==========
def running_agent():
    # Run summary once
    state = app.invoke({})
    

    while True:
        user_input = input("\n📥 Question: ")
        if user_input.lower() in ["exit", "quit"]:
            break
        state["messages"].append(HumanMessage(content=user_input))
        

running_agent()
