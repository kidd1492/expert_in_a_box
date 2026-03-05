# webapp/auth.py
from flask import Blueprint, request, jsonify, render_template
from rag.tools import tool_file
import os

research_bp = Blueprint('research', __name__, url_prefix='/research')


@research_bp.route("/home")
def home():
    if not os.path.exists("rag/data/youtube_files/youtube.json"):
        return render_template("research_learning.html", videos=[])

    load_last = tool_file.load_youtube_data("rag/data/youtube_files/youtube.json")
    cleaned = []
    for v in load_last:
        cleaned.append({
            "title": v["snippet"]["title"],
            "description": v["snippet"]["description"],
            "thumbnail": v["snippet"]["thumbnails"]["medium"]["url"],
            "videoId": v["id"]["videoId"]
        })

    return render_template('research_learning.html', videos=cleaned)


@research_bp.route("/youtube/<query>")
def youtube_search(query):
    videos = tool_file.get_youtube_videos(query=query, max_results=10)

    # Return only the fields the UI needs
    cleaned = []
    for v in videos:
        cleaned.append({
            "title": v["snippet"]["title"],
            "description": v["snippet"]["description"],
            "thumbnail": v["snippet"]["thumbnails"]["medium"]["url"],
            "videoId": v["id"]["videoId"]
        })

    return jsonify(cleaned)

@research_bp.route('/wiki/<term>')
def wiki_search(term):
    result = tool_file.wiki_search(term)
    return jsonify({"status": result})
