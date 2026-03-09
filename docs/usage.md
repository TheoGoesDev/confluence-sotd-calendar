# Usage

## Basic command

```bash
python sotd.py --engineers alice,bob,carol
```

This schedules the remaining workdays in the current month, starting from tomorrow.

## Options

| Option | Required | Description |
|--------|----------|-------------|
| `--engineers` | Yes | Comma-separated engineer names for the rotation |
| `--month` | No | Target month in `YYYY-MM` format (default: current month) |
| `--dry-run` | No | Preview the schedule without creating events |

## Examples

Schedule the current month:

```bash
python sotd.py --engineers theo,hari,olivier
```

Schedule a specific future month:

```bash
python sotd.py --engineers theo,hari,olivier --month 2026-04
```

Preview without creating events:

```bash
python sotd.py --engineers theo,hari,olivier --month 2026-04 --dry-run
```

Output:

```
Scheduling 22 SOTD events from 2026-04-01 to 2026-04-30:

  Date                 Day   Engineer
  -------------------- ----- --------------------
  2026-04-01           Wed   hari
  2026-04-02           Thu   theo
  2026-04-03           Fri   olivier
  ...

Dry run complete. No events created.
```

## Notes

- Weekends are automatically skipped.
- When no `--month` is given, the current month is used and scheduling starts from tomorrow.
- When a future month is specified, all workdays in that month are scheduled.
- The engineer rotation is shuffled each week for fairness, but the shuffle is deterministic (same input always produces the same schedule).
- Events are created as all-day events titled `"SOTD: <engineer_name>"`.
- The script exits with code `1` if any events fail to create.
