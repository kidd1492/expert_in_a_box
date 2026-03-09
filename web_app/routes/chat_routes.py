from flask import Blueprint, request, jsonify
from rag.services.web_services import retrieval_service, chat_service, memory_service
from utils.helper_functions import generate_new_thread_id

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
    thread_id = memory_service.last_thread_id()
    if thread_id:
        thread_id = thread_id
    else:
        thread_id = generate_new_thread_id()

    result = memory_service.load(thread_id)
    if not result:
        print(f"No memory found for thread {thread_id}. Starting fresh.")
        results = chat_service.invoke_chatbot(user_content=[query])
        messages=[f'{query}", ' + m.content for m in [results]]
        memory_service.save(thread_id, '', messages)
    else:
        print(f"Loaded memory for thread {thread_id}")
        summary, messages_list = result
        messages_list.append(query)
        results = chat_service.invoke_chatbot(messages_list)
        messages=[m.content for m in [results]]
        messages.append(results.content)
        memory_service.save(thread_id, '', messages)

    return jsonify({"answer": f"{results.content}"})
