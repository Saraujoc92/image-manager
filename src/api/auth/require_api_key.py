import logger
from typing import Annotated, Optional
from fastapi import Depends, Header, Request

from api.exceptions import AuthorizationError


def require_api_key(
    request: Request,
    x_api_key: Annotated[Optional[str], Header()] = None,
):
    if not x_api_key:
        logger.debug("API key is empty or None.", request)
        raise AuthorizationError()
    return x_api_key


RequireApiKeyHeader = Annotated[str, Depends(require_api_key)]
