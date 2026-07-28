import os
from dotenv import load_dotenv

load_dotenv()

project_endpoint = os.getenv("PROJECT_ENDPOINT")
model_deployment = os.getenv("MODEL_DEPLOYMENT_NAME")
embedding_model = os.getenv("EMBEDDING_MODEL")
embedding_model_endpoint = os.getenv("EMBEDDING_MODEL_ENDPOINT")