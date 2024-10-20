CREATE OR REPLACE TABLE property_search.austin_housing_attribute_embedding AS
SELECT *
  , ARRAY[
    ML.STANDARD_SCALER(latitude) OVER()
    , ML.STANDARD_SCALER(longitude) OVER()
    , ML.STANDARD_SCALER(garageSpaces) OVER()
    , ML.STANDARD_SCALER(parkingSpaces) OVER()
    , ML.STANDARD_SCALER(yearBuilt) OVER()
    , ML.STANDARD_SCALER(lotSizeSqFt) OVER()
    , ML.STANDARD_SCALER(livingAreaSqFt) OVER()
    , ML.STANDARD_SCALER(numOfBathrooms) OVER()
    , ML.STANDARD_SCALER(numOfBedrooms) OVER()
    , ML.STANDARD_SCALER(numOfStories) OVER()
    /* One-hot encoding for homeType */
    , ML.STANDARD_SCALER(IF(homeType = 'Single Family', 1.0, 0.0)) OVER()
    , ML.STANDARD_SCALER(IF(homeType = 'Townhouse', 1.0, 0.0)) OVER()
    , ML.STANDARD_SCALER(IF(homeType = 'Multiple Occupancy', 1.0, 0.0)) OVER()
    , ML.STANDARD_SCALER(IF(homeType = 'Condo', 1.0, 0.0)) OVER()
    , ML.STANDARD_SCALER(IF(homeType = 'Vacant Land', 1.0, 0.0)) OVER()
    , ML.STANDARD_SCALER(IF(homeType = 'Mobile / Manufactured', 1.0, 0.0)) OVER()
    , ML.STANDARD_SCALER(IF(homeType = 'Residential', 1.0, 0.0)) OVER()
    , ML.STANDARD_SCALER(IF(homeType = 'MultiFamily', 1.0, 0.0)) OVER()
    , ML.STANDARD_SCALER(IF(homeType = 'Apartment', 1.0, 0.0)) OVER()
  ] AS ml_generate_embedding_result
FROM property_search.austin_housing;

CREATE OR REPLACE VECTOR INDEX austin_housing_attribute_index
ON property_search.austin_housing_attribute_embedding(ml_generate_embedding_result)
STORING (zpid, zipcode)
OPTIONS(
  index_type = 'IVF'
  , distance_type = 'COSINE'
);
