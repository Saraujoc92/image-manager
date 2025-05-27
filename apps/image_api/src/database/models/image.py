from datetime import datetime
from sqlalchemy import Column, DateTime, String
from sqlalchemy.dialects.postgresql import UUID
import uuid

from database.client import Base


class Image(Base):
    __tablename__ = "image"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    cloud_path = Column(String(), nullable=False, unique=True)
    uploaded_by = Column(UUID(as_uuid=True), nullable=False)
    owner_team = Column(UUID(as_uuid=True), nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    deleted_at = Column(DateTime)

    def __repr__(self):
        return f"<Image(id={self.id}, path={self.cloud_path}, uploaded_by={self.uploaded_by})>"
