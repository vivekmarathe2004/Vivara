from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models.project import Project
from backend.services.clip_mode.clip_processor import ClipProcessor
from backend.services.subtitle.whisper_service import WhisperService
from backend.services.llm.factory import get_llm_provider
from backend.services.render.ffmpeg_renderer import FFmpegRenderer
from backend.config import settings
import uuid
import pathlib

router = APIRouter(prefix="/api/clip", tags=["clip"])

def get_clip_processor():
    whisper = WhisperService(settings.whisper_model)
    llm = get_llm_provider(settings)
    ffmpeg = FFmpegRenderer(settings.ffmpeg_path, settings.gpu_enabled)
    return ClipProcessor(whisper, llm, ffmpeg)

@router.post("/create")
def create_clip(video_path: str, db: Session = Depends(get_db)):
    project = Project(title="Clip Project", video_type="clip", topic="clip")
    db.add(project)
    db.commit()
    db.refresh(project)
    return project

@router.post("/{id}/transcribe")
async def transcribe_clip(id: str, video_path: str):
    processor = get_clip_processor()
    transcript = await processor.transcribe(video_path)
    return transcript

@router.post("/{id}/find-moments")
async def find_moments(id: str, transcript: dict):
    processor = get_clip_processor()
    moments = await processor.find_viral_moments(transcript)
    return moments

@router.post("/{id}/cut")
async def cut_clips(id: str, video_path: str, moments: list):
    processor = get_clip_processor()
    out_dir = pathlib.Path(settings.storage_dir) / "output" / id
    out_dir.mkdir(parents=True, exist_ok=True)
    clips = await processor.cut_clips(video_path, moments, str(out_dir))
    return clips

@router.post("/{id}/add-captions")
async def add_captions(id: str, clip_path: str, transcript_segment: dict, style: str = "default"):
    processor = get_clip_processor()
    out_path = await processor.add_captions(clip_path, transcript_segment, style)
    return {"path": out_path}

@router.post("/{id}/export")
async def export_shorts(id: str, clips: list):
    processor = get_clip_processor()
    out_dir = pathlib.Path(settings.storage_dir) / "output" / id
    final_clips = await processor.export_shorts(clips, str(out_dir))
    return final_clips

@router.get("/{id}/moments")
def get_moments(id: str):
    return []

@router.put("/{id}/moments/{moment_id}")
def update_moment(id: str, moment_id: str, updates: dict):
    return {"status": "updated"}
