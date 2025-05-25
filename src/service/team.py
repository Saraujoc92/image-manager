from uuid import UUID
from fastapi import Request
from collections.abc import Sequence

import logger
from api.exceptions import BadRequestError, NotFoundError
from database.client import DbSession
from database.repositories import user_repository
from database.repositories import api_key_repository
from database.repositories import team_repository
from entities.team import Team


def get_all_teams(db: DbSession, request: Request) -> Sequence[Team]:
    teams = team_repository.get_all_teams(db)
    logger.info(f"Retrieved {len(teams)} teams from the database", request)
    return teams
    return teams


def get_team_by_id(db: DbSession, team_id: str, request: Request) -> Team:
    team = team_repository.get_team_by_id(db, team_id)
    if not team:
        raise NotFoundError(message="Team not found")
    logger.info(f"Retrieved team with ID {team_id}", request)
    return team


def create_team(db: DbSession, team_name: str, request: Request) -> Team:
    new_team = team_repository.create_team(db, team_name)
    if not new_team:
        raise BadRequestError(message="Failed to create team")
    logger.info(f"Created team {new_team.name}: ID {new_team.id}", request)
    return new_team


def delete_team(db: DbSession, team_id: UUID, request: Request) -> None:
    """sets the team and all its members to inactive"""
    logger.info(f"Deleting team with ID {team_id}", request)
    team_repository.delete_team(db, team_id)
    deleted_users = user_repository.delete_users_by_team_id(db, team_id)
    api_key_repository.deactivate_api_key_for_users(db, deleted_users)
    db.commit()
    logger.info(f"Deactivated {len(deleted_users)} users from team {team_id}", request)
