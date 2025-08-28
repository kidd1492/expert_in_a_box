 # sqlite database

 - I've included a test.db.py file that allows you to look at the setup of the sqlite database

# MemorySaver
```
from langgraph.checkpoint.memory import MemorySaver
memory = MemorySaver()
app = builder.compile(checkpointer=memory)
```

### appending to a conversation_history = []
```
conversation_history = []

def process(state: AgentState) -> AgentState:
    """This node will solve the request you input"""
    response = llm.invoke(state["messages"])

    #appending response here!!

    state["messages"].append(AIMessage(content=response))
    print(f"\nAI: {response}")
    return state

user_input = input("Enter: ")
while user_input != "exit":
    conversation_history.append(HumanMessage(content=user_input))
    result = agent.invoke({"messages": conversation_history})
    conversation_history = result["messages"]
```

# Literal summarizing_chat.py

I tried to run this the way it showed in the module but it was giving me and error. 


### #-> Literal ["summarize_conversation", "end"]:
```
def should_continue(state: State): #-> Literal ["summarize_conversation", "end"]:
    messages =  state["messages"]
    if len(messages) > 6:
        return "summarized"
    else:
        return "end"


builder = StateGraph(State)
builder.add_node("conversation", call_model)
builder.add_node("summarize_conversation", summarize_conversation)

builder.add_edge(START, "conversation")
builder.add_conditional_edges(
    "conversation",
    should_continue,
    {
        "summarized": "summarize_conversation",
        "end": END,
    }
)
builder.add_edge("summarize_conversation", END)
```
