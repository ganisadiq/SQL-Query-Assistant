from src.embedding.azure_embedding_service import AzureEmbeddingService
from src.retrieval.faiss_retriever import FAISSRetriever


def main():

    embedding_service = AzureEmbeddingService()

    retriever = FAISSRetriever(embedding_service)

    query = "What is the notice period?"

    chunks = retriever.retrieve(query)

    print(f"Retrieved {len(chunks)} chunks\n")

    for i, chunk in enumerate(chunks, start=1):
        print("=" * 50)
        print(f"Result {i}")
        print("=" * 50)
        print(f"Chunk ID     : {chunk.chunk_id}")
        print(f"Document ID  : {chunk.document_id}")
        print(f"Metadata     : {chunk.metadata}")
        print("\nText:")
        print(chunk.text)
        print()


if __name__ == "__main__":
    main()