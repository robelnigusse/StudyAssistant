
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
import os
from dotenv import load_dotenv

load_dotenv()


# Embedding model
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


# Existing vector database
vector_store = Chroma(
    embedding_function=embeddings,
    persist_directory="./chroma_db"
)


# Retriever
retriever = vector_store.as_retriever(
    search_kwargs={"k": 5}
)

def format_docs(docs):

    formatted = []

    for doc in docs:

        source = doc.metadata.get(
            "title",
            "Unknown"
        )

        page = doc.metadata.get(
            "page",
            "Unknown"
        )

        # PDF page numbers are often zero-based
        if isinstance(page, int):
            page = page + 1

        formatted.append(
            f"""
                Source: {source}
                Page: {page}

                {doc.page_content}
                """
                        )

    return "\n\n---\n\n".join(formatted)




# Gemini
llm = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash-lite",
    google_api_key=os.getenv("GOOGLE_API_KEY")
)


# Prompt
prompt = ChatPromptTemplate.from_template(
    """
    You are a document-based study assistant.

    Answer the question using ONLY the provided context.

    Give a detailed answer.

    If the answer cannot be found in the context,
    say:

    "I don't know based on the provided documents."

    At the end of your answer, provide the sources
    using the source name and page number provided
    in the context.

    Context:
    {context}

    Question:
    {question}
    """
)

rag_chain = {
    "context": retriever | format_docs,
    "question": RunnablePassthrough()
} | prompt | llm

def ask_question(question: str):

    response = rag_chain.invoke(question)

    return response.content[0]["text"]

print(ask_question("What is software testing?"))