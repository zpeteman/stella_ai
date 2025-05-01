
import json
import os

CONV_FILE = "conversation_history.json"

def load_conversation_history():
    if os.path.exists(CONV_FILE):
        with open(CONV_FILE, "r") as f:
            return json.load(f)
    return []

def save_conversation_history(history):
    with open(CONV_FILE, "w") as f:
        json.dump(history, f, indent=2)
