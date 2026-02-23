# llm_providers/base.py
from abc import ABC, abstractmethod
from typing import List, Dict, AsyncIterator

class BaseLLMProvider(ABC):
    """
    Abstract base class for all LLM providers.
    All concrete providers must implement these methods.
    """

    @abstractmethod
    async def list_models(self) -> List[str]:
        """
        Return a list of available models for this provider.
        """
        pass

    @abstractmethod
    async def test(self) -> bool:
        """
        Test the provider API key / connectivity.
        Returns True if successful, False otherwise.
        """
        pass

    @abstractmethod
    async def complete(
        self,
        messages: List[Dict],
        model: str,
        system_instruction: str = ""
    ) -> str:
        """
        Returns the full response (non-streaming) from the model.
        
        :param messages: List of message dicts, e.g. [{"role": "user", "content": "Hi"}]
        :param model: Name of the model to use
        :param system_instruction: Optional system prompt
        :return: Full response string
        """
        pass

    @abstractmethod
    async def stream(
        self,
        messages: List[Dict],
        model: str,
        system_instruction: str = ""
    ) -> AsyncIterator[str]:
        """
        Streams the response token by token from the model.
        
        :param messages: List of message dicts
        :param model: Name of the model to use
        :param system_instruction: Optional system prompt
        :yield: Tokens as strings
        """
        pass

    @abstractmethod
    async def embed_text(self, text: str, model: str = None) -> list:
        """
        Return embeddings for the given text.
        """
        pass