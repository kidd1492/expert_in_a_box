from typing import Literal
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, AIMessage, RemoveMessage, SystemMessage
from langgraph.graph import START, StateGraph, END, MessagesState
from langgraph.checkpoint.memory import MemorySaver

class State(MessagesState):
    summary: str

model = ChatOllama(model="llama3.2:3b")


def call_model(state: State):
    summary = state.get("summary", "")
    if summary:
        system_message = f"Summary of conversation earlier: {summary}"
        messages = [SystemMessage(content=system_message)] + state["messages"]
    else:
        messages = state["messages"]

    response = model.invoke(messages)
    return {"messages": response}


def summarize_conversation(state: State):
    summary = state.get("summary", "")
    if summary:
        summary_message =(
            f"This is a summary of the conversation to date: {summary}\n\n"
            "Extend the summary by taking into account the new messages above:"
        )
    else:
        summary_message = "Create a summary of the conversation above: "

    messages =  state["messages"] + [HumanMessage(content=summary_message)]
    response = model.invoke(messages)

    delete_messages = [RemoveMessage(id=m.id) for m in state["messages"][:-2]]
    return {"summary": response.content, "messages": delete_messages}


def should_continue(state: State): #-> Literal ["summarize_conversation", "end"]:
    messages =  state["messages"]
    if len(messages) > 6:
        return "summarized"
    else:
        return "end"


builder = StateGraph(State)
builder.add_node("conversation", call_model)
builder.add_node("summarize_conversation", summarize_conversation)

builder.add_edge(START, "conversation")
builder.add_conditional_edges(
    "conversation",
    should_continue,
    {
        "summarized": "summarize_conversation",
        "end": END,
    }
)
builder.add_edge("summarize_conversation", END)

memory = MemorySaver()
app = builder.compile(checkpointer=memory)

with open("summarizing_chat.png", "wb") as f:
    f.write(app.get_graph().draw_mermaid_png())

# Create a thread
config = {"configurable": {"thread_id": "1"}}

# Start conversation
input_message = HumanMessage(content="hi! I'm Lance")
output = app.invoke({"messages": [input_message]}, config) 
for m in output['messages'][-1:]:
    m.pretty_print()

input_message = HumanMessage(content="what's my name?")
output = app.invoke({"messages": [input_message]}, config) 
for m in output['messages'][-1:]:
    m.pretty_print()

input_message = HumanMessage(content="i like the 49ers!")
output = app.invoke({"messages": [input_message]}, config) 
for m in output['messages'][-1:]:
    m.pretty_print()


print(f"\n\n{app.get_state(config).values.get("summary","")}\n\n")

input_message = HumanMessage(content="i like Nick Bosa, isn't he the highest paid defensive player?")
output = app.invoke({"messages": [input_message]}, config) 
for m in output['messages'][-1:]:
    m.pretty_print()

print(f"\n\n{app.get_state(config).values.get("summary","")}")