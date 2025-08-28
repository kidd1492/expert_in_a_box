from typing import TypedDict
from langgraph.graph import START, END, StateGraph


class InputState(TypedDict):
    question:str

class OutputState(TypedDict):
    answer: str

class OverallState(TypedDict):
    question:str
    answer: str
    notes: str


def thinking_node(state:InputState):
    return {"answer": "bye", "notes": "... his name is Chris"}

def answer_node(state:OverallState) -> OutputState:
    return {"answer": "bye Chris"}

builder = StateGraph(OverallState, input_schema=InputState, output_schema=OutputState)

builder.add_node("thinking_node", thinking_node)
builder.add_node("answer_node", answer_node)

builder.add_edge(START, "thinking_node")
builder.add_edge("thinking_node", "answer_node")
builder.add_edge("answer_node", END)
app = builder.compile()

with open("multiple_schemas.png", "wb") as f:
    f.write(app.get_graph().draw_mermaid_png())


print(app.invoke({'question': "Hi"}))