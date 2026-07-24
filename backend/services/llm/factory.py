"""
LLM Provider Factory
--------------------
Provides OmniRoute AI Gateway as the single unified LLM platform for Vivara.
"""
from __future__ import annotations

from backend.config import Settings
from backend.services.llm.base import LLMProvider
from backend.services.llm.omniroute_provider import OmniRouteProvider
from backend.services.llm.fallback_provider import FallbackLLMProvider


def get_llm_provider(settings: Settings) -> LLMProvider:
    """
    Returns the OmniRoute AI Gateway provider wrapped in FallbackLLMProvider.
    OmniRoute is the sole unified LLM platform for Vivara.
    """
    primary = OmniRouteProvider(
        base_url=settings.llm_base_url or "http://localhost:20128/v1",
        api_key=settings.llm_api_key or "",
        model=settings.llm_model or "auto"
    )
    return FallbackLLMProvider(primary_provider=primary)
