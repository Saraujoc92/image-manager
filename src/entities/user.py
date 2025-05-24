from pydantic import BaseModel

class User(BaseModel):
    id: str
    team_id: str
    email: str
    name: str
    active: bool = True
    created_at: str
    deleted_at: str

    def __repr__(self):
        return f"<User(email='{self.email}', name='{self.name}')>"