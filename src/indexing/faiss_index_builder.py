from src.embedding.base_embedding_service import BaseEmbeddingService
import faiss
import numpy as np
import os
import json


class FAISSIndexBuilder:

    def __init__(self, embedding_service: BaseEmbeddingService):
        self.embedding_service = embedding_service
        self.index = None
        self.metadata = []

    def build(self, chunks):

        if not chunks:
            raise ValueError("No chunks were provided to build the index.")

        texts = [chunk.text for chunk in chunks]
        embeddings = self.embedding_service.embed_texts(texts)
        dimension = len(embeddings[0])
        self.index = faiss.IndexFlatL2(dimension)
        embedding_array = np.array(embeddings).astype('float32')
        self.index.add(embedding_array)
        for chunk in chunks:
            self.metadata.append({
                "chunk_id": chunk.chunk_id,
                "document_id": chunk.document_id,
                "text": chunk.text,
                "metadata": chunk.metadata
            })

    def save(self, output_directory: str):

        os.makedirs(output_directory, exist_ok=True)

        faiss.write_index(
            self.index,
            os.path.join(output_directory, "index.faiss")
        )

        with open(
            os.path.join(output_directory, "metadata.json"),
            "w",
            encoding="utf-8"
        ) as file:
            json.dump(self.metadata, file, indent=4)