import logger
from slowapi.util import get_remote_address
from slowapi import Limiter, _rate_limit_exceeded_handler

limiter = Limiter(key_func=get_remote_address)

def rate_limit_exceeded_handler(request, exc):
    logger.error(f"Rate limit exceeded: {exc.detail}", request)
    return _rate_limit_exceeded_handler(request, exc)