from flask import Blueprint, request, jsonify
from rag.services.web_services import retrieval_service, chat_service

chat_bp = Blueprint('chat_route', __name__, url_prefix='/chat_route')


@chat_bp.route("/chat")
def chat():
    query = request.args.get("query", "")
    titles = request.args.get("titles", "all")
    mode = request.args.get("mode", "answer")

    context = retrieval_service.retrieve(query, titles=titles)
  
    if mode == "answer":
        result = chat_service.answer_question(query, context)
    elif mode == "summarize":
        result = chat_service.summarize(context)
    elif mode == "outline":
        result = chat_service.outline(context)
    else:
        result = "Unknown mode."

    return jsonify({
        "answer": result,
        "context": context
    })