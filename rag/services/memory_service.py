# services/memory_service.py
from typing import List, Tuple, Optional
from core.memory import MemoryStore


class MemoryService:
    def __init__(self, memory_store: MemoryStore | None = None):
        self.memory_store = memory_store or MemoryStore()

    def load(self, thread_id: str) -> Optional[Tuple[str, List[str]]]:
        return self.memory_store.load_memory(thread_id)

    def save(self, thread_id: str, summary: str, messages: List[str]):
        self.memory_store.save_memory(thread_id, summary, messages)

    def last_thread_id(self) -> Optional[str]:
        return self.memory_store.get_last_thread_id()
