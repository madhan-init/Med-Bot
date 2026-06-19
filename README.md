# Med-Bot

Med-Bot is an AI-powered medical assistant application that leverages Retrieval-Augmented Generation (RAG) to provide contextual, role-based medical information. Built with a **FastAPI** backend and a **Streamlit** frontend, it uses LangChain, FAISS vector databases, and Google Generative AI Embeddings to securely answer queries from users depending on their assigned role.

---

## Features

- **Role-Based Access Control**: Tailored chat experiences and responses based on the user's role (Visitor, Patient, Doctor, Admin).
- **RAG Engine**: Retrieves knowledge from uploaded documents using LangChain and a FAISS local vector store.
- **Document Sourcing & Citations**: Admins have the exclusive ability to view document sources and page citations for the AI's answers.
- **Modern Chat Interface**: A custom-styled, brutalism-inspired Streamlit frontend.
- **Robust API**: A scalable FastAPI backend handling chat generation, document uploads, authentication, and FAQs.

---

## Project Structure

```text
Med-Bot/
├── backend/            # FastAPI server, RAG engine, and API endpoints
│   ├── api/            # API routers (chat, upload, auth, faq)
│   ├── services/       # Core business logic and RAG setup
│   └── main.py         # FastAPI application entry point
├── frontend/           # Streamlit application
│   ├── pages/          # Additional Streamlit pages
│   ├── api_client.py   # Connection logic to the FastAPI backend
│   └── Chat.py         # Main chat interface and UI configuration
├── data/               # Local data storage 
│   └── vector_store/   # FAISS vector database files
├── assets/             # Static assets (images, icons, etc.)
└── requirements.txt    # Project Python dependencies
```

---

## Prerequisites

- **Python 3.11+**
- API Keys for Google Gemini (Embeddings) and Groq (LLM generation).

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
- **Visitor / Patient / Doctor**: You will receive answers tailored to your context and clearance.
- **Admin**: Has elevated privileges, including the ability to see the specific document citations and exact pages where the AI retrieved its information.

