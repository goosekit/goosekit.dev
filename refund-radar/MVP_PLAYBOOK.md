# Refund Radar MVP Playbook

Refund Radar validates a direct-money SaaS pain: refunds, cancellations, failed payments, and churn reasons.

## Wedge

Do not start as a generic analytics product. Sell a **weekly churn doctor report**:

- what money leaked this week
- why users left or refunded
- which onboarding/pricing/support fix to ship
- which winback email to send

## First validation workflow

1. Ask for payment platform, monthly customer count, and the last 10–30 cancellation/refund reasons.
2. Import CSV manually or paste events into the report generator.
3. Group reasons into buckets: setup friction, missing feature, pricing objection, failed payment, no longer needed, unclear value.
4. Deliver 3 retention actions and one winback email.
5. Ask whether they would pay €9–€19/mo for continuous monitoring.

## Pricing hypothesis

- €9/mo: up to 100 customers, weekly churn report.
- €19/mo: up to 1k customers, cancellation reason capture + winback templates.
- €49/mo: segments, failed-payment recovery ideas, and team alerts.

## Avoid for now

- full Stripe OAuth before demand
- complex dashboards
- pretending churn prediction works with tiny datasets
- generic “AI insights” copy
