from langchain_ollama import ChatOllama
from langgraph.graph import START, END, StateGraph, MessagesState
from langchain_core.messages import HumanMessage
from langgraph.prebuilt import ToolNode, tools_condition


class State(MessagesState):
    pass

llm = ChatOllama(model='qwen2.5:3b')


def multipy(a: int, b: int) -> int:
    '''this tool will multipy two numbers'''
    return a * b


tools = [multipy]
llm_with_tools = llm.bind_tools(tools=tools)


def tool_calling_llm(state: MessagesState):
    return {"messages": [llm_with_tools.invoke(state['messages'])]}


builder = StateGraph(MessagesState)

builder.add_node('tool_calling_llm', tool_calling_llm)
builder.add_node('tools', ToolNode(tools=tools))

builder.add_edge(START, 'tool_calling_llm')
builder.add_conditional_edges('tool_calling_llm', tools_condition)
builder.add_edge('tools', END)

app = builder.compile()


with open("router.png", "wb") as f:
    f.write(app.get_graph().draw_mermaid_png())


messages = HumanMessage(content="what is 3 times 3?")
messages = app.invoke({"messages":messages})
for m in messages["messages"]:
    m.pretty_print()