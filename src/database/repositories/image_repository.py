from uuid import UUID
from database.client import DbSession
from database.models.image import Image
from entities.image import Image as ImageModel


def insert_image(db: DbSession, image_path: str, uploaded_by: UUID, owner_team: UUID):
    image = Image(cloud_path=image_path, uploaded_by=uploaded_by, owner_team=owner_team)
    db.add(image)
    db.commit()
    db.refresh(image)
    return image


def get_all_team_images(db: DbSession, team_id: UUID) -> list[ImageModel]:
    images = (
        db.query(Image)
        .filter(Image.owner_team == team_id, Image.deleted_at.is_(None))
        .all()
    )
    return [ImageModel.model_validate(image) for image in images]
