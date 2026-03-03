import json

def normalize_metadata(meta):
    if isinstance(meta, dict):
        return meta
    try:
        loaded = json.loads(meta)
        if isinstance(loaded, dict):
            return loaded
        return {"title": str(loaded)}
    except Exception:
        return {"title": str(meta)}


def chunk_to_dict(record):
    """
    Convert a retrieval record into a unified chunk dict.
    Expected record shape:
    {
        "id": int | None,
        "content": str,
        "metadata": dict,
        "score": float | None
    }
    """
    content = record.get("content", "")
    meta = normalize_metadata(record.get("metadata", {}))

    return {
        "id": record.get("id"),
        "content": content,
        "title": meta.get("title", "Unknown Document"),
        "page_number": meta.get("page_number"),
        "score": record.get("score"),
        "metadata": meta
    }


def build_context(records):
    """
    Convert a list of retrieval records into a list of unified chunk dicts.
    """
    return [chunk_to_dict(record) for record in records]
