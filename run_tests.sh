#!/usr/bin/env bash
pytest -vvvv --cov=src --cov-report term-missing tests/
