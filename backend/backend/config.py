from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    OLLAMA_ENDPOINT: str = "http://ollama:7869"
    OLLAMA_MODEL: str = "qwen2.5-coder:32b"


settings = Settings()
