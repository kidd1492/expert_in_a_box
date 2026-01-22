# **Expert‑in‑a‑Box**  
*A transparent, offline‑first Retrieval‑Augmented Generation (RAG) system with a modular backend and a lightweight Flask UI.*

`https://img.shields.io/badge/Python-3.10%2B-blue`  
`https://img.shields.io/badge/License-MIT-green`

---

## **Overview**
**Expert‑in‑a‑Box** is a fully local, privacy‑preserving RAG platform built for developers who value transparency, control, and extensibility. It combines a clean Python RAG engine with a three‑panel Flask web interface that allows users to:

- Ingest documents  
- Retrieve relevant chunks  
- Run Wikipedia searches  
- Prepare context for LLM‑based question answering  

Every step of the ingestion and retrieval pipeline is exposed — no hidden agent behavior, no opaque chains. All data, embeddings, and logs are stored locally using SQLite and the filesystem.

---

## **Features**

### **Retrieval‑Augmented Generation Engine**
- Local SQLite‑backed vector store  
- Local SQLite conversation memory  
- Chunking via `RecursiveCharacterTextSplitter`  
- Embeddings generated through local Ollama models  
- Transparent metadata (title, page number, source file)  
- Document‑level filtering for targeted retrieval  
- Top‑k similarity search  

---

### **Document Ingestion**
Supports:
- `.txt`  
- `.md`  
- `.pdf`

Ingestion pipeline:
1. Load file  
2. Chunk text  
3. Embed chunks  
4. Store embeddings + metadata in SQLite  

All ingestion happens locally — no cloud calls, no external dependencies.

---

## **Flask Web Application**
A clean, three‑column interface designed for clarity and workflow efficiency.

### **Left Column — Document Management**
- Displays all ingested documents  
- Checkboxes for selecting documents  
- “Select All” option  
- Clicking a document shows all its chunks   

### **Middle Column — Retrieval Panel**
- Query input  
- “Query Selected Documents” button  
- Retrieves top‑k chunks from selected documents  

### **Right Column — Wikipedia Tools**
- Input for Wikipedia search term  
- “Search Wikipedia” button (fetches content only)  
- “Add Results” button:
  - Fetches wiki content  
  - Saves it to `rag/data/wiki/<term>.txt`  
  - Ingests the saved file into the vector store
- “Add Document” button:
  - add selected document to the vector store

---

## **Tools**

### **`wiki_search(term)`**
Fetches Wikipedia content and returns it (no file saved).

### **`add_wiki(term)`**
- Calls `wiki_search(term)`  
- Saves content to `rag/data/wiki/<term>.txt`  
- Passes the file to the ingestion service  

### **`add_file(filepath)`**
Loads any supported file into the RAG system.

---

## **Architecture**
```
expert_in_a_box/
│
├── rag/
│   ├── core/              # chunking, embeddings, vectors, memory
│   ├── services/          # ingestion, retrieval, memory services
│   ├── agents/            # legacy ReAct agent (being simplified)
│   ├── utils/             # logging, db checks
│   └── data/
│       ├── wiki/          # auto-generated Wikipedia documents
│       ├── uploads/       # user-uploaded files
│       ├── rag_store.db   # SQLite vector store
│       └── memory.db      # conversation memory (optional)
│
├── web_app/
│   ├── templates/         # index.html, layout.html
│   ├── static/            # javascript.js, styles.css
│   ├── routes.py          # Flask endpoints
│   └── __init__.py        # create_app()
│
├── logs/                  # system logs
│
├── main.py                # CLI interaction with agent
└── run.py                 # Launch Flask UI, ensure directories, start Ollama
```

---

## **Quick Start**

```bash
pip install -r requirements.txt
python run.py
```

The app will:

- Ensure required directories exist  
- Initialize the SQLite vector store  
- Optionally start the local Ollama server  
- Launch the Flask UI  
---

## **Roadmap**
- [ ] Add chatbot functionality using retrieved chunks as context  
- [ ] Replace legacy ReAct agent with a minimal, transparent model‑call function  
- [ ] Auto‑refresh document list after ingestion  
- [ ] UI polish (loading indicators, success messages)  
- [ ] Local file uploads (completed)  
- [ ] Directory ingestion  
- [ ] Streaming responses  

---

## **Why This Project Exists**
Expert‑in‑a‑Box is built for developers who want:

- Full control over retrieval  
- Transparent chunk‑level inspection  
- Local, offline‑first operation  
- A modular architecture that’s easy to extend  
- A clean UI for interacting with RAG workflows  

It’s a foundation for building personal research assistants, knowledge bases, or agentic systems — **without relying on cloud services or opaque pipelines**.

This project is licensed under the MIT License — see the LICENSE file for details.
