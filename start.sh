#!/bin/sh
# Start the course (macOS and Linux). Installs uv the first time if it's missing.
set -eu
cd "$(dirname "$0")"

UV_VERSION=0.13.5
if ! command -v uv >/dev/null 2>&1; then
    PATH="$HOME/.local/bin:$PATH"
    if ! command -v uv >/dev/null 2>&1; then
        echo "First run: installing uv $UV_VERSION, which sets up Python for this course..."
        if ! command -v curl >/dev/null 2>&1; then
            echo "Please install curl, then run ./start.sh again." >&2
            exit 1
        fi
        curl -LsSf "https://astral.sh/uv/$UV_VERSION/install.sh" | sh
    fi
fi

echo "Preparing the course (the first time can take a few minutes)..."
uv sync --frozen --no-dev --quiet
exec uv run --frozen --no-sync python -m learn_llm.launch "$@"
