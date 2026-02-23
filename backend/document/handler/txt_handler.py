from pathlib import Path
from .base import BaseDocumentHandler


class TxtHandler(BaseDocumentHandler):
    """
    Handler for .txt files.
    Reads the text, translates via TextTranslator, and saves a new file.
    """

    async def translate(self, file_path: str, text_translator, target_language: str) -> str:
        file_path = Path(file_path)

        # Read original text
        text = file_path.read_text(encoding="utf-8")

        # Translate using the TextTranslator
        translated_text = await text_translator.translate_text(
            text, target_language
        )

        # Save translated text to new file
        output_path = file_path.with_name(f"{file_path.stem}_{target_language}.txt")
        output_path.write_text(translated_text, encoding="utf-8")

        return str(output_path)