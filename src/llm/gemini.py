from __future__ import annotations

import os
from google import genai
from .base import LLMProvider

DEFAULT_MODEL = "gemini-1.5-flash"


class GeminiProvider(LLMProvider):
    """Google Gemini backend — free tier, used for prototyping."""

    def __init__(self, model: str | None = None):
        api_key = os.environ.get("GOOGLE_API_KEY")
        if not api_key:
            raise EnvironmentError("GOOGLE_API_KEY is not set. Get a free key at https://aistudio.google.com")
        self.client = genai.Client(api_key=api_key)
        self.model_name = model or DEFAULT_MODEL

    def complete(self, system_prompt: str, user_prompt: str) -> str:
        # Gemini combines system + user prompt in a single message
        full_prompt = f"{system_prompt}\n\n{user_prompt}"
        response = self.client.models.generate_content(
            model=self.model_name,
            contents=full_prompt,
        )
        return response.text
