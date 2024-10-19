
from .ollama import OllamaBackend


class ModelRegistry(object):
    def __init__(self):
        self.models = {}
        self.ollama = OllamaBackend()
        self.models["chat"] = self.ollama.get_chat_model()

    def get_chat_model(self):
        return self.models["chat"]
