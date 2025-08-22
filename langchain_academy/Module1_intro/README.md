# LangGraph Conditional Edge Comparison

When I setup how they showed in the course it detatched the nodes
from the rest of the graph. I ran it both way and had the same result. 

Both have the same logical flow:  
`__start__ → node_1 → (node_2 or node_3) → __end__`

Both setups work the same at runtime
The difference lies in how conditional edges are defined.

## Implicit vs. Explicit

### graph.png (Implicit)
```python
builder.add_conditional_edges('node_1', condition)
```
- Relies on condition returning exact node names.
- Nodes may appear disconnected in visualization.
- Less robust for debugging or semantic routing.

### graph2.png (Explicit)
```python
builder.add_conditional_edges(
    'node_1',
    condition,
    {
        "node_2": "node_2",
        "node_3": "node_3",
    }
)
```
- Explicitly maps condition outputs to node names.
- Graph renders correctly with all edges.
- Recommended for clarity and maintainability.


# tools_condition
what is tool condition doing?
```
from langgraph.prebuilt import tools_condition
builder.add_conditional_edges("assistant", tools_condition)
```
-----------------------------------------------------------------
### function
```
def tool_condition(state: MessagesState):
    messages = state["messages"]
    last_message = messages[-1]
    return "continue" if getattr(last_message, "tool_calls", None) else "end"
```
### when adding the conditional_edge
```
builder.add_conditional_edges(
    "assistant",
    tool_condition,
    {
        "continue": "tools",
        "end": END,
    },
)
```
-------------------------------------------------------------

# MessagesState
```
class MessagesState(TypedDict):
    messages: AnyMessage[list[AnyMessage], add_messages]


class State(MessagesState):
    pass
```