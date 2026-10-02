from fastapi import UploadFile
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_pymupdf4llm import PyMuPDF4LLMLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

def upload_and_process_pdf(file: UploadFile):
    # Load the PDF file using PyMuPDF4LLMLoader
    loader = PyMuPDF4LLMLoader(file.file, mode="page")
    documents = loader.load()

    # Split the documents into chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = text_splitter.split_documents(documents)

    # Generate embeddings for the chunks
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    # Create a Chroma vector store from the chunks and embeddings
    vector_store = Chroma.from_documents(
        embedding=embeddings,
        documents=chunks,
        persist_directory="./chroma_db"
    )

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




