# Goose Monitor MVP Playbook

Goose Monitor should validate paid demand for **actionable weekly market reports** before building a full SaaS dashboard.

## Positioning

Do not sell “competitor monitoring” generically. Sell: **competitor changes turned into SEO and distribution actions for indie SaaS teams**.

The wedge is small teams that cannot justify enterprise competitive-intelligence tools and do not want another noisy dashboard.

## First paid workflow

1. Ask for a brief: site, 2–3 competitors, and one growth question.
2. Run `scripts/goose_monitor_report.py` against the watched URLs.
3. Manually verify important claims.
4. Add judgment: which page/CTA/reply should be shipped this week?
5. Send the report as a Markdown/PDF/email deliverable.
6. Ask whether the founder would pay for 3 weekly reports.

## Pricing tests

- First report: €49 one-time.
- Three-report validation pack: €99.
- Later SaaS: €19/mo for one project and 3 competitors; €49/mo for 3 projects or daily checks.

## Technical scope now

Keep it deliberately boring:

- snapshot watched pages
- detect changed title/meta/H1/text/intent keywords
- emit Markdown action reports
- no auth, no billing, no dashboard until reports get demand

## What to avoid

- competing with Crayon/Klue/Kompyte on enterprise competitive intelligence
- building a generic Visualping clone
- adding charts before the action report is useful
- pretending automated recommendations are reliable before manual QA proves the pattern
