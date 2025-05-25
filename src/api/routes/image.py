from fastapi import APIRouter, Request, UploadFile

from api.auth.require_team import RequireActiveTeam, RequireSameTeamUser
from api.exceptions import BadRequestError
from database.client import DbSession
from api.rate_limiter import limiter
import logger
from service import image as image_service

router = APIRouter(prefix="/team/{team_id}/image", tags=["Images"])

ALLOWED_IMAGE_TYPES = {"image/jpeg", "image/png"}


@router.post("", status_code=201)
@limiter.limit("1/minute")
def upload_image(
    db: DbSession,
    user: RequireSameTeamUser,
    team: RequireActiveTeam,
    request: Request,
    file: UploadFile,
):
    if file.content_type not in ALLOWED_IMAGE_TYPES:
        raise BadRequestError("Unsupported image type. Allowed types are: JPEG, PNG")

    logger.info(f"Uploading image for team {team.id}", request)
    image_bytes = file.file.read()
    
    if not image_bytes:
        raise BadRequestError("Empty file")
    
    image_service.upload_image(db, team.id, user.id, image_bytes, request)
    return {"message": "Uploaded successfully", "team_id": team.id, "user_id": user.id}


@router.get("/all", status_code=200)
@limiter.limit("5/minute")
def get_all_images(
    db: DbSession, user: RequireSameTeamUser, team: RequireActiveTeam, request: Request
):
    logger.info(f"Retrieving all images for team {team.id}", request)
    images = image_service.get_all_images(db, team.id, request)
    return {"images": images}
