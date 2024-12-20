from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    OLLAMA_ENDPOINT: str = "http://ollama:7869"
    OLLAMA_MODEL: str = "llama3.1:8b"


settings = Settings()
