from uuid import UUID

from pydantic import BaseModel


class GetImageResponse(BaseModel):
    image_path: str
    uploaded_by: UUID
    url: str

    model_config = {"from_attributes": True}
