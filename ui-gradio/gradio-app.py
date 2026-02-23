# ui-gradio/gradio-app.py
import sys
from pathlib import Path

# Add the backend folder to Python path
sys.path.append(str(Path(__file__).parent.parent / "backend"))

import gradio as gr
import asyncio
from agent_service import AgentService
import os


# Initialize backend agent
agent = AgentService(provider_name="openai", api_key="sk-...")

# --- Chat ---
async def chat_interface(user_input, sys_prompt=""):
    return await agent.chat(user_input, sys_prompt)

# --- Document QA ---
async def qa_interface(file, question, top_k=3):
    file_path = file.name  # Gradio saves uploads as temporary file
    return await agent.document_qa(file_path, question, top_k)

# --- Document Translation ---
async def translate_interface(file, target_language):
    file_path = file.name
    return await agent.document_translate(file_path, target_language)

# --- Gradio UI ---
with gr.Blocks() as demo:
    gr.Markdown("# AI Document Agent")

    with gr.Tab("Chat"):
        chat_input = gr.Textbox(label="Your prompt")
        chat_output = gr.Textbox(label="Response")
        chat_button = gr.Button("Send")
        chat_button.click(fn=chat_interface, inputs=[chat_input], outputs=[chat_output])

    with gr.Tab("Document QA"):
        qa_file = gr.File(label="Upload document")
        qa_question = gr.Textbox(label="Your question")
        qa_output = gr.Textbox(label="Answer")
        qa_button = gr.Button("Ask")
        qa_button.click(fn=qa_interface, inputs=[qa_file, qa_question], outputs=[qa_output])

    with gr.Tab("Document Translation"):
        trans_file = gr.File(label="Upload document")
        trans_lang = gr.Textbox(label="Target language")
        trans_output = gr.Textbox(label="Translated text")
        trans_button = gr.Button("Translate")
        trans_button.click(fn=translate_interface, inputs=[trans_file, trans_lang], outputs=[trans_output])

demo.launch()