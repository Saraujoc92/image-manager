from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel


class Image(BaseModel):
    id: UUID
    cloud_path: str
    uploaded_by: UUID
    owner_team: UUID
    created_at: datetime
    deleted_at: Optional[datetime] = None

    model_config = {"from_attributes": True}

    def __repr__(self):
        return f"<Image(id={self.id}, path={self.cloud_path}, uploaded_by={self.uploaded_by})>"
