from langchain_core.messages import SystemMessage, HumanMessage
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode
from tools_folder.tool_file import *


def human_node(state:AgentState) -> AgentState:
    user_input = input("Enter Your Question: ")
    return {"messages":[HumanMessage(content=user_input)]}


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
app = graph.compile()

with open("graph.png", "wb") as f:
    f.write(app.get_graph().draw_mermaid_png())
