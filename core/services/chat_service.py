# services/chat_service.py
from langchain_ollama import ChatOllama
from langchain.messages import HumanMessage, SystemMessage
from langchain_classic.schema import BaseMessage

def get_model():
    return ChatOllama(model="qwen2.5:3b")


class ChatService:
    def __init__(self, model=None):
        self.model = model or get_model()


    def _build_context(self, chunks):
        return "\n\n".join(chunk["content"] for chunk in chunks)


    def invoke(self, system_prompt, user_content):
        prompt = SystemMessage(content=system_prompt)
        user_input = HumanMessage(content=user_content)
        messages = [prompt, user_input]
        return self.model.invoke(messages)
    
    def invoke_chatbot(self, messages):
        return self.model.invoke(messages)

    def summarize_messages(self, messages: list[BaseMessage]) -> str:
        summary_prompt = [
            HumanMessage(content=(
                "Summarize the following conversation in a concise way that preserves important facts, "
                "names, goals, and context. Do NOT include irrelevant chit‑chat.\n\n"
                f"{messages}"
            ))
        ]
        result = self.model.invoke(summary_prompt)
        return result.content

    def answer_question(self, question, chunks):
        context_text = self._build_context(chunks)
        system_prompt = (
            "You are a helpful assistant. Use the provided context to answer the question.\n\n"
            f"Context:\n{context_text}"
        )
        return self.invoke(system_prompt, question)


    def summarize(self, chunks):
        context_text = self._build_context(chunks)
        system_prompt = "Summarize the following content:"
        return self.invoke(system_prompt, context_text)


    def outline(self, chunks):
        context_text = self._build_context(chunks)
        system_prompt = "Create an outline of the following content:"
        return self._invoke(system_prompt, context_text)


    def summarize_topic(self, term: str) -> str:
        prompt = f"Give a clear one or two paragraph overview of the topic '{term}'."
        return self.model.invoke(prompt)

    def generate_subtopics(self, term: str) -> list[str]:
        prompt = f"List 5 essential subtopics someone must learn to understand '{term}'. a list of terms only no other reponse. example- 'subtopics: [subtopic,subtopic, ...]'"
        response = self.model.invoke(prompt)
        return response

