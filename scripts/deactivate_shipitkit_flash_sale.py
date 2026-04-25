#!/usr/bin/env python3
"""Deactivate the Ship It Kit April flash sale and return pages to €49.

Default mode is dry-run. Use --apply after the sale window closes and after the
Lemon Squeezy product price has been restored to €49.
"""
from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

PARIS_TZ = ZoneInfo("Europe/Paris")
SALE_END_AT = datetime(2026, 4, 30, 23, 59, 59, tzinfo=PARIS_TZ)


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


def deactivate_flash_page(root: Path, apply: bool, changed: list[str]) -> None:
    path = root / "ship-it-kit-flash" / "index.html"
    text = path.read_text()
    replacements = [
        ("Ship It Kit flash sale ends April 30 at midnight CEST — €29 now, then back to €49", "Ship It Kit flash sale ended — Ship It Kit is back to €49", "topbar active"),
        ("Ship It Kit flash sale starts April 28 — €29 for 48 hours, then back to €49", "Ship It Kit flash sale ended — Ship It Kit is back to €49", "topbar preview"),
        ('<div class="badge">Limited Time</div>', '<div class="badge">Sale Ended</div>', "badge active"),
        ('<div class="badge">Coming Soon</div>', '<div class="badge">Sale Ended</div>', "badge preview"),
        ('Ship the paid SaaS foundation for €29.', 'Ship the paid SaaS foundation without rebuilding auth + billing.'),
        ('<span class="price">€29</span><span class="price-was">Was €49</span>', '<span class="price">€49</span><span class="price-was">Flash sale ended</span>'),
        ('<span class="price">€29</span><span class="price-was">Regular price €49</span>', '<span class="price">€49</span><span class="price-was">Flash sale ended</span>'),
        ('The flash sale is live. Buy only if the stack matches your project: Next.js + Supabase + Stripe.', 'The flash sale has ended. The regular Ship It Kit product page is the current source of truth.'),
        ('The checkout opens when the flash sale starts. Until then, use the product page to check fit honestly.', 'The flash sale has ended. The regular Ship It Kit product page is the current source of truth.'),
        ('data-countdown-target="2026-04-30T23:59:59+02:00"', 'data-countdown-target="2026-04-30T23:59:59+02:00"'),
        ('Sale ends April 30', 'Sale ended'),
        ('Sale starts April 28', 'Sale ended'),
        ('href="/go/ship-it-kit/checkout-flash-hero/" data-ph-event="ship_it_kit_flash_cta_clicked" data-ph-location="flash_hero_buy">Get instant repo access — €29</a>', 'href="/go/ship-it-kit/product-from-flash/" data-ph-event="ship_it_kit_flash_secondary_click" data-ph-location="flash_hero_product_after_sale">See current product page</a>'),
        ('href="mailto:arthur.pierrey@gmail.com?subject=Ship%20It%20Kit%20flash%20sale%20reminder" data-ph-event="ship_it_kit_flash_cta_clicked" data-ph-location="flash_hero_notify">Remind me when it starts</a>', 'href="/go/ship-it-kit/product-from-flash/" data-ph-event="ship_it_kit_flash_secondary_click" data-ph-location="flash_hero_product_after_sale">See current product page</a>'),
        ('href="/go/ship-it-kit/checkout-flash-bottom/" data-ph-event="ship_it_kit_flash_cta_clicked" data-ph-location="flash_bottom_buy">Get instant repo access — €29</a>', 'href="/go/ship-it-kit/product-from-flash/" data-ph-event="ship_it_kit_flash_secondary_click" data-ph-location="flash_bottom_product_after_sale">See current product page</a>'),
        ('href="mailto:arthur.pierrey@gmail.com?subject=Ship%20It%20Kit%20flash%20sale%20reminder" data-ph-event="ship_it_kit_flash_cta_clicked" data-ph-location="flash_bottom_notify">Remind me when it starts</a>', 'href="/go/ship-it-kit/product-from-flash/" data-ph-event="ship_it_kit_flash_secondary_click" data-ph-location="flash_bottom_product_after_sale">See current product page</a>'),
        ('<h3 style="margin:0 0 8px;color:#fff;">What happens after April 30?</h3>\n        <p style="margin:0 0 18px;color:#cbd5e1;">The flash-sale page closes and the product returns to the regular €49 price.</p>', '<h3 style="margin:0 0 8px;color:#fff;">What happened after April 30?</h3>\n        <p style="margin:0 0 18px;color:#cbd5e1;">The flash sale ended and the product returned to the regular €49 price.</p>'),
        ('<h3 style="margin:0 0 8px;color:#fff;">When does the sale start and end?</h3>\n        <p style="margin:0 0 18px;color:#cbd5e1;">It starts April 28 at 00:00 CEST and ends April 30 at 23:59 CEST.</p>', '<h3 style="margin:0 0 8px;color:#fff;">What happened after April 30?</h3>\n        <p style="margin:0 0 18px;color:#cbd5e1;">The flash sale ended and the product returned to the regular €49 price.</p>'),
        ('This is a short launch-window price to get the starter into more real projects quickly. After April 30, the product goes back to €49.', 'The launch-window price has ended. Ship It Kit is back at the regular €49 one-time price.'),
        ('This is a launch-window price to get the starter into more real projects quickly and learn from serious builders. After April 30, the price goes back to €49.', 'The launch-window price has ended. Ship It Kit is back at the regular €49 one-time price.'),
        ('The sale is live until April 30. Check the stack fit first; buy only if it matches your project.', 'The sale has ended. Check the current product page first; buy only if it matches your project.'),
        ('The sale starts April 28. Check the stack fit now; buy only if it matches your project.', 'The sale has ended. Check the current product page first; buy only if it matches your project.'),
        ('€29 window ends April 30 at midnight CEST. If the stack does not match, skip it honestly.', 'Flash sale ended. If the stack does not match, skip it honestly.'),
        ('€29 window starts April 28. If the stack does not match, skip it honestly.', 'Flash sale ended. If the stack does not match, skip it honestly.'),
        ("if (diff <= 0) { el.textContent = 'Sale ended'; return; }", "if (diff <= 0) { el.textContent = 'Sale ended'; return; }"),
        ("if (diff <= 0) { el.textContent = 'Sale is live'; return; }", "if (diff <= 0) { el.textContent = 'Sale ended'; return; }"),
        ("el.textContent = 'Ends in ' + days + 'd ' + pad(hours) + 'h ' + pad(minutes) + 'm';", "el.textContent = 'Sale ended';"),
        ("el.textContent = 'Starts in ' + days + 'd ' + pad(hours) + 'h ' + pad(minutes) + 'm';", "el.textContent = 'Sale ended';"),
    ]
    for item in replacements:
        old, new = item[0], item[1]
        if old in text:
            text = text.replace(old, new)
    if "/go/ship-it-kit/checkout-flash" in text or "mailto:" in text:
        raise RuntimeError("flash page still contains active checkout or mailto CTA after deactivation")
    write_if_changed(path, text, apply, changed)


