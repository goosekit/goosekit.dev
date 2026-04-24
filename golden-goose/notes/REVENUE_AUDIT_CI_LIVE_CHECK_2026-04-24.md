# Block 56 — JS Param Forwarding Verification

**Date:** 2026-04-24
**Status:** ✅ PASS — No fixes needed

## Method

Static JS simulation: extracted the inline `<script>` from both checkout helpers and ran the URL params construction logic through Node.js without any browser navigation or network requests.

## Results

### checkout-hero
Input: \`/go/offline-pack/checkout-hero/?source=night_sprint_test&utm_source=night_sprint&utm_campaign=param_check&ref=block56\`

Generated LS URL:
\`\`\`
https://shipitstudio.lemonsqueezy.com/checkout/buy/f897713c-9cd2-4aaa-bd95-abd5ecd6b757?source=night_sprint_test&utm_source=night_sprint&utm_campaign=param_check&ref=block56
\`\`\`

- \`source\`: ✅ PASS — present exactly once
- \`utm_source\`: ✅ PASS — present exactly once
- \`utm_campaign\`: ✅ PASS — present exactly once
- \`ref\`: ✅ PASS — present exactly once
- LS product URL correct: ✅ f897713c-9cd2-4aaa-bd95-abd5ecd6b757

### checkout-bottom
Input: \`/go/offline-pack/checkout-bottom/?source=night_sprint_test&utm_source=night_sprint&utm_campaign=param_check&ref=block56\`

Generated LS URL:
\`\`\`
https://shipitstudio.lemonsqueezy.com/checkout/buy/f897713c-9cd2-4aaa-bd95-abd5ecd6b757?source=night_sprint_test&utm_source=night_sprint&utm_campaign=param_check&ref=block56
\`\`\`

- \`source\`: ✅ PASS — present exactly once
- \`utm_source\`: ✅ PASS — present exactly once
- \`utm_campaign\`: ✅ PASS — present exactly once
- \`ref\`: ✅ PASS — present exactly once
- LS product URL correct: ✅ f897713c-9cd2-4aaa-bd95-abd5ecd6b757

## Audit Script Output

\`scripts/audit_revenue_paths.sh\` — Block 50 + Block 51 combined: **126 passed, 0 failed**

## Notes

- Both helpers use \`params.toString()\` which appends all URL params to the LS checkout URL via \`window.location.replace(checkoutUrl + glue + params.toString())\`.
- No deduplication or filtering of params — all \`source\`, \`utm_source\`, \`utm_campaign\`, \`ref\` pass through intact.
- JS redirect fires on \`DOMContentLoaded\`; manual fallback link (\`data-manual-checkout-link\`) is present but does not carry params (expected for the manual fallback).
- No purchases, no checkout completion, no profile browsing used.
