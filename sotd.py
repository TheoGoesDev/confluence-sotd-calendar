#!/usr/bin/env python3
"""Create Support of the Day (SOTD) calendar events in Confluence Team Calendars."""

import calendar
import itertools
import os
import random
import sys
from datetime import date, datetime, timedelta

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


def month_workdays(year: int, month: int, start_from: date) -> list[date]:
    """Return all Mon–Fri dates in the given month, starting from start_from."""
    first = max(date(year, month, 1), start_from)
    last_day = calendar.monthrange(year, month)[1]
    result = []
    for day in range(first.day, last_day + 1):
        d = date(year, month, day)
        if d.weekday() < 5:
            result.append(d)
    return result


def assign_engineers(days: list[date], engineers: list[str]) -> list[tuple[date, str]]:
    """Assign engineers to days, shuffling the rotation each week for fairness."""
    assignments = []
    week_days: list[date] = []
    current_week = None

    for d in days:
        week = d.isocalendar()[:2]  # (year, week_number)
        if week != current_week:
            if week_days:
                rng = random.Random(f"{current_week[0]}-W{current_week[1]}")
                shuffled = list(engineers)
                rng.shuffle(shuffled)
                assignments.extend(zip(week_days, itertools.cycle(shuffled)))
            week_days = []
            current_week = week
        week_days.append(d)

    if week_days:
        rng = random.Random(f"{current_week[0]}-W{current_week[1]}")
        shuffled = list(engineers)
        rng.shuffle(shuffled)
        assignments.extend(zip(week_days, itertools.cycle(shuffled)))

    return assignments


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
@click.option("--engineers", required=True, help="Comma-separated list of engineer names.")
@click.option(
    "--month",
    default=None,
    help="Target month in YYYY-MM format (default: current month).",
)
@click.option(
    "--dry-run", is_flag=True, default=False, help="Preview schedule without creating events."
)
def main(engineers: str, month: str | None, dry_run: bool) -> None:
    """Create SOTD calendar events in Confluence for a round-robin engineer rotation."""
    today = date.today()
    tomorrow = today + timedelta(days=1)

    if month:
        try:
            parsed = datetime.strptime(month, "%Y-%m")
            target_year, target_month = parsed.year, parsed.month
        except ValueError:
            click.echo(f"Error: invalid month format '{month}', expected YYYY-MM.", err=True)
            sys.exit(1)
    else:
        target_year, target_month = tomorrow.year, tomorrow.month

    # Determine start date within the target month
    if (target_year, target_month) < (today.year, today.month):
        click.echo(
            f"Error: cannot schedule events for a past month ({target_year}-{target_month:02d}).",
            err=True,
        )
        sys.exit(1)
    elif (target_year, target_month) == (today.year, today.month):
        start_from = tomorrow
    else:
        start_from = date(target_year, target_month, 1)

    engineer_list = [e.strip() for e in engineers.split(",") if e.strip()]
    if not engineer_list:
        click.echo("Error: no engineers provided.", err=True)
        sys.exit(1)

    days = month_workdays(target_year, target_month, start_from)
    if not days:
        click.echo(f"No workdays remaining in {target_year}-{target_month:02d}.")
        sys.exit(0)

    assignments = assign_engineers(days, engineer_list)

    click.echo(f"\nScheduling {len(assignments)} SOTD events from {days[0]} to {days[-1]}:\n")
    click.echo(f"  {'Date':<20} {'Day':<6}{'Engineer'}")
    click.echo(f"  {'-' * 20} {'-' * 5} {'-' * 20}")
    for d, eng in assignments:
        click.echo(f"  {str(d):<20} {d.strftime('%a'):<6}{eng}")

    click.echo()
    if dry_run:
        click.echo("Dry run complete. No events created.")
        sys.exit(0)

    config = load_config()

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
