#!/usr/bin/env python3
"""Create Support of the Day (SOTD) calendar events in Confluence Team Calendars."""

import itertools
import os
import sys
from datetime import date, timedelta

import click
import requests
from dotenv import load_dotenv

load_dotenv()

REQUIRED_ENV_VARS = [
    "CONFLUENCE_URL",
    "CONFLUENCE_EMAIL",
    "CONFLUENCE_API_TOKEN",
    "CONFLUENCE_CALENDAR_ID",
]


def load_config() -> dict:
    config = {var: os.getenv(var) for var in REQUIRED_ENV_VARS}
    missing = [var for var, val in config.items() if not val]
    if missing:
        click.echo(f"Error: missing required environment variables: {', '.join(missing)}", err=True)
        click.echo("Copy .env.example to .env and fill in your credentials.", err=True)
        sys.exit(1)
    return config


def workdays(start: date, num_days: int) -> list[date]:
    result = []
    current = start
    for _ in range(num_days):
        if current.weekday() < 5:
            result.append(current)
        current += timedelta(days=1)
    return result


def format_date(d: date) -> str:
    return d.strftime("%b %-d, %Y")


def create_event(config: dict, engineer: str, event_date: date) -> requests.Response:
    url = f"{config['CONFLUENCE_URL']}/rest/calendar-services/1.0/calendar/events.json"
    date_str = format_date(event_date)
    data = {
        "subCalendarId": config["CONFLUENCE_CALENDAR_ID"],
        "eventType": "custom",
        "what": f"SOTD: {engineer}",
        "startDate": date_str,
        "endDate": date_str,
        "allDayEvent": "true",
    }
    return requests.put(
        url,
        data=data,
        auth=(config["CONFLUENCE_EMAIL"], config["CONFLUENCE_API_TOKEN"]),
        timeout=10,
    )


@click.command()
@click.option("--number-of-days", required=True, type=int, help="Number of calendar days to schedule.")
@click.option("--engineers", required=True, help="Comma-separated list of engineer names.")
@click.option(
    "--start-date",
    default=None,
    help="Start date in YYYY-MM-DD format (default: tomorrow).",
)
def main(number_of_days: int, engineers: str, start_date: str | None) -> None:
    """Create SOTD calendar events in Confluence for a round-robin engineer rotation."""
    config = load_config()

    if start_date:
        try:
            start = date.fromisoformat(start_date)
        except ValueError:
            click.echo(f"Error: invalid date format '{start_date}', expected YYYY-MM-DD.", err=True)
            sys.exit(1)
    else:
        start = date.today() + timedelta(days=1)

    engineer_list = [e.strip() for e in engineers.split(",") if e.strip()]
    if not engineer_list:
        click.echo("Error: no engineers provided.", err=True)
        sys.exit(1)

    days = workdays(start, number_of_days)
    if not days:
        click.echo("No workdays found in the specified range.")
        sys.exit(0)

    assignments = list(zip(days, itertools.cycle(engineer_list)))

    click.echo(f"\nScheduling {len(assignments)} SOTD events from {days[0]} to {days[-1]}:\n")
    click.echo(f"  {'Date':<20} {'Engineer'}")
    click.echo(f"  {'-'*20} {'-'*20}")
    for d, eng in assignments:
        click.echo(f"  {str(d):<20} {eng}")

    click.echo()
    if not click.confirm("Create these events in Confluence?"):
        click.echo("Aborted.")
        sys.exit(0)

    click.echo()
    errors = 0
    for d, eng in assignments:
        try:
            resp = create_event(config, eng, d)
            if resp.ok:
                click.echo(f"  [OK]   {d} — {eng}")
            else:
                click.echo(f"  [FAIL] {d} — {eng}: HTTP {resp.status_code} {resp.text[:120]}")
                errors += 1
        except requests.RequestException as exc:
            click.echo(f"  [ERR]  {d} — {eng}: {exc}")
            errors += 1

    click.echo()
    if errors:
        click.echo(f"Done with {errors} error(s).")
        sys.exit(1)
    else:
        click.echo(f"All {len(assignments)} events created successfully.")


if __name__ == "__main__":
    main()
