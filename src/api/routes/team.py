from fastapi import APIRouter, Request, status

import service.team as service
from database.client import DbSession
from api.schemas.team import CreateTeamRequest
from api.auth.require_admin import RequireAdmin
from api.auth.require_team import RequireActiveTeam
from api.rate_limiter import limiter

router = APIRouter(prefix="/teams", tags=["Teams"])


@router.get("/all")
@limiter.limit("10/minute")
def get_all_teams(db: DbSession, api_key: RequireAdmin, request: Request):
    return service.get_all_teams(db, request)


@router.post("/", status_code=status.HTTP_201_CREATED)
@limiter.limit("5/minute")
def create_team(
    db: DbSession, team_data: CreateTeamRequest, api_key: RequireAdmin, request: Request
):
    new_team = service.create_team(db, team_data.name, request)
    return new_team


@router.delete("/{team_id}", status_code=status.HTTP_204_NO_CONTENT)
@limiter.limit("1/minute")
def delete_team(team: RequireActiveTeam, db: DbSession, api_key: RequireAdmin, request: Request):
    service.delete_team(db, team.id, request)
