# webapp/routes.py
from flask import Blueprint, request, jsonify
from .models import ingestion_service, retrieval_service

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return "RAG Web Interface Running"

@main_bp.route('/documents')
def list_documents():
    docs = ingestion_service.vector_store.list_docs()
    print(docs)
    return docs

@main_bp.route('/ingest', methods=['POST'])
def ingest():
    file = request.files['file']
    filepath = f"uploads/{file.filename}"
    file.save(filepath)
    result = ingestion_service.add_file(filepath)
    return jsonify({"status": result})

@main_bp.route('/retrieve', methods=['POST'])
def retrieve():
    data = request.json
    query = data.get("query")
    titles = data.get("titles", "all")
    results = retrieval_service.retrieve(query, titles=titles)
    return jsonify(results)
