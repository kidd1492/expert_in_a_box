# agents/tool_file.py
import wikipedia as wk
import json
from dotenv import load_dotenv
import os
import requests
from datetime import datetime, timedelta


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


def get_youtube_videos(query="machine learning transformer", max_results=10):
    load_dotenv()
    youtube_api_key = os.getenv("YOUTUBE_API_KEY")

    # Calculate yesterday and now in UTC
    now = datetime.utcnow()
    yesterday = now - timedelta(days=15)

    published_after = yesterday.isoformat("T") + "Z"
    published_before = now.isoformat("T") + "Z"

    url = (
        "https://www.googleapis.com/youtube/v3/search?"
        f"part=snippet&maxResults={max_results}&q={query}&type=video"
        #f"&publishedAfter={published_after}&publishedBefore={published_before}"
        f"&key={youtube_api_key}"
    )

    response = requests.get(url)
    if response.status_code == 200:
        videos = response.json().get("items", [])

        # Save to JSON
        filepath = f"rag/data/youtube_files/youtube.json"
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(videos, f, indent=2, ensure_ascii=False)

        print(f"Saved {len(videos)} videos")
        return videos
    else:
        print("Failed to fetch videos.")
        print(response.text)
        return []


def load_youtube_data(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        return json.load(file)

