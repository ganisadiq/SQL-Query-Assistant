from src.loaders.base_loader import BaseLoader
from src.models.document import Document
from pathlib import Path
import json

class JSONLoader(BaseLoader):
    def load (self, source) -> list[Document]:

        path = Path(source)
        

        if not path.exists():
            raise FileNotFoundError(f"File not found: {source}")
        
        with path.open("r", encoding="utf-8") as file:
            data = json.load(file)

            documents = []

            for policy in data:
                document = self._create_document(policy)
                documents.append(document)
        return [documents]
    
    def _create_document(self, policy: dict) -> Document:

        return Document(
            document_id=policy["id"],
            filename=policy["title"],
            text=policy["content"],
            metadata={
                key: value
                for key, value in policy.items()
                if key not in {"id", "title", "content"}
            },
        )