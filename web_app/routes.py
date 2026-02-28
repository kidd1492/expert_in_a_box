# webapp/routes.py
from flask import Blueprint, request, jsonify, render_template
from .models import ingestion_service, retrieval_service, chat_service
from rag.core import tool_file
import json

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    '''TODO see how the memory is going to be used??
    history = memory_service.memory_store.conversation_history()'''
    docs = retrieval_service.list_docs()
    return render_template('index.html', documents=docs)


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


@main_bp.route('/add_wiki/<term>')
def add_wiki(term):
    content = tool_file.wiki_search(term)
    new_term = term.replace(" ", "_")
    filepath = f"rag/data/wiki/{new_term}.txt"
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    result = ingestion_service.add_file(filepath)

    return jsonify({"status": result})


@main_bp.route('/ingest', methods=['POST'])
def ingest():
    file = request.files.get('file')
    if not file:
        return jsonify({"status": "no file"}), 400

    filepath = f"rag/data/uploads/{file.filename}"
    file.save(filepath)

    result = ingestion_service.add_file(filepath)
    return jsonify({"status": result})


@main_bp.route('/retrieve')
def retrieve():
    query = request.args.get("query", "")
    titles = request.args.get("titles", "all")

    raw_results = retrieval_service.retrieve(query=query, titles=titles, top_k=3)

    def normalize(meta):
        # meta may be a dict, a JSON string, or a raw string
        if isinstance(meta, dict):
            return meta
        try:
            loaded = json.loads(meta)
            if isinstance(loaded, dict):
                return loaded
            return {"title": str(loaded)}
        except Exception:
            return {"title": str(meta)}

    results = []
    for content, metadata in raw_results:
        meta = normalize(metadata)
        results.append({
            "title": meta.get("title", "Unknown Document"),
            "page_number": meta.get("page_number"),
            "text": content,
            "metadata": meta
        })

    return jsonify(results)


import json

@main_bp.route("/chat")
def chat():
    query = request.args.get("query", "")
    titles = request.args.get("titles", "all")
    mode = request.args.get("mode", "answer")

    raw_chunks = retrieval_service.retrieve(query, titles=titles)

    def normalize(meta):
        if isinstance(meta, dict):
            return meta
        try:
            loaded = json.loads(meta)
            if isinstance(loaded, dict):
                return loaded
            return {"title": str(loaded)}
        except Exception:
            return {"title": str(meta)}

    # Convert raw chunks into structured objects
    context = []
    for content, metadata in raw_chunks:
        meta = normalize(metadata)
        context.append({
            "title": meta.get("title", "Unknown Document"),
            "page_number": meta.get("page_number"),
            "text": content,
            "metadata": meta
        })

    # Model call
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

