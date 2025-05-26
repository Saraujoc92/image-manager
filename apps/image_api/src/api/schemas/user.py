from pydantic import BaseModel
from uuid import UUID
from datetime import datetime


class CreateUserRequest(BaseModel):
    email: str
    name: str


class CreateUserResponseBase(BaseModel):
    id: UUID
    name: str
    email: str
    team_id: UUID
    created_at: datetime

    model_config = {"from_attributes": True}


class CreateUserResponse(CreateUserResponseBase):
    api_key: str
