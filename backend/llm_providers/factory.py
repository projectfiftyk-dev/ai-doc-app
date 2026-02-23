# llm_providers/factory.py
from .openai_provider import OpenAIProvider
from .base import BaseLLMProvider
from typing import List

class LLMProviderFactory:
    """
    Factory to create LLM provider instances.
    Keeps a registry of available providers.
    """
    
    _registry = {
        "openai": OpenAIProvider
    }

    @staticmethod
    def create(provider_name: str, **kwargs) -> BaseLLMProvider:
        """
        Create a provider instance by name.
        
        :param provider_name: Name of the provider ("openai", etc.)
        :param kwargs: Provider-specific parameters (e.g., api_key)
        :return: Instance of a concrete BaseLLMProvider
        """
        provider_cls = LLMProviderFactory._registry.get(provider_name.lower())
        if not provider_cls:
            raise ValueError(f"Provider '{provider_name}' is not supported")
        return provider_cls(**kwargs)

    @staticmethod
    def list_providers() -> List[str]:
        """
        Return a list of all registered provider names.
        """
        return list(LLMProviderFactory._registry.keys())