from langchain_ollama import ChatOllama
from langgraph.graph import START, StateGraph, END, MessagesState
from ReAct_agent import running_agent
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langgraph.graph.message import RemoveMessage


class AgentState(MessagesState):
    pass

model = ChatOllama(model="qwen2.5:3b")

def human_node(state: AgentState) -> AgentState:
    user_input = input("Enter Question: ")
    state['messages'] = state['messages'] + [HumanMessage(content=user_input)] 
    return state


sys_msg = SystemMessage(content="""You are lesson planner. 
                        - Given the users topic: 
                        - ask 3 to 5 questions to better understand what the user would like to learn.
                        - once you have the information make a lesson plain to teach the topic""")



def chat_agent(state: AgentState) -> AgentState:
    result = model.invoke([sys_msg] + state["messages"]) 
    state['messages'] = state['messages'] + [AIMessage(content=result.content)] 
    print(result.content)
    return state


def research_node(state: AgentState) -> AgentState:
    research_msg = SystemMessage(content="""Take the conversation and make research plan.
                                 The plan should include. 
                                 - 2 search terms related to the topic for youtube video tutorials
                                 - if the outline mentions langgraph -2 search terms for the vectorstore
                                 - and one overall themed wikipedia search term. 
                                 reponse: return only in a json format with-  research topic:, youtube search terms:, vectorstore terms: wikisearch term:""")
    result = model.invoke([research_msg] + state["messages"])
    state['messages'] = state['messages'] + [AIMessage(content=result.content)]   
    print(result.content)
    return state


def should_continue(state:AgentState):
    if state['messages'][-1].content == "finished":
        return "delete"
    else:
        return "chat"
         

def delete_messages(state:AgentState):
    delete_messages = [RemoveMessage(id=m.id) for m in state["messages"][:-2]]
    return {"messages": delete_messages}


graph = StateGraph(AgentState)

graph.add_node("human_node", human_node)
graph.add_node('chatbot', chat_agent)
graph.add_node("research_node", research_node)
graph.add_node("delete_messages", delete_messages)

graph.add_edge(START, 'human_node')
graph.add_conditional_edges(
    "human_node",
    should_continue,
    {
        "delete": "delete_messages",
        "chat": "chatbot"
    }
)
graph.add_edge('chatbot', 'human_node')
graph.add_edge("delete_messages", "research_node")
graph.add_edge("research_node", END)
app = graph.compile()

# Optional: Save graph visualization
with open("graph.png", "wb") as f:
    f.write(app.get_graph().draw_mermaid_png())

result = app.invoke({})
print(result)
