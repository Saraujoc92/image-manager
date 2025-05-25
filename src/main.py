import logging
from fastapi import FastAPI

from logger import configure_logging
from api.middleware.request_id import RequestIdMiddleware
from api.middleware.log_context import LoggerContextMiddleware

from api.register_routes import register_routes

configure_logging(logging.DEBUG)

app = FastAPI()

app.add_middleware(RequestIdMiddleware)
app.add_middleware(LoggerContextMiddleware)

register_routes(app)
