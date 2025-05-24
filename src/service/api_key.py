import logging

from uuid import UUID
from fastapi import HTTPException

from database.client import DbSession
from database.models.api_key import ApiKey
from database.models.user import User
from entities.api_key import ApiKey as ApiKeyModel

def get_api_key(db: DbSession, api_key: str) -> ApiKeyModel:
    """
    Retrieve an API key from the database ensuring it exists and is active.

    Args:
        db (Session): The database session.
        api_key (str): The API key to retrieve.

    Returns:
        ApiKey: The retrieved API key object.
    """
    if not api_key:
        logging.debug("API key is empty or None.")
        raise HTTPException(status_code=401, detail="Unauthorized")
    api_key_obj = db.query(ApiKey).filter(ApiKey.key == api_key, ApiKey.active).first()

    if not api_key_obj:
        logging.debug(f"API key {api_key} not found.")
        raise HTTPException(status_code=401, detail="Unauthorized")
    return api_key_obj

