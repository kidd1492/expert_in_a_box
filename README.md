# **Expert‑in‑a‑Box**  
*A transparent, offline‑first Retrieval‑Augmented Generation (RAG) system with a modular backend and a lightweight Flask UI.*

![Python Version](https://img.shields.io/badge/Python-3.10%2B-blue)
![License: MIT](https://img.shields.io/badge/License-MIT-green)

---

## **Overview**
**Expert‑in‑a‑Box** is a fully local, privacy‑preserving RAG. It combines a clean Python RAG engine with a three‑panel Flask web interface that allows users to:

- Ingest documents  
- Retrieve relevant chunks  
- Run Wikipedia searches  
- Prepare context for LLM‑based question answering  

Every step of the ingestion and retrieval pipeline is exposed — no hidden agent behavior, no opaque chains. All data, embeddings, and logs are stored locally using SQLite and the filesystem.

---

## **Features**

### **Retrieval‑Augmented Generation Engine**
- Local SQLite‑backed vector store   
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
- “Ask chatbot” button 
- “Summarize” button
- “Outline” button

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
│   ├── core/              # chat_agent, chunking, data_ingestion, embedding, tools, vectors
│   ├── services/          # ingestion, retrieval, chat
│   ├── utils/             # logging, db checks
│   └── data/
│       ├── wiki/          # auto-generated Wikipedia documents
│       ├── uploads/       # user-uploaded files
│       ├── rag_store.db   # SQLite vector store
|       |__ logs           # tool,log, error.log, doc.log
│
├── web_app/
│   ├── templates/         # index.html, layout.html
│   ├── static/            # javascript.js, styles.css
│   ├── routes.py          # Flask endpoints
│   └── __init__.py        # create_app()
│
└── run.py                 # Launch Flask UI, ensure directories, start Ollama
```

---

## **Quick Start**
- Install Ollama
- https://humansideoftek.blogspot.com/2025/09/ollama-local-model-deployment-guide.html

```bash
git clone https://github.com/kidd1492/expert_in_a_box.git
```

```bash
cd expert_in_a_box
```

```bash
python -m venv venv
```
```bash
pip install -r requirements.txt
python run.py
```


The app will:

- Ensure required directories exist  
- Initialize the SQLite vector store  
- Start the local Ollama server  
---

## **Roadmap**    
- [ ] Auto‑refresh document list after ingestion  
- [ ] UI polish (loading indicators, success messages)    
- [ ] Streaming responses  

---

## **Why This Project Exists**
If you're anything like me, you have notes scattered across apps, folders, and formats — ideas, research, tasks, references, half‑finished thoughts. Finding what you need, when you need it, can be frustrating. I wanted a simple, fast way to organize all of it and instantly surface the relevant pieces for whatever I’m working on.

- Expert‑in‑a‑Box was built to solve that problem.

- It provides:

- A unified place to store and structure notes
- Fast retrieval of the exact information needed for a task
- A growing personal knowledge base you can build on over time
- Local LLM‑powered insight without sending data to the cloud
- Full transparency and control over how retrieval and reasoning work

This project is for anyone who wants their notes to become a living, searchable knowledge system — and who values privacy, clarity, and local control. It’s a foundation for personal research assistants, knowledge bases, and agentic workflows that you can trust and extend.

This project is licensed under the MIT License — see the LICENSE file for details.
