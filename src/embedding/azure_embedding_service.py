from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from azure.ai.projects import AIProjectClient
from src.embedding.base_embedding_service import BaseEmbeddingService
from src.config import project_endpoint, embedding_model,embedding_model_endpoint
from openai import OpenAI


class AzureEmbeddingService(BaseEmbeddingService):

    def __init__(self):
            
        self.credentials = get_bearer_token_provider(
            DefaultAzureCredential(),
            "https://ai.azure.com/.default"
        )
        self.openai_client = OpenAI(
            base_url=embedding_model_endpoint,
            api_key=self.credentials
        )

        self.embedding_model = embedding_model

    def embed_text(self, text:str) -> list[float]:
          
          
        response = self.openai_client.embeddings.create(
            model=self.embedding_model,
            input=text
            )
        return response.data[0].embedding
    
    def embed_texts(self, texts: list[str]) -> list[list[float]]:
        print("Project endpoint:", project_endpoint)
        print("Embedding model:", self.embedding_model)

        response = self.openai_client.embeddings.create(
            model=self.embedding_model,
            input=texts
            )

        return [item.embedding for item in response.data]