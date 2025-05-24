from fastapi import APIRouter, Depends
from typing import Annotated

from service.api_key import get_api_key
from database.client import DbSession
from service import user as service
from api.auth.require_admin import RequireAdmin


router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/all")
def get_current_user(db: DbSession):
    return service.get_all_users(db)


@router.get("/protected")
def get_current_users(db: DbSession, api_key: RequireAdmin):
    print(api_key)
    return service.get_all_users(db)
