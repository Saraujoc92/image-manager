import logging
from uuid import UUID
from sqlalchemy.orm import Session
from database.models.user import User
from database.client import DbSession
from entities.user import User as UserModel
from service.api_key import get_api_key
from fastapi import HTTPException


def get_all_users(db: Session) -> list[User]:
    users = db.query(User).all()
    logging.info(f"Successfully retrieved all users. Total count: {len(users)}")
    return users


def get_user_by_api_key(db: DbSession, api_key: str) -> UserModel:
    """
    Retrieve the user ID associated with an API key.

    Args:
        db (Session): The database session.
        api_key (str): The API key to retrieve the user ID for.

    Returns:
        UUID: The user ID associated with the API key.
    """
    api_key_obj = get_api_key(db, api_key)
    user_id = api_key_obj.user_id

    user = db.query(User).filter(User.id == user_id, User.active).first()
    if not user:
        logging.debug(f"User with ID {user_id} not found or inactive.")
        raise HTTPException(status_code=404, detail="User not found")
    
    return user
