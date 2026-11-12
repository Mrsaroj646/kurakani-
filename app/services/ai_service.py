"""Service layer that talks to the local Ollama language model."""

import httpx

from app.config import settings


class AIServiceError(Exception):
    """Raised when the AI model cannot produce a response."""


class AIService:
    def __init__(self, base_url: str, model: str, timeout: float):
        self.base_url = base_url.rstrip("/")
        self.model = model
        self.timeout = timeout

    def generate_chat_response(self, message: str) -> str:
        """Send the user's message to Ollama and return the model's reply."""
        payload = {
            "model": self.model,
            "messages": [{"role": "user", "content": message}],
            "stream": False,
        }

        try:
            response = httpx.post(
                f"{self.base_url}/api/chat", json=payload, timeout=self.timeout
            )
        except httpx.HTTPError as exc:
            raise AIServiceError(
                f"Could not reach Ollama at {self.base_url}. Is it running?"
            ) from exc

        if response.status_code == 404:
            raise AIServiceError(
                f"Model '{self.model}' was not found. "
                f"Create it with: ollama create {self.model} -f Modelfile"
            )
        if response.status_code != 200:
            raise AIServiceError(f"Ollama returned an error ({response.status_code}).")

        return response.json().get("message", {}).get("content", "").strip()


ai_service = AIService(
    base_url=settings.OLLAMA_BASE_URL,
    model=settings.OLLAMA_MODEL,
    timeout=settings.OLLAMA_TIMEOUT,
)
