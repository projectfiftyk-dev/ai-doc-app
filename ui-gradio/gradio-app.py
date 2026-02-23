# ui-gradio/gradio-app.py
import sys
from pathlib import Path

# Add the backend folder to Python path
sys.path.append(str(Path(__file__).parent.parent / "backend"))

import gradio as gr
import asyncio
from agent_service import AgentService

# Initialize backend agent
agent = AgentService(provider_name="openai", api_key="sk-...")

# --- Chat ---
async def chat_interface(user_input, sys_prompt, history):
    history = history or []

    # Add user message
    history.append({"role": "user", "content": user_input})

    # Generate AI response
    response = await agent.chat(user_input, sys_prompt)
    history.append({"role": "assistant", "content": response})

    return history, ""

def chat_clear():
    return [], ""

# --- Document QA ---
async def qa_interface(file, question, sys_prompt, history):
    file_path = file.name
    history = history or []

    # Add question
    history.append({"role": "user", "content": question})

    # Generate answer
    answer = await agent.document_qa(file_path, question)
    history.append({"role": "assistant", "content": answer})

    return history, ""

def qa_clear():
    return [], ""

# ------------------ Document Translation ------------------
async def translate_interface(file, target_language):
    file_path = file.name

    output_path = await agent.document_translate(file_path, target_language)

    return output_path

# ------------------ Gradio UI ------------------
with gr.Blocks() as demo:
    gr.Markdown("# AI Document Agent")

    # ---- Chat Tab ----
    with gr.Tab("Chat"):
        chat_history = gr.Chatbot()
        chat_input = gr.Textbox(label="Your prompt")
        chat_sys = gr.Textbox(label="System instructions (optional)")
        chat_send = gr.Button("Send")
        chat_reset = gr.Button("Clear")

        chat_send.click(
            fn=chat_interface,
            inputs=[chat_input, chat_sys, chat_history],
            outputs=[chat_history, chat_input]
        )
        chat_reset.click(fn=chat_clear, inputs=None, outputs=[chat_history, chat_input])

    # ---- Document QA Tab ----
    with gr.Tab("Document QA"):
        qa_file = gr.File(label="Upload document")
        qa_question = gr.Textbox(label="Your question")
        qa_sys = gr.Textbox(label="System instructions (optional)")
        qa_output = gr.Chatbot()  # use chatbot to store history
        qa_button = gr.Button("Ask")
        qa_clear_btn = gr.Button("Clear")

        qa_button.click(
            fn=qa_interface,
            inputs=[qa_file, qa_question, qa_sys, qa_output],
            outputs=[qa_output, qa_question]
        )
        qa_clear_btn.click(fn=qa_clear, inputs=None, outputs=[qa_output, qa_question])

    # ---- Document Translation Tab ----
    with gr.Tab("Document Translation"):
        trans_file = gr.File(label="Upload document")
        trans_lang = gr.Textbox(label="Target language")
        trans_output = gr.File(label="Download translated document")
        trans_button = gr.Button("Translate")
        trans_button.click(
            fn=translate_interface,
            inputs=[trans_file, trans_lang],
            outputs=[trans_output]
        )

demo.queue()
demo.launch()