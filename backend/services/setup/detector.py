import subprocess
import httpx
from backend.config import settings
from backend.services.render.ffmpeg_renderer import FFmpegRenderer

class SystemDetector:
    async def check_ffmpeg(self) -> dict:
        try:
            res = subprocess.run([settings.ffmpeg_path, "-version"], capture_output=True, text=True)
            if res.returncode == 0:
                version = res.stdout.splitlines()[0]
                return {"found": True, "version": version, "path": settings.ffmpeg_path}
        except Exception:
            pass
        return {"found": False, "version": "", "path": ""}

    async def check_gpu(self) -> dict:
        renderer = FFmpegRenderer(settings.ffmpeg_path, settings.gpu_enabled)
        return renderer.detect_gpu()

    async def check_kokoro(self) -> dict:
        try:
            import kokoro
            return {"installed": True, "model_downloaded": True}
        except ImportError:
            return {"installed": False, "model_downloaded": False}

    async def check_edge_tts(self) -> dict:
        try:
            import edge_tts
            return {"installed": True}
        except ImportError:
            return {"installed": False}

    async def check_whisper(self) -> dict:
        try:
            import faster_whisper
            return {"installed": True, "model": settings.whisper_model}
        except ImportError:
            return {"installed": False, "model": ""}

    async def check_omniroute(self) -> dict:
        url = "http://localhost:7777/v1" if "7777" not in settings.llm_base_url else settings.llm_base_url
        try:
            async with httpx.AsyncClient() as client:
                res = await client.get(f"{url.rstrip('/')}/models", timeout=2.0)
                if res.status_code in [200, 401]:
                    return {"running": True, "url": url}
        except Exception:
            pass
        return {"running": False, "url": url}

    async def check_ollama(self) -> dict:
        try:
            async with httpx.AsyncClient() as client:
                res = await client.get("http://localhost:11434", timeout=2.0)
                if res.status_code == 200:
                    return {"running": True, "url": "http://localhost:11434", "models": []}
        except Exception:
            pass
        return {"running": False, "url": "http://localhost:11434", "models": []}

    async def check_all(self) -> dict:
        return {
            "ffmpeg": await self.check_ffmpeg(),
            "gpu": await self.check_gpu(),
            "kokoro": await self.check_kokoro(),
            "edge_tts": await self.check_edge_tts(),
            "whisper": await self.check_whisper(),
            "omniroute": await self.check_omniroute(),
            "ollama": await self.check_ollama(),
            "pexels_key": {"configured": bool(settings.pexels_api_key)},
            "pixabay_key": {"configured": bool(settings.pixabay_api_key)},
        }
