from abc import ABC, abstractmethod


class LLMProvider(ABC):
    """Abstract interface for LLM backends. Swap providers by implementing this."""

    @abstractmethod
    def complete(self, system_prompt: str, user_prompt: str) -> str:
        """Send a prompt and return the generated text response."""
        ...
