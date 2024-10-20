from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=Path("../../../.env"),
        env_ignore_empty=True,
        extra="ignore",
    )
    PROJECT_NAME: str = "Property Search"
    API_V1_STR: str = "/api/v1"

    GOOGLE_CLOUD_PROJECT: str
    GOOGLE_CLOUD_LOCATION: str = "US"


settings = Settings()  # type: ignore
