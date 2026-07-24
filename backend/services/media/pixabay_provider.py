import httpx
from backend.services.media.base import MediaProvider
from backend.services.media.downloader import download_file

class PixabayProvider(MediaProvider):
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://pixabay.com/api"

    def is_configured(self) -> bool:
        return bool(self.api_key)

    async def search_videos(self, query: str, per_page: int = 10) -> list[dict]:
        if not self.is_configured():
            return []
            
        async with httpx.AsyncClient() as client:
            resp = await client.get(f"{self.base_url}/videos/", params={"key": self.api_key, "q": query, "per_page": per_page})
            if resp.status_code != 200:
                return []
            data = resp.json()
            results = []
            for hit in data.get("hits", []):
                videos = hit.get("videos", {})
                large = videos.get("large", {})
                if large and large.get("url"):
                    results.append({
                        "id": str(hit["id"]),
                        "thumbnail": f"https://i.vimeocdn.com/video/{hit['picture_id']}_295x166.jpg",
                        "preview_url": large["url"],
                        "download_url": large["url"],
                        "source": "pixabay",
                        "duration": hit.get("duration", 0),
                        "width": large.get("width"),
                        "height": large.get("height")
                    })
            return results

    async def search_images(self, query: str, per_page: int = 10) -> list[dict]:
        return []

    async def download(self, url: str, output_path: str) -> str:
        await download_file(url, output_path)
        return output_path
