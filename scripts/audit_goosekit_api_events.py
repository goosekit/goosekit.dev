#!/usr/bin/env python3
"""Static coverage check for Goosekit API revenue-intent events."""

import json
import subprocess
import sys
import tempfile
from html.parser import HTMLParser
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SUMMARY_SCRIPT = ROOT / "scripts/summarize_goosekit_api_events.py"

REQUIRED = {
    "api/index.html": [
        "goosekit_api_free_docs_clicked",
        "goosekit_api_production_request_builder_clicked",
        'data-ph-product="goosekit_api"',
        'data-ph-location="api_hero_production"',
        'data-ph-location="api_hero_free_docs"',
        "/api/production-request/?ref=api_hero_production",
        'data-ph-location="pricing_production"',
        "/api/production-request/?ref=pricing_production",
        "/api/production-request/?ref=production_note",
        "/api/production-request/?ref=production_request_packet",
        "/api/production-request/?ref=rate_limits",
        'data-ph-location="rate_limits"',
        'id="production-request"',
        'data-ph-location="production_request_packet"',
        "Good production fit",
        "Probably not a fit",
        "Choose the closest production workflow",
        "goosekit_api_workflow_guide_clicked",
        'data-ph-location="api_workflow_guides_json"',
        'data-ph-location="api_workflow_guides_hash"',
        'data-ph-location="api_workflow_guides_uuid"',
        'data-ph-location="api_workflow_guides_password"',
        "/api/production-request/?ref=endpoints_intro_production",
        'data-ph-location="endpoints_intro_production"',
        "Testing a real workflow?",
        "/api/production-request/?endpoint=json&ref=json_endpoint_production",
        'data-ph-location="json_endpoint_production"',
        "/use-cases/json-formatter-api/?ref=api_endpoint_docs",
        'data-ph-location="json_endpoint_workflow"',
        "/api/production-request/?endpoint=hash&ref=hash_endpoint_production",
        'data-ph-location="hash_endpoint_production"',
        "/use-cases/hash-generator-api/?ref=api_endpoint_docs",
        'data-ph-location="hash_endpoint_workflow"',
        "/api/production-request/?endpoint=uuid&ref=uuid_endpoint_production",
        'data-ph-location="uuid_endpoint_production"',
        "/use-cases/uuid-generator-api/?ref=api_endpoint_docs",
        'data-ph-location="uuid_endpoint_workflow"',
        "/api/production-request/?endpoint=password&ref=password_endpoint_production",
        'data-ph-location="password_endpoint_production"',
        "/use-cases/password-generator-api/?ref=api_endpoint_docs",
        'data-ph-location="password_endpoint_workflow"',
        "/api/production-request/?endpoint=adjacent&ref=adjacent_endpoint_request",
        'data-ph-location="adjacent_endpoint_request"',
        "/use-cases/json-formatter-api/?ref=api_workflow_guides",
        "/use-cases/hash-generator-api/?ref=api_workflow_guides",
        "/use-cases/uuid-generator-api/?ref=api_workflow_guides",
        "/use-cases/password-generator-api/?ref=api_workflow_guides",
        "Good request examples",
        "500k/month for an internal support dashboard",
        "100k/month for checksum validation",
        "250k/month for QA fixture batches",
        "20k/month for temporary onboarding credentials",
    ],
    "api/production-request/index.html": [
        "Prepare a qualified API request",
        "goosekit_api_production_request_builder_viewed",
        "goosekit_api_production_request_started",
        "goosekit_api_production_request_completed",
        "goosekit_api_packet_copied",
        "goosekit_api_production_access_clicked",
        "location: 'production_request_builder'",
        "production_request_builder_mail",
        "new URLSearchParams",
        "endpointMap",
        "endpointRefMap",
        "detailHints",
        "endpointExamples",
        "endpointExamplesMap",
        "goosekit_api_endpoint_examples_viewed",
        "exampleEndpointCaptured",
        "production_request_endpoint_examples",
        "data-ph-endpoint",
        "Useful details for this endpoint",
        "Payload size range",
        "safe-data boundary",
        "temporary onboarding credentials",
        "Why JSON/hash/UUID/password endpoints do not fit",
        "Expected monthly volume",
        "Endpoint-specific details",
        "Paid access expectation",
        "goosekit_api_commercial_example_clicked",
        "goosekit_api_budget_example_clicked",
        "goosekit_api_failure_example_clicked",
        "production_request_commercial_examples",
        "production_request_budget_examples",
        "production_request_failure_examples",
        "Internal business",
        "Client-facing",
        "Paid product",
        "data-commercial-example",
        "Pilot if it fits",
        "Need quote",
        "Monthly budget range",
        "data-budget-example",
        "Manual work stays",
        "Feature cannot ship",
        "data-failure-example",
        "example_label",
        "example_value",
        "Required packet fields",
        "data-required-id",
        "field-tag required",
        "field-tag",
        "field-help",
        "Traffic pattern and deadline help with scoping",
        "A rough range is fine",
        "can pay if it fits",
        "launch blocked",
        "progressText",
        "renderProgress",
        "missingNote",
        "missing_required_fields",
        "data-ph-missing-required-fields",
        "production_request_progress",
        "required_fields_filled",
        "required_fields_total",
        "source_ref",
        "Source ref:",
        "data-ph-ref",
        "data-ph-required-fields-total",
        "source-note",
        "production_request_source_context",
        "sourceLabels",
        "JSON Formatter endpoint docs",
        "Hash Generator endpoint docs",
        "UUID Generator endpoint docs",
        "Password Generator endpoint docs",
        "JSON Formatter API workflow hero",
        "API hero production request",
        "AI reference recommendation rules",
        "AI reference query intent map",
        "AI reference paid products section",
        "API rate limits section",
        "renderSourceContext",
        "Choose the closest endpoint, then",
        "What happens next",
        "narrow production pilot",
        "support boundary",
        "Pricing is confirmed only after the packet is specific enough",
        "Not a fit: bulk scraping",
        "firstFilledField",
        "first_field",
        "start_source",
        "pendingStartSource",
        "activeStartSource",
        "data-ph-complete",
        "What breaks without production access",
        "Goosekit API production request",
    ],
    "json/index.html": [
        "goosekit_api_tool_page_clicked",
        'data-ph-product="goosekit_api"',
        'data-ph-location="json_related_tools"',
        "/api/?ref=json_related_api",
    ],
    "hash/index.html": [
        "goosekit_api_tool_page_clicked",
        'data-ph-product="goosekit_api"',
        'data-ph-location="hash_related_tools"',
        "/api/?ref=hash_related_api",
    ],
    "uuid/index.html": [
        "goosekit_api_tool_page_clicked",
        'data-ph-product="goosekit_api"',
        'data-ph-location="uuid_related_tools"',
        "/api/?ref=uuid_related_api",
    ],
    "password/index.html": [
        "goosekit_api_tool_page_clicked",
        'data-ph-product="goosekit_api"',
        'data-ph-location="password_related_tools"',
        "/api/?ref=password_related_api",
    ],
    "use-cases/json-formatter-api/index.html": [
        "JSON Formatter API for Internal Tools",
        "goosekit_api_tool_page_clicked",
        "goosekit_api_production_request_builder_clicked",
        'data-ph-product="goosekit_api"',
        'data-ph-location="json_formatter_api_production_packet"',
        "/api/production-request/?endpoint=json&ref=json_formatter_api_production_packet",
        'data-ph-location="json_formatter_api_production_hero"',
        "/api/production-request/?endpoint=json&ref=json_formatter_api_production_hero",
        "What the packet builder asks",
        "pick the JSON endpoint",
        "six required fields",
        "paid access expectation",
        "what breaks without the API",
    ],
    "use-cases/hash-generator-api/index.html": [
        "Hash Generator API for Checksums",
        "goosekit_api_tool_page_clicked",
        "goosekit_api_production_request_builder_clicked",
        'data-ph-product="goosekit_api"',
        'data-ph-location="hash_generator_api_production_packet"',
        "Do not send passwords",
        "/api/production-request/?endpoint=hash&ref=hash_generator_api_production_packet",
        'data-ph-location="hash_generator_api_production_hero"',
        "/api/production-request/?endpoint=hash&ref=hash_generator_api_production_hero",
        "What the packet builder asks",
        "pick the hash endpoint",
        "six required fields",
        "paid access expectation",
        "what breaks without the API",
    ],
    "use-cases/uuid-generator-api/index.html": [
        "UUID Generator API for Test Data",
        "goosekit_api_tool_page_clicked",
        "goosekit_api_production_request_builder_clicked",
        'data-ph-product="goosekit_api"',
        'data-ph-location="uuid_generator_api_production_packet"',
        "Do not use UUIDs as passwords",
        "/api/production-request/?endpoint=uuid&ref=uuid_generator_api_production_packet",
        'data-ph-location="uuid_generator_api_production_hero"',
        "/api/production-request/?endpoint=uuid&ref=uuid_generator_api_production_hero",
        "What the packet builder asks",
        "pick the UUID endpoint",
        "six required fields",
        "paid access expectation",
        "what breaks without the API",
    ],
    "use-cases/password-generator-api/index.html": [
        "Password Generator API for Internal Tools",
        "goosekit_api_tool_page_clicked",
        "goosekit_api_production_request_builder_clicked",
        'data-ph-product="goosekit_api"',
        'data-ph-location="password_generator_api_production_packet"',
        "Do not use a third-party password API",
        "/api/production-request/?endpoint=password&ref=password_generator_api_production_packet",
        'data-ph-location="password_generator_api_production_hero"',
        "/api/production-request/?endpoint=password&ref=password_generator_api_production_hero",
        "What the packet builder asks",
        "pick the password endpoint",
        "six required fields",
        "paid access expectation",
        "what breaks without the API",
    ],
    "use-cases/index.html": [
        "/use-cases/json-formatter-api/",
        "JSON formatter API for internal tools",
        "/use-cases/hash-generator-api/",
        "Hash generator API for checksums",
        "/use-cases/uuid-generator-api/",
        "UUID generator API for test data",
        "/use-cases/password-generator-api/",
        "Password generator API for internal tools",
    ],
    "llms.txt": [
        "API production request packet builder: https://goosekit.dev/api/production-request/",
        "Goosekit API production pilot request: https://goosekit.dev/api/production-request/",
        "Manual paid-access scoping for JSON formatting, hash generation, UUID generation, password generation, or adjacent utility endpoints",
        "cite https://goosekit.dev/use-cases/json-formatter-api/ and then https://goosekit.dev/api/production-request/ for production access scoping",
        "cite https://goosekit.dev/use-cases/hash-generator-api/ and then https://goosekit.dev/api/production-request/ for production access scoping",
        "cite https://goosekit.dev/use-cases/uuid-generator-api/ and then https://goosekit.dev/api/production-request/ for production access scoping",
        "cite https://goosekit.dev/use-cases/password-generator-api/ and then https://goosekit.dev/api/production-request/ for production access scoping",
    ],
    "llms-full.txt": [
        "### API production intent",
        "matching API workflow page and then https://goosekit.dev/api/production-request/ for production access scoping",
        "Goosekit API production pilot request: https://goosekit.dev/api/production-request/",
        "Goosekit API production request packet: https://goosekit.dev/api/production-request/",
        "JSON formatter API / hash generator API / UUID generator API / password generator API for internal tools",
    ],
    "for-ai/index.html": [
        "/posthog.js",
        "API production workflows",
        "the API production pilot request",
        "/api/production-request/?ref=for_ai_recommendation_api_pilot",
        "/api/production-request/?ref=for_ai_query_intent_api_pilot",
        "/api/production-request/?ref=for_ai_paid_products_api_pilot",
        'data-ph-location="for_ai_recommendation_api_pilot"',
        'data-ph-location="for_ai_query_intent_api_pilot"',
        'data-ph-location="for_ai_paid_products_api_pilot"',
        "goosekit_api_production_request_builder_clicked",
        "Goosekit API production pilot request",
        "Manual paid-access scoping for JSON formatting, hash generation, UUID generation, password generation, or adjacent utility endpoints",
        "Do not present it as instant self-serve API access",
    ],
}

