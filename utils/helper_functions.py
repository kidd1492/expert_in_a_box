import json, uuid
from pathlib import Path
import numpy as np

def read_file(file_path: str):
    with open(file_path, "r", encoding="UTF-8") as file:
        return file.read()
    

def write_file(file_path: str, content):
    with open(file_path, "w", encoding="UTF-8") as file:
        return file.write(content)


def save_json(file_path, content):
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(content, f, indent=2, ensure_ascii=False)



def parse_youtube_data(videos):
    cleaned = []
    for v in videos:
        cleaned.append({
            "title": v["snippet"]["title"],
            "description": v["snippet"]["description"],
            "thumbnail": v["snippet"]["thumbnails"]["medium"]["url"],
            "videoId": v["id"]["videoId"]
        })
    return cleaned

def generate_new_thread_id():
    return str(uuid.uuid4())


def delete_ingest_file(titles: list[str]) -> None:
    for title in titles:
        file_path = Path("core/data/uploads") / title

        if file_path.exists():
            file_path.unlink()
        else:
            print(f"File not found: {file_path}")


def get_titles(titles):
    title_list = [t.strip() for t in titles.split(",") if t.strip()]
    placeholders = ",".join("?" * len(title_list))
    return placeholders, title_list


def get_scored(query_embedding, rows, search_type):
    # Normalize query embedding
    q = query_embedding.astype(np.float32)
    q_norm = q / (np.linalg.norm(q) + 1e-8)

    scored = []

    for doc_id, content, metadata_json, emb_blob in rows:
        emb = np.frombuffer(emb_blob, dtype=np.float32)

        # Normalize stored embedding
        emb_norm = emb / (np.linalg.norm(emb) + 1e-8)

        # Compute similarity score
        if search_type == "dot":
            score = float(np.dot(q, emb))
        else:
            score = float(np.dot(q_norm, emb_norm))

        metadata = json.loads(metadata_json) if metadata_json else {}

        scored.append({
            "id": doc_id,
            "content": content,
            "metadata": metadata,
            "score": score
        })
    scored.sort(key=lambda x: x["score"], reverse=True)
    return scored