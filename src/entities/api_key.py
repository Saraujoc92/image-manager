from pydantic import BaseModel

class ApiKey(BaseModel):
    id: str
    key: str
    user_id: str
    active: bool = True
    is_admin: bool = False
    created_at: str
    deleted_at: str

    def __repr__(self):
        return f"<ApiKey(id={self.id}, key={self.key}, user_id={self.user_id})>"