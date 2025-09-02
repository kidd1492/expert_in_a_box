from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage, RemoveMessage
from langgraph.graph import StateGraph, START, END, MessagesState
from langgraph.checkpoint.sqlite import SqliteSaver
import sqlite3


class AgentState(MessagesState):
    summary : str


db_path = "example.db"
conn = sqlite3.connect(db_path, check_same_thread=False)
memory = SqliteSaver(conn)
model = ChatOllama(model="personal:3b")


def human_node(state:AgentState) -> AgentState:
    user_input = input("Enter Your Question: ")
    return {"messages":[HumanMessage(content=user_input)]}


def should_continue(state:AgentState):
    if state['messages'][-1].content == "finished":
        return "end"
    else:
        return "chat_node"


def chat(state: AgentState):
    summary = state.get("summary", "")
    if summary:
        system_message = f"Summary of conversation earlier: {summary}"
        messages = [SystemMessage(content=system_message)] + state["messages"]
    else:
        messages = state["messages"]

    response = model.invoke(messages)
    print("\n", response)
    return {"messages": response}


def summary_node(state: AgentState):
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


def should_summarize(state: AgentState): #-> Literal ["summarize_conversation", "end"]:
    messages =  state["messages"]
    if len(messages) > 6:
        return "summarized"
    else:
        return "human"


graph = StateGraph(AgentState)

graph.add_node("human_node", human_node)
graph.add_node("chat", chat)
graph.add_node("summary_node", summary_node) 

graph.add_edge(START, "human_node")
graph.add_conditional_edges(
    "human_node",
    should_continue,
    {
        "end": END,
        "chat_node": "chat"
    }
)
graph.add_conditional_edges(
    "chat", 
    should_summarize, 
    {
        "summarized" : "summary_node",
        "human" : "human_node"
    }
)
graph.add_edge("summary_node", "human_node")
app = graph.compile(checkpointer=memory)

with open("graph.png", "wb") as f:
    f.write(app.get_graph().draw_mermaid_png())

config = {"configurable": {"thread_id": "1"}}
output = app.invoke({}, config)
print(f"\n\n{app.get_state(config).values.get("summary","")}\n\n")
for m in output['messages']:
    m.pretty_print()