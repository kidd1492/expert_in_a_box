# LangGraph Conditional Edge Comparison


Both  epresent the same logical flow:  
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
