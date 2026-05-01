# Refund Radar validation pack — 2026-05-01

Purpose: validate whether indie SaaS founders will send 10–30 churn/refund events in exchange for a concrete weekly retention report.

Public-posting guardrails:
- Do not claim this is a finished SaaS dashboard.
- Do not say Arthur built a full product or integrations yet.
- Say it is an early Goosekit experiment/manual-assisted report.
- Before posting to Reddit/HN/etc., check current community rules and adapt the angle.

## Best target

Founder with Stripe, Lemon Squeezy, or Paddle revenue who has at least a few refunds/cancellations and is unsure what to fix first.

## Buyer-intent queries

Use these to find exact-fit conversations before posting anywhere:

- `site:reddit.com/r/SaaS refund reasons churn cancelled users Stripe`
- `site:reddit.com/r/SideProject SaaS churn refunds cancellation reasons`
- `site:reddit.com/r/indiehackers refund requests churn SaaS`
- `"Lemon Squeezy" refund churn SaaS founder`
- `"Stripe" "cancellation reasons" SaaS founder`

## Contextual reply draft

Only use when someone is already discussing refunds, cancellations, churn reasons, onboarding friction, pricing objections, or failed payments.

> One small thing that helped me think about this: don’t start with a dashboard. Export the last 10–30 refund/cancellation/payment-failure rows and bucket the reasons first: setup friction, pricing objection, missing feature, unclear value, failed payment, support friction. Then pick one fix for the biggest bucket and one winback email.
>
> I’m testing a tiny Goosekit experiment around exactly this — a manual-assisted “weekly churn doctor” report from CSV exports, not a full analytics product yet: https://goosekit.dev/refund-radar/
>
> The useful output is basically: where money leaked, why, what to fix this week, and the winback email to send.

## Short social post draft

Needs channel-specific rule check before posting.

> I’m testing a small Goosekit experiment for indie SaaS founders with refunds/cancellations.
>
> The idea: instead of another analytics dashboard, send a weekly “churn doctor” report from a Stripe/Lemon Squeezy/Paddle CSV export.
>
> Input: 10–30 rows of refunds, cancellations, failed payments, or support notes.
> Output: reason buckets, the biggest leak, 3 retention fixes, and one winback email draft.
>
> It’s manual-assisted first, deliberately. If nobody wants the report, I won’t build OAuth or a dashboard.
>
> Sample: https://goosekit.dev/refund-radar/sample-report/

## DM / email brief

Subject: Quick churn/refund report from your last 10–30 events?

Hi — I’m testing Refund Radar, a small Goosekit experiment for indie SaaS retention.

If you have a few refunds/cancellations/failed payments, I can turn a small CSV export into a weekly-style action report: top reason buckets, the biggest money leak, 3 fixes, and one winback email.

No dashboard or integration needed for the first test. Stripe, Lemon Squeezy, Paddle, or a spreadsheet is fine.

Sample report: https://goosekit.dev/refund-radar/sample-report/

## Success criteria

- Win: at least one founder sends a real or anonymized export / asks for the report.
- Mixed: clicks, replies, or objections but no data shared.
- Lose: no relevant replies/clicks; change target or angle before building more.

## Tracking

Use a fresh row in `distribution_actions.csv` if/when a real public reply, post, or DM is sent. Suggested campaign label: `refund-radar-validation-2026-05`.
