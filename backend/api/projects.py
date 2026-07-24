from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from backend.database import get_db
from backend.models.project import Project
from backend.models.job import PipelineStage
from backend.schemas.project import ProjectCreate, ProjectUpdate, ProjectResponse
import json
import os
from fastapi.responses import FileResponse

router = APIRouter(prefix="/api/projects", tags=["projects"])

@router.get("/", response_model=List[ProjectResponse])
def list_projects(db: Session = Depends(get_db)):
    projects = db.query(Project).order_by(Project.created_at.desc()).all()
    result = []
    for p in projects:
        stages = db.query(PipelineStage).filter(PipelineStage.project_id == p.id).all()
        p_dict = {
            "id": p.id,
            "title": p.title,
            "video_type": p.video_type,
            "status": p.status,
            "topic": p.topic,
            "script": p.script,
            "settings_json": p.settings_json,
            "thumbnail_path": p.thumbnail_path,
            "output_path": p.output_path,
            "created_at": p.created_at,
            "updated_at": p.updated_at,
            "stages": stages
        }
        result.append(p_dict)
    return result

@router.post("/", response_model=ProjectResponse)
def create_project(project: ProjectCreate, db: Session = Depends(get_db)):
    new_project = Project(
        title=project.title,
        video_type=project.video_type,
        topic=project.topic,
        settings_json=json.dumps(project.settings)
    )
    db.add(new_project)
    db.commit()
    db.refresh(new_project)
    
    stages = ["script", "voice", "subtitles", "media", "render"]
    for stage_name in stages:
        stage = PipelineStage(project_id=new_project.id, stage=stage_name)
        db.add(stage)
    db.commit()
    
    stages_db = db.query(PipelineStage).filter(PipelineStage.project_id == new_project.id).all()
    p_dict = {
        "id": new_project.id,
        "title": new_project.title,
        "video_type": new_project.video_type,
        "status": new_project.status,
        "topic": new_project.topic,
        "script": new_project.script,
        "settings_json": new_project.settings_json,
        "thumbnail_path": new_project.thumbnail_path,
        "output_path": new_project.output_path,
        "created_at": new_project.created_at,
        "updated_at": new_project.updated_at,
        "stages": stages_db
    }
    return p_dict

@router.get("/{id}", response_model=ProjectResponse)
def get_project(id: str, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == id).first()
    if not project:
        raise HTTPException(status_code=404, detail=f"Project with ID '{id}' was not found in the database.")
    stages = db.query(PipelineStage).filter(PipelineStage.project_id == id).all()
    p_dict = {
        "id": project.id,
        "title": project.title,
        "video_type": project.video_type,
        "status": project.status,
        "topic": project.topic,
        "script": project.script,
        "settings_json": project.settings_json,
        "thumbnail_path": project.thumbnail_path,
        "output_path": project.output_path,
        "created_at": project.created_at,
        "updated_at": project.updated_at,
        "stages": stages
    }
    return p_dict

@router.put("/{id}", response_model=ProjectResponse)
def update_project(id: str, project_update: ProjectUpdate, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == id).first()
    if not project:
        raise HTTPException(status_code=404, detail=f"Cannot update: Project with ID '{id}' was not found.")
    
    if project_update.title is not None:
        project.title = project_update.title
    if project_update.script is not None:
        project.script = project_update.script
    if project_update.settings is not None:
        project.settings_json = json.dumps(project_update.settings)
        
    db.commit()
    db.refresh(project)
    
    stages = db.query(PipelineStage).filter(PipelineStage.project_id == id).all()
    p_dict = {
        "id": project.id,
        "title": project.title,
        "video_type": project.video_type,
        "status": project.status,
        "topic": project.topic,
        "script": project.script,
        "settings_json": project.settings_json,
        "thumbnail_path": project.thumbnail_path,
        "output_path": project.output_path,
        "created_at": project.created_at,
        "updated_at": project.updated_at,
        "stages": stages
    }
    return p_dict

@router.delete("/{id}")
def delete_project(id: str, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == id).first()
    if not project:
        raise HTTPException(status_code=404, detail=f"Cannot delete: Project with ID '{id}' was not found.")
    
    if project.output_path and os.path.exists(project.output_path):
        try:
            os.remove(project.output_path)
        except Exception as exc:
            pass
            
    db.query(PipelineStage).filter(PipelineStage.project_id == id).delete()
    db.delete(project)
    db.commit()
    return {"message": f"Project '{project.title}' deleted successfully"}

@router.get("/{id}/download")
def download_project(id: str, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == id).first()
    if not project:
        raise HTTPException(status_code=404, detail=f"Project with ID '{id}' was not found.")
    if not project.output_path or not os.path.exists(project.output_path):
        raise HTTPException(
            status_code=404, 
            detail=f"Rendered MP4 file for '{project.title}' does not exist on disk. Please run the render stage first."
        )
    return FileResponse(project.output_path)
