import httpx

from langchain_ollama import ChatOllama

from utils.logger import logger

from config import settings


class OllamaBackend(object):
    def __init__(self):
        self._pull_models()

    def _pull_models(self):
        logger.info(f"Pulling Ollama model '{settings.OLLAMA_MODEL}' at endpoint '{
                    settings.OLLAMA_ENDPOINT}' ...")
        with httpx.Client() as client:
            response = client.post(
                f"{settings.OLLAMA_ENDPOINT}/api/pull",
                json={"name": settings.OLLAMA_MODEL})
            for chunk in response.iter_lines():
                logger.info(f"Ollama: {chunk}")
        logger.info("Pulling Ollama model done")

    def get_chat_model(self):
        return ChatOllama(model=settings.OLLAMA_MODEL,
                          base_url=settings.OLLAMA_ENDPOINT)

    def get_chat_model_json(self):
        return ChatOllama(model=settings.OLLAMA_MODEL,
                          base_url=settings.OLLAMA_ENDPOINT,
                          format="json",
                          temperature=0.1)
