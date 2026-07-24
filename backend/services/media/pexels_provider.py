import httpx
from backend.services.media.base import MediaProvider
from backend.services.media.downloader import download_file

class PexelsProvider(MediaProvider):
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.pexels.com"
        self.headers = {"Authorization": self.api_key}

    def is_configured(self) -> bool:
        return bool(self.api_key)

    async def search_videos(self, query: str, per_page: int = 10) -> list[dict]:
        if not self.is_configured():
            return []
            
        async with httpx.AsyncClient() as client:
            resp = await client.get(f"{self.base_url}/videos/search", params={"query": query, "per_page": per_page}, headers=self.headers)
            if resp.status_code != 200:
                return []
            data = resp.json()
            results = []
            for video in data.get("videos", []):
                files = video.get("video_files", [])
                hd_files = [f for f in files if f.get("quality") == "hd"]
                if hd_files:
                    best_file = hd_files[0]
                    results.append({
                        "id": str(video["id"]),
                        "thumbnail": video["image"],
                        "preview_url": best_file["link"],
                        "download_url": best_file["link"],
                        "source": "pexels",
                        "duration": video.get("duration", 0),
                        "width": best_file["width"],
                        "height": best_file["height"]
                    })
            return results

    async def search_images(self, query: str, per_page: int = 10) -> list[dict]:
        return []

    async def download(self, url: str, output_path: str) -> str:
        await download_file(url, output_path)
        return output_path
