# Setup

## Prerequisites

- Python ≥3.11
- [uv](https://docs.astral.sh/uv/) installed
- A Confluence Cloud account with Team Calendars

## Install dependencies

```bash
uv sync
```

## Configure credentials

Copy `.env.example` to `.env` and fill in each value:

```
CONFLUENCE_URL=https://yourcompany.atlassian.net
CONFLUENCE_EMAIL=you@example.com
CONFLUENCE_API_TOKEN=your_api_token_here
CONFLUENCE_CALENDAR_ID=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
```

### Atlassian API token

Generate one at: **Atlassian account settings → Security → API tokens**

### Calendar ID

The `CONFLUENCE_CALENDAR_ID` is the UUID of the Team Calendar sub-calendar where events will be created. To find it:

1. Open the Team Calendars page in Confluence.
2. Click **"…"** next to the calendar name → **"Copy CalDAV URL"**.
3. The UUID in the URL is your calendar ID.

Alternatively, open browser dev tools and watch network requests while the calendar loads — the UUID appears in API calls to `/rest/calendar-services/`.
