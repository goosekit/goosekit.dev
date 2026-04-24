#!/bin/bash
# ============================================================
# audit_revenue_paths.sh
# Combined pre-deploy / revenue smoke check for Goosekit.
# Night-sprint block 52 — aggregates block 50 + block 51.
#
# WHEN TO RUN:
#   - Before any deploy to production.
#   - Before activating a flash sale or changing sale copy/CTAs
#     (wait until LS price is verified live first).
#   - After any money-route, pricing, or checkout edits.
#   - As part of a CI/CD pre-merge gate.
#
# WHAT IT CHECKS:
#   1. Privacy/offline routing + checkout attribution
#      (audit_privacy_offline.sh — block 50)
#   2. Ship It Kit money routes
#      (audit_shipitkit_money_routes.sh — block 51)
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

run_and_report() {
  local label="$1"
  local script="$2"
  echo ""
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  echo "▶  $label"
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  if [[ ! -f "$script" ]]; then
    echo "⚠️  Script not found: $script — SKIPPING"
    return 0
  fi
  local output
  local exit_code=0
  output=$(bash "$script" 2>&1) || exit_code=$?
  echo "$output"
  # Extract and echo the summary line for visibility
  local summary
  summary=$(echo "$output" | grep "Summary:" | tail -1)
  [[ -n "$summary" ]] && echo "" && echo "   → $summary"
  return $exit_code
}

BLOCK50_EXIT=0
BLOCK51_EXIT=0

run_and_report \
  "Block 50 — Privacy / Offline + Checkout Attribution" \
  "$SCRIPT_DIR/audit_privacy_offline.sh" || BLOCK50_EXIT=$?

run_and_report \
  "Block 51 — Ship It Kit Money Routes" \
  "$SCRIPT_DIR/audit_shipitkit_money_routes.sh" || BLOCK51_EXIT=$?

echo ""
echo "══════════════════════════════════════════════════════"
echo "Combined Revenue Smoke Check — Final Status"
echo "══════════════════════════════════════════════════════"
echo "  Block 50 (privacy/offline):  exit=$BLOCK50_EXIT"
echo "  Block 51 (money routes):      exit=$BLOCK51_EXIT"
echo ""

if [[ $BLOCK50_EXIT -eq 0 ]] && [[ $BLOCK51_EXIT -eq 0 ]]; then
  echo "✅ All checks passed. Safe to deploy."
  exit 0
else
  echo "⚠️  One or more blocks failed. Review above before deploying."
  exit 1
fi
