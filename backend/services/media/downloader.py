import httpx
import aiofiles

async def download_file(url: str, output_path: str):
    async with httpx.AsyncClient(follow_redirects=True) as client:
        async with client.stream("GET", url) as response:
            response.raise_for_status()
            async with aiofiles.open(output_path, "wb") as f:
                async for chunk in response.aiter_bytes():
                    await f.write(chunk)
