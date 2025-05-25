from datetime import datetime
from uuid import UUID
import logger
from typing import Optional
from psycopg2.errors import UniqueViolation
from sqlalchemy.exc import IntegrityError

from fastapi import Request
from database.models.user import User
from database.client import DbSession
from api.schemas.user import CreateUserResponseBase


def add_user(
    db: DbSession, new_user: User, request: Request
) -> Optional[CreateUserResponseBase]:
    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return CreateUserResponseBase.model_validate(new_user)

    except IntegrityError as e:
        if isinstance(e.orig, UniqueViolation):
            logger.info(
                f"User already exists: {new_user.email}.",
                request,
            )
            return None
        raise e

    except Exception as e:
        logger.error(f"Unexpected error adding user: {e}", request)
        db.rollback()
        raise e


def delete_users_by_team_id(db: DbSession, team_id: UUID) -> list[UUID]:
    users_to_deactivate = db.query(User).filter(User.team_id == team_id).all()
    db.query(User).filter(User.team_id == team_id).update(
        {"active": False, "deleted_at": datetime.now()}
    )
    return [getattr(user, "id") for user in users_to_deactivate]


def get_user_by_id(db: DbSession, user_id: UUID) -> Optional[User]:
    return db.query(User).filter(User.id == user_id, User.active).first()


def get_all_users(db: DbSession) -> list[User]:
    return db.query(User).all()


def get_all_team_users(db: DbSession, team_id: UUID) -> list[User]:
    return db.query(User).filter(User.team_id == team_id, User.active).all()
