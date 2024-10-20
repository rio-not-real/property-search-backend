from functools import lru_cache

from google.cloud.bigquery import Client

from app.core.config import settings


@lru_cache
def get_bq_client() -> Client:
    bq_client: Client = Client(
        project=settings.GOOGLE_CLOUD_PROJECT,
        location=settings.GOOGLE_CLOUD_LOCATION,
    )
    return bq_client
