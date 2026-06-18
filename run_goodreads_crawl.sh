#!/usr/bin/env bash
set -euo pipefail

# Run from the folder that contains this script.
cd "$(dirname "$0")"

VENV_DIR=".venv"
REQUIREMENTS_FILE="requirements.txt"

if command -v python3 >/dev/null 2>&1; then
    PYTHON_BIN="python3"
elif command -v python >/dev/null 2>&1; then
    PYTHON_BIN="python"
else
    echo "Python is not installed or not available in PATH." >&2
    exit 1
fi

if [ ! -d "$VENV_DIR" ]; then
    "$PYTHON_BIN" -m venv "$VENV_DIR"
fi

"$VENV_DIR/bin/python" -m pip install --upgrade pip
"$VENV_DIR/bin/python" -m pip install -r "$REQUIREMENTS_FILE"
"$VENV_DIR/bin/python" goodreads_quotes_crawl.py
