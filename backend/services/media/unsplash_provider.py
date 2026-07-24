"""
Unsplash Media Provider
-----------------------
Fetches free high-resolution stock photography via Unsplash API (Free Tier: 50 req/hr).
"""
from __future__ import annotations

import logging
import httpx
from backend.services.media.base import MediaProvider
from backend.services.media.downloader import AsyncDownloader

logger = logging.getLogger(__name__)


class UnsplashProvider(MediaProvider):
    def __init__(self, api_key: str = ""):
        self.api_key = api_key
        self.downloader = AsyncDownloader()

    def is_configured(self) -> bool:
        return bool(self.api_key)

    async def search_videos(self, query: str, per_page: int = 10) -> list[dict]:
        # Unsplash is photo-only; return empty for video query
        return []

    async def search_images(self, query: str, per_page: int = 10) -> list[dict]:
        if not self.api_key:
            return []

        url = "https://api.unsplash.com/search/photos"
        headers = {"Authorization": f"Client-ID {self.api_key}"}
        params = {"query": query, "per_page": per_page, "orientation": "landscape"}

        try:
            async with httpx.AsyncClient() as client:
                res = await client.get(url, headers=headers, params=params, timeout=10.0)
                res.raise_for_status()
                data = res.json()

                results = []
                for item in data.get("results", []):
                    results.append({
                        "id": str(item["id"]),
                        "title": item.get("alt_description") or query,
                        "thumbnail": item["urls"]["small"],
                        "preview_url": item["urls"]["regular"],
                        "download_url": item["urls"]["full"],
                        "source": "unsplash",
                        "type": "image",
                        "width": item.get("width", 1920),
                        "height": item.get("height", 1080),
                        "author": item.get("user", {}).get("name", "Unsplash Creator"),
                    })
                return results
        except Exception as exc:
            logger.error(f"Unsplash photo search failed: {exc}")
            return []

    async def download(self, url: str, output_path: str) -> str:
        return await self.downloader.download_file(url, output_path)
