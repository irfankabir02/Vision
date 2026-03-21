# Copilot Code Review Instructions — Vision

## Code Quality

- Type hints encouraged on all function signatures.
- Basic Python style: PEP 8 compliance.
- Flag any dependency additions without justification.

## Security

- Flag pip dependency security issues.
- No `eval()`, `exec()`, or `pickle` on untrusted input.
- Flag any secret/credential patterns.

## Shared Rules

- Flag scope expansion beyond PR description.
- Conventional commits.
