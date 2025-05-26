from datetime import datetime
from sqlalchemy import Boolean, Column, DateTime, String
from sqlalchemy.dialects.postgresql import UUID
import uuid

from database.client import Base


class Team(Base):
    __tablename__ = "team"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(50), nullable=False, unique=True)
    active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now())
    deleted_at = Column(DateTime)

    def __repr__(self):
        return f"<Team(id={self.id}, name={self.name})>"
