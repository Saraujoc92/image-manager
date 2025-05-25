from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel


class Team(BaseModel):
    id: UUID
    name: str
    active: bool = True
    created_at: datetime
    deleted_at: Optional[datetime] = None

    def __repr__(self):
        return f"<Team(name='{self.name}', id='{self.id}')>"
