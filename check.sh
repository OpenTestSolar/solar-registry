#!/usr/bin/env bash

set -exu -o pipefail

pdm run ruff format src
pdm run ruff format tests
pdm run ruff check src
pdm run ruff check tests
pdm run mypy src --strict
pdm run mypy tests --strict
pdm run pytest tests --durations=5 --cov=. --cov-report term