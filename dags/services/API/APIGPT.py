import requests
import os
import json
import logging

from libs.Config import Config

# prompt para o GPT:
prompt = """
Preencha os campos do seguinte objeto JSON com base nos dados fornecidos abaixo. 
Utilize os dados disponíveis de forma inteligente. 
Respeite rigorosamente os tipos e formatos solicitados.

Objeto JSON de saída:

{
  "link": string,                 // use o campo "link" do objeto original
  "texto": string,                // use o texto mais completo e relevante (articleBody, description ou snippet) e tente junta-lo com um titulo (se houver) para ficar mais completo.
  "temImagem": boolean,           // true se houver imagem detectável (ex: og:image ou cse_image)
  "temVideo": boolean,            // true se for mencionado ou detectado vídeo (ex: metatags, texto, etc), senão false
  "dataPublish": string,          // data em formato YYYY-MM-DD, use o campo dateModified se possível, senão tente inferir do texto
  "sentimento": int               // 0 - neutro ou indeterminado, 1 - positivo, 2 - negativo
}

Dado o seguinte objeto de entrada, responda com **apenas** o JSON preenchido, sem explicações ou texto adicional.

Objeto JSON de entrada:

"""

config = Config()

OPENAI_API_KEY = config.openai_api_key
OPENAI_API_URL = config.openai_api_url

if not OPENAI_API_KEY or not OPENAI_API_URL:
    raise ValueError("OPENAI_API_KEY ou OPENAI_API_URL não estão configurados corretamente.")


def chat(obj:dict):

    model: str = "gpt-3.5-turbo-1106"

    messages = [
        {
            "role": "system",
            "content": "Você é um assistente especializado em preencher objetos JSON com dados de outros objetos JSON."
        },
        {
            "role": "user",
            "content": prompt + json.dumps(obj, ensure_ascii=False, indent=2)
        }
    ]

    try:

        logging.info("Iniciando requisição para a API OpenAI...")

        url = f"{OPENAI_API_URL}"

        headers = {
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": model,
            "messages": messages,
            "temperature": 0
        }
    
        response = requests.post(url, json=payload, headers=headers, timeout=30)
        response.raise_for_status()

        data = response.json()
        choices = data.get("choices", [])
        if not choices or "message" not in choices[0]:
            raise RuntimeError("Resposta inesperada da API OpenAI.")
        
        return data["choices"][0]["message"]["content"].strip()
    
    except requests.exceptions.RequestException as e:
        logging.error(f"Erro ao chamar a API OpenAI: {e}")