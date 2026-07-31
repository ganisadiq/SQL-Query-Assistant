from src.config import sql_server_connection_string
from src.database.sql_server_database import SQLServerDatabase
from src.loaders.sql_schema_loader import SQLSchemaLoader

db = SQLServerDatabase(sql_server_connection_string)

loader = SQLSchemaLoader(db)

documents = loader.load()

for document in documents:
    print("=" * 50)
    print(document.filename)
    print(document.text)