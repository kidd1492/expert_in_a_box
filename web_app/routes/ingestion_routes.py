from flask import Blueprint, request, jsonify
from rag.services.web_services import ingestion_service
from rag.tools import tool_file
from utils.helper_functions import write_file

ingestion_bp = Blueprint('ingestion', __name__, url_prefix='/ingestion')

@ingestion_bp.route('/add_wiki/<term>')
def add_wiki(term):
    content = tool_file.wiki_search(term)
    new_term = term.replace(" ", "_")
    filepath = f"rag/data/wiki/{new_term}.txt"
    write_file(filepath, content)
    result = ingestion_service.add_file(filepath)
    return jsonify({"status": result})


@ingestion_bp.route('/ingest', methods=['POST'])
def ingest():
    file = request.files.get('file')
    if not file:
        return jsonify({"status": "no file"}), 400

    filepath = f"rag/data/uploads/{file.filename}"
    file.save(filepath)

    result = ingestion_service.add_file(filepath)
    return jsonify({"status": result})