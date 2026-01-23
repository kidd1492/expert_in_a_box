import subprocess, os
from web_app import create_app

def start_ollama():
    """Start the Ollama server and ensure the AI model is ready."""
    installed = ollama_installed()
    if installed == True:
        try:
            print("Starting Ollama Server...")
            subprocess.Popen(
                ['cmd', '/c', 'start', 'ollama', 'serve'],
                shell=True
            )
            print("Finished Ollama Setup.")
        except Exception as e:
            print("Please make sure Ollama is installed.")
            print(e)


def ollama_installed():
    """Check if Ollama is installed before proceeding."""
    try:
        subprocess.run(["ollama", "--version"], capture_output=True, check=True)
        return True
    except subprocess.CalledProcessError:
        print("Ollama is not installed. Please install it before proceeding.")
        print("ollama.com to intall:")
        return False


def ensure_directories():
    os.makedirs("rag/data", exist_ok=True)  # ensures DB directory exists
    os.makedirs("rag/data/wiki", exist_ok=True)
    os.makedirs("rag/data/uploads", exist_ok=True)
    os.makedirs("rag/data/logs", exist_ok=True)



if __name__ == "__main__":
    ensure_directories()
    start_ollama()
    app = create_app()
    app.run(debug=True)
