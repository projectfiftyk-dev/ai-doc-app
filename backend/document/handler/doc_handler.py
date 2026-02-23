import subprocess
from pathlib import Path
from .base import BaseDocumentHandler
from .docx_handler import DocxHandler


class DocHandler(BaseDocumentHandler):

    async def translate(self, file_path: str, text_translator, target_language: str) -> str:
        file_path = Path(file_path)

        # 1️⃣ Convert .doc → .docx
        converted_path = await self._convert_to_docx(file_path)

        # 2️⃣ Use DocxHandler
        docx_handler = DocxHandler()
        translated_docx = await docx_handler.translate(
            str(converted_path),
            text_translator,
            target_language
        )

        # 3️⃣ Optional: convert back to .doc
        final_doc = await self._convert_to_doc(translated_docx)

        return final_doc


    async def _convert_to_docx(self, file_path: Path) -> Path:
        output_dir = file_path.parent

        subprocess.run([
            "soffice",
            "--headless",
            "--convert-to",
            "docx",
            str(file_path),
            "--outdir",
            str(output_dir)
        ], check=True)

        return output_dir / (file_path.stem + ".docx")


    async def _convert_to_doc(self, file_path: str) -> str:
        file_path = Path(file_path)
        output_dir = file_path.parent

        subprocess.run([
            "soffice",
            "--headless",
            "--convert-to",
            "doc",
            str(file_path),
            "--outdir",
            str(output_dir)
        ], check=True)

        return str(output_dir / (file_path.stem + ".doc"))