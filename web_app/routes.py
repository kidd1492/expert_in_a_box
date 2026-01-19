# webapp/routes.py
from flask import Blueprint, request, jsonify, render_template
from .models import ingestion_service, retrieval_service

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    from .models import ingestion_service
    from .models import memory_service
    history = memory_service.memory_store.conversation_history()
    docs = ingestion_service.vector_store.list_docs()
    return render_template('index.html', documents=docs, history=history)

@main_bp.route('/document/<title>')
def view_document(title):
    from .models import retrieval_service

    # Retrieve ALL chunks for this document
    results = retrieval_service.retrieve(
        query="", 
        search_type="similarity", 
        titles=title, 
        top_k=50
    )

    return jsonify({
        "title": title,
        "chunks": results
    })


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
