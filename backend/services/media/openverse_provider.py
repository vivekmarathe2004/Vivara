"""
Openverse / Wikimedia Open Media Provider
-----------------------------------------
Searches millions of public domain and CC-licensed stock media.
100% FREE — NO API KEY REQUIRED!
"""
from __future__ import annotations

import logging
import httpx
from backend.services.media.base import MediaProvider
from backend.services.media.downloader import AsyncDownloader

logger = logging.getLogger(__name__)


class OpenverseProvider(MediaProvider):
    def __init__(self):
        self.downloader = AsyncDownloader()

    def is_configured(self) -> bool:
        return True  # Always configured! No key needed.

    async def search_videos(self, query: str, per_page: int = 10) -> list[dict]:
        return []

    async def search_images(self, query: str, per_page: int = 10) -> list[dict]:
        url = "https://api.openverse.org/v1/images/"
        params = {
            "q": query,
            "page_size": per_page,
            "license_type": "commercial,modification",
        }

        try:
            async with httpx.AsyncClient() as client:
                res = await client.get(url, params=params, timeout=10.0)
                res.raise_for_status()
                data = res.json()

                results = []
                for item in data.get("results", []):
                    results.append({
                        "id": str(item.get("id")),
                        "title": item.get("title") or query,
                        "thumbnail": item.get("thumbnail") or item.get("url"),
                        "preview_url": item.get("url"),
                        "download_url": item.get("url"),
                        "source": "openverse",
                        "type": "image",
                        "width": item.get("width", 1920),
                        "height": item.get("height", 1080),
                        "author": item.get("creator") or "Open License",
                    })
                return results
        except Exception as exc:
            logger.error(f"Openverse open media search failed: {exc}")
            return []

    async def download(self, url: str, output_path: str) -> str:
        return await self.downloader.download_file(url, output_path)
