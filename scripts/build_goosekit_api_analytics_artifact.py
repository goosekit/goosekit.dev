#!/usr/bin/env python3
"""Build a durable Goosekit API analytics artifact from a PostHog export.

This wraps the API export summarizer with run context and a machine-readable
decision block. It never updates lead, revenue, or MRR counters.
"""
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

from summarize_goosekit_api_events import build_summary, format_markdown, load_events


COUNTER_KEYS = (
    "events_total",
    "api_events",
    "builder_clicks",
    "endpoint_production_clicks",
    "free_docs_clicks",
    "api_workflow_page_views",
    "builder_views",
    "endpoint_example_views",
    "volume_example_clicks",
    "runtime_example_clicks",
    "specifics_example_clicks",
    "commercial_example_clicks",
    "budget_example_clicks",
    "failure_example_clicks",
    "builder_starts",
    "completed_packets",
    "packet_copies",
    "mail_clicks",
    "complete_mail_clicks",
    "incomplete_mail_clicks",
    "mailbox_packets",
    "api_events_missing_product",
    "api_events_missing_location",
)
MAP_KEYS = (
    "missing_required_fields",
    "missing_fields_by_start_source",
    "endpoint_example_views_by_endpoint",
    "volume_example_choices",
    "runtime_example_choices",
    "specifics_example_choices",
    "commercial_example_choices",
    "budget_example_choices",
    "failure_example_choices",
    "first_fields",
    "start_sources",
    "completion_sources",
    "packet_copy_sources",
    "mail_click_sources",
    "builder_refs",
    "workflow_page_views",
    "locations",
    "endpoints",
)


def build_artifact(
    input_path: Path | None,
    fmt: str,
    mailbox_packets: int,
    window: str,
    mailbox_check: str,
) -> str:
    events = load_events(input_path, fmt)
    export_source = str(input_path) if input_path else "stdin"
    summary = build_summary(events, mailbox_packets)
    summary.update(
        {
            "export_source": export_source,
            "window": window,
            "mailbox_check": mailbox_check,
        }
    )
    markdown_summary = format_markdown(
        summary,
        export_source=export_source,
        window=window,
        mailbox_check=mailbox_check,
    ).rstrip()
    decision = {
        "recommended_action": summary["recommended_action"],
        "reason": summary["reason"],
        "export_source": export_source,
        "window": window,
        "mailbox_packets": mailbox_packets,
        "mailbox_check": mailbox_check,
        "counters": {key: summary.get(key, 0) for key in COUNTER_KEYS},
        "maps": {key: summary.get(key, {}) for key in MAP_KEYS},
        "ledger_rule": (
            "score_actual_inbound_before_lead_or_offer"
            if summary["recommended_action"] == "score_inbound_packet"
            else "do_not_update_counters_from_analytics_alone"
        ),
    }
    return "\n".join(
        [
            "# Goosekit API analytics artifact",
            "",
            "## Run context",
            "",
            f"- Export source: {export_source}",
            f"- Window: {window}",
            f"- Mailbox packets checked: {mailbox_packets}",
            f"- Mailbox check note: {mailbox_check}",
            "",
            markdown_summary,
            "",
            "## Machine decision JSON",
            "",
            "```json",
            json.dumps(decision, indent=2, sort_keys=True),
            "```",
            "",
            "## Ledger reminder",
            "",
            "- Do not update send/lead/revenue/MRR counters unless there is a real email, buyer reply, paid checkout, paid fix, or MRR row.",
        ]
    )


def default_output_path(output_dir: Path, now: datetime | None = None) -> Path:
    timestamp = (now or datetime.now(timezone.utc)).strftime("%Y-%m-%d_%H%M")
    return output_dir / f"GOOSEKIT_API_ANALYTICS_ARTIFACT_{timestamp}.md"


def main() -> int:
    parser = argparse.ArgumentParser(description="Build a Goosekit API analytics artifact")
    parser.add_argument("input", nargs="?", help="CSV/JSON export path; defaults to stdin")
    parser.add_argument("--format", choices=("auto", "csv", "json"), default="auto")
    parser.add_argument("--mailbox-packets", type=int, default=0)
    parser.add_argument(
        "--window",
        default="not recorded",
        help="Human-readable export/mailbox window, e.g. 2026-06-19T08:00Z..2026-06-19T09:00Z",
    )
    parser.add_argument(
        "--mailbox-check",
        default="not recorded",
        help="Human-readable mailbox verification note for the same window",
    )
    parser.add_argument("--output", help="Write artifact to this path instead of stdout")
    parser.add_argument("--output-dir", help="Write artifact to this directory using a UTC timestamped filename")
    parser.add_argument("--overwrite", action="store_true", help="Allow overwriting an existing artifact path")
    args = parser.parse_args()

    if args.mailbox_packets < 0:
        parser.error("--mailbox-packets must be 0 or greater")
    if (args.output or args.output_dir) and args.window == "not recorded":
        parser.error("--window is required when saving an artifact")
    if (args.output or args.output_dir) and args.mailbox_check == "not recorded":
        parser.error("--mailbox-check is required when saving an artifact")
    if args.output and args.output_dir:
        parser.error("--output and --output-dir are mutually exclusive")

    artifact = build_artifact(
        Path(args.input) if args.input else None,
        args.format,
        args.mailbox_packets,
        args.window,
        args.mailbox_check,
    )
    output_path: Path | None = None
    if args.output:
        output_path = Path(args.output)
    elif args.output_dir:
        output_path = default_output_path(Path(args.output_dir))

    if output_path:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        if output_path.exists() and not args.overwrite:
            parser.error(f"output already exists: {output_path} (use --overwrite to replace)")
        output_path.write_text(artifact + "\n", encoding="utf-8")
        print(f"wrote={output_path}")
    else:
        print(artifact)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
