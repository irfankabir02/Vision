#!/usr/bin/env bash
set -euo pipefail

if ! command -v uv >/dev/null 2>&1; then
  python3 -m pip install uv
fi

uv sync --frozen --extra dev
uvx ruff check .
uv run pytest -q
uv run pip-audit --ignore-vuln "GHSA-2fbw-wxqw-8h3w"
uvx --from build pyproject-build
