#!/usr/bin/env python3
"""Static coverage check for Goosekit API revenue-intent events."""

from html.parser import HTMLParser
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

REQUIRED = {
    "api/index.html": [
        "goosekit_api_free_docs_clicked",
        "goosekit_api_production_access_clicked",
        'data-ph-product="goosekit_api"',
        'data-ph-location="pricing_production"',
        "Endpoint(s)%20I%20need",
        "Estimated%20monthly%20volume",
        "Commercial%20or%20client-facing%20use",
        'id="production-request"',
        'data-ph-location="production_request_packet"',
        "What%20breaks%20without%20production%20access",
        "Good production fit",
        "Probably not a fit",
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
        "goosekit_api_production_access_clicked",
        'data-ph-product="goosekit_api"',
        'data-ph-location="json_formatter_api_production_packet"',
        "/api/#production-request",
    ],
    "use-cases/hash-generator-api/index.html": [
        "Hash Generator API for Checksums",
        "goosekit_api_tool_page_clicked",
        "goosekit_api_production_access_clicked",
        'data-ph-product="goosekit_api"',
        'data-ph-location="hash_generator_api_production_packet"',
        "Do not send passwords",
        "/api/#production-request",
    ],
    "use-cases/index.html": [
        "/use-cases/json-formatter-api/",
        "JSON formatter API for internal tools",
        "/use-cases/hash-generator-api/",
        "Hash generator API for checksums",
    ],
}

FORBIDDEN_API_COPY = [
    "lorem ipsum. Use the free tier",
    "lorem generation",
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

    print("GOOSEKIT_API_EVENT_AUDIT_OK")


if __name__ == "__main__":
    main()
