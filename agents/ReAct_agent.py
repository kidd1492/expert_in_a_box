from typing import Annotated, Sequence, TypedDict
from dotenv import load_dotenv
from langchain_core.messages import BaseMessage, SystemMessage, HumanMessage
from langchain_ollama import ChatOllama
from langchain_core.tools import tool
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
import os, requests, json


load_dotenv()
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
ZIP_CODE = "45140"  # You can override this as needed

class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]


@tool
def add(a: int, b: int):
    """This is a function to add two numbers together"""
    return a + b


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

tools = [add, get_weather]

model = ChatOllama(model='llama3.2:3b').bind_tools(tools)


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


inputs = {"messages": [HumanMessage(content="what is the weather like today? what would be something good to do outside today?")]}
print_stream(app.stream(inputs, stream_mode="values"))
