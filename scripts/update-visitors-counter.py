#!/usr/bin/env python3
import datetime
import json
import os
import subprocess
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / 'stats' / 'visitors.json'
STATE = ROOT / 'stats' / 'visitors-state.json'
DEFAULT_COUNT = 3475
ZONE_TAG = os.environ.get('ZONE_TAG', '76eefb78a7d47ea40f34b6768fa2cf05')
TOKEN_FILE = Path(os.environ.get('TOKEN_FILE', str(Path.home() / '.config/goosekit/cf-analytics-token')))
SCRIPT_CANDIDATES = [
    Path(os.environ['GOOSEKIT_CF_VISITORS_SCRIPT']) if os.environ.get('GOOSEKIT_CF_VISITORS_SCRIPT') else None,
    Path.home() / '.openclaw/workspace/golden-goose/scripts/goosekit_cloudflare_visitors.sh',
    Path('/home/openclaw/.openclaw/workspace/golden-goose/scripts/goosekit_cloudflare_visitors.sh'),
    Path('/Users/arthurpierrey/.openclaw/workspace/golden-goose/scripts/goosekit_cloudflare_visitors.sh'),
]

def utc_today():
    return datetime.datetime.now(datetime.UTC).date()

def parse_helper_output(raw):
    vals = {}
    for line in raw.splitlines():
        if '=' in line:
            k, v = line.strip().split('=', 1)
            vals[k] = v
    return vals

def helper_metrics():
    for script in SCRIPT_CANDIDATES:
        if script and script.exists() and os.access(script, os.X_OK):
            raw = subprocess.check_output([str(script)], text=True)
            vals = parse_helper_output(raw)
            return {
                vals.get('yesterday_utc.date'): int(vals.get('yesterday_utc.uniques', '0') or '0'),
                vals.get('today_utc.date'): int(vals.get('today_utc.uniques', '0') or '0'),
            }
    raise FileNotFoundError('No executable goosekit_cloudflare_visitors.sh found')

def cloudflare_daily_uniques(start_date, end_date_exclusive):
    if not TOKEN_FILE.exists():
        # Fall back to the helper for normal yesterday/today refreshes.
        return helper_metrics()
    token = TOKEN_FILE.read_text().strip()
    query = '''query($zoneTag: String!, $start: Time!, $end: Time!) {
      viewer {
        zones(filter: { zoneTag: $zoneTag }) {
          httpRequests1dGroups(limit: 100, filter: { date_geq: $start, date_lt: $end }) {
            dimensions { date }
            uniq { uniques }
          }
        }
      }
    }'''
    payload = json.dumps({
        'query': query,
        'variables': {
            'zoneTag': ZONE_TAG,
            'start': start_date.isoformat(),
            'end': end_date_exclusive.isoformat(),
        },
    }).encode()
    req = urllib.request.Request(
        'https://api.cloudflare.com/client/v4/graphql',
        data=payload,
        headers={'Authorization': 'Bearer ' + token, 'Content-Type': 'application/json'},
    )
    with urllib.request.urlopen(req, timeout=25) as res:
        resp = json.loads(res.read())
    if resp.get('errors'):
        raise RuntimeError(json.dumps(resp, indent=2))
    rows = resp['data']['viewer']['zones'][0]['httpRequests1dGroups']
    return {
        row['dimensions']['date']: int(row.get('uniq', {}).get('uniques') or 0)
        for row in rows
    }

def load_state(today_iso):
    if STATE.exists():
        return json.loads(STATE.read_text())
    base = DEFAULT_COUNT
    if PUBLIC.exists():
        try:
            base = int(json.loads(PUBLIC.read_text()).get('count', DEFAULT_COUNT))
        except Exception:
            pass
    return {'displayCount': base, 'sourceDate': today_iso, 'sourceUniques': 0}

today = utc_today()
tomorrow = today + datetime.timedelta(days=1)
state = load_state(today.isoformat())
source_date = datetime.date.fromisoformat(state.get('sourceDate') or today.isoformat())
source_uniques = int(state.get('sourceUniques', 0) or 0)
display_count = int(state.get('displayCount', DEFAULT_COUNT))

# Reconcile from the last recorded source date through today. This keeps the
# public counter correct even if the daily cron was disabled for several days.
metrics = cloudflare_daily_uniques(source_date, tomorrow)
for day in (source_date + datetime.timedelta(days=i) for i in range((today - source_date).days + 1)):
    day_iso = day.isoformat()
    uniques = int(metrics.get(day_iso, 0) or 0)
    baseline = source_uniques if day == source_date else 0
    display_count += max(0, uniques - baseline)

state = {
    'displayCount': display_count,
    'sourceDate': today.isoformat(),
    'sourceUniques': int(metrics.get(today.isoformat(), 0) or 0),
}
updated_at = datetime.datetime.now(datetime.UTC).replace(microsecond=0).isoformat().replace('+00:00', 'Z')
public = {
    'count': int(state['displayCount']),
    'updatedAt': updated_at,
    'sourceDate': state['sourceDate'],
    'sourceUniques': int(state['sourceUniques']),
}
STATE.parent.mkdir(parents=True, exist_ok=True)
STATE.write_text(json.dumps(state, indent=2) + '\n')
PUBLIC.write_text(json.dumps(public, indent=2) + '\n')
print(json.dumps(public))
