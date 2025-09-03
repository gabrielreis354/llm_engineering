import os
import gradio as gr
from transformers import pipeline
from openai import OpenAI

# Configure a API Key da OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Modelos Hugging Face
chatbot = pipeline("text-generation", model="gpt2")
image_captioner = pipeline("image-to-text", model="nlpconnect/vit-gpt2-image-captioning")
speech_to_text = pipeline("automatic-speech-recognition", model="openai/whisper-base")

# Função de chat multimodal
def multimodal_chat(mensagem, imagem, audio, historico):
    resposta_texto = ""

    # Transcreve áudio
    if audio is not None:
        transcricao = speech_to_text(audio)["text"]
        mensagem = (mensagem or "") + " " + transcricao
        resposta_texto += f"(Transcrição de áudio: {transcricao})\n\n"

    # Gera legenda da imagem
    if imagem is not None:
        legenda = image_captioner(imagem)[0]["generated_text"]
        mensagem = (mensagem or "") + f" (imagem: {legenda})"
        resposta_texto += f"(Descrição da imagem: {legenda})\n\n"

    # Resposta do chatbot
    if mensagem:
        saida = chatbot(mensagem, max_length=100, num_return_sequences=1)[0]["generated_text"]
        resposta_texto += saida

    historico.append((mensagem, resposta_texto))
    return historico, historico

# Função de geração de imagem com OpenAI
def gerar_imagem(prompt):
    response = client.images.generate(
        model="gpt-4o-mini",  # ou "dall-e-3"
        prompt=prompt,
        size="512x512"
    )
    return response.data[0].url

# Interface Gradio
with gr.Blocks() as demo:
    gr.Markdown("# 🤖 Chat Multimodal + Geração de Imagens")

    chatbot_ui = gr.Chatbot()
    with gr.Row():
        texto = gr.Textbox(label="Mensagem de texto")
        imagem = gr.Image(label="Envie uma imagem", type="filepath")
        audio = gr.Audio(label="Envie áudio", type="filepath")
    enviar = gr.Button("Enviar")
    estado = gr.State([])

    enviar.click(fn=multimodal_chat,
                 inputs=[texto, imagem, audio, estado],
                 outputs=[chatbot_ui, estado])

    # Seção de geração de imagens
    gr.Markdown("## 🎨 Gerar Imagens com OpenAI")
    prompt_img = gr.Textbox(label="Prompt da Imagem")
    botao_img = gr.Button("Gerar Imagem")
    saida_img = gr.Image(label="Imagem Gerada")

    botao_img.click(fn=gerar_imagem, inputs=prompt_img, outputs=saida_img)

demo.launch()
