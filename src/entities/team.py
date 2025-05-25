from typing import Optional
from uuid import UUID
from pydantic import BaseModel


class Team(BaseModel):
    id: UUID
    name: str
    active: bool = True
    created_at: str
    deleted_at: Optional[str] = None

    def __repr__(self):
        return f"<Team(name='{self.name}', id='{self.id}')>"
