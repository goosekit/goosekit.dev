#!/bin/bash
# ============================================================
# audit_revenue_paths.sh
# Goosekit pre-deploy smoke check for the current free-tools-first contract.
#
# Default mode, 2026-06-28:
#   Goosekit's primary surface is free browser tools. This audit now verifies
#   that the core tool pages stay free/local/no-signup and that the SEO
#   workflow pages are present, linked, and indexed in the sitemap.
#
# Legacy revenue audits:
#   Set GOOSEKIT_LEGACY_REVENUE_AUDIT=1 to additionally run the historical
#   Ship It Kit / checkout / billing route audits.
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="${1:-$(cd "$SCRIPT_DIR/.." && pwd)}"

run_and_report() {
  local label="$1"
  shift
  echo ""
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  echo "▶  $label"
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  "$@"
}

FREE_EXIT=0
LEGACY_EXIT=0

run_and_report \
  "Free tools first contract" \
  python3 "$SCRIPT_DIR/audit_free_tools_first.py" || FREE_EXIT=$?

if [[ "${GOOSEKIT_LEGACY_REVENUE_AUDIT:-0}" == "1" ]]; then
  echo ""
  echo "Legacy revenue audits enabled via GOOSEKIT_LEGACY_REVENUE_AUDIT=1"
  for script in "$SCRIPT_DIR/audit_privacy_offline.sh" "$SCRIPT_DIR/audit_shipitkit_money_routes.sh"; do
    if [[ -f "$script" ]]; then
      run_and_report "$(basename "$script")" bash "$script" "$ROOT" || LEGACY_EXIT=$?
    else
      echo "Skipping missing legacy audit: $script"
    fi
  done
else
  echo ""
  echo "Legacy revenue audits skipped by default under free-tools-first."
  echo "Set GOOSEKIT_LEGACY_REVENUE_AUDIT=1 to run Ship It Kit / checkout checks."
fi

echo ""
echo "══════════════════════════════════════════════════════"
echo "Goosekit Smoke Check — Final Status"
echo "══════════════════════════════════════════════════════"
echo "  Free tools first: exit=$FREE_EXIT"
echo "  Legacy revenue:   exit=$LEGACY_EXIT"
echo ""

if [[ $FREE_EXIT -eq 0 ]] && [[ $LEGACY_EXIT -eq 0 ]]; then
  echo "All required checks passed."
  exit 0
fi

echo "One or more required checks failed."
exit 1
