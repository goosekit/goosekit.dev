#!/usr/bin/env python3
"""Summarize Goosekit API PostHog exports into conservative operator signals.

This script reads a CSV/JSON export from PostHog. It does not call PostHog and
it never turns clicks into leads by itself.
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
from collections import Counter
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable


PRODUCT = "goosekit_api"
API_EVENTS = {
    "goosekit_api_free_docs_clicked",
    "goosekit_api_tool_page_clicked",
    "goosekit_api_workflow_guide_clicked",
    "goosekit_api_production_request_builder_clicked",
    "goosekit_api_production_request_builder_viewed",
    "goosekit_api_production_request_completed",
    "goosekit_api_packet_copied",
    "goosekit_api_production_access_clicked",
}
BUILDER_REFS = {
    "pricing_production",
    "production_note",
    "production_request_packet",
    "rate_limits",
    "json_formatter_api_production_packet",
    "hash_generator_api_production_packet",
    "uuid_generator_api_production_packet",
    "password_generator_api_production_packet",
}


@dataclass
class Event:
    name: str
    timestamp: str
    product: str
    location: str
    endpoint: str
    ref: str
    complete: str
    required_fields_filled: str
    target_href: str


def parse_properties(value: Any) -> dict[str, Any]:
    if isinstance(value, dict):
        return value
    if not value or not isinstance(value, str):
        return {}
    try:
        parsed = json.loads(value)
    except json.JSONDecodeError:
        return {}
    return parsed if isinstance(parsed, dict) else {}


def first(row: dict[str, Any], names: Iterable[str], default: str = "") -> str:
    for name in names:
        value = row.get(name)
        if value is not None and str(value) != "":
            return str(value)
    return default


def event_from_row(row: dict[str, Any]) -> Event:
    props = parse_properties(row.get("properties") or row.get("Properties") or row.get("$properties"))

    def prop(*names: str) -> str:
        return first(props, names)

    return Event(
        name=first(row, ("event", "Event", "event_name", "Event Name", "$event")),
        timestamp=first(row, ("timestamp", "Timestamp", "time", "created_at", "Created At")),
        product=prop("product"),
        location=prop("location"),
        endpoint=prop("endpoint"),
        ref=prop("ref"),
        complete=prop("complete"),
        required_fields_filled=prop("required_fields_filled"),
        target_href=prop("target_href", "href", "$current_url"),
    )


def load_json(text: str) -> list[dict[str, Any]]:
    data = json.loads(text)
    if isinstance(data, list):
        return [item for item in data if isinstance(item, dict)]
    if isinstance(data, dict):
        for key in ("results", "events", "data"):
            value = data.get(key)
            if isinstance(value, list):
                return [item for item in value if isinstance(item, dict)]
    raise ValueError("JSON input must be a list or contain results/events/data list")


def load_events(input_path: Path | None, fmt: str) -> list[Event]:
    text = input_path.read_text(encoding="utf-8", errors="replace") if input_path else sys.stdin.read()
    if not text.strip():
        return []
    if fmt == "json" or (fmt == "auto" and text.lstrip().startswith(("{", "["))):
        rows = load_json(text)
    else:
        rows = list(csv.DictReader(text.splitlines()))
    return [event_from_row(row) for row in rows]


def is_complete(value: str) -> bool:
    return value.lower() == "true"


def build_summary(events: list[Event], mailbox_packets: int) -> dict[str, Any]:
    api_events = [event for event in events if event.product == PRODUCT or event.name in API_EVENTS]
    counts = Counter(event.name for event in api_events)
    locations = Counter(event.location for event in api_events if event.location)
    endpoints = Counter(event.endpoint for event in api_events if event.endpoint)
    refs = Counter(event.ref for event in api_events if event.ref)

    builder_clicks = counts["goosekit_api_production_request_builder_clicked"]
    builder_views = counts["goosekit_api_production_request_builder_viewed"]
    completed = counts["goosekit_api_production_request_completed"]
    packet_copies = counts["goosekit_api_packet_copied"]
    mail_clicks = counts["goosekit_api_production_access_clicked"]
    complete_mail_clicks = sum(
        1 for event in api_events if event.name == "goosekit_api_production_access_clicked" and is_complete(event.complete)
    )
    incomplete_mail_clicks = mail_clicks - complete_mail_clicks
    missing_product = sum(1 for event in api_events if event.name in API_EVENTS and not event.product)
    missing_location = sum(1 for event in api_events if event.name in API_EVENTS and not event.location)

    if missing_product or missing_location:
        action = "repair_instrumentation_first"
        reason = "api_intent_events_missing_product_or_location"
    elif mailbox_packets > 0:
        action = "score_inbound_packet"
        reason = "real_mailbox_packet_present"
    elif complete_mail_clicks or packet_copies:
        action = "check_mailbox_before_lead"
        reason = "complete_or_copied_packet_without_mailbox_packet"
    elif mail_clicks:
        action = "investigate_mailto_completion"
        reason = "mail_click_without_complete_packet_or_mailbox_packet"
    elif builder_views and not completed:
        action = "inspect_builder_field_burden"
        reason = "builder_views_without_completed_packets"
    elif builder_clicks and not builder_views:
        action = "inspect_builder_navigation"
        reason = "builder_clicks_without_builder_views"
    else:
        action = "no_lead_update"
        reason = "no_api_paid_intent_signal"

    return {
        "events_total": len(events),
        "api_events": len(api_events),
        "builder_clicks": builder_clicks,
        "builder_views": builder_views,
        "completed_packets": completed,
        "packet_copies": packet_copies,
        "mail_clicks": mail_clicks,
        "complete_mail_clicks": complete_mail_clicks,
        "incomplete_mail_clicks": incomplete_mail_clicks,
        "mailbox_packets": mailbox_packets,
        "api_events_missing_product": missing_product,
        "api_events_missing_location": missing_location,
        "recommended_action": action,
        "reason": reason,
        "builder_refs": dict(sorted(refs.items())),
        "locations": dict(locations.most_common(20)),
        "endpoints": dict(endpoints.most_common(20)),
        "do_not_update_counters_from_analytics_alone": True,
    }


def format_markdown(summary: dict[str, Any], *, export_source: str, window: str, mailbox_check: str) -> str:
    lines = [
        "# Goosekit API event summary",
        "",
        f"export_source={export_source}",
        f"window={window}",
        f"mailbox_check={mailbox_check}",
        f"events_total={summary['events_total']}",
        f"api_events={summary['api_events']}",
        f"builder_clicks={summary['builder_clicks']}",
        f"builder_views={summary['builder_views']}",
        f"completed_packets={summary['completed_packets']}",
        f"packet_copies={summary['packet_copies']}",
        f"mail_clicks={summary['mail_clicks']}",
        f"complete_mail_clicks={summary['complete_mail_clicks']}",
        f"incomplete_mail_clicks={summary['incomplete_mail_clicks']}",
        f"mailbox_packets={summary['mailbox_packets']}",
        f"api_events_missing_product={summary['api_events_missing_product']}",
        f"api_events_missing_location={summary['api_events_missing_location']}",
        f"recommended_action={summary['recommended_action']}",
        f"reason={summary['reason']}",
        "",
        "## Builder refs",
    ]
    builder_refs = summary["builder_refs"]
    for ref in sorted(BUILDER_REFS | set(builder_refs)):
        if builder_refs.get(ref):
            lines.append(f"- {ref}: {builder_refs[ref]}")
    lines.append("")
    lines.append("## Locations")
    for location, count in summary["locations"].items():
        lines.append(f"- {location}: {count}")
    lines.append("")
    lines.append("## Endpoints")
    for endpoint, count in summary["endpoints"].items():
        lines.append(f"- {endpoint}: {count}")
    lines.append("")
    lines.append("Do not update lead, revenue, or MRR counters from this summary alone.")
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Summarize Goosekit API PostHog export")
    parser.add_argument("export", nargs="?", help="CSV/JSON export path; defaults to stdin")
    parser.add_argument("--format", choices=("auto", "csv", "json"), default="auto")
    parser.add_argument("--mailbox-packets", type=int, default=0)
    parser.add_argument("--window", default="", help="Export/mailbox window, e.g. 2026-06-18T07:00Z..08:00Z")
    parser.add_argument("--mailbox-check", default="", help="Human-readable note confirming mailbox check for the same window")
    parser.add_argument("--json", action="store_true", help="Emit machine-readable JSON instead of markdown")
    parser.add_argument("--output-dir", help="Write timestamped markdown artifact to this directory")
    args = parser.parse_args()
    if args.mailbox_packets < 0:
        parser.error("--mailbox-packets must be 0 or greater")
    if args.output_dir and (not args.window or not args.mailbox_check):
        parser.error("--output-dir requires --window and --mailbox-check")
    events = load_events(Path(args.export) if args.export else None, args.format)
    export_source = args.export or "stdin"
    summary = build_summary(events, args.mailbox_packets)
    summary.update(
        {
            "export_source": export_source,
            "window": args.window,
            "mailbox_check": args.mailbox_check,
        }
    )
    if args.json:
        print(json.dumps(summary, indent=2, sort_keys=True))
    else:
        markdown = format_markdown(
            summary,
            export_source=export_source,
            window=args.window,
            mailbox_check=args.mailbox_check,
        )
        if args.output_dir:
            output_dir = Path(args.output_dir)
            output_dir.mkdir(parents=True, exist_ok=True)
            stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
            output_path = output_dir / f"GOOSEKIT_API_ANALYTICS_SUMMARY_{stamp}.md"
            output_path.write_text(markdown, encoding="utf-8")
            print(output_path)
        else:
            print(markdown, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
