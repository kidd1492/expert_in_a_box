from typing import TypedDict
from random import randint
from langgraph.graph import START, END, StateGraph


class State(TypedDict):
    graph_state : str


def node_1(state):
    print("node_1")
    return {"graph_state": state['graph_state'] + "I am "}

def node_2(state):
    print("node_2")
    return {"graph_state": state['graph_state'] + "happy!!"}

def node_3(state):
    print("node_3")
    return {"graph_state": state['graph_state'] + "sad."}


def condition(State):

    num = randint(0, 9)
    if num < 5:return "node_2"
    else:return "node_3"


builder = StateGraph(State)

builder.add_node('node_1', node_1)
builder.add_node('node_2', node_2)
builder.add_node('node_3', node_3)

builder.add_edge(START, 'node_1')

builder.add_conditional_edges(
    'node_1', 
    condition,
    {
        "node_2" : "node_2",
        "node_3" : "node_3",
    }
)
builder. add_edge('node_2', END)
builder. add_edge('node_3', END)

app = builder.compile()

# Optional: Save graph visualization
with open("simple_graph.png", "wb") as f:
    f.write(app.get_graph().draw_mermaid_png())

result = app.invoke({"graph_state": "hello i am chris "})
print(result)