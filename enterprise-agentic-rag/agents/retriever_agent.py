"""
Retriever Agent — embeds the query and retrieves top-k documents from Qdrant.
"""
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Qdrant
from qdrant_client import QdrantClient
from typing import List
import os


COLLECTION_NAME = os.getenv("QDRANT_COLLECTION", "enterprise_docs")
QDRANT_URL      = os.getenv("QDRANT_URL",        "http://localhost:6333")
TOP_K           = int(os.getenv("RETRIEVER_TOP_K", "5"))


def get_vectorstore() -> Qdrant:
    client = QdrantClient(url=QDRANT_URL)
    embeddings = OpenAIEmbeddings()
    return Qdrant(client=client, collection_name=COLLECTION_NAME, embeddings=embeddings)


def run_retriever(query: str, top_k: int = TOP_K) -> List[dict]:
    """Retrieve top-k relevant document chunks for the given query."""
    vectorstore = get_vectorstore()
    docs = vectorstore.similarity_search_with_score(query, k=top_k)

    results = []
    for doc, score in docs:
        results.append({
            "content":  doc.page_content,
            "source":   doc.metadata.get("source", "unknown"),
            "title":    doc.metadata.get("title",  "Untitled"),
            "score":    round(float(score), 4),
        })
    return results


def ingest_documents(docs_path: str) -> int:
    """Chunk, embed, and store documents from a folder into Qdrant."""
    from langchain.document_loaders import DirectoryLoader, PyPDFLoader
    from langchain.text_splitter import RecursiveCharacterTextSplitter

    loader   = DirectoryLoader(docs_path, glob="**/*.pdf", loader_cls=PyPDFLoader)
    splitter = RecursiveCharacterTextSplitter(chunk_size=512, chunk_overlap=64)
    documents = splitter.split_documents(loader.load())

    vectorstore = get_vectorstore()
    vectorstore.add_documents(documents)
    return len(documents)
