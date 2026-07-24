from sqlalchemy import Column, String, Text, DateTime
from backend.database import Base
import uuid
import datetime

class Project(Base):
    __tablename__ = "projects"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String, nullable=False)
    video_type = Column(String, nullable=False)  # ranking, review, explainer, shorts, documentary, educational, clip
    status = Column(String, nullable=False, default="draft")  # draft, generating, done, error
    topic = Column(String, nullable=False)
    script = Column(Text, nullable=True)
    settings_json = Column(Text, nullable=False, default="{}")
    thumbnail_path = Column(String, nullable=True)
    output_path = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
