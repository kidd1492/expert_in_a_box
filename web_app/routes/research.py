# webapp/auth.py
from flask import Blueprint, request, jsonify, render_template
from rag.tools import tool_file
import json

research_bp = Blueprint('research', __name__, url_prefix='/research')

@research_bp.route("/home")
def home():
    return render_template('research_learning.html')


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
