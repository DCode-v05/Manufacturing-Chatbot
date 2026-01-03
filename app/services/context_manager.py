class ContextManager:
    def __init__(self, max_messages=6):
        self.max_messages = max_messages
        self.history = []

    def add(self, role, text):
        self.history.append({"role": role, "text": text})
        if len(self.history) > self.max_messages:
            self.history.pop(0)

    def get(self):
        messages = []
        for msg in self.history:
            messages.append({
                "role": "user" if msg["role"] == "user" else "model",
                "parts": [{"text": msg["text"]}]
            })
        return messages
