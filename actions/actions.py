# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


#This is a simple example for a custom action which utters "Hello World!"

import json
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import ActionExecuted, SessionStarted, EventType
import requests
from rasa_sdk import Action
from rasa_sdk.executor import CollectingDispatcher


# Carica la chiave API da config.json
with open("config.json") as f:
    config = json.load(f)

OPENROUTER_API_KEY = config["openrouter_api_key"]

class ActionHelloWorld(Action):

    def name(self) -> Text:
        return "action_hello_world"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text="Hello World!")

        return []


    
class ActionSessionStart(Action):
    def name(self) -> str:
        return "action_session_start"

    async def run(self, dispatcher: CollectingDispatcher,
                  tracker: Tracker,
                  domain: dict) -> list[EventType]:


        # Inizializza la sessione
        events = [SessionStarted(), ActionExecuted("action_listen")]
        
        dispatcher.utter_message(text="Benvenuto nel bot 👋")

        return events
    
class ActionAskLLama3(Action):
    def name(self):
        return "action_ask_llama3"

    def run(self, dispatcher, tracker, domain):
        user_message = tracker.latest_message.get("text")

        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "meta-llama/llama-3-70b-instruct",
                "messages": [
                    {"role": "system", "content": "Sei un assistente utile e amichevole."},
                    {"role": "user", "content": user_message}
                ]
            }
        )

        if response.status_code == 200:
            reply = response.json()["choices"][0]["message"]["content"]
        else:
            reply = "Mi dispiace, si è verificato un errore con LLaMA."

        dispatcher.utter_message(reply)
        return []
