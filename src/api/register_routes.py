from fastapi import FastAPI
from api.routes.users import router as users_router
from api.routes.team import router as teams_router

def register_routes(app: FastAPI):
    app.include_router(users_router)
    app.include_router(teams_router)