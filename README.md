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

### Backend
Navigate to the `backend` directory, activate your virtual environment, and run the server:
```bash
cd backend
# Activate virtual environment (Windows)
.\venv\Scripts\Activate.ps1
# Start server
uvicorn main:app --reload
```

### Frontend
Navigate to the `frontend` directory and start the Vite development server:
```bash
cd frontend
npm run dev
```
