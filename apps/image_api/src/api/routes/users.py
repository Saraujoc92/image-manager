from fastapi import APIRouter, Request, status

from database.client import DbSession
from api.auth.require_self import RequireSelf
from api.auth.require_team import RequireActiveTeam, RequireSameTeamUser
from api.auth.require_admin import RequireAdmin
from api.schemas.user import (
    CreateUserRequest,
    CreateUserResponse,
    GetUserResponse,
    RotateUserCredentialsResponse,
)
from service import user as service
from api.rate_limiter import limiter


router = APIRouter(tags=["Users"])


@router.get(
    "/user/all",
    summary="Get all users [Admin Only]",
    description="""
    Get a list of all users across all teams. **Requires admin privileges**.
    """,
    response_model=list[GetUserResponse],
)
@limiter.limit("5/minute")
def get_all_users(db: DbSession, user: RequireAdmin, request: Request):
    return service.get_all_users(db, request)


@router.post(
    "/user/{user_id}/credentials/rotate",
    summary="Rotate user credentials",
    description="""
    Rotate the API key for a user. **NON REVERSIBLE**.
    The api key must belong to the user whose credentials are being rotated.
    """,
    response_model=RotateUserCredentialsResponse,
)
@limiter.limit("1/minute")
def rotate_user_credentials(db: DbSession, user: RequireSelf, request: Request):
    new_api_key = service.rotate_user_credentials(db, user, request)
    return {"api_key": new_api_key}


@router.get(
    "/team/{team_id}/user/all",
    summary="Get all users in a team",
    description="""
    Get a list of all users in a specific team. Requires active team membership or Admin privileges.
    """,
    response_model=list[GetUserResponse],
)
def get_all_team_users(
    db: DbSession, user: RequireSameTeamUser, team: RequireActiveTeam, request: Request
):
    return service.get_all_team_users(db, team.id, request)


@router.post(
    "/team/{team_id}/user",
    status_code=status.HTTP_201_CREATED,
    description="""
             Create a new user in the team. Requires active team membership or Admin privileges.
             Will return the created user with an API key. **Store the API key securely, it cannot be retrieved later**.
             """,
    response_model=CreateUserResponse,
)
@limiter.limit("10/minute")
def create_new_user(
    db: DbSession,
    user: RequireSameTeamUser,
    user_data: CreateUserRequest,
    team: RequireActiveTeam,
    request: Request,
):
    return service.create_new_user(db, user_data, team.id, request)
