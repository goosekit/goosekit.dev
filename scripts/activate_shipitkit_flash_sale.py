#!/usr/bin/env python3
"""Activate the Ship It Kit April 28 flash sale after Lemon Squeezy shows €29.

Default mode is dry-run. Use --apply only inside the sale window, after the Lemon
Squeezy product price has been changed and verified at €29.
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

LS_URL = "https://shipitstudio.lemonsqueezy.com/checkout/buy/66928c03-2807-4c41-aa34-69cfdb6ae07a"
PARIS_TZ = ZoneInfo("Europe/Paris")
SALE_START_AT = datetime(2026, 4, 28, 0, 0, 0, tzinfo=PARIS_TZ)
SALE_END = "2026-04-30T23:59:59+02:00"

CHECKOUT_TEMPLATE = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="robots" content="noindex, nofollow">
  <title>Opening secure checkout…</title>
  <meta http-equiv="refresh" content="3; url={LS_URL}">
  <script>
    (function () {{
      var params = new URLSearchParams(window.location.search);
      if (!params.get('ref')) params.set('ref', 'ship_it_kit_flash_sale');
      var target = '{LS_URL}';
      var glue = target.indexOf('?') === -1 ? '?' : '&';
      window.location.replace(target + glue + params.toString());
    }})();
  </script>
  <script defer src="/posthog.js"></script>
  <style>body{{margin:0;min-height:100vh;display:grid;place-items:center;padding:24px;font-family:system-ui,-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;color:#e2e8f0;background:#0f172a}}.card{{max-width:620px;padding:28px;border:1px solid rgba(255,255,255,.1);border-radius:20px;background:rgba(15,23,42,.82)}}a{{color:#ff4800}}</style>
</head>
<body><main class="card"><h1>Opening secure checkout…</h1><p>If it does not open automatically, <a href="{LS_URL}">continue to Lemon Squeezy</a>.</p></main></body>
</html>
'''


def replace_exact(text: str, old: str, new: str, label: str) -> str:
    if old not in text:
        raise RuntimeError(f"missing expected text for {label}: {old[:90]!r}")
    return text.replace(old, new)


def write_if_changed(path: Path, text: str, apply: bool, changed: list[str]) -> None:
    original = path.read_text()
    if original == text:
        return
    changed.append(str(path))
    if apply:
        path.write_text(text)


def activate_flash_page(root: Path, apply: bool, changed: list[str]) -> None:
    path = root / "ship-it-kit-flash" / "index.html"
    text = path.read_text()
    replacements = [
        ("Ship It Kit flash sale starts April 28 — €29 until April 30, then back to €49", "Ship It Kit flash sale ends April 30 at midnight CEST — €29 now, then back to €49", "topbar"),
        ('<div class="badge">Coming Soon</div>', '<div class="badge">Limited Time</div>', "badge"),
        ('<span class="price-was">Regular price €49</span>', '<span class="price-was">Was €49</span>', "was price"),
        ('The checkout opens when the flash sale starts. Until then, use the product page to check fit honestly.', 'The flash sale is live. Buy only if the stack matches your project: Next.js + Supabase + Stripe.', "sale-open note"),
        ('data-countdown-target="2026-04-28T00:00:00+02:00"', f'data-countdown-target="{SALE_END}"', "countdown target"),
        ('Sale starts April 28', 'Sale ends April 30', "countdown fallback"),
        ('href="/go/ship-it-kit/notify-flash/" data-ph-event="ship_it_kit_flash_cta_clicked" data-ph-location="flash_hero_notify">Remind me when it starts</a>', 'href="/go/ship-it-kit/checkout-flash-hero/" data-ph-event="ship_it_kit_flash_cta_clicked" data-ph-location="flash_hero_buy">Get instant repo access — €29</a>', "hero CTA"),
        ('href="/go/ship-it-kit/notify-flash/" data-ph-event="ship_it_kit_flash_cta_clicked" data-ph-location="flash_bottom_notify">Remind me when it starts</a>', 'href="/go/ship-it-kit/checkout-flash-bottom/" data-ph-event="ship_it_kit_flash_cta_clicked" data-ph-location="flash_bottom_buy">Get instant repo access — €29</a>', "bottom CTA"),
        ('<a class="btn btn-secondary" href="/ship-it-kit-flash-sale.ics" data-ph-event="ship_it_kit_flash_calendar_clicked" data-ph-location="flash_hero_calendar">Add sale to calendar</a>', '', "hero calendar CTA"),
        ('<a class="btn btn-secondary" href="/ship-it-kit-flash-sale.ics" data-ph-event="ship_it_kit_flash_calendar_clicked" data-ph-location="flash_bottom_calendar">Add sale to calendar</a>', '', "bottom calendar CTA"),
        ('<h3 style="margin:0 0 8px;color:#fff;">When does the sale start and end?</h3>\n        <p style="margin:0 0 18px;color:#cbd5e1;">It starts April 28 at 00:00 CEST and ends April 30 at 23:59 CEST.</p>', '<h3 style="margin:0 0 8px;color:#fff;">What happens after April 30?</h3>\n        <p style="margin:0 0 18px;color:#cbd5e1;">The flash-sale page closes and the product returns to the regular €49 price.</p>', "FAQ sale window"),
        ('This is a launch-window price to get the starter into more real projects quickly and learn from serious builders. After April 30, the price goes back to €49.', 'This is a short launch-window price to get the starter into more real projects quickly. After April 30, the product goes back to €49.', "temporary price"),
        ('The sale starts April 28. Check the stack fit now; buy only if it matches your project.', 'The sale is live until April 30. Check the stack fit first; buy only if it matches your project.', "bottom sub"),
        ('€29 window starts April 28. If the stack does not match, skip it honestly.', '€29 window ends April 30 at midnight CEST. If the stack does not match, skip it honestly.', "footer"),
        ("if (diff <= 0) { el.textContent = 'Sale is live'; return; }", "if (diff <= 0) { el.textContent = 'Sale ended'; return; }", "countdown ended"),
        ("el.textContent = 'Starts in ' + days + 'd ' + pad(hours) + 'h ' + pad(minutes) + 'm';", "el.textContent = 'Ends in ' + days + 'd ' + pad(hours) + 'h ' + pad(minutes) + 'm';", "countdown label"),
    ]
    for old, new, label in replacements:
        text = replace_exact(text, old, new, label)
    write_if_changed(path, text, apply, changed)


def activate_product_page(root: Path, apply: bool, changed: list[str]) -> None:
    path = root / "ship-it-kit" / "index.html"
    text = path.read_text()
    replacements = [
        ('<a class="launch-banner-link" href="/ship-it-kit-flash/?ref=product_launch_banner" data-ph-event="ship_it_kit_secondary_click" data-ph-location="launch_banner_flash_preview">Flash sale starts April 28 — €29 until April 30. Check fit before buying.</a>', '<a class="launch-banner-link" href="/go/ship-it-kit/checkout-product-sticky/?source=launch_banner" data-ph-event="ship_it_kit_cta_clicked" data-ph-location="launch_banner">Flash sale is live — get Ship It Kit for €29 until April 30</a>'),
        ('€49 one-time.', '€29 until April 30.'),
        ('worth €49 to you', 'worth €29 to you'),
        ('"price": "49"', '"price": "29"'),
        ('Launch week pricing — ends April 30', '€29 until April 30 — buy now'),
        ('Get the starter, €49', 'Get the starter, €29'),
        ('€49 <span>one-time</span>', '€29 <span>until April 30</span>'),
        ('€49 to skip the auth + billing loop.', '€29 to skip the auth + billing loop.'),
        ('€49 <span>one-time</span>', '€29 <span>until April 30</span>'),
        ('Why only €49?', 'Why only €29 during the flash sale?'),
        ('€49 one-time, instant repo access, lifetime starter updates, 30-day money-back guarantee.', '€29 until April 30, instant repo access, lifetime starter updates, 30-day money-back guarantee.'),
    ]
    for old, new in replacements:
        if old in text:
            text = text.replace(old, new)
    write_if_changed(path, text, apply, changed)


def activate_weekend_page(root: Path, apply: bool, changed: list[str]) -> None:
    path = root / "ship-it-kit-weekend" / "index.html"
    text = path.read_text()
    replacements = [
        ('€49 one-time.', '€29 until April 30.', False),
        ('🚨 Ship It Kit Launch — €49 ends April 30', '🚨 Ship It Kit Flash Sale — €29 ends April 30', False),
        ('🚨 Flash sale starts April 28 — Ship It Kit will be €29 until April 30', '🚨 Ship It Kit Flash Sale — €29 ends April 30', True),
        ('/ship-it-kit-flash/?ref=weekend_topbar_flash', '/go/ship-it-kit/checkout-flash-hero/?source=ship_it_kit_weekend_topbar', True),
        ('Check the €29 window →', 'Get instant repo access, €29 →', True),
        ('/go/ship-it-kit/checkout-weekend-hero/?source=ship_it_kit_weekend_hero', '/go/ship-it-kit/checkout-flash-hero/?source=ship_it_kit_weekend_hero', True),
        ('💳 Get instant repo access, €49 →', '💳 Get instant repo access, €29 →', True),
        ('⚡ Launch window — €49 ends April 30 · Regular price goes up after', '⚡ Flash sale — €29 ends April 30 · Regular price goes back after', False),
        ('⚡ Weekend build angle — get auth + billing wired before Monday', '⚡ Flash sale — €29 ends April 30 · Regular price goes back after', True),
        ("What if I'm not ready for €49?", "What if I'm not ready for €29?", True),
        ('€49 one-time. Ship your first paying customer this month.', '€29 until April 30. Ship your first paying customer this month.', False),
        ('/go/ship-it-kit/checkout-weekend-bottom/?source=ship_it_kit_weekend_bottom', '/go/ship-it-kit/checkout-flash-bottom/?source=ship_it_kit_weekend_bottom', True),
        ('💳 Get instant repo access — €49 →', '💳 Get instant repo access — €29 →', True),
    ]
    for old, new, required in replacements:
        if old in text:
            text = text.replace(old, new)
        elif required:
            raise RuntimeError(f"missing expected text for weekend {old[:40]}: {old[:90]!r}")
    write_if_changed(path, text, apply, changed)


def create_checkout_helpers(root: Path, apply: bool, changed: list[str]) -> None:
    for name in ["checkout-flash-hero", "checkout-flash-bottom"]:
        path = root / "go" / "ship-it-kit" / name / "index.html"
        if path.exists() and path.read_text() == CHECKOUT_TEMPLATE:
            continue
        changed.append(str(path))
        if apply:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(CHECKOUT_TEMPLATE)


def run_checks(root: Path) -> int:
    env = dict(**__import__('os').environ, SHIPITKIT_FLASH_SALE_ACTIVE="1")
    cmd = ["bash", str(root / "scripts" / "audit_revenue_paths.sh"), str(root)]
    result = subprocess.run(cmd, env=env, text=True, capture_output=True)
    print(result.stdout)
    if result.returncode:
        print(result.stderr, file=sys.stderr)
    return result.returncode


def assert_apply_guard(args: argparse.Namespace) -> None:
    if not args.apply:
        return
    if not args.price_verified_29:
        raise RuntimeError("Refusing --apply until Lemon Squeezy checkout has been verified at €29. Re-run with --price-verified-29 after manual verification.")
    now = datetime.now(PARIS_TZ)
    if now < SALE_START_AT and not args.allow_early:
        raise RuntimeError(f"Refusing --apply before sale start ({SALE_START_AT.isoformat()}). Use --allow-early only for isolated tests, not production.")


def main() -> int:
    parser = argparse.ArgumentParser(description="Activate Ship It Kit flash sale after LS price verification")
    parser.add_argument("--root", default=".", help="Goosekit repo root")
    parser.add_argument("--apply", action="store_true", help="write changes; otherwise dry-run only")
    parser.add_argument("--price-verified-29", action="store_true", help="required with --apply after verifying Lemon Squeezy checkout displays €29")
    parser.add_argument("--allow-early", action="store_true", help="test-only escape hatch for isolated pre-sale activation simulations")
    parser.add_argument("--run-checks", action="store_true", help="run active-sale checks after changes")
    args = parser.parse_args()
    assert_apply_guard(args)

    root = Path(args.root).resolve()
    changed: list[str] = []
    activate_flash_page(root, args.apply, changed)
    activate_product_page(root, args.apply, changed)
    activate_weekend_page(root, args.apply, changed)
    create_checkout_helpers(root, args.apply, changed)

    mode = "APPLIED" if args.apply else "DRY_RUN"
    print(f"{mode}: {len(changed)} files would change" if not args.apply else f"{mode}: {len(changed)} files changed")
    for path in changed:
        print(f"- {Path(path).relative_to(root)}")

    if args.run_checks:
        return run_checks(root)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
