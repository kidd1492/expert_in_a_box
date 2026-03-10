# webapp/auth.py
from flask import Blueprint, jsonify, render_template
from core.tools import tool_file
from utils.helper_functions import parse_youtube_data
import os

research_bp = Blueprint('research', __name__, url_prefix='/research')


@research_bp.route("/home")
def home():
    if not os.path.exists("core/data/youtube_files/youtube.json"):
        return render_template("research_learning.html", videos=[])

    load_last = tool_file.load_youtube_data("core/data/youtube_files/youtube.json")
    cleaned = parse_youtube_data(load_last)
    return render_template('research_learning.html', videos=cleaned)


@research_bp.route("/youtube/<query>")
def youtube_search(query):
    videos = tool_file.get_youtube_videos(query=query, max_results=10)
    cleaned = parse_youtube_data(videos)
    # Return only the fields the UI needs
    return jsonify(cleaned)


@research_bp.route('/wiki/<term>')
def wiki_search(term):
    result = tool_file.wiki_search(term)
    return jsonify({"status": result})
