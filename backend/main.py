import asyncio
from llm_providers.factory import LLMProviderFactory

async def main():
    # 1️⃣ List available providers
    print("Available providers:", LLMProviderFactory.list_providers())

    # 2️⃣ Create OpenAI provider instance
    provider = LLMProviderFactory.create("openai", api_key="sk-...")
    # 3️⃣ Test API key
    success = await provider.test()
    print("API key test passed:", success)

    # 4️⃣ List available models
    models = await provider.list_models()
    print("Available OpenAI models (first 10):", models[:10])

    # 5️⃣ Simple chat with streaming
    print("\nStreaming response from OpenAI:")
    async for token in provider.stream(
        messages=[{"role": "user", "content": "Hello, can you introduce yourself?"}],
        model="gpt-3.5-turbo"
    ):
        print(token, end="", flush=True)
    print("\n\nStreaming complete!")

# Run async main
if __name__ == "__main__":
    asyncio.run(main())