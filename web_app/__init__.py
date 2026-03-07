from flask import Flask
import subprocess, os


def start_ollama():
    try:
        print("Starting Ollama Server...")
        subprocess.Popen(
            ['cmd', '/c', 'start', 'ollama', 'serve'],
            shell=True
        )
        print("Finished Ollama Setup.")
    except Exception as e:
        print("Error starting Ollama:")
        print(e)


def ensure_directories():
    os.makedirs("rag/data", exist_ok=True)  # ensures directories exists
    os.makedirs("rag/data/uploads", exist_ok=True)
    os.makedirs("rag/logging/logs", exist_ok=True)
    os.makedirs("rag/data/youtube_files", exist_ok=True)


def create_app():
    ensure_directories()
    start_ollama()
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'dev-key'
    app.config['DATABASE'] = 'data/rag_store.db'

    # Register blueprints
    from .routes.auth import auth_bp
    from .routes.func_routes import main_bp
    from .routes.research import research_bp
    from .routes.chat_routes import chat_bp 
    from .routes.ingestion_routes import ingestion_bp
    from .routes.retrieval_routes import retrieval_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(research_bp)
    app.register_blueprint(chat_bp)
    app.register_blueprint(ingestion_bp)
    app.register_blueprint(retrieval_bp)

    return app
