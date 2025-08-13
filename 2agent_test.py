from typing import Annotated, Sequence, TypedDict
from langchain_core.messages import BaseMessage, SystemMessage, HumanMessage, AIMessage
from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain_core.tools import tool
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, END, START
from langchain_community.vectorstores import FAISS
import wikipedia as wk
import re

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
def wiki_search(term: str) -> str:
    print(f"🔍 wiki_search tool called with: {term}")
    try:
        page = wk.page(term)
        response = page.content
        with open('wikiSearch.txt', 'a', encoding='UTF-8') as file:
            file.write(response)
    except wk.exceptions.DisambiguationError:
        response = f"Multiple options found for '{term}'. Please specify."
    except wk.exceptions.PageError:
        response = f"No Wikipedia page found for '{term}'"
    return response

def retriever_tool(query: str) -> str:
    print(f"📚 retriever_tool called with: {query}")
    vectorstore = load_vector_store()
    retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 5})
    docs = retriever.invoke(query)
    if not docs:
        return "I found no relevant information."
    return "\n\n".join([f"Document {i+1}:\n{doc.page_content}" for i, doc in enumerate(docs)])

tools_dict = {
    "wiki_search": wiki_search,
    "retriever_tool": retriever_tool
}

# ========== Models ==========
initial_model = ChatOllama(model='llama3.2:3b')
tool_model = ChatOllama(model='llama3.2:3b')

# ========== Node Definitions ==========
def initial_model_call(state: AgentState) -> AgentState:
    print(f"📨 Initial agent received {len(state['messages'])} messages")
    system_prompt = SystemMessage(content=f"""You are an assistant. massage_number={len(state['messages'])} 
If massage_number=1 and one of these tools would help — tools = [wiki_search, retriever_tool] — then respond with format:
need tool: wiki_search [search terms] or need tool: retriever_tool [query]
If tools won't help, just answer the prompt.
If massage_number > 1, use the information to complete the task.""")
    input_messages = [system_prompt] + state["messages"]
    response = initial_model.invoke(input_messages)
    return {"messages": state["messages"] + [response]}

def tool_model_call(state: AgentState) -> AgentState:
    print(f"🔧 Tool agent received {len(state['messages'])} messages")
    last_message = state["messages"][-1]
    match = re.search(r"need tool:\s*(\w+)\s*\[(.+?)\]", last_message.content)
    if match:
        tool_name, arg = match.groups()
        tool_func = tools_dict.get(tool_name)
        if tool_func:
            result = tool_func(arg)
            return {"messages": state["messages"] + [AIMessage(content=result)]}
    return {"messages": state["messages"] + [AIMessage(content="⚠️ Tool request not understood.")]}

def initial_should_continue(state: AgentState):
    last_message = state["messages"][-1]
    if "need tool:" in last_message.content:
        return "needs_tool"
    else:
        return "end"

# ========== LangGraph ==========
graph = StateGraph(AgentState)

graph.add_node("initial_agent", initial_model_call)
graph.add_node("tool_agent", tool_model_call)

graph.add_edge(START, "initial_agent")

graph.add_conditional_edges(
    "initial_agent",
    initial_should_continue,
    {
        "needs_tool": "tool_agent",
        "end": END
    }
)

graph.add_edge("tool_agent", "initial_agent")

app = graph.compile()

# Optional: Save graph visualization
with open("graph.png", "wb") as f:
    f.write(app.get_graph().draw_mermaid_png())

# ========== Run Agent ==========
def running_agent():
    state = {"messages": []}
    while True:
        user_input = input("\n📥 Question: ")
        if user_input.lower() in ["exit", "quit"]:
            break
        state["messages"].append(HumanMessage(content=user_input))
        state = app.invoke(state)
        print("\n🧠 Final Response:")
        print(state["messages"][-1].content)

# Uncomment to run
running_agent()
