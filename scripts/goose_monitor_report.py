#!/usr/bin/env python3
"""Generate a small Goose Monitor market-radar report.

This is intentionally lightweight: no SaaS backend, no queue, no database.
It fetches a project's watched pages, stores JSON snapshots, compares against
previous snapshots, and emits a Markdown action report for manual-assisted MVPs.
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import html
import json
import re
import sys
from dataclasses import dataclass, asdict
from html.parser import HTMLParser
from pathlib import Path
from typing import Any
from urllib.parse import urljoin, urlparse
from urllib.request import Request, urlopen

USER_AGENT = "GooseMonitor/0.1 (+https://goosekit.dev/goose-monitor/)"
DEFAULT_SNAPSHOT_DIR = Path(".goose-monitor-snapshots")
WATCH_WORDS = {
    "pricing": ["pricing", "price", "plan", "free", "trial", "$", "€", "refund", "discount"],
    "comparison": ["compare", "alternative", "vs", "versus", "competitor"],
    "launch": ["launch", "new", "beta", "changelog", "release", "update"],
    "proof": ["case study", "customer", "testimonial", "review", "trusted"],
    "distribution": ["product hunt", "reddit", "hacker news", "directory", "featured"],
}


def count_keyword(text: str, keyword: str) -> int:
    if keyword in {"$", "€"}:
        return text.count(keyword)
    pattern = r"(?<![a-z0-9])" + re.escape(keyword) + r"(?![a-z0-9])"
    return len(re.findall(pattern, text))


class Extractor(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.title: str = ""
        self.meta_description: str = ""
        self.h1: list[str] = []
        self.links: list[dict[str, str]] = []
        self._tag_stack: list[str] = []
        self._capture_title = False
        self._capture_h1 = False
        self._text_parts: list[str] = []
        self._current_link: str | None = None
        self._current_link_text: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attrs_dict = {k.lower(): v or "" for k, v in attrs}
        self._tag_stack.append(tag)
        if tag == "title":
            self._capture_title = True
        elif tag == "meta" and attrs_dict.get("name", "").lower() == "description":
            self.meta_description = attrs_dict.get("content", "").strip()
        elif tag == "h1":
            self._capture_h1 = True
        elif tag == "a" and attrs_dict.get("href"):
            self._current_link = attrs_dict["href"].strip()
            self._current_link_text = []

    def handle_endtag(self, tag: str) -> None:
        if tag == "title":
            self._capture_title = False
        elif tag == "h1":
            self._capture_h1 = False
        elif tag == "a" and self._current_link:
            text = clean_text(" ".join(self._current_link_text))[:120]
            self.links.append({"href": self._current_link, "text": text})
            self._current_link = None
            self._current_link_text = []
        if self._tag_stack:
            self._tag_stack.pop()

    def handle_data(self, data: str) -> None:
        if not data.strip():
            return
        if any(tag in {"script", "style", "noscript"} for tag in self._tag_stack):
            return
        if self._capture_title:
            self.title += data
        if self._capture_h1:
            self.h1.append(data)
        if self._current_link is not None:
            self._current_link_text.append(data)
        self._text_parts.append(data)

    @property
    def text(self) -> str:
        return clean_text(" ".join(self._text_parts))


def clean_text(value: str) -> str:
    return re.sub(r"\s+", " ", html.unescape(value or "")).strip()


def slugify(value: str) -> str:
    parsed = urlparse(value)
    base = (parsed.netloc + parsed.path).strip("/") or value
    return re.sub(r"[^a-z0-9]+", "-", base.lower()).strip("-")[:90] or "page"


@dataclass
class Snapshot:
    url: str
    fetched_at: str
    status: int
    title: str
    meta_description: str
    h1: list[str]
    text_hash: str
    text_excerpt: str
    keywords: dict[str, int]
    notable_links: list[dict[str, str]]


def fetch_html(url: str, timeout: int) -> tuple[int, str]:
    req = Request(url, headers={"User-Agent": USER_AGENT, "Accept": "text/html,*/*;q=0.8"})
    with urlopen(req, timeout=timeout) as response:
        charset = response.headers.get_content_charset() or "utf-8"
        body = response.read(1_500_000).decode(charset, "replace")
        return int(response.status), body


def snapshot_url(url: str, timeout: int) -> Snapshot:
    status, body = fetch_html(url, timeout)
    parser = Extractor()
    parser.feed(body)
    text = parser.text
    lower = text.lower()
    keywords = {group: sum(count_keyword(lower, word) for word in words) for group, words in WATCH_WORDS.items()}
    notable_links = []
    for link in parser.links:
        hay = (link.get("href", "") + " " + link.get("text", "")).lower()
        if any(word in hay for words in WATCH_WORDS.values() for word in words):
            href = link["href"]
            if not urlparse(href).netloc:
                href = urljoin(url, href)
            notable_links.append({"href": href, "text": link.get("text", "")})
    return Snapshot(
        url=url,
        fetched_at=dt.datetime.now(dt.UTC).isoformat(timespec="seconds"),
        status=status,
        title=clean_text(parser.title),
        meta_description=clean_text(parser.meta_description),
        h1=[clean_text(x) for x in parser.h1 if clean_text(x)][:3],
        text_hash=hashlib.sha256(text.encode("utf-8")).hexdigest(),
        text_excerpt=text[:420],
        keywords=keywords,
        notable_links=notable_links[:12],
    )


def load_json(path: Path) -> Any:
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def save_snapshot(snapshot: Snapshot, snapshot_dir: Path) -> Path:
    snapshot_dir.mkdir(parents=True, exist_ok=True)
    path = snapshot_dir / f"{slugify(snapshot.url)}.json"
    path.write_text(json.dumps(asdict(snapshot), indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return path


def diff_snapshot(old: dict[str, Any] | None, new: Snapshot) -> list[str]:
    if not old:
        return ["First snapshot captured; use the next run for concrete diffs."]
    changes: list[str] = []
    if old.get("title") != new.title:
        changes.append(f"Title changed from “{old.get('title','')}” to “{new.title}”.")
    if old.get("meta_description") != new.meta_description:
        changes.append("Meta description changed.")
    if old.get("h1") != new.h1:
        changes.append(f"H1 changed to: {', '.join(new.h1) or 'none'}.")
    if old.get("text_hash") != new.text_hash:
        changes.append("Main page text changed.")
    old_keywords = old.get("keywords", {}) if isinstance(old.get("keywords"), dict) else {}
    for group, count in new.keywords.items():
        previous = int(old_keywords.get(group, 0) or 0)
        if abs(count - previous) >= 2:
            direction = "increased" if count > previous else "decreased"
            changes.append(f"{group.title()} language {direction}: {previous} → {count} mentions.")
    return changes or ["No meaningful change detected against the previous snapshot."]


def action_ideas(name: str, snapshot: Snapshot, changes: list[str]) -> list[str]:
    ideas: list[str] = []
    if snapshot.keywords.get("pricing", 0) >= 2 or any("Pricing" in c or "pricing" in c for c in changes):
        ideas.append(f"Review {name}'s pricing/offer language and update your pricing FAQ or CTA if their promise is clearer.")
    if snapshot.keywords.get("comparison", 0) >= 1 or any("comparison" in (l.get("href", "") + l.get("text", "")).lower() for l in snapshot.notable_links):
        ideas.append(f"Consider a focused comparison or alternative page against {name} if search intent exists.")
    if snapshot.keywords.get("launch", 0) >= 2:
        ideas.append(f"Check whether {name}'s launch/update creates a timely distribution angle or objection to answer.")
    if snapshot.keywords.get("proof", 0) >= 2:
        ideas.append(f"Extract proof patterns from {name}'s page and strengthen your own proof section with real specifics.")
    if not ideas:
        ideas.append(f"No urgent action. Keep {name} on the watchlist and prioritize clearer buyer-intent pages first.")
    return ideas[:3]


def markdown_report(config: dict[str, Any], rows: list[tuple[dict[str, Any], Snapshot, list[str], list[str]]]) -> str:
    now = dt.datetime.now(dt.UTC).strftime("%Y-%m-%d %H:%M UTC")
    project = config.get("project_name", "Project")
    question = config.get("question", "What should we do next to win qualified traffic?")
    lines = [
        f"# Goose Monitor report — {project}",
        "",
        f"Generated: {now}",
        f"Main question: {question}",
        "",
        "## Executive read",
        "",
        "This report highlights page changes and market signals that can turn into SEO, pricing, or distribution actions. Treat it as a working draft: verify important claims manually before publishing or replying publicly.",
        "",
        "## Watched pages",
        "",
    ]
    for item, snap, changes, ideas in rows:
        name = item.get("name") or snap.url
        lines += [f"### {name}", "", f"URL: {snap.url}", f"Title: {snap.title or 'n/a'}", f"H1: {', '.join(snap.h1) or 'n/a'}", "", "Signals:"]
        lines += [f"- {change}" for change in changes]
        if snap.notable_links:
            lines.append("- Notable intent links: " + "; ".join(f"{l.get('text') or l.get('href')}" for l in snap.notable_links[:4]))
        lines += ["", "Suggested actions:"]
        lines += [f"- {idea}" for idea in ideas]
        lines.append("")
    lines += [
        "## Next 7-day plan",
        "",
        "1. Pick the single clearest buyer-intent action above.",
        "2. Ship one page/CTA/FAQ update, not a broad redesign.",
        "3. Track whether the changed page gets impressions, clicks, replies, or checkout movement.",
        "4. Run Goose Monitor again next week and compare deltas.",
        "",
    ]
    return "\n".join(lines)


def demo_config() -> dict[str, Any]:
    return {
        "project_name": "TinyDev CRM",
        "question": "Which competitor moves should become SEO or distribution actions this week?",
        "watch": [
            {"name": "Example homepage", "url": "https://example.com/"},
            {"name": "IANA reserved domains", "url": "https://www.iana.org/domains/reserved"},
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate a Goose Monitor snapshot/diff Markdown report.")
    parser.add_argument("--config", type=Path, help="JSON config with project_name, question, and watch[] URLs.")
    parser.add_argument("--out", type=Path, default=Path("goose-monitor-report.md"), help="Markdown output path.")
    parser.add_argument("--snapshot-dir", type=Path, default=DEFAULT_SNAPSHOT_DIR, help="Snapshot JSON directory.")
    parser.add_argument("--timeout", type=int, default=18, help="Fetch timeout per page in seconds.")
    parser.add_argument("--demo", action="store_true", help="Print a sample config and exit.")
    args = parser.parse_args()

    if args.demo:
        print(json.dumps(demo_config(), indent=2))
        return 0
    if not args.config:
        parser.error("--config is required unless --demo is used")
    config = load_json(args.config)
    if not isinstance(config, dict):
        raise SystemExit(f"Invalid config: {args.config}")
    watch = config.get("watch")
    if not isinstance(watch, list) or not watch:
        raise SystemExit("Config must include a non-empty watch[] list")

    rows = []
    for item in watch:
        if not isinstance(item, dict) or not item.get("url"):
            raise SystemExit("Each watch item must be an object with a url")
        url = item["url"]
        previous_path = args.snapshot_dir / f"{slugify(url)}.json"
        previous = load_json(previous_path)
        try:
            snap = snapshot_url(url, args.timeout)
        except Exception as exc:  # report errors without hiding other pages
            print(f"warning: failed to fetch {url}: {exc}", file=sys.stderr)
            continue
        changes = diff_snapshot(previous, snap)
        ideas = action_ideas(item.get("name") or url, snap, changes)
        rows.append((item, snap, changes, ideas))
        save_snapshot(snap, args.snapshot_dir)

    if not rows:
        raise SystemExit("No pages could be fetched; no report written")
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(markdown_report(config, rows), encoding="utf-8")
    print(f"wrote {args.out}")
    print(f"updated snapshots in {args.snapshot_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
