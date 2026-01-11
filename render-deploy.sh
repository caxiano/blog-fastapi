#!/usr/bin/env bash
set -e

alemb upgrade head
uvicorn src.main:app --host 0.0.0.0 --port $PORT