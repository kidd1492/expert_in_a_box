from typing import Annotated, Sequence, TypedDict
from dotenv import load_dotenv
from langchain_core.messages import BaseMessage, SystemMessage, HumanMessage
from langchain_ollama import ChatOllama
from langchain_core.tools import tool
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, END, START
from langgraph.prebuilt import ToolNode
from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain_community.vectorstores import FAISS
import wikipedia as wk
from ReAct_agent import running_agent

class State(TypedDict):
    topic: str
    blog_outline: str

model = ChatOllama(model="llama3.2:3b")


def outline(State: State) -> State:
    state = State
    print(state)
    system_prompt = SystemMessage(content="""You are an assistant. Given the user's Topic or Code,:
                                    1. generate an  step by step outline for a tutorial-style blog post, 
                                    2. search_terms: A list of search terms to look up for better understanding of the topic
                                       search terms for the vectorstore dealing with langgraph, wikipedia for any other""")
    user_input = input("Enter a Topic: ")
    state["topic"] = user_input
    result = model.invoke(f"user's Topic: {user_input} {system_prompt}")
    state['blog_outline'] = result.content
    running_agent(result.content)
    print("Outline sent to agent.", "\n")
    return state



graph = StateGraph(State)

graph.add_node('outline', outline)
graph.add_edge(START, 'outline')
graph.add_edge('outline', END)
app = graph.compile()


def run_system():
    app.invoke(input={})


run_system()