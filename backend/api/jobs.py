from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from sse_starlette.sse import EventSourceResponse
from backend.database import get_db
from backend.models.job import PipelineStage
import asyncio
import json

router = APIRouter(prefix="/api/jobs", tags=["jobs"])

@router.get("/{project_id}/stream")
async def stream_jobs(project_id: str, request: Request, db: Session = Depends(get_db)):
    async def event_generator():
        while True:
            if await request.is_disconnected():
                break
            # Note: need a fresh db session or refresh instances as this is a long running stream
            stages = db.query(PipelineStage).filter(PipelineStage.project_id == project_id).all()
            for s in stages:
                db.refresh(s)
                data = {
                    "stage": s.stage,
                    "status": s.status,
                    "progress": s.progress,
                    "log": s.log,
                    "error": s.error_msg
                }
                yield {"data": json.dumps(data)}
            await asyncio.sleep(0.5)

    return EventSourceResponse(event_generator())

@router.get("/{project_id}/status")
def get_jobs_status(project_id: str, db: Session = Depends(get_db)):
    stages = db.query(PipelineStage).filter(PipelineStage.project_id == project_id).all()
    return stages
