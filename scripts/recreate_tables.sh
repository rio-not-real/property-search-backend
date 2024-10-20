#!/usr/bin/env bash

SCRIPTS_DIR=$( cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &> /dev/null && pwd )
cd "$SCRIPTS_DIR/.."

bq query --use_legacy_sql=false < scripts/drop_tables.sql

bq load \
--allow_quoted_newlines=true --source_format=CSV --skip_leading_rows=1 \
$GOOGLE_CLOUD_PROJECT:property_search.austin_housing \
resources/austinHousingData.csv \
resources/austinHousingSchema.json

bq query --use_legacy_sql=false < scripts/recreate_attribute_index.sql 
# sed -e"s,@@project,$GOOGLE_CLOUD_PROJECT,g" scripts/recreate_content_index.sql | bq query --use_legacy_sql=false
