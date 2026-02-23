# document/loader/docx_loader.py
from .base import BaseLoader
import docx

class DocxLoader(BaseLoader):
    def load_file(self, file_path: str) -> str:
        doc = docx.Document(file_path)
        text = "\n".join([p.text for p in doc.paragraphs if p.text.strip()])
        return text