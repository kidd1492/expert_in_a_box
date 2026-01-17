import sqlite3
import json
import numpy as np
from typing import List, Tuple, Dict, Any


class VectorStore:
    """
    SQLite‑backed vector store with JSON metadata.
    Stores:
        - content (TEXT)
        - title (TEXT)
        - metadata (TEXT, JSON-encoded)
        - embedding (BLOB, raw float32 bytes)
    """

    def __init__(self, db_path: str = "data/rag_store.db"):
        self.db_path = db_path
        self._init_schema()


    def _init_schema(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS documents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                content TEXT NOT NULL,
                title TEXT,
                metadata TEXT,              -- JSON string
                embedding BLOB NOT NULL
            )
        """)

        conn.commit()
        conn.close()


    def add_document(
        self,
        content: str,
        title: str,
        metadata: Dict[str, Any],
        embedding: np.ndarray
    ) -> int:
        """
        Insert a document with JSON metadata + embedding.
        Returns the inserted document ID.
        """

        metadata_json = json.dumps(metadata, ensure_ascii=False)
        embedding_bytes = embedding.astype(np.float32).tobytes()

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO documents (content, title, metadata, embedding)
            VALUES (?, ?, ?, ?)
        """, (content, title, metadata_json, embedding_bytes))

        doc_id = cursor.lastrowid
        conn.commit()
        conn.close()

        return doc_id


    def query_documents(
        self,
        query_embedding: np.ndarray,
        search_type: str = "similarity",
        top_k: int = 3
    ) -> List[Tuple[str, Dict[str, Any]]]:
        """
        Returns a list of (content, metadata_dict) tuples.
        Supports:
            - cosine similarity
            - dot product
        """

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("SELECT id, content, metadata, embedding FROM documents")
        rows = cursor.fetchall()
        conn.close()

        if not rows:
            return []

        # Normalize query embedding
        q = query_embedding.astype(np.float32)
        q_norm = q / (np.linalg.norm(q) + 1e-8)

        scored = []

        for doc_id, content, metadata_json, emb_blob in rows:
            emb = np.frombuffer(emb_blob, dtype=np.float32)

            # Normalize stored embedding
            emb_norm = emb / (np.linalg.norm(emb) + 1e-8)

            if search_type == "dot":
                score = float(np.dot(q, emb))
            else:
                # cosine similarity
                score = float(np.dot(q_norm, emb_norm))

            metadata = json.loads(metadata_json) if metadata_json else {}
            scored.append((score, content, metadata))

        # Sort by score descending
        scored.sort(key=lambda x: x[0], reverse=True)

        # Return top_k
        return [(content, metadata) for score, content, metadata in scored[:top_k]]
