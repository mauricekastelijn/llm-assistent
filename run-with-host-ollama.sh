#!/bin/bash

set -o errexit
set -o errtrace
set -o pipefail
set -o nounset

SCRIPT_PATH="$(dirname "$(realpath $0)")"
CWD="$(pwd)"

if [ $# -eq 0 ]; then
    ROOT_PATH="$CWD"
else
    ROOT_PATH="$(realpath $1)"
fi
echo Using code base root path $ROOT_PATH

docker compose -f $SCRIPT_PATH/docker-compose-dev.yml build backend
docker compose -f $SCRIPT_PATH/docker-compose-dev.yml run -it --rm \
    --env OLLAMA_ENDPOINT="http://host.docker.internal:11434" \
    -p 8000:8000 \
    -v "$ROOT_PATH/backend/backend/:/home/backend" \
    -v "$ROOT_PATH/secrets/backend/.env:/home/backend/secrets/.env" \
    backend
