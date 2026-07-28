from abc import ABC,abstractmethod
from src.models.document import Document
from pathlib import Path
import pymupdf

class BaseLoader(ABC):
    """
    Base class for all document loaders.
    """

    @abstractmethod
    def load(self,source: str) -> list[Document]: 

        pass

