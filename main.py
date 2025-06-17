from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests

app = FastAPI()

class UserMessage(BaseModel):
    sender: str
    message: str

RASA_URL = "http://localhost:5005/webhooks/rest/webhook"

@app.post("/chat/")
def chat_with_bot(user_message: UserMessage):
    payload = {
        "sender": user_message.sender,
        "message": user_message.message
    }

    try:
        response = requests.post(RASA_URL, json=payload)
        response.raise_for_status()
        bot_responses = response.json()

        # Estrarre i messaggi di testo del bot
        texts = [msg.get("text") for msg in bot_responses if "text" in msg]

        return {"responses": texts}
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))
