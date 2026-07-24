import httpx
from backend.services.llm.base import LLMProvider

class OpenAICompatProvider(LLMProvider):
    def __init__(self, base_url: str, api_key: str, model: str):
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self.model = model

    async def generate(self, messages: list[dict], **kwargs) -> str:
        headers = {}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
            
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json={
                    "model": self.model,
                    "messages": messages,
                    **kwargs
                },
                timeout=120.0
            )
            response.raise_for_status()
            data = response.json()
            return data["choices"][0]["message"]["content"]

    async def is_available(self) -> bool:
        try:
            # simple check if domain is reachable
            async with httpx.AsyncClient() as client:
                response = await client.get(self.base_url, timeout=5.0)
                # It might return 401 or 404, but at least it's reachable
                return True
        except Exception:
            return False

    @property
    def name(self) -> str:
        return "OpenAI Compatible"
