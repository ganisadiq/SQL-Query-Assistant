from pathlib import Path
import pymupdf
from src.loaders.base_loader import BaseLoader
from src.models.document import Document


class PDFLoader(BaseLoader):

    def load(self,source: str) -> list[Document]:
        path = Path(source)
        if not path.exists():
            raise FileNotFoundError(f"{source} doesnt exist")
        
        page_text = []
        
        with pymupdf.open(path) as pdf:

            
            for page in pdf:
                text = self._extract_page_text(page)
                page_text.append(text)

        full_text = "\n".join(page_text)

        document = Document(
            document_id=path.stem,
            filename=path.name,
            text=full_text,
            metadata={
                "source":str(path),
                "type":"pdf"
            }
        )

        return [document]
    
    def _extract_page_text(self, page):
        return page.get_text()
        



