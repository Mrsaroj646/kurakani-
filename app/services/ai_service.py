from openai import OpenAI

class AIService:
    def __init__(self):
        self.client = OpenAI(
            api_key="fake-local-key-for-ollama",
            base_url="http://localhost:11434/v1"
        )

    def generate_chat_response(self, message: str) -> str:
        response = self.client.chat.completions.create(
            model="kurakani",
            messages=[{"role": "user", "content": message}]
        )
        return response.choices[0].message.content

ai_service = AIService()