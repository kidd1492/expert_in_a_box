from langchain_ollama import ChatOllama, OllamaEmbeddings
from langgraph.graph import START, END, StateGraph
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
import numpy as np
from typing import TypedDict, List
from memory import RAGDatabase

model = ChatOllama(model="qwen2.5:3b")
embedding_model = OllamaEmbeddings(model='mxbai-embed-large:335m')

class AgentState(TypedDict):
    messages: HumanMessage | AIMessage

def chat_node(state: AgentState) -> AgentState:
    db = RAGDatabase()
    user_message = state['messages'][0]
    query_embedding = embedding_model.embed_query(user_message.content)
    query_array = np.array(query_embedding, dtype=np.float32)

    # Retrieve memory if available
    if db.count() == 0:
        memory_context = "No prior memory available."
    else:
        retrieved = db.search_similar(query_array, top_k=3)
        memory_context = "\n".join([f"{role}: {content}" for role, content in retrieved]) or "No relevant memory found."

    # Construct prompt
    system_prompt = SystemMessage(content="Use the following memory to inform your response:\n" + memory_context)
    full_prompt = [system_prompt, user_message]

    response = model.invoke(full_prompt)
    print(response)
    return {"messages": [response]}

def embedding_node(state: AgentState):
    db = RAGDatabase()
    message = state['messages'][0]
    embedding = embedding_model.embed_query(message.content)
    embedding_array = np.array(embedding, dtype=np.float32)
    db.add_message(
        role=message.type,
        content=message.content,
        embedding=embedding_array
    )
    print("Stored embedding:", embedding_array)

def should_continue(state: AgentState):
    message = state['messages'][0]
    if isinstance(message, HumanMessage):
        return "chat"
    else:
        return "end"

graph = StateGraph(AgentState)
graph.add_node('chat_node', chat_node)
graph.add_node('embedding_node', embedding_node)

graph.add_edge(START, 'embedding_node')
graph.add_conditional_edges('embedding_node', should_continue, {
    'chat': 'chat_node',
    'end': END
})
graph.add_edge('chat_node', 'embedding_node')
agent = graph.compile()

with open("graph.png", "wb") as f:
    f.write(agent.get_graph().draw_mermaid_png())

user_input = input("Enter Question: ")
inputs = {"messages": [HumanMessage(content=user_input)]}
agent.invoke(inputs)
