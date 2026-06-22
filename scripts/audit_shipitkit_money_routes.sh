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
#   6. Ship It Kit setup-help page preserves structured request
#      routing, source attribution, and direct email fallback.
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
# CHECK 1 — Ship It Kit main page price state
# ----------------------------------------------------------
FLASH_ACTIVE="${SHIPITKIT_FLASH_SALE_ACTIVE:-0}"
if [[ "$FLASH_ACTIVE" == "1" ]]; then
  echo "--- Check 1: Ship It Kit main page — active €29 flash-sale price displayed ---"
else
  echo "--- Check 1: Ship It Kit main page — €49 displayed ---"
fi

SIK_FILE="$ROOT/ship-it-kit/index.html"
if [[ ! -f "$SIK_FILE" ]]; then
  fail "ship-it-kit/index.html missing"
else
  if [[ "$FLASH_ACTIVE" == "1" ]]; then
    if grep -q "€29" "$SIK_FILE"; then
      pass "ship-it-kit — displays €29 flash-sale price"
    else
      fail "ship-it-kit — missing €29 flash-sale price display"
    fi
    if grep -q '"price": "29"' "$SIK_FILE"; then
      pass "ship-it-kit JSON-LD price is 29"
    else
      fail "ship-it-kit JSON-LD price missing or not 29"
    fi
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
      if grep -q "Checkout opens after Lemon Squeezy shows €29" "$SIK_FILE" && ! grep -qE "/go/ship-it-kit/checkout-product-(hero|pricing|bottom|sticky)/" "$SIK_FILE"; then
        pass "ship-it-kit — pending €29 copy has no active product checkout CTAs"
      else
        fail "ship-it-kit — stale or unsafe €29 flash-sale copy found"
      fi
    else
      pass "ship-it-kit — no stale €29 flash-sale copy"
    fi
    if grep -q "product_hero_existing_repo" "$SIK_FILE" && \
       grep -q "decision_strip_existing_repo" "$SIK_FILE" && \
       grep -q "data-ph-event=\"ship_it_kit_setup_help_interest\"" "$SIK_FILE"; then
      pass "ship-it-kit — high-intent setup-help CTAs are measured"
    else
      fail "ship-it-kit — missing measured setup-help CTAs for existing-repo buyers"
    fi
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

  if grep -qE "pending_redirect|price verification|paid link is held|/ship-it-kit-quick-fit/" "$file"; then
    fail "$name — stale pending/quick-fit checkout gate still present"
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

