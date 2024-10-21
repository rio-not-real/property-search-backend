from pathlib import Path
from typing import Annotated

from pydantic import AnyUrl, BeforeValidator, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


def parse_cors(origins: str) -> list[str]:
    return [origin.strip() for origin in origins.strip("[]{}()").split(",")]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=Path("../../../.env"),
        env_ignore_empty=True,
        extra="ignore",
    )
    PROJECT_NAME: str = "Property Search"
    API_V1_STR: str = "/api/v1"

    FRONTEND_HOST: str = "http://localhost:8501"
    BACKEND_CORS_ORIGINS: Annotated[
        list[AnyUrl] | str, BeforeValidator(parse_cors)
    ] = []

    @computed_field  # type: ignore[prop-decorator]
    @property
    def all_cors_origins(self) -> list[str]:
        return [str(origin).rstrip("/") for origin in self.BACKEND_CORS_ORIGINS] + [
            self.FRONTEND_HOST
        ]

    GOOGLE_CLOUD_PROJECT: str
    GOOGLE_CLOUD_LOCATION: str = "US"


settings = Settings()  # type: ignore
