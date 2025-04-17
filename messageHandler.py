from identity import Identity

class MessageHandler:
    def __init__(self):
        self.identity = Identity()
        self.client = None
        self.handlers = {
            "presence": self.handle_presence
        }

    def set_client(self, client):
        self.client = client

    def handle_message(self, topic: str, payload) -> None:
        if topic in self.handlers:
            self.handlers[topic](payload)
        else:
            print(f"No handler found for topic: {topic}")

    def handle_presence(self, payload) -> None:
        print(f"Presence detected: {payload}")
        self.client.publish("presence/confirm", self.identity.get_identity_json())