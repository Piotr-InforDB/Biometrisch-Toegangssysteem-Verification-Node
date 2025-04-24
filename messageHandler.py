from identity import Identity

class MessageHandler:
    def __init__(self):
        self.identity = Identity()
        self.client = None
        self.handlers = {
            "presence": self.handle_presence,
            "client/identity": self.handle_identity,
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

    def handle_identity(self, payload) -> None:
        print(f"Identity detected: {payload}")
        if payload != self.identity.id:
            return
        print('Identity confirmed')
        self.client.publish(f"client/identity/{self.identity.id}", self.identity.get_identity_json())