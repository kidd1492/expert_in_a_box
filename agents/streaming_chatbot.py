from typing import Annotated, Sequence, TypedDict
from langchain_core.messages import BaseMessage, SystemMessage, HumanMessage
from langchain_ollama import ChatOllama
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, END, START


class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]


model = ChatOllama(model='llama3.2:3b')


def model_call(state: AgentState) -> AgentState:
    print(len(state['messages']), "\n")
    system_prompt = SystemMessage(content="You are an assistant, please answer my query to the best of your ability.")
    input_messages = [system_prompt] + state["messages"]
    response = model.invoke(input_messages)
    return {"messages": [response]}


graph = StateGraph(AgentState)

graph.add_node('Agent', model_call)
graph.add_edge(START, 'Agent')
graph.add_edge('Agent', END)

app = graph.compile()

with open("graph.png", "wb") as f:
    f.write(app.get_graph().draw_mermaid_png())


conversation_history = []

def running_agent():
    print("Agent Ready")
    while True:
        user_input = input("\n📥 Question: ")
        if user_input.lower() in ["exit", "quit"]:
            break

        # Add user message to history
        conversation_history.append(HumanMessage(content=user_input))

        # Stream response with full history
        inputs = {"messages": conversation_history}
        final_ai_message = None

        for s in app.stream(inputs, stream_mode="values"):
            messages = s.get("messages", [])
            if messages:
                last = messages[-1]
                try:
                    last.pretty_print()
                except AttributeError:
                    print(last)
                final_ai_message = last  # Capture last AI message

        # Append AI message to history
        if final_ai_message:
            conversation_history.append(final_ai_message)


running_agent()
