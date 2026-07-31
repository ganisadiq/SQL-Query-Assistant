import glob
import os

from src.loaders.pdf_loader import PDFLoader
from src.loaders.docx_loader import DOCXLoader
from src.loaders.json_loader import JSONLoader
from src.chunker.chunker import TextChunker
from src.embedding.azure_embedding_service import AzureEmbeddingService
from src.indexing.faiss_index_builder import FAISSIndexBuilder
from src.config import sql_server_connection_string
from src.loaders.sql_schema_loader import SQLSchemaLoader
from src.database.sql_server_database import SQLServerDatabase

def main():

    data_directory = "data"

    files = (
        glob.glob(os.path.join(data_directory, "*.pdf"))+
        glob.glob(os.path.join(data_directory, "*.json"))+
        glob.glob(os.path.join(data_directory, "*.docx"))
    )

    documents = []
    if not files:
        print("No supported documents found.")
        return

    for file_path in files:

        if file_path.endswith(".pdf"):
            loader = PDFLoader()

        elif file_path.endswith(".docx"):
            loader = DOCXLoader()

        elif file_path.endswith(".json"):
            loader = JSONLoader()

        else:
            continue

        document = loader.load(file_path)
        documents.extend(document)

    database = SQLServerDatabase(sql_server_connection_string)
    schema_loader = SQLSchemaLoader(database=database)
    documents.extend(schema_loader.load())

    chunker = TextChunker(chunk_size=500, chunk_overlap=100)
    chunks = chunker.chunk(documents=documents)

    embedding_service = AzureEmbeddingService()
    index_builder = FAISSIndexBuilder(embedding_service=embedding_service)

    index_builder.build(chunks=chunks)
    index_builder.save("storage/faiss")



if __name__ == "__main__":
    main()

