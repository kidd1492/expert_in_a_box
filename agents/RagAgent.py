from dotenv import load_dotenv
import os
from langgraph.graph import StateGraph, END
from typing import Annotated, Sequence, TypedDict
from langchain_core.messages import BaseMessage, SystemMessage, HumanMessage, ToolMessage
from operator import add as add_messages
from langchain_ollama import ChatOllama
from langchain_ollama import OllamaEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.tools import tool
from langchain_chroma import Chroma

load_dotenv()

llm = ChatOllama(
    model='llama3.2:3b', temperature=0)

embeddings = OllamaEmbeddings(
    model="mxbai-embed-large:335m",
)



pdf_path = "C:/Users/chris/Desktop/AI_research/FFXfinal.pdf"
if not os.path.exists(pdf_path):
    raise FileNotFoundError(f"PDF file not found: {pdf_path}")

pdf_loader = PyPDFLoader(pdf_path)

try:
    pages = pdf_loader.load()
    print(F"PDF has been loaded and has {len(pages)} pages")
except Exception as e:
    print(f"Error loading PDF: {e}")
    raise FileNotFoundError(f"PDF file not found: {pdf_path}")


text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=100
)

page_split = text_splitter.split_documents(pages)

persist_directory = r"C:/Users/chris/Desktop/expert_in_a_box/agents/out"
collection_name = "llms"

if os.path.exists(persist_directory):
    os.makedirs(persist_directory)

try:
    vectorstore = Chroma.from_documents(
        documents=page_split,
        embedding=embeddings,
        persist_directory=persist_directory,
        collection_name=collection_name
    )
    print(f"Created ChromaDB vecor store!")
except Exception as e:
    print(f"Error Setting up ChromaDB: {str(e)}")


retriever = vectorstore.as_retriever(
    search_type='similarity',
    search_kwargs={"k": 5}
)

@tool
def retriever_tool(query: str) -> str:
    "this tool searches and returns the information from the documents provided"
    docs = retriever.invoke(query)

    if not docs:
        return "I found no data for that!"
    
    results = []
    for i, docs in enumerate(docs):
        results.append(f"Document {i+1}:\n{docs.page_content}")

    return "\n\n".join(results)

tools = [retriever_tool]
llm = llm.bind_tools(tools)

class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]


def should_continue(state: AgentState):
    """Check if the last message contains toll calls."""
    result = state["messages"][-1]
    return hasattr(result, 'tool_calls') and len(result.tool_calls) > 0

system_promp = """
You are an intelligent LLM that is to answer question about my documents and other to the best of your ability
Please always cite the specific parts of the documents you use in your answer.
"""

tools_dict = {our_tool.name: our_tool for our_tool in tools}

def call_llm(state: AgentState) -> AgentState:
    """Function to call the LLM with the current state"""
    messages = list(state["messages"])
    messages = [SystemMessage(content=system_promp)] + messages
    messages = llm.invoke(messages)
    return {'messages': [messages]}

def take_action(state: AgentState) -> AgentState:
    '''Execute tool calls from the LLM's response'''

    tool_calls = state["messages"][-1].tool_calls
    results = []
    for t in tool_calls:
        print(f"Calling Tool: {t['name']} with query: {t['args'].get('query', 'No query provided')}")

        if not t['name'] in tools_dict:
            print(f"\nTool: {t['name']} does not exist")
            result = "Incorrect tool name, Please Retry and Select tool from list of Available tools"
        else:
            result = tools_dict[t['name']].invoke(t['args'].get('query', ''))
            print(f"Result Length: {len(str(result))}")

        results.append(ToolMessage(tool_call_id=t['id'], name=t['name'], content=str(result)))

    print("Tool Execution Comoplete. Back to the model!")
    return {'messages': results}


graph = StateGraph(AgentState)
graph.add_node("llm", call_llm)
graph.add_node("retriever_agent", take_action)

graph.add_conditional_edges(
    "llm", 
    should_continue, 
    {True: "retriever_agent", False: END}
)
graph.add_edge("retriever_agent", "llm")
graph.set_entry_point("llm")

rag_agent = graph.compile()


def running_agent():
    print("Rag_agent")
    while True:
        user_input = input("\nWhat is your question: ")
        if user_input.lower() in ['exit', 'quit']:
            break

        messages = [HumanMessage(content=user_input)]
        result = rag_agent.invoke({'messages': messages})

        print("\n === Anser ===")
        print(result['messages'][-1].content)


running_agent()