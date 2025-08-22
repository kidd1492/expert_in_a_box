from dotenv import load_dotenv
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_ollama import ChatOllama
from langchain_core.tools import tool
from langgraph.graph import StateGraph, END, MessagesState
import os, requests
from langgraph.prebuilt import tools_condition, ToolNode

load_dotenv()

WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
ZIP_CODE = "45205"  # You can override this as needed

class AgentState(MessagesState):
    pass


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
model = ChatOllama(model='qwen2.5:3b').bind_tools(tools)


def model_call(state: AgentState) -> AgentState:
    system_prompt = SystemMessage(content="You are an assistant, please answer my query to the best of your ability.")
    input_messages = [system_prompt] + state["messages"]
    response = model.invoke(input_messages)
    return {"messages": [response]}


graph = StateGraph(AgentState)
graph.add_node("our_agent", model_call)
graph.add_node("tools", ToolNode(tools=tools))

graph.set_entry_point("our_agent")
graph.add_conditional_edges("our_agent", tools_condition)
graph.add_edge("tools", "our_agent")

app = graph.compile()

# Optional: Save graph visualization
with open("ReAct_agent.png", "wb") as f:
    f.write(app.get_graph().draw_mermaid_png())


print("Agent Ready")
while True:
    user_input = input("Enter Question: ")
    if user_input.lower() in ["exit", "quit", "q"]:
        break

    output = app.invoke({"messages": [HumanMessage(content=user_input)]}) 
    for m in output['messages']:
        m.pretty_print()
