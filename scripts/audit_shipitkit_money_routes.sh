#!/bin/bash
# ============================================================
# audit_shipitkit_money_routes.sh
# Night-sprint regression guard: Ship It Kit money routes
# Block 51 — extends block 50 privacy/offline audit
#
# Checks:
#   1. Ship It Kit main page shows €49 (not stale €29 flash-sale)
#   2. Compare pages have NO raw LS checkout links bypassing
#      attribution helpers
#   3. Checkout helpers point to expected LS URL, preserve
#      source/redirect param, and have fallback default
#   4. No active flash-sale routes (/ship-it-kit-flash/ or
#      flash checkout helpers)
#   5. Ship It Kit Lite explicitly out of current attribution
#      scope (direct LS link there is intentional)
#
# Usage: ./audit_shipitkit_money_routes.sh [goosekit-root]
#   defaults to ~/goosekit.dev
# ============================================================

ROOT="${1:-$HOME/goosekit.dev}"
FAILED=0
PASSED=0

echo "============================================="
echo "Ship It Kit — Money Routes Regression Audit"
echo "Root: $ROOT"
echo "============================================="
echo ""

# ----------------------------------------------------------
# Helpers
# ----------------------------------------------------------
pass() { echo "  ✅ $1"; PASSED=$((PASSED+1)); }
fail() { echo "  ❌ $1"; FAILED=$((FAILED+1)); }
info() { echo "  ℹ️  $1"; }

# ----------------------------------------------------------
# CHECK 1 — Ship It Kit main page shows €49 (not €29)
# ----------------------------------------------------------
echo "--- Check 1: Ship It Kit main page — €49 displayed ---"

SIK_FILE="$ROOT/ship-it-kit/index.html"
if [[ ! -f "$SIK_FILE" ]]; then
  fail "ship-it-kit/index.html missing"
else
  if grep -q "€49" "$SIK_FILE"; then
    pass "ship-it-kit — displays €49 price"
  else
    fail "ship-it-kit — missing €49 price display"
  fi
  if grep -q '"price": "49"' "$SIK_FILE"; then
    pass "ship-it-kit JSON-LD price is 49"
  else
    fail "ship-it-kit JSON-LD price missing or not 49"
  fi
  if grep -qE "€29.*[Ss]hip.It.Kit|[Ss]hip.It.Kit.*€29" "$SIK_FILE"; then
    fail "ship-it-kit — stale €29 flash-sale copy found"
  else
    pass "ship-it-kit — no stale €29 flash-sale copy"
  fi
fi

echo ""

# ----------------------------------------------------------
# CHECK 2 — Compare pages: no raw LS checkout links
# ----------------------------------------------------------
echo "--- Check 2: Compare pages — no raw LS checkout links ---"

COMPARE_DIR="$ROOT/compare"
RAW_LS_PATTERN="shipitstudio.lemonsqueezy.com/buy/"
had_any=false

if [[ -d "$COMPARE_DIR" ]]; then
  for f in $(find "$COMPARE_DIR" -name "*.html" -type f 2>/dev/null); do
    had_any=true
    raw_links=$(grep -hE "$RAW_LS_PATTERN" "$f" 2>/dev/null || true)
    if [[ -n "$raw_links" ]]; then
      fail "compare page has raw LS link: ${f#$COMPARE_DIR/}"
      echo "    Raw link: $(echo "$raw_links" | head -1)"
    else
      pass "$(basename "$f") — no raw LS checkout links"
    fi
  done
  if [[ "$had_any" == "false" ]]; then
    info "No compare HTML files found"
  fi
else
  info "compare dir not found, skipping"
fi

echo ""

# ----------------------------------------------------------
# CHECK 3 — Ship It Kit checkout helpers
# ----------------------------------------------------------
echo "--- Check 3: Ship It Kit checkout helpers ---"

EXPECTED_LS_URL="https://shipitstudio.lemonsqueezy.com/checkout/buy/66928c03-2807-4c41-aa34-69cfdb6ae07a"
CHECKOUT_DIR="$ROOT/go/ship-it-kit"

check_sik_helper() {
  local name="$1"
  local file="$2"

  if [[ ! -f "$file" ]]; then
    fail "$name — file missing ($file)"
    return
  fi

  # 3a: correct LS URL
  if grep -q "$EXPECTED_LS_URL" "$file"; then
    pass "$name — correct LS URL"
  else
    fail "$name — LS URL mismatch or missing"
  fi

  # 3b: reads param (source or ref) from URL
  if grep -q "URLSearchParams\|params.get\|source.*param\|ref.*param\|window.location.search" "$file"; then
    pass "$name — reads param from URL"
  else
    fail "$name — does not read param from URL"
  fi

  # 3c: has fallback default for param (source=, ref=, or inline default)
  # Accept: source = 'fallback', ref: 'fallback', params.set('ref','fallback'),
  # params.set('source','fallback'), or the ref/default pattern used in compare-competitors
  if grep -qE "source.*=.*['\"][^'\"]+['\"]|ref.*=.*['\"][^'\"]+['\"]|params\.(set|append)\(['\"]" "$file"; then
    pass "$name — has param fallback/default"
  else
    fail "$name — missing param fallback/default"
  fi
}

had_checkout=false
if [[ -d "$CHECKOUT_DIR" ]]; then
  for f in "$CHECKOUT_DIR"/checkout-*/*.html; do
    [[ -f "$f" ]] || continue
    had_checkout=true
    check_sik_helper "$(basename "$(dirname "$f")")/$(basename "$f")" "$f"
  done
  if [[ "$had_checkout" == "false" ]]; then
    info "No checkout helper HTML files found in $CHECKOUT_DIR"
  fi
else
  info "checkout dir not found, skipping"
fi

echo ""

# ----------------------------------------------------------
# CHECK 4 — No active flash-sale routes
# ----------------------------------------------------------
echo "--- Check 4: No active flash-sale routes ---"

FLASH_LINKS=$(grep -rlE "ship-it-kit-flash|/flash/" "$ROOT" --include="*.html" 2>/dev/null || true)
if [[ -n "$FLASH_LINKS" ]]; then
  fail "flash-sale route referenced in site:"
  echo "    Files: $(echo "$FLASH_LINKS" | tr '\n' ' ')"
else
  pass "No ship-it-kit-flash routes referenced"
fi

echo ""

# ----------------------------------------------------------
# CHECK 5 — Ship It Kit Lite out of scope
# ----------------------------------------------------------
echo "--- Check 5: Ship It Kit Lite — scope boundary ---"

SIK_LITE="$ROOT/ship-it-kit-lite/index.html"
if [[ -f "$SIK_LITE" ]]; then
  if grep -q "€19" "$SIK_LITE"; then
    pass "ship-it-kit-lite — shows €19 (Lite is separate product, out of scope)"
  else
    info "ship-it-kit-lite — €19 not found (may need review)"
  fi
  if grep -q "66928c03-2807-4c41-aa34-69cfdb6ae07a" "$SIK_LITE"; then
    fail "ship-it-kit-lite — uses Ship It Kit LS URL (should use Lite variant)"
  else
    pass "ship-it-kit-lite — does NOT use main Ship It Kit LS URL"
  fi
else
  info "ship-it-kit-lite not found (not yet created — OK)"
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
