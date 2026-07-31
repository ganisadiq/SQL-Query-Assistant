from src.loaders.base_loader import BaseLoader
from src.database.sql_server_database import SQLServerDatabase
from src.models.document import Document

class SQLSchemaLoader(BaseLoader):

    def __init__(self, database: SQLServerDatabase):
        self.database = database

    def load(self) -> list[Document]:

        tables = self.database.execute_query("""
            SELECT TABLE_NAME
            FROM INFORMATION_SCHEMA.TABLES
            WHERE TABLE_TYPE = 'BASE TABLE'
            ORDER BY TABLE_NAME
        """)

        document = []

        for table in tables:
            table_name = table['TABLE_NAME']
            columns = self.database.execute_query(f"""
                SELECT
                    COLUMN_NAME,
                    DATA_TYPE
                FROM INFORMATION_SCHEMA.COLUMNS
                WHERE TABLE_NAME = '{table_name}'
                ORDER BY ORDINAL_POSITION
            """)

            text = f"Table: {table_name}\n\nColumn:\n"

            for column in columns:
                text += (
                    f"- {column['COLUMN_NAME']} "
                    f"({column['DATA_TYPE']})\n"
                )

            document.append(
                Document(
                    document_id=table_name,
                    filename=f"{table_name}.schema",
                    text=text,
                    metadata={
                        "source": "database",
                        "table": table_name
                    }
                )
            )

        return document