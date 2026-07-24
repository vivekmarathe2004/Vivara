from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models.job import PipelineStage
from backend.models.project import Project
from backend.schemas.stage import GenerateRequest
from backend.services.pipeline.stage_runner import PipelineStageRunner

router = APIRouter(prefix="/api/generate", tags=["generate"])

@router.post("/{project_id}/stage/{stage_name}")
async def run_stage(project_id: str, stage_name: str, background_tasks: BackgroundTasks, req: GenerateRequest = None, db: Session = Depends(get_db)):
    stage = db.query(PipelineStage).filter(PipelineStage.project_id == project_id, PipelineStage.stage == stage_name).first()
    if not stage:
        raise HTTPException(
            status_code=404, 
            detail=f"Pipeline stage '{stage_name}' for project ID '{project_id}' was not found."
        )
    
    runner = PipelineStageRunner()
    background_tasks.add_task(runner.run_stage, project_id, stage_name)
    
    return {"job_id": stage.id, "status": "running"}

@router.post("/{project_id}/run-all")
async def run_all(project_id: str, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(
            status_code=404, 
            detail=f"Cannot execute pipeline: Project with ID '{project_id}' was not found."
        )
        
    runner = PipelineStageRunner()
    background_tasks.add_task(runner.run_all, project_id)
    return {"status": "started"}

@router.post("/{project_id}/skip/{stage_name}")
def skip_stage(project_id: str, stage_name: str, db: Session = Depends(get_db)):
    stage = db.query(PipelineStage).filter(PipelineStage.project_id == project_id, PipelineStage.stage == stage_name).first()
    if not stage:
        raise HTTPException(
            status_code=404, 
            detail=f"Cannot skip: Stage '{stage_name}' for project ID '{project_id}' was not found."
        )
    stage.status = "skipped"
    db.commit()
    db.refresh(stage)
    return stage
