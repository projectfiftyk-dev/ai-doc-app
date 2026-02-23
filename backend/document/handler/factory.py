from .docx_handler import DocxHandler
from .doc_handler import DocHandler
from .txt_handler import TxtHandler

class DocumentHandlerFactory:

    handlers = {
        "docx": DocxHandler,
        "doc": DocHandler,
        "txt": TxtHandler
    }

    @staticmethod
    def create(file_ext: str):
        ext = file_ext.lower().replace(".", "")
        if ext in DocumentHandlerFactory.handlers:
            return DocumentHandlerFactory.handlers[ext]()
        else:
            raise ValueError(f"No handler available for {ext}")