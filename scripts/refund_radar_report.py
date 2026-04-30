#!/usr/bin/env python3
"""Generate a lightweight Refund Radar churn/refund action report from CSV.

CSV columns are flexible. Useful names: email, customer, event, amount, reason,
notes, created_at. The script groups reasons into practical retention buckets and
emits a Markdown report with actions and winback copy.
"""
from __future__ import annotations
import argparse, csv, datetime as dt, re
from collections import Counter, defaultdict
from pathlib import Path

BUCKETS = {
    "setup friction": ["setup", "install", "configure", "hard", "confusing", "onboarding", "docs", "documentation"],
    "missing feature": ["missing", "feature", "doesn't", "does not", "can't", "cannot", "integrate", "integration"],
    "pricing objection": ["price", "expensive", "cost", "budget", "cheap", "too much", "billing"],
    "failed payment": ["failed", "card", "payment", "invoice", "declined", "charge"],
    "unclear value": ["value", "use", "need", "not using", "unused", "roi", "benefit"],
    "support friction": ["support", "response", "help", "bug", "broken", "error", "slow"],
}


def norm(value: str | None) -> str:
    return re.sub(r"\s+", " ", (value or "").strip())


def bucket_reason(text: str) -> str:
    lower = text.lower()
    scores = {name: sum(1 for word in words if word in lower) for name, words in BUCKETS.items()}
    best, score = max(scores.items(), key=lambda item: item[1])
    return best if score else "uncategorized"


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as fh:
        return [{k.strip().lower(): norm(v) for k, v in row.items()} for row in csv.DictReader(fh)]


def reason_for(row: dict[str, str]) -> str:
    return row.get("reason") or row.get("notes") or row.get("description") or row.get("comment") or ""


def event_for(row: dict[str, str]) -> str:
    raw = " ".join([row.get("event", ""), row.get("type", ""), row.get("status", "")]).lower()
    if "refund" in raw: return "refund"
    if "cancel" in raw or "churn" in raw: return "cancellation"
    if "failed" in raw or "declined" in raw: return "failed payment"
    return raw.strip() or "event"


def action_for(bucket: str) -> str:
    return {
        "setup friction": "Ship a shorter first-run checklist and send it immediately after purchase/trial start.",
        "missing feature": "Add a public roadmap/fit note and a targeted alternative workflow before promising a feature.",
        "pricing objection": "Add a pricing FAQ that explains value, refund policy, and a smaller entry path.",
        "failed payment": "Send a softer dunning email with product value recap before the payment retry.",
        "unclear value": "Move the first-win email earlier and show one concrete outcome in the first session.",
        "support friction": "Create a known-issues/support macro and proactively email affected customers.",
    }.get(bucket, "Read the raw reasons and manually decide whether this is product, pricing, onboarding, or support.")


def winback_for(bucket: str) -> str:
    if bucket == "setup friction":
        return "Subject: Want a 10-minute setup shortcut?\n\nI saw setup got in the way. I made a shorter checklist for the first useful result. If you want, reply with your use case and I’ll point you to the quickest path."
    if bucket == "pricing objection":
        return "Subject: Was the plan too much for what you needed?\n\nThanks for trying us. If pricing was the blocker, I’d love to understand what felt mismatched: price, plan limits, or unclear value. Your reply will help us fix the offer."
    if bucket == "missing feature":
        return "Subject: Quick question about the missing feature\n\nYou left because something important was missing. What was the exact workflow you needed? If there is a workaround, I’ll send it. If not, I’ll log it honestly."
    return "Subject: Quick question after cancellation\n\nThanks for trying the product. What was the main reason it did not stick? One sentence is enough and helps us improve the next version."


def report(rows: list[dict[str, str]], product: str) -> str:
    now = dt.datetime.now(dt.UTC).strftime("%Y-%m-%d %H:%M UTC")
    events = Counter(event_for(r) for r in rows)
    buckets = Counter(bucket_reason(reason_for(r)) for r in rows)
    examples = defaultdict(list)
    for row in rows:
        b = bucket_reason(reason_for(row))
        reason = reason_for(row)
        if reason and len(examples[b]) < 3:
            examples[b].append(reason)
    lines = [f"# Refund Radar report — {product}", "", f"Generated: {now}", f"Events analyzed: {len(rows)}", "", "## Event mix", ""]
    lines += [f"- {name}: {count}" for name, count in events.most_common()]
    lines += ["", "## Churn/refund reasons", ""]
    for bucket, count in buckets.most_common():
        lines += [f"### {bucket.title()} — {count}", "", f"Action: {action_for(bucket)}", ""]
        if examples[bucket]:
            lines.append("Evidence:")
            lines += [f"- “{ex}”" for ex in examples[bucket]]
            lines.append("")
    top = buckets.most_common(1)[0][0] if buckets else "uncategorized"
    lines += ["## Winback email draft", "", winback_for(top), "", "## Next 7-day plan", "", "1. Fix the top bucket before adding new acquisition work.", "2. Add/adjust one cancellation reason question so future data is cleaner.", "3. Send the winback email to the matching segment.", "4. Re-run this report next week and compare bucket movement.", ""]
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate a Refund Radar Markdown report from CSV exports.")
    parser.add_argument("--csv", type=Path, required=True)
    parser.add_argument("--product", default="Product")
    parser.add_argument("--out", type=Path, default=Path("refund-radar-report.md"))
    args = parser.parse_args()
    rows = read_rows(args.csv)
    if not rows:
        raise SystemExit("CSV has no rows")
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(report(rows, args.product), encoding="utf-8")
    print(f"wrote {args.out}")
    return 0
if __name__ == "__main__":
    raise SystemExit(main())
