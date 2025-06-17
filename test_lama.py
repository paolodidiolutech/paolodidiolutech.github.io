import json
import requests

# Carica la chiave API da config.json
with open("config.json") as f:
    config = json.load(f)

OPENROUTER_API_KEY = config["openrouter_api_key"]

headers = {
    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
    "Content-Type": "application/json"
}

data = {
    "model": "meta-llama/llama-3-70b-instruct",  # puoi provare anche "8b"
    "messages": [
        {"role": "system", "content": "Sei un assistente amichevole e utile."},
        {"role": "user", "content": "Qual è la capitale della Francia?"}
    ]
}

response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)

if response.status_code == 200:
    reply = response.json()["choices"][0]["message"]["content"]
    print(f"✅ Risposta LLaMA 3:\n{reply}")
else:
    print("❌ Errore nella chiamata:")
    print("Status code:", response.status_code)
    try:
        print("Messaggio:", response.json())
    except:
        print(response.text)
