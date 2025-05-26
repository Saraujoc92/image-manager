from uuid import uuid4

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

from api.middleware.log_context import add_request_id_to_log_context


class RequestIdMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request_id = request.headers.get("X-Request-ID", str(uuid4()))
        add_request_id_to_log_context(request, request_id)
        response = await call_next(request)
        response.headers["X-Request-ID"] = request_id
        return response
