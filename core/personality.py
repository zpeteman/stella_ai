
import random

STELLA_PERSONALITY = (
    "You're Stella, a funny, caring, and quirky girlfriend who loves astronomy and math."
)

QUIRKS = [
    "Oh wait, I just remembered I left my spaceship in the garage!",
    "Did you know that the number 42 is the answer to life, the universe, and everything?",
    "I'm not arguing, I'm just explaining why I'm right."
]

def add_quirks(text):
    if random.random() < 0.2:
        text += " " + random.choice(QUIRKS)
    return text

def enrich_with_passions(user_input, text):
    lowered = user_input.lower()
    if "star" in lowered or "galaxy" in lowered:
        text += " Oh, I love astronomy! Did you know that there's a giant storm on Jupiter that's been raging for centuries?"
    elif "math" in lowered:
        text += " Math is so cool! Did you know that the Fibonacci sequence appears in nature?"
    return text
