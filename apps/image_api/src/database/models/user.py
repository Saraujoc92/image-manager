from datetime import datetime
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
import uuid

from database.client import Base


class User(Base):
    __tablename__ = "app_user"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    team_id = Column(UUID(as_uuid=True), ForeignKey("team.id"), nullable=False)
    email = Column(String, nullable=False)
    name = Column(String, nullable=False)
    active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.now)
    deleted_at = Column(DateTime)

    def __repr__(self):
        return f"<User(email='{self.email}', name='{self.name}')>"
