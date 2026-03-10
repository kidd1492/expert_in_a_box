# services/memory_service.py
from typing import List, Tuple, Optional
from rag.core.memory import MemoryStore
import json
from langchain_classic.schema import BaseMessage, messages_from_dict, message_to_dict


class MemoryService:
    def __init__(self, memory_store: MemoryStore | None = None):
        self.memory_store = memory_store or MemoryStore()


    def load(self, thread_id):
        row = self.memory_store.load_memory(thread_id)
        if not row:
            return None

        summary, messages_json = row
        messages_dicts = json.loads(messages_json)
        messages = messages_from_dict(messages_dicts)

        return summary, messages

    def reduce_if_needed(self, thread_id: str, messages: list[BaseMessage], chat_service):
        # Only reduce if more than 6 messages
        if len(messages) <= 6:
            return None, messages

        # Split messages
        old_messages = messages[:-2]   # everything except last 2
        recent_messages = messages[-2:]  # last 2 messages

        # Summarize old messages
        summary = chat_service.summarize_messages(old_messages)
        print("\n", "summarized")

        # Return new summary + trimmed messages
        return summary, recent_messages


    def save(self, thread_id, summary, messages: list[BaseMessage]):
        messages_json = json.dumps([message_to_dict(m) for m in messages], ensure_ascii=False)
        self.memory_store.save_memory(thread_id, summary, messages_json)


    def last_thread_id(self) -> Optional[str]:
        return self.memory_store.get_last_thread_id()
    
    def conversation_history(self):
        return self.memory_store.conversation_history(self)