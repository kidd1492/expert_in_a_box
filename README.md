# Local RAG System with Qwen and FAISS

This project is a modular Retrieval-Augmented Generation (RAG) pipeline that leverages a local Ollama Qwen model to answer questions from PDF documents. The pipeline includes PDF ingestion, intelligent text chunking, embedding generation, and vector search via FAISS.

## 🔧 Modules

- `data_ingestion.py` — Loads and cleans PDF text using PyMuPDF.
- `chunking.py` — Chunks raw text into LangChain Document objects.
- `embedding.py` — Embeds and stores chunks in a FAISS vector database using Ollama embeddings.
- `query.py` — (to be implemented) Retrieves relevant context and generates responses using the Qwen model.


project/
├── data_ingestion.py
├── chunking.py
├── embedding.py
├── query.py
├── faiss_index/ 
└── requirements.txt


## 🚀 Quickstart

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
