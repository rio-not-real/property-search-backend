import logging
from typing import Any, Literal

from google.cloud.bigquery import Client, table

from app.constants import DEFAULT_DATASET, DEFAULT_DISTANCE_TYPE, DEFAULT_TABLE

logger = logging.getLogger(__name__)


def read_property_by_zpid(
    zpid: int,
    bq_client: Client,
    dataset_name: str = DEFAULT_DATASET,
    table_name: str = DEFAULT_TABLE,
) -> dict[str, Any] | None:
    """Gets a property by zpid."""

    stmt: str = (
        f"SELECT * FROM {dataset_name}.{table_name} WHERE zpid = {zpid} LIMIT 1;"
    )
    logger.debug("Executing statement: %s", stmt)
    row: table.RowIterator = bq_client.query_and_wait(stmt)
    try:
        return dict(next(row))
    except StopIteration:
        logger.warning("Property with zpid %s not found", zpid)
        return None


def property_exists(
    zpid: int,
    bq_client: Client,
    dataset_name: str = DEFAULT_DATASET,
    table_name: str = DEFAULT_TABLE,
) -> bool:
    """Checks if a property exists."""

    stmt: str = f"""
SELECT EXISTS(
    SELECT zpid FROM {dataset_name}.{table_name} WHERE zpid = {zpid}
) AS property_exists;
"""
    logger.debug("Executing statement: %s", stmt)
    row: table.RowIterator = bq_client.query_and_wait(stmt)
    property_exists: bool = next(row).property_exists
    return property_exists


def search_similar_properties_by_content(
    search_query: str,
    bq_client: Client,
    top_k: int = 6,
    distance_type: Literal[
        "EUCLIDEAN", "COSINE", "DOT_PRODUCT"
    ] = DEFAULT_DISTANCE_TYPE,  # type: ignore[assignment]
) -> list[dict[str, Any]]:
    """Given a search query, finds the top k properties with the most similar listing descriptions."""

    stmt: str = f"""
SELECT *
FROM VECTOR_SEARCH(
    TABLE {DEFAULT_DATASET}.{DEFAULT_TABLE}
    , 'ml_generate_embedding_result'
    , (
        SELECT ml_generate_embedding_result, content AS query
        FROM ML.GENERATE_EMBEDDING(
            MODEL {DEFAULT_DATASET}.embedding_model
            , (SELECT '{search_query}' AS content)
        )
    )
    , top_k => {top_k}
    , distance_type => '{distance_type}'
)
"""
    print(stmt)
    logger.debug("Executing statement: %s", stmt)
    rows: table.RowIterator = bq_client.query_and_wait(stmt)
    return [dict(row) for row in rows]


def search_get_similar_properties_by_id(
    zpid: int,
    bq_client: Client,
    dataset_name: str = DEFAULT_DATASET,
    table_name: str = f"{DEFAULT_TABLE}_attribute_embedding",
    top_k: int = 6,
    distance_type: Literal[
        "EUCLIDEAN", "COSINE", "DOT_PRODUCT"
    ] = DEFAULT_DISTANCE_TYPE,  # type: ignore[assignment]
) -> list[dict[str, Any]]:
    """Given a property, finds the top k most similar properties.
    Prioritising properties in the same zipcode over properties in different zipcodes.
    """

    stmt: str = f"""
DECLARE zipcode INT64 DEFAULT (
    SELECT zipcode FROM {dataset_name}.{table_name} WHERE zpid = {zpid} LIMIT 1
);
WITH same_zipcode AS (
    SELECT base.*
    FROM VECTOR_SEARCH(
        (
            SELECT *
            FROM {dataset_name}.{table_name}
            WHERE zpid <> {zpid} AND zipcode = zipcode
        )
        , 'ml_generate_embedding_result'
        , (
            SELECT ml_generate_embedding_result
            FROM {dataset_name}.{table_name}
            WHERE zpid = {zpid}
        )
        , top_k => {top_k}
        , distance_type => '{distance_type}'
    )
)
, different_zipcode AS (
    SELECT base.*
    FROM VECTOR_SEARCH(
        (
            SELECT *
            FROM {dataset_name}.{table_name}
            WHERE zpid <> {zpid} AND zipcode <> zipcode
        )
        , 'ml_generate_embedding_result'
        , (
            SELECT ml_generate_embedding_result
            FROM {dataset_name}.{table_name}
            WHERE zpid = {zpid}
        )
        , top_k => {top_k}
        , distance_type => '{distance_type}'
    )
)
SELECT * FROM (
    SELECT * EXCEPT (ml_generate_embedding_result)
    FROM same_zipcode
    UNION ALL
    SELECT * EXCEPT (ml_generate_embedding_result)
    FROM different_zipcode
)
LIMIT {top_k};
"""
    logger.debug("Executing statement: %s", stmt)
    properties: table.RowIterator = bq_client.query_and_wait(stmt)
    return [dict(row) for row in properties]
