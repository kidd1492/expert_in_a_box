# Local Agent using Ollama, Langgraph


This repository is a personal sandbox for experimenting with agentic AI systems using LangGraph, LangChain, and Ollama—all running locally on a laptop. 

It’s a fun and practical way to explore how agents can reason, retrieve, and collaborate to solve tasks. From simple chatbots to multi-agent orchestration, this project reflects a hands-on journey into modular design, retrieval workflows, and educational applications.

## Project Overview

The goal of this project is to:

- Build and test different types of agents using LangGraph and LangChain
- Run everything locally using Ollama for privacy.
- Explore streaming responses, memory, and conditional routing
- Develop a foundation for scalable, adaptive learning system.


### `agents/`

Contains prototypes of various agents:

| File                   | Description                                         
| `RagAgent.py`          | RAG using Chroma  
| `chatbot_1.py`         | Minimal chatbot for baseline testing                                       
| `chatbot_2.py`         | chatbot using checkpointer-memory and MessageState                            
| `conversation.py`      | using 2 bots to have a conversation for a set number of turns. 
                           The topic of the conversation is what my 9th grader is learning about at school.        

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

