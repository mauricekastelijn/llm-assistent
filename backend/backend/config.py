from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    OLLAMA_ENDPOINT: str = "http://ollama:7869"
    OLLAMA_MODEL: str = "llama3.2"

    class Config:
        env_file = ".env"


settings = Settings()
