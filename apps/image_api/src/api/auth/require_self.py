from typing import Annotated
from uuid import UUID
from fastapi import Depends, Request
import logger
from api.exceptions import AuthorizationError
from api.auth.require_admin import CurrentUser
from entities.user import User


def require_self(user: CurrentUser, user_id: UUID, request: Request) -> User:
    if user.id != user_id:
        logger.warning(
            f"User {user.id} attempted to access user {user_id} without permission.",
            request,
        )
        raise AuthorizationError()
    return user


RequireSelf = Annotated[User, Depends(require_self)]
