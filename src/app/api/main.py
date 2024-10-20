from fastapi import APIRouter

from app.api.routes import properties

api_router = APIRouter()
api_router.include_router(properties.router, prefix="/properties", tags=["properties"])
