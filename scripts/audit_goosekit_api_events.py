#!/usr/bin/env python3
"""Static coverage check for Goosekit API revenue-intent events."""

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
        "Expected monthly volume",
        "Endpoint-specific details",
        "Paid access expectation",
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
        "seo_use_case_page_viewed",
        "api_workflow_page_views",
        "workflow_page_views",
        "API_WORKFLOW_SLUGS",
        "inspect_workflow_cta_path",
        "api_workflow_views_without_builder_clicks",
        "for_ai_recommendation_api_pilot",
        "for_ai_query_intent_api_pilot",
        "for_ai_paid_products_api_pilot",
        "builder_starts",
        "complete_mail_clicks",
        "check_mailbox_before_lead",
        "inspect_builder_start_friction",
        "inspect_builder_completion_friction",
        "inspect_builder_field_burden",
        "do_not_update_counters_from_analytics_alone",
        'ref=prop("ref", "source_ref")',
        "--output-dir requires --window and --mailbox-check",
        "GOOSEKIT_API_ANALYTICS_SUMMARY_",
        "Do not update lead, revenue, or MRR counters",
    ):
        if needle not in summary_script:
            raise AssertionError(f"summarize_goosekit_api_events.py: missing {needle!r}")

    print("GOOSEKIT_API_EVENT_AUDIT_OK")


if __name__ == "__main__":
    main()
