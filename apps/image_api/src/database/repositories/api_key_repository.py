from datetime import datetime
from typing import Optional
from uuid import UUID
from database.client import DbSession
from database.models.api_key import ApiKey


def disable_api_key_for_user(db: DbSession, user_id: UUID) -> None:
    db.query(ApiKey).filter(ApiKey.user_id == user_id).update(
        {"active": False, "deleted_at": datetime.now()}
    )
    db.commit()


def create_api_key(db: DbSession, user_id: UUID) -> ApiKey:
    new_api_key = ApiKey(user_id=user_id)
    db.add(new_api_key)
    db.commit()
    db.refresh(new_api_key)
    return new_api_key


def get_api_key(db: DbSession, key: str) -> Optional[ApiKey]:
    return db.query(ApiKey).filter(ApiKey.key == key, ApiKey.active).first()

def deactivate_api_key_for_users(db: DbSession, user_ids: list[UUID]) -> None:
    db.query(ApiKey).filter(ApiKey.user_id.in_(user_ids)).update(
        {"active": False, "deleted_at": datetime.now()}, synchronize_session=False
    )