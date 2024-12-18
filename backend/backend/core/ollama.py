import httpx

from pydantic.json_schema import JsonSchemaValue
from typing import Literal, Union

from langchain_ollama import ChatOllama

from config import settings
from utils.logger import logger


class OllamaBackend(object):
    def __init__(self):
        self._pull_models()

    def _pull_models(self):
        logger.info(
            f"Pulling Ollama model '{settings.OLLAMA_MODEL}' at endpoint '{
                    settings.OLLAMA_ENDPOINT}' ..."
        )
        with httpx.Client() as client:
            response = client.post(
                f"{settings.OLLAMA_ENDPOINT}/api/pull",
                json={"name": settings.OLLAMA_MODEL},
            )
            for chunk in response.iter_lines():
                logger.info(f"Ollama: {chunk}")
        logger.info("Pulling Ollama model done")

    def get_chat_model(self):
        return ChatOllama(
            model=settings.OLLAMA_MODEL, base_url=settings.OLLAMA_ENDPOINT
        )

    def get_chat_model_json(
        self, format: Union[Literal["", "json"], JsonSchemaValue] = "json"
    ):
        """
        Get the chat model with the specified format.

        Args:
            format Specify the format of the output (options: "json", JSON schema).

        Returns:
            ChatOllama: An instance of the ChatOllama class with the specified format.
        """
        # FIXME: despite the langchain documentation, a JsonSchemaValue is not a valid value for the format parameter
        return ChatOllama(
            model=settings.OLLAMA_MODEL,
            base_url=settings.OLLAMA_ENDPOINT,
            format="json",
            temperature=0.1,
        )
