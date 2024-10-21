import logging

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

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


if settings.all_cors_origins:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.all_cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(api_router, prefix=settings.API_V1_STR)
