from langchain_core.messages import SystemMessage, HumanMessage, RemoveMessage
from langchain_ollama import ChatOllama
from langgraph.graph import StateGraph, START, END, MessagesState
from langgraph.prebuilt import ToolNode
from tool_file import add_file, wiki_search, retriever_tool
from langgraph.checkpoint.sqlite import SqliteSaver
import sqlite3



class AgentState(MessagesState):
    summary : str

db_path = "example.db"
conn = sqlite3.connect(db_path, check_same_thread=False)
memory = SqliteSaver(conn)
tools = [add_file, wiki_search, retriever_tool]
model = ChatOllama(model='qwen2.5:3b').bind_tools(tools)


def human_node(state:AgentState) -> AgentState:
    user_input = input("Enter Your Question: ")
    return {"messages":[HumanMessage(content=user_input)]}


def should_continue(state:AgentState):
    if state['messages'][-1].content == "finished":
        return "end"
    elif len(state["messages"]) > 6:
        return "summarized"
    else:
        return "chat"


def chat(state: AgentState):
    summary = state.get("summary", "")
    if summary:
        system_message = f"Summary of conversation earlier: {summary}"
        messages = [SystemMessage(content=system_message)] + state["messages"]
    else:
        messages = state["messages"]

    response = model.invoke(messages)
    print("\n", response.content)
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


def tools_condition(state: AgentState): 
    messages = state["messages"]
    last_message = messages[-1]
    return "continue" if getattr(last_message, "tool_calls", None) else "human"


graph = StateGraph(AgentState)
graph.add_node("human_node", human_node)
graph.add_node("chatbot", chat)
graph.add_node("tools", ToolNode(tools=tools))
graph.add_node("summary_node", summary_node) 

graph.add_edge(START, "human_node")
graph.add_conditional_edges(
    "human_node",
    should_continue,
    {
        "summarized" : "summary_node",
        "end": END,
        "chat": "chatbot"
    }
)

graph.add_conditional_edges(
    "chatbot",
    tools_condition,
    {
        "continue": "tools",
        "human": "human_node"
    }
)
graph.add_edge("tools", "chatbot")
graph.add_edge("summary_node", "chatbot")
app = graph.compile(checkpointer=memory)

with open("graph.png", "wb") as f:
    f.write(app.get_graph().draw_mermaid_png())

config = {"configurable": {"thread_id": "1"}}
output = app.invoke({}, config)
print(f"\n\n{app.get_state(config).values.get("summary","")}\n\n")

