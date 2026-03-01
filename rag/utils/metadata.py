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


def chunk_to_dict(content, meta):
    return {
        "title": meta.get("title", "Unknown Document"),
        "page_number": meta.get("page_number"),
        "text": content,
        "metadata": meta
    }
