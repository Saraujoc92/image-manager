import logging
from fastapi import FastAPI

from logger import configure_logging
from api.middleware.request_id import RequestIdMiddleware
from api.middleware.log_context import LoggerContextMiddleware

from api.register_routes import register_routes
from api.rate_limiter import limiter, rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

configure_logging(logging.DEBUG)

app = FastAPI()

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, rate_limit_exceeded_handler)
    
app.add_middleware(RequestIdMiddleware)
app.add_middleware(LoggerContextMiddleware)

register_routes(app)
