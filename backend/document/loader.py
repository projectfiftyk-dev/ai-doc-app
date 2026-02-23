# document/loader.py
from pathlib import Path
import docx
import pdfplumber

class DocumentLoader:
    def __init__(self):
        pass

    def load_file(self, file_path: str) -> str:
        ext = Path(file_path).suffix.lower()
        if ext == ".txt":
            return self._load_txt(file_path)
        elif ext == ".pdf":
            return self._load_pdf(file_path)
        elif ext == ".docx":
            return self._load_docx(file_path)
        else:
            raise ValueError(f"Unsupported file type: {ext}")

    def _load_txt(self, file_path: str) -> str:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()

    def _load_pdf(self, file_path: str) -> str:
        text = ""
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                text += page.extract_text() + "\n"
        return text

    def _load_docx(self, file_path: str) -> str:
        doc = docx.Document(file_path)
        text = "\n".join([p.text for p in doc.paragraphs])
        return text