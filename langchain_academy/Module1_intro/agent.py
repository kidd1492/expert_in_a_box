from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.graph import MessagesState, START, END, StateGraph
from langgraph.prebuilt import tools_condition, ToolNode


class State(MessagesState):
    pass


def multipy(a:int, b:int) -> int:
    '''this function multipies two numbers'''
    return a * b


def add(a:int, b:int) -> int:
    '''this function adds two numbers'''
    return a + b


def subtract(a:int, b:int) -> int:
    '''this function subtracts two numbers'''
    return a - b


llm = ChatOllama(model='qwen2.5:3b')

tools = [multipy, add, subtract]
llm_with_tools = llm.bind_tools(tools=tools)

sys_msg = SystemMessage(content="""You are a helpful assistant tasked with performing arithmatic on a set of inputs.
                         you have tools = [multipy, add, subtract] arg a:int, b:int""")


def assistant(state: MessagesState):
    return {"messages": [llm_with_tools.invoke([sys_msg] + state["messages"])]}

'''
def should_continue(state: MessagesState):
    messages = state["messages"]
    last_message = messages[-1]
    return "continue" if getattr(last_message, "tool_calls", None) else "end"
'''

builder = StateGraph(MessagesState)

builder.add_node("assistant", assistant)
builder.add_node("tools", ToolNode(tools=tools))

builder.add_edge(START, "assistant")
builder.add_conditional_edges("assistant", tools_condition)

'''
builder.add_conditional_edges(
    "assistant",
    should_continue,
    {
        "continue": "tools",
        "end": END,
    },
)
'''
builder.add_edge("tools", "assistant")

app = builder.compile()

with open("agent.png", "wb") as f:
    f.write(app.get_graph().draw_mermaid_png())

while True:
    user_input = input("Enter Question: ")
    if user_input.lower() in ["exit", "quit", "q"]:
        break

    messages = HumanMessage(content=user_input)
    messages = app.invoke({"messages":messages})
    for m in messages["messages"]:
        m.pretty_print()
