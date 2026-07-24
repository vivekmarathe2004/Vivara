from sqlalchemy import Column, String, Integer, Text, DateTime, ForeignKey
from backend.database import Base
import uuid
import datetime

class PipelineStage(Base):
    __tablename__ = "pipeline_stages"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    project_id = Column(String, ForeignKey("projects.id"))
    stage = Column(String, nullable=False)  # script, voice, subtitles, media, render
    status = Column(String, nullable=False, default="pending")  # pending, running, done, error, skipped
    progress = Column(Integer, default=0)
    result_path = Column(String, nullable=True)
    error_msg = Column(String, nullable=True)
    log = Column(Text, default="")
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
