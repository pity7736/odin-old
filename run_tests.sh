#!/usr/bin/env bash
pytest -vvvv -s --cov=odin --cov-report term-missing tests/
