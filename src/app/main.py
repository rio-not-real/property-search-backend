import logging

from fastapi import FastAPI

from app.api.main import api_router
from app.core.config import settings
from app.core.logger import setup_logging

setup_logging()
logger = logging.getLogger(__name__)


app = FastAPI(
    title=f"{settings.PROJECT_NAME} API",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
)


@app.get("/")
def root() -> str:
    return f"Welcome to {app.title}"


app.include_router(api_router, prefix=settings.API_V1_STR)
