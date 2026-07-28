import json
import faiss
import numpy as np

from src.models.chunk import Chunk

class FAISSRetriever:

    def __init__(self,
                 embedding_service,
                 index_path="storage/faiss/index.faiss",
                 metadata_path = "storage/faiss/metadata.json"):
        self.embedding_service = embedding_service
        self.index = faiss.read_index(index_path)
        with open(metadata_path, "r",encoding="utf-8") as file:
            self.metadata = json.load(file)


    def retrieve(self, query, top_k = 3):
        query_embedding = self.embedding_service.embed_text(query)

        query_vector = np.array(
            [query_embedding],
            dtype="float32"
        )

        distance, indices = self.index.search(
            query_vector,
            top_k
        )

        result = []

        for idx in indices[0]:
            item = self.metadata[idx]

            chunk = Chunk(
                chunk_id=item["chunk_id"],
                document_id=item["document_id"],
                text=item['text'],
                metadata=item["metadata"]
            )

            result.append(chunk)

        return result

