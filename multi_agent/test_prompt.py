from typing import TypedDict, List, Union
from langchain_ollama import ChatOllama
from langgraph.graph import START, StateGraph, END
from ReAct_agent import running_agent

class PromptState(TypedDict):
    topic: str
    question: str
    research_summary: str

model = ChatOllama(model="qwen2.5:3b")


def chat_agent(state: PromptState) -> PromptState:
    system_prompt = "from the following Topic generate 5 question that will help expand on the topic given. -only return the 5 question. topic: "
    result = model.invoke(f"{system_prompt} {state['topic']}")
    state['question'] = result.content
    print(result.content)
    return state


graph = StateGraph(PromptState)
graph.add_node('chatbot', chat_agent)
graph.add_edge(START, 'chatbot')
graph.add_edge('chatbot', END)
app = graph.compile()

# Optional: Save graph visualization
with open("graph.png", "wb") as f:
    f.write(app.get_graph().draw_mermaid_png())


user_input = input("Enter a Topic: ")
state = app.invoke({'topic': user_input})
result = running_agent(f"{state['topic']} {state['question']}")
state['research_summary'] = result
print("\n", result)

