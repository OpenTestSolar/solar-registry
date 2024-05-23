#!/usr/bin/env bash

pdm run ruff check src
pdm run ruff check tests
pdm run mypy src --strict
pdm run mypy tests --strict
pdm run pytest tests --durations=5 --cov=. --cov-report term