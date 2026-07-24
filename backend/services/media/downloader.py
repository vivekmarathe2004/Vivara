import httpx
from pathlib import Path


async def download_file(url: str, output_path: str) -> str:
    """Download a remote URL to output_path using async streaming."""
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    async with httpx.AsyncClient(follow_redirects=True, timeout=60.0) as client:
        async with client.stream("GET", url) as response:
            response.raise_for_status()
            with open(output_path, "wb") as f:
                async for chunk in response.aiter_bytes(chunk_size=65536):
                    f.write(chunk)
    return output_path


class AsyncDownloader:
    """Class wrapper for async file downloader."""

    async def download_file(self, url: str, output_path: str) -> str:
        return await download_file(url, output_path)
