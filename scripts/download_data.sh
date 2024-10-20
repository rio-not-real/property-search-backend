#!/usr/bin/env bash

SCRIPTS_DIR=$( cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &> /dev/null && pwd )
cd "$SCRIPTS_DIR/.."

curl -L -o resources/archive.zip \
https://www.kaggle.com/api/v1/datasets/download/ericpierce/austinhousingprices

unzip resources/archive.zip -d resources/
