
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")
MODEL = os.getenv("MODEL_NAME")
ENDPOINT = "https://openrouter.ai/api/v1/chat/completions"
