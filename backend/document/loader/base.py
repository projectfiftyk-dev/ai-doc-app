# document/loader/base.py
from abc import ABC, abstractmethod

class BaseLoader(ABC):
    @abstractmethod
    def load_file(self, file_path: str) -> str:
        """Load a file and return its text"""
        pass