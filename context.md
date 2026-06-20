# Med-Bot Context & Overview

## 1. Project Description
Med-Bot is an AI-powered medical assistant application that uses Retrieval-Augmented Generation (RAG) to provide contextual, role-based medical information safely and accurately. 

## 2. Tech Stack
- **Frontend**: Streamlit
- **Backend API**: FastAPI (Python)
- **Vector Database**: FAISS (Facebook AI Similarity Search)
- **Embeddings**: Google Generative AI Embeddings (`models/gemini-embedding-001`)
- **LLM**: Groq API (`llama-3.1-8b-instant`)
- **Orchestration**: LangChain

## 3. High-Level Architecture
The application is strictly decoupled into a frontend UI and a backend API.
* **Frontend (UI)**: Built with Streamlit, it features a customized "brutalist" design. It handles role-based access (Visitor, Patient, Admin) and queries the backend.
* **Backend (API)**: Built with FastAPI, it manages data ingestion, exposes REST endpoints (`/chat`, `/login`), and houses the RAG engine.
* **Database**: Raw medical documents (PDFs/TXTs) are ingested, chunked, embedded, and stored locally in a FAISS vector store.

## 4. Directory Structure

- `frontend/`
  - `Chat.py`: The main Streamlit entry point. Manages roles, sessions, custom CSS, and chat history.
  - `pages/Admin.py`: Admin dashboard for elevated actions.
  - `api_client.py`: Handles HTTP requests from the Streamlit UI to the FastAPI backend.
- `backend/`
  - `main.py`: The FastAPI application entry point. Loads the FAISS vector DB on startup and registers routers.
  - `api/`: Contains route definitions (`chat.py`, `auth.py`, `upload.py`, `faq.py`).
  - `services/rag_engine.py`: Configures LangChain, the Groq LLM, and the specific system prompts (including safety guardrails against diagnosing illnesses).
  - `services/knowledge_base.py`: The ingestion pipeline. Parses PDFs/Text files from `/data/raw_documents`, splits them into chunks, creates Google GenAI embeddings, and saves them to the FAISS database.
- `data/`
  - `raw_documents/`: Directory where source text/PDF files are stored.
  - `vector_store/`: The compiled FAISS local database.
- `assets/`: Images and diagrams for documentation.

## 5. Core Workflows

### Data Ingestion
1. Raw PDFs/Text files are placed in `data/raw_documents/`.
2. Running `backend/services/knowledge_base.py` splits these files into manageable chunks.
3. Chunks are passed to Google's Embedding API to turn text into vector representations.
4. The vectors are saved to disk in `data/vector_store/` using FAISS.

### Chat Inference
1. A user (e.g., Visitor) opens the Streamlit UI and submits a question.
2. The UI sends a POST request with the query and role to the backend `/chat` endpoint.
3. The `rag_engine.py` searches the FAISS DB for the top 2 most relevant text chunks (k=2).
4. The backend constructs a prompt containing the user's role, the question, the retrieved context, and strict safety guidelines.
5. The prompt is sent to the Groq LLM, which streams back a contextual answer.
6. The frontend displays the answer. If the user is an Admin, it also displays the exact source files (citations) where the information was found.