def deactivate_product_page(root: Path, apply: bool, changed: list[str]) -> None:
    path = root / "ship-it-kit" / "index.html"
    text = path.read_text()
    replacements = [
        ('€29 until April 30.', '€49 one-time.'),
        ('worth €29 to you', 'worth €49 to you'),
        ('"price": "29"', '"price": "49"'),
        ('€29 until April 30 — buy now', 'Launch week pricing — ended April 30'),
        ('Get the starter, €29', 'Get the starter, €49'),
        ('€29 <span>until April 30</span>', '€49 <span>one-time</span>'),
        ('€29 to skip the auth + billing loop.', '€49 to skip the auth + billing loop.'),
        ('Why only €29 during the flash sale?', 'Why is it only €49?'),
        ('€29 until April 30, instant repo access, lifetime starter updates, 30-day money-back guarantee.', '€49 one-time, instant repo access, lifetime starter updates, 30-day money-back guarantee.'),
    ]
    for old, new in replacements:
        text = text.replace(old, new)
    write_if_changed(path, text, apply, changed)


def deactivate_weekend_page(root: Path, apply: bool, changed: list[str]) -> None:
    path = root / "ship-it-kit-weekend" / "index.html"
    text = path.read_text()
    replacements = [
        ('€29 until April 30.', '€49 one-time.'),
        ('🚨 Ship It Kit Flash Sale — €29 ends April 30', '🚨 Ship It Kit Launch — €49 ended April 30'),
        ('/go/ship-it-kit/checkout-flash-hero/?source=ship_it_kit_weekend_hero', '/go/ship-it-kit/checkout-weekend-hero/?source=ship_it_kit_weekend_hero'),
        ('💳 Get instant repo access, €29 →', '💳 Get instant repo access, €49 →'),
        ('⚡ Flash sale — €29 ends April 30 · Regular price goes back after', '⚡ Launch window ended April 30 · Regular price is back'),
        ("What if I'm not ready for €29?", "What if I'm not ready for €49?"),
        ('€29 until April 30. Ship your first paying customer this month.', '€49 one-time. Ship your first paying customer this month.'),
        ('/go/ship-it-kit/checkout-flash-bottom/?source=ship_it_kit_weekend_bottom', '/go/ship-it-kit/checkout-weekend-bottom/?source=ship_it_kit_weekend_bottom'),
        ('💳 Get instant repo access — €29 →', '💳 Get instant repo access — €49 →'),
    ]
    for old, new in replacements:
        text = text.replace(old, new)
    write_if_changed(path, text, apply, changed)


