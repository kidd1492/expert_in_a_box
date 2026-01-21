# **Expert‑in‑a‑Box**  
A fully offline‑first, transparent Retrieval‑Augmented Generation (RAG) system with a modular backend and a lightweight Flask web interface.

## **Overview**
Expert‑in‑a‑Box is a local, privacy‑preserving RAG platform designed for transparency, control, and extensibility. It combines a clean Python RAG engine with a three‑panel Flask UI that allows users to ingest documents, retrieve relevant chunks, run Wikipedia searches, and prepare context for LLM‑based question answering.

The system avoids hidden agent behavior and instead exposes every step of the retrieval and ingestion pipeline. All data, embeddings, and logs are stored locally using SQLite and the filesystem.

---

## **Features**

### **Retrieval‑Augmented Generation Engine**
- Local SQLite‑backed vector store  
- Local SQLite conversation memory  
- Chunking via `RecursiveCharacterTextSplitter`  
- Embeddings generated through local Ollama models  
- Transparent metadata (title, page number)  
- Document‑level filtering for targeted retrieval  
- Top‑k similarity search  

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

---
## **Flask Web Application**
A three‑column interface:

### **Left Column — Document Management**
- Displays all ingested documents  
- Each document has a checkbox  
- “Select All” option  
- Clicking a document shows all its chunks in the viewer  
- Conversation history display  

### **Middle Column — Retrieval Panel**
- Query input  
- “Query Selected Documents” button  
- Retrieves top‑k chunks from selected documents    

### **Right Column — Wikipedia Tools**
- Input for Wikipedia search term  
- “Search Wikipedia” button (fetches content only)  
- “Add Document” button:
  - Fetches wiki content  
  - Saves it to `rag/data/wiki/<term>.txt`  
  - Ingests the saved file into the vector store  

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
│   ├── core/          # chunking, ingestion, embeddings, vectors, memory
│   ├── services/      # ingestion, retrieval, memory services
│   ├── agents/        # legacy ReAct agent (being simplified)
│   ├── utils/         # logging, db checks
│   └── data/          # wiki files, ingested files, SQLite DB
│
├── web_app/
│   ├── templates/     # index.html, layout.html
│   ├── static/        # javascript.js, styles.css
│   ├── routes.py      # Flask endpoints
│   └── __init__.py    # create_app()
│
├── main.py            # CLI interaction with agent
└── run.py             # Launch Flask UI
```

## **Current Development Goals**
- Add chatbot functionality using retrieved chunks as context  
- Replace the legacy ReAct agent with a minimal, transparent model‑call function  
- Auto‑refresh document list after ingestion  
- Add UI polish (loading indicators, success messages)  
- Expand toolset as needed (e.g., local file uploads, directory ingestion)

---

## **Why This Project Exists**
Expert‑in‑a‑Box is built for developers who want:
- Full control over retrieval  
- Transparent chunk‑level inspection  
- Local, offline‑first operation  
- A modular architecture that’s easy to extend  
- A clean UI for interacting with RAG workflows  

It’s a foundation for building personal research assistants, knowledge bases, or agentic systems without relying on cloud services.
