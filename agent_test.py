from typing import Annotated, Sequence, TypedDict

from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.messages import BaseMessage, SystemMessage, HumanMessage
from langchain_ollama import ChatOllama
from langchain_core.tools import tool

from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, END, START
from langgraph.prebuilt import ToolNode

import wikipedia as wk


# ===== Agent State =====
class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]

# ===== FAISS Vector Store Setup =====
def load_vector_store(index_path="testing/faiss_index", embedding_model_name="mxbai-embed-large:335m"):
    embeddings = OllamaEmbeddings(model=embedding_model_name)
    vector_store = FAISS.load_local(index_path, embeddings, allow_dangerous_deserialization=True)
    print("✅ FAISS store loaded successfully!")
    return vector_store

# ===== Tools =====
@tool
def wiki_search(term: str) -> str:
    """Search Wikipedia for a given term."""
    try:
        page = wk.summary(term)
        return page
    except wk.exceptions.DisambiguationError:
        return f"Multiple options found for '{term}'. Please specify."
    except wk.exceptions.PageError:
        return f"No Wikipedia page found for '{term}'"

@tool
def retriever_tool(query: str) -> str:
    """Query FAISS-indexed documents."""
    VECTOR_STORE_PATH = "testing/faiss_index"
    EMBED_MODEL = "mxbai-embed-large:335m"
    vectorstore = load_vector_store(index_path=VECTOR_STORE_PATH, embedding_model_name=EMBED_MODEL)
    retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 5})
    docs = retriever.invoke(query)
    if not docs:
        return "No relevant documents found."
    return "\n\n".join([f"Doc {i+1}:\n{doc.page_content}" for i, doc in enumerate(docs)])

tools = [wiki_search, retriever_tool]

# ===== Models =====
init_model = ChatOllama(model='llama3.2:3b')
tool_model = ChatOllama(model='llama3.2:3b').bind_tools(tools)

# ===== Nodes =====
def init_model_call(state: AgentState) -> AgentState:
    print("🔧 init_model_call")
    system_prompt = SystemMessage(content="""You are an assistant. Given a user question, generate a json type response:
                                    {'outline: An outline for a tutorial-style blog post, 
                                     'search_terms: A list of search terms to look up""")
    
    input_messages = [system_prompt] + state["messages"]
    response = init_model.invoke(input_messages)
    
    return {"messages": state["messages"] + [response]}

def tool_model_call(state: AgentState) -> AgentState:
    print("🔧 tool_model_call")
    system_prompt = SystemMessage(content="""You are a tool-using assistant. If search terms are present, use the tools to gather information.
                                        Use:
                                        - `retriever_tool` for LangChain/LangGraph topics
                                        - `wiki_search` for general topics

                                        After gathering info, write a tutorial-style blog post using the retrieved content.""")
    input_messages = [system_prompt] + state["messages"]
    response = tool_model.invoke(input_messages)
    return {"messages": state["messages"] + [response]}


def should_continue(state: AgentState):
    print("enter should continue")
    print(state["messages"], "\n\n")

    last_message = state["messages"][-1]
    print(last_message)

    tool_calls = getattr(last_message, "tool_calls", None) or last_message.additional_kwargs.get("tool_calls", None)
    return "continue" if tool_calls else "end"


# ===== Graph Setup =====
graph = StateGraph(AgentState)

graph.add_node("init_agent", init_model_call)
graph.add_node("tool_agent", tool_model_call)
graph.add_node("tools", ToolNode(tools=tools))

graph.add_edge(START, "init_agent")
graph.add_edge("init_agent", "tool_agent")

graph.add_conditional_edges(
    "tool_agent",
    should_continue,
    {
        "continue": "tools",
        "end": END,
    },
)

graph.add_edge("tools", "tool_agent")

app = graph.compile()

# Optional: Save graph visualization
with open("graph.png", "wb") as f:
    f.write(app.get_graph().draw_mermaid_png())


# ===== Run Agent Loop =====
def running_agent():
    print("💡 Agent Ready")
    user_input = input("\n📥 Question: ")    
    inputs = {"messages": [HumanMessage(content=user_input)]}
    app.invoke(inputs)

running_agent()
