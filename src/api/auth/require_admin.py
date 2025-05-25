import logger
from fastapi import Depends, Request
from typing import Annotated

from entities.api_key import ApiKey
from api.exceptions import AuthorizationError
from entities.user import User
from service.user import get_current_user


CurrentUser = Annotated[User, Depends(get_current_user)]


def require_admin(user: CurrentUser, request: Request) -> User:
    if not user.is_admin:
        logger.warning(f"User {user.id} is not an admin.", request)
        raise AuthorizationError()

    return user


RequireAdmin = Annotated[ApiKey, Depends(require_admin)]
