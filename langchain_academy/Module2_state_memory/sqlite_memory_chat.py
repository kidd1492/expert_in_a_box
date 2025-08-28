import sqlite3
from langgraph.checkpoint.sqlite import SqliteSaver
from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage, RemoveMessage
from langgraph.graph import END, START, MessagesState, StateGraph

db_path = "example.db"
conn = sqlite3.connect(db_path, check_same_thread=False)
memory = SqliteSaver(conn)
model = ChatOllama(model="qwen2.5:3b")


class State(MessagesState):
    summary: str


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
app = builder.compile(checkpointer=memory)

with open("sqlite_memory_chat.png", "wb") as f:
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
