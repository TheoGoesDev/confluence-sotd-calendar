# Contributing

## Prerequisites

- Python ≥ 3.11
- [uv](https://docs.astral.sh/uv/) for dependency management

## Setup

```bash
git clone <repo-url>
cd confluence-sotd-calendar
uv sync
cp .env.example .env   # fill in your Confluence credentials
```

## Development workflow

```bash
uv run ruff check .    # lint
uv run ruff format .   # format
uv run python sotd.py --help  # smoke test
```

All logic lives in `sotd.py` (single-file design). Keep it that way unless there's a strong reason to split.

## Making changes

1. Fork the repo and create a branch: `git checkout -b feat/your-feature`
2. Make your changes and ensure `ruff check` passes with no errors
3. Format with `ruff format .` before committing
4. Open a pull request against `main`

## Code style

- Ruff is the single linter/formatter — no other tools needed
- Line length: 100 characters
- Follow existing patterns in `sotd.py` (Click for CLI, `requests` for HTTP, `python-dotenv` for config)

## Reporting issues

Open a GitHub issue with:
- What you ran (command + flags)
- Expected vs. actual behaviour
- Python version (`python --version`) and OS
