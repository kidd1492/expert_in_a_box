from flask import Blueprint, request, jsonify
from rag.services.web_services import retrieval_service

retrieval_bp = Blueprint('retrieval', __name__, url_prefix='/retrieval')

@retrieval_bp.route('/document/<title>')
def view_document(title):
    results = retrieval_service.retrieve_doc(title=title)
    return jsonify({
        "title": title,
        "chunks": results
    })
 

@retrieval_bp.route('/retrieve')
def retrieve():
    query = request.args.get("query", "")
    titles = request.args.get("titles", "all")

    results = retrieval_service.retrieve(query=query, titles=titles, top_k=3)
    return jsonify(results)

