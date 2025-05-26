from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel


class ApiKey(BaseModel):
    id: UUID
    key: str
    user_id: UUID
    active: bool = True
    created_at: datetime
    deleted_at: Optional[datetime] = None

    def __repr__(self):
        return f"<ApiKey(id={self.id}, key={self.key}, user_id={self.user_id})>"
