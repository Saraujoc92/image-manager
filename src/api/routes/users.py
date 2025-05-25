from fastapi import APIRouter, Request, status

from database.client import DbSession
from api.auth.require_team import RequireActiveTeam, RequireSameTeam
from api.auth.require_admin import RequireAdmin
from api.schemas.user import CreateUserRequest
from service import user as service


router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/all")
def get_all_users(db: DbSession, user: RequireAdmin, request: Request):
    return service.get_all_users(db, request)


@router.get("/all/{team_id}")
def get_all_team_users(
    db: DbSession, user: RequireSameTeam, team: RequireActiveTeam, request: Request
):
    return service.get_all_team_users(db, team.id, request)


@router.post("/{team_id}", status_code=status.HTTP_201_CREATED)
def create_new_user(
    db: DbSession,
    user: RequireSameTeam,
    user_data: CreateUserRequest,
    team: RequireActiveTeam,
    request: Request,
):
    return service.create_new_user(db, user_data, team.id, request)
