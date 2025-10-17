#!/bin/bash

set -euo pipefail

DEBUG=1 uv run uvicorn app:app --reload --port 8000
