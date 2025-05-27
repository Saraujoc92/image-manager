from fastapi import APIRouter, FastAPI
from api.routes.users import router as users_router
from api.routes.team import router as teams_router
from api.routes.image import router as images_router

def register_routes(app: FastAPI):
    router = APIRouter(prefix="/api/v1")
    router.include_router(teams_router)
    router.include_router(users_router)
    router.include_router(images_router)    
    app.include_router(router)