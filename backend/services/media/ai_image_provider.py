"""
AI Scene Image Provider
-----------------------
Generates custom AI images for video scenes using Pollinations.ai (Flux / SD model).
100% FREE — NO API KEY REQUIRED!
"""
from __future__ import annotations

import logging
import random
import urllib.parse
import httpx
from backend.services.media.base import MediaProvider
from backend.services.media.downloader import AsyncDownloader

logger = logging.getLogger(__name__)


class AIImageProvider(MediaProvider):
    def __init__(self, model: str = "flux"):
        self.model = model
        self.downloader = AsyncDownloader()

    def is_configured(self) -> bool:
        return True  # 100% free, always configured!

    async def search_videos(self, query: str, per_page: int = 10) -> list[dict]:
        return []

    async def search_images(self, query: str, per_page: int = 10) -> list[dict]:
        encoded_prompt = urllib.parse.quote(query)
        seed = random.randint(1, 999999)
        url = f"https://pollinations.ai/p/{encoded_prompt}?width=1920&height=1080&seed={seed}&model={self.model}&nologo=true"

        return [{
            "id": f"pollinations_{seed}",
            "title": query,
            "thumbnail": url,
            "preview_url": url,
            "download_url": url,
            "source": "pollinations_ai",
            "type": "image",
            "width": 1920,
            "height": 1080,
            "author": "Pollinations AI (Flux)",
        }]

    async def download(self, url: str, output_path: str) -> str:
        return await self.downloader.download_file(url, output_path)
