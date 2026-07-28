from typing import Any

class Chunk:

    def __init__(
            self, 
            chunk_id: str,
            document_id: str,
            text: str,
            metadata: dict[str, Any],
            embedding: list[float] | None = None) -> None:
        
        self.chunk_id = chunk_id
        self.document_id = document_id
        self.text = text
        self.metadata = metadata
        self.embedding = embedding