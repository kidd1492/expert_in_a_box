import subprocess, os
from web_app import create_app

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
    os.makedirs("rag/data", exist_ok=True)  # ensures DB directory exists
    os.makedirs("rag/data/wiki", exist_ok=True)
    os.makedirs("rag/data/uploads", exist_ok=True)
    os.makedirs("rag/data/logs", exist_ok=True)
    os.makedirs("rag/data/youtube_files", exist_ok=True)



if __name__ == "__main__":
    ensure_directories()
    start_ollama()
    app = create_app()
    app.run(debug=True)
