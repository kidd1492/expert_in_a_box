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
from data_ingestion import load_pdf


load_dotenv()
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
ZIP_CODE = "45140"  # You can override this as needed

class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]


# ========== FAISS Vector Store Setup ==========
def load_vector_store(index_path="faiss_index", embedding_model_name="mxbai-embed-large:335m"):
    embeddings = OllamaEmbeddings(model=embedding_model_name)
    vector_store = FAISS.load_local(index_path, embeddings, allow_dangerous_deserialization=True)
    print("✅ FAISS store loaded successfully!")
    return vector_store

VECTOR_STORE_PATH = "faiss_index"
EMBED_MODEL = "mxbai-embed-large:335m"
vectorstore = load_vector_store(index_path=VECTOR_STORE_PATH, embedding_model_name=EMBED_MODEL)
retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 3})

@tool
def retriever_tool(query: str) -> str:
    """Tool that queries FAISS-indexed documents."""
    docs = retriever.invoke(query)
    if not docs:
        return "I found no relevant information."

    return "\n\n".join([f"Document {i+1}:\n{doc.page_content}" for i, doc in enumerate(docs)])



@tool
def add_pdf(filepath):
    """This is a function for adding data ingestion for rag system"""
    load_pdf(filepath)
    return "loaded pdf"


#Get real-time weather from OpenWeather API
@tool
def get_weather(zip_code=ZIP_CODE, units="imperial") -> dict:
    '''A funtion to fetch weather data from API'''
    response = requests.get(
        f"https://api.openweathermap.org/data/2.5/weather?zip={zip_code}&appid={WEATHER_API_KEY}&units={units}"
    )
    if response.status_code != 200:
        raise Exception(f"Failed to fetch weather: {response.status_code}")
    return response.json()

tools = [load_pdf, get_weather, retriever_tool]

model = ChatOllama(model='qwen3:1.7b').bind_tools(tools)


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