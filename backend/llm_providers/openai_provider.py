# llm_providers/openai_provider.py
import openai
from typing import List, Dict, AsyncIterator
from .base import BaseLLMProvider
import asyncio

class OpenAIProvider(BaseLLMProvider):
    """
    Concrete LLM provider implementation for OpenAI.
    Implements BaseLLMProvider interface.
    """

    def __init__(self, api_key: str, base_url: str = None):
        self.api_key = api_key
        if base_url:
            openai.api_base = base_url
        openai.api_key = api_key

    async def list_models(self) -> List[str]:
        """Return a list of available OpenAI models."""
        resp = openai.Model.list()
        return [m['id'] for m in resp['data']]

    async def test(self, model: str = "gpt-3.5-turbo") -> bool:
        try:
            # Simple call to check if model works
            prompt = "Say hello"
            await self.complete(messages=[{"role": "user", "content": prompt}], model=model)
            return True
        except Exception:
            return False
        
    async def complete(
        self,
        messages: List[Dict],
        model: str,
        system_instruction: str = ""
    ) -> str:
        """Return full response (non-streaming)."""
        chat_messages = []
        if system_instruction:
            chat_messages.append({"role": "system", "content": system_instruction})
        chat_messages.extend(messages)

        resp = openai.ChatCompletion.create(
            model=model,
            messages=chat_messages
        )
        return resp['choices'][0]['message']['content']

    async def stream(
        self,
        messages: List[Dict],
        model: str,
        system_instruction: str = ""
    ) -> AsyncIterator[str]:
        """Stream response token by token."""
        chat_messages = []
        if system_instruction:
            chat_messages.append({"role": "system", "content": system_instruction})
        chat_messages.extend(messages)

        stream_resp = openai.ChatCompletion.create(
            model=model,
            messages=chat_messages,
            stream=True
        )

        for event in stream_resp:
            if 'choices' in event:
                delta = event['choices'][0]['delta']
                if 'content' in delta:
                    yield delta['content']
                    await asyncio.sleep(0)  # allow async streaming

    async def embed_text(self, text: str, model: str = "text-embedding-3-large") -> list:
        resp = openai.Embedding.create(
            input=text,
            model=model
        )
        return resp["data"][0]["embedding"]