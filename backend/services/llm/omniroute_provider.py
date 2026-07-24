"""
OmniRoute LLM Provider
----------------------
Integrates OmniRoute — an open-source, provider-agnostic OpenAI-compatible
router proxy that unifies local models (Ollama, vLLM, LM Studio) and cloud APIs
(OpenRouter, Groq, Anthropic, OpenAI, DeepSeek) under a single endpoint.
"""
from __future__ import annotations

import logging
import httpx
from backend.services.llm.base import LLMProvider

logger = logging.getLogger(__name__)


class OmniRouteProvider(LLMProvider):
    """
    OmniRoute gateway provider.

    Exposes OpenAI-compatible `/v1/chat/completions` API with auto-discovery
    of available model routes.
    """

    def __init__(self, base_url: str = "http://localhost:7777/v1", api_key: str = "", model: str = "auto"):
        # Ensure base URL format (normalizes trailing slashes and /v1 suffix)
        clean_url = base_url.rstrip("/")
        if not clean_url.endswith("/v1") and not "/v1/" in clean_url:
            clean_url = f"{clean_url}/v1"

        self.base_url = clean_url
        self.api_key = api_key
        self.model = model or "auto"

    async def generate(self, messages: list[dict], **kwargs) -> str:
        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"

        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": kwargs.get("temperature", 0.7),
            "max_tokens": kwargs.get("max_tokens", 4096),
        }

        # Include additional extra params if passed
        for k, v in kwargs.items():
            if k not in ["temperature", "max_tokens"]:
                payload[k] = v

        url = f"{self.base_url}/chat/completions"

        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(url, headers=headers, json=payload, timeout=120.0)
                response.raise_for_status()
                data = response.json()

                if "choices" in data and len(data["choices"]) > 0:
                    choice = data["choices"][0]
                    if "message" in choice and "content" in choice["message"]:
                        return choice["message"]["content"]
                    elif "text" in choice:
                        return choice["text"]

                raise RuntimeError(f"Unexpected OmniRoute response structure: {data}")

            except httpx.HTTPStatusError as exc:
                logger.error(f"OmniRoute HTTP error {exc.response.status_code}: {exc.response.text}")
                raise RuntimeError(f"OmniRoute request failed [{exc.response.status_code}]: {exc.response.text}")
            except Exception as exc:
                logger.error(f"OmniRoute connection failed: {exc}")
                raise RuntimeError(f"Failed to connect to OmniRoute at {self.base_url}: {exc}")

    async def is_available(self) -> bool:
        """Check if OmniRoute service is up and responsive."""
        headers = {}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"

        try:
            async with httpx.AsyncClient() as client:
                # First try GET /models
                resp = await client.get(f"{self.base_url}/models", headers=headers, timeout=3.0)
                if resp.status_code in [200, 401]:
                    return True

                # Fallback check base url
                resp2 = await client.get(self.base_url, headers=headers, timeout=3.0)
                return resp2.status_code < 500
        except Exception:
            return False

    async def list_models(self) -> list[str]:
        """Fetch list of available models from OmniRoute router."""
        headers = {}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"

        try:
            async with httpx.AsyncClient() as client:
                resp = await client.get(f"{self.base_url}/models", headers=headers, timeout=5.0)
                if resp.status_code == 200:
                    data = resp.json()
                    if "data" in data:
                        return [m["id"] for m in data["data"] if "id" in m]
        except Exception:
            pass
        return [self.model]

    @property
    def name(self) -> str:
        return "OmniRoute AI Gateway"
