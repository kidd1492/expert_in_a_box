# services/chat_service.py
from langchain_ollama import ChatOllama


def get_model():
    return ChatOllama(model="llama3.2:3b")


class ChatService:
    def __init__(self, model=None):
        self.model = model or get_model()


    def _build_context(self, chunks):
        """
        chunks is now a list of dicts:
        {
            "id": int,
            "content": str,
            "metadata": dict,
            "score": float,
            ...
        }
        """
        return "\n\n".join(chunk["content"] for chunk in chunks)


    def _invoke(self, system_prompt, user_content):
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_content}
        ]
        return self.model.invoke(messages).content


    def answer_question(self, question, chunks):
        context_text = self._build_context(chunks)
        system_prompt = (
            "You are a helpful assistant. Use the provided context to answer the question.\n\n"
            f"Context:\n{context_text}"
        )
        return self._invoke(system_prompt, question)


    def summarize(self, chunks):
        context_text = self._build_context(chunks)
        system_prompt = "Summarize the following content:"
        return self._invoke(system_prompt, context_text)


    def outline(self, chunks):
        context_text = self._build_context(chunks)
        system_prompt = "Create an outline of the following content:"
        return self._invoke(system_prompt, context_text)
