#!/bin/bash
poetry install
poetry run python server.py 2> logs/error.log > logs/app.log &
