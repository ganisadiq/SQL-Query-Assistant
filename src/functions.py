from src.embedding.azure_embedding_service import AzureEmbeddingService
from src.retrieval.faiss_retriever import FAISSRetriever


embedding_service = AzureEmbeddingService()
retriever = FAISSRetriever(embedding_service)

def search_policies(policy: str):

    chunks = retriever.retrieve(policy)

    if not chunks:
        return "Sorry, I couldn't find any relevant HR policy."

    context = ""

    for chunk in chunks:
        context += chunk.text
        context += "\n\n-----------------------------\n\n"

        return context