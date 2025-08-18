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
| `ReAct_agent.py`       | Agent using ReAct-style reasoning and tool use      
| `chatbot_2.py`         | Intermediate chatbot with enhanced logic            
| `simple_chatbot.py`    | Minimal chatbot for baseline testing                
| `streaming_chatbot.py` | Chatbot with streaming response capabilities        

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

### `multi_agent/`

An experimental setup for multi-agent collaboration. It tests how agents can communicate and delegate tasks to reach a shared goal.

**Workflow:**

1. Chatbot agent (`test_prompt.py`) receives a topic and generates 5 clarifying questions.
2. ReAct agent (`ReAct_agent.py`) receives the topic and questions, performs research via Wikipedia and FAISS, and returns a summary.
3. The system updates shared state with the findings.
4. Current research focus: exchanging state between agents using LangGraph.

## Setup Instructions

1. Clone the repository:
   ```bash
   git clone https://github.com/kidd1492/expert_in_a_box.git

