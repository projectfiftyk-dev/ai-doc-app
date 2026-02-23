# document/loader.py
from pathlib import Path
import docx
import pdfplumber

class DocumentLoader:
    def __init__(self):
        pass

    def load_file(self, file_path: str) -> str:
        # Normalize the path
        file_path = file_path.strip().rstrip("\\/")
        path = Path(file_path)
        ext = path.suffix.lower()

        if ext == ".txt":
            return self._load_txt(path)
        elif ext == ".pdf":
            return self._load_pdf(path)
        elif ext == ".docx":
            return self._load_docx(path)
        else:
            raise ValueError(f"Unsupported file type: {ext}")

    def _load_txt(self, path: Path) -> str:
        with path.open("r", encoding="utf-8") as f:
            return f.read()

    def _load_pdf(self, path: Path) -> str:
        text = ""
        with pdfplumber.open(path) as pdf:
            for page in pdf.pages:
                text += page.extract_text() + "\n"
        return text

    def _load_docx(self, path: Path) -> str:
        doc = docx.Document(path)
        text = "\n".join([p.text for p in doc.paragraphs])
        return text