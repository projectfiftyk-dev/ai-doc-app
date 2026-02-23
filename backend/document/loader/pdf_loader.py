# document/loader/pdf_loader.py
from .base import BaseLoader
import pdfplumber

class PdfLoader(BaseLoader):
    def load_file(self, file_path: str) -> str:
        text = ""
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        return text