import logging
from typing import Any

from fastapi import APIRouter, HTTPException
from fastapi.responses import ORJSONResponse

from app.api.deps import ClientDep
from app.constants import MAX_TOP_K
from app.crud import (
    property_exists,
    read_property_by_zpid,
    search_get_similar_properties_by_id,
)

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/{property_id}", response_class=ORJSONResponse)
async def get_property_by_id(bq_client: ClientDep, property_id: int) -> Any:
    """Gets a property by its ID."""

    try:
        result = read_property_by_zpid(
            zpid=property_id,
            bq_client=bq_client,
        )
    except Exception as exc:
        logger.error("Unexpected error: %s", exc)
        raise HTTPException(status_code=500, detail="Internal server error")

    if result is None:
        raise HTTPException(status_code=404, detail="Property not found")

    return ORJSONResponse(result)


@router.get("/", response_class=ORJSONResponse)
async def get_similar_properties_by_id(
    bq_client: ClientDep, zpid: int, top_k: int
) -> Any:
    """Given a property ID, returns top k similar properties."""

    if top_k > MAX_TOP_K:
        raise HTTPException(
            status_code=400,
            detail=f"top_k must be less than or equal to {MAX_TOP_K}",
        )

    if not property_exists(
        zpid=zpid,
        bq_client=bq_client,
    ):
        raise HTTPException(status_code=404, detail="Property not found")

    try:
        properties = search_get_similar_properties_by_id(
            zpid=zpid,
            bq_client=bq_client,
            top_k=top_k,
        )
    except Exception as exc:
        logger.error("Unexpected error: %s", exc)
        raise HTTPException(status_code=500, detail="Internal server error")

    return ORJSONResponse(properties)
