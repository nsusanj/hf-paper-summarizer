from __future__ import annotations

import os
import anthropic
from .base import LLMProvider

DEFAULT_MODEL = "claude-sonnet-4-6"


class ClaudeProvider(LLMProvider):
    """Anthropic Claude backend — production use once API key is set up."""

    def __init__(self, model: str | None = None):
        api_key = os.environ.get("ANTHROPIC_API_KEY")
        if not api_key:
            raise EnvironmentError(
                "ANTHROPIC_API_KEY is not set. Get a key at https://console.anthropic.com\n"
                "Note: this is separate from your claude.ai Pro subscription."
            )
        self.client = anthropic.Anthropic(api_key=api_key)
        self.model_name = model or DEFAULT_MODEL

    def complete(self, system_prompt: str, user_prompt: str) -> str:
        message = self.client.messages.create(
            model=self.model_name,
            max_tokens=4096,
            system=system_prompt,
            messages=[{"role": "user", "content": user_prompt}],
        )
        return message.content[0].text
