#!/usr/bin/env python3
"""Set each sitemap <lastmod> to the last git commit date of the URL's index.html.

Run from the repo root (or pass the root as the first argument):
    python3 scripts/update_sitemap_lastmod.py
URLs whose file has no git history keep their existing lastmod.
"""
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent
SITEMAP = ROOT / "sitemap.xml"


def last_commit_date(path: Path) -> str | None:
    try:
        out = subprocess.run(
            ["git", "log", "-1", "--format=%as", "--", str(path.relative_to(ROOT))],
            cwd=ROOT, capture_output=True, text=True, check=True,
        ).stdout.strip()
        return out or None
    except subprocess.CalledProcessError:
        return None


def main() -> None:
    s = SITEMAP.read_text()
    updated = 0

    def repl(m: re.Match) -> str:
        nonlocal updated
        url_path = m.group("path") or "/"
        rel = url_path.strip("/")
        file = ROOT / rel / "index.html" if rel else ROOT / "index.html"
        if not file.exists():
            return m.group(0)
        date = last_commit_date(file)
        if not date or date == m.group("date"):
            return m.group(0)
        updated += 1
        return m.group(0).replace(
            f"<lastmod>{m.group('date')}</lastmod>", f"<lastmod>{date}</lastmod>"
        )

    s = re.sub(
        r"<url>(?:(?!</url>).)*?<loc>https://goosekit\.dev(?P<path>/[^<]*)?</loc>"
        r"(?:(?!</url>).)*?<lastmod>(?P<date>[^<]+)</lastmod>(?:(?!</url>).)*?</url>",
        repl, s, flags=re.S,
    )
    SITEMAP.write_text(s)
    print(f"updated {updated} lastmod entries")


if __name__ == "__main__":
    main()
