from fastapi import APIRouter
from backend.services.media.pexels_provider import PexelsProvider
from backend.services.media.pixabay_provider import PixabayProvider
from backend.services.media.downloader import download_file
from backend.config import settings
import pathlib

router = APIRouter(prefix="/api/media", tags=["media"])

@router.get("/search")
async def search_media(q: str, source: str = "pexels", per_page: int = 10):
    if source == "pexels":
        provider = PexelsProvider(settings.pexels_api_key)
        return await provider.search_videos(q, per_page)
    elif source == "pixabay":
        provider = PixabayProvider(settings.pixabay_api_key)
        return await provider.search_videos(q, per_page)
    return []

@router.get("/download")
async def download_media(url: str, type: str):
    storage_path = pathlib.Path(settings.storage_dir) / 'media'
    storage_path.mkdir(parents=True, exist_ok=True)
    import hashlib
    file_id = hashlib.md5(url.encode()).hexdigest()
    ext = ".mp4" if type == "video" else ".jpg"
    out_path = storage_path / f"{file_id}{ext}"
    await download_file(url, str(out_path))
    return {"path": str(out_path)}
