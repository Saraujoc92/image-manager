from datetime import datetime
from typing import Optional
from uuid import UUID

from database.client import DbSession
from database.models.team import Team


def get_all_teams(db: DbSession) -> list[Team]:
    return db.query(Team).all()


def get_team_by_id(db: DbSession, team_id: str) -> Optional[Team]:
    return db.query(Team).filter(Team.id == team_id, Team.active).first()


def create_team(db: DbSession, team_name: str) -> Team:
    new_team = Team(name=team_name)
    db.add(new_team)
    db.commit()
    db.refresh(new_team)
    return new_team


def delete_team(db: DbSession, team_id: UUID) -> None:
    db.query(Team).filter(Team.id == team_id).update(
        {"active": False, "deleted_at": datetime.now()}
    )
