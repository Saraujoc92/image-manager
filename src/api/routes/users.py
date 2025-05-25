from fastapi import APIRouter, Request, status

from database.client import DbSession
from api.auth.require_team import RequireActiveTeam, RequireSameTeamUser
from api.auth.require_admin import RequireAdmin
from api.schemas.user import CreateUserRequest
from service import user as service
from api.rate_limiter import limiter


router = APIRouter(tags=["Users"])


@router.get("/user/all")
@limiter.limit("5/minute")
def get_all_users(db: DbSession, user: RequireAdmin, request: Request):
    return service.get_all_users(db, request)


@router.get("/team/{team_id}/user/all")
def get_all_team_users(
    db: DbSession, user: RequireSameTeamUser, team: RequireActiveTeam, request: Request
):
    return service.get_all_team_users(db, team.id, request)


@router.post("/team/{team_id}/user", status_code=status.HTTP_201_CREATED)
@limiter.limit("10/minute")
def create_new_user(
    db: DbSession,
    user: RequireSameTeamUser,
    user_data: CreateUserRequest,
    team: RequireActiveTeam,
    request: Request,
):
    return service.create_new_user(db, user_data, team.id, request)
