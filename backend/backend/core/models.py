
from .ollama import OllamaBackend


class ModelRegistry(object):
    def __init__(self):
        self.models = {}
        self.ollama = OllamaBackend()

    def get_chat_model(self):
        return self.ollama.get_chat_model()

    def get_chat_model_json(self, format="json"):
        return self.ollama.get_chat_model_json(format)
