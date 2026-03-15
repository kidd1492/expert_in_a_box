# agents/tool_file.py
import wikipedia as wk
import json, os, requests
from dotenv import load_dotenv
from datetime import datetime, timedelta
from langchain_ollama import ChatOllama
from tavily import TavilyClient


def wiki_search(term):
    """This function will gather research information from wikipedia and save it to a file."""
    try:
        page = wk.page(term)
        response = page.content
    except wk.exceptions.DisambiguationError:
        print(f"Multiple options found for '{term}'. Please specify.")
        response = f"Multiple options found for '{term}'. Please specify."
    except wk.exceptions.PageError:
        print(f"No Wikipedia page found for '{term}'")
        response = f"No Wikipedia page found for '{term}'"
    return response


def get_youtube_videos(query, max_results=3):
    load_dotenv()
    youtube_api_key = os.getenv("YOUTUBE_API_KEY")

    # Calculate yesterday and now in UTC
    now = datetime.now()
    yesterday = now - timedelta(days=15)

    published_after = yesterday.isoformat("T") + "Z"
    published_before = now.isoformat("T") + "Z"

    url = (
        "https://www.googleapis.com/youtube/v3/search?"
        f"part=snippet&maxResults={max_results}&q={query}&type=video"
        f"&publishedAfter={published_after}&publishedBefore={published_before}"
        f"&key={youtube_api_key}"
    )

    response = requests.get(url)
    if response.status_code == 200:
        videos = response.json().get("items", [])
        video_data = parse_video_data(videos)
        return video_data
    else:
        print("Failed to fetch videos.")
        print(response.text)
        return []


def parse_video_data(videos):
    cleaned = []
    for v in videos:
        cleaned.append({
            "title": v["snippet"]["title"],
            "description": v["snippet"]["description"],
            "thumbnail": v["snippet"]["thumbnails"]["medium"]["url"],
            "videoId": v["id"]["videoId"]
        })
    return cleaned


def save_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

def load_topic_data(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)


def summarize_topic(term: str) -> str:
    model = ChatOllama(model="qwen2.5:3b")
    prompt = f"Give a clear one or two paragraph overview of the topic '{term}'."
    result = model.invoke(prompt)
    return result.content


def generate_subtopics(term: str) -> list[str]:
    model = ChatOllama(model="qwen2.5:3b")
    prompt = f"List 5 essential subtopics someone must learn to understand '{term}'. a list of terms only no other reponse. example- 'subtopics: [subtopic,subtopic, ...]'"
    response = model.invoke(prompt)
    subtopic_list = response.content[1:-1].split(",")
    return subtopic_list

def web_search(query: str)-> list:
    load_dotenv()
    TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

    trvily_client = TavilyClient(api_key=TAVILY_API_KEY)
    result = trvily_client.search(query)
    links = []
    for r in  result['results']:
        links.append(r["url"])
    return links


if __name__ == "__main__":
    result = web_search("sqlite")
    print(result)