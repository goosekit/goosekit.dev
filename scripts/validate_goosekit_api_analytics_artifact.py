#!/usr/bin/env python3
"""Validate a saved Goosekit API analytics artifact."""
from __future__ import annotations

import argparse
import glob
import json
import re
from pathlib import Path
from typing import Any


REQUIRED_DECISION_KEYS = {
    "recommended_action",
    "reason",
    "export_source",
    "window",
    "mailbox_packets",
    "mailbox_check",
    "counters",
    "maps",
    "ledger_rule",
}
VALID_ACTIONS = {
    "repair_instrumentation_first",
    "score_inbound_packet",
    "check_mailbox_before_lead",
    "investigate_mailto_completion",
    "inspect_builder_completion_friction",
    "inspect_builder_start_friction",
    "inspect_builder_field_burden",
    "inspect_builder_navigation",
    "inspect_workflow_cta_path",
    "inspect_docs_to_production_bridge",
    "no_lead_update",
}
VALID_LEDGER_RULES = {
    "score_actual_inbound_before_lead_or_offer",
    "do_not_update_counters_from_analytics_alone",
}
REQUIRED_COUNTERS = {
    "api_events",
    "builder_clicks",
    "builder_views",
    "builder_starts",
    "completed_packets",
    "packet_copies",
    "mail_clicks",
    "complete_mail_clicks",
    "mailbox_packets",
    "api_events_missing_product",
    "api_events_missing_location",
}
REQUIRED_MAPS = {
    "missing_required_fields",
    "missing_fields_by_start_source",
    "start_sources",
    "completion_sources",
    "packet_copy_sources",
    "mail_click_sources",
    "builder_refs",
    "locations",
    "endpoints",
}


def extract_decision(markdown: str) -> dict[str, Any]:
    match = re.search(
        r"## Machine decision JSON\s+```json\s*(\{.*?\})\s*```",
        markdown,
        flags=re.DOTALL,
    )
    if not match:
        raise ValueError("missing Machine decision JSON block")
    try:
        parsed = json.loads(match.group(1))
    except json.JSONDecodeError as exc:
        raise ValueError(f"invalid Machine decision JSON: {exc}") from exc
    if not isinstance(parsed, dict):
        raise ValueError("Machine decision JSON must be an object")
    return parsed


def validate_counter_map(name: str, value: Any, failures: list[str]) -> None:
    if not isinstance(value, dict):
        failures.append(f"{name} must be an object")
        return
    for key, count in value.items():
        if not isinstance(key, str) or not key:
            failures.append(f"{name} keys must be non-empty strings")
        if isinstance(count, dict):
            validate_counter_map(f"{name}.{key}", count, failures)
        elif not isinstance(count, int) or count < 0:
            failures.append(f"{name}.{key} must be a non-negative integer")


def validate_decision(decision: dict[str, Any]) -> list[str]:
    failures: list[str] = []
    missing = sorted(REQUIRED_DECISION_KEYS - decision.keys())
    if missing:
        failures.append("missing decision keys: " + ", ".join(missing))

    action = decision.get("recommended_action")
    if action not in VALID_ACTIONS:
        failures.append(f"invalid recommended_action: {action!r}")

    ledger_rule = decision.get("ledger_rule")
    if ledger_rule not in VALID_LEDGER_RULES:
        failures.append(f"invalid ledger_rule: {ledger_rule!r}")

    for key in ("export_source", "window", "mailbox_check", "reason"):
        value = decision.get(key)
        if not isinstance(value, str) or not value.strip() or value == "not recorded":
            failures.append(f"{key} is missing or not recorded")

    mailbox_packets = decision.get("mailbox_packets")
    if not isinstance(mailbox_packets, int) or mailbox_packets < 0:
        failures.append("mailbox_packets must be a non-negative integer")

    counters = decision.get("counters")
    if not isinstance(counters, dict):
        failures.append("counters must be an object")
    else:
        missing_counters = sorted(REQUIRED_COUNTERS - counters.keys())
        if missing_counters:
            failures.append("missing counters: " + ", ".join(missing_counters))
        for key, value in counters.items():
            if not isinstance(value, int) or value < 0:
                failures.append(f"counters.{key} must be a non-negative integer")

    maps = decision.get("maps")
    if not isinstance(maps, dict):
        failures.append("maps must be an object")
    else:
        missing_maps = sorted(REQUIRED_MAPS - maps.keys())
        if missing_maps:
            failures.append("missing maps: " + ", ".join(missing_maps))
        for key, value in maps.items():
            validate_counter_map(f"maps.{key}", value, failures)

    if action == "score_inbound_packet":
        if mailbox_packets == 0:
            failures.append("score_inbound_packet requires at least one mailbox packet")
        if ledger_rule != "score_actual_inbound_before_lead_or_offer":
            failures.append("score_inbound_packet requires score_actual_inbound_before_lead_or_offer")
    elif ledger_rule != "do_not_update_counters_from_analytics_alone":
        failures.append("non-scoring actions must not allow ledger updates from analytics alone")

    if isinstance(counters, dict) and isinstance(mailbox_packets, int):
        counter_mailbox_packets = counters.get("mailbox_packets")
        if counter_mailbox_packets != mailbox_packets:
            failures.append("mailbox_packets must match counters.mailbox_packets")

    return failures


