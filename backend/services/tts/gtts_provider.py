"""
Google Translate TTS (gTTS) Provider
-------------------------------------
Synthesizes audio using Google's free TTS web endpoint.
100% FREE — NO API KEY REQUIRED! Supports 100+ languages.
"""
from __future__ import annotations

import logging
import urllib.parse
import httpx
from backend.services.tts.base import TTSProvider

logger = logging.getLogger(__name__)


class GTTSProvider(TTSProvider):
    def __init__(self, lang: str = "en"):
        self.lang = lang or "en"

    async def synthesize(self, text: str, output_path: str, voice: str = "") -> dict:
        target_lang = voice or self.lang or "en"
        encoded_text = urllib.parse.quote(text)
        url = f"https://translate.google.com/translate_tts?ie=UTF-8&q={encoded_text}&tl={target_lang}&client=tw-ob"

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }

        async with httpx.AsyncClient() as client:
            try:
                res = await client.get(url, headers=headers, timeout=30.0)
                res.raise_for_status()

                with open(output_path, "wb") as f:
                    f.write(res.content)

                return {
                    "audio_path": output_path,
                    "duration": len(text) * 0.06,
                    "word_timings": []
                }
            except Exception as exc:
                logger.error(f"gTTS synthesis failed: {exc}")
                raise RuntimeError(f"Google Translate TTS synthesis failed: {exc}")

    async def list_voices(self) -> list[dict]:
        return [
            {"id": "en", "name": "English (Google Voice)"},
            {"id": "es", "name": "Spanish (Google Voice)"},
            {"id": "fr", "name": "French (Google Voice)"},
            {"id": "de", "name": "German (Google Voice)"},
            {"id": "hi", "name": "Hindi (Google Voice)"},
            {"id": "ja", "name": "Japanese (Google Voice)"},
            {"id": "pt", "name": "Portuguese (Google Voice)"},
            {"id": "ru", "name": "Russian (Google Voice)"},
            {"id": "zh-CN", "name": "Chinese Mandarin (Google Voice)"},
        ]

    async def is_available(self) -> bool:
        return True
