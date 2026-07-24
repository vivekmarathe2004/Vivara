from backend.config import Settings
from backend.services.llm.base import LLMProvider
from backend.services.llm.omniroute_provider import OmniRouteProvider
from backend.services.llm.ollama_provider import OllamaProvider
from backend.services.llm.openai_compat import OpenAICompatProvider
from backend.services.llm.fallback_provider import FallbackLLMProvider


def get_llm_provider(settings: Settings) -> LLMProvider:
    """
    Returns the appropriate LLM provider based on settings, wrapped in
    FallbackLLMProvider for guaranteed zero-crash script generation.
    """
    provider_name = (settings.llm_provider or "auto").lower()

    if provider_name == "omniroute":
        primary = OmniRouteProvider(
            base_url=settings.llm_base_url or "http://localhost:7777/v1",
            api_key=settings.llm_api_key,
            model=settings.llm_model or "auto"
        )
    elif provider_name == "ollama":
        primary = OllamaProvider(
            base_url=settings.llm_base_url or "http://localhost:11434",
            model=settings.llm_model or "llama3.2"
        )
    elif provider_name in ["openai_compat", "lm_studio", "vllm", "openrouter", "custom"]:
        primary = OpenAICompatProvider(
            base_url=settings.llm_base_url,
            api_key=settings.llm_api_key,
            model=settings.llm_model
        )
    else:  # "auto" mode
        if settings.llm_base_url and ("7777" in settings.llm_base_url or "omniroute" in settings.llm_base_url):
            primary = OmniRouteProvider(
                base_url=settings.llm_base_url,
                api_key=settings.llm_api_key,
                model=settings.llm_model
            )
        elif settings.llm_api_key:
            primary = OpenAICompatProvider(
                base_url=settings.llm_base_url or "https://openrouter.ai/api/v1",
                api_key=settings.llm_api_key,
                model=settings.llm_model or "auto"
            )
        else:
            primary = OllamaProvider(
                base_url=settings.llm_base_url or "http://localhost:11434",
                model=settings.llm_model or "llama3.2"
            )

    return FallbackLLMProvider(primary_provider=primary)
