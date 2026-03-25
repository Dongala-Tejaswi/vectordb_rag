from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

DB_PATH = "db/"

def query_db(query):
    embedding = HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2"
    )

    db = Chroma(
        persist_directory=DB_PATH,
        embedding_function=embedding
    )

    results = db.similarity_search(query, k=3)

    answer = "\n\n".join([r.page_content for r in results])

    return answer, results