from src.models.document import Document
from src.models.chunk import Chunk

class TextChunker:

    def __init__(self,
                 chunk_size: int,
                 chunk_overlap: int) -> None:
        
        if chunk_size <= 0:
            raise ValueError("chunk_size must be greater than 0.")

        if chunk_overlap < 0:
            raise ValueError("chunk_overlap cannot be negative.")

        if chunk_overlap >= chunk_size:
            raise ValueError("chunk_overlap must be smaller than chunk_size.")
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        
    def chunk(self,
              documents: list[Document]) -> list[Chunk]:
        
        chunks : list[Chunk] = []

        for document in documents:
            pieces = self._split_text(document.text)

            for chunk_number,chunk_text in enumerate(pieces, start=1):
                chunk = self._create_chunk(
                        document=document,
                        chunk_text=chunk_text,
                        chunk_number=chunk_number
                    )

                chunks.append(chunk)

        return chunks


    def _split_text(
                self,
                text: str
                ) -> list[str]:
        
        pieces : list[str] = []

        start = 0 
        while start < len(text):
            piece = text[start: (start+self.chunk_size) ]
            pieces.append(piece)
            start += self.chunk_size - self.chunk_overlap
        return pieces



    def _create_chunk(
                        self,
                        document: Document,
                        chunk_text: str,
                        chunk_number: int
                    ) -> Chunk:
        
        chunk_id = f"{document.document_id}_chunk_{chunk_number}"

        return Chunk(
            chunk_id=chunk_id,
            document_id=document.document_id,
            text=chunk_text,
            metadata=document.metadata,
            embedding=None
        )

