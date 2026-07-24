"""
ElevenLabs TTS Provider
-----------------------
Synthesizes speech using ElevenLabs API (Free tier: 10,000 characters/month).
"""
from __future__ import annotations

import logging
import httpx
from backend.services.tts.base import TTSProvider

logger = logging.getLogger(__name__)


class ElevenLabsTTSProvider(TTSProvider):
    def __init__(self, api_key: str = "", voice_id: str = "21m00Tcm4TlvDq8ikWAM"):
        self.api_key = api_key
        self.voice_id = voice_id or "21m00Tcm4TlvDq8ikWAM"  # Default: Rachel

    async def synthesize(self, text: str, output_path: str, voice: str = "") -> dict:
        if not self.api_key:
            raise RuntimeError("ElevenLabs API Key is missing. Please configure your free ElevenLabs API Key in Settings.")

        target_voice = voice or self.voice_id
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{target_voice}"
        headers = {
            "xi-api-key": self.api_key,
            "Content-Type": "application/json",
            "Accept": "audio/mpeg"
        }
        payload = {
            "text": text,
            "model_id": "eleven_monolingual_v1",
            "voice_settings": {
                "stability": 0.5,
                "similarity_boost": 0.75
            }
        }

        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(url, headers=headers, json=payload, timeout=60.0)
                response.raise_for_status()

                with open(output_path, "wb") as f:
                    f.write(response.content)

                return {
                    "audio_path": output_path,
                    "duration": len(text) * 0.06,  # Estimated duration
                    "word_timings": []
                }
            except httpx.HTTPStatusError as exc:
                logger.error(f"ElevenLabs TTS error [{exc.response.status_code}]: {exc.response.text}")
                raise RuntimeError(f"ElevenLabs API Error [{exc.response.status_code}]: {exc.response.text}")
            except Exception as exc:
                logger.error(f"ElevenLabs TTS failed: {exc}")
                raise RuntimeError(f"ElevenLabs synthesis failed: {exc}")

    async def list_voices(self) -> list[dict]:
        if not self.api_key:
            return [
                {"id": "21m00Tcm4TlvDq8ikWAM", "name": "Rachel (Female)"},
                {"id": "AZnzlk1XvdvUeBnXmlld", "name": "Domi (Female)"},
                {"id": "EXAVITQu4vr4xnSDxMaL", "name": "Bella (Female)"},
                {"id": "ErXwobaYiN019PkySvjV", "name": "Antoni (Male)"},
                {"id": "MF3mGyEYCl7XYWbV9V6O", "name": "Elli (Female)"},
                {"id": "TxGEqnHWrfWFTfGW9XjX", "name": "Josh (Male)"},
            ]

        url = "https://api.elevenlabs.io/v1/voices"
        headers = {"xi-api-key": self.api_key}
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.get(url, headers=headers, timeout=5.0)
                if resp.status_code == 200:
                    data = resp.json()
                    if "voices" in data:
                        return [{"id": v["voice_id"], "name": f"{v['name']} ({v.get('category','Voice')})"} for v in data["voices"]]
        except Exception:
            pass

        return [{"id": "21m00Tcm4TlvDq8ikWAM", "name": "Rachel (Female)"}]

    async def is_available(self) -> bool:
        return bool(self.api_key)
