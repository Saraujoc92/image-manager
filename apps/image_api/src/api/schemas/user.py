from pydantic import BaseModel, EmailStr
from uuid import UUID
from datetime import datetime


class GetUserResponse(BaseModel):
    id: UUID
    name: str
    email: str
    team_id: UUID
    created_at: datetime

    model_config = {"from_attributes": True}
    
class RotateUserCredentialsResponse(BaseModel):
    api_key: str

    model_config = {"from_attributes": True}

class CreateUserRequest(BaseModel):
    email: EmailStr
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
