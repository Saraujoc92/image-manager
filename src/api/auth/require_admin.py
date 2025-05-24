from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated

from service.api_key import get_api_key
from entities.api_key import ApiKey

DependsApiKey = Annotated[ApiKey, Depends(get_api_key)]

def require_admin(api_key: DependsApiKey) -> ApiKey:
    if not api_key.is_admin:
        raise HTTPException(status_code=401, detail="Unauthorized")

    return api_key

RequireAdmin = Annotated[ApiKey, Depends(require_admin)]
