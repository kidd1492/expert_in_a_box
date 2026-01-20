# webapp/routes.py
from flask import Blueprint, request, jsonify, render_template
from .models import ingestion_service, retrieval_service, memory_service
from rag.agents import tool_file


main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    history = memory_service.memory_store.conversation_history()
    docs = ingestion_service.vector_store.list_docs()
    return render_template('index.html', documents=docs, history=history)


@main_bp.route('/document/<title>')
def view_document(title):
    # Retrieve ALL chunks for this document
    results = retrieval_service.retrieve_doc(title=title)
    return jsonify({
        "title": title,
        "chunks": results
    })


@main_bp.route('/wiki/<term>')
def wiki_search(term):
    result = tool_file.wiki_search(term)
    return jsonify({"status": result})



@main_bp.route('/ingest/<file_path>', methods=['POST'])
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