PRODUCT_DECISION_CHECKOUT="$CHECKOUT_DIR/checkout-product-decision-strip/index.html"
if [[ -f "$PRODUCT_DECISION_CHECKOUT" ]]; then
  if grep -qiE '<meta[^>]+http-equiv=["'\'']refresh["'\''][^>]+shipitstudio\.lemonsqueezy\.com/checkout/buy' "$PRODUCT_DECISION_CHECKOUT"; then
    fail "checkout-product-decision-strip — raw Lemon Squeezy meta-refresh can bypass source preservation"
  else
    pass "checkout-product-decision-strip — no raw Lemon Squeezy meta-refresh"
  fi
fi

echo ""

# ----------------------------------------------------------
# CHECK 4 — Ship It Kit setup-help request path
# ----------------------------------------------------------
echo "--- Check 4: Ship It Kit setup-help — structured request route ---"

SETUP_HELP_FILE="$ROOT/ship-it-kit-setup-help/index.html"
if [[ ! -f "$SETUP_HELP_FILE" ]]; then
  fail "ship-it-kit-setup-help/index.html missing"
else
  if grep -q "/go/billing-reliability/setup-request/?source=shipit_setup_help_hero_packet" "$SETUP_HELP_FILE" && \
     grep -q "/go/billing-reliability/setup-request/?source=shipit_setup_help_packet" "$SETUP_HELP_FILE" && \
     grep -q "/go/billing-reliability/setup-request/?source=shipit_setup_help_production_saas" "$SETUP_HELP_FILE" && \
     grep -q "/go/billing-reliability/setup-request/?source=shipit_setup_help_bottom_packet" "$SETUP_HELP_FILE"; then
    pass "setup-help — structured request CTAs preserve Ship It Kit source"
  else
    fail "setup-help — missing structured setup-request source CTAs"
  fi

  if grep -q "data-ph-event=\"setup_help_request_clicked\"" "$SETUP_HELP_FILE" && \
     grep -q "data-ph-location=\"shipit_setup_help_packet\"" "$SETUP_HELP_FILE" && \
     grep -q "data-ph-location=\"shipit_setup_help_production_saas\"" "$SETUP_HELP_FILE"; then
    pass "setup-help — measured packet CTA present"
  else
    fail "setup-help — missing measured packet CTA"
  fi

  if grep -q "Turning a demo repo into a production SaaS" "$SETUP_HELP_FILE" && \
     grep -q "tenant or organization ids" "$SETUP_HELP_FILE" && \
     grep -q "Stripe checkout, signed webhook, customer portal" "$SETUP_HELP_FILE"; then
    pass "setup-help — production SaaS conversion scope is explicit"
  else
    fail "setup-help — missing production SaaS conversion scope"
  fi

  if grep -q "data-preserve-source-ref=\"true\"" "$SETUP_HELP_FILE" && \
     grep -q "source_ref" "$SETUP_HELP_FILE" && \
     grep -q "data-ph-source-ref" "$SETUP_HELP_FILE"; then
    pass "setup-help — preserves product-page source ref into setup request"
  else
    fail "setup-help — missing source_ref preservation from product page"
  fi

  measured_links=$(grep -c "data-ph-event=" "$SETUP_HELP_FILE" || true)
  measured_links_with_source_ref=$(grep "data-ph-event=" "$SETUP_HELP_FILE" | grep -c "data-preserve-source-ref=\"true\"" || true)
  if [[ "$measured_links" -gt 0 && "$measured_links" -eq "$measured_links_with_source_ref" ]]; then
    pass "setup-help — all measured links preserve product-page source ref"
  else
    fail "setup-help — measured links without source_ref preservation ($measured_links_with_source_ref/$measured_links)"
  fi

  if grep -q "posthog.capture(link.getAttribute('data-ph-event')" "$SETUP_HELP_FILE" && \
     grep -q "source_ref: link.getAttribute('data-ph-source-ref') || sourceRef" "$SETUP_HELP_FILE" && \
     grep -q "target_href: link.getAttribute('href') || null" "$SETUP_HELP_FILE"; then
    pass "setup-help — click capture includes source_ref and target_href"
  else
    fail "setup-help — click capture missing source_ref or target_href"
  fi

  if grep -q "/go/billing-reliability/setup-request/?source=shipit_setup_help_bottom_fallback_packet" "$SETUP_HELP_FILE" && \
     grep -q "data-ph-location=\"shipit_setup_help_bottom_fallback_packet\"" "$SETUP_HELP_FILE"; then
    pass "setup-help — bottom fallback routes through structured setup request"
  else
    fail "setup-help — bottom fallback missing structured setup-request route"
  fi

  SETUP_REQUEST_FILE="$ROOT/go/billing-reliability/setup-request/index.html"
  if [[ ! -f "$SETUP_REQUEST_FILE" ]]; then
    fail "billing setup request route missing"
  elif grep -q "ship_it_kit_setup_help" "$SETUP_REQUEST_FILE" && \
       grep -q "Ship It Kit setup help request" "$SETUP_REQUEST_FILE" && \
       grep -q "requestedPriceRange = params.get('price_range_eur')" "$SETUP_REQUEST_FILE" && \
       grep -q "priceRange = requestedPriceRange || (isShipItKit ? '199-plus' : '99-149')" "$SETUP_REQUEST_FILE" && \
       grep -q "sourceRef = params.get('source_ref')" "$SETUP_REQUEST_FILE" && \
       grep -q "Source ref: " "$SETUP_REQUEST_FILE" && \
       grep -q "setup_help_request_manual_click.*target_href: mailto" "$SETUP_REQUEST_FILE" && \
       grep -q "setup_help_request_mailto_opened.*target_href: mailto" "$SETUP_REQUEST_FILE" && \
       grep -q "setup_help_request_email_copy_clicked" "$SETUP_REQUEST_FILE" && \
       grep -q "setup_help_request_subject_copy_clicked" "$SETUP_REQUEST_FILE" && \
       grep -q "setup_help_request_gmail_clicked" "$SETUP_REQUEST_FILE" && \
       grep -q "setup_help_request_outlook_clicked" "$SETUP_REQUEST_FILE" && \
       grep -q "setup_help_request_form_started" "$SETUP_REQUEST_FILE" && \
       grep -q "setup_help_request_field_completed" "$SETUP_REQUEST_FILE" && \
       grep -q "setup_help_request_ready_to_send" "$SETUP_REQUEST_FILE" && \
       grep -q "setup_help_request_formspree_submit" "$SETUP_REQUEST_FILE" && \
       grep -q "setup_help_request_auto_mailto_suppressed" "$SETUP_REQUEST_FILE" && \
       grep -q "https://formspree.io/f/xblgwdqz" "$SETUP_REQUEST_FILE" && \
       grep -q 'name="request_packet"' "$SETUP_REQUEST_FILE" && \
       grep -q 'name="_next"' "$SETUP_REQUEST_FILE" && \
       grep -q "&source_ref=' + encodeURIComponent(sourceRef || source)" "$SETUP_REQUEST_FILE" && \
       grep -q "/go/billing-reliability/setup-request-sent/" "$SETUP_REQUEST_FILE" && \
       grep -q 'data-button-position="after_form"' "$SETUP_REQUEST_FILE" && \
       grep -q "data-copy-email" "$SETUP_REQUEST_FILE" && \
       grep -q "data-gmail-link" "$SETUP_REQUEST_FILE" && \
       grep -q 'data-request-field="blocker"' "$SETUP_REQUEST_FILE"; then
    pass "setup-request route — preserves Ship It Kit request context and source ref"
  else
    fail "setup-request route — missing Ship It Kit context, source ref, price range, mailto target_href capture, Formspree return, or webmail/manual email fallback"
  fi

  SETUP_REQUEST_SENT_FILE="$ROOT/go/billing-reliability/setup-request-sent/index.html"
  if [[ ! -f "$SETUP_REQUEST_SENT_FILE" ]]; then
    fail "billing setup request sent route missing"
  elif grep -q "setup_help_request_formspree_returned" "$SETUP_REQUEST_SENT_FILE" && \
       grep -q "setup_help_request_sent_route" "$SETUP_REQUEST_SENT_FILE" && \
       grep -q "price_range_eur" "$SETUP_REQUEST_SENT_FILE" && \
       grep -q "params.get('source_ref') || source" "$SETUP_REQUEST_SENT_FILE" && \
       grep -q "/ship-it-kit-setup-help/" "$SETUP_REQUEST_SENT_FILE"; then
    pass "setup-request sent route — tracks Formspree return and routes back to setup help"
  else
    fail "setup-request sent route — missing Formspree return tracking or setup-help return link"
  fi
fi

echo ""

# ----------------------------------------------------------
# CHECK 5 — Flash sale state
# ----------------------------------------------------------
FLASH_PAGE="$ROOT/ship-it-kit-flash/index.html"
if [[ "$FLASH_ACTIVE" == "1" ]]; then
  echo "--- Check 5: Flash sale is active checkout path ---"
  if [[ -f "$FLASH_PAGE" ]]; then
    if grep -q "Limited Time" "$FLASH_PAGE" && \
       grep -q "data-countdown-target=\"2026-04-30T23:59:59+02:00\"" "$FLASH_PAGE" && \
       grep -qE "/go/ship-it-kit/checkout-flash-(hero|bottom)/" "$FLASH_PAGE" && \
       ! grep -q "mailto:" "$FLASH_PAGE"; then
      pass "ship-it-kit-flash — active sale page links to flash checkout"
    else
      fail "ship-it-kit-flash — active sale page is missing checkout/end-state requirements"
    fi
  else
    fail "ship-it-kit-flash missing during active sale"
  fi
else
  echo "--- Check 5: Flash sale preview is not an active checkout path ---"
  FLASH_CHECKOUT_LINKS=$(grep -rlE "/go/ship-it-kit/checkout-flash|/flash/" "$ROOT" --include="*.html" 2>/dev/null || true)
  if [[ -n "$FLASH_CHECKOUT_LINKS" ]]; then
    fail "active flash checkout route referenced in site:"
    echo "    Files: $(echo "$FLASH_CHECKOUT_LINKS" | tr '\n' ' ')"
  else
    pass "No active flash checkout routes referenced"
  fi

  if [[ -f "$FLASH_PAGE" ]]; then
    if (grep -q "The checkout opens when the flash sale starts" "$FLASH_PAGE" || grep -q "checkout stays closed until Lemon Squeezy shows €29" "$FLASH_PAGE" || grep -q "Sale Ended" "$FLASH_PAGE") && \
       ! grep -qE "/go/ship-it-kit/checkout-flash|shipitstudio\.lemonsqueezy\.com/checkout/buy" "$FLASH_PAGE"; then
      pass "ship-it-kit-flash — inactive sale page, no live checkout"
    else
      fail "ship-it-kit-flash — not clearly inactive or links to checkout"
    fi
  else
    info "ship-it-kit-flash not found (OK before sale activation)"
  fi
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
