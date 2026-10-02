from fastapi import UploadFile
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_pymupdf4llm import PyMuPDF4LLMLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

import tempfile
import os

def upload_and_process_pdf(file: UploadFile):
    # Save to a temporary file on disk because PyMuPDF4LLMLoader expects a path
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(file.file.read())
        tmp_path = tmp.name

    try:
        loader = PyMuPDF4LLMLoader(tmp_path, mode="page")
        documents = loader.load()

        
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        chunks = text_splitter.split_documents(documents)

        # Inject original filename into metadata for tracking
        for chunk in chunks:
            chunk.metadata["source"] = file.filename

        
        embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

        
        vector_store = Chroma.from_documents(
            embedding=embeddings,
            documents=chunks,
            persist_directory="./chroma_db"
        )
    finally:
        os.remove(tmp_path)

def get_all_books():
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vector_store = Chroma(
        embedding_function=embeddings,
        persist_directory="./chroma_db"
    )
    data = vector_store.get()
    metadatas = data.get("metadatas", [])
    books = set()
    for meta in metadatas:
        # Prioritize 'title' from metadata as requested
        title = meta.get("title")
        if not title:
            # Fallback to source but heavily cleaned up
            source = meta.get("source", "")
            if source:
                title = source.replace("\\", "/").split("/")[-1]
                
        if title:
            books.add(title)
    return list(books)

def delete_book(filename: str):
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vector_store = Chroma(
        embedding_function=embeddings,
        persist_directory="./chroma_db"
    )
    # Fetch all to match derived titles manually, ensuring we delete exactly what's shown
    data = vector_store.get()
    metadatas = data.get("metadatas", [])
    ids = data.get("ids", [])
    
    ids_to_delete = []
    for i, meta in enumerate(metadatas):
        title = meta.get("title")
        if not title:
            source = meta.get("source", "")
            if source:
                title = source.replace("\\", "/").split("/")[-1]
                
        if title == filename:
            ids_to_delete.append(ids[i])
            
    if ids_to_delete:
        vector_store.delete(ids=ids_to_delete)
        return True
    return False

# loader = PyMuPDF4LLMLoader(
#     "document/Introduction to Software Testing.pdf",
#     mode="page"
# )
# documents = loader.load()

# text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)

# chunks = text_splitter.split_documents(documents)

# embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# vector_store= Chroma.from_documents(
#     embedding= embeddings,
#     documents= chunks,
#     persist_directory= "./chroma_db"
# )




