#!/usr/bin/env python3
"""Static guard for the Goosekit free-tools-first contract."""

import re
import sys
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

PRIMARY_TOOLS = [
    "json",
    "regex",
    "jwt",
    "base64",
    "hash",
    "diff",
    "text-case",
    "image-to-pdf",
    "json-yaml",
    "meta-tag",
    "og-preview",
]

SEO_WORKFLOWS = [
    "format-json-locally",
    "regex-examples-javascript",
    "decode-jwt-locally",
    "base64-decode-locally",
    "hash-checksum-locally",
    "image-to-pdf-browser",
    "open-graph-meta-tags",
]

FORBIDDEN_IN_PRIMARY = [
    "Ship It Kit",
    "/go/ship-it-kit/",
    "shipitstudio.lemonsqueezy.com",
    "checkout-product",
    "Buy €",
    "€29",
    "€49",
    "Request production access",
    "API production request",
    "goosekit_api_production",
]

TRUST_TERMS = [
    "browser",
    "no signup",
    "local",
    "client-side",
    "no upload",
    "no data sent",
]


class LinkParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.links: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag not in {"a", "link", "script", "img"}:
            return
        attrs_dict = dict(attrs)
        href = attrs_dict.get("href") or attrs_dict.get("src")
        if href and href.startswith("/") and not href.startswith("//"):
            self.links.append(href.split("#", 1)[0].split("?", 1)[0])


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def route_file(route: str) -> Path:
    clean = route.strip("/")
    if not clean:
        return ROOT / "index.html"
    if Path(clean).suffix:
        return ROOT / clean
    return ROOT / clean / "index.html"


def check_primary_tools(errors: list[str]) -> None:
    for slug in PRIMARY_TOOLS:
        path = ROOT / slug / "index.html"
        if not path.exists():
            errors.append(f"missing primary tool page: /{slug}/")
            continue
        html = read(path)
        lowered = html.lower()
        for forbidden in FORBIDDEN_IN_PRIMARY:
            if forbidden.lower() in lowered:
                errors.append(f"/{slug}/ contains forbidden paid/API copy: {forbidden}")
        if not any(term in lowered for term in TRUST_TERMS):
            errors.append(f"/{slug}/ is missing visible free/local/browser trust language")


def check_workflows(errors: list[str]) -> None:
    sitemap = read(ROOT / "sitemap.xml")
    all_tools = read(ROOT / "all-tools" / "index.html")
    for slug in SEO_WORKFLOWS:
        path = ROOT / "use-cases" / slug / "index.html"
        if not path.exists():
            errors.append(f"missing SEO workflow page: /use-cases/{slug}/")
            continue
        html = read(path).lower()
        if "ship it kit" in html or "checkout" in html or "request production" in html:
            errors.append(f"/use-cases/{slug}/ contains paid/API conversion copy")
        loc = f"https://goosekit.dev/use-cases/{slug}/"
        if loc not in sitemap:
            errors.append(f"sitemap missing {loc}")
        if f"/use-cases/{slug}/" not in all_tools:
            errors.append(f"all-tools missing /use-cases/{slug}/")


def check_sitemap(errors: list[str]) -> None:
    root = ET.parse(ROOT / "sitemap.xml").getroot()
    ns = "{http://www.sitemaps.org/schemas/sitemap/0.9}"
    locs = [node.find(ns + "loc").text for node in root.findall(ns + "url")]
    duplicates = sorted({loc for loc in locs if locs.count(loc) > 1})
    if duplicates:
        errors.append("duplicate sitemap locs: " + ", ".join(duplicates))


def check_internal_links(errors: list[str]) -> None:
    files = [ROOT / slug / "index.html" for slug in PRIMARY_TOOLS]
    files += [ROOT / "use-cases" / slug / "index.html" for slug in SEO_WORKFLOWS]
    files.append(ROOT / "all-tools" / "index.html")
    checked = 0
    for file in files:
        parser = LinkParser()
        parser.feed(read(file))
        for href in parser.links:
            checked += 1
            target = route_file(href)
            if not target.exists():
                errors.append(f"{file.relative_to(ROOT)} links to missing {href}")
    print(f"internal_links_checked={checked}")


def main() -> int:
    errors: list[str] = []
    check_primary_tools(errors)
    check_workflows(errors)
    check_sitemap(errors)
    check_internal_links(errors)
    if errors:
        print("FREE_TOOLS_FIRST_AUDIT_FAILED")
        for error in errors:
            print(f"- {error}")
        return 1
    print("FREE_TOOLS_FIRST_AUDIT_OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
