#!/bin/bash
# ============================================================
# audit_privacy_offline.sh
# Night-sprint regression guard: privacy/offline routing +
# checkout attribution for Goosekit Offline Pack + Ship It Kit
#
# Checks:
#   1. High-privacy pages have Offline Pack nav link with
#      title="Run offline — no data leaves your device"
#   2. Offline Pack checkout helpers read+preserve source param
#      and redirect to the correct LS URL pattern
#   3. Ship It Kit compare pages have NO raw LS checkout links
#      bypassing attribution helpers
#   4. Offline Pack price in site is €29 (not €19)
#
# Usage: ./audit_privacy_offline.sh [goosekit-root]
#   defaults to ~/goosekit.dev
# ============================================================

ROOT="${1:-$HOME/goosekit.dev}"
FAILED=0
PASSED=0

echo "============================================="
echo "Goosekit — Night Sprint Regression Audit"
echo "Root: $ROOT"
echo "============================================="
echo ""

# ----------------------------------------------------------
# Helpers (avoid set -e pitfalls with arithmetic)
# ----------------------------------------------------------
pass() { echo "  ✅ $1"; PASSED=$((PASSED+1)); }
fail() { echo "  ❌ $1"; FAILED=$((FAILED+1)); }
info() { echo "  ℹ️  $1"; }

# ----------------------------------------------------------
# CHECK 1 — High-privacy pages have correct Offline Pack link
# ----------------------------------------------------------
echo "--- Check 1: High-privacy pages — Offline Pack link ---"

PRIVACY_PAGES="json jwt hash base64 regex diff sql-formatter password"
REQUIRED_HREF="/offline-pack/"
REQUIRED_TITLE='title="Run offline — no data leaves your device"'

for page in $PRIVACY_PAGES; do
  FILE="$ROOT/$page/index.html"
  if [[ ! -f "$FILE" ]]; then
    fail "$page/index.html missing"
    continue
  fi

  # Check for both the href and the correct title attribute
  if grep -q "href=\"$REQUIRED_HREF\"" "$FILE" && \
     grep -q "$REQUIRED_TITLE" "$FILE"; then
    pass "$page — has correct Offline Pack nav link"
  elif grep -q "href=\"$REQUIRED_HREF\"" "$FILE"; then
    fail "$page — has /offline-pack/ link but missing correct title attr"
  else
    fail "$page — missing /offline-pack/ nav link entirely"
  fi
done

echo ""

# ----------------------------------------------------------
# CHECK 2 — Offline Pack checkout helpers
# ----------------------------------------------------------
echo "--- Check 2: Offline Pack checkout helpers ---"

check_checkout_helper() {
  local name="$1"
  local file="$2"
  local expected_ls="https://shipitstudio.lemonsqueezy.com/checkout/buy/f897713c-9cd2-4aaa-bd95-abd5ecd6b757"

  if [[ ! -f "$file" ]]; then
    fail "$name — file missing ($file)"
    return
  fi

  # 2a: correct LS URL pattern
  if grep -q "$expected_ls" "$file"; then
    pass "$name — correct LS URL"
  else
    fail "$name — LS URL mismatch or missing"
  fi

  # 2b: reads source param from URL
  if grep -q "URLSearchParams\|params.get\|source.*param\|window.location.search" "$file"; then
    pass "$name — reads source param from URL"
  else
    fail "$name — does not read source param from URL"
  fi

  # 2c: has PostHog fallback/default source value
  if grep -q "offline_pack_hero\|offline_pack_bottom" "$file"; then
    pass "$name — has source fallback value"
  else
    fail "$name — missing source fallback/default"
  fi
}

check_checkout_helper "checkout-hero" "$ROOT/go/offline-pack/checkout-hero/index.html"
check_checkout_helper "checkout-bottom" "$ROOT/go/offline-pack/checkout-bottom/index.html"

echo ""

# ----------------------------------------------------------
# CHECK 3 — Ship It Kit compare pages: NO raw LS links
# ----------------------------------------------------------
echo "--- Check 3: Ship It Kit compare pages — no raw LS links ---"

COMPARE_DIR="$ROOT/compare"
RAW_LS_GREP_PATTERN="shipitstudio.lemonsqueezy.com/buy/"

had_compare_page=false
if [[ -d "$COMPARE_DIR" ]]; then
  for f in "$COMPARE_DIR"/*.html; do
    [[ -f "$f" ]] || continue
    had_compare_page=true
    raw_links=$(grep -hE "$RAW_LS_GREP_PATTERN" "$f" 2>/dev/null || true)
    if [[ -n "$raw_links" ]]; then
      fail "compare page has raw LS link: $(basename $f)"
      echo "    Raw link: $(echo "$raw_links" | head -1)"
    else
      pass "$(basename $f) — no raw LS checkout links"
    fi
  done
  # Also check ship-it-kit-vs-* subdirs
  for subdir in "$COMPARE_DIR/ship-it-kit-vs-shipfast" "$COMPARE_DIR/ship-it-kit-vs-makerkit" "$COMPARE_DIR/ship-it-kit-vs-competitors"; do
    if [[ -d "$subdir" ]]; then
      for f in "$subdir"/*.html; do
        [[ -f "$f" ]] || continue
        raw_links=$(grep -hE "$RAW_LS_GREP_PATTERN" "$f" 2>/dev/null || true)
        if [[ -n "$raw_links" ]]; then
          fail "compare subpage has raw LS link: ${f#$COMPARE_DIR/}"
          echo "    Raw link: $(echo "$raw_links" | head -1)"
        else
          pass "$(basename $f) — no raw LS checkout links"
        fi
      done
    fi
  done
  if [[ "$had_compare_page" == "false" ]]; then
    info "No compare HTML files found at top level"
  fi
else
  info "compare dir not found, skipping"
fi

echo ""

# ----------------------------------------------------------
# CHECK 4 — Offline Pack price is €29 (not €19)
# ----------------------------------------------------------
echo "--- Check 4: Offline Pack price is €29 ---"

OP_FILE="$ROOT/offline-pack/index.html"
if [[ ! -f "$OP_FILE" ]]; then
  fail "Offline Pack index.html missing"
else
  # Check €29 appears in display price
  if grep -q "€29" "$OP_FILE"; then
    pass "Offline Pack displays €29 price"
  else
    fail "Offline Pack missing €29 price display"
  fi

  # Check schema.org JSON-LD has price 29
  if grep -q '"price": "29"' "$OP_FILE"; then
    pass "JSON-LD price is 29"
  else
    fail "JSON-LD price missing or not 29"
  fi

  # Double-check €19 is NOT the main price for Offline Pack
  if grep -qE "price.*19|€19.*[Oo]ffline|[Oo]ffline.*€19" "$OP_FILE"; then
    fail "Offline Pack shows €19 (should only show €29)"
  else
    pass "Offline Pack does NOT show €19"
  fi
fi

echo ""

# ----------------------------------------------------------
# Summary
# ----------------------------------------------------------
echo "============================================="
echo "Summary: $PASSED passed, $FAILED failed"
echo "============================================="

if [[ $FAILED -gt 0 ]]; then
  echo ""
  echo "⚠️  One or more checks failed. Review above."
  echo "   Fix real failures before deploying."
  exit 1
else
  echo ""
  echo "✅ All checks passed."
  exit 0
fi
