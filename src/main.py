import logging
from fastapi import FastAPI

from api.register_routes import register_routes
from logger import configure_logging
from database.client import engine, Base
from database.models.user import User
from database.models.team import Team
from database.models.api_key import ApiKey

Base.metadata.create_all(bind=engine)

configure_logging(logging.DEBUG)

app = FastAPI()


register_routes(app)
