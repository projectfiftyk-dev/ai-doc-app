# agent_service.py
import asyncio
from pathlib import Path
from document.loader.factory import DocumentLoaderFactory
from llm_providers.factory import LLMProviderFactory
from document.qa import DocumentQA
from document.chunker import Chunker

class AgentService:
    def __init__(self, provider_name: str, api_key: str, model: str = "gpt-3.5-turbo"):
        # Create the LLM provider
        self.provider = LLMProviderFactory.create(provider_name, api_key=api_key)
        self.model = model

    async def chat(self, user_prompt: str, sys_prompt: str = "") -> str:
        """Text-to-Text Chat mode"""
        messages = []
        if sys_prompt:
            messages.append({"role": "system", "content": sys_prompt})
        messages.append({"role": "user", "content": user_prompt})
        response = await self.provider.complete(
            messages=messages,
            model=self.model
        )
        return response

    async def document_qa(self, doc_path: str, question: str, top_k: int = 3) -> str:
        """Document QA mode"""
        # Use factory to load document
        ext = Path(doc_path).suffix
        loader = DocumentLoaderFactory.create(ext)
        text = loader.load_file(doc_path)

        # Prepare QA
        doc_qa = DocumentQA(llm_provider=self.provider)
        await doc_qa.load_and_embed_document(text)

        # Embed question & retrieve chunks
        question_embedding = await self.provider.embed_text(question)
        top_chunks = doc_qa.retrieve_relevant_chunks(question_embedding, top_k=top_k)
        context = "\n\n".join(top_chunks)

        # Send to LLM to generate answer
        prompt = f"Answer the question based on the following context:\n{context}\n\nQuestion: {question}"
        answer = await self.provider.complete(
            messages=[{"role": "user", "content": prompt}],
            model=self.model
        )
        return answer

    async def document_translate(self, doc_path: str, target_language: str) -> str:
        """Document Translation mode"""
        # Use factory to load document
        ext = Path(doc_path).suffix
        loader = DocumentLoaderFactory.create(ext)
        text = loader.load_file(doc_path)

        # Chunk the document
        chunker = Chunker()
        chunks = chunker.chunk_text(text)

        # Translate each chunk
        translated_chunks = []
        for chunk in chunks:
            prompt = f"Translate the following text to {target_language}:\n\n{chunk}"
            translation = await self.provider.complete(
                messages=[{"role": "user", "content": prompt}],
                model=self.model
            )
            translated_chunks.append(translation)

        # Combine translations
        return "\n\n".join(translated_chunks)