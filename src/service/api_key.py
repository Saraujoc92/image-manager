import logger

from typing import Annotated
from uuid import UUID
from fastapi import Depends, Request

from database.client import DbSession
from database.repositories import api_key_repository as api_key_repo
from entities.api_key import ApiKey as ApiKeyModel
from api.auth.require_api_key import RequireApiKeyHeader
from api.exceptions import AuthorizationError


def get_api_key(
    db: DbSession, api_key: RequireApiKeyHeader, request: Request
) -> ApiKeyModel:
    if not api_key:
        logger.debug("API key is empty or None.", request)
        raise AuthorizationError()
    api_key_obj = api_key_repo.get_api_key(db, api_key)
    if not api_key_obj:
        logger.debug(f"API key {api_key} not found.", request)
        raise AuthorizationError()
    return api_key_obj


def create_api_key(db: DbSession, user_id: UUID, request: Request) -> ApiKeyModel:
    new_api_key = api_key_repo.create_api_key(db, user_id)
    logger.info(f"New API key created with ID: {new_api_key.id}", request)
    return new_api_key


DependsApiKey = Annotated[ApiKeyModel, Depends(get_api_key)]
