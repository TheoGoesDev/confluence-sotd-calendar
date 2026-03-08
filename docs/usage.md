# Usage

## Basic command

```bash
python sotd.py --number-of-days 30 --engineers alice,bob,carol
```

## Options

| Option | Required | Description |
|--------|----------|-------------|
| `--number-of-days` | Yes | Number of calendar days to scan for workdays |
| `--engineers` | Yes | Comma-separated engineer names for the rotation |
| `--start-date` | No | Start date in `YYYY-MM-DD` format (default: tomorrow) |

## Example

```bash
python sotd.py \
  --number-of-days 10 \
  --engineers theo,hari,olivier \
  --start-date 2026-04-01
```

Output:

```
Scheduling 8 SOTD events from 2026-04-01 to 2026-04-10:

  Date                 Engineer
  -------------------- --------------------
  2026-04-01           theo
  2026-04-02           hari
  ...

Create these events in Confluence? [y/N]:
```

Confirm with `y` to create events. Each event is reported as `[OK]` or `[FAIL]` with the HTTP status on failure.

## Notes

- Weekends are automatically skipped; `--number-of-days` counts calendar days, not workdays.
- Events are created as all-day events titled `"SOTD: <engineer_name>"`.
- The script exits with code `1` if any events fail to create.