def validate_artifact(artifact_path: Path) -> tuple[bool, dict[str, Any]]:
    text = artifact_path.read_text(encoding="utf-8", errors="replace")
    try:
        decision = extract_decision(text)
    except ValueError as exc:
        return False, {"valid": False, "artifact": str(artifact_path), "failures": [str(exc)]}

    failures = validate_decision(decision)
    if failures:
        return False, {
            "valid": False,
            "artifact": str(artifact_path),
            "failures": failures,
            "decision": decision,
        }
    return True, {
        "valid": True,
        "artifact": str(artifact_path),
        "recommended_action": decision["recommended_action"],
        "ledger_rule": decision["ledger_rule"],
        "mailbox_packets": decision["mailbox_packets"],
        "window": decision["window"],
        "decision": decision,
    }


def expand_artifacts(patterns: list[str]) -> tuple[list[Path], list[str]]:
    paths: list[Path] = []
    failures: list[str] = []
    for pattern in patterns:
        if any(char in pattern for char in "*?["):
            matches = sorted(glob.glob(pattern))
            if not matches:
                failures.append(f"no artifacts matched pattern: {pattern}")
                continue
            paths.extend(Path(match) for match in matches)
            continue
        path = Path(pattern)
        if not path.exists():
            failures.append(f"artifact does not exist: {pattern}")
            continue
        paths.append(path)
    return paths, failures


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate Goosekit API analytics artifacts")
    parser.add_argument("artifacts", nargs="+", help="Path(s) to saved Goosekit API analytics artifacts")
    parser.add_argument("--json", action="store_true", help="Print machine-readable validation result")
    args = parser.parse_args()

    artifact_paths, expansion_failures = expand_artifacts(args.artifacts)
    results = [validate_artifact(artifact) for artifact in artifact_paths]
    all_valid = all(valid for valid, _result in results) and not expansion_failures
    result_objects = [result for _valid, result in results]
    result_objects.extend(
        {"valid": False, "artifact": pattern, "failures": [pattern]}
        for pattern in expansion_failures
    )

    if args.json:
        payload: dict[str, Any] = {
            "valid": all_valid,
            "artifact_count": len(result_objects),
            "artifacts": result_objects,
        }
        if len(result_objects) == 1:
            payload.update(result_objects[0])
        print(json.dumps(payload, indent=2, sort_keys=True))
        return 0 if all_valid else 1

    for valid, result in results:
        artifact_path = result["artifact"]
        if valid:
            print(f"GOOSEKIT_API_ANALYTICS_ARTIFACT_OK {artifact_path}")
            print(f"recommended_action={result['recommended_action']}")
            print(f"ledger_rule={result['ledger_rule']}")
            print(f"mailbox_packets={result['mailbox_packets']}")
            print(f"window={result['window']}")
        else:
            print(f"GOOSEKIT_API_ANALYTICS_ARTIFACT_INVALID {artifact_path}")
            for failure in result["failures"]:
                print(f"- {failure}")
    for failure in expansion_failures:
        print("GOOSEKIT_API_ANALYTICS_ARTIFACT_INVALID pattern")
        print(f"- {failure}")

    if all_valid and result_objects:
        print(f"GOOSEKIT_API_ANALYTICS_ARTIFACTS_OK count={len(result_objects)}")
    else:
        print(f"GOOSEKIT_API_ANALYTICS_ARTIFACTS_INVALID count={len(result_objects)}")
    return 0 if all_valid else 1


if __name__ == "__main__":
    raise SystemExit(main())
