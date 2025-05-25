import logger
from typing import Annotated
from uuid import UUID

from fastapi import Depends, Request
from entities.user import User
from api.auth.require_admin import CurrentUser
from entities.team import Team
from service.team import get_team_by_id
from api.exceptions import AuthorizationError


def require_same_team(user: CurrentUser, team_id: UUID, request: Request) -> None:
    if not user.is_admin and user.team_id != team_id:
        logger.debug(f"User {user.id} does not belong to team {team_id}.", request)
        logger.warning(
            f"User {user.id} from team {user.team_id} attempted to access team {team_id} without permission.",
            request,
        )
        raise AuthorizationError()
    pass


RequireActiveTeam = Annotated[Team, Depends(get_team_by_id)]

RequireSameTeam = Annotated[User, Depends(require_same_team)]
