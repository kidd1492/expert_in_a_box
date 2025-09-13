import sqlite3, json
import numpy as np
from typing import List, Tuple, Optional

class RAGDatabase:
    def __init__(self, db_path="data/rag_store.db"):
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self._init_schema()

    def _init_schema(self):
        cursor = self.conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS documents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                content TEXT,
                title TEXT,
                metadata TEXT
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS embeddings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                document_id INTEGER,
                embedding_vector BLOB,
                FOREIGN KEY(document_id) REFERENCES documents(id)
            )
        """)
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


    def add_document(self, content: str, title: str, metadata: str, embedding: np.ndarray):
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO documents (content, title, metadata)
            VALUES (?, ?, ?)
        """, (content, title, metadata))
        doc_id = cursor.lastrowid
        cursor.execute("""
            INSERT INTO embeddings (document_id, embedding_vector)
            VALUES (?, ?)
        """, (doc_id, embedding.tobytes()))
        self.conn.commit()

    def query_documents(self, query_embedding: np.ndarray, search_type="similarity", top_k=3) -> List[Tuple[str, str]]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT document_id, embedding_vector FROM embeddings")
        rows = cursor.fetchall()

        similarities = []
        for doc_id, blob in rows:
            vec = np.frombuffer(blob, dtype=np.float32)
            sim = np.dot(query_embedding, vec) / (np.linalg.norm(query_embedding) * np.linalg.norm(vec))
            similarities.append((doc_id, vec, sim))

        if search_type == "mmr":
            selected = []
            remaining = sorted(similarities, key=lambda x: x[2], reverse=True)
            while remaining and len(selected) < top_k:
                best = remaining.pop(0)
                selected.append(best)
                remaining = [r for r in remaining if np.dot(best[1], r[1]) / (np.linalg.norm(best[1]) * np.linalg.norm(r[1])) < 0.95]
        else:
            selected = sorted(similarities, key=lambda x: x[2], reverse=True)[:top_k]

        doc_ids = [doc_id for doc_id, _, _ in selected]
        placeholders = ",".join("?" for _ in doc_ids)
        cursor.execute(f"SELECT content, metadata FROM documents WHERE id IN ({placeholders})", doc_ids)
        return cursor.fetchall()
