# confluence-sotd-calendar

CLI tool to bulk-create "Support of the Day" (SOTD) all-day events in a Confluence Cloud Team Calendar, rotating engineers round-robin across workdays.

## Quick start

```bash
cp .env.example .env   # fill in your Confluence credentials
uv sync
python sotd.py --number-of-days 30 --engineers alice,bob,carol
```

See [`docs/setup.md`](docs/setup.md) for credential setup and [`docs/usage.md`](docs/usage.md) for full CLI reference.
