from backend.config import Settings
from backend.services.llm.base import LLMProvider
from backend.services.llm.omniroute_provider import OmniRouteProvider
from backend.services.llm.ollama_provider import OllamaProvider
from backend.services.llm.openai_compat import OpenAICompatProvider

def get_llm_provider(settings: Settings) -> LLMProvider:
    """
    Returns the appropriate LLM provider based on settings.
    
    Default order for 'auto':
    1. OmniRoute Gateway (universal multi-backend router)
    2. Ollama (local)
    3. OpenAI-compatible endpoint
    """
    provider = (settings.llm_provider or "auto").lower()

    if provider == "omniroute":
        return OmniRouteProvider(
            base_url=settings.llm_base_url or "http://localhost:7777/v1",
            api_key=settings.llm_api_key,
            model=settings.llm_model or "auto"
        )
    elif provider == "ollama":
        return OllamaProvider(
            base_url=settings.llm_base_url or "http://localhost:11434",
            model=settings.llm_model or "llama3.2"
        )
    elif provider in ["openai_compat", "lm_studio", "vllm", "openrouter", "custom"]:
        return OpenAICompatProvider(
            base_url=settings.llm_base_url,
            api_key=settings.llm_api_key,
            model=settings.llm_model
        )
    else:  # "auto" mode
        # By default, use OmniRoute if configured or default to OmniRoute/Ollama provider
        if settings.llm_base_url and ("7777" in settings.llm_base_url or "omniroute" in settings.llm_base_url):
            return OmniRouteProvider(
                base_url=settings.llm_base_url,
                api_key=settings.llm_api_key,
                model=settings.llm_model
            )
        # Default auto falls back to Ollama or OpenAICompat depending on API key presence
        if settings.llm_api_key:
            return OpenAICompatProvider(
                base_url=settings.llm_base_url or "https://openrouter.ai/api/v1",
                api_key=settings.llm_api_key,
                model=settings.llm_model or "auto"
            )
        return OllamaProvider(
            base_url=settings.llm_base_url or "http://localhost:11434",
            model=settings.llm_model or "llama3.2"
        )
