# **Expert‑in‑a‑Box**  
*A transparent, offline‑first Retrieval‑Augmented Generation (RAG) system with modular pipelines, local embeddings, and a clean Flask UI.*

`https://img.shields.io/badge/Python-3.10%2B-blue`
`https://img.shields.io/badge/License-MIT-green`

---

# Overview

**Expert‑in‑a‑Box** is a fully local, privacy‑preserving RAG system designed for clarity, transparency, and extensibility. It provides:

- A complete **document ingestion pipeline**  
- A fast **semantic retrieval engine**  
- A structured **chat pipeline** with memory  
- Built‑in **research tools** (Wikipedia + YouTube)  
- A clean, three‑panel **Flask web interface**  

Every step of the system is visible and inspectable — no hidden chains, no opaque agent behavior, no cloud calls. All embeddings, files, and conversation memory are stored locally using SQLite and the filesystem.

This project is ideal for:

- Personal knowledge bases  
- Research workflows  
- Local LLM experimentation  
- Agentic system development  
- Transparent RAG learning  

---

# Key Features

## Retrieval‑Augmented Generation Engine
- Local SQLite vector store  
- Chunking via `RecursiveCharacterTextSplitter`  
- Local embeddings using **Ollama**  
- Transparent metadata (title, chunk index, source)  
- Document‑level filtering  
- Top‑k similarity search  

## Document Ingestion Pipeline
Supports:
- `.pdf`
- `.txt`
- `.md`

Pipeline steps:
1. Read file  
2. Extract text  
3. Chunk text  
4. Embed chunks  
5. Store embeddings + metadata  
6. Save original file  

All processing is **offline** and **local**.

## Chat Pipeline
- Builds prompts from retrieved context  
- Supports **Ask**, **Summarize**, and **Outline** modes  
- Uses local Ollama LLMs  
- Stores conversation memory per thread  
- Optional ReAct‑style agent mode  

## Memory System
- SQLite‑backed memory store  
- Thread‑based summaries  
- Full message history  
- Automatic loading/saving  

## Research Tools
- Wikipedia search + ingestion  
- YouTube metadata search  
- Auto‑generated wiki documents  

---

# Architecture

```
expert_in_a_box/
├── rag/
  ├── agents/                 # ReAct_agent
  ├── core/                   # Chunking, ingestion, embedding, vectors, memory
  ├── services/               # Ingestion, retrieval, chat, memory, web services
  └── data/
    ├── uploads/              # User-uploaded files
    ├── rag_store.db          # SQLite vector store
  ├── logging                 # logs, log_handler
  ├── tools                   # tools_file

├── utils/                    # Helper functions
├── web_app/                  # Flask UI, routes, templates, static JS/CSS
  ├── routes                  # auth, chat, func, ingestion, research, retrieval
  ├── static                  # javascript, css
    ├──js_files               # chat, func_helper, ingestion, research, retrieval.js
  ├── templates               # index, layout, research
  ├── __inti__                # starts ollama server, makes directory, registers apps
├── run.py                    # entry point
├── main.py                   # developer tools

```

---

# Pipeline Architecture

## Ingestion Pipeline
```
read_document → chunk_text → embed_documents → add_document → save_file
```

## Retrieval Pipeline
```
embed_text(query) → query_documents → score + rank → return top_k
```

## Chat Pipeline
```
load_memory → retrieve_context → build_prompt → LLM.invoke → save_memory
```

These pipelines are modular, testable, and easy to extend.

---

# Flask Web Application

A clean, three‑column interface:

### **Left — Document Management**
- List all ingested documents  
- Select one or many  
- View chunks  
- Remove documents  

### **Middle — Retrieval + Chat**
- Query input  
- Retrieve top‑k chunks  
- Ask chatbot  
- Summarize  
- Outline  

### **Right — Research Tools**
- Wikipedia search  
- Add wiki content to vector store  
- YouTube search  

---

# 🛠️ Tools

### `wiki_search(term)`
Fetches Wikipedia content.

### `add_wiki(term)`
Fetches → saves → ingests wiki content.

### `add_file(filepath)`
Loads any supported file into the RAG system.

---

# ⚙️ Installation & Quick Start

### 1. Install Ollama  
Guide: [https://humansideoftek.blogspot.com/2025/09/ollama-local-model-deployment-guide.html](https://humansideoftek.blogspot.com/2025/09/ollama-local-model-deployment-guide.html)

### 2. Pull embedding model  
```bash
ollama pull mxbai-embed-large:335m
```

### 3. Clone the repo  
```bash
git clone https://github.com/kidd1492/expert_in_a_box.git
cd expert_in_a_box
```

### 4. Create virtual environment  
```bash
python -m venv venv
source venv/bin/activate  # or Windows equivalent
```

### 5. Install dependencies  
```bash
pip install -r requirements.txt
```

### 6. Run the app  
```bash
python run.py
```

The app will:

- Ensure required directories exist  
- Initialize the SQLite vector store  
- Start the local Ollama server  
- Launch the Flask UI  

---

# Roadmap

- [ ] Auto‑refresh document list after ingestion  
- [ ] UI polish (loading indicators, success messages)  
- [ ] Streaming LLM responses  
- [ ] Multi‑threaded memory  
- [ ] Rerankers (cross‑encoder)  
- [ ] Semantic chunking  
- [ ] Agentic workflows  

---

# Why This Project Exists

Most people have notes, research, and documents scattered across formats and folders. Finding what you need — and using it effectively — is hard.

**Expert‑in‑a‑Box** solves that by giving you:

- A unified place to store and structure knowledge  
- Fast retrieval of exactly what matters  
- Local LLM‑powered insight  
- Full transparency and control  
- A foundation for agentic workflows  

It’s a personal knowledge engine you can trust, extend, and understand.

---

# 📄 License
MIT License — see `LICENSE` for details.
