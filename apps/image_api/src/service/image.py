from datetime import datetime
from uuid import UUID

from fastapi import Request
from clients import cloud_storage as cloud_storage_client
from database.client import DbSession
from database.repositories.image_repository import insert_image, get_all_team_images


def upload_image(
    db: DbSession,
    team_id: UUID,
    uploader_id: UUID,
    file_name: str,
    image: bytes,
    request: Request,
):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    image_path = f"team_{team_id}/{uploader_id}/{file_name}_{timestamp}.jpg"
    cloud_storage_client.upload_file_to_bucket(
        file_path=image_path, file=image, request=request
    )
    insert_image(
        db=db, image_path=image_path, uploaded_by=uploader_id, owner_team=team_id
    )


def get_all_images(db: DbSession, team_id: UUID, request: Request):
    images = get_all_team_images(db=db, team_id=team_id)
    return [
        (
            {
                "image_path": image.cloud_path,
                "uploaded_by": str(image.uploaded_by),
                "url": cloud_storage_client.get_bucket_file_url(image.cloud_path),
            }
        )
        for image in images
    ]
