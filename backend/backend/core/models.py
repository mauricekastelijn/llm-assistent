
from .ollama import OllamaBackend


class ModelRegistry(object):
    def __init__(self):
        self.models = {}
        self.ollama = OllamaBackend()
        self.models["chat"] = self.ollama.get_chat_model()
        self.models["chat_json"] = self.ollama.get_chat_model_json()

    def get_chat_model(self):
        return self.models["chat"]

    def get_chat_model_json(self):
        return self.models["chat_json"]
