from flask import Blueprint, request, jsonify
from rag.services.web_services import retrieval_service, chat_service, memory_service
from utils.helper_functions import generate_new_thread_id
from langchain.messages import HumanMessage, AIMessage


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
        "answer": result.content,
        "context": context
    })


@chat_bp.route("/chatbot")
def chatbot():
    query = request.args.get("query", "")
    thread_id = memory_service.last_thread_id() or generate_new_thread_id()

    loaded = memory_service.load(thread_id)
    if loaded:
        summary, messages = loaded
    else:
        summary, messages = "", []

    # Add user message
    messages.append(HumanMessage(content=query))

    # Invoke model with full history
    result = chat_service.invoke_chatbot(messages)

    # Add result message
    messages.append(AIMessage(content=result.content))

    # Save back to DB
    memory_service.save(thread_id, summary, messages)

    return jsonify({"answer": result.content})

