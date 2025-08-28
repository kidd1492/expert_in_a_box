from pprint import pprint
from langchain_core.messages import AIMessage, HumanMessage, RemoveMessage
from langgraph.graph import MessagesState, START, StateGraph, END
from langchain_ollama import ChatOllama


messages = [AIMessage(content=f"you are researching ocean mamals?", name="Bot", id="0")]
messages.append(HumanMessage(f"Hi", name="Chris", id="1"))
messages.append(AIMessage(content=f"Hi !", name="Bot", id="2"))
messages.append(HumanMessage(f"Yes, I know about whatles. But what others should I learn about", name="Chris", id="3"))
messages.append(AIMessage(content=f"there are a large veriety of other ocean mamals!", name="Bot", id="4"))
messages.append(HumanMessage(f"Yes, I know about whales. But what others should I learn about", name="Chris", id="5"))

#for m in messages:m.pretty_print()

llm = ChatOllama(model="qwen2.5:3b")

'''deletes all but the last 2 messages. '''
def filter_messages(state:MessagesState):
    delete_messages = [RemoveMessage(id=m.id) for m in state["messages"][:-2]]
    return {"messages": delete_messages}


'''state["messages"][-1:] this passes the last message when invoking the model. the state remains unchanged.
reducing the number of tokent the model has to process '''
def chat_model_node(state: MessagesState):
    return {"messages": llm.invoke(state["messages"][-1:])}


builder = StateGraph(MessagesState)
builder.add_node('filter', filter_messages)
builder.add_node("chat_model", chat_model_node)
builder.add_edge(START, "filter")
builder.add_edge("filter", "chat_model")
builder.add_edge("chat_model", END)

app = builder.compile()

with open("trim_filter_messages.png", "wb") as f:
    f.write(app.get_graph().draw_mermaid_png())

output = app.invoke({"messages": messages})
for m in output["messages"]:
    m.pretty_print()