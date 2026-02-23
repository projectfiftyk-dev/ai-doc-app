# main.py
import asyncio
from llm_providers.factory import LLMProviderFactory
from agent_service import AgentService
import os

async def main():
    # --- Step 1: Create AgentService with OpenAI ---
    agent = AgentService(provider_name="openai", api_key="sk-...")

    # Test provider
    test_passed = await agent.provider.test()
    print("API key test passed:", test_passed)

    # --- Step 2: Document QA ---
    doc_file = r"path-to-sample"
    question = "What is the main topic of the document?"
    
    import os
    print(os.path.exists(doc_file))  # Should be True
    print(os.path.basename(doc_file))  # Should print 'sample.txt'

    answer = await agent.document_qa(doc_file, question, top_k=3)
    print("\nAnswer from document QA:")
    print(answer)

    # --- Optional: Document Translation ---
    target_language = "Spanish"
    translated_text = await agent.document_translate(doc_file, target_language)
    print("\nTranslated document preview (first 500 chars):")
    print(translated_text[:500])

    # --- Optional: Chat mode test ---
    user_prompt = "Say hello in a friendly way."
    chat_response = await agent.chat(user_prompt)
    print("\nChat response:")
    print(chat_response)

if __name__ == "__main__":
    asyncio.run(main())