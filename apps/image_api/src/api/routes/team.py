from fastapi import APIRouter, Request, status

import service.team as service
from database.client import DbSession
from api.schemas.team import CreateTeamRequest, GetTeamResponse
from api.auth.require_admin import RequireAdmin
from api.auth.require_team import RequireActiveTeam
from api.rate_limiter import limiter

router = APIRouter(prefix="/team", tags=["Teams"])


@router.get(
    "/all",
    summary="Get all teams [Admin Only]",
    description="Get all teams. **Requires admin privileges**.",
    response_model=list[GetTeamResponse],
)
@limiter.limit("10/minute")
def get_all_teams(db: DbSession, api_key: RequireAdmin, request: Request):
    return service.get_all_teams(db, request)


@router.post(
    "/",
    summary="Create a new team [Admin Only]",
    description="Create a new team. **Requires admin privileges**.",
    response_model=GetTeamResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        400: {
            "description": "Bad Request",
            "content": {
                "application/json": {"example": {"detail": "Team already exists"}}
            },
        }
    },
)
@limiter.limit("5/minute")
def create_team(
    db: DbSession, team_data: CreateTeamRequest, api_key: RequireAdmin, request: Request
):
    new_team = service.create_team(db, team_data.name, request)
    return new_team


@router.delete(
    "/{team_id}",
    summary="Delete a team [Admin Only]",
    description="Delete a team and all its members. **NON REVERSIBLE. Requires admin privileges**.",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        404: {
            "description": "Not Found",
            "content": {
                "application/json": {"example": {"detail": "Team not found"}}
            },
        }
    },
)
@limiter.limit("1/minute")
def delete_team(
    team: RequireActiveTeam, db: DbSession, api_key: RequireAdmin, request: Request
):
    service.delete_team(db, team.id, request)
