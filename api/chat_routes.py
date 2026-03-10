from flask import Blueprint, request, jsonify
from core.services.web_services import retrieval_service, chat_service, memory_service
from utils.helper_functions import generate_new_thread_id
from langchain.messages import HumanMessage, AIMessage, SystemMessage


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

    # Reduce if needed
    new_summary, reduced_messages = memory_service.reduce_if_needed(
        thread_id, messages, chat_service
    )

    if new_summary is not None:
        summary = new_summary
        messages = reduced_messages

    # Invoke model with summary + messages
    full_context = []
    if summary:
        full_context.append(SystemMessage(content=f"Conversation summary: {summary}"))
    full_context.extend(messages)

    result = chat_service.invoke_chatbot(full_context)

    # Add assistant message
    messages.append(AIMessage(content=result.content))

    # Save
    memory_service.save(thread_id, summary, messages)

    return jsonify({"answer": result.content})


@chat_bp.route("/chat/history")
def chat_history():
    thread_id = memory_service.last_thread_id()
    if not thread_id:
        return jsonify({"summary": "", "messages": []})

    loaded = memory_service.load(thread_id)
    if not loaded:
        return jsonify({"summary": "", "messages": []})

    summary, messages = loaded

    # Convert messages to simple JSON for the UI
    ui_messages = []
    for m in messages:
        ui_messages.append({
            "type": m.type,       # "human" or "ai"
            "content": m.content
        })

    return jsonify({
        "summary": summary,
        "messages": ui_messages
    })
