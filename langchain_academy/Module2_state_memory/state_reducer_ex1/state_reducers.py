from operator import add
from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, START, END
from langgraph.errors import InvalidUpdateError


class State(TypedDict):
    #foo:int
    foo: Annotated[list[int], add]


def node_1(state):
    print("node_1")
    return {'foo': [state['foo'][-1] + 1]}

def node_2(state):
    print("node_2")
    return {'foo': [state['foo'][-1] + 1]}

def node_3(state):
    print("node_3")
    return {'foo': [state['foo'][-1] + 1]}


builder =  StateGraph(State)

builder.add_node('node_1', node_1)
builder.add_node('node_2', node_2)
builder.add_node('node_3', node_3)

builder.add_edge(START, 'node_1')
builder.add_edge('node_1', 'node_2')
builder.add_edge('node_1', 'node_3')
builder.add_edge('node_2', END)
builder.add_edge('node_3', END)

app = builder.compile()

with open("state_reducers.png", "wb") as f:
    f.write(app.get_graph().draw_mermaid_png())

try:
    print(app.invoke({"foo" : [1]}))
except InvalidUpdateError as e:
    print(f"invalid input error {e}")