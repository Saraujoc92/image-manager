import logger
from datetime import datetime
from uuid import UUID

from api.schemas.user import (
    CreateUserRequest,
    CreateUserResponse,
    CreateUserResponseBase,
)
from database.models.user import User
from database.client import DbSession
from entities.user import User as UserModel
from service.api_key import DependsApiKey, create_api_key
from fastapi import Request
from database.repositories import user_repository

from api.middleware.log_context import add_user_id_to_log_context
from api.exceptions import BadRequestError, NotFoundError


def get_all_users(db: DbSession, request: Request) -> list[User]:
    users = user_repository.get_all_users(db)
    logger.info(f"Successfully retrieved all users. Total count: {len(users)}", request)
    return users


def get_all_team_users(db: DbSession, team_id: UUID, request: Request) -> list[User]:
    users = user_repository.get_all_team_users(db, team_id)
    logger.info(
        f"Successfully retrieved all users in team {team_id}. Total count: {len(users)}",
        request,
    )
    return users


def get_current_user(
    db: DbSession,
    api_key_obj: DependsApiKey,
    request: Request,
) -> UserModel:
    user_id = api_key_obj.user_id
    user = user_repository.get_user_by_id(db, user_id)
    if not user:
        logger.debug(f"User with ID {user_id} not found or inactive.", request)
        raise NotFoundError(message="User not found")

    add_user_id_to_log_context(request, user_id)
    return user


def create_new_user(
    db: DbSession, user_data: CreateUserRequest, team_id: UUID, request: Request
) -> CreateUserResponse:
    new_user = user_repository.add_user(
        db, User(**user_data.model_dump(), team_id=team_id), request
    )
    if not new_user:
        raise BadRequestError(message="Failed to create user")
    api_key = create_api_key(db, new_user.id, request)
    logger.info(f"New user in team {team_id} created with ID: {new_user.id}", request)

    return CreateUserResponse(**new_user.model_dump(), api_key=api_key.key)
