"""Application settings, loaded from environment variables / a .env file."""

import os

from dotenv import load_dotenv

load_dotenv()


class Settings:
    """Central place for all configuration values."""

    HOST: str = os.getenv("HOST", "127.0.0.1")
    PORT: int = int(os.getenv("PORT", "8000"))

    # Ollama runs the language model locally (https://ollama.com)
    OLLAMA_BASE_URL: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    OLLAMA_MODEL: str = os.getenv("OLLAMA_MODEL", "kurakani")
    OLLAMA_TIMEOUT: float = float(os.getenv("OLLAMA_TIMEOUT", "120"))


settings = Settings()