def remove_flash_checkout_helpers(root: Path, apply: bool, changed: list[str]) -> None:
    for name in ["checkout-flash-hero", "checkout-flash-bottom"]:
        path = root / "go" / "ship-it-kit" / name
        if path.exists():
            changed.append(str(path))
            if apply:
                shutil.rmtree(path)


def run_checks(root: Path) -> int:
    cmd = ["bash", str(root / "scripts" / "audit_revenue_paths.sh"), str(root)]
    result = subprocess.run(cmd, text=True, capture_output=True)
    print(result.stdout)
    if result.returncode:
        print(result.stderr, file=sys.stderr)
    return result.returncode


def assert_apply_guard(args: argparse.Namespace) -> None:
    if not args.apply:
        return
    if not args.price_verified_49:
        raise RuntimeError("Refusing --apply until Lemon Squeezy checkout has been restored to €49. Re-run with --price-verified-49 after manual verification.")
    now = datetime.now(PARIS_TZ)
    if now < SALE_END_AT and not args.allow_early:
        raise RuntimeError(f"Refusing --apply before sale end ({SALE_END_AT.isoformat()}). Use --allow-early only for isolated tests, not production.")


def main() -> int:
    parser = argparse.ArgumentParser(description="Deactivate Ship It Kit flash sale after restoring LS price to €49")
    parser.add_argument("--root", default=".", help="Goosekit repo root")
    parser.add_argument("--apply", action="store_true", help="write changes; otherwise dry-run only")
    parser.add_argument("--price-verified-49", action="store_true", help="required with --apply after verifying Lemon Squeezy checkout displays €49")
    parser.add_argument("--allow-early", action="store_true", help="test-only escape hatch for isolated pre-sale rollback simulations")
    parser.add_argument("--run-checks", action="store_true", help="run normal post-sale revenue checks after changes")
    args = parser.parse_args()
    assert_apply_guard(args)

    root = Path(args.root).resolve()
    changed: list[str] = []
    deactivate_flash_page(root, args.apply, changed)
    deactivate_product_page(root, args.apply, changed)
    deactivate_weekend_page(root, args.apply, changed)
    remove_flash_checkout_helpers(root, args.apply, changed)

    mode = "APPLIED" if args.apply else "DRY_RUN"
    print(f"{mode}: {len(changed)} files changed" if args.apply else f"{mode}: {len(changed)} files would change")
    for path in changed:
        print(f"- {Path(path).relative_to(root)}")

    if args.run_checks:
        return run_checks(root)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
