from flask import Blueprint, request, jsonify
from api.dependencies import ingestion_service
from core.tools import tool_file
import os

ingestion_bp = Blueprint('ingestion', __name__, url_prefix='/ingestion')


@ingestion_bp.route('/ingest', methods=['POST'])
def ingest():
    file = request.files.get('file')
    if not file:
        return jsonify({"status": "no file"}), 400

    file_path = f"core/data/uploads/{file.filename}"
    if os.path.exists(file_path):
        return jsonify({"status": "file already exist"}), 400 

    # Ingest into vector store
    try:
        result = ingestion_service.add_file(file_path)
        return jsonify({"status": result})
    except Exception as e:
        return jsonify({"error": f"Ingestion failed: {str(e)}"}), 400



@ingestion_bp.route('/add_wiki/<term>')
def add_wiki(term):
    if not term.strip():
        return jsonify({"error": "Empty search term"}), 400

    # Fetch wiki content
    try:
        content = tool_file.wiki_search(term)
        if not content:
            return jsonify({"error": "No content returned from wiki search"}), 400
    except Exception as e:
        return jsonify({"error": f"Wiki search failed: {str(e)}"}), 500

    # Build file path
    new_term = term.replace(" ", "_")
    file_path = f"core/data/uploads/{new_term}.txt"

    # Reject duplicates (same behavior as /ingest)
    if os.path.exists(file_path):
        return jsonify({"error": "file already exist"}), 400

    # Save file
    try:
        with open(file_path, "w", encoding="UTF-8") as file:
            file.write(content)
    except Exception as e:
        return jsonify({"error": f"Failed to save wiki file: {str(e)}"}), 500

    # Ingest into vector store
    try:
        result = ingestion_service.add_file(file_path)
        return jsonify({"status": result})
    except Exception as e:
        return jsonify({"error": f"Ingestion failed: {str(e)}"}), 400


@ingestion_bp.route('/remove_selected/<titles>', methods=["DELETE"])
def remove(titles):
    ingestion_service.remove_file(titles)
    return {"status": "ok"}
