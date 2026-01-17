import sqlite3, json
from typing import List, Tuple, Optional


class MemoryStore:
    def __init__(self, db_path="data/rag_store.db"):
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self._init_schema()

    def _init_schema(self):
        cursor = self.conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS memory (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT,
                thread_id TEXT UNIQUE,
                summary TEXT,
                messages TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        self.conn.commit()

    def load_memory(self, thread_id: str) -> Optional[Tuple[str, List[str]]]:
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT summary, messages FROM memory
            WHERE thread_id = ?
            ORDER BY timestamp DESC LIMIT 1
        """, (thread_id,))
        row = cursor.fetchone()
        if row:
            summary, messages_json = row
            return summary, json.loads(messages_json)
        return None

    def save_memory(self, thread_id: str, summary: str, messages: List[str]):
        messages_json = json.dumps(messages)
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO memory (session_id, thread_id, summary, messages)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(thread_id) DO UPDATE SET
                summary=excluded.summary,
                messages=excluded.messages,
                timestamp=CURRENT_TIMESTAMP
        """, (None, thread_id, summary, messages_json))
        self.conn.commit()


    def get_last_thread_id(self) -> Optional[str]:
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT thread_id FROM memory
            ORDER BY timestamp DESC LIMIT 1
        """)
        row = cursor.fetchone()
        return row[0] if row else None
    

    def conversation_history(self) -> Optional[str]:
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT thread_id FROM memory
        """)
        rows = cursor.fetchall()
        print(rows)
        return rows if rows else None

