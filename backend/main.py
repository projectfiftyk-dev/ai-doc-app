# main.py
import asyncio
from llm_providers.factory import LLMProviderFactory
from document.qa import DocumentQA
import os

async def main():
    # --- Step 1: Create LLM Provider ---
    provider = LLMProviderFactory.create("openai", api_key="sk-...")

    # Test provider
    test_passed = await provider.test()
    print("API key test passed:", test_passed)

    # --- Step 2: Load document and embed chunks ---
    doc_file = "C:\Coding\Sample_Files\sample.txt"  # replace with your test file (TXT, PDF, DOCX)
    doc_qa = DocumentQA(llm_provider=provider)
    await doc_qa.load_and_embed_document(doc_file)
    print(f"Document loaded and embedded. Total chunks: {len(doc_qa.chunks)}")

    # --- Step 3: Ask a sample question ---
    question = "What is the main topic of the document?"
    question_embedding = await provider.embed_text(question)

    # Retrieve top 3 relevant chunks
    top_chunks = doc_qa.retrieve_relevant_chunks(question_embedding, top_k=3)
    print("\nTop 3 chunks for the question:")
    for i, chunk in enumerate(top_chunks, 1):
        print(f"\n--- Chunk {i} ---\n{chunk[:500]}...")  # show first 500 chars

if __name__ == "__main__":
    asyncio.run(main())