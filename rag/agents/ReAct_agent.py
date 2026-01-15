from langchain_core.messages import SystemMessage, HumanMessage, RemoveMessage
from langgraph.graph import StateGraph, START, END, MessagesState
from langgraph.prebuilt import ToolNode
from langchain_ollama import ChatOllama

from utils.log_handler import app_logger, project_logger
from services.memory_service import MemoryService
from agents.tool_file import add_file, wiki_search, retriever_tool

memory = MemoryService()

class AgentState(MessagesState):
    summary: str
    thread_id: str


def human_node(state: AgentState) -> AgentState:
    user_input = input("Enter Your Question: ")
    return {"messages": [HumanMessage(content=user_input)]}


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


tools = [add_file, wiki_search, retriever_tool]
model = ChatOllama(model="qwen2.5:3b").bind_tools(tools)


def should_continue(state: AgentState):
    last_msg = state["messages"][-1].content.lower()

    if last_msg in ["exit", "quit", "q"]:
        thread_id = state.get("thread_id")
        summary = state.get("summary", "")
        messages = [m.content for m in state.get("messages", [])]

        memory.save(thread_id, summary, messages)
        project_logger.info(f"Session finalized and memory saved. Thread_id: {thread_id}")

        return "end"

    elif len(state["messages"]) > 6:
        return "summarized"

    else:
        return "chat"


def summary_node(state: AgentState):
    summary = state.get("summary", "")

    if summary:
        summary_message = (
            f"This is a summary of the conversation to date: {summary}\n\n"
            "Extend the summary by taking into account the new messages above:"
        )
    else:
        summary_message = "Create a summary of the conversation above: "

    messages = state["messages"] + [HumanMessage(content=summary_message)]
    response = model.invoke(messages)

    # Remove older messages
    delete_messages = [RemoveMessage(id=m.id) for m in state["messages"][:-2]]

    # Save updated memory
    memory.save(
        thread_id=state["thread_id"],
        summary=response.content,
        messages=[m.content for m in state["messages"][-2:]]
    )

    project_logger.info(
        f"Session summarized and memory saved. Thread_id: {state['thread_id']}"
    )

    return {"summary": response.content, "messages": delete_messages}


def tools_condition(state: AgentState):
    last_message = state["messages"][-1]
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
        "summarized": "summary_node",
        "end": END,
        "chat": "chatbot",
    },
)

graph.add_conditional_edges(
    "chatbot",
    tools_condition,
    {
        "continue": "tools",
        "human": "human_node",
    },
)

graph.add_edge("tools", "chatbot")
graph.add_edge("summary_node", "chatbot")

app = graph.compile()

# Optional: generate graph visualization
#with open("graph.png", "wb") as f:
#    f.write(app.get_graph().draw_mermaid_png())
