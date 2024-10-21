from typing import Annotated, AsyncGenerator

from fastapi import Depends
from google.cloud.bigquery import Client

from app.core.db import get_bq_client


async def bq_client() -> AsyncGenerator[Client, None]:
    with get_bq_client() as client:
        yield client


ClientDep = Annotated[Client, Depends(bq_client)]
