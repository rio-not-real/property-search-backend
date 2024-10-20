from typing import Annotated, Generator

from fastapi import Depends
from google.cloud.bigquery import Client

from app.core.db import get_bq_client


def bq_client() -> Generator[Client, None, None]:
    with get_bq_client() as client:
        yield client


ClientDep = Annotated[Client, Depends(bq_client)]
