import json

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
