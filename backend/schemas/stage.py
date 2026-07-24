from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime

class StageResponse(BaseModel):
    id: str
    project_id: str
    stage: str
    status: str
    progress: int
    result_path: Optional[str] = None
    error_msg: Optional[str] = None
    log: str
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class GenerateRequest(BaseModel):
    stages: Optional[List[str]] = None
    settings_overrides: Optional[Dict[str, Any]] = None
