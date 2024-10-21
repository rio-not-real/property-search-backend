#!/usr/bin/env bash

docker run -ti --env-file .env -p 80:80 \
$DOCKER_IMAGE_NAME /bin/bash -c \
"gcloud auth login --update-adc && fastapi dev --host 0.0.0.0 --port 80 src/app/main.py"