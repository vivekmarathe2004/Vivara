"""
OmniRoute LLM Provider
----------------------
Integrates OmniRoute — an open-source, provider-agnostic OpenAI-compatible
router proxy that unifies local models (Ollama, vLLM, LM Studio) and cloud APIs
(OpenRouter, Groq, Anthropic, OpenAI, DeepSeek) under a single endpoint.
"""
from __future__ import annotations

import json
import logging
import httpx
from backend.services.llm.base import LLMProvider

logger = logging.getLogger(__name__)


class OmniRouteProvider(LLMProvider):
    """
    OmniRoute gateway provider.

    Exposes OpenAI-compatible `/v1/chat/completions` API with auto-discovery
    and streaming/non-streaming payload handling.
    """

    def __init__(self, base_url: str = "http://localhost:20128/v1", api_key: str = "", model: str = "auto"):
        clean_url = base_url.rstrip("/")
        if not clean_url.endswith("/v1") and "/v1/" not in clean_url:
            clean_url = f"{clean_url}/v1"

        self.base_url = clean_url
        self.api_key = api_key
        self.model = model or "auto"

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
                    if "data" in data and isinstance(data["data"], list):
                        return [m["id"] for m in data["data"] if isinstance(m, dict) and "id" in m]
        except Exception as exc:
            logger.debug(f"OmniRoute list_models warning: {exc}")
        return []

    async def _resolve_model(self) -> str:
        """Resolve generic model names to valid OmniRoute model routes."""
        available = await self.list_models()
        if not available:
            return self.model if self.model != "auto" else "auto/best-free"

        if self.model in available:
            return self.model

        # Priority model choices if user specified 'auto', 'llama3.2', or invalid name
        preferred_defaults = ["auto/best-free", "auto/fast", "auto/best-fast", "auto/chat", "auto/smart"]
        for p in preferred_defaults:
            if p in available:
                return p

        return available[0]

    async def generate(self, messages: list[dict], **kwargs) -> str:
        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"

        target_model = await self._resolve_model()

        payload = {
            "model": target_model,
            "messages": messages,
            "stream": False,  # Explicitly request non-streaming JSON
            "temperature": kwargs.get("temperature", 0.7),
            "max_tokens": kwargs.get("max_tokens", 4096),
        }

        for k, v in kwargs.items():
            if k not in ["temperature", "max_tokens", "stream"]:
                payload[k] = v

        url = f"{self.base_url}/chat/completions"

        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(url, headers=headers, json=payload, timeout=120.0)
                response.raise_for_status()
                text = response.text.strip()

                # Case 1: Standard JSON completion response
                if text.startswith("{") and text.endswith("}"):
                    data = json.loads(text)
                    if "choices" in data and len(data["choices"]) > 0:
                        choice = data["choices"][0]
                        if "message" in choice and "content" in choice["message"]:
                            return choice["message"]["content"]
                        elif "text" in choice:
                            return choice["text"]

                # Case 2: SSE Chunked Response (data: {...})
                content_chunks = []
                for line in text.splitlines():
                    line_str = line.strip()
                    if line_str.startswith("data:") and not line_str.endswith("[DONE]"):
                        chunk_json = line_str[5:].strip()
                        try:
                            cdata = json.loads(chunk_json)
                            if "choices" in cdata and len(cdata["choices"]) > 0:
                                delta = cdata["choices"][0].get("delta", {})
                                if "content" in delta and delta["content"]:
                                    content_chunks.append(delta["content"])
                                elif "text" in cdata["choices"][0]:
                                    content_chunks.append(cdata["choices"][0]["text"])
                        except Exception:
                            continue

                if content_chunks:
                    return "".join(content_chunks)

                raise RuntimeError(f"Unexpected OmniRoute response format: {text[:300]}")

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
                resp = await client.get(f"{self.base_url}/models", headers=headers, timeout=3.0)
                return resp.status_code in [200, 401]
        except Exception:
            return False

    @property
    def name(self) -> str:
        return "OmniRoute AI Gateway"