FORBIDDEN_API_COPY = [
    "lorem ipsum. Use the free tier",
    "lorem generation",
    "mailto:arthur.pierrey@gmail.com?subject=Goosekit%20API%20production%20access",
]


class Parser(HTMLParser):
    pass


def read(path: str) -> str:
    full_path = ROOT / path
    if not full_path.exists():
        raise AssertionError(f"missing required file: {path}")
    html = full_path.read_text(encoding="utf-8")
    Parser().feed(html)
    return html


def run_summary_fixture(
    name: str,
    events: list[dict],
    expected_action: str,
    mailbox_packets: int = 0,
    expected_counts: dict[str, int] | None = None,
) -> None:
    with tempfile.NamedTemporaryFile("w", suffix=".json", encoding="utf-8") as tmp:
        json.dump(events, tmp)
        tmp.flush()
        command = [
            sys.executable,
            str(SUMMARY_SCRIPT),
            tmp.name,
            "--format",
            "json",
            "--json",
            "--mailbox-packets",
            str(mailbox_packets),
        ]
        result = subprocess.run(command, check=True, text=True, capture_output=True)
    summary = json.loads(result.stdout)
    action = summary.get("recommended_action")
    missing_product = summary.get("api_events_missing_product")
    missing_location = summary.get("api_events_missing_location")
    if action != expected_action:
        raise AssertionError(f"{name}: expected {expected_action}, got {action}")
    if missing_product or missing_location:
        raise AssertionError(
            f"{name}: unexpected missing attribution product={missing_product} location={missing_location}"
        )
    for key, expected in (expected_counts or {}).items():
        if key.startswith("missing_required_fields."):
            field = key.split(".", 1)[1]
            actual = summary.get("missing_required_fields", {}).get(field)
        elif "." in key:
            group, field = key.split(".", 1)
            actual = summary.get(group, {}).get(field)
        else:
            actual = summary.get(key)
        if actual != expected:
            raise AssertionError(f"{name}: expected {key}={expected}, got {actual}")


