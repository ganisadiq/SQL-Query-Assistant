from src.embedding.azure_embedding_service import AzureEmbeddingService
from src.retrieval.faiss_retriever import FAISSRetriever


embedding_service = AzureEmbeddingService()
retriever = FAISSRetriever(embedding_service)

def search_database_schema(question: str):

    chunks = retriever.retrieve(question)

    if not chunks:
        return "Sorry, I couldn't find any relevant database schema information."

    context = ""

    for chunk in chunks:
        context += chunk.text
        context += "\n\n-----------------------------\n\n"

    return context