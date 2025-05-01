
import requests
import json
from .config import API_KEY, MODEL, ENDPOINT
from .personality import STELLA_PERSONALITY, add_quirks, enrich_with_passions
from .history import save_conversation_history

def chat_with_rima(user_input, conversation_history=None):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    if conversation_history is None:
        conversation_history = []

    messages = [{"role": "system", "content": STELLA_PERSONALITY}]
    for conv in conversation_history:
        messages.append({"role": "user", "content": conv["user"]})
        messages.append({"role": "assistant", "content": conv["assistant"]})
    messages.append({"role": "user", "content": user_input})

    data = {
        "model": MODEL,
        "messages": messages
    }

    response = requests.post(ENDPOINT, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        assistant_response = response.json()["choices"][0]["message"]["content"]
        assistant_response = add_quirks(assistant_response)
        assistant_response = enrich_with_passions(user_input, assistant_response)

        conversation_history.append({
            "user": user_input,
            "assistant": assistant_response
        })
        save_conversation_history(conversation_history)
        return assistant_response
    else:
        return f"Error: {response.status_code}"
