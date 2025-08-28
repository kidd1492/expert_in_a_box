from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langgraph.graph import StateGraph, START, END, MessagesState
from langgraph.checkpoint.sqlite import SqliteSaver
import sqlite3


class AgentState(MessagesState):
    tokens: int


db_path = "example.db"
conn = sqlite3.connect(db_path, check_same_thread=False)
memory = SqliteSaver(conn)
model = ChatOllama(model="personal:3b")


def human_node(state:AgentState) -> AgentState:
    user_input = input("Enter Your Question: ")
    print(f"length user input: {len(user_input)}")
    return {"messages":[HumanMessage(content=user_input)]}


def should_continue(state:AgentState):
    if state['messages'][-1].content == "finished":
        return "end"
    else:
        return "chat_node"


def chat(state: AgentState) -> AgentState:
    results = model.invoke(state["messages"])
    tokens = int(results.usage_metadata["total_tokens"])
    print(f"total tokens: {tokens}\n")
    print(results.content)
    return {"messages": results, "tokens":tokens}


graph = StateGraph(AgentState)

graph.add_node("human_node", human_node)
graph.add_node("chat", chat) 

graph.add_edge(START, "human_node")
graph.add_conditional_edges(
    "human_node",
    should_continue,
    {
        "end": END,
        "chat_node": "chat"
    }
)
graph.add_edge("chat", "human_node")
app = graph.compile(checkpointer=memory)

with open("graph.png", "wb") as f:
    f.write(app.get_graph().draw_mermaid_png())
config = {"configurable": {"thread_id": "1"}}
app.invoke({"tokens":0}, config)
