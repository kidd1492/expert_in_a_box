# webapp/auth.py
from flask import Blueprint, request, jsonify, render_template
from rag.core import tool_file
import json

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route("/learning")
def learning():
    return render_template('research_learning.html')


@auth_bp.route("/youtube/<query>")
def youtube_search(query):
    videos = tool_file.get_youtube_videos(query=query, max_results=10)

    # Return only the fields the UI needs
    cleaned = []
    for v in videos:
        cleaned.append({
            "title": v["snippet"]["title"],
            "description": v["snippet"]["description"],
            "thumbnail": v["snippet"]["thumbnails"]["medium"]["url"],
            #"videoId": v["id"]["videoId"]
        })

    return jsonify(cleaned)
