from app.llm.base import LLMProvider
from app.llm.gemini_provider import GeminiProvider
from app.llm.mock_provider import MockLLMProvider

from app.config import settings

def get_llm_provider(provider_name: str) -> LLMProvider:

    if provider_name == "mock":
        return MockLLMProvider()

    if provider_name == "gemini":

        if not settings.gemini_api_key:
            raise ValueError(
                "GEMINI_API_KEY is required when using Gemini"
            )

        return GeminiProvider(
            api_key=settings.gemini_api_key,
            model=settings.llm_model
        )
    
    raise ValueError(
        f"Unsupported LLM provider: {provider_name}"
    )