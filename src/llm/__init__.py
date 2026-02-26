from .base import LLMProvider
from .gemini import GeminiProvider
from .claude import ClaudeProvider

def get_provider(provider_name: str, model: str | None = None) -> LLMProvider:
    providers = {
        "gemini": GeminiProvider,
        "claude": ClaudeProvider,
    }
    if provider_name not in providers:
        raise ValueError(f"Unknown LLM provider: '{provider_name}'. Choose from: {list(providers)}")
    return providers[provider_name](model=model)
