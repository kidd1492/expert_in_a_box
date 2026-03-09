from flask import Blueprint, request, jsonify
from rag.services.web_services import retrieval_service, chat_service, memory_service
from rag.agents.ReAct_agent import app
from langchain.messages import HumanMessage


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


@chat_bp.route("/chatbot")
def chatbot():
    query = request.args.get("query", "")
    user_input = [HumanMessage(content=query)]
    thread_id = memory_service.get_last_thread_id()
    result = memory_service.load_memory(thread_id)
    print(result)
    if not result:
        print(f"No memory found for thread {thread_id}. Starting fresh.")
        app.invoke({"messages": user_input, 'thread_id': thread_id})
    else:
        summary, messages_list = result
        messages_list.append([user_input])
        messages = HumanMessage(content=query)
        print(f"Loaded memory for thread {thread_id}")
        responce = app.invoke({"messages": user_input, 'thread_id': thread_id})
        last_message = responce["messages"][-1].content
    return jsonify({"answer": f"{last_message}"})
