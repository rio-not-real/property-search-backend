CREATE OR REPLACE MODEL property_search.embedding_model
REMOTE WITH CONNECTION `projects/@@project/locations/US/connections/bigquery-vertex-conn`
OPTIONS (ENDPOINT = 'text-embedding-preview-0815');

CREATE OR REPLACE TABLE property_search.austin_housing_content_embedding AS
SELECT * FROM ML.GENERATE_EMBEDDING(
  MODEL property_search.embedding_model
  , TABLE property_search.austin_housing
  , STRUCT(
    TRUE AS flatten_json_output
    , 'SEMANTIC_SIMILARITY' AS task_type
    , 768 AS output_dimensionality
  )
)
WHERE LENGTH(ml_generate_embedding_status) = 0;

CREATE OR REPLACE VECTOR INDEX austin_housing_attribute_index
ON property_search.austin_housing_attribute_embedding(ml_generate_embedding_result)
STORING (zpid, zipcode, homeType, numOfBedrooms, numOfBathrooms, garageSpaces)
OPTIONS(
  index_type = 'IVF'
  , distance_type = 'COSINE'
);
