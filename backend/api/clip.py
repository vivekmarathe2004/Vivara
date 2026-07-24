from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models.project import Project
from backend.services.clip_mode.clip_processor import ClipProcessor
from backend.services.subtitle.whisper_service import WhisperService
from backend.services.llm.factory import get_llm_provider
from backend.services.render.ffmpeg_renderer import FFmpegRenderer
from backend.config import settings
import pathlib

router = APIRouter(prefix="/api/clip", tags=["clip"])

def get_clip_processor():
    whisper = WhisperService(settings.whisper_model)
    llm = get_llm_provider(settings)
    ffmpeg = FFmpegRenderer(settings.ffmpeg_path, settings.gpu_enabled)
    return ClipProcessor(whisper, llm, ffmpeg)

class ClipCreateReq(BaseModel):
    video_path: str = ""
    title: str = "Repurposed Short"

class TranscribeReq(BaseModel):
    video_path: str

class FindMomentsReq(BaseModel):
    transcript: dict
    count: int = 5

class CutClipsReq(BaseModel):
    video_path: str
    moments: list

class AddCaptionsReq(BaseModel):
    clip_path: str
    transcript_segment: dict = {}
    style: str = "default"

class ExportShortsReq(BaseModel):
    clips: list
    aspect_ratio: str = "9:16"
    add_zoom: bool = True

@router.post("/create")
def create_clip(req: ClipCreateReq, db: Session = Depends(get_db)):
    project = Project(
        title=req.title or "Clip Project",
        video_type="shorts",
        topic=req.video_path or "repurpose"
    )
    db.add(project)
    db.commit()
    db.refresh(project)
    return project

@router.post("/{id}/transcribe")
async def transcribe_clip(id: str, req: TranscribeReq):
    if not req.video_path or not pathlib.Path(req.video_path).exists():
        raise HTTPException(status_code=400, detail=f"Source video file not found at '{req.video_path}'.")
    processor = get_clip_processor()
    transcript = await processor.transcribe(req.video_path)
    return transcript

@router.post("/{id}/find-moments")
async def find_moments(id: str, req: FindMomentsReq):
    processor = get_clip_processor()
    moments = await processor.find_viral_moments(req.transcript, count=req.count)
    return moments

@router.post("/{id}/cut")
async def cut_clips(id: str, req: CutClipsReq):
    processor = get_clip_processor()
    out_dir = pathlib.Path(settings.storage_dir) / "output" / id
    out_dir.mkdir(parents=True, exist_ok=True)
    clips = await processor.cut_clips(req.video_path, req.moments, str(out_dir))
    return clips

@router.post("/{id}/add-captions")
async def add_captions(id: str, req: AddCaptionsReq):
    processor = get_clip_processor()
    out_path = await processor.add_captions(req.clip_path, req.transcript_segment, req.style)
    return {"path": out_path}

@router.post("/{id}/export")
async def export_shorts(id: str, req: ExportShortsReq):
    processor = get_clip_processor()
    out_dir = pathlib.Path(settings.storage_dir) / "output" / id
    out_dir.mkdir(parents=True, exist_ok=True)
    final_clips = await processor.export_shorts(
        req.clips, 
        str(out_dir), 
        aspect_ratio=req.aspect_ratio, 
        add_zoom=req.add_zoom
    )
    return final_clips

@router.get("/{id}/moments")
def get_moments(id: str):
    return []

@router.put("/{id}/moments/{moment_id}")
def update_moment(id: str, moment_id: str, updates: dict):
    return {"status": "updated"}
