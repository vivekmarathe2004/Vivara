"""
OpenAI Speech (TTS) Provider
----------------------------
Synthesizes speech using OpenAI's Audio API or OpenAI-compatible endpoint.
Voices: alloy, echo, fable, onyx, nova, shimmer.
"""
from __future__ import annotations

import logging
import httpx
from backend.services.tts.base import TTSProvider

logger = logging.getLogger(__name__)


class OpenAITTSProvider(TTSProvider):
    def __init__(self, api_key: str = "", base_url: str = "https://api.openai.com/v1", voice: str = "alloy", model: str = "tts-1"):
        self.api_key = api_key
        self.base_url = base_url.rstrip("/") if base_url else "https://api.openai.com/v1"
        self.voice = voice or "alloy"
        self.model = model or "tts-1"

    async def synthesize(self, text: str, output_path: str, voice: str = "") -> dict:
        url = f"{self.base_url}/audio/speech"
        target_voice = voice or self.voice or "alloy"

        headers = {
            "Content-Type": "application/json",
        }
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"

        payload = {
            "model": self.model,
            "input": text,
            "voice": target_voice,
            "response_format": "mp3"
        }

        async with httpx.AsyncClient() as client:
            try:
                res = await client.post(url, headers=headers, json=payload, timeout=60.0)
                res.raise_for_status()

                with open(output_path, "wb") as f:
                    f.write(res.content)

                return {
                    "audio_path": output_path,
                    "duration": len(text) * 0.06,
                    "word_timings": []
                }
            except httpx.HTTPStatusError as exc:
                logger.error(f"OpenAI TTS HTTP Error [{exc.response.status_code}]: {exc.response.text}")
                raise RuntimeError(f"OpenAI TTS Error [{exc.response.status_code}]: {exc.response.text}")
            except Exception as exc:
                logger.error(f"OpenAI TTS failed: {exc}")
                raise RuntimeError(f"OpenAI Speech synthesis failed: {exc}")

    async def list_voices(self) -> list[dict]:
        return [
            {"id": "alloy", "name": "Alloy (Neutral, Versatile)"},
            {"id": "echo", "name": "Echo (Male, Warm)"},
            {"id": "fable", "name": "Fable (British, Expressive)"},
            {"id": "onyx", "name": "Onyx (Male, Deep)"},
            {"id": "nova", "name": "Nova (Female, Energetic)"},
            {"id": "shimmer", "name": "Shimmer (Female, Clear)"},
        ]

    async def is_available(self) -> bool:
        return bool(self.api_key or "localhost" in self.base_url)
