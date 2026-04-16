#!/usr/bin/env python3
import json, subprocess, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = Path('/Users/arthurpierrey/.openclaw/workspace/golden-goose/scripts/goosekit_cloudflare_visitors.sh')
PUBLIC = ROOT / 'stats' / 'visitors.json'
STATE = ROOT / 'stats' / 'visitors-state.json'

DEFAULT_COUNT = 3475

raw = subprocess.check_output([str(SCRIPT)], text=True)
vals = {}
for line in raw.splitlines():
    if '=' in line:
        k, v = line.strip().split('=', 1)
        vals[k] = v

today_date = vals.get('today_utc.date')
yesterday_date = vals.get('yesterday_utc.date')
today_uniques = int(vals.get('today_utc.uniques', '0') or '0')
yesterday_uniques = int(vals.get('yesterday_utc.uniques', '0') or '0')

if STATE.exists():
    state = json.loads(STATE.read_text())
else:
    base = DEFAULT_COUNT
    if PUBLIC.exists():
        try:
            base = int(json.loads(PUBLIC.read_text()).get('count', DEFAULT_COUNT))
        except Exception:
            pass
    state = {
        'displayCount': base,
        'sourceDate': today_date,
        'sourceUniques': today_uniques,
    }

if state.get('sourceDate') == today_date:
    delta = max(0, today_uniques - int(state.get('sourceUniques', 0) or 0))
    state['displayCount'] = int(state.get('displayCount', DEFAULT_COUNT)) + delta
    state['sourceUniques'] = today_uniques
else:
    if state.get('sourceDate') == yesterday_date:
        delta = max(0, yesterday_uniques - int(state.get('sourceUniques', 0) or 0))
        state['displayCount'] = int(state.get('displayCount', DEFAULT_COUNT)) + delta
    state['sourceDate'] = today_date
    state['sourceUniques'] = today_uniques

updated_at = datetime.datetime.utcnow().replace(microsecond=0).isoformat() + 'Z'
public = {
    'count': int(state['displayCount']),
    'updatedAt': updated_at,
    'sourceDate': state['sourceDate'],
    'sourceUniques': int(state['sourceUniques']),
}
STATE.write_text(json.dumps(state, indent=2) + "\n")
PUBLIC.write_text(json.dumps(public, indent=2) + "\n")
print(json.dumps(public))
