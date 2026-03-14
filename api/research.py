# webapp/auth.py
from flask import Blueprint, jsonify, render_template
from core.tools import tool_file
from api.dependencies import research_service
import os

research_bp = Blueprint('research', __name__, url_prefix='/research')


@research_bp.route("/home")
def home():
    summary = "hello this is a summary"
    if not os.path.exists("core/data/topic_files/sqlite.json"):
        return render_template("research_learning.html", videos=[], summary=summary)

    load_last = tool_file.load_topic_data("core/data/topic_files/sqlite.json")
    videos = load_last['videos']
    summary = load_last['overview']
    subtopics = load_last['subtopics']
    links = load_last['links']
    return render_template('research_learning.html', videos=videos, summary=summary, subtopics=subtopics, links=links)


@research_bp.route('/new_topic/<term>')
def new_topic(term):
    result = research_service.prepare_topic(term)
    return jsonify(result)


@research_bp.route('/subtopic/<term>')
def subtopic(term):
    result = research_service.prepare_subtopic(term)
    return jsonify(result)


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