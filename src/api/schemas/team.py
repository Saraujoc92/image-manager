from pydantic import BaseModel

class CreateTeamRequest(BaseModel):
    name: str
    