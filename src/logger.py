import logging
from typing import Optional
from fastapi import Request


LOG_FORMAT_DEBUG = "%(levelname)s:%(message)s:%(pathname)s:%(funcName)s:%(lineno)d"


def configure_logging(log_level: int = logging.INFO) -> None:
    logging.basicConfig(level=log_level, format=LOG_FORMAT_DEBUG)


class Log:
    request_id: Optional[str] = None
    user_id: Optional[str] = None


def _get_log_context(request: Request) -> Log:
    return request.state.log


def _log_context(request: Request, message: str) -> str:
    log = _get_log_context(request)
    return f"Request ID: {log.request_id} | User ID: {log.user_id} | {message}"


def debug(message: str, request: Request) -> None:
    logging.debug(_log_context(request, message))


def info(message: str, request: Request) -> None:
    logging.info(_log_context(request, message))


def warning(message: str, request: Request) -> None:
    logging.warning(_log_context(request, message))


def error(message: str, request: Request) -> None:
    logging.error(_log_context(request, message))
    # TODO: Implement error logging to alering service
