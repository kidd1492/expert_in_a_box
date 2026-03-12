# webapp/auth.py
from flask import Blueprint, jsonify, render_template
from core.tools import tool_file
import os

research_bp = Blueprint('research', __name__, url_prefix='/research')


@research_bp.route("/home")
def home():
    if not os.path.exists("core/data/youtube_files/youtube.json"):
        return render_template("research_learning.html", videos=[])

    load_last = tool_file.load_youtube_data("core/data/youtube_files/youtube.json")
    cleaned = tool_file.parse_youtube_data(load_last)
    return render_template('research_learning.html', videos=cleaned)


@research_bp.route("/youtube/<query>")
def youtube_search(query):
    videos = tool_file.get_youtube_videos(query=query, max_results=10)
    cleaned = tool_file.parse_youtube_data(videos)
    # Return only the fields the UI needs
    return jsonify(cleaned)


@research_bp.route('/wiki/<term>')
def wiki_search(term):
    # Fetch wiki content
    try:
        content = tool_file.wiki_search(term)
        if not content:
            return jsonify({"error": "No content returned from wiki search"}), 400
    except Exception as e:
        return jsonify({"error": f"Wiki search failed: {str(e)}"}), 500
    return jsonify({"status": content})
