import env

import logging
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError

from logger import configure_logging
from api.middleware.request_id import RequestIdMiddleware
from api.middleware.log_context import LoggerContextMiddleware
from api.exceptions import validation_exception_handler
from api.routes.register import register_routes
from api.rate_limiter import limiter, rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

configure_logging(logging.DEBUG)

app = FastAPI()

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, rate_limit_exceeded_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)

app.add_middleware(RequestIdMiddleware)
app.add_middleware(LoggerContextMiddleware)

register_routes(app)
