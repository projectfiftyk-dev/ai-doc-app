# document/loader/txt_loader.py
from .base import BaseLoader

class TxtLoader(BaseLoader):
    def load_file(self, file_path: str) -> str:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()