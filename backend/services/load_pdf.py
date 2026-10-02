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

        
        embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

        
        vector_store = Chroma.from_documents(
            embedding=embeddings,
            documents=chunks,
            persist_directory="./chroma_db"
        )
    finally:
        os.remove(tmp_path)

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




