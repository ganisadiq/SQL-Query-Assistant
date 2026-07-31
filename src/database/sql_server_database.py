from src.database.base_database import BaseDatabase
from sqlalchemy import create_engine, text

class SQLServerDatabase(BaseDatabase):

    def __init__(self, connection_string: str):

        self.engine = create_engine(connection_string)

    def execute_query(self, query: str) -> list[dict]:
        with self.engine.connect() as connection:
            result = connection.execute(text(query))
            return [ dict(row._mapping)  for row in result]