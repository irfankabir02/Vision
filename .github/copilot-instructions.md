# Vision Copilot Instructions

## Review Guardrails

- Python 3.13+, type hints required on all functions and methods.
- Package manager: `uv` only — never `pip`, `poetry`, or `conda`.
- No `eval()`, `exec()`, or `pickle` in runtime code.
- Do not hardcode paths, tokens, or desktop-specific secrets.
- Prefer deterministic tests over environment-specific OCR behavior.
- Keep `pytest`, `pip-audit`, and build validation green.

## Stack

Python 3.13+, pytesseract (OCR), Pillow, transformers (HuggingFace), rich (terminal UI).
Testing: pytest. Linting: ruff. Security: pip-audit.

## Commands

```bash
uv sync --frozen --extra dev     # Install deps
uv run ruff check .              # Lint
uv run ruff format --check .     # Format check
uv run pytest -q --tb=short      # Tests
uv run pip-audit                 # Security audit
```

## Structure

- `UI_UX/` — Screen-aware utilities package.
- `vision_ui/` — CLI core logic. Entry point: `vision-ui` (defined in pyproject.toml).
- `tests/` — Test suite.

## Code Review Focus

- **CLI stability**: Keep the `vision-ui` entry point contract stable.
- **Token budgeting**: Summarization logic must preserve profile-specific output constraints.
- **OCR pipeline**: Graceful degradation when tesseract binary is unavailable.
- **Dependencies**: Keep minimal. Avoid adding ML libraries beyond existing `transformers`.

## Environment

- GitHub account: `irfankabir02` (separate from primary workspace account).
- CI: `ci.yml` (uv sync → ruff → pytest → pip-audit → build).
- Releases: `release.yml` handles PyPI publishing.
