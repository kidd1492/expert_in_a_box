# Local Agent using Ollama, Langgraph



## Project Overview

The goal of this project is to:

- Build and test different types of agents using LangGraph and LangChain
- Run everything locally using Ollama for privacy.
- Explore streaming responses, memory, and conditional routing
- Develop a foundation for scalable, adaptive learning system.
      

### `RAG_system/`

A ReAct-style agent with retrieval and ingestion tools. It acts as a local-first research assistant.

**Capabilities:**

- Wikipedia search using LangChain tools
- Retrieval from a FAISS vectorstore
- File ingestion (supports `.txt` and `.pdf`; more formats coming soon)
- Logging system to track ingested files

**Key Components:**

| File               | Purpose                                                  
| `ReAct_agent.py`   | Main agent logic using ReAct-style reasoning             
| `chunking.py`      | Splits documents into manageable chunks                  
| `data_ingestion.py`| Handles file loading and preprocessing                   
| `embedding.py`     | Embeds chunks and stores them in FAISS                   
| `log_handler.py`   | Logs ingested files for traceability                     
| `graph.png`        | Visual flowchart of the agent's decision logic           



## Setup Instructions

1. Clone the repository:
   ```bash
   git clone https://github.com/kidd1492/expert_in_a_box.git

