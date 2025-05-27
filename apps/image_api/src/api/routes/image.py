from fastapi import APIRouter, Request, UploadFile, status

from api.auth.require_team import RequireActiveTeam, RequireSameTeamUser
from api.exceptions import BadRequestError
from api.schemas.image import GetImageResponse
from database.client import DbSession
from api.rate_limiter import limiter
import logger
from service import image as image_service

router = APIRouter(prefix="/team/{team_id}/image", tags=["Images"])

ALLOWED_IMAGE_TYPES = {"image/jpeg", "image/png"}


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    summary="Upload an image",
    description="Upload an image to the team. Supported formats: JPEG, PNG. Max size: 2 MB.",
    responses={
        200: {
            "description": "Image uploaded successfully",
            "content": {
                "application/json": {
                    "example": {
                        "message": "Uploaded successfully",
                        "team_id": "*****",
                        "user_id": "*****",
                    }
                }
            },
        },
        400: {
            "description": "Bad Request",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Unsupported image type. Allowed types are: JPEG, PNG"
                    }
                }
            },
        },
        404: {
            "description": "Not Found",
            "content": {"application/json": {"example": {"detail": "Team not found"}}},
        },
    },
)
@limiter.limit("3/minute")
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
    
    if len(image_bytes) > 2 * 1024 * 1024:  # 2 MB limit
        raise BadRequestError("File size exceeds 2 MB limit")

    image_service.upload_image(
        db, team.id, user.id, file.filename or "nn", image_bytes, request
    )
    return {"message": "Uploaded successfully", "team_id": team.id, "user_id": user.id}


@router.get(
    "/all",
    status_code=200,
    summary="Get all images for a team",
    description="Retrieve all images uploaded to the team. Requires active team membership.",
    response_model=list[GetImageResponse],
    responses={
        404: {
            "description": "Not Found",
            "content": {"application/json": {"example": {"detail": "Team not found"}}},
        }
    },
)
@limiter.limit("5/minute")
def get_all_images(
    db: DbSession, user: RequireSameTeamUser, team: RequireActiveTeam, request: Request
):
    logger.info(f"Retrieving all images for team {team.id}", request)
    return image_service.get_all_images(db, team.id, request)
