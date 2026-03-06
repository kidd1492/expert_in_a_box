import sqlite3, json
import numpy as np
from typing import List, Dict, Any
from utils.helper_functions import get_scored, get_titles

# DB Connection Helper
def connect_db(db_path="rag/data/rag_store.db"):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    return conn, cursor


class VectorStore:

    def __init__(self, db_path="rag/data/rag_store.db"):
        self.db_path = db_path
        self._init_schema()


    def _init_schema(self):
        conn, cursor = connect_db(self.db_path)

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


    def add_document(self,
        content: str,
        title: str,
        metadata: Dict[str, Any],
        embedding: np.ndarray
    ) -> int:
        """ Insert a document with JSON metadata + embedding. """
        metadata_json = json.dumps(metadata, ensure_ascii=False)
        embedding_bytes = embedding.astype(np.float32).tobytes()

        conn, cursor = connect_db(self.db_path)
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
        top_k: int = 3,
        titles: str = "all"
    ) -> List[Dict[str, Any]]:
        
        conn, cursor = connect_db()
        if titles == "all":
            cursor.execute("SELECT id, content, metadata, embedding FROM documents")
        else:
            placeholders, title_list = get_titles(titles)
            cursor.execute(
                f"SELECT id, content, metadata, embedding FROM documents WHERE title IN ({placeholders})",
                title_list
            )
        rows = cursor.fetchall()
        conn.close()

        if not rows:
            return []

        scored = get_scored(query_embedding, rows, search_type)
        return scored[:top_k]


    def list_docs(self):
        conn, cursor = connect_db(self.db_path)
        cursor.execute("SELECT DISTINCT title FROM documents")
        docs = [row[0] for row in cursor.fetchall()]
        conn.close()
        return docs


    def retrieve_document(self, title: str):
        conn, cursor = connect_db(self.db_path)
        cursor.execute("SELECT content FROM documents WHERE title == ?", (title,))
        document = cursor.fetchall()
        conn.close()
        return document
    

    def remove_file(self, titles):
        conn, cursor = connect_db(self.db_path)

        for title in titles:
            cursor.execute("DELETE FROM documents WHERE title = ?", (title,))

        conn.commit()
        conn.close()
        return


