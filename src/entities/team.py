from uuid import UUID
from pydantic import BaseModel
from typing import Union


class Team(BaseModel):
    id: UUID
    name: str
    active: bool = True
    created_at: str
    deleted_at: Union[str, None] = None

    def __repr__(self):
        return f"<Team(name='{self.name}', id='{self.id}')>"
