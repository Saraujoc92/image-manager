from uuid import UUID
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from logger import Log


class LoggerContextMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        log = Log()
        request.state.log = log
        response = await call_next(request)
        return response


def add_user_id_to_log_context(request: Request, user_id: UUID) -> None:
    request.state.log.user_id = f"{user_id}"


def add_team_id_to_log_context(request: Request, team_id: UUID) -> None:
    request.state.log.team_id = f"{team_id}"

def add_request_id_to_log_context(request: Request, request_id: str) -> None:
    request.state.log.request_id = request_id