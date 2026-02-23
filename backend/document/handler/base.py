from abc import ABC, abstractmethod

class BaseDocumentHandler(ABC):

    @abstractmethod
    async def translate(self, file_path: str, text_translator, target_language: str) -> str:
        """
        Translates document and returns output file path.
        """
        pass