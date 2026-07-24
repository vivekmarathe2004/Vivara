from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import datetime
from backend.schemas.stage import StageResponse

class ProjectCreate(BaseModel):
    title: str
    video_type: str
    topic: str
    settings: Dict[str, Any] = Field(default_factory=dict)

class ProjectUpdate(BaseModel):
    title: Optional[str] = None
    script: Optional[str] = None
    settings: Optional[Dict[str, Any]] = None

class ProjectResponse(BaseModel):
    id: str
    title: str
    video_type: str
    status: str
    topic: str
    script: Optional[str] = None
    settings_json: str
    thumbnail_path: Optional[str] = None
    output_path: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    stages: Optional[List[StageResponse]] = None

    class Config:
        from_attributes = True
