from fastapi import APIRouter, BackgroundTasks
from backend.services.setup.detector import SystemDetector
import pathlib
import os
from backend.config import settings

router = APIRouter(prefix="/api/setup", tags=["setup"])

@router.get("/check")
async def run_check():
    detector = SystemDetector()
    results = await detector.check_all()
    storage_path = pathlib.Path(settings.storage_dir)
    results["first_run"] = not (storage_path / ".setup_complete").exists()
    return results

@router.post("/complete")
def complete_setup():
    storage_path = pathlib.Path(settings.storage_dir)
    storage_path.mkdir(parents=True, exist_ok=True)
    (storage_path / ".setup_complete").touch()
    return {"status": "ok"}

@router.post("/install/kokoro")
def install_kokoro(background_tasks: BackgroundTasks):
    # Dummy mock for kokoro install
    return {"status": "started"}

@router.post("/install/whisper")
def install_whisper(background_tasks: BackgroundTasks):
    return {"status": "started"}

from sse_starlette.sse import EventSourceResponse
import asyncio

@router.get("/install/progress")
async def install_progress():
    async def event_generator():
        yield {"data": "Installation not running or finished"}
        await asyncio.sleep(1)
    return EventSourceResponse(event_generator())
