from langgraph.graph.message import StateGraph, MessagesState
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langgraph.graph import START, END
from langchain_ollama import ChatOllama

class AgentState(MessagesState):
    count : int


model = ChatOllama(model="llama3.2:3b", temperature=0.5)


def fed(state:AgentState) -> AgentState:
    system_message = SystemMessage(content="""You are a Federalist in the year 1791, perhaps channeling the voice of John Adams or Alexander Hamilton.
                                    - You believe in a strong centralized government, a national bank, and the importance of order and stability.
                                    - Respond to the Non-Federalist's remarks with eloquence and conviction, referencing Enlightenment ideals, the Constitution, and the dangers of factionalism.
                                    - Ask probing questions that challenge their assumptions about liberty and governance.
                                    - Use formal, period-appropriate language and maintain a tone of intellectual rigor.
                                    - Response length should be about 2 paragraphs.""")

    results =  model.invoke(f"{system_message}, {state['messages']}")
    with open("output.txt", "a", encoding="utf-8") as output:
         output.write(f"Federalist-response: {results.content}\n")
    print(f"\nFederalist-response: {results.content}")
    return {"messages": results}


def non_fed(state:AgentState) -> AgentState:
    count = state['count'] + 1
    system_message = SystemMessage(content="""You are a Non-Federalist in the year 1791, perhaps channeling the voice of Thomas Jefferson or Patrick Henry.
                                    - You advocate for states rights, individual liberty, and fear the rise of tyranny through centralized power.
                                    - Respond to the Federalists remarks with passion and philosophical depth, referencing the Declaration of Independence, natural rights, and the lessons of monarchy.
                                    - Ask thought-provoking questions that highlight the risks of federal overreach.
                                    - Use expressive, period-appropriate language and appeal to the common citizens wisdom.
                                    - Response length should be about 2 paragraphs.""")

    results = model.invoke(f"{system_message}, {state['messages']}")
    with open("output.txt", "a", encoding="utf-8") as output:
         output.write(f"NON-Federalist-response: {results.content}\n")
    print(f"\nnon-fed-reply: {results.content}")
    return {"messages": results, "count":count}


def should_continue(state:AgentState):
     count = state["count"]
     print(f"\n{count}\n")
     if count != 2:
          return "continue"
     else:
          return "summarize_convo"

def summary_node(state:AgentState) -> AgentState:
    system_message = SystemMessage(content="""here is a conversation between a federalist and a non-federalist.
                                    - Summarize the conversation.
                                    - highlight the point in the reponses brake down the arguments between the two sides.
                                    - Ask thought-provoking questions 3 follow up question for a 9th grade student to think about relating to the conversation.""")
    results = model.invoke(f"{system_message}, {state['messages']}")
    with open("output.txt", "a", encoding="utf-8") as output:
         output.write(f"Summary: {results.content}\n")
    print(f"\nSummary: {results.content}")
    return {"messages": results}

graph = StateGraph(AgentState)

graph.add_node("federalist", fed)
graph.add_node("non_federalist", non_fed)
graph.add_node("summary", summary_node)

graph.add_edge(START, "federalist")
graph.add_edge("federalist", "non_federalist")
graph.add_conditional_edges(
     "non_federalist",
     should_continue,
     {
          "continue": "federalist",
          "summarize_convo": "summary"
     }
)

app = graph.compile()

with open("conversation.png", "wb") as f:
    f.write(app.get_graph().draw_mermaid_png())


user_input = ("The year is 1791. The Constitution has just been ratified, and the young republic stands at a crossroads. debate the future of governance. start the debate")
with open("output.txt", "a", encoding="utf-8") as output:
         output.write(f"setup: {user_input}\n")
         
app.invoke({"messages": HumanMessage(content=user_input), "count": 0})
