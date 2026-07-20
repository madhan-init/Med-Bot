# Med-Bot

Med-Bot is an AI-powered medical assistant application that leverages Retrieval-Augmented Generation (RAG) to provide contextual, role-based medical information. Built with a **FastAPI** backend and a **Streamlit** frontend, it uses LangChain, FAISS vector databases, and Google Generative AI Embeddings to securely answer queries from users depending on their assigned role.

---

## Features

- **Role-Based Access Control**: Tailored chat experiences and responses based on the user's role (Visitor, Patient, Admin).
- **RAG Engine**: Retrieves knowledge from uploaded documents using LangChain and a FAISS local vector store.
- **Document Sourcing & Citations**: Admins have the exclusive ability to view document sources and page citations for the AI's answers.
- **Redis Caching**: Smart caching layer to temporarily store generated responses, lowering API costs and response latency.
- **Robust API**: A scalable FastAPI backend handling chat generation, document uploads, authentication, and FAQs.

---

## Prerequisites

- **Python 3.11+**
- API Keys for Google Gemini (Embeddings) and Groq (LLM generation).
- **Redis Server**: Local installation or cloud-hosted instance (e.g. Render Redis, Upstash, Redis Labs).

---

## Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd Med-Bot
   ```

2. **Set up a virtual environment:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Variables:**
   Create a `.env` file in the root directory and add your necessary API keys:
   ```env
   GOOGLE_API_KEY=your_google_gemini_api_key
   GROQ_API_KEY=your_groq_api_key
   REDIS_URL=redis://default:your_password@your_redis_host:port  # Optional for caching
   # Add any other required DB or Auth URLs here
   ```

---

## Usage

### 1. Start the Backend (FastAPI)
The backend manages the RAG engine and API requests. Run it using Uvicorn:

```bash
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```
*The API documentation will be available at `http://localhost:8000/docs`.*

### 2. Start the Frontend (Streamlit)
In a new terminal window (with the virtual environment activated), start the Streamlit UI:

```bash
cd frontend
streamlit run Chat.py
```
*The interface will automatically open in your browser at `http://localhost:8501`.*

---

## Usage Roles

Upon launching the frontend, you will be prompted to select a role. 
- **Visitor / Patient**: You will receive answers tailored to your context and clearance.
- **Admin**: Has elevated privileges, including the ability to see the specific document citations and exact pages where the AI retrieved its information.

---

## Redis Caching & Testing

The backend includes a Redis-based cache to store chat answers. 

To test your Redis connection, you can run the helper script in the root directory:
```bash
python test_redis.py
```
This script validates whether your `REDIS_URL` is configured correctly and verifies the credentials by pinging the server.

