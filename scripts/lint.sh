#!/usr/bin/env bash

SCRIPTS_DIR=$( cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &> /dev/null && pwd )
cd "$SCRIPTS_DIR/.."

ruff check src --fix
ruff format src --check
mypy src
