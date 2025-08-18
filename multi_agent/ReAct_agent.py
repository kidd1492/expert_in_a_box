from typing import Annotated, Sequence, TypedDict
from langchain_core.messages import BaseMessage, SystemMessage, HumanMessage
from langchain_ollama import ChatOllama
from langchain_core.tools import tool
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain_community.vectorstores import FAISS
import wikipedia as wk


class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]


# ========== FAISS Vector Store Setup ==========
def load_vector_store(index_path="C:/Users/chris/Desktop/expert_in_a_box/RAG_system/faiss_index", embedding_model_name="mxbai-embed-large:335m"):
    embeddings = OllamaEmbeddings(model=embedding_model_name)
    vector_store = FAISS.load_local(index_path, embeddings, allow_dangerous_deserialization=True)
    print("FAISS store loaded successfully!")
    return vector_store



@tool
def wiki_search(term):
    """This function will gather research information from wikipedia and append it it wikiSearch.txt"""
    try:
        page = wk.page(term)
        response = page.content
        print(response)
        with open("output.txt", "a", encoding="utf-8") as output:
            output.write(f"\nwiki_search: {response} \n")
    except wk.exceptions.DisambiguationError:
        response = f"Multiple options found for '{term}'. Please specify."
    except wk.exceptions.PageError:
        response = f"No Wikipedia page found for '{term}'"

    return "response saved to wikiSearch.txt"


@tool
def retriever_tool(query: str) -> str:
    """Tool that queries FAISS-indexed documents."""
    VECTOR_STORE_PATH = "C:/Users/chris/Desktop/expert_in_a_box/RAG_system/faiss_index"
    EMBED_MODEL = "mxbai-embed-large:335m"
    vectorstore = load_vector_store(index_path=VECTOR_STORE_PATH, embedding_model_name=EMBED_MODEL)
    retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 5})
    docs = retriever.invoke(query)
    with open("output.txt", "a", encoding="utf-8") as output:
        output.write("\n".join([f"Document {i+1}:\n{doc.page_content}" for i, doc in enumerate(docs)]))
    if not docs:
        return "I found no relevant information."

    return "\n\n".join([f"Document {i+1}:\n{doc.page_content}" for i, doc in enumerate(docs)])



tools = [wiki_search, retriever_tool]

model = ChatOllama(model='llama3.2:3b').bind_tools(tools)


def model_call(state: AgentState) -> AgentState:
    system_prompt = SystemMessage(content="""You are an researcher with these tools:tools = [wiki_search, retriever_tool], based on the following Topic:
    1. - use the retreiver_tool to exicute query about langgraph. -limit 2. 
    2. - use the wikiSearch tool to exicute searches for additonal information. limit 2.
    3. - use the information to write a draft blog post on the Topic: """)
    input_messages = [system_prompt] + state["messages"]
    with open("output.txt", "a", encoding="utf-8") as output:
        output.write(f"\nInput Message: {input_messages}\n")
    response = model.invoke(input_messages)
    with open("output.txt", "a", encoding="utf-8") as output:
        output.write(f"\nfinal output: {response.content}\n")
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



with open("graph.png", "wb") as f:
    f.write(app.get_graph().draw_mermaid_png())


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
def running_agent(outline):
    print("Agent Ready")
    user_input = outline
    inputs = {"messages": [HumanMessage(content=user_input)]}
    result = app.invoke(inputs)
    return result['messages'][-1].content

