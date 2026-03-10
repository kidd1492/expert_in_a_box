from flask import Blueprint, request, jsonify
from core.services.web_services import retrieval_service

retrieval_bp = Blueprint('retrieval', __name__, url_prefix='/retrieval')

@retrieval_bp.route('/document/<title>')
def view_document(title):
    if not title or title.strip() == "":
        return jsonify({
            "success": False,
            "error": "Missing or invalid title"
        }), 400

    try:
        results = retrieval_service.retrieve_doc(title=title)

        return jsonify({
            "success": True,
            "title": title,
            "chunks": results
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Retrieval failed: {str(e)}"
        }), 500

 

@retrieval_bp.route('/retrieve')
def retrieve():
    query = request.args.get("query", "").strip()
    titles = request.args.get("titles", "all").strip()

    if not query:
        return jsonify({
            "success": False,
            "error": "Query parameter is required"
        }), 400

    try:
        results = retrieval_service.retrieve(
            query=query,
            titles=titles,
            top_k=3
        )

        return jsonify({
            "success": True,
            "results": results
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Retrieval failed: {str(e)}"
        }), 500


