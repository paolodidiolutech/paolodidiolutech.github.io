const RASA_ENDPOINT = "http://localhost:5005/webhooks/rest/webhook";

// Funzione per inviare messaggi a Rasa
async function sendMessage(message, sender_id) {
  try {
    const response = await fetch(RASA_ENDPOINT, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        sender: sender_id,
        message: message
      })
    });

    const data = await response.json();
    data.forEach((resp) => {
      if (resp.text) {
        appendMessage("bot", resp.text);
      }
    });
  } catch (error) {
    appendMessage("bot", "Errore di connessione con il server Rasa.");
    console.error("Errore:", error);
  }
}

// Funzione per aggiungere un messaggio nella chat
function appendMessage(sender, message) {
  const chats = document.getElementById("chats");
  const msgDiv = document.createElement("div");
  msgDiv.textContent = `${sender === "user" ? "You" : "Bot"}: ${message}`;
  msgDiv.style.marginBottom = "10px";
  chats.appendChild(msgDiv);
  chats.scrollTop = chats.scrollHeight;
}

// Funzione per gestire l'invio dell'input utente
function handleUserMessage() {
  const input = document.getElementById("userInput");
  const message = input.value.trim();
  if (!message) return;

  appendMessage("user", message);
  input.value = "";

  const sender_id = localStorage.getItem("sender_id") || generateSenderId();
  sendMessage(message, sender_id);
}

// Genera un ID utente univoco (persistente nella sessione)
function generateSenderId() {
  const id = "user_" + Math.random().toString(36).substring(7);
  localStorage.setItem("sender_id", id);
  return id;
}

// Event listener per bottone "Send"
document.getElementById("sendButton").addEventListener("click", handleUserMessage);

// Event listener per invio con "Enter"
document.getElementById("userInput").addEventListener("keypress", function (e) {
  if (e.key === "Enter" && !e.shiftKey) {
    e.preventDefault();
    handleUserMessage();
  }
});

// Pulsante "Clear"
document.getElementById("clear").addEventListener("click", () => {
  document.getElementById("chats").innerHTML = "";
});

// Pulsante "Restart" (resetta la sessione utente)
document.getElementById("restart").addEventListener("click", () => {
  localStorage.removeItem("sender_id");
  document.getElementById("chats").innerHTML = "";
  appendMessage("bot", "Sessione riavviata. Scrivi qualcosa per iniziare!");
});

// Pulsante "Close" (nasconde la chat)
document.getElementById("close").addEventListener("click", () => {
  document.getElementById("chatbot-widget").style.display = "none";
});
