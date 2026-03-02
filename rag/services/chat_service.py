# rag/services/chat_service.py
from langchain_core.messages import SystemMessage, HumanMessage


from langchain_ollama import ChatOllama

def get_model():
    return ChatOllama(model="qwen2.5:3b")



class ChatService:

    def __init__(self, model=None):
        self.model = model or get_model()

    def _build_context(self, chunks):
        return "\n\n".join(chunk["text"] for chunk in chunks)

    def _invoke(self, system_prompt, user_content):
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_content)
        ]
        return self.model.invoke(messages).content

    def answer_question(self, question, chunks):
        context = self._build_context(chunks)
        system_prompt = (
            "You are Expert-in-a-Box, a retrieval-augmented assistant. "
            "Use ONLY the provided context when answering. "
            "If the answer is not in the context, say you don't know."
        )
        user_content = f"Context:\n{context}\n\nUser question: {question}"
        return self._invoke(system_prompt, user_content)

    def summarize(self, chunks):
        context = self._build_context(chunks)
        return self._invoke(
            "Summarize the following retrieved context clearly and concisely.",
            context
        )

    def outline(self, chunks):
        context = self._build_context(chunks)
        return self._invoke(
            "Create a structured outline of the following context.",
            context
        )
