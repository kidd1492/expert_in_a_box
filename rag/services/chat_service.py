from rag.core.chat_agent import model
from langchain_core.messages import SystemMessage, HumanMessage

class ChatService:

    def __init__(self):
        self.model = model

    def answer_question(self, question: str, chunks: list[tuple]):
        context = "\n\n".join(chunk[0] for chunk in chunks)

        system_prompt = (
            "You are Expert-in-a-Box, a retrieval-augmented assistant. "
            "Use ONLY the provided context when answering. "
            "If the answer is not in the context, say you don't know."
        )

        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=f"Context:\n{context}\n\nUser question: {question}")
        ]
        return self.model.invoke(messages).content


    def summarize(self, chunks: list[tuple]):
        context = "\n\n".join(chunk[0] for chunk in chunks)

        messages = [
            SystemMessage(content="Summarize the following retrieved context clearly and concisely."),
            HumanMessage(content=context)
        ]
        return self.model.invoke(messages).content


    def outline(self, chunks: list[tuple]):
        context = "\n\n".join(chunk[0] for chunk in chunks)

        messages = [
            SystemMessage(content="Create a structured outline of the following context."),
            HumanMessage(content=context)
        ]
        return self.model.invoke(messages).content

