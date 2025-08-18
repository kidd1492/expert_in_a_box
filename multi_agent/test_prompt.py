from typing import Annotated, Sequence, TypedDict
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages
from langchain_ollama import ChatOllama
from langgraph.graph import START, StateGraph, END
from ReAct_agent import running_agent

class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]
    system_prompt: str
    topic: str
    question: str
    research_summary: str

model = ChatOllama(model="qwen2.5:3b")


def chat_agent(state: AgentState) -> AgentState:
    result = model.invoke(f"{state['system_prompt']} {state['topic']}")
    state['question'] = result.content
    print(result.content)
    return state


graph = StateGraph(AgentState)
graph.add_node('chatbot', chat_agent)
graph.add_node('researcher', running_agent)

graph.add_edge(START, 'chatbot')
graph.add_edge('chatbot', 'researcher')
graph.add_edge('researcher', END)
app = graph.compile()

# Optional: Save graph visualization
with open("graph.png", "wb") as f:
    f.write(app.get_graph().draw_mermaid_png())


user_input = input("Enter a Topic: ")
system_prompt = "from the following Topic generate 5 question that will help expand on the topic given. -only return the 5 question. topic: "

state = app.invoke({'system_prompt': system_prompt,'topic': user_input})
#print(state)

