from flask import Blueprint, request, jsonify, render_template
from rag.services.web_services import retrieval_service
from rag.tools import tool_file
from rag.utils.metadata import build_context

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    docs = retrieval_service.list_docs()
    return render_template('index.html', documents=docs)


@main_bp.route('/document/<title>')
def view_document(title):
    results = retrieval_service.retrieve_doc(title=title)
    return jsonify({
        "title": title,
        "chunks": results
    })
 

@main_bp.route('/retrieve')
def retrieve():
    query = request.args.get("query", "")
    titles = request.args.get("titles", "all")

    raw_results = retrieval_service.retrieve(query=query, titles=titles, top_k=3)
    results = build_context(raw_results)

    return jsonify(results)
