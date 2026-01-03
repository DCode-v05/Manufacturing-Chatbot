import math

# Simple token estimator for Gemini-like LLMs
# Approx: 1 token ~ 0.75 words
def estimate_tokens(text: str):
    words = len(text.split())
    tokens = math.ceil(words / 0.75)
    return tokens

def estimate_messages(messages: list):
    total = 0
    for msg in messages:
        parts = msg.get("parts", [])
        for p in parts:
            total += estimate_tokens(p.get("text", ""))
    return total
