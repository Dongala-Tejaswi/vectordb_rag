from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

import os

DATA_PATH = "data/"
DB_PATH = "db/"

def load_documents():
    docs = []
    for file in os.listdir(DATA_PATH):
        path = os.path.join(DATA_PATH, file)
        if file.endswith(".pdf"):
            loader = PyPDFLoader(path)
        else:
            loader = TextLoader(path)
        docs.extend(loader.load())
    return docs

def split_docs(documents):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )
    return splitter.split_documents(documents)

def create_vector_db():
    documents = load_documents()
    chunks = split_docs(documents)

    embedding = HuggingFaceEmbeddings(
    model_name="all-MiniLM-L6-v2"
)

    db = Chroma.from_documents(
        chunks,
        embedding,
        persist_directory=DB_PATH
    )

    db.persist()
    print("✅ Vector DB created successfully!")

if __name__ == "__main__":
    create_vector_db()