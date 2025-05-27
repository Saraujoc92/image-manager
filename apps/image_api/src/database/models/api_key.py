from datetime import datetime
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
import uuid
from database.client import Base


class ApiKey(Base):
    __tablename__ = "api_key"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    key = Column(String, unique=True, index=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(UUID(as_uuid=True), ForeignKey("app_user.id"), nullable=False)
    active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now)
    deleted_at = Column(DateTime)

    def __repr__(self):
        return f"<ApiKey(id={self.id}, key={self.key})>"

