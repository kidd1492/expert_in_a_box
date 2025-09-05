# Local Agent using Ollama, LangGraph

This repository is a personal sandbox for experimenting with agentic AI systems using LangGraph, LangChain, and Ollama—all running locally on a laptop.

## Project Overview

**Goals:**

- Build a RAG system that I would actually use
- Run everything locally using Ollama, LangGraph, and LangChain for privacy
- Explore streaming responses, memory, chunking, ingestion, and retrieval
- Develop a foundation for scalable, adaptive learning systems
- Enable general question answering in a back-and-forth chat format
- Build a system that can ingest and store documents of various types in a vectorstore
- Implement RAG capabilities with file tracking
- Integrate external lookup (e.g., web search)
- Support continuous querying of ingested documents

### `RagAgent.py`

This is a complete one-shot RAG agent. It ingests a file, chunks it, runs the embedding model, and creates a Chroma database. It then takes the user's input, retrieves relevant information, returns a response, and ends the session. While useful for one-off queries, it's limited in long-term utility. To improve this, I added modularity and broke the components down into the `RAG_system` directory.

### `RAG_system/`

A ReAct-style agent with retrieval and ingestion tools. It acts as a local-first research assistant.

**Capabilities:**

- Wikipedia search using LangChain tools
- Retrieval from a FAISS vectorstore
- File ingestion (supports `.txt` and `.pdf`; more formats coming soon)
- Logging system to track ingested files

**Key Components:**

| File                | Purpose                                                 |
|---------------------|---------------------------------------------------------|
| `ReAct_agent.py`    | Main agent logic using ReAct-style reasoning            |
| `chunking.py`       | Splits documents into manageable chunks                 |
| `data_ingestion.py` | Handles file loading and preprocessing                  |
| `embedding.py`      | Embeds chunks and stores them in FAISS                  |
| `log_handler.py`    | Logs ingested files for traceability                    |
| `graph.png`         | Visual flowchart of the agent's decision logic          |

### `rag/`

This directory mirrors `RAG_system` but adds a dedicated tools file. It introduces a `Human_node`, memory with summarization, and reducers. This forms the foundation for a more helpful agent with broader use cases, such as a Tutor Bot or Telephone Agent.



## Setup Instructions

1. Clone the repository:
   ```bash
   git clone https://github.com/kidd1492/expert_in_a_box.git
   ```
