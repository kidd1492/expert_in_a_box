from typing import Annotated, Sequence, TypedDict
from dotenv import load_dotenv
from langchain_core.messages import BaseMessage, SystemMessage, HumanMessage
from langchain_ollama import ChatOllama
from langchain_core.tools import tool
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
import os, requests, json
from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain_community.vectorstores import FAISS
from data_ingestion import read_document
import wikipedia as wk


load_dotenv()


class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]


# ========== FAISS Vector Store Setup ==========
def load_vector_store(index_path="faiss_index", embedding_model_name="mxbai-embed-large:335m"):
    embeddings = OllamaEmbeddings(model=embedding_model_name)
    vector_store = FAISS.load_local(index_path, embeddings, allow_dangerous_deserialization=True)
    print("✅ FAISS store loaded successfully!")
    return vector_store



@tool
def wiki_search(term):
    """This function will gather research information from wikipedia and append it it wikiSearch.txt"""
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
    """Tool that queries FAISS-indexed documents."""
    VECTOR_STORE_PATH = "faiss_index"
    EMBED_MODEL = "mxbai-embed-large:335m"
    vectorstore = load_vector_store(index_path=VECTOR_STORE_PATH, embedding_model_name=EMBED_MODEL)
    retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 3})
    docs = retriever.invoke(query)
    if not docs:
        return "I found no relevant information."

    return "\n\n".join([f"Document {i+1}:\n{doc.page_content}" for i, doc in enumerate(docs)])



@tool
def add_file(filepath):
    """This is a function to load a PDF or txt file into the FAISS vectorstore rag system"""
    read_document(filepath)
    return "loaded file into store"



tools = [add_file, wiki_search, retriever_tool]

model = ChatOllama(model='personal:3b').bind_tools(tools)


def model_call(state: AgentState) -> AgentState:
    system_prompt = SystemMessage(content="You are an assistant, please answer my query to the best of your ability.")
    input_messages = [system_prompt] + state["messages"]
    response = model.invoke(input_messages)
    return {"messages": [response]}


def should_continue(state: AgentState):
    messages = state["messages"]
    last_message = messages[-1]
    return "continue" if getattr(last_message, "tool_calls", None) else "end"


graph = StateGraph(AgentState)
graph.add_node("our_agent", model_call)
graph.add_node("tools", ToolNode(tools=tools))

graph.set_entry_point("our_agent")

graph.add_conditional_edges(
    "our_agent",
    should_continue,
    {
        "continue": "tools",
        "end": END,
    },
)

graph.add_edge("tools", "our_agent")

app = graph.compile()


def print_stream(stream):
    for s in stream:
        messages = s.get("messages", [])
        if messages:
            last = messages[-1]
            try:
                last.pretty_print()
            except AttributeError:
                print(last)



# ========== Run Agent Loop ==========
def running_agent():
    print("💡 RAG Agent Ready")
    while True:
        user_input = input("\n📥 Question: ")
        if user_input.lower() in ["exit", "quit"]:
            break
        inputs = {"messages": [HumanMessage(content=user_input)]}
        print_stream(app.stream(inputs, stream_mode="values"))



running_agent()