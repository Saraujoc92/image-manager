import logger
from typing import Annotated

from fastapi import Depends, Request
from entities.user import User
from api.auth.require_admin import CurrentUser
from entities.team import Team
from service.team import get_team_by_id
from api.exceptions import AuthorizationError


RequireActiveTeam = Annotated[Team, Depends(get_team_by_id)]


def require_same_team(
    user: CurrentUser, team: RequireActiveTeam, request: Request
) -> User:
    if not user.is_admin and user.team_id != team.id:
        logger.debug(f"User {user.id} does not belong to team {team.id}.", request)
        logger.warning(
            f"User {user.id} from team {user.team_id} attempted to access team {team.id} without permission.",
            request,
        )
        raise AuthorizationError()
    return user


RequireSameTeamUser = Annotated[User, Depends(require_same_team)]
