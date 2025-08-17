from typing import Annotated, Sequence, TypedDict
from langchain_core.messages import BaseMessage, SystemMessage, HumanMessage, AIMessage
from langchain_ollama import ChatOllama
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, END, START

class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]

model = ChatOllama(model='llama3.2:3b')

def model_call(state: AgentState) -> AgentState:
    system_prompt = SystemMessage(content="You are an assistant, please answer my query to the best of your ability.")
    input_messages = [system_prompt] + state["messages"]
    response = model.invoke(input_messages)
    state["messages"].append(response)
    print(f"\nAI: {response.content}")
    return {"messages": state["messages"]}

graph = StateGraph(AgentState)
graph.add_node('Agent', model_call)
graph.add_edge(START, 'Agent')
graph.add_edge('Agent', END)
agent = graph.compile()

conversation_history: Sequence[BaseMessage] = []

print("Agent Ready")
while True:
    user_input = input("Enter Question: ")
    if user_input.lower() in ["exit", "quit", "q"]:
        break

    conversation_history.append(HumanMessage(content=user_input))
    inputs = {"messages": conversation_history}
    result = agent.invoke(inputs)
    conversation_history = result["messages"]
