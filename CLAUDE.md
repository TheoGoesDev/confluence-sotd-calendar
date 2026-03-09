# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

`confluence-sotd-calendar` is a Python CLI tool that creates "Support of the Day" (SOTD) all-day events in a Confluence Cloud Team Calendar. Engineers rotate on a round-robin schedule across workdays (Mon–Fri).

## Technology Stack

- **Language:** Python ≥3.11
- **Package manager:** uv
- **Linter/formatter:** Ruff
- **Key dependencies:** `click`, `requests`, `python-dotenv`

## Common Commands

```bash
uv sync              # Install dependencies
uv run python sotd.py --help  # Show CLI usage
uv run ruff check .  # Lint
uv run ruff format . # Format
```

## Environment

Secrets are stored in `.env` (gitignored). Copy `.env.example` to `.env` and fill in:
- `CONFLUENCE_URL` — e.g. `https://yourcompany.atlassian.net`
- `CONFLUENCE_EMAIL` — Atlassian account email
- `CONFLUENCE_API_TOKEN` — Atlassian API token
- `CONFLUENCE_CALENDAR_ID` — UUID of the target Team Calendar sub-calendar

## Project Structure

- `sotd.py` — single-file CLI entrypoint (all logic lives here)
- `pyproject.toml` — project metadata and dependencies
- `.env.example` — template for required environment variables
- `docs/` — extended documentation