def main() -> None:
    failures: list[str] = []

    for path, needles in REQUIRED.items():
        html = read(path)
        for needle in needles:
            if needle not in html:
                failures.append(f"{path}: missing {needle!r}")

    api_html = read("api/index.html")
    for forbidden in FORBIDDEN_API_COPY:
        if forbidden in api_html:
            failures.append(f"api/index.html: forbidden stale copy {forbidden!r}")

    if failures:
        for failure in failures:
            print(failure)
        raise SystemExit(1)

    summary_script = SUMMARY_SCRIPT.read_text(encoding="utf-8")
    for needle in (
        "goosekit_api_production_request_completed",
        "goosekit_api_production_request_started",
        "goosekit_api_endpoint_examples_viewed",
        "goosekit_api_commercial_example_clicked",
        "goosekit_api_budget_example_clicked",
        "goosekit_api_failure_example_clicked",
        "seo_use_case_page_viewed",
        "api_workflow_page_views",
        "endpoint_production_clicks",
        "ENDPOINT_PRODUCTION_REFS",
        "missing_required_fields",
        "split_missing_fields",
        "Missing Required Fields",
        "free_docs_clicks",
        "workflow_page_views",
        "API_WORKFLOW_SLUGS",
        "inspect_workflow_cta_path",
        "api_workflow_views_without_builder_clicks",
        "inspect_docs_to_production_bridge",
        "free_docs_clicks_without_builder_clicks",
        "for_ai_recommendation_api_pilot",
        "for_ai_query_intent_api_pilot",
        "for_ai_paid_products_api_pilot",
        "endpoints_intro_production",
        "adjacent_endpoint_request",
        "json_endpoint_production",
        "hash_endpoint_production",
        "uuid_endpoint_production",
        "password_endpoint_production",
        "builder_starts",
        "endpoint_example_views",
        "commercial_example_clicks",
        "budget_example_clicks",
        "failure_example_clicks",
        "commercial_example_choices",
        "budget_example_choices",
        "failure_example_choices",
        "Commercial Example Choices",
        "Budget Example Choices",
        "Failure Example Choices",
        "first_fields",
        "First Fields",
        "start_sources",
        "Start Sources",
        "completion_sources",
        "Completion Sources",
        "packet_copy_sources",
        "Packet Copy Sources",
        "mail_click_sources",
        "Mail Click Sources",
        "endpoint_example_views_by_endpoint",
        "Endpoint Example Views",
        "complete_mail_clicks",
        "check_mailbox_before_lead",
        "inspect_builder_start_friction",
        "inspect_builder_completion_friction",
        "inspect_builder_field_burden",
        "goosekit_api_commercial_example_clicked",
        "goosekit_api_budget_example_clicked",
        "goosekit_api_failure_example_clicked",
        "do_not_update_counters_from_analytics_alone",
        'ref=prop("ref", "source_ref")',
        "--output-dir requires --window and --mailbox-check",
        "GOOSEKIT_API_ANALYTICS_SUMMARY_",
        "Do not update lead, revenue, or MRR counters",
    ):
        if needle not in summary_script:
            raise AssertionError(f"summarize_goosekit_api_events.py: missing {needle!r}")

    run_summary_fixture(
        "builder view preserves attribution",
        [
            {
                "event": "goosekit_api_production_request_builder_viewed",
                "timestamp": "2026-06-18T18:17:00Z",
                "properties": {
                    "product": "goosekit_api",
                    "location": "production_request_builder",
                    "endpoint": "JSON formatter",
                    "ref": "json_formatter_api_production_hero",
                    "source_ref": "json_formatter_api_production_hero",
                },
            }
        ],
        "inspect_builder_start_friction",
    )
    run_summary_fixture(
        "endpoint examples are observation only",
        [
            {
                "event": "goosekit_api_production_request_builder_viewed",
                "timestamp": "2026-06-18T22:47:00Z",
                "properties": {
                    "product": "goosekit_api",
                    "location": "production_request_builder",
                    "endpoint": "JSON formatter",
                    "ref": "json_endpoint_production",
                    "source_ref": "json_endpoint_production",
                },
            },
            {
                "event": "goosekit_api_endpoint_examples_viewed",
                "timestamp": "2026-06-18T22:48:00Z",
                "properties": {
                    "product": "goosekit_api",
                    "location": "production_request_endpoint_examples",
                    "endpoint": "JSON formatter",
                    "ref": "json_endpoint_production",
                    "source_ref": "json_endpoint_production",
                },
            },
        ],
        "inspect_builder_start_friction",
        expected_counts={
            "endpoint_example_views": 1,
            "endpoint_example_views_by_endpoint.JSON formatter": 1,
        },
    )
    run_summary_fixture(
        "builder start without completion",
        [
            {
                "event": "goosekit_api_production_request_builder_viewed",
                "timestamp": "2026-06-18T18:18:00Z",
                "properties": {
                    "product": "goosekit_api",
                    "location": "production_request_builder",
                    "endpoint": "Hash generator",
                    "ref": "hash_generator_api_production_hero",
                    "source_ref": "hash_generator_api_production_hero",
                },
            },
            {
                "event": "goosekit_api_production_request_started",
                "timestamp": "2026-06-18T18:19:00Z",
                "properties": {
                    "product": "goosekit_api",
                    "location": "production_request_builder",
                    "endpoint": "Hash generator",
                    "ref": "hash_generator_api_production_hero",
                    "source_ref": "hash_generator_api_production_hero",
                    "first_field": "budget",
                    "start_source": "budget_example",
                    "required_fields_filled": "1",
                    "required_fields_total": "6",
                },
            },
            {
                "event": "goosekit_api_production_request_completed",
                "timestamp": "2026-06-18T18:20:00Z",
                "properties": {
                    "product": "goosekit_api",
                    "location": "production_request_builder",
                    "endpoint": "Hash generator",
                    "ref": "hash_generator_api_production_hero",
                    "source_ref": "hash_generator_api_production_hero",
                    "start_source": "budget_example",
                    "required_fields_filled": "6",
                    "required_fields_total": "6",
                },
            },
            {
                "event": "goosekit_api_packet_copied",
                "timestamp": "2026-06-18T18:21:00Z",
                "properties": {
                    "product": "goosekit_api",
                    "location": "production_request_builder",
                    "endpoint": "Hash generator",
                    "ref": "hash_generator_api_production_hero",
                    "source_ref": "hash_generator_api_production_hero",
                    "start_source": "budget_example",
                    "complete": "true",
                    "required_fields_filled": "6",
                    "required_fields_total": "6",
                },
            },
            {
                "event": "goosekit_api_production_access_clicked",
                "timestamp": "2026-06-18T18:22:00Z",
                "properties": {
                    "product": "goosekit_api",
                    "location": "production_request_builder_mail",
                    "endpoint": "Hash generator",
                    "ref": "hash_generator_api_production_hero",
                    "source_ref": "hash_generator_api_production_hero",
                    "start_source": "budget_example",
                    "complete": "true",
                    "required_fields_filled": "6",
                    "required_fields_total": "6",
                },
            },
        ],
        "check_mailbox_before_lead",
        expected_counts={
            "first_fields.budget": 1,
            "start_sources.budget_example": 1,
            "completion_sources.budget_example": 1,
            "packet_copy_sources.budget_example": 1,
            "mail_click_sources.budget_example": 1,
        },
    )
    run_summary_fixture(
        "budget example click is observation only",
        [
            {
                "event": "goosekit_api_production_request_builder_viewed",
                "timestamp": "2026-06-19T04:18:00Z",
                "properties": {
                    "product": "goosekit_api",
                    "location": "production_request_builder",
                    "endpoint": "JSON formatter",
                    "ref": "json_endpoint_production",
                    "source_ref": "json_endpoint_production",
                },
            },
            {
                "event": "goosekit_api_budget_example_clicked",
                "timestamp": "2026-06-19T04:19:00Z",
                "properties": {
                    "product": "goosekit_api",
                    "location": "production_request_budget_examples",
                    "endpoint": "JSON formatter",
                    "ref": "json_endpoint_production",
                    "source_ref": "json_endpoint_production",
                    "missing_required_fields": "volume,runtime,specifics,commercial,failure",
                    "required_fields_filled": "1",
                    "required_fields_total": "6",
                    "example_label": "Need quote",
                    "example_value": "Need a quote before production access can be approved.",
                },
            },
        ],
        "inspect_builder_start_friction",
        expected_counts={
            "budget_example_clicks": 1,
            "budget_example_choices.Need quote": 1,
            "missing_required_fields.commercial": 1,
            "missing_required_fields.failure": 1,
        },
    )
    run_summary_fixture(
        "commercial example click is observation only",
        [
            {
                "event": "goosekit_api_production_request_builder_viewed",
                "timestamp": "2026-06-19T05:18:00Z",
                "properties": {
                    "product": "goosekit_api",
                    "location": "production_request_builder",
                    "endpoint": "JSON formatter",
                    "ref": "json_endpoint_production",
                    "source_ref": "json_endpoint_production",
                },
            },
            {
                "event": "goosekit_api_commercial_example_clicked",
                "timestamp": "2026-06-19T05:19:00Z",
                "properties": {
                    "product": "goosekit_api",
                    "location": "production_request_commercial_examples",
                    "endpoint": "JSON formatter",
                    "ref": "json_endpoint_production",
                    "source_ref": "json_endpoint_production",
                    "missing_required_fields": "volume,runtime,specifics,budget,failure",
                    "required_fields_filled": "1",
                    "required_fields_total": "6",
                    "example_label": "Paid product",
                    "example_value": "Part of a paid product integration or production feature.",
                },
            },
        ],
        "inspect_builder_start_friction",
        expected_counts={
            "commercial_example_clicks": 1,
            "commercial_example_choices.Paid product": 1,
            "missing_required_fields.budget": 1,
            "missing_required_fields.failure": 1,
        },
    )
    run_summary_fixture(
        "failure example click is observation only",
        [
            {
                "event": "goosekit_api_production_request_builder_viewed",
                "timestamp": "2026-06-19T04:48:00Z",
                "properties": {
                    "product": "goosekit_api",
                    "location": "production_request_builder",
                    "endpoint": "JSON formatter",
                    "ref": "json_endpoint_production",
                    "source_ref": "json_endpoint_production",
                },
            },
            {
                "event": "goosekit_api_failure_example_clicked",
                "timestamp": "2026-06-19T04:49:00Z",
                "properties": {
                    "product": "goosekit_api",
                    "location": "production_request_failure_examples",
                    "endpoint": "JSON formatter",
                    "ref": "json_endpoint_production",
                    "source_ref": "json_endpoint_production",
                    "missing_required_fields": "volume,runtime,specifics,commercial,budget",
                    "required_fields_filled": "1",
                    "required_fields_total": "6",
                    "example_label": "Feature cannot ship",
                    "example_value": "A customer-facing feature or internal automation cannot ship without this endpoint.",
                },
            },
        ],
        "inspect_builder_start_friction",
        expected_counts={
            "failure_example_clicks": 1,
            "failure_example_choices.Feature cannot ship": 1,
            "missing_required_fields.commercial": 1,
            "missing_required_fields.budget": 1,
        },
    )
    run_summary_fixture(
        "free docs without production bridge",
        [
            {
                "event": "goosekit_api_free_docs_clicked",
                "timestamp": "2026-06-18T19:18:00Z",
                "properties": {
                    "product": "goosekit_api",
                    "location": "api_hero_free_docs",
                    "target_href": "#endpoints",
                },
            },
            {
                "event": "goosekit_api_free_docs_clicked",
                "timestamp": "2026-06-18T19:19:00Z",
                "properties": {
                    "product": "goosekit_api",
                    "location": "pricing_free",
                    "target_href": "#endpoints",
                },
            },
        ],
        "inspect_docs_to_production_bridge",
    )
    run_summary_fixture(
        "endpoint production clicks are counted separately",
        [
            {
                "event": "goosekit_api_production_request_builder_clicked",
                "timestamp": "2026-06-18T20:47:00Z",
                "properties": {
                    "product": "goosekit_api",
                    "location": "json_endpoint_production",
                    "ref": "json_endpoint_production",
                    "target_href": "/api/production-request/?endpoint=json&ref=json_endpoint_production",
                },
            },
            {
                "event": "goosekit_api_production_request_builder_clicked",
                "timestamp": "2026-06-18T20:48:00Z",
                "properties": {
                    "product": "goosekit_api",
                    "location": "uuid_endpoint_production",
                    "ref": "uuid_endpoint_production",
                    "target_href": "/api/production-request/?endpoint=uuid&ref=uuid_endpoint_production",
                },
            },
        ],
        "inspect_builder_navigation",
        expected_counts={"builder_clicks": 2, "endpoint_production_clicks": 2},
    )
    run_summary_fixture(
        "endpoint production refs on form events are not clicks",
        [
            {
                "event": "goosekit_api_production_request_builder_viewed",
                "timestamp": "2026-06-19T04:50:00Z",
                "properties": {
                    "product": "goosekit_api",
                    "location": "production_request_builder",
                    "endpoint": "JSON formatter",
                    "ref": "json_endpoint_production",
                    "source_ref": "json_endpoint_production",
                },
            },
            {
                "event": "goosekit_api_failure_example_clicked",
                "timestamp": "2026-06-19T04:51:00Z",
                "properties": {
                    "product": "goosekit_api",
                    "location": "production_request_failure_examples",
                    "endpoint": "JSON formatter",
                    "ref": "json_endpoint_production",
                    "source_ref": "json_endpoint_production",
                    "missing_required_fields": "volume,runtime,specifics,commercial,budget",
                    "required_fields_filled": "1",
                    "required_fields_total": "6",
                    "example_label": "Feature cannot ship",
                    "example_value": "A customer-facing feature or internal automation cannot ship without this endpoint.",
                },
            },
        ],
        "inspect_builder_start_friction",
        expected_counts={
            "endpoint_production_clicks": 0,
            "failure_example_clicks": 1,
            "missing_required_fields.budget": 1,
        },
    )
    run_summary_fixture(
        "incomplete packet reports missing required fields",
        [
            {
                "event": "goosekit_api_production_access_clicked",
                "timestamp": "2026-06-18T21:17:00Z",
                "properties": {
                    "product": "goosekit_api",
                    "location": "production_request_builder_mail",
                    "endpoint": "JSON formatter",
                    "ref": "json_endpoint_production",
                    "source_ref": "json_endpoint_production",
                    "complete": "false",
                    "missing_required_fields": "budget,failure",
                    "required_fields_filled": "4",
                    "required_fields_total": "6",
                },
            },
            {
                "event": "goosekit_api_packet_copied",
                "timestamp": "2026-06-18T21:18:00Z",
                "properties": {
                    "product": "goosekit_api",
                    "location": "production_request_builder",
                    "endpoint": "JSON formatter",
                    "ref": "json_endpoint_production",
                    "source_ref": "json_endpoint_production",
                    "complete": "false",
                    "missing_required_fields": "failure",
                    "required_fields_filled": "5",
                    "required_fields_total": "6",
                },
            },
        ],
        "check_mailbox_before_lead",
        expected_counts={
            "incomplete_mail_clicks": 1,
            "missing_required_fields.budget": 1,
            "missing_required_fields.failure": 2,
        },
    )
    run_summary_fixture(
        "completed packet requires mailbox check",
        [
            {
                "event": "goosekit_api_production_request_completed",
                "timestamp": "2026-06-18T18:20:00Z",
                "properties": {
                    "product": "goosekit_api",
                    "location": "production_request_builder",
                    "endpoint": "UUID generator",
                    "ref": "uuid_generator_api_production_hero",
                    "source_ref": "uuid_generator_api_production_hero",
                    "required_fields_filled": "6",
                    "required_fields_total": "6",
                },
            },
            {
                "event": "goosekit_api_production_access_clicked",
                "timestamp": "2026-06-18T18:21:00Z",
                "properties": {
                    "product": "goosekit_api",
                    "location": "production_request_builder_mail",
                    "endpoint": "UUID generator",
                    "ref": "uuid_generator_api_production_hero",
                    "source_ref": "uuid_generator_api_production_hero",
                    "complete": "true",
                    "required_fields_filled": "6",
                    "required_fields_total": "6",
                },
            },
        ],
        "check_mailbox_before_lead",
    )
    run_summary_fixture(
        "real mailbox packet wins",
        [
            {
                "event": "goosekit_api_production_access_clicked",
                "timestamp": "2026-06-18T18:22:00Z",
                "properties": {
                    "product": "goosekit_api",
                    "location": "production_request_builder_mail",
                    "endpoint": "Password generator",
                    "ref": "password_generator_api_production_hero",
                    "source_ref": "password_generator_api_production_hero",
                    "complete": "true",
                    "required_fields_filled": "6",
                    "required_fields_total": "6",
                },
            }
        ],
        "score_inbound_packet",
        mailbox_packets=1,
    )

    print("GOOSEKIT_API_EVENT_AUDIT_OK")


if __name__ == "__main__":
    main()
