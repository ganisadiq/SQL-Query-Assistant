from typing import Any

class Document:
        """
    Represents a document after it has been loaded into the application.

    Every loader (PDF, DOCX, JSON, etc.) converts its input into this
    common document format so the rest of the application works with
    a consistent object.
    """
        def __init__(
                    self,
                    document_id: str,
                    filename: str,
                    text: str,
                    metadata: dict[str, Any] | None=None
                     )-> None:
                self.document_id = document_id
                self.filename = filename
                self.text = text
                self.metadata = metadata if metadata is not None else {}