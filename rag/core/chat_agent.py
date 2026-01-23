from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage

model = ChatOllama(model="qwen2.5:3b")

def chat_with_model(user_message: str, retrieved_chunks: list[str]):
    system_prompt = (
        "You are Expert-in-a-Box, a retrieval-augmented assistant. "
        "Use ONLY the provided context when answering. "
        "If the answer is not in the context, say you don't know."
    )

    context_text = "\n\n".join(retrieved_chunks)

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=f"Context:\n{context_text}\n\nUser question: {user_message}")
    ]

    response = model.invoke(messages)
    return response.content
