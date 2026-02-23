# document/loader/factory.py
from .txt_loader import TxtLoader
from .pdf_loader import PdfLoader
from .docx_loader import DocxLoader
from .uri_loader import UriLoader

class DocumentLoaderFactory:
    loaders = {
        "txt": TxtLoader,
        "pdf": PdfLoader,
        "docx": DocxLoader,
        "uri": UriLoader
    }

    @staticmethod
    def create(file_ext: str):
        ext = file_ext.lower().replace(".", "")
        if ext in DocumentLoaderFactory.loaders:
            return DocumentLoaderFactory.loaders[ext]()
        else:
            raise ValueError(f"No loader available for {ext}")