
from langchain_core.messages import HumanMessage
from langchain_ollama import ChatOllama
from langgraph.graph import StateGraph, END, START, MessagesState
from langgraph.checkpoint.memory import MemorySaver


class AgentState(MessagesState):
    pass

model = ChatOllama(model='llama3.2:3b')
memory = MemorySaver()

def model_call(state: AgentState):
    messages = state["messages"]
    response = model.invoke(messages)
    return {"messages": response}


graph = StateGraph(AgentState)
graph.add_node('bot', model_call)
graph.add_edge(START, 'bot')
graph.add_edge('bot', END)
app = graph.compile(checkpointer=memory)

with open("chatbot_2.png", "wb") as f:
    f.write(app.get_graph().draw_mermaid_png())

config = {"configurable": {"thread_id": "1"}}

print("Agent Ready")
while True:
    user_input = input("Enter Question: ")
    if user_input.lower() in ["exit", "quit", "q"]:
        break

    output = app.invoke({"messages": [HumanMessage(content=user_input)]}, config) 
    for m in output['messages'][-1:]:
        m.pretty_print()
