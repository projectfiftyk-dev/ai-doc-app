from typing import List
import asyncio


class TextTranslator:
    """
    Provider-agnostic text translation layer.
    Handles chunking, batching and prompt standardization.
    """

    def __init__(
        self,
        llm_provider,
        model: str,
        max_chunk_chars: int = 4000,
        concurrent_requests: int = 5
    ):
        self.provider = llm_provider
        self.model = model
        self.max_chunk_chars = max_chunk_chars
        self.concurrent_requests = concurrent_requests

    # ----------------------------------------------------
    # Public API
    # ----------------------------------------------------

    async def translate_text(self, text: str, target_language: str) -> str:
        """
        Translates arbitrary-length text safely.
        Automatically chunks if needed.
        """
        if len(text) <= self.max_chunk_chars:
            return await self._translate_chunk(text, target_language)

        chunks = self._chunk_text(text)
        translated_chunks = await self._translate_in_batches(
            chunks, target_language
        )

        return "".join(translated_chunks)

    # ----------------------------------------------------
    # Internal Helpers
    # ----------------------------------------------------

    async def _translate_chunk(self, chunk: str, target_language: str) -> str:
        """
        Translate a single chunk via LLM.
        """

        system_instruction = (
            "You are a professional translation engine. "
            "Translate the text exactly as provided. "
            "Preserve formatting, punctuation, line breaks, and structure. "
            "Do not summarize. Do not add explanations."
        )

        user_prompt = f"Translate the following text to {target_language}:\n\n{chunk}"

        response = await self.provider.complete(
            messages=[{"role": "user", "content": user_prompt}],
            model=self.model,
            system_instruction=system_instruction
        )

        return response

    def _chunk_text(self, text: str) -> List[str]:
        """
        Character-based chunking to avoid token overflow.
        Keeps structure intact.
        """
        chunks = []
        start = 0
        while start < len(text):
            end = start + self.max_chunk_chars
            chunks.append(text[start:end])
            start = end
        return chunks

    async def _translate_in_batches(
        self,
        chunks: List[str],
        target_language: str
    ) -> List[str]:
        """
        Translate chunks concurrently with rate control.
        """

        semaphore = asyncio.Semaphore(self.concurrent_requests)

        async def sem_task(chunk):
            async with semaphore:
                return await self._translate_chunk(chunk, target_language)

        tasks = [sem_task(chunk) for chunk in chunks]
        return await asyncio.gather(*tasks)