from abc import ABC, abstractmethod

class BaseDatabase(ABC):

    @abstractmethod
    def execute_query(self, query: str) -> list[dict]:
        pass