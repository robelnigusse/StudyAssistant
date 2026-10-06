# StudyAssistant 🎓

StudyAssistant is a GPT-style AI web application that helps you study by allowing you to upload course materials (PDFs) and ask questions directly about them. The system uses **Retrieval-Augmented Generation (RAG)** to provide accurate, context-aware answers based strictly on your uploaded books.

## Tech Stack
- **Frontend**: React (Vite), custom CSS styling with a modern dark theme and responsive layout.
- **Backend**: Python, FastAPI.
- **Vector Database**: ChromaDB.
- **Embeddings**: HuggingFace (`sentence-transformers/all-MiniLM-L6-v2`).
- **PDF Processing**: LangChain + PyMuPDF4LLM.

## Features
- **Modern Chat Interface**: Clean, dark-themed UI reminiscent of ChatGPT.
- **PDF Management**: Upload course PDFs directly from the sidebar. You can manage and delete your uploaded books in the library popup.
- **Chat Histories**: Conversations are persisted and stored, allowing you to seamlessly switch between multiple study topics.
- **Intelligent RAG Pipeline**: Accurately fetches context from your textbooks before generating intelligent answers.

## Architecture & RAG Pipeline

The application relies on a Retrieval-Augmented Generation (RAG) architecture to function. This pipeline seamlessly handles both document ingestion (uploading PDFs) and retrieval/generation (answering questions).

![RAG Pipeline Architecture Diagram](RAG%20Pipeline%20Architecture%20Diagram.png)

### 1. Document Ingestion (Upload)
When you upload a PDF, the backend extracts the text, splits it into digestible chunks, computes vector embeddings, and stores them securely in ChromaDB.

### 2. Retrieval & Generation (Q&A)
When you ask a question, the backend calculates an embedding for your query, retrieves the most relevant document chunks from ChromaDB, and provides them as context to the LLM to generate a precise answer.

## Running the Application

Before running the application, you **must** configure your environment variables. 
Navigate to the `backend/` directory, copy `.env.example` to `.env`, and insert your Gemini API Key.
```bash
cp backend/.env.example backend/.env
```
*(Make sure to open `backend/.env` and replace `your_gemini_api_key_here` with your actual key!)*

You can run this project in two ways: using Docker (Recommended) or manually.

### Method 1: Using Docker (Recommended)

Running with Docker automatically sets up the PostgreSQL database, backend server, and frontend server in isolated containers without requiring local dependencies.

1. Ensure Docker Desktop is running.
2. In the root directory of the project, run:
```powershell
# We set BUILD_PROVENANCE=0 to bypass a known freeze bug with Docker BuildKit on Windows
$env:BUILD_PROVENANCE="0"; docker compose up --build
```

3. The application will be available at:
   - **Frontend**: `http://localhost:5173`
   - **Backend API**: `http://localhost:8000`

### Method 2: Running Manually

If you prefer to run the application natively without Docker, you will need to host your own PostgreSQL database locally.

1. **Database Setup**: Ensure PostgreSQL is installed and running on your machine. Update the `DB_URL` in your `backend/.env` file to point to your local PostgreSQL instance (the default provided in `.env.example` is `postgresql+psycopg://<your_username>:<your_password>@localhost:5432/<your_database_name>`).

2. **Backend**:
Navigate to the `backend` directory, activate your virtual environment, and run the server:
```bash
cd backend
# Activate virtual environment (Windows)
.\venv\Scripts\Activate.ps1
# Install dependencies
pip install -r requirements.txt
# Start FastAPI server
uvicorn main:app --reload
```

3. **Frontend**:
Open a new terminal, navigate to the `frontend` directory, and start the Vite development server:
```bash
cd frontend
npm install
npm run dev
```
