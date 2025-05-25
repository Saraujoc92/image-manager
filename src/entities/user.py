from typing import Optional
from uuid import UUID
from pydantic import BaseModel

class User(BaseModel):
    id: UUID
    team_id: UUID
    email: str
    name: str
    active: bool = True
    is_admin: bool = False
    created_at: str
    deleted_at: Optional[str] = None

    def __repr__(self):
        return f"<User(email='{self.email}', name='{self.name}')>"