# document/qa.py
from typing import List
from llm_providers.base import BaseLLMProvider
from document.chunker import Chunker
from document.loader.factory import DocumentLoaderFactory
from pathlib import Path
import numpy as np

class DocumentQA:
    def __init__(self, llm_provider: BaseLLMProvider, chunk_size: int = 500, overlap: int = 50):
        self.llm_provider = llm_provider
        self.chunker = Chunker(chunk_size=chunk_size, overlap=overlap)
        self.chunks: List[str] = []
        self.embeddings: List[np.ndarray] = []

    async def load_and_embed_document(self, text: str):
        # Chunk the document
        self.chunks = self.chunker.chunk_text(text)

        # Embed each chunk
        self.embeddings = []
        for chunk in self.chunks:
            emb = await self.llm_provider.embed_text(chunk)
            self.embeddings.append(np.array(emb))

    def retrieve_relevant_chunks(self, question_embedding: np.ndarray, top_k: int = 3) -> List[str]:
        """
        Retrieve top_k most similar chunks using cosine similarity
        """
        if not self.embeddings:
            raise ValueError("Document not loaded or embeddings not computed")

        similarities = [self.cosine_similarity(question_embedding, emb) for emb in self.embeddings]
        top_indices = np.argsort(similarities)[-top_k:][::-1]
        return [self.chunks[i] for i in top_indices]

    @staticmethod
    def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
        return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-8)