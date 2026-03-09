# confluence-sotd-calendar

CLI tool to bulk-create "Support of the Day" (SOTD) all-day events in a Confluence Cloud Team Calendar, rotating engineers round-robin across workdays.

## Quick start

```bash
cp .env.example .env   # fill in your Confluence credentials
uv sync
python sotd.py --engineers alice,bob,carol --dry-run   # preview the schedule
python sotd.py --engineers alice,bob,carol              # create events for current month
```

See [`docs/setup.md`](docs/setup.md) for credential setup and [`docs/usage.md`](docs/usage.md) for full CLI reference.
